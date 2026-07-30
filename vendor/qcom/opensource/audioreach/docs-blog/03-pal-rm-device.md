# 第 3 篇 PAL（下）：ResourceManager 路由决策与 Device 抽象

上一篇看到，每路 Stream 构造时都要 `ResourceManager::getInstance()` 和
`Device::getInstance()`。这一篇讲这两个东西：**ResourceManager 是 PAL 的全局大脑**，
负责用例决策、设备路由、并发仲裁；**Device 是硬件端点的抽象**，把扬声器/耳机/蓝牙/USB
统一成一组 `start/stop/config` 接口。

## 一、ResourceManager：全局单例大脑

[ResourceManager.cpp](../audioreach-pal/resource_manager/src/ResourceManager.cpp) 一个
文件一万四千行，是 PAL 里最重的模块。它是**进程内单例**，职责可归为四类：

### 1) 配置解析（启动时）

初始化时解析多份 XML，把“平台有哪些设备、哪个用例该配什么”读进内存：

```cpp
// ResourceManager.cpp init 路径
XmlParser(SNDPARSER);          // /vendor/etc/card-defs.xml：声卡与后端定义
XmlParser(rmngr_xml_file);     // resourcemanager.xml：设备能力/用例默认配置
// 另有 usecase manager xml、hapticsconfig xml、mixer xml 等
```

这些 XML 决定了 PAL 的“世界观”：有哪些 backend（后端/BE）、每个设备默认采样率/通道/
位宽、哪些用例要走哪个后端。**改设备配置往往改 XML，而不是改代码**（源码里也留了
`//TBD: decide on supported devices from XML and not in code` 的注释，说明方向是往
数据驱动走）。相关入口：`getDeviceInfo`
（[ResourceManager.cpp:2503](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L2503)）、
`getDeviceConfig`
（[ResourceManager.cpp:2822](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L2822)）。

### 2) 设备配置决策

Stream 拿到的 `pal_device` 只是个“愿望”（我想用扬声器），真正生效的采样率/通道/
位宽由 RM 结合 XML + 当前并发情况算出来：

- `checkAndGetDeviceConfig`
  （[ResourceManager.cpp:6215](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L6215)）：
  校正并填好设备配置。
- `checkAndUpdateGroupDevConfig`
  （[ResourceManager.cpp:6346](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L6346)）：
  处理**设备组**（如多路流共享一个物理后端时，配置要统一）。
- `getDeviceEpName`
  （[ResourceManager.cpp:6735](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L6735)）、
  `getBackEndNames`
  （[ResourceManager.cpp:7616](../audioreach-pal/resource_manager/src/ResourceManager.cpp#L7616)）：
  把设备 ID 映射成 ALSA 后端名/端点名——这就是连接 ALSA/AGM 的桥。

### 3) 并发仲裁与共享后端（这是重点）

多路流可能落到**同一个物理后端（Shared Backend, BE）**。比如深缓冲和低时延同时放到
扬声器，它们在 DSP 侧共享同一个硬件端点。RM 用一组“活跃流-设备”映射来管理：

```cpp
// 拿到与某设备共享同一后端的所有活跃流
getSharedBEActiveStreamDevs(activeStreamsDevices, dev_id);
// ResourceManager.cpp:7406
```

为什么重要？**同一后端只能有一套配置**。当第二路流想用不同采样率接入同一后端时，
RM 必须仲裁：要么让新流适配已有配置，要么触发**设备切换**把所有共享流一起切到新配置。

### 4) 路由与设备切换

运行中切设备（拔耳机、连蓝牙）走 `streamDevSwitch` /`forceDeviceSwitch`：

```cpp
// ResourceManager.cpp:8037
int32_t ResourceManager::streamDevSwitch(
        std::vector<std::tuple<Stream*, uint32_t>> streamDevDisconnectList,
        std::vector<std::tuple<Stream*, uint32_t>> streamDevConnectList);
```

它接收“要断开的(流,设备)列表”和“要连接的列表”，成对完成断开→连接。`pal_stream_set_device`
（[Pal.cpp:1025](../audioreach-pal/Pal.cpp#L1025)）最终就走到这里。切换全程也持
`lockGraph()`，因为它要重连底层的图。

### lockGraph：并发模型的核心

RM 持有一把全局图锁 `mGraphMutex`（`lockGraph`/`unlockGraph`）。**任何会改变 DSP 侧
图拓扑的操作——起流、停流、设备切换——都必须持这把锁串行执行。** 这是 PAL 面对
“多路并发 + 共享硬件 + 单一 DSP 图空间”时最简单可靠的选择。理解这把锁，就理解了
PAL 为什么很多操作看起来是串行的。

### 决策流程（起一路流时 RM 做了什么）

```
Stream.open/start
   │
   ├─ getDeviceInfo / getDeviceConfig      查 XML，得到设备默认能力
   ├─ checkAndGetDeviceConfig              校正为本次用例实际配置
   ├─ getSharedBEActiveStreamDevs          看这个后端上还有谁在跑
   │      └─ 有并发？ checkAndUpdateGroupDevConfig 统一配置
   │              └─ 配置冲突？ streamDevSwitch 把共享流一起切
   ├─ getBackEndNames / getDeviceEpName     算出 ALSA 后端名（交给 Session）
   └─ (lockGraph 保护整个过程)
```

## 二、Device：硬件端点抽象

`Device` 基类（[Device.h:83](../audioreach-pal/device/inc/Device.h#L83)）把所有物理
端点统一成一组接口：

```cpp
// Device.h（节选）
static std::shared_ptr<Device> getInstance(struct pal_device*, std::shared_ptr<ResourceManager>);
static std::shared_ptr<Device> getObject(pal_device_id_t dev_id);
virtual int start();                 // 起硬件端点
virtual int stop();
virtual int getDeviceAttributes(struct pal_device *dattr, ...);
virtual int getCodecConfig(struct pal_media_config *config);
virtual int32_t setDeviceParameter(uint32_t param_id, void *param);
virtual bool isDeviceReady() { return true; }
```

### getInstance 是“按设备 ID 分派 + 单例”

[Device.cpp](../audioreach-pal/device/src/Device.cpp) 里 `getInstance` 按
`device->id` 分派到具体子类，而每个子类内部维护自己的单例：

```cpp
switch (device->id) {
case PAL_DEVICE_OUT_SPEAKER:              return Speaker::getInstance(device, Rm);
case PAL_DEVICE_OUT_WIRED_HEADSET:
case PAL_DEVICE_OUT_WIRED_HEADPHONE:      return Headphone::getInstance(device, Rm);
case PAL_DEVICE_OUT_USB_DEVICE: ...       return USB::getInstance(device, Rm);
case PAL_DEVICE_OUT_BLUETOOTH_A2DP: ...   return BtA2dp::getInstance(device, Rm);
case PAL_DEVICE_IN_VI_FEEDBACK:           return SpeakerFeedback::getInstance(device, Rm);
...
}
```

**单例的意义**：一个物理扬声器在系统里只有一个 `Speaker` 对象，被所有用到它的流共享。
起停靠引用计数——最后一路流停了才真正关硬件。这与 RM 的共享后端仲裁是同一件事的
两面：RM 管“逻辑并发”，Device 单例管“物理复用”。

### 设备家族一览

[device/src/](../audioreach-pal/device/src/) 下的子类，按复杂度分三档：

| 档 | 设备 | 特点 |
|----|------|------|
| 简单端点 | Speaker / Handset / Headphone / HeadsetMic / SpeakerMic | 直接对接 codec/I2S 后端 |
| 协议设备 | BtA2dp / BtSco / USBAudio / DisplayPort | 带自己的编解码协商、连接状态；A2dp 还要处理 suspend/mute |
| 特殊功能 | SpeakerProtection / HapticsDevProtection / ECRefDevice / ExtEC / RTProxy / UltrasoundDevice | 不只是端点，含算法/回采/代理逻辑 |

### 两个值得音频工程师关注的特例

**SpeakerProtection**（[SpeakerProtection.cpp](../audioreach-pal/device/src/SpeakerProtection.cpp)）：
扬声器保护需要 **VI feedback**（电压/电流回采）——所以你会看到 `PAL_DEVICE_IN_VI_FEEDBACK`
这个“输入设备”其实是扬声器的反馈通道，配合 DSP 里的保护算法（限幅、热模型）防止喇叭
烧毁。这是“一个逻辑用例牵出多个物理设备”的典型。

**BtA2dp**（[Bluetooth.cpp](../audioreach-pal/device/src/Bluetooth.cpp)）：蓝牙音频的
编解码（SBC/AAC/LDAC/aptX）协商、A2DP suspend（通话时挂起）、以及和扬声器之间的
mute 联动，都在这里。上一篇 start 里那段 `a2dpSuspend` / `a2dpMuted` 逻辑就是和它配合。

## 小结

- ResourceManager 是 PAL 的大脑：解析 XML 建立世界观、决策设备实际配置、仲裁共享
  后端上的并发、执行设备切换，全程用 `lockGraph` 串行化图操作。
- Device 把物理端点抽象成统一接口，`getInstance` 按 ID 分派且每个物理设备单例化，
  靠引用计数在多路流间复用。
- RM 管逻辑并发，Device 单例管物理复用，两者共同解决“多流共享一套硬件与一张 DSP 图”
  的根本矛盾。
- 特殊设备（SpeakerProtection 的 VI 回采、蓝牙的编解码协商）说明：一个用例常常不止
  一个设备，PAL 在这层把这些复杂度收敛掉，再交给 Session 去下发。

下一篇：Session 如何把这些决策落到 ALSA/AGM——SessionAlsaPcm / Compress / Voice 的
分工，PayloadBuilder 如何拼参数，以及 PAL 的跨进程 IPC（HwBinder）。
