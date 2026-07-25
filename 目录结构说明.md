# 代码目录结构说明（按 Qualcomm / AOSP 代码树层级归置）

> 本仓库为高通 **AudioReach 新架构**（Android 14/15+，骁龙 8 Gen2 及以后平台）的音频代码集合。
> 各子模块已按 Qualcomm / AOSP 实际源码树层级归置，方便区分 **Framework / HAL / 用户空间 / DSP / Kernel** 各层。

---

## 分层结构总览

```
qcom-audio/
│
├── frameworks/                         ① Framework 层（Google 纯正 AOSP）
│   ├── av/                                音频框架：AudioFlinger / AudioPolicy / AudioTrack
│   └── base/                              系统框架：AudioManager / AudioService（Java 层）
│
├── system/
│   └── media/                          ① Framework 层：音频公共库（audio_utils 等）
│
├── hardware/
│   ├── interfaces/                     ② HAL 接口层（Google 定义的 AIDL Audio HAL 标准）
│   └── qcom/
│       └── audio-aidl/                 ③ HAL 实现层：ARHAL —— 高通对 AIDL Audio HAL 的实现
│
└── vendor/qcom/opensource/            —— 高通厂商私有代码
    ├── agm/                            ④ 用户空间：AGM（Audio Graph Manager）音频图管理器
    ├── pal/                            ④ 用户空间：PAL（Platform Abstraction Layer）平台抽象层
    ├── graphservices/                  ④ 用户空间：GSL / ACDB（Graph Service Layer 图服务层）
    ├── audioreach-engine/              ⑤ DSP 侧：SPF（Signal Processing Framework）信号处理框架
    ├── audioreach-conf/                ⑥ 配置：ACDB / Graph 拓扑定义
    └── audio-kernel-ar/                ⑦ Kernel 层：AR ASoC 驱动 / GPR 驱动
```

---

## 各层角色对照表

| 层级 | 目录 | 子模块（原名） | 在 AudioReach 架构中的角色 | 归属 |
|------|------|----------------|----------------------------|------|
| ① Framework | `frameworks/av` | aosp-frameworks-av | AudioFlinger / AudioPolicyService，上层音频框架 | Google 纯正 AOSP |
| ① Framework | `frameworks/base` | aosp-frameworks-base | AudioManager / AudioService（Java 系统服务） | Google 纯正 AOSP |
| ① Framework | `system/media` | aosp-system-media | 音频公共库（audio_utils 等） | Google 纯正 AOSP |
| ② HAL 接口 | `hardware/interfaces` | aosp-hardware-interfaces | AIDL Audio HAL 标准接口定义（IModule / IStream 等） | Google 纯正 AOSP |
| ③ HAL 实现 | `hardware/qcom/audio-aidl` | ahal-aidl | **ARHAL**：高通实现的 AIDL Audio HAL，对接上层框架 | Qualcomm |
| ④ 用户空间 | `vendor/qcom/opensource/agm` | agm | **AGM**：音频图管理器，与 GSL 一起决定 DSP 图长什么样 | Qualcomm |
| ④ 用户空间 | `vendor/qcom/opensource/pal` | pal | **PAL**：平台抽象层，管理 usecase / 设备路由 / 参数 | Qualcomm |
| ④ 用户空间 | `vendor/qcom/opensource/graphservices` | graphservices | **GSL / ACDB**：图服务层，SPF 的驱动层 | Qualcomm |
| ⑤ DSP 侧 | `vendor/qcom/opensource/audioreach-engine` | ar-engine | **SPF**：DSP 上真正干活的信号处理框架、处理模块 | Qualcomm |
| ⑥ 配置 | `vendor/qcom/opensource/audioreach-conf` | ar-conf | **ACDB / Graph 配置**：校准数据库、图拓扑定义 | Qualcomm |
| ⑦ Kernel | `vendor/qcom/opensource/audio-kernel-ar` | audio-kernel-ar | **内核驱动**：AR ASoC 驱动、GPR 跨核 IPC 驱动 | Qualcomm |

---

## 数据流方向（从 App 到 DSP）

```
App (AudioTrack/MediaPlayer)
   │
   ▼  ① frameworks/base  →  frameworks/av (AudioFlinger/AudioPolicy)
   │
   ▼  ② hardware/interfaces  (AIDL Audio HAL 接口)
   │
   ▼  ③ hardware/qcom/audio-aidl  (ARHAL：高通 HAL 实现)
   │
   ▼  ④ vendor/qcom/opensource/pal + agm + graphservices  (用户空间：路由/图管理/GSL)
   │
   ▼  ⑦ vendor/qcom/opensource/audio-kernel-ar  (内核：GPR 驱动 → 跨核传输)
   │
   ▼  ⑤ vendor/qcom/opensource/audioreach-engine  (DSP 侧 SPF：加载模块、构建图、跑数据)
        └── ⑥ audioreach-conf (ACDB/Graph 配置在建图时被加载)
```

---

## 备注

- **PAL 未被移除**：AudioReach 架构保留了 PAL，但它是新的 AudioReach-PAL（对接 AGM/GSL），并非旧 APM 架构中对接 APR 的 legacy PAL。这是本仓库确实为新架构的标志之一。
- 各子模块通过 `.gitmodules` 管理，`path` 已同步更新到上述新路径；`git submodule status` 已验证全部健全。
- `frameworks/`、`system/`、`hardware/interfaces` 为 Google 纯正 AOSP 代码，仅作对照参考；高通改动集中在 `hardware/qcom/` 与 `vendor/qcom/opensource/`。
