# Platform Porting Guide

## Porting Dependency and requirements

## Porting Manual

AudioReach is designed with cross-platform requirement in mind. In order to port AudioReach onto desired hardware and software platform, developer are expected to develop platform & OS abstraction layers and hardware & software endpoint modules. In addition, platform should provide execution environment for AudioReach components to run on.

### Platform & OS Abstraction Layer

-
  **ARGS OSAL**

  Platform specific OSAL implementation is required for porting AudioReach Graph Services and Signal Processing Engine.
  See[Operating System Abstraction Layer](../design/args_design.html#args-osal)for functionalities to be implemented.Refer to[OSAL API’s](https://github.com/Audioreach/audioreach-graphservices/tree/master/ar_osal/api)and[Linux Implementation](https://github.com/Audioreach/audioreach-graphservices/tree/master/ar_osal/src/linux)for more details.
-
  **ARE POSAL**

  Custom POSAL implementation must provide implementation for following functionalities.

    - Signal, Mutex, condition var, channel, thread
    - Timer
    - Cache, memory
    - Memory map
    - Data logging (PCM and Binary data),
    - Thread priority mapping
    - Power Voting (MIPS and Memory bandwidth voting)

  Refer to [POSAL API’s](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/posal/inc) and [Generic and Linux Implementation](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/posal/src) for more details.
-
  **GPR platform layer**

  To implement GPR platform layer refer to [Custom Platform Wrapper](../design/gpr_design.html#gpr-custom-platform-wrapper) and [Custom Domain ID](../design/gpr_design.html#gpr-custom-domain-id). See [gpr_init_lx_wrapper.c](https://github.com/Audioreach/audioreach-graphservices/blob/master/gpr/platform/linux/gpr_init_lx_wrapper.c) for linux based platform layer.
-
  **GPR datalink layer**

  To implement custom datalink layer refer to steps and code example at [Custom IPC Data Link or Transport Layer](../design/gpr_design.html#gpr-custom-ipc-data-link). See [gpr_lx.c](https://github.com/Audioreach/audioreach-graphservices/blob/master/gpr/datalinks/gpr_lx/src/gpr_lx.c) for linux based datalink layer.

### Hardware & Software Endpoint Modules

Refer ALSA Endpoint module code [here](https://github.com/Audioreach/audioreach-engine/tree/master/fwk/platform/modules/generic/endpoint/alsa_device).

### Provide Execution Environment

Platform should provide execution environment for AudioReach components like:

- GSL ( [gsl_init()](https://github.com/Audioreach/audioreach-graphservices/blob/master/gsl/src/gsl_main.c) )
- ARE Framework ( [spf_framework_pre_init()](https://github.com/Audioreach/audioreach-engine/blob/master/fwk/spf/utils/cmn/src/spf_main.c) and [spf_framework_post_init()](https://github.com/Audioreach/audioreach-engine/blob/master/fwk/spf/utils/cmn/src/spf_main.c) )

For example, as part of AGM initialization ( [agm_init()](https://github.com/Audioreach/audioreach-graphmgr/blob/master/service/src/agm.c) ), GSL and ARE framework can be initialized. Where GSL in turn initializes OS Abstraction layer (OSAL), Audio Calibration Database (ACDB) and other utilities (say for logging data), framework pre init includes initializing Audio Module Data Base (AMDB), Data Logging Service (DLS), Integrated Resource Monitor (IRM) and framework post init initializes Audio Processing Manager (APM) service.

#### Sample ARE Framework init execution environment

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
