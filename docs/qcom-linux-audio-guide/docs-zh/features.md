# 高级音频特性

## 抑制回声与噪声

在 VoIP（基于 IP 的语音通话）系统中，回声和噪声问题很常见。语音从远端（far-end）说话人发出，经过一段时间延迟后回传，形成回声，影响听感。回声消除（echo cancellation）用于在通话过程中削弱来自远端说话人的回声；噪声抑制（noise suppression）用于削弱麦克风通道上的噪声。Fluence 回声消除与噪声抑制（Echo Cancellation and Noise Suppression，ECNS）算法可提供平稳噪声与非平稳噪声的抑制，以及回声消除能力。

声学回声（acoustic echo）指的是由于设备扬声器与麦克风之间的声学路径（声学耦合，acoustic coupling）而产生的回声。它对免提（hands-free）和电话会议类应用尤为重要。

下图展示了声学回声路径，以及扬声器与麦克风之间是如何产生声学回声的。

![噪声与声学回声](../images/features-ECNS_overview.svg)

*噪声与声学回声*

- **回声消除器（Echo Canceller）** —— 一种自适应滤波器，通过自我调整系数来抵消回声。每一路回声都有其回声路径，可用冲激响应（impulse response）来刻画。回声消除器会自适应网络回声路径，从而抵消回声。
- **噪声抑制（Noise Suppression）** —— 单麦克风回声消除与噪声抑制器（Single Mic Echo Canceller and Noise Suppressor，SMECNS）可在嘈杂环境中使用设备时，抑制周围的平稳噪声。

### 为录制启用 SMECNS

录制时，Fluence 通过抑制麦克风采集到的背景噪声，来保持录制路径中的语音质量。

对于单麦克风录制，只能实现平稳噪声（stationary noise）的抑制。平稳噪声是指频率不随时间变化的噪声，例如路噪或白噪声。

下图展示了如何通过增益（gain）、SMECNS 和后处理模块去除外部噪声与回声，从而输出干净的语音。

![录制用 SMECNS 软件模块](../images/features-fluence_recording.svg)

*录制用 SMECNS 软件模块*

在录制路径中启用 SMECNS 的步骤如下：

1. 用 `wpctl status` 命令列出可用节点。

   ```shell
   wpctl status
   ```
2. 运行 `wpctl set-default` 把源节点设为手柄麦克风（handset mic）。

   ```shell
   wpctl set-default <handset mic node>
   ```
3. 运行 `pw-record` 开始录制。下面的示例以详细模式（verbose）运行，并把录音保存到 `/opt/test.wav`。

   ```shell
   pw-record /opt/test.wav -v
   ```

### 为 VoIP 启用 SMECNS

Fluence 可降低 VoIP 通话中的噪声并消除回声，同时抑制麦克风信号上的噪声和声学回声。

SDK 支持 PipeWire 的 VoIP source 和 sink，你在开发应用时可以直接使用它们。

下图展示了在 VoIP 通话中应用增益、Fluence 和后处理模块后，输入语音到输出语音的处理流程。

![VoIP 用 SMECNS 软件模块](../images/features-voip_call_diagram.svg)

*VoIP 用 SMECNS 软件模块*

在 VoIP 路径中启用 SMECNS 的方式如下：

| 操作 | 命令 |
| --- | --- |
| **设置录制源** | `pw-record /opt/record_voip.wav -v --target=voip-tx0` |
| **设置播放汇** | `pw-play /opt/test.wav -v --target=voip-rx0` |

> **注意**
>
> 务必先把一个 PCM 文件（`<FileName>.wav`）推送到 `/opt/` 目录。

### 启用压缩卸载播放（compress offload playback）

启用通过低功耗卸载路径（offload path）进行的音频播放，其中解码和后处理都由 DSP 完成。与标准播放路径相比，这种方式在提升性能的同时还能降低功耗。

1. 把 MP3 文件推送到设备。

   ```shell
   adb push <test.mp3> /opt/
   ```
2. 列出可用的音频节点。

   ```shell
   wpctl status
   ```
3. 设置默认的 compress 节点。

   ```shell
   wpctl set-default <Compress-Number>
   ```
4. 开始播放。

   ```shell
   pw-encplay /opt/<test.mp3>
   ```

> **注意**
>
> 压缩卸载路径仅支持 MP3。
