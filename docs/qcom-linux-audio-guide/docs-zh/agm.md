# 定制音频图

每个音频用例都是一张图（graph），由若干特定类型的子图（subgraph）构成。每个子图包含一个或多个功能性软件块（称为模块，module），各自完成特定功能。

## 音频图相关术语

| 术语 | 说明 |
| --- | --- |
| **用例（Use case）** | 一张由模块组成的图，从源端点（source endpoint）连到汇端点（sink endpoint），满足产品定义的用例需求。 |
| **图（Graph）** | 对一组相互连接的子图的逻辑表述，用于实现某个特定用例。 |
| **子图（Subgraph）** | 对一组模块的逻辑抽象，这些模块相互连接、作为一个整体被操作。 |
| **容器（Container）** | 让系统设计者能够把多个音频处理模块归到一起、在同一个软件线程中运行的对象。 |
| **模块（Module）** | 信号处理框架中最小的独立处理单元。 |
| **键值对（Key-Value，KV pair）** | 键向量中单个的键及其关联的值。例如，键可以是某个声音设备，值可以是耳机、扬声器或其他声音设备。 |
| **键向量（Key vector）** | 通过一组 KV 对唯一标识一张图或一个子图。 |
| **图键向量（Graph Key Vector，GKV）** | GKV 是用于获取某张图的唯一标识，以 KV 对表示。系统设计者在 QACT UI 画布上创建子图时，会为其关联一组唯一的 `<keys>` 和 `<values>`。 |
| **校准键向量（Calibration Key Vector，CKV）** | CKV 是用于获取校准数据的唯一标识，以 KV 对表示。系统设计者在存储校准数据时，会为其关联一组唯一的 `<keys>` 和 `<values>`。 |
| **标签与标签键向量（Tag / Tag Key Vector，TKV）** | 标签（tag）是一种标识符，用于设置一个或多个模块的运行时参数。它允许在运行时更新模块配置（例如启用/禁用回声消除、均衡等特性）。 |

## 图的分段

一个音频用例包含以下几段。

前端（front-end）对应 stream 与 streamPP 子图，后端（back-end）对应每流每设备（Per-Stream Per-Device，PSPD）、devicePP 和 device 子图。

| 分段 | 说明 |
| --- | --- |
| **Stream** | 提供数据写入/读取接口，并对压缩数据进行解码与编码。 |
| **StreamPP** | 承载基于流的处理模块（例如均衡器 equalizer）。 |
| **PSPD** | 承载一个模块，负责把流的媒体格式转换成设备的媒体格式。 |
| **DevicePP** | 承载用于声音设备调音（tuning）的处理模块。 |
| **Device** | 硬件端点，例如 CodecDMA（SoundWire）、I2S 或 TDM 端口。 |

前端通过路由混音器控件（routing mixer control）连接到后端后，完整的 GKV 由子图 GKV 与通过混音器控件指定的 CKV 拼接而成。当打开前端的 PCM 或压缩（compress）设备时，AGM 用拼接好的 GKV 与 CKV 调用 GSL API，在 SPF 中搭建图并应用校准。与此同时，AGM 打开与所连接后端相对应的内核 PCM 设备，开始配置音频外设。

## 音频图示例

下图展示了一个用于播放场景的音频图示例。

![播放用音频图示例](../images/agm-sample_audio_graph.svg)

*播放用音频图示例*

在这张图中：

1. stream 子图包含一个写共享内存端点（write shared memory endpoint）、一个 PCM 解码器和一个 PCM 转换器。客户端把 PCM 采样数据传给写共享内存端点。
2. 如有必要，PCM 转换器会把 PCM 采样转换成流专属后处理模块所支持的格式。
3. stream 子图的输出送入 stream-device 子图，其中包含媒体格式转换器（Media Format Converter，MFC）。MFC 把 stream 子图的 PCM 转换成 device 子图的 PCM 格式。
4. 转换完成后，stream-device 子图的输出送入 device PP 子图，进行设备专属的后处理。子图开头放置了一个混音器（mixer），用于混合输入流。
5. devicePP 子图的输出接着送入 device 子图，其中包含硬件端点模块，例如 I2S 驱动。

这张示例图对应的 GKV 如下：

```text
GKV1: <StreamRX1 KVs, StreamRX2 PP KVs, StreamRX1DeviceRX KVs, DeviceRX PP KVs, DeviceRX KVs>

GKV2: <StreamRX2 KVs, StreamRX2 PP KVs, StreamRX2DeviceRX KVs, DeviceRX PP KVs, DeviceRX KVs>
```

### 音频图管理器（AGM）

音频图管理器（Audio Graph Manager，AGM）提供接口，使基于 TinyALSA 的混音器控件与 PCM/压缩音频插件能够相互交互，进而启用各类音频用例。AGM 作为运行在用户空间的 PipeWire 服务的一部分运行。

AGM 为混音器插件以及 PCM/压缩 API 提供接口，用于搭建音频用例。它维护多个 ALSA 客户端来搭建用例，同时还负责管理前端到后端的连接。

下图展示了 AGM 模块的高层结构。

![AGM 软件模块（高层）](../images/agm-AGM_service_blocks.svg)

*AGM 软件模块（高层）*

| 对象 | 说明 |
| --- | --- |
| **Session（会话）** | 会话对象代表一次音频播放或采集会话。调用会话专属的混音器控件或 API 会创建会话。它为 TinyALSA 插件提供配置流的 API，并管理图对象与设备对象的状态转换。 |
| **Graph（图）** | 图对象代表一个音频用例。它与 GSL 交互，负责打开、管理和关闭图；提供图创建的 API，管理图，并配置流与设备端点。 |
| **Device（设备）** | 设备对象代表 ALSA 声卡中的一个 ALSA 设备。它枚举可用的音频接口，并提供用于切换设备状态的设备 API。 |

### AudioReach 图服务（ARGS）

AudioReach™ 信号处理框架图服务（AudioReach Graph Services，ARGS）由图服务层（Graph Service Layer，GSL）、通用数据包路由器（Generic Packet Router，GPR）和 acdb 管理层（acdb Management Layer，AML）组成。它负责图的初始化与创建，以及构造数据包，向 SPF 下发一系列命令。

| 组件 | 说明 |
| --- | --- |
| **GSL** | 图服务层（GSL）是 SPF 的软件驱动，负责管理图、子图、缓冲区和各类配置。它使用图键向量（GKV）加载并初始化图，处理数据命令以及 SPF 模块校准。 |
| **GPR** | 通用数据包路由器（GPR）在 SPF 与图服务库之间路由音频消息数据包。处理用于构建音频图和处理音频的命令。 |
| **AML** | acdb 管理层（AML）提供 get/set API，用于读取和调整 acdb 文件中的数据。它为音频驱动及其组件如何消费校准数据提供了数据抽象与组织方式。 |

## 音频校准数据库（acdb）

acdb 是应用处理器上的一个静态数据库，包含 LPAI 的全部调音/校准参数。`*.acdb` 文件格式负责为各种用例、各种音频模块组织校准数据。

用 QACT（一款 PC 工具）编辑这种文件格式，并把文件放到设备文件系统的 `/etc/acdbdata/` 目录下。在用例初始化或设备切换期间，AML 会用指定的 GKV 查询 acdb 数据库，并把设备校准数据推送给 SPF。

### 信号处理框架（SPF）

信号处理框架（Signal Processing Framework，SPF）运行在 LPAI 子系统中，负责音频数据处理。

下图给出了 SPF 中所用功能块的高层概览。

![SPF 软件模块（高层）](../images/agm-spf_blocks.svg)

*SPF 软件模块（高层）*

| 组件 | 说明 |
| --- | --- |
| **APM** | 音频处理管理器（Audio Processing Manager，APM）在 SPF 中搭建并管理用例图。它向图管理库和 APM 客户端提供标准 API，用于搭建和配置音频用例。 |
| **Modules（模块）** | 模块是 SPF 中的功能块，在 LPAI 子系统中执行实时音频处理。 |
| **Containers（容器）** | 容器是一种框架实现，把一组数据处理模块放在同一个软件线程中一起运行。每个容器都运行在各自独立的软件线程里。 |
