# 启用基于 TinyALSA 的应用

TinyALSA 是一个库，把 ALSA 内核接口封装成客户端可调用的 API。它同时提供一套插件接口，用于模拟（emulate）ALSA API。

TinyALSA 源码位于：

`build-qcom-wayland/workspace/sources/tinyalsa` 和

`build-qcom-wayland/workspace/sources/tinycompress`。

下图展示了 TinyALSA 的插件架构。

![TinyALSA 插件架构](../images/tinyalsa-tinyalsa_plugin_architecture.svg)

*TinyALSA 插件架构*

内核中的 ALSA 框架为 PCM、compress（压缩）和 mixer（混音器）暴露 card（声卡）与 device（设备）节点。

PCM、mixer、compress 插件都是 TinyALSA 插件。它们把应用发来的所有 PCM、mixer、compress 调用路由到各插件专属的具体实现。

这些插件会创建一块虚拟声卡，带有 PCM、compress、mixer 节点。虚拟节点映射到设备上的 `.so` 文件（可动态加载的共享对象）。

虚拟声卡的配置位于 `card-defs.xml` 文件中。该文件在设备的 `/etc/` 目录下。

## TinyALSA API

以下是常用的 TinyALSA API。完整的 API 说明参见 [TinyALSA 开源文档](https://github.com/tinyalsa/tinyalsa/blob/master/include/tinyalsa/pcm.h)。

### pcm_open

打开一个 PCM 音频设备以进行输入输出操作。它初始化一个用于通信的 PCM 设备，从而支持对音频数据的读/写操作。

```c
struct pcm *pcm_open(
     unsigned int card,
     unsigned int device,
     unsigned int flags,
     struct pcm_config *config)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| card | 声卡编号。 |
| device | 所选声卡中的设备编号。 |
| flags | 用于配置 PCM 设备的标志位。 |
| config | 指定音频流参数的结构体变量。 |

**返回值**

`pcm* handle`（PCM 设备句柄）

### pcm_is_ready

检查 PCM 设备是否已准备好进行输入输出操作。

```c
int pcm_is_ready(struct pcm *pcm)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |

**返回值**

- PCM 设备就绪时返回非零值
- PCM 设备未就绪时返回 0

### pcm_prepare

为 PCM 设备的输入输出操作做准备。

```c
int pcm_prepare(
     struct pcm *pcm)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pcm_start

启动 PCM 音频设备以进行输入输出操作。

```c
int pcm_start(
     struct pcm *pcm)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pcm_write

向音频 PCM 设备写入音频数据。它以音频数据为输入，并把数据发送到 PCM 设备进行播放或处理。

```c
int pcm_write(
     struct pcm *pcm,
     const void *data,
     unsigned int count)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |
| data | 要写入的音频数据。 |
| count | 要写入的音频帧数。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pcm_read

从 PCM 设备读取音频数据，使应用能够从麦克风采集音频数据。

```c
int pcm_read(
     struct pcm *pcm,
     void *data,
     unsigned int count)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |
| data | 要读取的音频数据。 |
| count | 要读取的音频帧数。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pcm_stop

停止 PCM 音频设备，使其不再进行输入输出操作。

```c
int pcm_stop(
     struct pcm *pcm)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |

**返回值**

- 成功返回 0
- 失败返回错误码

### pcm_close

关闭 PCM 音频设备。此操作会释放与该 PCM 设备关联的资源，并释放内存。

```c
int pcm_close(
     struct pcm *pcm)
```

**参数**

| 参数 | 说明 |
| --- | --- |
| pcm | 指向已打开 PCM 设备的指针。 |

**返回值**

- 成功返回 0
- 失败返回错误码

## 配置 TinyALSA

要从 TinyALSA 运行音频用例，需要配置虚拟混音器控件。

这些控件由 mixer 插件创建，用于搭建音频用例图和模块。它们大多基于字节数组（byte array），通过 `mixer_ctl_set_array` API 进行配置。元数据（称为 “PCM100 metadata”）通过键值对（KV pair）设置。实现细节参见 `build-qcom-wayland/workspace/sources/qcom-agm/opensource/agm/plugins/tinyalsa/test/agmmixer.c` 中的 `set_agm_audio_intf_metadata` API。

```c
/**
            * Key Vector pair
            */
            struct agm_key_value {
            uint32_t key; /**< key */
            uint32_t value; /**< value */
            };
            /*Sample allocation for the key value pair*/
            gkv = calloc(num_gkv, sizeof(struct agm_key_value));
            ckv = calloc(num_ckv, sizeof(struct agm_key_value));
```

基于 TinyALSA 的 agmplay 和 agmcap 工具的示例代码位于：

`build-qcom-wayland/workspace/sources/qcom-agm/opensource/agm/plugins/tinyalsa/test`。

从 TinyALSA 启用并执行音频用例的步骤如下：

1. 设置音频接口（后端）设备配置，包括采样率、声道数、格式（format）和数据格式（data format）。

   ```text
   'CODEC_DMA-LPAIF_WSA-RX-0 rate ch fmt' 48000 2 2(PCM_16)
   ```
2. 设置元数据，包括设备与 DevicePP 的图键（graph key）和校准键（cal key）。

   ```text
   'CODEC_DMA-LPAIF_WSA-RX-0 metadata' bytes
   ```
3. 设置控件，表明后续的混音器配置将为 stream 和 StreamPP 子图设置元数据。取值为 0 表示后续命令针对的是 stream。

   ```text
   'PCM100 control' Zero
                       'PCM100 metadata' bytes
   ```
4. 设置控件，表明后续的混音器配置将为 DevicePP 和 stream-device 子图设置元数据。`CODEC_DMA-LPAIF_WSA-RX-0` 表示后续命令针对的是 stream-device。`CODEC_DMA-LPAIF_WSA-RX-0` 是注册到 ALSA ASOC 框架的音频接口之一，全部音频接口的列表可在 `/proc/asound/pcm` 中查看。

   ```text
   'PCM100 control' CODEC_DMA-LPAIF_WSA-RX-0
                       'PCM100 metadata' bytes
   ```
5. 获取与某个会话（stream 与音频接口之间）关联的全部 tag、模块 ID 和实例 ID。

   ```text
   'PCM100 getTaggedInfo' bytes
   ```
6. 设置控件，表明后续的混音器配置将为 stream 子图上的模块设置参数。

   ```text
   'PCM100 control' Zero
                       'PCM100 setParam' bytes
   ```
7. 设置控件，表明后续的混音器配置将为 StreamDevice 和 DevicePP 子图上的模块设置参数。

   ```text
   'PCM100 control' CODEC_DMA-LPAIF_WSA-RX-0
                       'PCM100 setParam' bytes
   ```
8. 把前端（stream）与后端（codec/音频接口）连接起来。

   ```text
   'PCM100 connect'CODEC_DMA-LPAIF_WSA-RX-0
   ```
9. 打开 PCM 设备。

   ```text
   pcm_open
   ```
10. 为 PCM 设备的输入输出操作做准备。

    ```text
    pcm_prepare
    ```
11. 启动 PCM 音频设备以进行输入输出操作。

    ```text
    pcm_start
    ```
12. 从音频 PCM 设备写入和读取音频数据。

    ```text
    pcm_write/pcm_read
    ```
13. 停止 PCM 设备。

    ```text
    pcm_stop
    ```
14. 关闭 PCM 音频设备。

    ```text
    pcm_close
    ```

要获取某个虚拟设备的全部混音器控件，可使用以下命令：

```shell
ssh root@ip-addr
```

```shell
systemctl stop pipewire
```

```shell
tinymix set -D 100
```
