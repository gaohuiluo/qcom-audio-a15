# OS Abstraction Layer

- ar_osal_err
- ar_osal_log
- ar_osal_heap
- ar_osal_mem_op
- ar_osal_servreg
- ar_osal_signal
- ar_osal_signal2
- ar_osal_sleep
- ar_osal_sys_id
- ar_osal_types
- ar_osal_file_io
- ar_osal_shmem
- ar_osal_string
- ar_osal_thread

## ar_osal_err

本文件包含 AudioReach 使用的错误码。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_EOK`**

成功。操作完成且无错误。

**`AR_EFAILED`**

一般性失败。

**`AR_EBADPARAM`**

操作参数错误。

**`AR_EUNSUPPORTED`**

不支持的例程或操作。

**`AR_EVERSION`**

不支持的版本。

**`AR_EUNEXPECTED`**

遇到意外问题。

**`AR_EPANIC`**

发生了未处理的问题。

**`AR_ENORESOURCE`**

无法分配资源。

**`AR_EHANDLE`**

无效句柄。

**`AR_EALREADY`**

操作已被处理。

**`AR_ENOTREADY`**

操作尚未准备好被处理。

**`AR_EPENDING`**

操作正在等待完成。

**`AR_EBUSY`**

操作无法被接受或处理。

**`AR_EABORTED`**

操作因错误而中止。

**`AR_ECONTINUE`**

操作需要一次干预才能完成。

**`AR_EIMMEDIATE`**

操作需要一次立即干预才能完成。

**`AR_ENOTIMPL`**

操作未实现。

**`AR_ENEEDMORE`**

操作需要更多数据或资源。

**`AR_ENOMEMORY`**

操作没有内存。

**`AR_ENOTEXIST`**

项目不存在。

**`AR_ETERMINATED`**

操作已结束。

**`AR_ETIMEOUT`**

操作超时。

**`AR_EIODATA`**

数据读/写失败。

**`AR_ESUBSYSRESET`**

发生了子系统复位。

**`AR_EDUPLICATE`**

打开了重复的子图或连接。

**`AR_SUCCEEDED`(`x`)**

检查结果是否成功

**`AR_FAILED`(`x`)**

检查结果是否失败。

## ar_osal_log

定义用于消息日志记录的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_CRITICAL`**

严重消息，记录不可恢复的状况。

**`AR_ERROR`**

错误消息，表示应被调试并修复的代码缺陷。

**`AR_DEBUG`**

调试消息，调试时需要。默认不启用

**`AR_INFO`**

用于需要存在于默认日志中的重要信息

**`AR_VERBOSE`**

详尽消息，主要用于帮助开发者调试底层代码

**`AR_LOG_VERBOSE`(`log_tag`, `...`)**

**`AR_LOG_INFO`(`log_tag`, `...`)**

**`AR_LOG_DEBUG`(`log_tag`, `...`)**

**`AR_LOG_ERR`(`log_tag`, `...`)**

**`AR_LOG_CRITICAL`(`log_tag`, `...`)**

**`AR_FATAL_PRIO`**

致命优先级调试消息。

**`AR_ERROR_PRIO`**

错误优先级调试消息。

**`AR_HIGH_PRIO`**

高优先级调试消息。

**`AR_MED_PRIO`**

中优先级调试消息。

**`AR_LOW_PRIO`**

低优先级调试消息。

**`AR_LOG_FATAL`(`log_tag`, `...`)**

**`AR_LOG_HIGH`(`log_tag`, `...`)**

**`AR_LOG_ERROR`(`log_tag`, `...`)**

**`AR_LOG_MED`(`log_tag`, `...`)**

**`AR_LOG_LOW`(`log_tag`, `...`)**

Functions

**`void ar_log_init`(`void`)**

**`void ar_log_deinit`(`void`)**

**`void ar_log`(`uint32_t level`, `const char_t *log_tag`, `const char_t *file`, `const char_t *fn`, `int32_t ln`, `const char_t *format`, `...`)**

**`void ar_set_log_level`(`uint32_t level`)**

Variables

**`uint32_t ar_log_lvl`**

## ar_osal_heap

定义用于堆内存分配的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_HEAP_TAG_DEFAULT`**

默认堆内存标签 ASCII 字符：‘LASO’->’OSAL’

Typedefs

**`typedef enum _ar_heap_align_bytes ar_heap_align_bytes`**

堆内存字节对齐的枚举

**`typedef enum _ar_heap_id ar_heap_id`**

堆内存 id 的枚举

**`typedef enum _ar_heap_pool_type ar_heap_pool_type`**

堆内存类型的枚举

**`typedef struct ar_heap_info_t ar_heap_info`**

堆内存信息结构体

**`typedef struct ar_heap_info_t *par_heap_info`**

Enums

**`enum _ar_heap_align_bytes`**

堆内存字节对齐的枚举

*Values:*

**`enumerator AR_HEAP_ALIGN_DEFAULT`**

**`enumerator AR_HEAP_ALIGN_4_BYTES`**

默认对齐

**`enumerator AR_HEAP_ALIGN_8_BYTES`**

4 字节边界

**`enumerator AR_HEAP_ALIGN_16_BYTES`**

8 字节边界

**`enum _ar_heap_id`**

堆内存 id 的枚举

*Values:*

**`enumerator AR_HEAP_ID_DEFAULT`**

**`enumerator AR_HEAP_ID_1`**

默认堆 id

**`enumerator AR_HEAP_ID_2`**

自定义堆 id 1

**`enumerator AR_HEAP_ID_3`**

自定义堆 id 2

**`enumerator AR_HEAP_ID_4`**

自定义堆 id 3

**`enumerator AR_HEAP_ID_5`**

自定义堆 id 4

**`enumerator AR_HEAP_ID_6`**

自定义堆 id 5

**`enumerator AR_HEAP_ID_7`**

自定义堆 id 6

**`enumerator AR_HEAP_ID_8`**

自定义堆 id 7

**`enumerator AR_HEAP_ID_9`**

自定义堆 id 8

**`enumerator AR_HEAP_ID_10`**

自定义堆 id 9

**`enumerator AR_HEAP_ID_11`**

自定义堆 id 10

**`enum _ar_heap_pool_type`**

堆内存类型的枚举

*Values:*

**`enumerator AR_HEAP_POOL_DEFAULT`**

默认池类型，由各平台自行支持。

**`enumerator AR_HEAP_POOL_NON_PAGED_EXECUTE`**

所分配的内存是非分页且可执行的，也就是说，该内存中允许指令执行。

**`enumerator AR_HEAP_POOL_NON_PAGED_NX`**

所分配的内存是非分页的且禁止指令执行。

**`enumerator AR_HEAP_POOL_PAGED`**

所分配的内存是可分页的。

Functions

**`int32_t ar_heap_init`(`void`)**

ar_heap_init 初始化堆内存接口。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_heap_deinit`(`void`)**

ar_heap_deinit。反初始化堆内存接口。

**Returns:**

0 — 成功 非零 — 失败

**`void *ar_heap_malloc`(`size_t bytes`, `par_heap_info heap_info`)**

分配堆内存。

**Parameters:**

- **bytes** – **[in]** 要分配的堆内存字节数。
- **heap_info** – **[in]** 类型为 ar_heap_info 的指针。

**Returns:**

非零 — 成功：指向所分配堆内存的指针 NULL — 失败

**`void *ar_heap_calloc`(`size_t bytes`, `par_heap_info heap_info`)**

分配堆内存并初始化为 0。

**Parameters:**

- **bytes** – **[in]** 要分配的堆内存字节数。
- **heap_info** – **[in]** 类型为 ar_heap_info 的指针。

**Returns:**

非零 — 成功：指向所分配堆内存的指针 NULL — 失败

**`void ar_heap_free`(`void *heap_ptr`, `par_heap_info heap_info`)**

释放堆内存。

**Parameters:**

**heap_ptr** – **[in]** 由 ar_heap_alloc() 获得的指向堆内存的指针。

**Returns:**

0 — 成功 非零 — 失败

**`struct ar_heap_info_t`**

*#include <ar_osal_heap.h>*堆内存信息结构体

Public Members

**`ar_heap_align_bytes align_bytes`**

**`ar_heap_pool_type pool_type`**

所需的堆内存字节对齐。

**`ar_heap_id heap_id`**

用于分配堆内存的池类型。

**`uint32_t tag`**

用于分配堆内存的堆 id。

## ar_osal_mem_op

定义用于内存操作的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_mem_cpy`(`void *dest`, `size_t dest_size`, `const void *src`, `size_t size`)**

ar_mem_cpy 在缓冲区之间复制字节。

**Parameters:**

- **[in_out]** – dest：用于复制数据的目标缓冲区。
- **dest_size** – **[in]** 目标缓冲区大小。
- **src** – **[in]** 从中复制数据的源缓冲区指针。
- **size** – **[in]** 从源缓冲区复制的字节数。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_mem_move`(`void *dest`, `size_t dest_size`, `const void *src`, `size_t size`)**

ar_mem_move 将字节从源区域复制到目标区域。

**Parameters:**

- **[in_out]** – dest：用于复制数据的目标缓冲区。
- **dest_size** – **[in]** 目标缓冲区大小。
- **src** – **[in]** 从中复制数据的源缓冲区指针。
- **size** – **[in]** 从源缓冲区复制的字节数。

**Returns:**

0 — 成功 非零 — 失败 注意：如果源区域与目标区域的某些部分重叠，ar_mem_move 会确保重叠区域内的原始源字节在被覆盖前先被复制。

**`int32_t ar_mem_set`(`void *dest`, `int32_t c`, `size_t size`)**

ar_mem_set 将缓冲区设置为指定的值。

**Parameters:**

- **[in_out]** – dest：用于设置指定值的目标缓冲区。
- **c** – **[in]** 要设置的指定值，整型。
- **size** – **[in]** 要设置该值的缓冲区字节数，必须是指定值 “c” 数据大小的整数倍。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_mem_cmp`(`const void *buff1`, `const void *buff2`, `size_t size`)**

ar_mem_cmp 比较两个缓冲区。

**Parameters:**

- **buff1** – **[in]** 第一个缓冲区。
- **buff2** – **[in]** 第二个缓冲区。
- **size** – **[in]** 要比较的字节数。

**Returns:**

< 0 buff1 < buff2 0 buff1 == buff2  0 buff1 > buff2

## ar_osal_servreg

定义用于服务定位、通知和状态注册的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_OSAL_SERVREG_NAME_LENGTH_MAX`**

域名（即 “soc/domain/subdomain”）或服务名（即 “provider/service”）的最大长度为 64 字节，例如 msm/adsp/audio_pd 或 avs/audio 或 audio/avs_mdf_sdsp 或 audio/avs_mdf_mdsp

Typedefs

**`typedef void *ar_osal_servreg_t`**

ar osal servreg 类型对象。

**`typedef enum ar_osal_service_state ar_osal_service_state_type`**

服务状态 up/down 指示器。

**`typedef enum ar_osal_client ar_osal_client_type`**

Servreg 客户端类型：监听者或服务提供方。

**`typedef enum ar_osal_servreg_cb_event ar_osal_servreg_cb_event_type`**

Servreg 回调通知事件。

**`typedef struct ar_osal_servreg_state_notify_payload ar_osal_servreg_state_notify_payload_type`**

servreg 服务状态通知回调负载。

**`typedef void (*ar_osal_servreg_callback)(ar_osal_servreg_t servreg_handle, ar_osal_servreg_cb_event_type event_id, void *cb_context, void *payload, uint32_t payload_size)`**

ar_osal_servreg_callback 用于在服务状态（up/down）发生任何变化时通知客户端的回调函数。

**Param servreg_handle:**

**[in]** 由 ar_osal_servreg_register() 为给定服务返回的 Servreg 句柄。

**Param event_id:**

**[in]** ar_osal_servreg_cb_event_type 所支持的回调事件 id。

**Param cb_context:**

**[in]** 客户端在 ar_osal_servreg_register() 中提供的负载/上下文。

**Param payload:**

**[in]** 回调提供的负载。服务状态 UP/DOWN 负载 ar_osal_servreg_state_notify_payload_type。

**Param payload_size:**

**[in]** 负载大小，以字节为单位。

**Return:**

无

Enums

**`enum ar_osal_service_state`**

服务状态 up/down 指示器。

*Values:*

**`enumerator AR_OSAL_SERVICE_STATE_DOWN`**

**`enumerator AR_OSAL_SERVICE_STATE_UP`**

**`enum ar_osal_client`**

Servreg 客户端类型：监听者或服务提供方。

*Values:*

**`enumerator AR_OSAL_CLIENT_INVALID`**

**`enumerator AR_OSAL_CLIENT_LISTENER`**

**`enumerator AR_OSAL_CLIENT_SERVICE_PROVIDER`**

**`enum ar_osal_servreg_cb_event`**

Servreg 回调通知事件。

*Values:*

**`enumerator AR_OSAL_SERVICE_STATE_NOTIFY`**

Functions

**`int32_t ar_osal_servreg_init`(`void`)**

ar_osal_servreg_init 初始化 servreg 接口。注意：本 API 必须在该接口中的任何其他 API 之前调用。至少应调用一次，若多次调用，则期望其为串行化调用。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_servreg_deinit`(`void`)**

ar_osal_servreg_deinit 反初始化 servreg 接口。应与 ar_osal_servreg_init() 成对调用，且应为串行化调用。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_servreg_get_domainlist`(`ar_osal_servreg_entry_type *service`, `ar_osal_servreg_entry_type *domain_list`, `uint32_t *num_domains`)**

ar_osal_servreg_get_domainlist 客户端调用本 API 以获取给定服务（provider/service）所支持的域（msm/domain/subdomain）列表。

**Parameters:**

- **service** – **[in]** 需要获取域列表的服务（provider/service）。
- **domain_list** – **[inout]** 该服务所支持的域，由客户端提供负载缓冲区指针。
- **num_domains** – **[inout]** 客户端提供 num_domains 以获取域列表。若 num_domains 为零且 domain_list 为 NULL，且给定服务可用，则该 API 将返回其域的数量。

**Returns:**

0 — 成功 非零 — 失败 AR_ENOMEMORY - 因内存不足而失败，客户端应使用 num_domains 中返回的所需大小再次调用该 API。

**`ar_osal_servreg_t ar_osal_servreg_register`(`ar_osal_client_type client_type`, `ar_osal_servreg_callback cb_func`, `void *cb_context`, `ar_osal_servreg_entry_type *domain`, `ar_osal_servreg_entry_type *service`)**

ar_osal_servreg_register 服务客户端注册以接收域服务状态变化通知。

**Parameters:**

- **client_type** – **[in]** 指示注册的客户端是监听者还是服务提供方。
- **[in** – opt] cb_func：用于接收通知的回调函数指针。对于服务提供方注册，此参数是可选的。
- **[in** – opt] cb_context：客户端提供的回调函数负载/上下文。对于服务提供方注册，此参数是可选的。
- **domain** – **[in]** 需要提供状态变化通知的服务的域（msm/domain/subdomain）。
- **service** – **[in]** 需要提供状态变化通知的服务（provider/service）。

**Returns:**

成功时返回 servreg_handle。失败时返回 null。

**`int32_t ar_osal_servreg_deregister`(`ar_osal_servreg_t servreg_handle`)**

ar_osal_servreg_deregister 服务客户端注销以停止接收服务状态变化通知。

**Parameters:**

**servreg_handle** – **[in]** 由 ar_osal_servreg_register() 返回的接口句柄。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_servreg_set_state`(`ar_osal_servreg_t servreg_handle`, `ar_osal_service_state_type state`)**

ar_osal_servreg_set_state 服务提供方调用本 API 以注册其服务状态（UP/DOWN）。本 API 仅供服务提供方（msm/domain/subdomain/provider/service）使用，不供服务客户端使用。

**Parameters:**

- **servreg_handle** – **[in]** 由 ar_osal_servreg_register() 返回的接口句柄。
- **state** – **[in]** 使用 ar_osal_servreg_register() 注册的服务的新服务状态。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_servreg_restart_service`(`ar_osal_servreg_t servreg_handle`)**

ar_osal_servreg_restart_service HLOS 调用本 API 以在给定处理器上触发重启（PDR 或 SSR）

**Parameters:**

**servreg_handle** – **[in]** 由 ar_osal_servreg_register() 返回的接口句柄，用于标识目标处理器

**Returns:**

0 — 成功 非零 — 失败

**`void ar_osal_panic`()**

引发 panic 使系统崩溃

**`struct ar_osal_servreg_entry_type`**

*#include <ar_osal_servreg.h>*表示服务或域的名称以及实例 id 的结构体

Public Members

**`char_t name[AR_OSAL_SERVREG_NAME_LENGTH_MAX + 1]`**

< 服务或域的名称。实例 ID。

**`uint32_t instance_id`**

**`struct ar_osal_servreg_state_notify_payload`**

*#include <ar_osal_servreg.h>*servreg 服务状态通知回调负载。

Public Members

**`ar_osal_servreg_entry_type service`**

**`ar_osal_servreg_entry_type domain`**

**`ar_osal_service_state_type service_state`**

## ar_osal_signal

定义用于信号的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

## ar_osal_signal2

定义供 DSP 使用的 signal2 的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_osal_signal2_init`(`ar_osal_signal2_t signal2`)**

初始化一个 signal2 对象。Signal 返回已初始化的对象。信号对象初始处于清除状态。信号对象内存由客户端分配。

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**signal2** – **[in]** 指向已初始化对象的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_signal2_deinit`(`ar_osal_signal2_t signal2`)**

反初始化 signal2 对象。

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**signal2** – **[in]** 指向已初始化对象的指针。

**Returns:**

0 — 成功 非零 — 失败

**`size_t ar_osal_signal2_get_size`(`void`)**

获取信号对象大小，供客户端进行对象内存分配。

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Returns:**

信号对象的大小

**`int32_t ar_osal_signal2_create`(`ar_osal_signal2_t *signal2`)**

由本 API 分配并初始化信号对象内存。osal_signal2_create() 或 osal_signal2_init() 二者择一使用，不可同时使用。

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**[Out]** – signal2：指向已初始化对象的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_osal_signal2_destroy`(`ar_osal_signal2_t signal2`)**

销毁指定的信号对象。

@note1cont 信号对象在仍被使用时不得被销毁。如发生此情况，其行为未定义。@note1cont 一般而言，应用代码应在释放 signal2 对象之前先“销毁”它；在释放之前调用 osal_signal2_destroy() 可确保所有 osal_signal2_set() 调用均已完成。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

**signal2** – **[in]** 指向要销毁的信号对象的指针。

**Returns:**

0 — 成功 非零 — 失败

**`uint32_t ar_osal_signal2_wait_any`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

挂起当前线程，直到指定信号中的任意一个被置位。

信号以 32 位掩码值中的第 0-31 位表示。掩码位值为 1 表示要等待该信号，为 0 表示不等待该信号。

如果某线程正在信号对象上等待指定信号集合中的任意一个被置位，且这些信号中有一个或多个已在信号对象中置位，则该线程被唤醒。

在任一给定时刻，至多只有一个线程可以在信号对象上等待。

线程被唤醒时必须显式清除信号，等待操作不会自动清除它们。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** 指向要等待的信号对象的指针。
- **signal2_mask** – **[in]** 用于标识信号对象中要等待的各个信号的掩码值。

**Returns:**

一个包含当前信号的 32 位字。

**`uint32_t ar_osal_signal2_wait_all`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

挂起当前线程，直到所有指定信号都被置位。

信号以 32 位掩码值中的第 0-31 位表示。掩码位值为 1 表示要等待该信号，为 0 表示不等待该信号。

如果某线程正在信号对象上等待指定信号集合中的所有信号被置位，且所有这些信号都已在信号对象中置位，则该线程被唤醒。

在任一给定时刻，至多只有一个线程可以在信号对象上等待。

线程被唤醒时必须显式清除信号，等待操作不会自动清除它们。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** 指向要等待的信号对象的指针。
- **signal2_mask** – **[in]** 用于标识信号对象中要等待的各个信号的掩码值。

**Returns:**

一个包含当前信号的 32 位字。

**`int32_t ar_osal_signal2_set`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

在指定的信号对象中置位信号。

信号以 32 位掩码值中的第 0-31 位表示。掩码位值为 1 表示要置位该信号，为 0 表示不置位该信号。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** 指向要修改的信号对象的指针。
- **signal2_mask** – **[in]** 用于标识信号对象中要置位的各个信号的掩码值。

**Returns:**

0 — 成功 非零 — 失败

**`uint32_t ar_osal_signal2_get`(`ar_osal_signal2_t signal2`)**

从信号对象中获取信号。

返回指定信号对象的当前信号值。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

**signal2** – **[in]** 指向要访问的信号对象的指针。

**Returns:**

一个包含当前信号的 32 位字

**`int32_t ar_osal_signal2_clear`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

清除指定信号对象中的信号。

信号以 32 位 signal2_mask 值中的第 0-31 位表示。signal2_mask 位值为 1 表示要清除该信号，为 0 表示不清除该信号。

线程被唤醒时必须显式清除信号，等待操作不会自动清除它们。

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal** – **[in]** 指向要修改的信号对象的指针。
- **signal2_mask** – **[in]** 用于标识信号对象中要清除的各个信号的 signal2_mask 值。

**Returns:**

0 — 成功 非零 — 失败

## ar_osal_sleep

本文件包含用于将线程执行挂起所需时长的 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_osal_micro_sleep`(`uint64_t micro_seconds`)**

微秒级睡眠函数。实际睡眠时间可能不如所请求的精确，它会随系统时钟节拍的分辨率而变化。请注意，就绪线程并不保证会立即运行。因此，线程可能要在睡眠间隔过去后的一段时间才会运行。

**Dependencies** None.

**Parameters:**

**micro_seconds** – **[in]** 睡眠时长，以微秒为单位。

**Returns:**

0 — 成功 非零 — 失败

## ar_osal_sys_id

定义所支持的子系统 ID。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_SUB_SYS_ID_INVALID`**

无效的子系统

**`AR_MODEM_DSP`**

用于 MODEM DSP 子系统

**`AR_AUDIO_DSP`**

用于 ADSP 子系统

**`AR_APSS`**

用于 AP 子系统

**`AR_SENSOR_DSP`**

用于 SENSOR DSP 子系统

**`AR_COMPUTE_DSP`**

用于 COMPUTE DSP 子系统

**`AR_CC_DSP`**

用于伴随芯片 DSP（CC_DSP）子系统

**`AR_APSS2`**

用于 APSS2 子系统

**`AR_SUB_SYS_ID_FIRST`**

第一个子系统 ID

**`AR_SUB_SYS_ID_LAST`**

最后一个子系统 ID

**`AR_SUB_SYS_IDS_MASK`**

表示子系统 ID 的位掩码。当子系统被添加或移除时更新。

**`AR_DEFAULT_DSP`**

## ar_osal_types

本文件包含基本类型和预处理宏。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`FALSE`**

**`TRUE`**

**`PAGED_FUNCTIONS_START`**

分页函数与数据 默认情况下，链接器会为驱动镜像文件的代码段和数据段分配诸如 “.text” 和 “.data” 之类的名称。当驱动被加载时，I/O 管理器将这些段设为非分页。非分页段始终常驻内存。驱动开发者可以选择将驱动的指定部分设为可分页，以便 Windows 在这些部分不使用时将其移动到分页文件中。要使某个代码段或数据段可分页，驱动开发者需为该段分配一个以 “PAGE” 开头的名称。I/O 管理器在加载驱动时会检查各段的名称。如果段名以 “PAGE” 开头，I/O 管理器就将该段设为可分页。运行在 IRQL >= DISPATCH_LEVEL 的代码必须常驻内存。也就是说，这些代码必须要么位于非分页段中，要么位于被锁定在内存中的可分页段中。如果运行在 IRQL >= DISPATCH_LEVEL 的代码引发缺页，就会发生 bug check。驱动可以使用 PAGED_CODE 宏来验证可分页函数只在合适的 IRQL 下被调用。分页函数 应在要分页的函数组开头处使用

**`PAGED_FUNCTIONS_END`**

应在要分页的函数组结尾处使用

**`PAGED_FUNCTION`()**

应在可分页函数定义的开头处使用

**`PAGED_DATA_START`**

分页数据 应在要分页的变量组开头处使用

**`PAGED_DATA_END`**

应在要分页的变量组结尾处使用

**`__UNREFERENCED_PARAM`(`x`)**

**`__UNUSED`**

**`_In_`**

函数参数注解 此参数必须有有效值，且不会被函数更改

**`_In_opt_`**

此参数可能没有有效值，且不会被函数更改。

**`_Out_`**

此参数没有有效值，但在函数调用返回后必须为有效值。

**`_Out_opt_`**

此参数在函数调用返回前后都没有有效值。

**`_Inout_`**

此参数在调用前必须有有效值，并且在函数调用返回后应有一个不同的值。

**`_Inout_opt_`**

此参数在函数调用返回前后都可能没有有效值。

**`_Outptr_`**

此参数不能为 null，且在函数调用返回后应有一个指向某位置的有效指针。

**`_Outptr_opt_`**

此参数可以为 null，且在函数调用返回后应有一个指向某位置的有效指针。

**`_IRQL_requires_max_`(`irql`)**

中断请求级别（IRQL） 驱动代码或系统 API 只能在特定 IRQL 上运行。开发者必须确保满足 IRQL 要求。自旋锁内使用的代码不得被分页。自旋锁内的代码应尽可能少。运行在 DISPATCH IRQL（高优先级）的中断/回调函数不应被分页。识别出可能运行在 PASSIVE IRQL（低优先级）的函数。

**`_IRQL_requires_min_`(`irql`)**

**`PASSIVE_LEVEL`**

正常优先级级别

**`DISPATCH_LEVEL`**

运行在高优先级级别，这些函数不应被分页。

Typedefs

**`typedef char char_t`**

else of defined(**H2XML**) 字符类型

**`typedef unsigned char bool_t`**

布尔值类型。

## ar_osal_file_io

定义用于文件 IO 操作的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_FOPEN_READ_ONLY`**

以读方式打开，文件位置位于开头。如果文件不存在，ar_fopen 调用失败。

**`AR_FOPEN_WRITE_ONLY`**

以写方式打开一个空文件。如果给定文件已存在，其内容将被销毁，文件位置位于开头。

**`AR_FOPEN_READ_WRITE`**

以读写两用方式打开一个空文件。如果文件已存在，其内容将被销毁，文件位置位于开头。

**`AR_FOPEN_APPEND`**

以追加方式打开（在文件末尾写入），此参数不能单独与 ar_fopen 一起使用。

**`AR_FOPEN_WRITE_ONLY_APPEND`**

以在文件末尾写入（追加）的方式打开。如果文件不存在则创建它。

**`AR_FOPEN_READ_WRITE_APPEND`**

以读取和追加方式打开。如果文件不存在则创建它。读取的文件位置位于文件开头，但写入的数据始终追加到文件末尾。

**`AR_FOPEN_READ_ONLY_WRITE`**

以读写两用方式打开。文件必须存在，文件位置位于文件开头。

Typedefs

**`typedef void *ar_fhandle`**

Structures and Typedefs

**`typedef enum ar_fseek_reference ar_fseek_reference_t`**

Enums

**`enum ar_fseek_reference`**

*Values:*

**`enumerator AR_FSEEK_BEGIN`**

起点为零，即文件的开头。

**`enumerator AR_FSEEK_END`**

起点为当前的文件末尾位置。

**`enumerator AR_FSEEK_CURRENT`**

起点为文件指针的当前值。

Functions

**`int32_t ar_fopen`(`ar_fhandle *handle`, `const char_t *path`, `uint32_t access`)**

ar_fopen 打开一个文件，若不存在则创建。

**Parameters:**

- **handle** – **[out]** 文件的句柄。
- **path** – **[in]** 绝对文件路径。
- **access** – **[in]** 访问类型 AR_FILE_OPEN_READ_ONLY AR_FILE_OPEN_WRITE_ONLY AR_FILE_OPEN_READ_WRITE AR_FOPEN_WRITE_ONLY_APPEND AR_FOPEN_READ_WRITE_APPEND AR_FOPEN_READ_ONLY_WRITE

**Returns:**

0 — 成功 非零 — 失败

**`size_t ar_fsize`(`ar_fhandle handle`)**

ar_fsize 返回文件大小。

**Parameters:**

**handle** – **[in]** 文件的句柄。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fmap`(`ar_fhandle handle`, `const void **fbuffer`)**

ar_fmap 将文件映射到数据内存以进行只读访问

本调用是否为缓冲区分配堆内存取决于平台。在某些内存较低的平台上，它可能改为将非易失性存储映射到一个可读的内存窗口。要释放本调用可能分配的任何资源，调用者必须调用 ar_funmap

**Parameters:**

- **handle** – **[in]** 文件的句柄
- **fbuffer** – **[out]** 指向只读数据内存缓冲区的指针

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_funmap`(`const void *fbuffer`)**

ar_funmap 将文件从数据内存中解除映射

本调用释放先前由 ar_fmap 调用获得的缓冲区，并释放其可能正在使用的任何资源。文件仍需通过调用 ar_fclose 来关闭

**Parameters:**

**fbuffer** – **[in]** 由 ar_fmap 获得的文件缓冲区指针

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fseek`(`ar_fhandle handle`, `size_t offset`, `ar_fseek_reference_t ref`)**

ar_fseek 将用于读/写的文件指针移动到所需的偏移量。

**Parameters:**

- **handle** – **[in]** 文件的句柄。
- **offset** – **[in]** 要移动文件指针的字节数。
- **ref** – **[in]** 有关选项请参阅 ar_fseek_reference_t。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fread`(`ar_fhandle handle`, `void *buf_ptr`, `size_t read_size`, `size_t *bytes_read`)**

ar_fread 从文件读取。

**Parameters:**

- **handle** – **[in]** 文件的句柄。
- **[in_out]** – buf_ptr：用于将数据读入的缓冲区指针。
- **read_size** – **[in]** 要从文件读取的数据大小。
- **[in_out]** – bytes_read：从文件实际读取的数据大小。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fwrite`(`ar_fhandle handle`, `void *buf_ptr`, `size_t write_size`, `size_t *bytes_written`)**

ar_fwrite 写入文件。

**Parameters:**

- **handle** – **[in]** 文件的句柄。
- **buf_ptr** – **[in]** 用于写出数据的缓冲区指针。
- **write_size** – **[in]** 要写入文件的数据大小。
- **[in_out]** – bytes_written：实际写入文件的数据大小。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fclose`(`ar_fhandle handle`)**

ar_fclose

**Parameters:**

**handle** – **[in]** 文件的句柄。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_fdelete`(`const char_t *path`)**

ar_fdelete

**Parameters:**

**path** – **[in]** 绝对文件路径。

**Returns:**

0 — 成功 非零 — 失败

## ar_osal_shmem

定义用于为 DSP 分配共享内存的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_SHMEM_HW_ACCELERATOR_ENABLED`**

**`AR_SHMEM_HW_ACCELERATOR_DISABLED`**

硬件加速器标志的位掩码

**`AR_SHMEM_BIT_MASK_HW_ACCELERATOR_FLAG`**

硬件加速器设置标志的移位量

**`AR_SHMEM_SHIFT_HW_ACCELERATOR_FLAG`**

Typedefs

**`typedef enum ar_shmem_memory_type ar_shmem_memory_type_t`**

shmem 内存类型的枚举

**`typedef enum ar_shmem_cache_type ar_shmem_cache_type_t`**

shmem 缓存类型的枚举

**`typedef enum ar_shmem_buffer_index_type ar_shmem_buffer_index_type_t`**

shmem 偏移量/地址缓冲区索引类型的枚举

**`typedef enum ar_shmem_pd_type ar_shmem_pd_type_t`**

用于指示硬件加速器是否启用/禁用的位

**`typedef struct ar_shmem_proc_info_t ar_shmem_proc_info`**

**`typedef struct ar_shmem_info_t ar_shmem_info`**

共享内存信息结构体

**`typedef struct ar_shmem_hyp_assign_phys_addr_t ar_shmem_hyp_assign_phys_addr`**

用于 hyp assign 的共享内存物理地址和大小详情。

**`typedef enum ar_shmem_hyp_assign_dest_sys_perm_t ar_shmem_hyp_assign_dest_sys_perm`**

所支持的目标子系统权限位掩码类型。可根据需要组合使用各种权限。

**`typedef struct ar_shmem_hyp_assign_dest_sys_info_t ar_shmem_hyp_assign_dest_sys_info`**

用于 hyp assign 的目标子系统 id 详情和所需权限。

**`typedef struct ar_shmem_hyp_assign_phys_info_t ar_shmem_hyp_assign_phys_info`**

Hyp assign 物理内存信息结构体。

Enums

**`enum ar_shmem_memory_type`**

shmem 内存类型的枚举

*Values:*

**`enumerator AR_SHMEM_PHYSICAL_MEMORY`**

0 共享物理内存分配。

**`enumerator AR_SHMEM_VIRTUAL_MEMORY`**

1 共享虚拟内存分配

**`enum ar_shmem_cache_type`**

shmem 缓存类型的枚举

*Values:*

**`enumerator AR_SHMEM_CACHED`**

0 缓存的。

**`enumerator AR_SHMEM_UNCACHED`**

1 非缓存的。

**`enum ar_shmem_buffer_index_type`**

shmem 偏移量/地址缓冲区索引类型的枚举

*Values:*

**`enumerator AR_SHMEM_BUFFER_ADDRESS`**

0 使用物理或虚拟地址。

**`enumerator AR_SHMEM_BUFFER_OFFSET`**

1 使用偏移量，偏移量相对于基地址。

**`enum ar_shmem_pd_type`**

*Values:*

**`enumerator STATIC_PD`**

**`enumerator DYNAMIC_PD`**

**`enum ar_shmem_hyp_assign_dest_sys_perm_t`**

所支持的目标子系统权限位掩码类型。可根据需要组合使用各种权限。

*Values:*

**`enumerator DEST_SYS_PERM_INVALID`**

无效权限位掩码。

**`enumerator DEST_SYS_PERM_EXEC`**

执行权限位掩码。

**`enumerator DEST_SYS_PERM_WRITE_ONLY`**

只写权限位掩码。

**`enumerator DEST_SYS_PERM_EXEC_WRITE`**

执行和写权限。

**`enumerator DEST_SYS_PERM_READ_ONLY`**

只读权限位掩码。

**`enumerator DEST_SYS_PERM_EXEC_READ`**

执行和读权限。

**`enumerator DEST_SYS_PERM_WRITE_READ`**

写和读权限。

**`enumerator DEST_SYS_PERM_EXEC_WRITE_READ`**

执行、写和读权限。

Functions

**`int32_t ar_shmem_init`()**

初始化共享内存接口（V1 API）。

本函数使用默认配置初始化共享内存接口。它执行传统的初始化流程。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_init_v2`(`uint32_t num_master_procs`, `uint32_t *master_procs`)**

使用处理器域列表初始化共享内存接口（V2 API）。

本 V2 API 根据所提供的处理器域 ID 列表选择合适的共享内存实现。

传入 num_master_procs = 0 会得到与 V1 API（ar_shmem_init）等效的行为，从而允许从 V1 平滑过渡到 V2。

**Parameters:**

- **num_master_procs** – **[in]** 处理器域 ID 的数量。
- **master_procs** – **[in]** 指向处理器域 ID 数组的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_alloc`(`ar_shmem_info *info`)**

分配共享内存。仅支持非缓存内存分配。大小为 4KB 的整数倍，返回值对齐到 4KB 边界。缓冲区起始地址应至少 64 位倍数对齐。

**Parameters:**

**[in_out]** – info：指向 ar_shmem_info 的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_free`(`ar_shmem_info *info`)**

释放共享内存。

**Parameters:**

**info** – **[in]** 指向 ar_shmem_info 的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_map`(`ar_shmem_info *info`)**

帮助为给定子系统用 SMMU 映射一块已分配的共享内存。大小应为 4KB 边界的整数倍。缓冲区起始地址应 64 位对齐。

**Parameters:**

**[in_out]** – info：指向 ar_shmem_info 的指针。ar_shmem_info 中所需的输入参数 ar_shmem_info_t.cache_type ar_shmem_info_t.buf_size ar_shmem_info_t.mem_type ar_shmem_info_t.pa_lsw ar_shmem_info_t.pa_msw ar_shmem_info_t.num_sys_id ar_shmem_info_t.sys_id ar_shmem_info 中所需的输出参数 ar_shmem_info_t.ipa_lsw ar_shmem_info_t.ipa_msw

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_unmap`(`ar_shmem_info *info`)**

帮助解除映射由外部用 SMMU 分配的共享内存。

**Parameters:**

**info** – **[in]** 指向 ar_shmem_info 的指针。ar_shmem_info 中所需的输入参数 ar_shmem_info_t.cache_type ar_shmem_info_t.buf_size ar_shmem_info_t.mem_type ar_shmem_info_t.pa_lsw ar_shmem_info_t.pa_msw ar_shmem_info_t.num_sys_id ar_shmem_info_t.sys_id

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_hyp_assign_phys`(`ar_shmem_hyp_assign_phys_info *info`)**

帮助在源子系统和目标子系统之间进行物理内存的 hyp assign。

**Parameters:**

**info** – **[in]** 指向 ar_shmem_hyp_assign_phys_info 的指针。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_get_uid`(`uint64_t alloc_handle`, `uint64_t *uid`)**

ar_shmem_get_uid。获取由 alloc_handle 指向的共享内存所关联的唯一标识符（UID），不支持 UID 的平台应返回 alloc_handle 作为 UID，前提是 alloc_handle 是唯一的。

**Parameters:**

- **alloc_handle** – **[in]** 共享内存的句柄。
- **uid** – **[out]** 该 shmem 的唯一标识符。

**Returns:**

0 — 成功 非零 — 失败

**`int32_t ar_shmem_deinit`(`void`)**

ar_shmem_deinit。

**Returns:**

0 — 成功 非零 — 失败

**`struct ar_shmem_proc_info_t`**

*#include <ar_osal_shmem.h>*Public Members

**`uint8_t proc_id`**

**`ar_shmem_pd_type_t proc_type`**

**`bool_t is_active`**

**`struct ar_shmem_info_t`**

*#include <ar_osal_shmem.h>*共享内存信息结构体

Public Members

**`ar_shmem_cache_type_t cache_type`**

输入，缓存类型，缓存或非缓存内存

**`size_t buf_size`**

输入，共享缓冲区大小，应至少为 4K 且仅为 4K 的整数倍

**`ar_shmem_memory_type_t mem_type`**

输出，shmem 内存类型，虚拟或物理，用于 ar_shmem_alloc() 输入，shmem 内存类型，虚拟或物理，用于 ar_shmem_map()

**`ar_shmem_buffer_index_type_t index_type`**

输出，DSP 是对缓冲区偏移量还是对地址指针进行操作。

**`uint32_t ipa_lsw`**

输出，smmu 映射的 ipa lsw，为 ar_shmem_alloc()/ar_shmem_map() 的输出

**`uint32_t ipa_msw`**

输出，smmu 映射的 ipa msw，为 ar_shmem_alloc()/ar_shmem_map() 的输出

**`uint32_t pa_lsw`**

输出，物理地址 lsw，适用对齐要求，如 4k、起始地址为 64 的倍数，为 ar_shmem_alloc() 的输出 输入，物理地址 lsw，适用对齐要求，如 4k、起始地址为 64 的倍数，为 ar_shmem_map() 的输入

**`uint32_t pa_msw`**

输出，物理地址 msw，适用对齐要求，如 4k、起始地址为 64 的倍数，为 ar_shmem_alloc() 的输出 输入，物理地址 lsw，适用对齐要求，如 4k 起始地址为 64 的倍数，为 ar_shmem_map() 的输入

**`void *vaddr`**

输出，虚拟地址 64 位/32 位，适用对齐要求，如 4k、起始地址为 64 的倍数，为 ar_shmem_alloc() 的输入

**`uint64_t metadata`**

输出可选，指向由各平台为 ar_shmem_alloc() 定义的元数据结构的指针地址

**`uint8_t num_sys_id`**

输入，随 ar_shmem_alloc()/ar_shmem_map() 调用提供的子系统 ID 数量。

**`ar_shmem_proc_info *sys_id`**

输入，指向大小为 num_sys_id 的数组的指针，用于 ar_osal_sys_id.h 中提供的子系统 Id，用于在随 ar_shmem_alloc()/ar_shmem_map() 调用提供的 sys_id 列表之间分配共享内存。

**`uint32_t platform_info`**

输入可选，用于向 OSAL 传递平台特定数据的可选字段，例如可用于传达某些堆属性，仅为 ar_shmem_alloc() 提供

**`uint32_t flags`**

输入，标志位字段。1 — 启用硬件加速器，使用 AR_SHMEM_HW_ACCELERATOR_ENABLED 0 — 禁用硬件加速器，使用 AR_SHMEM_HW_ACCELERATOR_DISABLED 要设置此位，使用 AR_SHMEM_BIT_MASK_HW_ACCELERATOR_FLAG 和 AR_SHMEM_SHIFT_HW_ACCELERATOR_FLAG 所有其他位均为保留位；必须设为 0。

**`struct ar_shmem_hyp_assign_phys_addr_t`**

*#include <ar_osal_shmem.h>*用于 hyp assign 的共享内存物理地址和大小详情。

Public Members

**`uint64_t phys_addr`**

64 位物理地址。

**`size_t size`**

由 phys_addr 指向的缓冲区的大小，以字节为单位

**`struct ar_shmem_hyp_assign_dest_sys_info_t`**

*#include <ar_osal_shmem.h>*用于 hyp assign 的目标子系统 id 详情和所需权限。

Public Members

**`uint64_t dest_sys_id`**

目标子系统 id，参阅 ar_osal_sys_id.h

**`ar_shmem_hyp_assign_dest_sys_perm dest_perm`**

目标权限

**`struct ar_shmem_hyp_assign_phys_info_t`**

*#include <ar_osal_shmem.h>*Hyp assign 物理内存信息结构体。

Public Members

**`ar_shmem_hyp_assign_phys_addr *phys_addr_list`**

hyp_assign_phys_addr 结构体的列表。

**`uint32_t phys_addr_list_size`**

phys_addr_list 条目的数量。

**`uint64_t *src_sys_list`**

源子系统 Id 列表，sys id 参阅 ar_osal_sys_id.h。

**`uint32_t src_sys_list_size`**

src_sys_list 条目的数量。

**`ar_shmem_hyp_assign_dest_sys_info *dest_sys_list`**

目标 sys 列表 hyp_assign_dest_sys_info。

**`uint32_t dest_sys_list_size`**

目标 sys 列表/dest_sys_list 条目的数量。

**`uint64_t metadata`**

输入可选，指向在 ar_shmem_alloc() 调用期间由平台定义的元数据结构的指针地址。

## ar_osal_string

定义用于字符串操作的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`ar_sprintf`(`str_dest`, `str_dest_size`, `format`, `...`)**

ar_sprintf 将格式化数据写入字符串。

ar_sscanf 从字符串读取格式化数据。

**Parameters:**

- **[in_out]** – str_dest：目标字符串缓冲区。
- **str_dest_size** – **[in]** 大小，以字节为单位。
- **format** – **[in]** 格式控制字符串。
- **...** – **[in]** ：可变参数。
- **str_src** – **[in]** 已存储的字符串缓冲区。
- **format** – **[in]** 格式控制字符串。
- **...** – **[in]** ：可变参数。

**Returns:**

写入缓冲区的字符数（不计入 null 终止符）。目标始终追加 null 终止符，如果数据大于目标缓冲区大小，则会发生截断并追加 null 终止符。

**Returns:**

成功转换并赋值的字段数量，返回值不包括已读取但未赋值的字段。返回值为 0 表示没有字段被赋值。

**`ar_sscanf`(`str_src`, `format`, `...`)**

Functions

**`size_t ar_strlen`(`const char_t *str`, `size_t size`)**

ar_strlen 获取字符串的长度。

**Parameters:**

- **str** – **[in]** 以 NULL 结尾的字符串缓冲区指针。
- **size** – **[in]** 字符串缓冲区大小，以字节为单位。

**Returns:**

字符串中的字符数，不包括终止 null 字符。如果缓冲区中没有 null 终止符，则返回所提供的字符串缓冲区大小以指示错误。

**`int32_t ar_strcpy`(`char_t *str_dest`, `size_t str_dest_size`, `const char_t *str_src`, `size_t cpy_size`)**

ar_strcpy 将字符从源字符串复制到目标字符串。

**Parameters:**

- **[in_out]** – str_dest：目标字符串缓冲区。
- **str_dest_size** – **[in]** 大小，以字符为单位。
- **str_src** – **[in]** 从中复制的源字符串。
- **cpy_size** – **[in]** 从源字符串复制的大小，以字符为单位。

**Returns:**

0 — 成功 非零 — 失败 注意：始终会在目标末尾追加 null 终止符，如果目标大小小于或等于要复制的字符数，则会发生字符串截断。

**`int32_t ar_strcmp`(`const char_t *str1`, `const char_t *str2`, `size_t num`)**

ar_strcmp 比较两个给定字符串中的字符。

**Parameters:**

- **str1** – **[in]** 以 Null 结尾的字符串 1
- **str2** – **[in]** 以 Null 结尾的字符串 2
- **num** – **[in]** 要比较的字符数。

**Returns:**

< 0 str1 < str2 0 str1 == str2  0 str1 > str2

**`int32_t ar_strcat`(`char_t *str_dest`, `size_t str_dest_size`, `const char_t *str_src`, `size_t apnd_size`)**

ar_strcat 将字符从源字符串追加到目标字符串。

**Parameters:**

- **[in_out]** – str_dest：目标字符串缓冲区。
- **str_dest_size** – **[in]** 大小，以字符为单位。
- **str_src** – **[in]** 从中复制的源字符串。
- **apnd_size** – **[in]** 从源字符串追加的大小，以字符为单位。

**Returns:**

0 — 成功 非零 — 失败 注意：拼接后始终会在目标末尾追加 null 终止符，如果目标大小小于或等于源，则会发生字符串截断。

**`char_t *ar_strstr`(`const char_t *str`, `const char_t *str_search`)**

ar_strstr 在字符串中搜索字符串。

**Parameters:**

- **str** – **[in]** 以 Null 结尾的字符串
- **str_search** – **[in]** 要搜索的以 Null 结尾的字符串。

**Returns:**

指向 str 中 str_search 首次出现处的指针。NULL - 如果未找到。

## ar_osal_thread

定义用于线程的公共 API。

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

**`struct ar_osal_thread_attr_t`**

*#include <ar_osal_thread.h>*线程属性。

Public Members

**`char_t *thread_name`**

指向线程名称的指针

**`uint32_t stack_size`**

线程栈的大小

**`int32_t priority`**

线程优先级
