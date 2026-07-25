# POSAL API’s

## posal_cache

本文件包含用于缓存操作的实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef void *posal_mem_addr_t`**

## posal_data_log

Posal 数据日志 API。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`SPF_LOG_PREFIX`**

Typedefs

**`typedef enum posal_data_log_format_t posal_data_log_format_t`**

日志数据格式。

**`typedef enum posal_data_log_mode_t posal_data_log_mode_t`**

**`typedef struct posal_data_log_pcm_info_t posal_data_log_pcm_info_t`**

供日志实用工具用户使用的 PCM 数据信息。

**`typedef struct posal_data_log_fmt_info_t posal_data_log_fmt_info_t`**

被记录数据的格式：PCM 或比特流。

**`typedef struct posal_data_log_info_t posal_data_log_info_t`**

供日志实用工具用户使用的日志头与数据负载信息。

Enums

**`enum posal_data_log_format_t`**

日志数据格式。

*Values:*

**`enumerator LOG_DATA_FMT_PCM`**

PCM 数据格式。

**`enumerator LOG_DATA_FMT_BITSTREAM`**

比特流数据格式。

**`enumerator LOG_DATA_FMT_RAW`**

原始数据格式。

**`enum posal_data_log_mode_t`**

*Values:*

**`enumerator LOG_DEFAULT`**

**`enumerator LOG_IMMEDIATE`**

Functions

**[`bool_t`](args_arosal.md) `posal_data_log_code_status`(`uint32_t log_code`)**

此函数检查该日志代码是否已启用。

**Dependencies** None

**Returns:**

如果日志代码已启用则返回 TRUE，禁用则返回 FALSE。

**`uint32_t posal_data_log_get_max_buf_size`()**

此函数给出日志记录所允许的最大数据包大小。

**Dependencies** None

**`void *posal_data_log_alloc`(`uint32_t buf_Size`, `uint32_t log_code`, `posal_data_log_format_t data_fmt`)**

为 PCM/比特流数据日志记录分配一个日志数据包。

**Associated data types**#log_data_format

**Dependencies** None.

**Parameters:**

- **buf_Size** – **[in]** 数据负载的大小，不包括日志头。
- **log_code** – **[in]** 此日志数据包的日志代码。
- **data_fmt** – **[in]** PCM 或比特流数据格式。

**Returns:**

指向已分配日志数据包负载的指针。如果缓冲区分配失败或日志代码被禁用，则返回 NULL。

**`ar_result_t posal_data_log_commit`(`void *log_pkt_payload_ptr`, `posal_data_log_info_t *log_info_ptr`)**

填充已分配日志数据包的日志头与数据负载，并提交该数据包以进行日志记录。

Nonzero — Failure

**Dependencies** None

**Parameters:**

- **log_pkt_payload_ptr** – **[in]** 指向已分配日志数据包负载的指针。
- **log_tap_id** – **[in]** 日志数据包的抽头点（tap point）ID。
- **session_id** – **[in]** 日志数据包的会话 ID。
- **buf_size** – **[in]** 日志数据包的负载大小。

**Returns:**

0 — Success

**`ar_result_t posal_data_log_alloc_commit`(`posal_data_log_info_t *log_info_ptr`)**

分配日志数据包，填充日志头与数据负载，并提交该数据包以进行日志记录。

**Associated data types**#log_info

Nonzero — Failure

**Dependencies** None

**Parameters:**

**log_info_ptr** – **[in]** 指向对象的指针，该对象包含供日志实用工具客户端使用的日志头与数据负载信息。

**Returns:**

0 — Success

**`void posal_data_log_free`(`void *log_pkt_payload_ptr`)**

此函数在出错场景下释放数据日志缓冲区。

**Dependencies** None

**Parameters:**

**log_ptr** – **[in]** ：要释放的数据日志缓冲区的负载

**Returns:**

None.

**`struct posal_data_log_pcm_info_t`**

*#include <posal_data_log.h>*供日志实用工具用户使用的 PCM 数据信息。

Public Members

**`uint32_t sampling_rate`**

PCM 采样率。8000 Hz、48000 Hz 等。

**`uint16_t num_channels`**

PCM 流中的通道数。

**`uint8_t bits_per_sample`**

PCM 数据的每样本位数。

**`uint8_t interleaved`**

指定数据是否为交织（interleaved）格式。

**`uint8_t q_factor`**

日志数据包的 q factor 信息。

**`uint8_t data_format`**

日志数据包的 data_format 信息。

**`uint16_t *channel_mapping`**

通道映射数组。

**`struct posal_data_log_fmt_info_t`**

*#include <posal_data_log.h>*被记录数据的格式：PCM 或比特流。

Public Members

**`posal_data_log_pcm_info_t pcm_data_fmt`**

PCM 数据的格式。

**`uint32_t media_fmt_id`**

比特流数据的格式。

**`struct posal_data_log_info_t`**

*#include <posal_data_log.h>*供日志实用工具用户使用的日志头与数据负载信息。

Public Members

**`uint32_t log_code`**

日志数据包的日志代码。

**`int8_t *buf_ptr`**

指向要记录的缓冲区的指针。

**`uint32_t buf_size`**

要记录的负载大小，以字节为单位。

**`uint32_t session_id`**

日志数据包的会话 ID。

**`uint32_t log_tap_id`**

抽头点的 GUID。

**`uint64_t log_time_stamp`**

以微秒为单位的时间戳。

**`posal_data_log_format_t data_fmt`**

日志数据包的数据格式。

**`posal_data_log_fmt_info_t data_info`**

指向数据包信息的指针。

**`uint32_t *seq_number_ptr`**

对客户端共享的序列号变量的引用。

## posal_globalstate

本文件包含 posal 环境的全局状态结构。此状态包括系统级信息，例如活动线程数量和 malloc 计数器。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

**`struct posal_mem_stats_t`**

*#include <posal_globalstate.h>*在测试用例运行期间获得的内存使用统计信息。

Public Members

**`uint32_t num_mallocs`**

到测试当前时刻为止的内存分配总次数。

**`uint32_t num_frees`**

到测试当前时刻为止内存被释放的总次数。

**`uint32_t curr_heap`**

测试当前时刻的堆使用量。

**`uint32_t peak_heap`**

到测试当前时刻为止的堆使用峰值。

**`struct posal_globalstate_t`**

*#include <posal_globalstate.h>*用于跟踪线程和队列等资源的全局结构。此结构用于调试和泄漏检查等任务。

Public Members

**`posal_mem_stats_t avs_stats[POSAL_HEAP_MGR_MAX_NUM_HEAPS + 1]`**

Audio-Voice 子系统（AVS）线程的堆统计信息。

此数量由一个默认堆加上 #POSAL_HEAP_MGR_MAX_NUM_HEAPS 个非默认堆组成。

**`posal_mem_stats_t non_avs_stats`**

非 AVS 线程的堆统计信息。

**`volatile int32_t nSimulatedMallocFailCount`**

如果失败计数 > 0，则对内存分配递减计数直至零，然后模拟内存不足。此计数用于测试。

**`posal_atomic_word_t nMsgQs`**

队列计数器，用于帮助生成唯一名称。

**`posal_atomic_word_t nMemRegions`**

系统中内存区域数量的计数器。

**`posal_mutex_t mutex`**

用于此结构线程安全的互斥锁。

**`posal_memorymap_client_t *mem_map_client_list[POSAL_MEMORY_MAP_MAX_CLIENTS]`**

系统中内存映射客户端的链表。

**`uint32_t num_registered_memmap_clients`**

**`volatile uint32_t bEnableQLogging`**

记录进入队列和离开队列的命令。

**`volatile uint32_t uSvcUpStatus`**

指定 aDSP 静态服务是否已启动并就绪。

**[`bool_t`](args_arosal.md) `is_global_init_done`**

用于在全局初始化完成时设置的标志。

**`struct posal_memorymap_client_t`**

*#include <posal_globalstate.h>*维护一个注册到 posal_memorymap 的客户端链表。

Public Members

**`posal_memorymap_node_t *pMemMapListNode`**

此客户端的内存映射节点列表。

**`posal_mutex_t mClientMutex`**

访问该列表的互斥锁。

**`uint32_t client_id`**

客户端 ID。

## posal_heapmgr

本文件包含用于内存分配与释放的实用工具。本文件为 C 和 C++ 提供内存分配函数和宏。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_internal_inline

内部定义。通过进行内联调用来帮助优化。由于向后兼容性方面的考虑，不得被共享库使用。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`static inline uint32_t posal_channel_wait_inline`(`posal_channel_t pChannel`, `uint32_t unEnableBitfield`)**

**`static inline uint32_t posal_channel_poll_inline`(`posal_channel_t pChannel`, `uint32_t unEnableBitfield`)**

**`static inline` [`bool_t`](args_arosal.md) `posal_island_get_island_status_inline`(`void`)**

**`static inline void posal_mutex_unlock_inline`(`posal_mutex_t posal_mutex`)**

**`static inline void posal_mutex_lock_inline`(`posal_mutex_t posal_mutex`)**

**`static inline posal_channel_t posal_signal_get_channel_inline`(`posal_signal_t p_signal`)**

**`static inline uint32_t posal_signal_get_channel_bit_inline`(`posal_signal_t p_signal`)**

**`static inline void posal_signal_clear_inline`(`posal_signal_t p_signal`)**

**`static inline` [`bool_t`](args_arosal.md) `posal_signal_is_set_inline`(`posal_signal_t p_signal`)**

**`struct posal_channel_internal_t`**

*#include <posal_internal_inline.h>*Public Members

**`qurt_signal2_t anysig`**

任意 32 位信号通道。

**`uint32_t unBitsUsedMask`**

已用位的掩码记账。1 — 已用 0 — 可用

**`struct posal_signal_internal_t`**

*#include <posal_internal_inline.h>*由事件触发的信号，或用于触发事件的信号。该信号在某个通道位（channel bit）上合并。接收信号的唯一方式是通过其关联的通道。

Public Members

**`posal_channel_internal_t *pChannel`**

指向关联通道的指针。

**`uint32_t unMyChannelBit`**

此信号的通道位域。

## posal_island

本文件包含 island 实用工具的声明。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Enums

**`enum posal_island_heap_t`**

*Values:*

**`enumerator POSAL_ISLAND_HEAP_Q6_TCM`**

**`enumerator POSAL_ISLAND_HEAP_LPASS_TCM`**

**`enumerator POSAL_ISLAND_HEAP_LLC`**

**`enumerator POSAL_ISLAND_HEAP_NUM_SUPPORTED`**

Functions

**`POSAL_HEAP_ID posal_private_get_island_heap_id_v2`(`uint32_t island_heap_type`)**

用于获取 island 堆 id 的私有 API

**`posal_mem_t posal_private_get_mem_type_from_heap_type`(`uint32_t island_heap_type`)**

用于获取 posal 内存类型的私有 API

**`ar_result_t posal_island_trigger_island_exit`(`void`)**

此函数处理 island 退出。

**Dependencies** None.

**Returns:**

成功（0）或失败（非零）的指示。

**`static inline ar_result_t posal_island_trigger_island_exit_inline`(`void`)**

当未定义 USES_AUDIO_IN_ISLAND 时用于退出 island 的内联函数

**Dependencies** None.

**Returns:**

成功（0）或失败（非零）的指示。

**[`bool_t`](args_arosal.md) `posal_island_get_island_status`(`void`)**

此函数获取 island 模式状态。

返回一个值，指示底层系统是否正在 island 模式下执行。

**Dependencies** None.

**Returns:**

0 - 正常模式。1 - island 模式。

**`static inline POSAL_HEAP_ID posal_get_island_heap_id`(`void`)**

**`static inline POSAL_HEAP_ID posal_get_island_heap_id_v2`(`posal_island_heap_t heap_type`)**

**`static inline POSAL_HEAP_ID posal_get_heap_id`(`posal_mem_t mem_type`)**

**`static inline posal_mem_t posal_get_mem_type_from_heap_type`(`posal_island_heap_t heap_type`)**

Variables

**`POSAL_HEAP_ID spf_mem_island_heap_id`**

默认 island 堆 = 默认为 Q6 TCM。

## posal_memorymap

本文件包含用于共享内存的内存映射与取消映射的实用工具。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

**`struct posal_memorymap_node_t`**

*#include <posal_memorymap.h>*Public Members

**`uint32_t shmem_id`**

用于映射此共享内存区域的唯一标识符

**`uint32_t MemPool`**

创建该内存区域所用的内存池。

**`uint16_t unNumContPhysReg`**

此节点中的物理内存区域数量。

**`int16_t ref_count`**

引用计数，客户端可以递增它以锁定此内存映射句柄。

只有当 ref_count 达到零时才能执行取消映射。

当客户端不再使用此内存映射句柄时，必须递减 ref_count。

**`uint32_t mapping_mode`**

指定映射是物理的还是虚拟的，或者它是否为物理偏移。

**`uint32_t reserved`**

保留字段，用于确保此结构大小对齐到 64 字节。

**`posal_memorymap_node_t *pNext`**

指向链表中下一个节点的指针。

@tblsubhd{If unNumContPhysReg is greater than 1} 除了跟在此结构之后的若干个 posal_memorymap_region_record_t 结构外，还会再跟一个 ContPhysReg，用于表示所有 ContPhysReg 的主区域（称为*虚拟内存区域*）。

释放这些区域时，后续的所有空间也会一并被释放。

**`struct posal_memorymap_shm_region_t`**

*#include <posal_memorymap.h>*连续的共享内存区域，带有起始地址和大小。

Public Members

**`uint32_t shm_addr_lsw`**

要映射的内存区域共享内存地址的低 32 位。

**`uint32_t shm_addr_msw`**

要映射的内存区域共享内存地址的高 32 位。

由 shm_addr_lsw 和 shm_addr_msw 字组成的 64 位数值必须是连续内存，且必须 4 KB 对齐。

对于 32 位共享内存地址，此字段必须设置为 0。对于 36 位共享内存地址，第 31 位到第 4 位必须设置为 0。对于 64 位共享内存地址，可为任意 32 位值。

**`uint32_t mem_size`**

共享内存区域的大小。

共享内存区域中的字节数。

4 KB 的倍数

底层操作系统必须始终将这些区域映射为虚拟连续内存，但内存大小必须是 4 KB 的倍数，以避免在虚拟连续映射内存中出现间隙。

**`struct posal_memorymap_mem_region_attrib_t`**

*#include <posal_memorymap.h>*内存映射区域属性。

Public Members

**`uint32_t base_phy_addr_lsw`**

64 位内存区域起始（基）物理地址的低 32 位。

**`uint32_t base_phy_addr_msw`**

64 位内存区域起始（基）物理地址的高 32 位。

由 mem_reg_base_phy_addr_lsw 和 mem_reg_base_phy_addr_msw 字组成的 64 位数值必须是连续内存，且必须 4 KB 对齐。

对于 32 位共享内存地址，此字段必须设置为 0。对于 36 位共享内存地址，第 31 位到第 4 位必须设置为 0。对于 64 位共享内存地址，可为任意 32 位值。

**`uint32_t mem_reg_size`**

共享内存区域的大小。

共享内存区域中的字节数。

4 KB 的倍数

底层操作系统必须始终将这些区域映射为虚拟连续内存，但内存大小必须是 4 KB 的倍数，以避免在虚拟连续映射内存中出现间隙。

**`uint32_t base_virt_addr`**

内存区域起始（基）虚拟地址。

**`uint32_t req_virt_adrr`**

对应于所请求物理地址的虚拟地址。

**`uint32_t rem_reg_size`**

从所请求物理地址开始（含该物理地址）的剩余内存区域大小：

（[mem_reg_base_phy_addr_msw,mem_reg_base_phy_addr_lsw] + mem_reg_size - [所请求的物理地址]）

**`struct posal_mem_map_v2_input_args_t`**

*#include <posal_memorymap.h>*Public Members

**`uint32_t unique_shmem_id_24bit`**

**`uint32_t client_token`**

唯一共享内存 Id，只有低 24 位有效。如果设置了唯一 shm id，它将在输出参数中作为内存映射句柄返回。

**`posal_memorymap_shm_region_t *shm_mem_reg_ptr`**

Posal memorymap 驱动已注册的客户端令牌

**`uint16_t num_shm_reg`**

指向要映射的共享内存区域数组的指针。

**[`bool_t`](args_arosal.md) `is_cached`**

数组中共享内存区域的数量。

**[`bool_t`](args_arosal.md) `is_offset_map`**

指示内存是缓存的还是非缓存的

**`POSAL_MEMORYPOOLTYPE pool_id`**

指示该映射是基于偏移的还是基于指针的。

**`POSAL_HEAP_ID heap_id`**

此区域映射到的内存池 ID。

## posal_mutex

本文件包含互斥锁实用工具。为进行线程安全编程，始终使用递归互斥锁。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void posal_mutex_lock`(`posal_mutex_t posal_mutex`)**

锁定一个互斥锁。始终使用递归互斥锁。

**Associated data types**posal_mutex_t

**Dependencies** 在调用此函数之前，该对象必须已被创建并初始化。

**Parameters:**

**posal_mutex** – **[in]** 互斥锁对象句柄。

**Returns:**

None.

**`ar_result_t posal_mutex_try_lock`(`posal_mutex_t posal_mutex`)**

尝试锁定一个互斥锁。如果互斥锁已被锁定且不可用，则返回失败。

**Associated data types**posal_mutex_t

**Dependencies** 在调用此函数之前，该对象必须已被创建并初始化。

**Parameters:**

**posal_mutex** – **[in]** 互斥锁对象句柄。

**Returns:**

成功（0）或失败（非零）的指示。

**`void posal_mutex_unlock`(`posal_mutex_t posal_mutex`)**

解锁一个互斥锁。始终使用递归互斥锁。

**Associated data types**posal_mutex_t

**Dependencies** 在调用此函数之前，该对象必须已被创建并初始化。

**Parameters:**

**posal_mutex** – **[in]** 互斥锁对象句柄。

**Returns:**

None.

## posal_power_mgr

PM 的轻量封装。主要用于服务性能剖析（profiling）。目标不是隐藏 MMPM/PM 的细节。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`PM_SERVER_CLIENT_TOKEN_PREFIX`**

**`PM_SERVER_CLIENT_TOKEN_LENGTH`**

**`PM_SERVER_CLIENT_NAME_LENGTH`**

**`PM_SERVER_CLIENT_NAME_MAX_LENGTH`**

Typedefs

**`typedef void *posal_pm_handle_t`**

**`typedef enum posal_pm_mode_t posal_pm_mode_t`**

PM island 类型

**`typedef enum posal_pm_island_type_t posal_pm_island_type_t`**

PM island 投票（Vote）

**`typedef enum posal_pm_island_vote_type_t posal_pm_island_vote_type_t`**

**`typedef enum posal_pm_cpu_lpr_id_t posal_pm_cpu_lpr_id_t`**

PM CPU LPR 投票类型

**`typedef enum posal_pm_cpu_lpr_vote_type_t posal_pm_cpu_lpr_vote_type_t`**

注册信息

**`typedef struct posal_pm_register_t posal_pm_register_t`**

**`typedef struct posal_pm_mpps_t posal_pm_mpps_t`**

**`typedef struct posal_pm_bw_t posal_pm_bw_t`**

**`typedef struct posal_pm_sleep_latency_t posal_pm_sleep_latency_t`**

**`typedef struct posal_pm_island_vote_t posal_pm_island_vote_t`**

**`typedef struct posal_pm_cpu_lpr_vote_t posal_pm_cpu_lpr_vote_t`**

**`typedef struct posal_pm_resources_t posal_pm_resources_t`**

**`typedef struct posal_pm_request_info_t posal_pm_request_info_t`**

**`typedef struct posal_pm_release_info_t posal_pm_release_info_t`**

Enums

**`enum posal_pm_mode_t`**

*Values:*

**`enumerator PM_MODE_DEFAULT`**

非 island、不可抑制（non-suppressible）

**`enumerator PM_MODE_ISLAND`**

island、可抑制（suppressible）

**`enumerator PM_MODE_ISLAND_DUTY_CYCLE`**

不是 island 容器，但仅带宽（BW）投票可抑制（主要用于 BT A2DP 用例）

**`enum posal_pm_island_type_t`**

*Values:*

**`enumerator PM_ISLAND_TYPE_DEFAULT`**

**`enumerator PM_ISLAND_TYPE_LOW_POWER`**

< 默认 island 类型 用于进入 STD island 的 island 类型

**`enumerator PM_ISLAND_TYPE_LOW_POWER_2`**

用于进入 LLC island 的 island 类型

**`enum posal_pm_island_vote_type_t`**

*Values:*

**`enumerator PM_ISLAND_VOTE_ENTRY`**

为 island 进入状态投出的 island 投票

**`enumerator PM_ISLAND_VOTE_EXIT`**

为 island 退出状态投出的 island 投票

**`enumerator PM_ISLAND_VOTE_DONT_CARE`**

为 island don't care 状态投出的 island 投票

**`enum posal_pm_cpu_lpr_id_t`**

*Values:*

**`enumerator PM_LPR_CPU_SS_SLEEP`**

**`enumerator PM_LPR_CPU_MAX`**

**`enum posal_pm_cpu_lpr_vote_type_t`**

*Values:*

**`enumerator PM_VOTE_FOR_CPU_LPR_SUB_SYSTEM_SLEEP`**

**`enumerator PM_VOTE_AGAINST_CPU_LPR_SUB_SYSTEM_SLEEP`**

**`enumerator PM_VOTE_NUM_CPU_LPR`**

Functions

**`ar_result_t posal_power_mgr_request`(`posal_pm_request_info_t *request_info_ptr`)**

向 ADSPPM 发送请求

**Dependencies** None.

**Returns:**

返回错误码。

**`ar_result_t posal_power_mgr_release`(`posal_pm_release_info_t *release_info_ptr`)**

向 ADSPPM 发送释放

**Dependencies** None.

**Returns:**

返回错误码。

**`ar_result_t posal_power_mgr_register`(`posal_pm_register_t register_info`, `posal_pm_handle_t *pm_handle_pptr`, `posal_signal_t wait_signal`, `uint32_t log_id`)**

为 kpps 和 bw 进行注册

**Dependencies** None.

**Returns:**

返回错误码。

**`ar_result_t posal_power_mgr_deregister`(`posal_pm_handle_t *pm_handle_pptr`, `uint32_t log_id`)**

从 ADSPPM 注销

**Dependencies** None.

**Returns:**

返回错误码。

**[`bool_t`](args_arosal.md) `posal_power_mgr_is_registered`(`posal_pm_handle_t pm_handle_ptr`)**

如果客户端已注册则返回 true。

**`ar_result_t posal_power_mgr_request_max_out`(`posal_pm_handle_t pm_handle_ptr`, `posal_signal_t wait_signal`, `uint32_t log_id`)**

拉高总线和 Q6 时钟。

**`ar_result_t posal_power_mgr_release_max_out`(`posal_pm_handle_t pm_handle_ptr`, `uint32_t log_id`, `uint32_t delay_ms`)**

释放总线和 Q6 时钟。

**`void posal_power_mgr_init`()**

初始化结构和互斥锁（如果有）

**`void posal_power_mgr_deinit`()**

反初始化结构和互斥锁（如果有）

**`ar_result_t posal_power_mgr_send_command`(`uint32_t msg_opcode`, `void *payload_ptr`, `uint32_t payload_size`)**

向 PM SERVER 发送消息命令

**`struct posal_pm_register_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_mode_t mode`**

PM 模式

**`posal_pm_island_type_t island_type`**

Island 类型

**`struct posal_pm_mpps_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

**`uint32_t value`**

**`uint64_t floor_clk`**

**`struct posal_pm_bw_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

**`uint32_t value`**

**`struct posal_pm_sleep_latency_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

**`uint32_t value`**

**`struct posal_pm_island_vote_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

**`posal_pm_island_vote_type_t island_vote_type`**

**`posal_pm_island_type_t island_type`**

**`struct posal_pm_cpu_lpr_vote_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

**`posal_pm_cpu_lpr_id_t lpr_id`**

**`posal_pm_cpu_lpr_vote_type_t cpu_lpr_vote_type`**

**`struct posal_pm_resources_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_mpps_t mpps`**

**`posal_pm_bw_t bw`**

**`posal_pm_sleep_latency_t sleep_latency`**

**`posal_pm_island_vote_t island_vote`**

**`posal_pm_cpu_lpr_vote_t cpu_lpr_vote[PM_LPR_CPU_MAX]`**

**`struct posal_pm_request_info_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_handle_t pm_handle_ptr`**

**`uint32_t client_log_id`**

**`posal_signal_t wait_signal_ptr`**

**`posal_pm_resources_t resources`**

**`struct posal_pm_release_info_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_handle_t pm_handle_ptr`**

**`uint32_t client_log_id`**

**`posal_signal_t wait_signal_ptr`**

**`uint32_t delay_ms`**

**`posal_pm_resources_t resources`**

## posal_root_msg

Defines

**`POSAL_ROOT_VA_NUM_ARGS_IMPL`(`a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `_N`, `...`)**

**`POSAL_ROOT_VA_NUM_ARGS`(`...`)**

**`POSAL_ROOT_TOKENPASTE`(`x`, `y`)**

**`POSAL_ROOT_MSG_x`(`_N`)**

**`POSAL_ROOT_MSG`(`xx_ss_mask`, `xx_fmt`, `...`)**

**`POSAL_ROOT_MSG_ISLAND`(`xx_ss_mask`, `xx_fmt`, `...`)**

## posal_signal

本文件包含信号实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_thread

本文件包含用于线程的实用工具。必须 join 线程以避免内存泄漏。本文件提供创建和销毁线程以及更改线程优先级的函数。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_thread_profiling

本文件包含用于线程性能剖析的公开（PUBLIC）实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`ar_result_t posal_thread_profiling_get_stack_info`(`uint32_t tid`, `uint32_t *current_stack_usage_ptr`, `uint32_t *stack_size_ptr`)**

## posal_bufpool

用于小额分配的缓冲池功能的头文件。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`POSAL_BUFPOOL_INVALID_HANDLE`**

Typedefs

**`typedef enum posal_bufpool_align_t posal_bufpool_align_t`**

Enums

**`enum posal_bufpool_align_t`**

*Values:*

**`enumerator FOUR_BYTE_ALIGN`**

**`enumerator EIGHT_BYTE_ALIGN`**

Functions

**`uint32_t posal_bufpool_pool_create`(`uint16_t node_size`, `POSAL_HEAP_ID heap_id`, `uint32_t num_arrays`, `posal_bufpool_align_t alignment`, `uint16_t nodes_per_arr`)**

**`void *posal_bufpool_get_node`(`uint32_t pool_handle`)**

**`void posal_bufpool_return_node`(`void *node_ptr`)**

**`void posal_bufpool_pool_destroy`(`uint32_t pool_handle`)**

**`void posal_bufpool_pool_reset_to_base`(`uint32_t pool_handle`)**

**`void posal_bufpool_pool_free_unused_lists`(`uint32_t pool_handle`)**

**[`bool_t`](args_arosal.md) `posal_bufpool_is_address_in_bufpool`(`void *ptr`, `uint32_t pool_handle`)**

**`uint32_t posal_bufpool_profile_all_mem_usage`()**

**`ar_result_t posal_bufpool_profile_mem_usage`(`uint32_t pool_handle`, `uint32_t *bytes_used_ptr`, `uint32_t *bytes_allocated_ptr`)**

## posal_condvar

本文件包含条件变量（ConditionVariables）实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_err_fatal

包含用于调用强制崩溃的 API。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void posal_err_fatal`(`const char *err_str`)**

## posal

这是 posal 实用工具的顶层包含文件。本文件包含使用 posal 函数所需的所有头文件。posal 的用户只需包含此文件即可调用 posal 函数。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void posal_init`(`void`)**

**`void posal_deinit`(`void`)**

**`static inline uint32_t posal_cmn_divide`(`uint32_t num`, `uint32_t den`)**

## posal_inline_mutex

Typedefs

**`typedef qurt_mutex_t posal_inline_mutex_t`**

Functions

**`static inline ar_result_t posal_inline_mutex_init`(`posal_inline_mutex_t *pposal_mutex`)**

初始化一个互斥锁。始终使用递归互斥锁。

**Associated data types**posal_mutex_t

Nonzero — Failure

**Dependencies** None.

**Parameters:**

**posal_mutex** – **[in]** 指向互斥锁对象句柄的指针。

**Returns:**

0 — Success

**`static inline void posal_inline_mutex_deinit`(`posal_inline_mutex_t *pposal_mutex`)**

反初始化一个互斥锁。对于每个相应的 posal_mutex_init() 函数，都必须调用此函数以清理所有资源。

**Associated data types**posal_mutex_t

**Dependencies** 在调用此函数之前，该对象必须已被创建并初始化。

**Parameters:**

**pposal_mutex** – **[in]** 指向要销毁的互斥锁的指针。

**Returns:**

None.

## posal_interrupt

本文件包含用于注册中断的实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_memory

本文件包含用于内存分配与释放的实用工具。本文件为 C 和 C++ 提供内存分配函数和宏。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_mem_prof

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct posal_mem_prof_marker_t posal_mem_prof_marker_t`**

用于标记内存以进行跟踪性能剖析的结构（追加在内存末尾） 用于保存 heap-id 到内存计数映射的哈希节点结构

**`typedef struct posal_mem_prof_node_t posal_mem_prof_node_t`**

用于指示内存性能剖析是否已启动的枚举

**`typedef enum posal_mem_prof_state_t posal_mem_prof_state_t`**

Posal 内存性能剖析主结构

**`typedef struct posal_mem_prof_t posal_mem_prof_t`**

Enums

**`enum posal_mem_prof_state_t`**

*Values:*

**`enumerator POSAL_MEM_PROF_STOPPED`**

**`enumerator POSAL_MEM_PROF_STARTED`**

Functions

**`ar_result_t posal_mem_prof_init`(`POSAL_HEAP_ID heap_id`)**

初始化 posal 内存性能剖析器，创建互斥锁。

**Dependencies** None

**Parameters:**

**heapId** – **[in]** 用于分配内存的堆的 ID。

**Returns:**

结果。

**`ar_result_t posal_mem_prof_start`()**

启动 posal 内存性能剖析，创建用于存储 heapid 到内存计数映射所需的哈希表。

**Dependencies** None

**Parameters:**

**None** –

**Returns:**

结果。

**`ar_result_t posal_mem_prof_stop`()**

停止 posal 内存性能剖析，销毁用于存储 heapid 到内存计数映射所需的哈希表。

**Dependencies** None

**Parameters:**

**None** –

**Returns:**

结果。

**`void posal_mem_prof_deinit`()**

反初始化 posal 内存性能剖析，销毁性能剖析互斥锁。

**Dependencies** None

**Parameters:**

**None** –

**Returns:**

结果。

**`void posal_mem_prof_pre_process_malloc`(`POSAL_HEAP_ID orig_heap_id`, `POSAL_HEAP_ID *heap_id_ptr`, `uint32_t *bytes_ptr`)**

从原始 heap id 中提取 heap id，更新所需字节数。

**Dependencies** None

**Parameters:**

- **orig_heap_id** – **[in]** 客户端发送的 heap id。
- **heap_id_ptr** – **[in]** 指向 heap id 的指针，存储从 orig_heap_id 中提取的值。
- **heap_id_ptr** – **[in]** 指向要分配字节数的指针，如果性能剖析已启动，此值将为 + sizeof(uint64_t)

**Returns:**

None.

**`void posal_mem_prof_post_process_malloc`(`void *ptr`, `POSAL_HEAP_ID orig_heap_id`, [`bool_t`](args_arosal.md) `is_mem_tracked`)**

在分配的尾部更新 heap id 和魔数（magic number），如果启用了性能剖析则更新统计信息。

**Dependencies** None

**Parameters:**

- **ptr** – **[in]** 指向新分配内存的指针。
- **orig_heap_id** – **[in]** 客户端发送的 heap id。
- **is_mem_tracked** – **[in]** 布尔值，指示分配时内存是否被跟踪。

**Returns:**

None.

**`void posal_mem_prof_process_free`(`void *ptr`)**

从 ptr 中提取 heapid 和内存大小，更新统计信息。

**Dependencies** None

**Parameters:**

**ptr** – **[in]** 指向新分配内存的指针。

**Returns:**

None.

**`void posal_mem_prof_query`(`POSAL_HEAP_ID heap_id`, `uint32_t *mem_usage_ptr`)**

如果统计信息存在，则更新客户端所询问的内存使用查询。

**Dependencies** None

**Parameters:**

- **heap_id** – **[in]** 查询的 heap id。
- **mem_usage_ptr** – **[in]** 需要进行查询更新的目标指针。

**Returns:**

None.

**`uint32_t posal_mem_prof_get_mem_size`(`void *ptr`, `POSAL_HEAP_ID heap_id`)**

用于从一个指针获取内存大小。

**Dependencies** None

**Parameters:**

- **ptr** – **[in]** 已分配内存的指针。
- **heap_id** – **[in]** 查询的 heap id。

**Returns:**

内存的块大小

**`struct posal_mem_prof_marker_t`**

*#include <posal_mem_prof.h>*用于标记内存以进行跟踪性能剖析的结构（追加在内存末尾）

Public Members

**`POSAL_HEAP_ID heap_id`**

所分配内存的 Heap ID

**`uint32_t magic_number`**

用于验证内存跟踪的魔数

**`struct posal_mem_prof_node_t`**

*#include <posal_mem_prof.h>*Public Members

**`spf_hash_node_t hash_node`**

哈希节点

**`POSAL_HEAP_ID heap_id`**

键 - heap id 用作哈希节点的键

**`uint32_t mem_count`**

值 - 内存分配的计数，以字节为单位

**`struct posal_mem_prof_t`**

*#include <posal_mem_prof.h>*Public Members

**`spf_hashtable_t mem_ht`**

用于保存 heap id 到内存计数映射的哈希表

**`POSAL_HEAP_ID heap_id`**

posal 内存性能剖析器要使用的 heap id

**`posal_mutex_t prof_mutex`**

posal 内存性能剖析器要使用的互斥锁

**`posal_mem_prof_state_t mem_prof_status`**

用于指示性能剖析是否已启动的标志

## posal_nmutex

本文件包含普通互斥锁实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_queue

本文件包含队列实用工具。队列在使用之前必须先创建并添加到某个通道。队列从后端压入，可从前端（FIFO）或后端（LIFO）弹出。队列在不再需要时必须被销毁。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`uint32_t posal_queue_get_queue_fullness`(`posal_queue_t *q_ptr`)**

用于获取队列充满程度的函数

它返回队列中当前的元素数量

**`struct posal_queue_init_attr_t`**

*#include <posal_queue.h>*包含与 posal_queue_t 类型关联的属性的结构

Public Members

**[`char_t`](args_arosal.md) `name[POSAL_DEFAULT_NAME_LEN]`**

队列的名称。

**`int32_t max_nodes`**

队列节点的最大数量。

**`int32_t prealloc_nodes`**

预分配节点的数量

**`POSAL_HEAP_ID heap_id`**

用于分配节点的 Heap ID。

**[`bool_t`](args_arosal.md) `is_priority_queue`**

FALSE：默认 FIFO 队列，TRUE：优先级队列。

## posal_rtld

本文件包含运行时链接（Run-Time Linking，rtld）实用工具。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`POSAL_RTLD_LAZY`**

**`POSAL_RTLD_NOW`**

**`RTLD_DI_LOAD_ADDR`**

理想情况下 dlfcn.h 必须定义这些宏。但在某些目标上它们未被定义。这是一个变通方案。

**`RTLD_DI_LOAD_SIZE`**

Functions

**`void *posal_dlopen`(`const char *name`, `int flags`)**

打开指定的动态库

**Associated data types**const char*, int

**Dependencies** None.

**Parameters:**

- **name** – **[in]** 要打开的文件的名称
- **flags** – **[in]** 用于指示应如何打开文件的标志。可能的值为 POSAL_RTLD_LAZY 和 POSAL_RTLD_NOW

**Returns:**

返回指向已打开动态库的指针，失败时返回 0

**`void *posal_dlopenbuf`(`const char *name`, `const char *buf`, `int len`, `int flags`)**

打开位于给定缓冲区中的指定动态库

**Associated data types**const char*, const char*, int

**Dependencies** None.

**Parameters:**

- **name** – **[in]** 要打开的文件的名称
- **buf** – **[in]** 动态库的缓冲区
- **flags** – **[in]** 用于指示应如何打开文件的标志。可能的值为 POSAL_RTLD_LAZY 和 POSAL_RTLD_NOW

**Returns:**

返回指向已打开动态库的指针，失败时返回 0

**`int posal_dlclose`(`void *handle`)**

关闭指定的动态库

**Associated data types**void *

**Dependencies** None.

**Parameters:**

**handle** – **[in]** 要关闭的 dl 的句柄

**Returns:**

0 — Success

**`void *posal_dlsym`(`void *handle`, `const char *name`)**

获取动态库中某符号的指针

**Associated data types**void *, const char *

**Dependencies** None.

**Parameters:**

- **handle** – **[in]** 含所需符号的 dl 的句柄
- **name** – **[in]** 符号的名称

**Returns:**

返回指向所请求符号的指针，失败时返回 0

**`char *posal_dlerror`(`void`)**

如果某个 dl 函数出现问题，给出错误的字符串

**Dependencies** None.

**Returns:**

返回指向错误字符串的指针

**`int posal_dlinfo`(`void *handle`, `int request`, `void *p`)**

根据请求获取有关动态库的信息

**Associated data types**void *, int, void *

**Dependencies** None.

**Parameters:**

- **handle** – **[in]** 所涉及 dl 的句柄
- **request** – **[in]** 请求的值
- **p** – **[out]** 请求的输出

**Returns:**

0 — Success

## posal_std

本文件包含标准 C 函数。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`AR_STD_MIN`(`a`, `b`)**

**`AR_STD_MAX`(`a`, `b`)**

Functions

**`uint32_t posal_strlcpy`([`char_t`](args_arosal.md) `*dest_ptr`, `const` [`char_t`](args_arosal.md) `*src_ptr`, `uint32_t dest_len`)**

将字符串从源指针复制到目标指针。

**Dependencies** None.

**Parameters:**

- **dest_ptr** – **[in]** 指向目标字符串的指针。
- **src_ptr** – **[in]** 指向源字符串的指针。
- **dest_len** – **[in]** 目标缓冲区的长度。

**Returns:**

src_len — 源字符串大小。

**`uint32_t posal_strnlen`(`const` [`char_t`](args_arosal.md) `*src_ptr`, `uint32_t size`)**

确定具有固定最大大小的字符串的长度。

**Dependencies** None.

**Parameters:**

- **src_ptr** – **[in]** 指向目标字符串的指针。
- **size** – **[in]** 指向源字符串的指针。

**Returns:**

字符串长度。

**`int32_t posal_strncmp`(`const char *s1`, `uint32_t s1_size`, `const char *s2`, `uint32_t s2_size`)**

按字符逐个比较两个字符串，比较范围以字符串长度为界。

**Dependencies** None.

**Parameters:**

- **s1** – **[in]** 指向目标字符串的指针。
- **s1_size** – **[in]** 指向源字符串的指针。
- **s2** – **[in]** 目标缓冲区的长度。
- **s2_size** – **[in]** 指向目标字符串的指针。

**Returns:**

<0 - 如果第一个不匹配的字符在 s1 中的 ASCII 值低于 s2 中的 0 - 如果两个字符串相同 >0 - 如果第一个不匹配的字符在 s1 中的 ASCII 值高于 s2 中的

**`void *posal_memcpy`(`void *dst`, `uint32_t dst_size`, `const void *src`, `uint32_t src_size`)**

从源指针复制 src_size 字节到目标指针。实际复制的字节数以 dst_size 为界，这可以在 dst_size 小于 src_size 时避免目标内存损坏。

**Dependencies** None.

**Parameters:**

- **dst** – **[in]** - 目标指针。
- **dst_size** – **[in]** - 目标指针的大小，以字节为单位。
- **src** – **[in]** - 源指针
- **src_size** – **[in]** - 要从源指针复制的字节数。

**Returns:**

返回目标指针的副本。

**`void *posal_memset`(`void *dst`, `int32_t c`, `uint32_t num_bytes`)**

将 dst 所指向内存的前 size 个字节设置为值 'c'（解释为 unsigned char）。

**Dependencies** None.

**Parameters:**

- **dst** – **[in]** - 目标指针
- **c** – **[in]** - 要设置的值。以 int32 传入，但解释为 unsigned char。
- **num_bytes** – **[in]** - 要设置为值 'c' 的字节数

**Returns:**

返回输入指针的副本。

**`int32_t posal_snprintf`([`char_t`](args_arosal.md) `*dst`, `uint32_t size`, `const` [`char_t`](args_arosal.md) `*format`, `...`)**

在目标指针中打印格式化字符串，打印的最大字符数以 size 为界。

**Dependencies** None.

**Parameters:**

- **dst** – **[in]** - 打印字符串的目标指针。
- **size** – **[in]** - 可打印的最大字符数。
- **format** – **[in]** - 指向格式字符串的指针。

**Returns:**

实际已打印的字符数。

## posal_thread_prio

本文件包含将暴露给框架的结构和函数声明，以便被调用来获取线程优先级。

**Copyright** Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef enum spf_thread_prio_id_t spf_thread_prio_id_t`**

**`typedef struct prio_query_t prio_query_t`**

prio_query_t 结构保存一个（static_req_id、线程优先级、帧时长），指示给定帧时长（以微秒计）下正确的线程优先级，或者一个 req ID（指示静态/动态）。

Enums

**`enum spf_thread_prio_id_t`**

*Values:*

**`enumerator SPF_THREAD_DYN_ID`**

**`enumerator SPF_THREAD_STAT_APM_ID`**

**`enumerator SPF_THREAD_STAT_CNTR_ID`**

**`enumerator SPF_THREAD_STAT_AMDB_ID`**

**`enumerator SPF_THREAD_STAT_IST_ID`**

**`enumerator SPF_THREAD_STAT_PRM_ID`**

**`enumerator SPF_THREAD_STAT_PM_SERVER_ID`**

**`enumerator SPF_THREAD_STAT_VOICE_TIMER_ID`**

**`enumerator SPF_THREAD_STAT_VCPM_ID`**

**`enumerator SPF_THREAD_STAT_ASPS_ID`**

**`enumerator SPF_THREAD_STAT_DLS_ID`**

**`enumerator SPF_THREAD_STAT_ID_MAX`**

Functions

**`ar_result_t posal_thread_calc_prio`(`prio_query_t *prio_query_ptr`, `posal_thread_prio_t *thread_prio_ptr`)**

**`ar_result_t posal_thread_determine_attributes`(`prio_query_t *prio_query_ptr`, `posal_thread_prio_t *thread_prio_ptr`, `uint32_t *sched_policy_ptr`, `uint32_t *cpu_set_ptr`)**

**`posal_thread_prio_t posal_thread_get_floor_prio`(`spf_thread_prio_id_t prio_id`)**

获取传入的 prio_id 的默认低优先级。目前仅为 SPF_THREAD_STAT_CNTR_ID 实现。

**`struct prio_query_t`**

*#include <posal_thread_prio.h>*prio_query_t 结构保存一个（static_req_id、线程优先级、帧时长），指示给定帧时长（以微秒计）下正确的线程优先级，或者一个 req ID（指示静态/动态）。

Public Members

**[`bool_t`](args_arosal.md) `is_interrupt_trig`**

**`spf_thread_prio_id_t static_req_id`**

**`uint32_t frame_duration_us`**
