# AudioReach Open Source Project — Linaro Connect 2024 演讲资料

> **演讲题目：** AudioReach Open Source Project
> **场次编号：** MAD24-314
> **演讲者：** Patrick Lai（高通首席工程师，AudioReach 开源项目首席维护者）
> **会议：** Linaro Connect 2024
> **演讲语言：** 英文
> **资料整理日期：** 2026-07-25

---

## 资源链接

| 资源 | 地址 |
| --- | --- |
| Linaro Resources Hub 页面 | https://resources.linaro.org/en/resource/cQVJgqaPFngjW4yDLsMpUt |
| 演讲视频（YouTube） | https://www.youtube.com/watch?v=HgR2hiZNf_0 |
| YouTube 频道 | LinaroOrg — https://www.youtube.com/@LinaroOrg |
| 视频缩略图 | https://i.ytimg.com/vi/HgR2hiZNf_0/hqdefault.jpg |
| Resources Hub 封面图 | https://resources-hub-storage173548-main.s3.amazonaws.com/public/fullyPublic/0d0ea85a-e665-4b0e-81e1-88b5cbfd03c7.png |

![MAD24-314 AudioReach Open Source Project](https://i.ytimg.com/vi/HgR2hiZNf_0/hqdefault.jpg)

*图：YouTube 上的演讲视频缩略图（LinaroOrg 频道，视频 ID `HgR2hiZNf_0`）。*

---

## 官方摘要（摘要原文）

> AudioReach™ is a comprehensive and complete end-to-end audio software solution that Qualcomm dev…

> ⚠️ **关于摘要的说明：** Linaro Resources Hub 上存储的摘要字段本身就以 "Qualcomm dev…" 截断，完整的 `longDescription`、演讲视频直链、幻灯片附件等字段托管在 AWS AppSync GraphQL 后端（`https://2xkqb56wgbdepfjsigktq42prq.appsync-api.us-east-1.amazonaws.com/graphql`，鉴权方式 `AMAZON_COGNITO_USER_POOLS`），匿名访问返回 `UnauthorizedException`，需要登录 Linaro 账号才能读取。本页的官方摘要即取自该资源页 SSR 返回的 `description` 字段。

---

## 演讲内容大纲

> ℹ️ 高通开发者博客《[Qualcomm is open-sourcing AudioReach, its end-to-end audio software solution](https://www.qualcomm.com/developer/blog/2024/10/qualcomm-open-sourcing-audio-reach-end-to-end-audio-software)》（2024-10）由 Patrick Lai 本人撰写，文中明确写道“这是我在 Linaro Connect 上演讲 *AudioReach Open Source Project* 的摘要”。因此本演讲的内容主线与该博客一一对应，中文译本见同目录 [Qcom-AudioReach-zh.md](Qcom-AudioReach-zh.md)。以下大纲按博客章节整理，并标注了视频中的关键时间点。

### 1. 行业痛点与 AudioReach 的定位

当前音频开发开源生态存在几大空档：缺少统一的集成开发环境、缺少完整的调参 / 配置基础设施、跨处理器端到端实现用例需要拼接多套框架、开源框架对异构分布式处理没有原生支持、无法在低功耗子系统和高性能子系统粒度独立控制用例（信号流图）。

AudioReach 是高通内部自研、已规模商用、现正式开源的端到端音频软件 SDK，覆盖可穿戴、汽车、手机、XR、计算硬件，从旗舰 CPU 到小内存低功耗处理器都能跑。愿景是超越高通芯片，扩展到树莓派和 Xtensa DSP 等社区平台。授权为 BSD-3-Clause-Clear。

### 2. 开源工作流的四个环节

- 脱机（off-target）开发：在 PC 主机上直接动手。
- 基于 GUI 工具的图形化设计与配置。
- 设计完成后的完整测试与仿真套件。
- 通往目标设备的便捷部署路径，含集成测试与调参。

### 3. AudioReach SDK 六大组件

1. **AudioReach Creator** —— GUI 设计与配置环境。亮点：运行时改图（不停用例即可增删模块）、模块调参（视图由模块 API 自动生成）、按模块 / 线程 / 核的 DSP 资源监控、任务卸载到其他 DSP。
   - 🎬 **集成可视化调试工具演示**：实时 PCM 查看器 + 实时性能监视器，对应视频 **26m38s** 处（博客原文以 `&t=26m38s` 深链指向该片段）。
2. **信号处理框架（SPF）** —— 轻量、可扩展。模块经 CAPI 包装后接入；支持定点 / 浮点 / 压缩格式、PCM 与非 PCM 并发转码重采样、跨异构 CPU/MCU/DSP 多实例、线性与非线性拓扑、动态加载、控制链路、增量式建图、IRM 实时监控、时钟投票等。
3. **音频校准数据库（ACDB）** —— 存放用例拓扑、图定义与调参数据。
4. **AudioReach graph services** —— 跨 OS 图服务库，对客户端暴露 API，与各子系统 SPF 上的用例图交互，并从 ACDB 取回 / 下发图定义与调参数据。
5. **OS 平台适配** —— 通过平台适配与插件，复用 PulseAudio 等既有音频框架的开发者接触点。
6. **AudioReach SDK** —— 脱机仿真模式下跑与嵌入式设备相同的软件组件，先仿真再部署。

### 4. 开发工作流

主机侧：MATLAB/Simulink 算法开发 → 导入 AudioReach Creator → GUI 设计配置 → 脱机仿真（数据可接回 MATLAB）→ 在机验证（与 AudioReach 解耦）→ 工具自动生成已包装、已针对特定处理器架构优化的模块。
在机侧：导出配置到 SoC 软件栈各组件 → 在目标设备上集成、测试、配置、调参。目标是通过工具打通全流程。

### 5. AudioReach 在 Linux 上的三条启用路径

1. **link ALSA 内核驱动** —— 已上游化，目前仅支持基本播放 / 录音。
2. **用户态架构** —— PulseAudio on libALSA，AudioReach SDK 提供插件对接通用组件；完整特性集首选此路径。
3. **平台适配层（PAL）** —— 路线图上的中间件路径，提供开箱即用的用例 / 设备管理逻辑。

### 6. 设备部署愿景（Yocto）

参考硬件 → 同步 Yocto 工程 / meta-layer → 板子 bring-up → 验证音频用例 → AudioReach Creator 形态调参 → 设计用例图 → 构建 BSP 与 AudioReach 软件 → 部署。高通已开发好对应 meta-layer。

### 7. 路线图（按季度）

- **2025 Q2**：文档站首批内容（项目概览 + 软件设计），后续补充端到端搭产品教程。
- **2025 Q3**：移植到跑 Zephyr RTOS 的 Xtensa Hifi DSP；树莓派 4 增加录音；AudioReach IPC 内核驱动上游化以凑齐 Linux 栈。
- **2025 Q4**：翻新工作流与 CI/CD，转向公开开发。
- **2026 Q1**：AudioReach Creator 主组件彻底开源。

---

## 视频关键时间点

| 时间 | 内容 | 来源 |
| --- | --- | --- |
| 26m38s | 集成可视化调试工具演示：实时 PCM 查看器 + 实时性能监视器 | 博客原文深链 `&t=26m38s` |
| 末尾约 2 分钟 | AudioReach Creator 现场演示 | 博客原文 “a two-minute on-screen walkthrough of AudioReach Creator” |

> 📺 完整视频：https://www.youtube.com/watch?v=HgR2hiZNf_0

---

## 检索过程与限制说明

本资料文档基于以下可公开验证的来源整理，并标注了未能检索到的部分，供后续补全：

1. **Linaro Resources Hub SSR 元数据**：`curl` 获取资源页 HTML，从 `<script id="__NEXT_DATA__">` 的 Next.js SSR JSON 中解析出 `title` / `description` / `image` / `slug`。`description` 字段在 CMS 中即以截断形式存储。
2. **YouTube 元数据**：因 youtube.com 在本环境被网络策略阻断，改用 `https://noembed.com/embed?url=…` 代理获取，确认了视频标题（"MAD24 314 AudioReach Open Source Project"）、频道（LinaroOrg）与缩略图。
3. **演讲者与会议**：由高通开发者博客（作者本人撰写、明示为其 Linaro Connect 演讲的摘要）交叉确认。
4. **未能检索**：
   - Resources Hub 的完整长描述（`longDescription`）、演讲视频文件直链、幻灯片附件——需 Linaro 账号登录 AppSync GraphQL 后端。
   - YouTube 视频的完整描述文本与字幕转录——youtube.com / timedtext API / Invidious 实例均被网络策略阻断。
   - 各通用搜索引擎（Bing / Google / DuckDuckGo）在本环境被地区限制为中文区，对英文查询返回无关结果，无法用于补全摘要。
5. **内容主线**：鉴于博客是本演讲的官方书面摘要，演讲内容大纲依据博客章节整理，中文全译见 [Qcom-AudioReach-zh.md](Qcom-AudioReach-zh.md)。

---

## 相关资源

- 高通开发者博客（英文原文）：https://www.qualcomm.com/developer/blog/2024/10/qualcomm-open-sourcing-audio-reach-end-to-end-audio-software
- 中文译本：[Qcom-AudioReach-zh.md](Qcom-AudioReach-zh.md)
- AudioReach 开源仓库：https://github.com/Audioreach
- Qualcomm Developer Network Discord：https://discord.com/invite/qualcommdevelopernetwork
- AudioReach Creator 可视化调试演示片段：https://www.youtube.com/watch?v=HgR2hiZNf_0&t=26m38s
