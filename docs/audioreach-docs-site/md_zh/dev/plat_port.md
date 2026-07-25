# 平台移植指南

## 移植依赖与要求

## 移植手册

AudioReach 在设计时就考虑了跨平台需求。为了将 AudioReach 移植到目标硬件和软件平台上，开发者需要开发平台与 OS 抽象层以及硬件与软件端点模块。此外，平台还应为 AudioReach 组件提供可运行的执行环境。

### 平台与 OS 抽象层

-
  **ARGS OSAL**

  移植 AudioReach 图服务和信号处理引擎需要平台特定的 OSAL 实现。
  有关需要实现的功能，请参阅[Operating System Abstraction Layer](../design/args_design.md)。更多细节请参阅[OSAL API’s](https://github.com/Audioreach/audioreach-graphservices/tree/master/ar_osal/api)和[Linux Implementation](https://github.com/Audioreach/audioreach-graphservices/tree/master/ar_osal/src/linux)。
-
  **ARE POSAL**

  自定义的 POSAL 实现必须为以下功能提供实现。

    - Signal、Mutex、condition var、channel、thread
    - Timer
    - Cache、memory
    - Memory map
    - 数据日志记录（PCM 和二进制数据）
    - 线程优先级映射
    - Power Voting（MIPS 和内存带宽投票）

  更多细节请参阅 [POSAL API’s](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/posal/inc) 和 [Generic and Linux Implementation](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/posal/src)。
-
  **GPR 平台层**

  要实现 GPR 平台层，请参阅 [Custom Platform Wrapper](../design/gpr_design.md) 和 [Custom Domain ID](../design/gpr_design.md)。有关基于 Linux 的平台层，请参阅 [gpr_init_lx_wrapper.c](https://github.com/Audioreach/audioreach-graphservices/blob/master/gpr/platform/linux/gpr_init_lx_wrapper.c)。
-
  **GPR 数据链路层**

  要实现自定义数据链路层，请参阅 [Custom IPC Data Link or Transport Layer](../design/gpr_design.md) 中的步骤和代码示例。有关基于 Linux 的数据链路层，请参阅 [gpr_lx.c](https://github.com/Audioreach/audioreach-graphservices/blob/master/gpr/datalinks/gpr_lx/src/gpr_lx.c)。

### 硬件与软件端点模块

ALSA 端点模块代码请参阅[此处](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/modules/generic/endpoint/alsa_device)。

### 提供执行环境

平台应为 AudioReach 组件提供执行环境，例如：

- GSL（ [gsl_init()](https://github.com/Audioreach/audioreach-graphservices/blob/master/gsl/src/gsl_main.c) ）
- ARE 框架（ [spf_framework_pre_init()](https://github.com/Audioreach/audioreach-engine/blob/master/fwk/spf/utils/cmn/src/spf_main.c) 和 [spf_framework_post_init()](https://github.com/Audioreach/audioreach-engine/blob/master/fwk/spf/utils/cmn/src/spf_main.c) ）

例如，作为 AGM 初始化（ [agm_init()](https://github.com/Audioreach/audioreach-graphmgr/blob/master/service/src/agm.c) ）的一部分，可以初始化 GSL 和 ARE 框架。其中 GSL 又会初始化 OS 抽象层（OSAL）、音频校准数据库（ACDB）以及其他实用工具（比如用于数据日志记录的工具），框架的 pre init 包括初始化 Audio Module Data Base（AMDB）、Data Logging Service（DLS）、Integrated Resource Monitor（IRM），框架的 post init 则初始化 Audio Processing Manager（APM）服务。

#### ARE 框架 init 执行环境示例

```C
// Sample framework init implementation.
ar_result_t audio_framework_init(void)
{
   ar_result_t result = AR_EOK;

   /* Init global state structure */
   posal_init();

   /* Init gpr infrastructure */
   result = gpr_init();
   if (result != AR_EOK)
   {
     //Handle failure. Update return code.
   }

   // Init spf framwork. Call pre_init() and post_init() functions.
   spf_framework_pre_init();

   spf_framework_post_init();

   printf("spf_framework_init done, framework ready to receive commands.");

   return result;
}
```
