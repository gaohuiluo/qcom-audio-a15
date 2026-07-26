# Qualcomm 音频文档资料库

> 高通（Qualcomm）音频相关的中文整理资料合集，面向音频 / 嵌入式工程师，供离线走读学习使用。
> 内容涵盖 **AudioReach 开源方案** 与 **Qualcomm Linux 音频子系统** 两大主线，均含中英对照。

## 📚 三大板块

### 1. [博客与演讲解读](blogs/) — 从这里入门
高通开源 AudioReach 的第一手资料：官方博客译文 + Linaro Connect 2024 技术演讲整理。
一两篇文章即可建立对 AudioReach「是什么、解决什么问题、整体架构」的认知。

- [高通开源 AudioReach 官方博客（中文）](blogs/qcom-audioreach-zh.md) ★ 建议第一篇读
- [官方博客英文原文](blogs/qcom-audioreach-en.md)
- [Linaro Connect 2024 演讲资料](blogs/linaro-connect-2024-talk.md)

### 2. [AudioReach 官方文档镜像](audioreach-official/) — 深入架构与开发
[AudioReach 官方文档站](https://audioreach.github.io) 的完整离线镜像与简体中文译本，共 **32 个页面**。
涵盖 DSP 信号处理框架（SPF / AudioReach 引擎）、跨 OS 图服务、API 参考、平台移植与开发工具链。

- **设计** — 架构概览、核心概念与术语、引擎/图服务/GPR 设计
- **API 参考** — 引擎 API、图服务 API、GPR API
- **开发者指南** — 开发工作流、平台移植、模块开发、ALSA lib 集成
- **平台参考** — Raspberry Pi 4 / RB3 Gen2 / NXP IMX8M Plus

→ 详见 [audioreach-official/README.md](audioreach-official/README.md) 的完整阅读导航（中英对照）。

### 3. [Qualcomm Linux 音频指南](qcom-linux-audio-guide/) — 落地实战
翻译自 Qualcomm 官方文档《Audio》（文档号 80-70030-16），面向在 Qualcomm Linux 平台上
搭建、启用、定制与调试音频的工程师。

- **音频概览** — 组件与软件架构
- **启用音频** — 硬件搭建、GStreamer / PipeWire 录放
- **定制用例** — PAL 层定制、TinyALSA、AGM 音频图
- **故障排查** — 日志抓取与分析
- **高级特性** — VoIP ECNS 降噪回声消除

→ 详见 [中文指南导航](qcom-linux-audio-guide/docs-zh/README.md)。

## 🗺️ 我该读哪个？

| 你的目标 | 从这里开始 |
| --- | --- |
| 快速了解 AudioReach 是什么 | [博客解读](blogs/qcom-audioreach-zh.md) |
| 理解 AudioReach 架构 / 核心概念 | [官方文档 · 设计](audioreach-official/md_zh/design/design_concept.md) |
| 开发 / 移植 AudioReach 模块 | [官方文档 · 开发者指南](audioreach-official/md_zh/dev/dev_workflow.md) |
| 在 Qualcomm Linux 板子上启用音频 | [Linux 音频指南 · 启用音频](qcom-linux-audio-guide/docs-zh/enable-audio.md) |
| 定制音频用例 / 调音频图 | [Linux 音频指南 · 定制](qcom-linux-audio-guide/docs-zh/agm.md) |
| 排查音频问题 | [Linux 音频指南 · 故障排查](qcom-linux-audio-guide/docs-zh/troubleshoot.md) |

## 📂 目录结构

```
docs/
├── README.md                    ← 本文件（总入口）
├── blogs/                       ← 博客与演讲解读（中英）
│   ├── README.md
│   └── images/
├── audioreach-official/         ← AudioReach 官方文档站镜像（32 页，中英对照）
│   ├── README.md                ← 完整阅读导航
│   ├── md_zh/  md_en/  raw/
└── qcom-linux-audio-guide/      ← Qualcomm Linux 音频指南（中英对照）
    ├── docs-zh/  md_en/  raw/  images/
```

## ℹ️ 说明

- 所有中文均为**忠实翻译**：代码、命令、API / 结构体 / 枚举 / 宏 / 类型、文件路径保留英文原样，只译自然语言叙述。
- 各板块内文档间均使用相对链接，可在 GitHub 或本地 Markdown 阅读器中直接跳转。
- 资料来源分别为高通开发者博客、AudioReach 官方文档站、Qualcomm 官方文档，版权归原作者所有；本仓库仅作学习整理。
