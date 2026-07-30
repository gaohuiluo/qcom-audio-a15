# 第 8 篇 SPF/DSP：APM、Container、Module 与 AMDB

GPR 把 `APM_CMD_GRAPH_OPEN` 送到了 DSP。终点到了——**SPF（Signal Processing Framework）**
是 DSP 侧的音频运行时。前面所有层的努力，都是为了在这里把一张“描述出来的图”变成
“运行中的模块”。

SPF 有三个核心角色：**APM**（图管理器，接命令、建图）、**Container**（承载图运行的
线程/调度单元）、**Module**（真正处理 PCM 的算法）。加上 **AMDB**（模块数据库）负责
把模块加载进来。

## 一、APM：DSP 侧的图管理器

APM（Audio Processing Manager，`fwk/spf/apm/`）
是 DSP 上第一个收到 GPR 命令的服务。它在 GPR 注册一个固定 port，处理一整套图命令
（`apm_api.h`）：

```c
#define APM_CMD_GRAPH_OPEN      0x01001000   // 建图：创建容器、模块、连接
#define APM_CMD_GRAPH_PREPARE   ...          // 准备
#define APM_CMD_GRAPH_START     ...          // 启动数据处理
#define APM_CMD_GRAPH_STOP / FLUSH / SUSPEND / CLOSE
#define APM_CMD_SET_CFG         ...          // 设参数/标定
```

这套命令与第 5 篇 AGM `graph.c` 里的 `gsl_ioctl(GSL_CMD_START/PREPARE/...)` **一一对应**——
GSL 的 GSL_CMD_* 经过打包，到 DSP 就成了 APM_CMD_*。

### 命令时序器：APM 的核心

APM 处理命令不是一步到位，而是走一个**命令时序器**（`apm_cmd_sequencer.c`，
`apm_cmd_sequencer.c:423`）。
以 `APM_CMD_GRAPH_OPEN` 为例，APM 要按顺序完成一串子步骤：

```
APM_CMD_GRAPH_OPEN 到达
  ├─ 解析 payload：子图、容器、模块、连接、配置（GSL 打包的那堆）
  ├─ 为每个容器创建 Container 实例（按容器类型选 gen/spl/olc/wear）
  ├─ 在容器内创建 Module 实例（通过 AMDB 加载 CAPI 模块）
  ├─ 按连接关系连好模块间、容器间的数据端口
  └─ 回 GPR 响应（带 token）给 GSL
```

为什么要时序器？因为建图涉及多容器、多模块、跨容器连接，且可能跨多个处理器（MDF），
必须**分阶段、可回滚**地推进。时序器就是这套状态机。

## 二、Container：图运行的“执行引擎”

**子图不会自己运行，它需要一个容器来承载。** Container 提供线程、调度、缓冲边界。
一个容器管理一到多个模块，容器之间通过数据队列连接。

`fwk/spf/containers/` 提供了四种容器，
针对不同用例特性：

| 容器 | 目录 | 定位 |
|------|------|------|
| **GEN_CNTR**（通用容器） | `gen_cntr/` | 最常用。硬件端点、编解码、常规处理，帧驱动 |
| **SPL_CNTR**（专用/特殊容器） | `spl_cntr/` | 低时延、信号驱动的处理路径（如某些实时后处理） |
| **OLC**（Offload Container） | `olc/` | 跨处理器 offload：本地容器代理远端（如 CDSP）子图 |
| **WEAR_CNTR** | `wear_cntr/` | 穿戴设备场景的裁剪容器 |

**为什么要分容器类型？** 不同用例对调度、时延、缓冲的要求差别很大。播放音乐可以帧
驱动、缓冲大、省电（GEN_CNTR）；某些实时链路要信号驱动、低时延（SPL_CNTR）；而跨核
子图需要一个本地代理来收发数据（OLC）。**容器类型决定了子图“怎么被调度和缓冲”。**

### OLC 与 MDF 呼应

第 6/7 篇说一张图的子图可以横跨处理器。落到 DSP 就是：主处理器上的 OLC 容器
（`containers/olc/`）作为远端子图的
本地代理——它在本地看起来是个普通容器，实际把数据/命令通过 GPR 转发给另一处理器上
真正运行该子图的容器。上层图逻辑因此无需关心物理分布。

## 三、Module：真正干活的算法

Module 是处理单元。AudioReach 用统一的 **CAPI（Common Audio Processing Interface）**
封装所有模块（`interfaces/module/capi/capi.h`），
无论内建还是第三方，都实现同一个 vtable：

```c
struct capi_vtbl_t {
    capi_err_t (*process)(capi_t*, capi_stream_data_t *input[], capi_stream_data_t *output[]); // 处理数据
    capi_err_t (*set_param)(capi_t*, uint32_t param_id, ...);   // 设参数（对应上层 TKV/标定）
    capi_err_t (*get_param)(capi_t*, uint32_t param_id, ...);
    capi_err_t (*set_properties)(capi_t*, capi_proplist_t*);    // 设属性（媒体格式、端口等）
    capi_err_t (*get_properties)(capi_t*, capi_proplist_t*);
    capi_err_t (*end)(capi_t*);                                 // 销毁
};
// 外加静态入口：
capi_get_static_properties_f / capi_init_f   // 查询静态属性 + 初始化实例
```

对音频工程师来说，这就是最熟悉的地方——**一个模块 = 一个 CAPI 实现**：

- `process()`：核心。输入缓冲 → 算法 → 输出缓冲。容器每帧调它。
- `set_param(param_id, ...)`：上层一路传下来的参数最终落到这里。第 4 篇 PayloadBuilder
  拼的那个 payload，第 6 篇 ACDB 里的标定，最后都变成某个 `param_id` + 结构体，进这个函数。
- `set_properties()`：告诉模块输入输出媒体格式、端口数等。

### 模块家族

`modules/` 下是内建模块，音频工程师一眼就懂：

| 类别 | 目录 | 例子 |
|------|------|------|
| 编解码 | `modules/audio/` | `pcm_decoder`、`pcm_encoder` |
| 后处理 | `modules/processing/` | `volume_control`、`gain_control`、`PoplessEqualizer`、`bassboost`、`Virtualizer`、`shoebox_reverb`、`channel_mixer`、`resamplers`、`filters` |
| 公共 | `modules/cmn/` | 通用工具模块 |

一条“深缓冲播放 + 均衡 + 音量”的图，在 DSP 里就是 `PoplessEqualizer` →
`volume_control` → 硬件端点模块 这样一串 CAPI 实例，被 GEN_CNTR 每帧依次 `process`。

### 硬件端点（HW-EP）

图的尽头是硬件端点模块（HW-EP），它对接物理接口：I2S、Slimbus、TDM、CodecDMA 等。
HW-EP 一端是图内的数据端口，另一端是编解码器/DMA。第 3 篇 PAL 的 Device、`getDeviceEpName`
算出的后端名，最终对应的就是 DSP 里这个 HW-EP 模块的配置。

## 四、AMDB：模块从哪来

APM 建图时要“创建某个 module_id 的实例”，谁负责把对应的 CAPI 代码找出来、加载、给出
`capi_init`？——**AMDB（AudioReach Module Database，`fwk/spf/amdb/`）**。

- **静态模块**（`amdb_static.h` / `amdb_autogen_def.h`）：编译进 SPF 镜像的内建模块，
  AMDB 里有一张 module_id → 入口函数的表，直接查。
- **动态模块**（`amdb_parallel_loader.h` / `amdb_thread.h`）：以 `.so` 形式存在的第三方
  或可选模块，用到时才从文件系统加载（`dlopen` 类机制），拿到 `capi_get_static_properties`
  和 `capi_init`。这与第 6 篇 GSL 的 `gsl_dynamic_module_mgr.c` 是同一件事的两端：GSL 在
  APPS 侧登记动态模块信息，AMDB 在 DSP 侧真正加载。
- **offload 加载**（`amdb_offload_utils.h`）：为跨处理器场景加载远端模块。

这套设计让 AudioReach 的模块集**可扩展**：加一个新算法，实现 CAPI、注册到 AMDB、在 ACDB
里把它编进某个用例的图，就能上线——**框架代码一行不用改**。

## 五、把整条链路合起来看

```
GSL(APPS)──GPR──►APM(DSP)
                  │ apm_cmd_sequencer 处理 GRAPH_OPEN
                  ├─ 建 Container（gen/spl/olc/wear）
                  │     └─ 建 Module（AMDB 加载 CAPI 实例）
                  │            └─ set_properties / set_param（媒体格式+标定+TKV）
                  ├─ 连接模块端口、容器队列
                  └─ GRAPH_START → 容器线程开始每帧调 module->process
                                        │
   共享内存 ◄──── HW-EP ◄── volume ◄── EQ ◄── decoder ◄── 数据(来自APPS共享内存)
```

数据流：APPS 写入的 PCM 放在共享内存（第 6 篇），DSP 容器线程被调度，把数据依次喂给
链上每个模块的 `process()`，最后经 HW-EP 出到编解码器；录音方向相反。

## 小结

- SPF 是 DSP 侧运行时：APM 接 GPR 命令建图，Container 承载子图运行，Module 是算法本体。
- APM 用命令时序器分阶段、可回滚地处理 GRAPH_OPEN 等命令，与 GSL 的 GSL_CMD_* 一一对应。
- 四种 Container（GEN/SPL/OLC/WEAR）按用例的调度/时延/缓冲/跨核特性分工；OLC 是跨处理器
  子图的本地代理，呼应 MDF。
- Module 全部实现统一的 CAPI vtable（process/set_param/set_properties…）；上层的参数和
  标定最终都落到 `set_param`。
- AMDB 负责加载模块（静态查表 / 动态 dlopen / offload），与 GSL 动态模块管理器两端配合，
  让模块集可扩展、框架不改码。

下一篇（收尾）：内核 audio-kernel-ar 如何承载 GPR 的跨核传输与共享内存数据搬运，把
用户态与 DSP 真正连起来。
