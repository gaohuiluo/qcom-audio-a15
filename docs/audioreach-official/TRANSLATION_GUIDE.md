# AudioReach 文档中译规范（供翻译使用）

## 目标
把 AudioReach 官方文档（Sphinx 站点）译为**简体中文**，面向**音频/嵌入式工程师**，
技术博客风格：准确、通顺、专业、可读，不生硬直译。

## 硬性规则
1. **只译正文叙述文字**。以下一律**保持英文原样，不翻译**：
   - 代码块（``` 包裹的内容）内的所有代码、命令、日志。
   - 内联代码 `code`（函数名、宏、文件名、路径、变量、寄存器、shell 命令）。
   - API 名 / 结构体名 / 枚举 / 宏 / 类型名（如 `apm_module_param_data_t`、`GPR_IDS_...`）。
   - 图片引用 `![alt](path)`：**路径与语法原样保留**，alt 文字可译可不译（建议译）。
   - Markdown 链接的 URL 部分 `](...)` 原样保留；链接显示文字可译。
   - 表格的 Markdown 结构（`|`、`---`）原样保留，只译单元格中的自然语言。
2. **标题层级 `#` 数量原样保留**，只译标题文字。标题里的专有名词按术语表处理。
3. 提示框 `> **Note**` / `> **Warning**` → 译为 `> **注意**` / `> **警告**`，引用格式保留。
4. 保留原文的段落顺序、列表结构、缩进。
5. 不要新增、删减、解释性扩写内容。忠实翻译。
6. 商标符号 `™` 保留。

## 术语表（统一译法；括号内为首次出现可加的英文原文）
- AudioReach → **AudioReach**（品牌名不译）
- AudioReach Engine (ARE) → **AudioReach 引擎（ARE）**
- AudioReach Creator (ARC) → **AudioReach Creator（ARC）**（工具名不译）
- Signal Processing Framework (SPF) → **信号处理框架（SPF）**
- AudioReach Graph Services (ARGS) → **AudioReach 图服务（ARGS）**
- Graph Services Layer (GSL) → **图服务层（GSL）**
- Generic Packet Router (GPR) → **通用包路由器（GPR）**
- Platform Abstraction Layer (POSAL) → **平台抽象层（POSAL）**
- graph → **图**；audio graph → **音频图**
- subgraph → **子图**
- module → **模块**
- container → **容器**
- use case → **用例**
- endpoint → **端点**；source/sink endpoint → **源端点 / 汇端点**
- stream / device → **流 / 设备**（stream-leg / device-leg → **流侧 / 设备侧**，首次可注 stream-leg）
- key vector → **键向量**
- Graph Key Vector (GKV) → **图键向量（GKV）**
- Calibration Key Vector (CKV) → **校准键向量（CKV）**
- Tag Key Vector (TKV) → **标签键向量（TKV）**
- key / value → **键 / 值**；key-value → **键值**
- calibration → **校准**；tuning → **调参 / 调校**
- ACDB (Audio Calibration Database) → **音频校准数据库（ACDB）**
- CAPI (Common Audio Processing Interface) → **CAPI**（不译，首次可注全称）
- topology → **拓扑**
- routing → **路由**
- port → **端口**
- data path / control path → **数据通路 / 控制通路**
- payload → **负载 / 载荷**（统一用“负载”）
- offload → **offload / 卸载**（音频 offload 语境保留 offload）
- runtime → **运行时**
- framework → **框架**
- host / target → **主机侧 / 目标侧（目标设备）**
- off-target / on-target → **脱机（off-target） / 在机（on-target）**
- plugin / plug-in → **插件**
- porting → **移植**
- build → **构建**（名词“构建产物”）；binary → **二进制**
- session → **会话**
- thread → **线程**
- buffer → **缓冲区**
- sample rate / bit width / channels → **采样率 / 位宽 / 通道数**
- PCM / non-PCM → 原样
- H2XML → 原样
- ASoC / ALSA / DAPM / tinyalsa / PulseAudio / Yocto / meta-layer → 原样

## 风格提示
- 用“我们 / 你”式的工程博客口吻可以，但以陈述为主，避免口水。
- 长英文被动句转为中文主动句。
- 中英文之间、中文与行内代码之间，按习惯自然留空格（不强制）。
- 句末统一用中文标点。
