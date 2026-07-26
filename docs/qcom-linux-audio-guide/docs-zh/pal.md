# 在 PAL 层定制

## PipeWire PAL 插件

PipeWire PAL 插件负责加载 PAL（平台抽象层）。它让客户端能够配置音频设备并调用各类音频用例。

PipeWire PAL 插件包含以下组件：

| 组件 | 说明 |
| --- | --- |
| **Card（声卡）** | 代表一块声卡，即一组受支持的 profile、port、sink 和 source。Card 模块的用途包括：加载/卸载 PAL；创建/释放 PAL 支持的 port；创建/释放 PAL 声卡；创建/释放 sink 或 source —— sink 是播放路径，source 是采集路径。 |
| **Sink（汇/播放）** | 配置音频播放路径。Sink 模块的用途包括：根据 module-pal-card 指定的配置打开/关闭一次播放会话；为 PAL 播放会话创建/释放写数据的 sink 线程；支持设置音量；支持获取延迟；支持路由。 |
| **Source（源/采集）** | 配置音频采集路径。Source 模块的用途包括：根据 module-pal-card 指定的配置打开/关闭一次 PAL 录制会话；创建/释放 PA source；为 PAL 录制会话创建读数据的 source 线程；支持路由。 |

## PAL API

PAL 对上层提供音频专用的 API，用于访问音频硬件与驱动，从而支持以下音频特性：

- 以 PCM 和压缩格式进行音频播放与录制，并可搭配各种前处理/后处理模块，其中包括对延迟和功耗敏感的用例。
- 对各类音频格式进行硬件加速的编码/解码。

客户端可通过各种 API 与 PAL 对接，用于控制和配置会话（session）与设备（device）。PAL 会执行以下操作：

- 配置混音器控件，以搭建硬件编解码器（codec）设备和流配置；
- 调用 TinyALSA API 来打开/启动音频会话。

PAL 的资源管理器（resource manager）会跟踪所有活动的会话与设备，以支持并发（concurrency）。它解析并加载以下平台 XML 文件的配置：

- `Resource_manager.xml` —— 设备到后端（device-to-backend）的映射，以及决策策略相关属性
- `Card-defs.xml` —— 虚拟 PCM 与压缩节点及其选项

PAL 的负载构造器（payload builder）为用例图构造元数据负载。关于图的更多信息，参见 [定制音频图](agm.md)。

PulseAudio 针对不同音频用例复用同一套 PAL API。PAL 模块的源码位于：

`build-qcom-wayland/workspace/sources/qcom-pal/opensource/arpal-lx`

下面这个文件给出了 PAL 模块暴露的全部 API：

`build-qcom-wayland/workspace/sources/qcom-pal/opensource/arpal-lx/inc/PalApi.h`

以下是常用的 PAL API。

### pal_init

初始化 PAL，解析相关配置文件，并把它们存入本地结构体供后续使用。

```c
int32_t pal_init( )
```

**参数**

无

**返回值**

- 成功返回 0
- 失败返回错误码

### pal_deinit

反初始化 PAL，释放初始化期间分配的资源。

```c
void pal_deinit()
```

**参数**

无

**返回值**

无

### pal_stream_open

按指定配置（源/汇设备、媒体配置等）打开一个流。成功时返回流句柄（stream handle）。

```c
int32_t pal_stream_open(
     struct pal_stream_attributes *attributes,
     uint32_t no_of_devices,
     struct pal_device *devices,
     uint32_t no_of_modifiers,
     struct modifier_kv *modifiers,
     pal_stream_callback cb,
     uint64_t cookie,
     pal_stream_handle_t **stream_handle)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| attributes | 有效的流属性。 |
| no_of_devices | 启动流时最初使用的音频设备数量。 |
| devices | pal_device 数组。数组大小以客户端在 no_of_devices 中指定的设备数量为准。 |
| no_of_modifiers | modifier 的数量。 |
| modifiers | modifier 数组。modifier 用于追加更多键值对。 |
| cb | 与该流关联的回调函数。此回调用于通知各类事件。 |
| cookie | 与该流关联的客户端数据。回调函数会把这个 cookie 原样返回。 |
| stream_handle | 操作成功时，会被更新为有效的流句柄。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pal_stream_start

启动一个流。

```c
int32_t pal_stream_start(
     pal_stream_handle_t *stream_handle)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| stream_handle | 来自 pal_stream_open 的有效流句柄。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pal_stream_read

读取从音频源设备采集到的音频缓冲区。

```c
ssize_t pal_stream_read(
     pal_stream_handle_t *stream_handle,
     struct pal_buffer *buf)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| stream_handle | 来自 pal_stream_open 的有效流句柄。 |
| buf | 指向 pal_buffer 的指针，其中包含音频采样数据和元数据。 |

**返回值**

- 读取的字节数
- 失败返回错误码

### pal_stream_write

写入音频缓冲区，以便在汇设备上渲染该流。

```c
ssize_t pal_stream_write(
     pal_stream_handle_t *stream_handle,
     struct pal_buffer *buf)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| stream_handle | 来自 pal_stream_open 的有效流句柄。 |
| buf | 指向 pal_buffer 的指针，其中包含音频采样数据和元数据。 |

**返回值**

- 写入的字节数
- 失败返回错误码

### pal_stream_stop

停止一个流。

```c
int32_t pal_stream_stop(
     pal_stream_handle_t *stream_handle)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| stream_handle | 来自 pal_stream_open 的有效流句柄。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pal_stream_close

关闭一个流。

```c
int32_t pal_stream_close(
     pal_stream_handle_t *stream_handle)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| stream_handle | 来自 pal_stream_open 的有效流句柄。 |

**返回值**

- 成功返回 0
- 失败返回错误码

## 配置文件

在 PAL 层，通过 `mixer_paths`、`resourcemanager` 和 `usecasekvmanager` 这几个 XML 文件来配置音频用例。

下表列出了不同硬件版本对应的配置文件：

| 变体 | 声卡名称 | Conf 文件 | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Core Kit（Qualcomm RB3 平台） | qcm6490-rb3-snd-card | qcm6490-rb3-snd-card.conf | mixer_paths_qcm6490_rb3.xml | resourcemanager_qcm6490_rb3.xml |
| Vision Kit | qcm6490-vision-snd-card | qcm6490-vision-snd-card.conf | mixer_paths_qcm6490_vision.xml | resourcemanager_qcm6490_vision.xml |
| Video Collab Kit | qcm6490-vc-snd-card | qcm6490-vc-snd-card.conf | mixer_paths_qcm6490_vc.xml | resourcemanager_qcm6490_vc.xml |

| 变体 | 声卡名称 | Conf 文件 | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Core Kit（RB8） | qcs9075-rb8-snd-card | qcs9075-rb8-snd-card.conf | mixer_paths_qcs9075_rb8.xml | resourcemanager_qcs9075_rb8.xml |

| 变体 | 声卡名称 | Conf 文件 | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Dragonwing IQ-8275 Beta 评估套件 | qcs8300-ridesx-snd-card | qcs8300-ridesx-snd-card.conf | mixer_paths_qcs8300_ridesx.xml | resourcemanager_qcs8300_ridesx.xml |

### 定制 mixer paths XML 文件

混音器控件（mixer control）是 ALSA 混音器向用户空间暴露的控制变量。它让用户空间能够访问 set/get 函数，并向 ALSA 混音器传递参数。

例如，下面是 `mixer_path.xml` 文件中启用单声道扬声器设备的条目。当触发播放且所选设备为扬声器时，会借助音频路由辅助类（audio route helper class）运行以下混音器控件。

```xml
<path name="speaker">
<!--Mixer controls related to speaker need to be defined here-->
</path>
```

平台使用 `mixer_paths_<sound-card-name>.xml` 文件作为混音器路径文件。该文件位于目标设备的 `/etc/` 目录下。

### 定制 resource manager XML 文件

`Resourcemanager.xml` 文件包含所有可能的设备、用例及其组合，还包含其他配置、模块参数和全局参数。

下面是资源管理器 XML 文件中扬声器设备条目的示例。它包含了扬声器设备的全部配置，例如后端名称（back-end name）、声道数、采样率、位宽等。

```xml
<out-device>
     <id>PAL_DEVICE_OUT_SPEAKER</id>
     <back_end_name>CODEC_DMA-LPAIF_WSA-RX-0</back_end_name>
     <max_channels>2</max_channels>
     <channels>2</channels>
     <samplerate>48000</samplerate>
     <bit_width>16</bit_width>
     <snd_device_name>speaker</snd_device_name>
</out-device>
```

### 定制 usecasekvmanager XML 文件

`Usecasekvmanager.xml` 文件存放每个用例的 GKV 详情。PAL 用这个 XML 文件获取每个用例的 KV 配置，再用该配置从 acdb 文件中取出图信息。该文件位于设备的 `/etc` 目录下。

下面是某个流与设备图键向量配置的示例。

**Stream KV（流键值）**

```xml
<stream type="PAL_STREAM_LOW_LATENCY">
     <keys_and_values Direction="RX" Instance="1">
     <!-- STREAMRX - PCM_LL_PLAYBACK -->
     <graph_kv key="0xA1000000" value="0xA100000E"/>
     <!-- INSTANCE - INSTANCE_1 -->
     <graph_kv key="0xAB000000" value="0x1"/>
</keys_and_values>
```

**Device KV（设备键值）**

```xml
<!-- Speaker Device -->
<device id="PAL_DEVICE_OUT_SPEAKER">
     <keys_and_values>
     <!-- DEVICERX - SPEAKER -->
     <graph_kv key="0xA2000000" value="0xA2000001"/>
     </keys_and_values>
</device>
```

**DevicePP KV（设备后处理键值）**

```xml
<!-- OUT Speaker DevicePPs -->
<devicepp id="PAL_DEVICE_OUT_SPEAKER">
<keys_and_values StreamType="PAL_STREAM_COMPRESSED,PAL_STREAM_LOW_LATENCY">
     <!-- DEVICERX - SPEAKER -->
     <graph_kv key="0xA2000000" value="0xA2000001"/>
     <!-- DEVICEPP_RX - DEVICEPP_RX_AUDIO_MBDRC -->
     <graph_kv key="0xAC000000" value="0xAC000002"/>
</keys_and_values>
```
