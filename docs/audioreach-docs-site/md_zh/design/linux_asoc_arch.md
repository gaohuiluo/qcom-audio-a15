# Linux ASoC 架构

## 简介

AudioReach ALSA 驱动提供了插入 ASoC 框架所需的驱动接口。这使得 AudioReach 能够利用 ASoC 拓扑框架，以数据驱动的方式为给定设备定义用例拓扑。AudioReach ALSA 驱动已上游合入内核源码树，位于 <kernel_src>/sound/soc/qcom/qdsp6。

查看以下链接以了解更多关于 ASoC 拓扑架构和拓扑配置的信息：

- [ALSA SoC Layer Overview](https://www.kernel.org/doc/html/v5.15/sound/soc/overview.html)
- [ALSA topology](https://www.alsa-project.org/wiki/ALSA_topology)
- [ASoC topology ELC talk slides](http://events17.linuxfoundation.org/sites/events/files/slides/ASoC_Topology_ELCNA17_230217.pdf)
