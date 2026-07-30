# 第 1 篇 总览：七层全景与端到端路径追踪

AudioReach 是高通新一代音频软件架构。和老的 hardware/audio + adsp 私有协议相比，
它最大的变化是：**用一张“图”（Graph）描述音频用例，把处理逻辑从代码里搬到数据里。**

对音频工程师来说，理解 AudioReach 的关键不是记住每个类名，而是搞清一条数据从
应用到 DSP 要穿过哪几层、每层负责把“抽象”降一档，最终变成 DSP 上一张可运行的图。

## 为什么是“图”

一个音频用例（比如“深缓冲播放到扬声器”）本质上是一串处理模块的连接：
解码 → 后处理（均衡/音量/限幅）→ 重采样 → 硬件端点。AudioReach 把这串连接抽象成：

- **Module（模块）**：一个处理单元，有若干输入/输出端口和一组可标定参数。
- **SubGraph（子图）**：一组模块 + 连接，是可复用、可独立起停的最小编排单位。
- **Container（容器）**：DSP 上承载子图运行的线程/调度/缓冲边界。
- **Graph（图）**：若干子图拼起来的完整用例。

图的**拓扑**和**标定参数**不写死在代码里，而是放在 ACDB 数据库中。上层只需说
“我要 stream type = DEEP_BUFFER，device = SPEAKER”，下面各层就能查出对应的图并
把它在 DSP 上跑起来。这就是所谓 **data-driven**。

## 七层全景

```
Android AudioFlinger / audio HAL
        │  (HIDL/AIDL HwBinder，可选)
┌───────▼──────────────────────────────────────── 用户空间 (APPS) ───────────┐
│ PAL   平台抽象层：统一 pal_stream_* API                                      │
│   Pal.cpp → Stream(PCM/Compress/SoundTrigger…)                             │
│            ├─ ResourceManager  选设备 / 定用例 / 并发 / 路由                  │
│            ├─ Device           Speaker/Headset/BT/USB… + SpeakerProtection  │
│            └─ Session          落到 ALSA(pcm/mixer) 或 AGM API               │
├───────────────────────── ALSA(pcm/mixer) + AGM plugin ─────────────────────┤
│ AGM   会话/图/设备生命周期编排                                                │
│   agm.c → session_obj.c → graph.c → graph_module.c                         │
├───────────────────────────────── gsl_* API ───────────────────────────────┤
│ GSL   图求解 / 子图 / 共享内存 / 数据通路           ← 查询 →  ACDB (图+标定)  │
│   gsl_main → gsl_graph → gsl_subgraph → gsl_datapath / gsl_shmem_mgr        │
├───────────────────────────── GPR packet (opcode+payload) ─────────────────┤
│ GPR   通用包路由，按 domain/port 跨处理器寻址                                 │
└───────────────────────────────────┬───────────────────────────────────────┘
   audio-kernel-ar (ASoC / glink / dsp) 内核态承载 GPR 传输与数据搬运
                                     │
┌────────────────────────────────────▼──────────────── DSP (SPF) ───────────┐
│ APM        接收 GPR 命令，按图 open/close/connect                            │
│ Container  gen_cntr / spl_cntr / olc / wear_cntr：线程/调度/缓冲            │
│ Module     modules/audio, processing, cmn：真正的算法                        │
│ AMDB       动态加载模块；HW-EP 对接编解码/I2S/Slimbus                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

每一层做的事情可以概括成一句：

- **PAL**：把“我要放音乐”翻译成“打开一个 stream，绑定一个 device，跑一个 session”。
- **AGM**：把 PAL 的 session/device 请求，映射成 GSL 能理解的“图”操作。
- **GSL + ACDB**：把图的名字变成实际的子图/模块拓扑与标定数据（真正的 graph solver）。
- **GPR**：把这些操作打成包，负责“送到哪个处理器的哪个模块”。
- **SPF**：在 DSP 上把包变成运行中的容器和模块，真正处理 PCM 数据。

## 端到端路径追踪：一次 PCM 播放

下面用 `StreamPCM`（深缓冲播放）追一条最典型的路径，代码位置都可点击。

### 1) 打开：`pal_stream_open`

入口在 `Pal.cpp:176`。它做三件事：拿到
`ResourceManager` 单例、用工厂造出具体 Stream、调用 `open()`。

```cpp
// Pal.cpp
rm = ResourceManager::getInstance();
s  = Stream::create(attributes, devices, no_of_devices, ...);  // 工厂
status = s->open();
notify_concurrent_stream(sAttr.type, sAttr.direction, true);   // 登记并发
```

`Stream::create`（`Stream.cpp:75`）
根据 `attributes->type` 分派到具体子类：PCM 类用例（LOW_LATENCY / DEEP_BUFFER /
VOIP / VOICE_CALL / LOOPBACK…）走 `StreamPCM`，压缩走 `StreamCompress`，
语音唤醒走 `StreamSoundTrigger`，等等。

### 2) 建会话与设备：`StreamPCM` 构造

在 `StreamPCM.cpp:117` 附近，
构造函数就把两个核心协作对象建好：

```cpp
session = Session::makeSession(rm, sattr);                 // 会话（落 ALSA/AGM）
for (...) dev = Device::getInstance(&dattr[i], rm);        // 设备（可复用单例）
rm->registerStream(this);                                  // 向 RM 登记
```

这里已经能看出 PAL 内部的三角关系：**Stream 是用例主体，Session 负责“怎么下发”，
Device 负责“下发到哪个硬件”，ResourceManager 在中间做仲裁。**

### 3) 启动：`pal_stream_start` → `StreamPCM::start`

启动时按方向（Rx/Tx）先起设备、再准备并启动会话，全程持 `rm->lockGraph()`
串行化图操作（`StreamPCM.cpp:471-503`）：

```cpp
rm->lockGraph();
mDevices[i]->start();      // 起硬件端点
session->prepare(this);    // 准备图
session->start(this);      // 启动图（真正把命令下到 AGM/GSL/DSP）
rm->unlockGraph();
```

### 4) 会话向下：Session → AGM → GSL → GPR → DSP

`session->start()` 最终走到 `SessionAlsaPcm`，它通过 tinyALSA 打开 PCM 设备并写
mixer control。挂在 ALSA 之下的是 **AGM plugin**（`agm_pcm_plugin.c` /
`agm_mixer_plugin.c`），plugin 把请求转给 **AGM 服务**（`agm.c` →
`session_obj.c` → `graph.c`）。AGM 再调用 **GSL** 的 `gsl_*` API。

GSL 是真正的 **graph solver**：它去 **ACDB** 查出该用例的子图/模块拓扑与标定，
构建出图（`gsl_graph` / `gsl_subgraph`），然后把 open/connect/start/set-param 等
操作通过 **GPR** 打包。GPR 按 `domain_id`（哪个处理器）+ `port`（哪个服务/模块）
路由，经内核 glink 送到 DSP。

DSP 侧的 **APM** 收到 GPR 命令，按图实例化 **Container**，在容器里加载并连接
**Module**，图就“活”了。此后 PCM 数据经共享内存在 APPS 与 DSP 间来回搬运。

### 端到端时序（简化）

```
App/HAL   PAL(Pal/Stream)   Session   AGM        GSL         GPR      SPF(DSP)
  │  open      │              │        │           │           │         │
  ├───────────►│ create+open  │        │           │           │         │
  │            ├─ makeSession─►│        │           │           │         │
  │            ├─ getInstance(Device)   │           │           │         │
  │  start     │              │        │           │           │         │
  ├───────────►│ dev.start    │        │           │           │         │
  │            ├─ session.prepare/start │           │           │         │
  │            │              ├─ALSA/AGM plugin────►│           │         │
  │            │              │        ├ graph_open ├─gsl_open─►│         │
  │            │              │        │           ├ query ACDB │         │
  │            │              │        │           ├──GPR pkt──►│ APM     │
  │            │              │        │           │           ├────────►│ open graph
  │            │              │        │           │           │         ├ Container+Module
  │  write     │              │        │           │           │         │
  ├───────────►│ session.write├─ shared memory ────────────────────────► │ 数据处理
```

## 各仓库速览（后续每篇的落点）

| 仓库 | 你会在这里找到 |
|------|----------------|
| `audioreach-pal` | `Pal.cpp`、`stream/`、`session/`、`device/`、`resource_manager/`、`ipc/` |
| `agm` | `service/src/agm.c`、`session_obj.c`、`graph.c`；`plugins/tinyalsa` |
| `audioreach-graphservices/gsl` | `gsl_main.c`、`gsl_graph.c`、`gsl_subgraph.c`、`gsl_datapath.c` |
| `audioreach-graphservices/acdb` | ACDB 解析、图/标定数据接口 |
| `audioreach-engine/gpr` | `core/`、`datalinks/gpr_lx`（Linux datalink） |
| `audioreach-engine/fwk/spf` | `apm/`、`containers/`、`modules/`、`amdb/` |
| `audio-kernel-ar` | `asoc/`、`dsp/`、`ipc/`、`soc/` |

## 小结

- AudioReach 的核心思想是**图驱动**：用例 = 图，拓扑与标定放在 ACDB，代码只做编排。
- 从上到下，每层把抽象降一档：**用例 → 会话/设备 → 图 → 子图/模块 → GPR 包 → 容器/模块实例**。
- PAL 是对上的统一门面，AGM/GSL/ACDB 是“图的编译器与链接器”，GPR 是“传输层”，
  SPF 是“运行时”。

下一篇进入 PAL：`pal_stream_*` 的语义、Stream 家族的分工与完整生命周期。
