# 第 2 篇 PAL（上）：入口、Stream 家族与生命周期

PAL（Platform Abstraction Layer）是 AudioReach 对上的统一门面。audio HAL 不再直接
和 ADSP 打交道，而是调用一组 `pal_stream_*` C API。PAL 内部再把它翻译成
Stream / Session / Device 三方协作，向下对接 AGM/GSL。

这一篇讲清两件事：**`pal_stream_*` API 的语义**，以及 **Stream 家族的分工与生命周期**。

## 一、对外 API：`pal_stream_*`

所有对外接口都在 [Pal.cpp](../audioreach-pal/Pal.cpp) 里，是一层很薄的转发：校验参数
→ 取 `ResourceManager` 单例 → 转调 `Stream` 对象的虚方法。核心 API：

| API | 作用 | 落点 |
|-----|------|------|
| `pal_stream_open` | 创建并打开一路流 | `Stream::create` + `s->open()` |
| `pal_stream_close` | 关闭并销毁 | `s->close()` + `delete s` |
| `pal_stream_start` / `stop` | 起停用例（起停图与设备） | `s->start()` / `s->stop()` |
| `pal_stream_write` / `read` | 送/取 PCM 数据 | `s->write()` / `s->read()` |
| `pal_stream_set_param` / `get_param` | 设置/查询参数（如后处理） | `s->setParameters()` |
| `pal_stream_set_volume` / `set_mute` | 音量/静音 | `s->setVolume()` / `s->mute()` |
| `pal_stream_pause` / `resume` / `drain` / `flush` | 播放控制 | 对应虚方法 |
| `pal_stream_set_device` | 运行中切设备（路由） | 见第 3 篇 |

### open 的三步（回顾并展开）

[Pal.cpp:176](../audioreach-pal/Pal.cpp#L176)：

```cpp
rm = ResourceManager::getInstance();                 // 1. 全局仲裁者
s  = Stream::create(attributes, devices, ...);        // 2. 工厂造具体子类
status = s->open();                                    // 3. 打开（建 session/device）
notify_concurrent_stream(sAttr.type, sAttr.direction, true);  // 登记并发用例
rm->initStreamUserCounter(s);                          // 引用计数（多客户端共享）
*stream_handle = reinterpret_cast<uint64_t*>(s);       // 句柄就是对象指针
```

注意 `stream_handle` 本质就是 `Stream*`。close 时会 `reinterpret_cast` 回来，
所以句柄的合法性由 `ResourceManager` 的活跃流表（`isActiveStream`）来兜底校验
（[Pal.cpp:278](../audioreach-pal/Pal.cpp#L278)）。

### 决定用例的入参：`pal_stream_attributes`

[PalDefs.h:824](../audioreach-pal/inc/PalDefs.h#L824)：

```cpp
struct pal_stream_attributes {
    pal_stream_type_t       type;             // 用例类型：决定走哪个 Stream 子类
    pal_stream_info_t       info;
    pal_stream_flags_t      flags;
    pal_stream_direction_t  direction;        // RX(播放)/TX(录音)/双向
    struct pal_media_config in_media_config;  // 采样率/位宽/通道
    struct pal_media_config out_media_config;
};
```

`type` 是最关键的字段：它既决定 PAL 内部实例化哪个 Stream 子类，也是后面
**ACDB 查图**的主键之一（type + device + 采样率等构成用例的 Graph Key Vector）。
`modifier_kv`（[PalDefs.h:834](../audioreach-pal/inc/PalDefs.h#L834)）则用于在默认
拓扑之上做微调（比如指定某种后处理变体）。

## 二、Stream 家族

`Stream` 是抽象基类（[Stream.h:179](../audioreach-pal/stream/inc/Stream.h#L179)），
定义了整套用例生命周期的纯虚接口：

```cpp
// Stream.h（节选）
virtual int32_t open()  = 0;
virtual int32_t close() = 0;
virtual int32_t start() = 0;
virtual int32_t stop()  = 0;
virtual int32_t prepare() = 0;
virtual int32_t write(struct pal_buffer *buf) = 0;
virtual int32_t read (struct pal_buffer *buf) = 0;
virtual int32_t setVolume(struct pal_volume_data *volume) = 0;
virtual int32_t setParameters(uint32_t param_id, void *payload) = 0;
virtual int32_t ssrDownHandler() = 0;   // SSR（DSP 子系统重启）处理
virtual int32_t ssrUpHandler()   = 0;
```

基类持有三样公共状态：

```cpp
struct pal_stream_attributes*         mStreamAttr;   // 用例属性
static std::shared_ptr<ResourceManager> rm;          // 全局仲裁者
// + Session* session、std::vector<std::shared_ptr<Device>> mDevices（在具体子类）
```

### 工厂分派

`Stream::create`（[Stream.cpp:75](../audioreach-pal/stream/src/Stream.cpp#L75)）按
`type` 分派：

| Stream 子类 | 覆盖的用例类型 |
|-------------|----------------|
| `StreamPCM` | LOW_LATENCY / DEEP_BUFFER / SPATIAL / GENERIC / VOIP / PCM_OFFLOAD / VOICE_CALL / LOOPBACK / ULL / PROXY / RAW / VOICE_RECOGNITION |
| `StreamCompress` | COMPRESSED（offload 解码） |
| `StreamSoundTrigger` | VOICE_UI（语音唤醒/热词） |
| `StreamInCall` | VOICE_CALL_RECORD / VOICE_CALL_MUSIC（通话中录/放） |
| `StreamNonTunnel` | NON_TUNNEL（纯 DSP 转码，不接硬件端点） |
| `StreamACD` | ACD（声学上下文检测） |
| `StreamHaptics` | HAPTICS（振动） |
| `StreamUltraSound` / `StreamSensorPCMData` / `StreamContextProxy` / `StreamCommonProxy` | 超声、传感器 PCM、上下文代理等 |

对音频工程师来说，**90% 的普通播放/录音都落在 `StreamPCM`**；offload 音乐在
`StreamCompress`；语音唤醒是完全不同的一条低功耗路径（`StreamSoundTrigger`，第 8 篇
会再提它和 DSP 的 detection 引擎如何配合）。

## 三、生命周期（以 StreamPCM 为例）

一路流的完整生命：**construct → open → start → (write/read/setParam)\* → stop → close**。

```
                 ┌──────────────── mStreamMutex 保护每步 ─────────────────┐
create ─► ctor: makeSession + getInstance(Device) + rm->registerStream
   │
open   ─► session->open(this)          // 建图（尚未起硬件）
   │
start  ─► lockGraph
         ├─ Device.start()             // Rx: 先起硬件端点
         ├─ session->prepare(this)
         ├─ session->start(this)       // 真正把图起到 DSP
         └─ unlockGraph
   │
write  ─► session->write(buf)          // 数据经共享内存到 DSP
   │
stop   ─► session->stop + Device.stop
   │
close  ─► session->close + 释放 Device 引用 + rm->deregisterStream
```

### construct：建立三角关系

[StreamPCM.cpp:117](../audioreach-pal/stream/src/StreamPCM.cpp#L117)：

```cpp
session = Session::makeSession(rm, sattr);            // 会话：决定“怎么下发”
for (int i = 0; i < no_of_devices; i++)
    dev = Device::getInstance(&dattr[i], rm);         // 设备：单例，可跨流复用
rm->registerStream(this);                             // 登记到活跃流表
```

`Device::getInstance` 是**单例**语义——同一个物理设备（如扬声器）被多路流共享，
所以设备是引用计数管理的，这直接影响并发路由（第 3 篇详解）。

### start：方向决定顺序

[StreamPCM.cpp:471-503](../audioreach-pal/stream/src/StreamPCM.cpp#L471-L503)：

- **RX（播放）**：先 `Device.start()` 起硬件端点，再 `session->prepare/start` 起图。
- **TX（录音）**：见 [StreamPCM.cpp:514+](../audioreach-pal/stream/src/StreamPCM.cpp#L514)，
  同样在 `lockGraph` 下串行化。

整段用 `rm->lockGraph()` / `unlockGraph()` 包住，是因为**图操作是全局串行资源**：
多路流并发起停时，底层 GSL/DSP 的图连接必须串行以避免拓扑竞争。这把锁是 PAL
并发模型的核心，后面讲 ResourceManager 时会再看到它。

### write/read：数据面

`pal_stream_write`（[Pal.cpp:438](../audioreach-pal/Pal.cpp#L438)）直接转
`s->write(buf)`，`pal_buffer`（[PalDefs.h:854](../audioreach-pal/inc/PalDefs.h#L854)）
携带数据指针、大小、时间戳与 metadata。控制面（open/start/setParam）走 mixer control
+ AGM/GSL，**数据面走共享内存**——这条区分贯穿整个 AudioReach，写代码时要时刻分清
自己在操作控制面还是数据面。

### SSR：不可忽视的一环

DSP 是独立子系统，可能崩溃重启（SSR，SubSystem Restart）。每个 Stream 都实现
`ssrDownHandler` / `ssrUpHandler`：DOWN 时缓存当前状态（如 `STREAM_STARTED`）、
释放底层资源；UP 时按缓存状态自动恢复。前一篇 start 里那段 `-ENETRESET` +
`cachedState = STREAM_STARTED` 的处理（[StreamPCM.cpp:481](../audioreach-pal/stream/src/StreamPCM.cpp#L481)）
就是为 SSR 服务：**对 HAL 返回成功，PAL 内部记住状态，等 DSP 起来再补起图。**

## 小结

- `pal_stream_*` 是一层薄转发，真正的生命周期逻辑在 Stream 子类里。
- `type` 决定 Stream 子类，也参与后续 ACDB 查图；普通播放/录音在 `StreamPCM`。
- Stream 在构造时就绑好 Session（怎么下发）和 Device（下发到哪），由
  ResourceManager 登记与仲裁。
- 图操作全局串行（`lockGraph`）；控制面走 mixer/AGM，数据面走共享内存；SSR 靠
  状态缓存 + 自动恢复。

下一篇进入 PAL 的“大脑”——ResourceManager 的路由/并发/用例决策，以及 Device 抽象
（含 SpeakerProtection、BT/USB 等特殊设备）。
