# 第 4 篇 PAL Session 与 IPC：如何落到 ALSA

前三篇讲了 PAL 对上的门面（Stream）、决策大脑（ResourceManager）、硬件抽象（Device）。
这一篇看**最后一公里**：Session 如何把这些决策变成实际的 ALSA 操作，最终跨过用户空间
边界进入 AGM。这是 PAL 与下层的真正接缝。

## 一、Session 家族与分派

`Session::makeSession`（`Session.cpp`）按流类型
造出具体会话：

```cpp
switch (sAttr->type) {
    case PAL_STREAM_COMPRESSED:  s = new SessionAlsaCompress(rm); break;  // offload 解码
    case PAL_STREAM_VOICE_CALL:  s = new SessionAlsaVoice(rm);    break;  // 通话（含 CVD）
    case PAL_STREAM_NON_TUNNEL:  s = new SessionAgm(rm);          break;  // 纯 DSP 转码
    default:                     s = new SessionAlsaPcm(rm);      break;  // 绝大多数 PCM
}
```

| Session | 用于 | 落地方式 |
|---------|------|----------|
| `SessionAlsaPcm` | 普通 PCM 播放/录音、VoIP、Loopback | tinyALSA **pcm** + mixer control |
| `SessionAlsaCompress` | 压缩 offload | tinyALSA **compress** + mixer control |
| `SessionAlsaVoice` | 语音通话 | ALSA + 语音专用图（CVD 相关标定） |
| `SessionAgm` | Non-Tunnel（无硬件端点，纯转码） | 直接走 **AGM API**（不经 ALSA pcm 设备节点） |

关键区分：**前三个通过 ALSA 设备节点 + mixer 控制来间接驱动 AGM，`SessionAgm` 直接调
`agm_*` API。** 这也解释了为什么 `SessionAlsaPcm.cpp` 里既 `#include <agm/agm_api.h>`
又大量用 tinyALSA 的 `mixer_ctl_*`。

## 二、SessionAlsaPcm：控制面怎么下发

会话的 `open()`（`SessionAlsaPcm.cpp:140`）
干的第一件事是拿到虚拟 mixer，然后按方向分配 PCM 前端设备号，调用
`SessionAlsaUtils::open` 建立前后端连接：

```cpp
// SessionAlsaPcm::open（简化）
rm->getVirtualAudioMixer(&mixer);
// 按方向拿到 PCM 前端设备号 pcmDevIds + 后端名 rxAifBackEnds/txAifBackEnds
SessionAlsaUtils::open(s, rm, pcmDevIds, rxAifBackEnds);   // RX
// 或 TX / 或 loopback 的 Rx+Tx 组合
```

### 核心机制：FE/BE mixer control + Metadata

真正把图“描述”下发给 AGM 的，是一组 mixer control。看
`SessionAlsaUtils::open`（`SessionAlsaUtils.cpp:364`）：

```cpp
// 每个前端(FE)有几个关键控件：CONTROL / METADATA / CONNECT / DISCONNECT
mixer_ctl_set_enum_by_string(feMixerCtrls[FE_CONTROL], "ZERO");           // 复位
mixer_ctl_set_array(feMixerCtrls[FE_METADATA], streamMetaData.buf, ...);   // 流的 GKV
// 对每个后端(BE)：
beMetaDataMixerCtrl = getBeMixerControl(mixerHandle, be->second, BE_METADATA);
mixer_ctl_set_array(beMetaDataMixerCtrl, deviceMetaData.buf, ...);         // 设备 GKV
mixer_ctl_set_enum_by_string(feMixerCtrls[FE_CONTROL], be->second.data());
mixer_ctl_set_array(feMixerCtrls[FE_METADATA], streamDeviceMetaData.buf, ...); // 流+设备 GKV
mixer_ctl_set_enum_by_string(feMixerCtrls[FE_CONNECT], be->second.data());     // 连接 FE↔BE
```

这里出现了 AudioReach 最关键的概念——**Metadata / GKV（Graph Key Vector）**。它是
一组 key-value，用来在 ACDB 里唯一确定“该用什么图、什么标定”。PAL 下发三种 metadata：

- **stream metadata**：流本身的 GKV（stream type、方向等）
- **device metadata**：设备的 GKV（哪个后端、什么配置）
- **stream-device metadata**：流+设备组合的 GKV（这个组合专属的图段与标定）

**mixer control 的名字（FE_CONTROL/METADATA/CONNECT）由 AGM 的 mixer plugin 注册**，
所以 PAL 写 mixer = AGM plugin 收到请求（下一篇讲 plugin 侧）。`FE_CONNECT`/`FE_DISCONNECT`
就是在告诉 AGM：“把这个前端接到/断开这个后端”，对应 DSP 侧图的连接与断开。

### 标签级配置：TKV 与 setConfig

除了 GKV 决定“用哪张图”，还有 **TKV（Tag Key Vector）** 用于运行时调某个模块的参数
（如切换某后端采样率、开关某算法）。见
`SessionAlsaPcm.cpp:349` 附近：

```cpp
tagConfig = malloc(sizeof(agm_tag_config) + tkv.size()*sizeof(agm_key_value));
SessionAlsaUtils::getTagMetadata(tagsent, tkv, tagConfig);
ctl = mixer_get_ctl_by_name(mixer, tagCntrlName.str().data());   // 形如 "<PCMx> setParamTag"
mixer_ctl_set_array(ctl, tagConfig, ...);
```

**GKV 决定图的拓扑（编译期），TKV 决定图里某模块的参数（运行期）**——记住这对概念，
后面 AGM/GSL/ACDB 都围着它转。

## 三、PayloadBuilder：把参数拼成模块能懂的字节流

设置具体算法参数（音量、MFC 重采样系数、通道映射、USB/DP 配置…）时，PAL 不能只发
key-value，得拼出 DSP 模块认识的**二进制 payload**。这是
`PayloadBuilder.cpp` 的活：

```cpp
PayloadBuilder::payloadVolumeConfig(&payload, &size, ...);   // 音量
PayloadBuilder::payloadMFCConfig(&payload, &size, ...);      // 重采样/通道转换
PayloadBuilder::populateChannelMap(pcmChannel, numChannel);  // 通道映射
PayloadBuilder::payloadUsbAudioConfig(...);                  // USB 端点参数
```

每个 `payloadXxx` 按对应模块的参数结构体（PID + 结构体布局）填好内存，Session 再通过
`setParamTag`/`setCustomPayload` 类 mixer control 把它送下去。PayloadBuilder 还负责解析
`graph_key_value` 相关 XML（`processGraphKVData`），把 XML 里的 GKV 定义读进来。

**对音频工程师最实用的一点**：想加一个新的调音参数，往往就是在这里加一个 `payloadXxx`，
按 DSP 模块 API 头文件里的 PID 和结构体填字节，然后挂到某个 tag 上下发。

## 四、数据面：write/read

控制面用 mixer control，**数据面用 PCM/compress 设备节点**。`SessionAlsaPcm::write`
最终是 tinyALSA 的 `pcm_write`（对 compress 是 `compress_write`），数据经内核 ALSA →
AGM plugin → 共享内存到 DSP。控制面和数据面在此彻底分开：一条是 mixer 控制流，一条是
PCM 字节流。

## 五、PAL IPC：跨进程的 PAL

PAL 既可以和 audio HAL 同进程，也可以作为独立服务跨进程。跨进程时走 HwBinder（HIDL）：
接口定义在 `ipc/HwBinders/interfaces/pal/1.0/IPAL.hal`，
一对 client/server 包装：

```
HAL 侧进程                         PAL 服务进程
pal_stream_open()                  IPAL::stream_open()
  │ pal_client_wrapper.cpp            │ pal_server_wrapper: 转调真正的 Pal.cpp
  └─ BpHwPAL (proxy) ──HwBinder──►    └─ BnHwPAL (stub) ──► pal_stream_open(Pal.cpp)
回调:                               事件:
PalCallback::event_callback  ◄──────  server 通过 IPALCallback 回调
```

- **client**：`pal_ipc_client/src/pal_client_wrapper.cpp`
  把 `pal_stream_*` 调用序列化成 HIDL 请求；数据缓冲用 `hidl_memory`/共享内存（`IAllocator`/`IMemory`）
  和 FastMessageQueue（`MQDescriptor`）传输，避免大块 PCM 走 binder 拷贝。
- **server**：反序列化后调用同一份 `Pal.cpp`。
- **callback**：DSP 事件（数据就绪、drain 完成、检测事件）通过 `IPALCallback` 反向回调，
  见 `PalCallback::event_callback`
  （`pal_client_wrapper.cpp:219`）。

关键点：**IPC 是可选透明层**。无论同进程还是跨进程，最终都汇聚到同一份 `Pal.cpp` 逻辑；
IPC 只解决进程隔离和内存传递，不改变上面几篇讲的 Stream/Session/Device 模型。

## 小结

- Session 按流类型分派：PCM/Compress/Voice 走 ALSA 设备节点 + mixer control，Non-Tunnel
  直接走 AGM API。
- 控制面靠 FE/BE mixer control 下发三类 **Metadata/GKV**（stream、device、stream-device），
  外加 **TKV** 做运行期参数；这套 control 由 AGM 的 mixer plugin 注册。
- **GKV 定拓扑、TKV 定参数**是贯穿全链路的核心二元；PayloadBuilder 负责把参数拼成 DSP
  模块认识的二进制。
- 数据面走 PCM/compress 节点与共享内存，与控制面分离。
- PAL IPC（HwBinder）是可选透明层，跨进程也汇聚到同一份 Pal.cpp。

下一篇跨过 ALSA 边界，进入 AGM：mixer plugin 如何把这些 control 变成 AGM 请求，
以及 AGM 如何编排会话/图/设备的生命周期。
