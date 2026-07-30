# AudioReach 架构解析：从 PAL 到 DSP

面向音频工程师的一套源码级架构博客，基于本仓库
`vendor/qcom/opensource` 下的 AudioReach 代码（Android A15 / qcom-audio）。

重点讲清各模块的**作用**与**交互边界**，不做冗长的概念铺陈。每篇都给出可点击的
关键代码位置与调用/时序图。

## 全链路一句话

`pal_stream_open/start` → ResourceManager 选设备定用例 → Session 通过 ALSA/AGM
plugin 打通 → AGM 编排会话与图 → GSL 结合 ACDB 图定义 + 标定求解出子图/模块拓扑
→ GPR 打包命令跨核送到 DSP → APM 按图实例化 Container 与 Module → 数据经共享内存
在 APPS/DSP 间流转。

## 分层与代码位置

| 层 | 角色 | 代码根 |
|----|------|--------|
| PAL | 平台抽象层，统一 `pal_stream_*` API | [audioreach-pal/](../audioreach-pal/) |
| AGM | 会话/图/设备生命周期编排 | [agm/](../../agm/) |
| GSL | 图求解、子图/共享内存/数据通路管理 | [audioreach-graphservices/gsl/](../audioreach-graphservices/gsl/) |
| ACDB | 图拓扑定义 + 标定数据 | [audioreach-graphservices/acdb/](../audioreach-graphservices/acdb/) |
| GPR | 通用包路由，跨处理器寻址 | [audioreach-engine/gpr/](../../audioreach-engine/gpr/) |
| SPF | DSP 侧信号处理框架（APM/Container/Module） | [audioreach-engine/fwk/spf/](../../audioreach-engine/fwk/spf/) |
| Kernel | ASoC/glink/dsp，承载 GPR 与数据搬运 | [audio-kernel-ar/](../../../audio-kernel-ar/) |

## 目录

1. [总览：七层全景与端到端路径追踪](01-overview.md)
2. [PAL（上）：入口、Stream 家族与生命周期](02-pal-stream.md)
3. [PAL（下）：ResourceManager 路由决策与 Device 抽象](03-pal-rm-device.md)
4. [PAL Session 与 IPC：如何落到 ALSA](04-pal-session-ipc.md)
5. [AGM：会话/图/设备编排与 ALSA plugin](05-agm.md)
6. [GSL + ACDB：图求解与标定](06-gsl-acdb.md)
7. [GPR：通用包路由与跨核传输](07-gpr.md)
8. [SPF/DSP：APM、Container、Module 与 AMDB](08-spf-dsp.md)
9. [内核篇：audio-kernel-ar 承载 GPR 与数据搬运](09-kernel.md)

> 说明：文中代码行号对应当前仓库快照，随版本可能漂移；引用以函数名/结构体名为准。
