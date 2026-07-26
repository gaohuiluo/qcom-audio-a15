# AudioReach 官方文档中文版

> 本目录是 AudioReach 官方文档站 **https://audioreach.github.io** 的完整离线镜像与简体中文译本。
> 抓取与翻译日期：2026-07-26。面向音频 / 嵌入式工程师，供离线走读学习使用。

## 这是什么

[AudioReach](https://github.com/Audioreach) 是高通开源的端到端音频软件方案（BSD-3-Clause-Clear），
涵盖 DSP 上的信号处理框架（SPF / AudioReach 引擎）、跨 OS 的图服务、平台适配与开发工具链。
本文档即其官方 Sphinx 文档站的全量内容，共 **32 个页面**，已转为 Markdown 并译为中文。

## 目录组织

```
audioreach-docs-site/
├── md_zh/          ← 中文译本（推荐从这里开始读）
│   └── _images/    ← 图片（118 张，供各页相对引用）
├── md_en/          ← 英文原文 Markdown（对照用）
│   └── _images/
├── raw/            ← 抓取的原始 HTML + 图片（存档）
├── TRANSLATION_GUIDE.md  ← 翻译术语规范
├── crawl_ar.sh     ← 站点抓取脚本
├── html2md.py      ← HTML→Markdown 转换脚本
└── fix_links.py    ← 站内链接改写脚本
```

> 说明：站内相对链接已从 `.html` 改写为 `.md`，中文文档之间可直接跳转；
> 外部链接（qualcomm.com / yoctoproject.org 等）保持原样。

## 阅读导航（中文版）

### 项目概览
- [AudioReach 项目概览 / SDK 概览与路线图](sdk_overview.md)

### 设计（Designs）—— 理解架构从这里入手
- [AudioReach 架构概览](design/arch_overview.md)
- [核心概念与术语](design/design_concept.md) ★ 建议先读：图 / 子图 / 模块 / 容器 / GKV / CKV / TKV
- [AudioReach 引擎（SPF）设计](design/arspf_design.md)
- [AudioReach 图服务（ARGS）设计](design/args_design.md)
- [通用包路由器（GPR）设计](design/gpr_design.md)
- [Linux 适配设计](design/lx_design.md)
  - [Linux ASoC 架构](design/linux_asoc_arch.md)
  - [Linux 插件架构](design/linux_plug-in_arch.md)

### API 参考
- [AudioReach 引擎 API](api/arspf_api.md)
  - [SPF CAPI 接口](api/spf_capi.md)
  - [POSAL 平台抽象层 API](api/posal_api.md)
- [AudioReach 图服务 API](api/args_api.md)
  - [GSL 图服务层 API](api/args_gsl.md)
  - [AROSAL OS 抽象层 API](api/args_arosal.md)
- [通用包路由器（GPR）API](api/gpr_api.md)

### 开发者指南（Developer Guides）
- [开发工作流](dev/dev_workflow.md)
- [系统工作流](dev/system_workflow.md)
- [平台移植指南](dev/plat_port.md)
- [可用音频模块列表](dev/available_modules.md)
- [如何添加音频模块](dev/adding_modules.md)
- [CAPI 模块开发指南](dev/capi_mod_dev.md) —— 最大篇幅，C 语言模块开发全流程
- [配合 AudioReach 使用 ALSA lib](dev/alsalib_using_audioreach.md)

### AudioReach Creator（ARC 工具）
- [ARC 介绍 / 路线图 / 架构](arc/index.md)

### 平台参考指南
- [Raspberry Pi 4](platform/raspberry_pi4.md)
- [RB3 Gen2](platform/rb3_gen2.md)
- [NXP IMX8M Plus](platform/nxp.md)

### 官方站首页
- [文档站首页（中文）](index.md)

## 翻译约定

- 代码、命令、API / 结构体 / 枚举 / 宏 / 类型名、文件路径一律保留英文原样；只译自然语言叙述。
- 术语统一，详见 [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)。
- 忠实翻译，不增删内容。每个中文页面的标题层级、代码块数、图片数均与英文原文逐一核对一致。

## 如何更新

重新抓取 → 转换 → 修链接：

```bash
bash crawl_ar.sh        # 抓取最新 HTML 与图片到 raw/
python html2md.py       # raw/*.html -> md_en/*.md
python fix_links.py     # md_zh 内部链接 .html -> .md（翻译后再跑）
```
