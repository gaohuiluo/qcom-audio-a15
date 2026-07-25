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

This file contains error codes used by AudioReach.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_EOK`**

Success. The operation completed with no errors.

**`AR_EFAILED`**

General failure.

**`AR_EBADPARAM`**

Bad operation parameter.

**`AR_EUNSUPPORTED`**

Unsupported routine or operation.

**`AR_EVERSION`**

Unsupported version.

**`AR_EUNEXPECTED`**

Unexpected problem encountered.

**`AR_EPANIC`**

Unhandled problem occurred.

**`AR_ENORESOURCE`**

Unable to allocate resource.

**`AR_EHANDLE`**

Invalid handle.

**`AR_EALREADY`**

Operation is already processed.

**`AR_ENOTREADY`**

Operation is not ready to be processed.

**`AR_EPENDING`**

Operation is pending completion.

**`AR_EBUSY`**

Operation cannot be accepted or processed.

**`AR_EABORTED`**

Operation was aborted due to an error.

**`AR_ECONTINUE`**

Operation requests an intervention to complete.

**`AR_EIMMEDIATE`**

Operation requests an immediate intervention to complete.

**`AR_ENOTIMPL`**

Operation was not implemented.

**`AR_ENEEDMORE`**

Operation needs more data or resources.

**`AR_ENOMEMORY`**

Operation does not have memory.

**`AR_ENOTEXIST`**

Item does not exist.

**`AR_ETERMINATED`**

Operation is finished.

**`AR_ETIMEOUT`**

Operation timeout.

**`AR_EIODATA`**

Data read/write failed.

**`AR_ESUBSYSRESET`**

Sub system reset occured.

**`AR_EDUPLICATE`**

Duplicate subgraph or connection opened.

**`AR_SUCCEEDED`(`x`)**

Checks if a result is a success

**`AR_FAILED`(`x`)**

Checks if a result is failure.

## ar_osal_log

Defines public APIs for message logging.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_CRITICAL`**

critical message, log unrecoverable condition .

**`AR_ERROR`**

error message, represents code bugs that should be debugged and fixed.

**`AR_DEBUG`**

debug message, required for debug. Not enabled by default

**`AR_INFO`**

Use for vital info that needs to exist in default logs

**`AR_VERBOSE`**

verbose message, useful primarily to help developers debug low-level code

**`AR_LOG_VERBOSE`(`log_tag`, `...`)**

**`AR_LOG_INFO`(`log_tag`, `...`)**

**`AR_LOG_DEBUG`(`log_tag`, `...`)**

**`AR_LOG_ERR`(`log_tag`, `...`)**

**`AR_LOG_CRITICAL`(`log_tag`, `...`)**

**`AR_FATAL_PRIO`**

Fatal priority debug message.

**`AR_ERROR_PRIO`**

Error priority debug message.

**`AR_HIGH_PRIO`**

High priority debug message.

**`AR_MED_PRIO`**

Medium priority debug message.

**`AR_LOW_PRIO`**

Low priority debug message.

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

Defines public APIs for heap memory allocation.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_HEAP_TAG_DEFAULT`**

default heap memory tag ASCII characters: ‘LASO’->’OSAL’

Typedefs

**`typedef enum _ar_heap_align_bytes ar_heap_align_bytes`**

enum for heap memory byte alignments

**`typedef enum _ar_heap_id ar_heap_id`**

enum for heap memory ids

**`typedef enum _ar_heap_pool_type ar_heap_pool_type`**

enum for heap memory types

**`typedef struct ar_heap_info_t ar_heap_info`**

Heap memory info structure

**`typedef struct ar_heap_info_t *par_heap_info`**

Enums

**`enum _ar_heap_align_bytes`**

enum for heap memory byte alignments

*Values:*

**`enumerator AR_HEAP_ALIGN_DEFAULT`**

**`enumerator AR_HEAP_ALIGN_4_BYTES`**

default alignment

**`enumerator AR_HEAP_ALIGN_8_BYTES`**

4-byte boundary

**`enumerator AR_HEAP_ALIGN_16_BYTES`**

8-byte boundary

**`enum _ar_heap_id`**

enum for heap memory ids

*Values:*

**`enumerator AR_HEAP_ID_DEFAULT`**

**`enumerator AR_HEAP_ID_1`**

default heap id

**`enumerator AR_HEAP_ID_2`**

custom heap id 1

**`enumerator AR_HEAP_ID_3`**

custom heap id 2

**`enumerator AR_HEAP_ID_4`**

custom heap id 3

**`enumerator AR_HEAP_ID_5`**

custom heap id 4

**`enumerator AR_HEAP_ID_6`**

custom heap id 5

**`enumerator AR_HEAP_ID_7`**

custom heap id 6

**`enumerator AR_HEAP_ID_8`**

custom heap id 7

**`enumerator AR_HEAP_ID_9`**

custom heap id 8

**`enumerator AR_HEAP_ID_10`**

custom heap id 9

**`enumerator AR_HEAP_ID_11`**

custom heap id 10

**`enum _ar_heap_pool_type`**

enum for heap memory types

*Values:*

**`enumerator AR_HEAP_POOL_DEFAULT`**

default pool type, as supported by each platform.

**`enumerator AR_HEAP_POOL_NON_PAGED_EXECUTE`**

allocated memory is nonpaged and executable that is, instruction execution is enabled in this memory.

**`enumerator AR_HEAP_POOL_NON_PAGED_NX`**

allocated memory is nonpaged and instruction execution is disabled.

**`enumerator AR_HEAP_POOL_PAGED`**

allocated memory is pageable.

Functions

**`int32_t ar_heap_init`(`void`)**

ar_heap_init initialize heap memory interface.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_heap_deinit`(`void`)**

ar_heap_deinit. De-initialize heap memory interface.

**Returns:**

0 — Success Nonzero — Failure

**`void *ar_heap_malloc`(`size_t bytes`, `par_heap_info heap_info`)**

Allocates heap memory.

**Parameters:**

- **bytes** – **[in]** number of bytes to allocate heap memory.
- **heap_info** – **[in]** pointer of type: ar_heap_info.

**Returns:**

Nonzero — Success: pointer to the allocated heap memory NULL — Failure

**`void *ar_heap_calloc`(`size_t bytes`, `par_heap_info heap_info`)**

Allocates heap memory and initialize with 0.

**Parameters:**

- **bytes** – **[in]** number of bytes to allocate heap memory.
- **heap_info** – **[in]** pointer of type: ar_heap_info.

**Returns:**

Nonzero — Success: pointer to the allocated heap memory NULL — Failure

**`void ar_heap_free`(`void *heap_ptr`, `par_heap_info heap_info`)**

Frees heap memory.

**Parameters:**

**heap_ptr** – **[in]** pointer to heap memory obtained from ar_heap_alloc().

**Returns:**

0 — Success Nonzero — Failure

**`struct ar_heap_info_t`**

*#include <ar_osal_heap.h>*Heap memory info structure

Public Members

**`ar_heap_align_bytes align_bytes`**

**`ar_heap_pool_type pool_type`**

heap memory byte alignment required.

**`ar_heap_id heap_id`**

pool type to allocate heap memory.

**`uint32_t tag`**

head id to allocate heap memory.

## ar_osal_mem_op

Defines public APIs for memory operations.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_mem_cpy`(`void *dest`, `size_t dest_size`, `const void *src`, `size_t size`)**

ar_mem_cpy copies bytes between buffers.

**Parameters:**

- **[in_out]** – dest: destinatiopn buffer to copy data.
- **dest_size** – **[in]** destination buffer size.
- **src** – **[in]** source buffer pointer to copy data from.
- **size** – **[in]** bytes to copy from source buffer.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_mem_move`(`void *dest`, `size_t dest_size`, `const void *src`, `size_t size`)**

ar_mem_move copies bytes from source area to destination area.

**Parameters:**

- **[in_out]** – dest: destinatiopn buffer to copy data.
- **dest_size** – **[in]** destination buffer size.
- **src** – **[in]** source buffer pointer to copy data from.
- **size** – **[in]** bytes to copy from source buffer.

**Returns:**

0 — Success Nonzero — Failure note: If some regions of the source area and the destination overlap, ar_mem_move ensures that the original source bytes in the overlapping region are copied before being overwritten.

**`int32_t ar_mem_set`(`void *dest`, `int32_t c`, `size_t size`)**

ar_mem_set set buffer to specified value.

**Parameters:**

- **[in_out]** – dest: destinatiopn buffer to set the specified value.
- **c** – **[in]** specified value to set, of integer type.
- **size** – **[in]** buffer bytes to set the value, must be multiple of specified value “c” data size.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_mem_cmp`(`const void *buff1`, `const void *buff2`, `size_t size`)**

ar_mem_cmp compare two buffers.

**Parameters:**

- **buff1** – **[in]** first buffer.
- **buff2** – **[in]** second buffer.
- **size** – **[in]** bytes to compare.

**Returns:**

< 0 buff1 < buff2 0 buff1 == buff2  0 buff1 > buff2

## ar_osal_servreg

Defines public APIs for service location, notification and state registration.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_OSAL_SERVREG_NAME_LENGTH_MAX`**

Max length of the domain name i.e “soc/domain/subdomain” or service name i.e “provider/service” is 64 bytes e.g. msm/adsp/audio_pd or avs/audio or audio/avs_mdf_sdsp or audio/avs_mdf_mdsp

Typedefs

**`typedef void *ar_osal_servreg_t`**

ar osal servreg type object.

**`typedef enum ar_osal_service_state ar_osal_service_state_type`**

Service state up/down indicator.

**`typedef enum ar_osal_client ar_osal_client_type`**

Servreg client type: listener or service provider.

**`typedef enum ar_osal_servreg_cb_event ar_osal_servreg_cb_event_type`**

Servreg callback notify events.

**`typedef struct ar_osal_servreg_state_notify_payload ar_osal_servreg_state_notify_payload_type`**

servreg service state notify callback payload.

**`typedef void (*ar_osal_servreg_callback)(ar_osal_servreg_t servreg_handle, ar_osal_servreg_cb_event_type event_id, void *cb_context, void *payload, uint32_t payload_size)`**

ar_osal_servreg_callback Callback function to notify clients for any changes in service state(up/down).

**Param servreg_handle:**

**[in]** Servreg handle returned with ar_osal_servreg_register() for the given service.

**Param event_id:**

**[in]** callback event id supported by ar_osal_servreg_cb_event_type .

**Param cb_context:**

**[in]** payload/context provided by client in ar_osal_servreg_register() . .

**Param payload:**

**[in]** payload provided by the callback. . service state UP/DOWN payload ar_osal_servreg_state_notify_payload_type. .

**Param payload_size:**

**[in]** payload size in bytes.

**Return:**

none

Enums

**`enum ar_osal_service_state`**

Service state up/down indicator.

*Values:*

**`enumerator AR_OSAL_SERVICE_STATE_DOWN`**

**`enumerator AR_OSAL_SERVICE_STATE_UP`**

**`enum ar_osal_client`**

Servreg client type: listener or service provider.

*Values:*

**`enumerator AR_OSAL_CLIENT_INVALID`**

**`enumerator AR_OSAL_CLIENT_LISTENER`**

**`enumerator AR_OSAL_CLIENT_SERVICE_PROVIDER`**

**`enum ar_osal_servreg_cb_event`**

Servreg callback notify events.

*Values:*

**`enumerator AR_OSAL_SERVICE_STATE_NOTIFY`**

Functions

**`int32_t ar_osal_servreg_init`(`void`)**

ar_osal_servreg_init Initialize servreg interface. Note:This API has to be called before any other API in this interface. Should be called at least once and is expected to be serialized if called multiple times.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_servreg_deinit`(`void`)**

ar_osal_servreg_deinit Uninitialize servreg interface. Should be called in pair with ar_osal_servreg_init() and should be a serialized call.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_servreg_get_domainlist`(`ar_osal_servreg_entry_type *service`, `ar_osal_servreg_entry_type *domain_list`, `uint32_t *num_domains`)**

ar_osal_servreg_get_domainlist Client to call this API to get a list of domains(msm/domain/subdomain) on which a given service(provider/service) is supported.

**Parameters:**

- **service** – **[in]** service(provider/service) for which domain(s) list is required.
- **domain_list** – **[inout]** service supported in domain(s), client to provide . payload buffer pointer.
- **num_domains** – **[inout]** Client to provide the num_domains to get the domain list. . If num_domains is zero and domain_list is NULL, API will return . the number of domains for the given service if available.

**Returns:**

0 — Success Nonzero — Failure AR_ENOMEMORY- Failed due to insufficient memory, client to call the API again with required size as returned in num_domains.

**`ar_osal_servreg_t ar_osal_servreg_register`(`ar_osal_client_type client_type`, `ar_osal_servreg_callback cb_func`, `void *cb_context`, `ar_osal_servreg_entry_type *domain`, `ar_osal_servreg_entry_type *service`)**

ar_osal_servreg_register Service client(s) to register for the domain service state change notifications.

**Parameters:**

- **client_type** – **[in]** indicates registering client is a listener or service provider.
- **[in** – opt] cb_func: callback function pointer to get notifications on. . This is parameter is optional to Service provider registration.
- **[in** – opt] cb_context: callback function payload/context provided by client. . This is parameter is optional to Service provider registration.
- **domain** – **[in]** domain of the service(msm/domain/subdomain) for which the . state change notifications to be provided.
- **service** – **[in]** service(provider/service) for which the . state change notifications to be provided.

**Returns:**

servreg_handle on success. null on failure.

**`int32_t ar_osal_servreg_deregister`(`ar_osal_servreg_t servreg_handle`)**

ar_osal_servreg_deregister Service client(s) to deregister for the service state change notifications.

**Parameters:**

**servreg_handle** – **[in]** interface handle returned by ar_osal_servreg_register().

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_servreg_set_state`(`ar_osal_servreg_t servreg_handle`, `ar_osal_service_state_type state`)**

ar_osal_servreg_set_state Service provider to call this API to register its service states(UP/DOWN). This API to be used only by the service provider(msm/domain/subdomain/provider/service) and not by service client(s).

**Parameters:**

- **servreg_handle** – **[in]** interface handle returned by ar_osal_servreg_register().
- **state** – **[in]** new service state for service registered using ar_osal_servreg_register().

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_servreg_restart_service`(`ar_osal_servreg_t servreg_handle`)**

ar_osal_servreg_restart_service HLOS calls this API to trigger a restart (PDR or SSR) on a given processor

**Parameters:**

**servreg_handle** – **[in]** interface handle returned by ar_osal_servreg_register() which identifies the desired processor

**Returns:**

0 — Success Nonzero — Failure

**`void ar_osal_panic`()**

induce panic to crash the system

**`struct ar_osal_servreg_entry_type`**

*#include <ar_osal_servreg.h>*Struct representing the name of the service or domain and the instance id

Public Members

**`char_t name[AR_OSAL_SERVREG_NAME_LENGTH_MAX + 1]`**

< Name of the service or domain. Instance ID.

**`uint32_t instance_id`**

**`struct ar_osal_servreg_state_notify_payload`**

*#include <ar_osal_servreg.h>*servreg service state notify callback payload.

Public Members

**`ar_osal_servreg_entry_type service`**

**`ar_osal_servreg_entry_type domain`**

**`ar_osal_service_state_type service_state`**

## ar_osal_signal

Defines public APIs for signal.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

## ar_osal_signal2

Defines public APIs for signal2 used by DSP.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_osal_signal2_init`(`ar_osal_signal2_t signal2`)**

Initializes a signal2 object. Signal returns the initialized object. The signal object is initially cleared. signal object memory is allocated by the client.

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**signal2** – **[in]** Pointer to the initialized object.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_signal2_deinit`(`ar_osal_signal2_t signal2`)**

De-initializes signal2 object.

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**signal2** – **[in]** Pointer to the initialized object.

**Returns:**

0 — Success Nonzero — Failure

**`size_t ar_osal_signal2_get_size`(`void`)**

Get signal object size for object memory allocation by client.

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Returns:**

Size of signal object

**`int32_t ar_osal_signal2_create`(`ar_osal_signal2_t *signal2`)**

Signal object memory is allocated and initialized by this API. osal_signal2_create() or osal_signal2_init() would be used, but not both.

**Associated data types**ar_osal_signal2_t

**Dependencies**

**Parameters:**

**[Out]** – signal2: Pointer to the initialized object.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_osal_signal2_destroy`(`ar_osal_signal2_t signal2`)**

Destroys the specified signal object.

@note1cont Signal objects must not be destroyed while they are still in use. If this happens the behavior is undefined. @note1cont In general, application code should “destroy” a signal2 object prior to deallocating it; calling osal_signal2_destroy() before deallocating it ensures that all osal_signal2_set() calls have completed.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

**signal2** – **[in]** Pointer to the signal object to destroy.

**Returns:**

0 — Success Nonzero — Failure

**`uint32_t ar_osal_signal2_wait_any`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

Suspends the current thread until any of the specified signals are set.

Signals are represented as bits 0-31 in the 32-bit mask value. A mask bit value of 1 indicates that a signal is to be waited on, and 0 that it is not to be waited on.

If a thread is waiting on a signal object for any of the specified set of signals to be set, and one or more of those signals is set in the signal object, then the thread is awakened.

At most one thread can wait on a signal object at any given time.

Signals must be explicitly cleared by a thread when it is awakened the wait operations do not automatically clear them.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** Pointer to the signal object to wait on.
- **signal2_mask** – **[in]** Mask value identifying the individual signals in the signal object to be waited on.

**Returns:**

A 32 bit word with current signals.

**`uint32_t ar_osal_signal2_wait_all`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

Suspends the current thread until all of the specified signals are set.

Signals are represented as bits 0-31 in the 32-bit mask value. A mask bit value of 1 indicates that a signal is to be waited on, and 0 that it is not to be waited on.

If a thread is waiting on a signal object for all of the specified set of signals to be set, and all of those signals are set in the signal object, then the thread is awakened.

At most one thread can wait on a signal object at any given time.

Signals must be explicitly cleared by a thread when it is awakened the wait operations do not automatically clear them.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** Pointer to the signal object to wait on.
- **signal2_mask** – **[in]** Mask value which identifies the individual signals in the signal object to be waited on.

**Returns:**

A 32 bit word with current signals.

**`int32_t ar_osal_signal2_set`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

Sets signals in the specified signal object.

Signals are represented as bits 0-31 in the 32-bit mask value. A mask bit value of 1 indicates that a signal is to be set, and 0 that it is not to be set.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal2** – **[in]** Pointer to the signal object to be modified.
- **signal2_mask** – **[in]** Mask value identifying the individual signals to be set in the signal object.

**Returns:**

0 — Success Nonzero — Failure

**`uint32_t ar_osal_signal2_get`(`ar_osal_signal2_t signal2`)**

Gets a signal from a signal object.

Returns the current signal values of the specified signal object.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

**signal2** – **[in]** Pointer to the signal object to access.

**Returns:**

A 32 bit word with current signals

**`int32_t ar_osal_signal2_clear`(`ar_osal_signal2_t signal2`, `uint32_t signal2_mask`)**

Clear signals in the specified signal object.

Signals are represented as bits 0-31 in the 32-bit signal2_mask value. A signal2_mask bit value of 1 indicates that a signal is to be cleared, and 0 that it is not to be cleared.

Signals must be explicitly cleared by a thread when it is awakened the wait operations do not automatically clear them.

**Associated data types**ar_osal_signal2_t

**Dependencies** None.

**Parameters:**

- **signal** – **[in]** Pointer to the signal object to modify.
- **signal2_mask** – **[in]** signal2_mask value identifying the individual signals to be cleared in the signal object.

**Returns:**

0 — Success Nonzero — Failure

## ar_osal_sleep

This file contains APIs to suspend thread execution for the required duration.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Functions

**`int32_t ar_osal_micro_sleep`(`uint64_t micro_seconds`)**

Micro second sleep function. Sleep internal may not be accurate as requested, it would vary based on resolution of system clock ticks. Note that a ready thread is not guaranteed to run immediately. Consequently, the thread may not run until some time after the sleep interval elapses.

**Dependencies** None.

**Parameters:**

**micro_seconds** – **[in]** sleep duration in micro seconds.

**Returns:**

0 — Success Nonzero — Failure

## ar_osal_sys_id

Defines Supported Sub-System IDs.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_SUB_SYS_ID_INVALID`**

Invalid sub system

**`AR_MODEM_DSP`**

Used for MODEM DSP sub system

**`AR_AUDIO_DSP`**

Used for ADSP sub system

**`AR_APSS`**

Used for AP sub system

**`AR_SENSOR_DSP`**

Used for SENSOR DSP sub system

**`AR_COMPUTE_DSP`**

Used for COMPUTE DSP sub system

**`AR_CC_DSP`**

Used for Companion chip DSP (CC_DSP) sub system

**`AR_APSS2`**

Used for APSS2 sub system

**`AR_SUB_SYS_ID_FIRST`**

First sub system ID

**`AR_SUB_SYS_ID_LAST`**

Last sub system ID

**`AR_SUB_SYS_IDS_MASK`**

Bit masks representing the subsystem IDs. Update when subystem gets added or removed.

**`AR_DEFAULT_DSP`**

## ar_osal_types

This file contains basic types and pre processor macros.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`FALSE`**

**`TRUE`**

**`PAGED_FUNCTIONS_START`**

PAGING functiona and data By default, the linker assigns names such as “.text” and “.data” to the code and data sections of a driver image file. When the driver is loaded, the I/O manager makes these sections nonpaged. A nonpaged section is always memory-resident. A driver developer has the option to make designated parts of a driver pageable so that Windows can move these parts to the paging file when they are not in use. To make a code or data section pageable, the driver developer assigns a name that begins with “PAGE” to the section. The I/O manager checks the names of the sections when it loads a driver. If a section name begins with “PAGE”, the I/O manager makes the section pageable. Code that runs at IRQL >= DISPATCH_LEVEL must be memory-resident. That is, this code must be either in a nonpageable segment, or in a pageable segment that is locked in memory. If code that is running at IRQL >= DISPATCH_LEVEL causes a page fault, a bug check occurs. Drivers can use the PAGED_CODE macro to verify that pageable functions are called only at appropriate IRQLs. Paged functions Should be used at the start of functions group to be paged

**`PAGED_FUNCTIONS_END`**

Should be used at the end of functions group to be paged

**`PAGED_FUNCTION`()**

Should be used at the start of the paged function definition

**`PAGED_DATA_START`**

Paged Data Should be used at the start of the vairables group to be paged

**`PAGED_DATA_END`**

Should be used at the end of the variables group to be paged

**`__UNREFERENCED_PARAM`(`x`)**

**`__UNUSED`**

**`_In_`**

Function parameter annotations This parameter must have a valid value and will not be changed by the function

**`_In_opt_`**

This parameter may not have valid value and will not be changed by the function.

**`_Out_`**

This parameter does not have a valid value, but must be a valid value after the function call returns.

**`_Out_opt_`**

This parameter does not have a valid value before and after the function call returns.

**`_Inout_`**

This parameter must have a valid value before and should have a different value after the function call returns.

**`_Inout_opt_`**

This parameter may not have a valid value before and after the function call returns.

**`_Outptr_`**

This Parameter cannot be null and should have a valid pointer to location after the function call returns.

**`_Outptr_opt_`**

This Parameter can be null and should have a valid pointer to location after the function call returns.

**`_IRQL_requires_max_`(`irql`)**

Interrupt request level(IRQL) Driver code or system APIs can only run on certain IRQLs. Developer must ensure IRQL requirements are met. Code with in spin lock usage must not be paged. Code with in spin lock must be minimum possible. Interrupts/callbacks function running at DISPATCH IRQL (high priorities) should not be paged. Identify functions which could run at PASSIVE IRQL( low priority).

**`_IRQL_requires_min_`(`irql`)**

**`PASSIVE_LEVEL`**

Normal priority level

**`DISPATCH_LEVEL`**

Runs at high priority level, these functions should not be paged.

Typedefs

**`typedef char char_t`**

else of defined(**H2XML**) Character type

**`typedef unsigned char bool_t`**

Boolean value type.

## ar_osal_file_io

Defines public APIs for file IO operations.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_FOPEN_READ_ONLY`**

Opens for reading, file position is at the beginning. If the file does not exist, the ar_fopen call fails.

**`AR_FOPEN_WRITE_ONLY`**

Opens an empty file for writing. If the given file exists, its contents are destroyed, file position is at the beginning.

**`AR_FOPEN_READ_WRITE`**

Opens an empty file for both reading and writing. If the file exists, its contents are destroyed, file position is at the beginning.

**`AR_FOPEN_APPEND`**

Open for appending (writing at end of file), this parameter alone cannot be used with ar_fopen.

**`AR_FOPEN_WRITE_ONLY_APPEND`**

Opens for writing at the end of the file(appending). Creates the file if it does not exist.

**`AR_FOPEN_READ_WRITE_APPEND`**

Opens for reading and appending. Creates the file if it does not exist. The file position for reading is at the beginning of the file, but write data is always appended to the end of the file.

**`AR_FOPEN_READ_ONLY_WRITE`**

Opens for both reading and writing. The file must exist, file position is at the beginning of file.

Typedefs

**`typedef void *ar_fhandle`**

Structures and Typedefs

**`typedef enum ar_fseek_reference ar_fseek_reference_t`**

Enums

**`enum ar_fseek_reference`**

*Values:*

**`enumerator AR_FSEEK_BEGIN`**

The starting point is zero or the beginning of the file.

**`enumerator AR_FSEEK_END`**

The starting point is the current end-of-file position.

**`enumerator AR_FSEEK_CURRENT`**

The start point is the current value of the file pointer.

Functions

**`int32_t ar_fopen`(`ar_fhandle *handle`, `const char_t *path`, `uint32_t access`)**

ar_fopen open a file or create if does not exist.

**Parameters:**

- **handle** – **[out]** Handle to the file.
- **path** – **[in]** Absolute file path.
- **access** – **[in]** Type of access AR_FILE_OPEN_READ_ONLY AR_FILE_OPEN_WRITE_ONLY AR_FILE_OPEN_READ_WRITE AR_FOPEN_WRITE_ONLY_APPEND AR_FOPEN_READ_WRITE_APPEND AR_FOPEN_READ_ONLY_WRITE

**Returns:**

0 — Success Nonzero — Failure

**`size_t ar_fsize`(`ar_fhandle handle`)**

ar_fsize Return file size.

**Parameters:**

**handle** – **[in]** Handle to the file.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fmap`(`ar_fhandle handle`, `const void **fbuffer`)**

ar_fmap Map a file into Data Memory for Read Only access

Whether this allocates heap memory for the buffer or not is platform dependent. On some platforms with low memory this may map non-volatile storage into a readable memory window instead. To free any possible resources allocated by this call, the caller MUST call ar_funmap

**Parameters:**

- **handle** – **[in]** Handle to the file
- **fbuffer** – **[out]** A pointer to the read-only Data memory buffer

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_funmap`(`const void *fbuffer`)**

ar_funmap Un-map a file from Data Memory

This call releases a buffer obtained by a previous call to ar_fmap and frees any resources that may be in use by it. The file still needs to be closed by a call to ar_fclose

**Parameters:**

**fbuffer** – **[in]** The pointer to the file buffer obtained by ar_fmap

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fseek`(`ar_fhandle handle`, `size_t offset`, `ar_fseek_reference_t ref`)**

ar_fseek Move the file pointer for read/write to the required offset.

**Parameters:**

- **handle** – **[in]** Handle to the file.
- **offset** – **[in]** The number of bytes to move the file pointer.
- **ref** – **[in]** Refer to ar_fseek_reference_t for options.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fread`(`ar_fhandle handle`, `void *buf_ptr`, `size_t read_size`, `size_t *bytes_read`)**

ar_fread Read from file.

**Parameters:**

- **handle** – **[in]** Handle to the file.
- **[in_out]** – buf_ptr: Buffer pointer to read data into.
- **read_size** – **[in]** Data size to read from file.
- **[in_out]** – bytes_read: Actual data size read from file.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fwrite`(`ar_fhandle handle`, `void *buf_ptr`, `size_t write_size`, `size_t *bytes_written`)**

ar_fwrite write to file.

**Parameters:**

- **handle** – **[in]** Handle to the file.
- **buf_ptr** – **[in]** Buffer pointer to write data from.
- **write_size** – **[in]** Data size to write into file.
- **[in_out]** – bytes_written: Actual data size written into file.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fclose`(`ar_fhandle handle`)**

ar_fclose

**Parameters:**

**handle** – **[in]** Handle to the file.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_fdelete`(`const char_t *path`)**

ar_fdelete

**Parameters:**

**path** – **[in]** Absolute file path.

**Returns:**

0 — Success Nonzero — Failure

## ar_osal_shmem

Defines public APIs for shared memory allocation for DSP.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`AR_SHMEM_HW_ACCELERATOR_ENABLED`**

**`AR_SHMEM_HW_ACCELERATOR_DISABLED`**

Bit mask for hardware accelerator flag

**`AR_SHMEM_BIT_MASK_HW_ACCELERATOR_FLAG`**

Shift amount for hardware accelerator setup flag

**`AR_SHMEM_SHIFT_HW_ACCELERATOR_FLAG`**

Typedefs

**`typedef enum ar_shmem_memory_type ar_shmem_memory_type_t`**

enum for shmem memory type

**`typedef enum ar_shmem_cache_type ar_shmem_cache_type_t`**

enum for shmem cache type

**`typedef enum ar_shmem_buffer_index_type ar_shmem_buffer_index_type_t`**

enum for shmem offset/address buffer index type

**`typedef enum ar_shmem_pd_type ar_shmem_pd_type_t`**

Bits to indicate if hardware accelerator is enabled/disabled

**`typedef struct ar_shmem_proc_info_t ar_shmem_proc_info`**

**`typedef struct ar_shmem_info_t ar_shmem_info`**

Shared memory info structure

**`typedef struct ar_shmem_hyp_assign_phys_addr_t ar_shmem_hyp_assign_phys_addr`**

Shared memory physical address and size details for hyp assign.

**`typedef enum ar_shmem_hyp_assign_dest_sys_perm_t ar_shmem_hyp_assign_dest_sys_perm`**

Destination sub system permission bit mask types supported. Combination of permissions can be used as per requirements.

**`typedef struct ar_shmem_hyp_assign_dest_sys_info_t ar_shmem_hyp_assign_dest_sys_info`**

Destination sub system id details and permission required for hyp assign.

**`typedef struct ar_shmem_hyp_assign_phys_info_t ar_shmem_hyp_assign_phys_info`**

Hyp assign physical memory info structure.

Enums

**`enum ar_shmem_memory_type`**

enum for shmem memory type

*Values:*

**`enumerator AR_SHMEM_PHYSICAL_MEMORY`**

0 Shared physical memory allocation.

**`enumerator AR_SHMEM_VIRTUAL_MEMORY`**

1 Shared virtual memory allocation

**`enum ar_shmem_cache_type`**

enum for shmem cache type

*Values:*

**`enumerator AR_SHMEM_CACHED`**

0 cached.

**`enumerator AR_SHMEM_UNCACHED`**

1 uncached.

**`enum ar_shmem_buffer_index_type`**

enum for shmem offset/address buffer index type

*Values:*

**`enumerator AR_SHMEM_BUFFER_ADDRESS`**

0 use physical or virtual addresses.

**`enumerator AR_SHMEM_BUFFER_OFFSET`**

1 use offsets, the offset is from the base address.

**`enum ar_shmem_pd_type`**

*Values:*

**`enumerator STATIC_PD`**

**`enumerator DYNAMIC_PD`**

**`enum ar_shmem_hyp_assign_dest_sys_perm_t`**

Destination sub system permission bit mask types supported. Combination of permissions can be used as per requirements.

*Values:*

**`enumerator DEST_SYS_PERM_INVALID`**

Invalid permission bit mask.

**`enumerator DEST_SYS_PERM_EXEC`**

Execute permission bit mask.

**`enumerator DEST_SYS_PERM_WRITE_ONLY`**

Write only permission bit mask.

**`enumerator DEST_SYS_PERM_EXEC_WRITE`**

Execute and Write permission.

**`enumerator DEST_SYS_PERM_READ_ONLY`**

Read only permission bit mask.

**`enumerator DEST_SYS_PERM_EXEC_READ`**

Execute and Read permission.

**`enumerator DEST_SYS_PERM_WRITE_READ`**

Write and Read permission.

**`enumerator DEST_SYS_PERM_EXEC_WRITE_READ`**

Execute, Write and Read permission.

Functions

**`int32_t ar_shmem_init`()**

Initialize the shared memory interface (V1 API).

This function initializes the shared memory interface using the default configuration. It performs the legacy initialization flow.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_init_v2`(`uint32_t num_master_procs`, `uint32_t *master_procs`)**

Initialize the shared memory interface using a list of processor domains (V2 API).

This V2 API selects the appropriate shared memory implementation based on the provided list of processor domain IDs.

Passing num_master_procs = 0 results in behavior equivalent to the V1 API (ar_shmem_init), allowing a smooth transition from V1 to V2.

**Parameters:**

- **num_master_procs** – **[in]** Number of processor domain IDs.
- **master_procs** – **[in]** Pointer to an array of processor domain IDs.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_alloc`(`ar_shmem_info *info`)**

Allocates shared memory. Only non cached memory allocation supported. Size if multiple of 4KB and the returned is aligned to 4KB boundary. Buffer start address should be atleast 64bit multiple aligned.

**Parameters:**

**[in_out]** – info: pointer to ar_shmem_info.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_free`(`ar_shmem_info *info`)**

Frees shared memory.

**Parameters:**

**info** – **[in]** pointer to ar_shmem_info.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_map`(`ar_shmem_info *info`)**

Helps map memory with SMMU an already allocated shared memory for a give sub system. Size should be multiple of 4KB boundary. Buffer start address should be 64bit aligned.

**Parameters:**

**[in_out]** – info: pointer to ar_shmem_info. required input parameters in ar_shmem_info ar_shmem_info_t.cache_type ar_shmem_info_t.buf_size ar_shmem_info_t.mem_type ar_shmem_info_t.pa_lsw ar_shmem_info_t.pa_msw ar_shmem_info_t.num_sys_id ar_shmem_info_t.sys_id required output parameters in ar_shmem_info ar_shmem_info_t.ipa_lsw ar_shmem_info_t.ipa_msw

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_unmap`(`ar_shmem_info *info`)**

Helps unmap the shared memory allocated externally with SMMU.

**Parameters:**

**info** – **[in]** pointer to ar_shmem_info. required input parameters in ar_shmem_info ar_shmem_info_t.cache_type ar_shmem_info_t.buf_size ar_shmem_info_t.mem_type ar_shmem_info_t.pa_lsw ar_shmem_info_t.pa_msw ar_shmem_info_t.num_sys_id ar_shmem_info_t.sys_id

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_hyp_assign_phys`(`ar_shmem_hyp_assign_phys_info *info`)**

Helps to hyp assign physical memory between source and destination sub systems.

**Parameters:**

**info** – **[in]** pointer to ar_shmem_hyp_assign_phys_info.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_get_uid`(`uint64_t alloc_handle`, `uint64_t *uid`)**

ar_shmem_get_uid. Get associated unique identifier(UID) for the shared memory pointed by alloc_handle, platform which doesn`t support UID should return alloc_handle as UID with expectation of alloc_handle being unique.

**Parameters:**

- **alloc_handle** – **[in]** handle for the shared memory.
- **uid** – **[out]** unique identifier to the shmem.

**Returns:**

0 — Success Nonzero — Failure

**`int32_t ar_shmem_deinit`(`void`)**

ar_shmem_deinit.

**Returns:**

0 — Success Nonzero — Failure

**`struct ar_shmem_proc_info_t`**

*#include <ar_osal_shmem.h>*Public Members

**`uint8_t proc_id`**

**`ar_shmem_pd_type_t proc_type`**

**`bool_t is_active`**

**`struct ar_shmem_info_t`**

*#include <ar_osal_shmem.h>*Shared memory info structure

Public Members

**`ar_shmem_cache_type_t cache_type`**

in, cache type, cached or uncached memory

**`size_t buf_size`**

in, shared buffer size, should be a minimum of 4K and multiple of 4K only

**`ar_shmem_memory_type_t mem_type`**

out, shmem memory type, virtual or physical for ar_shmem_alloc() in, shmem memory type, virtual or physical for ar_shmem_map()

**`ar_shmem_buffer_index_type_t index_type`**

out, DSP to operate on buffer offsets or on address pointers.

**`uint32_t ipa_lsw`**

out, smmu mapped ipa lsw, output for ar_shmem_alloc()/ar_shmem_map()

**`uint32_t ipa_msw`**

out, smmu mapped ipa msw, output for ar_shmem_alloc()/ar_shmem_map()

**`uint32_t pa_lsw`**

out, physical address lsw, alignment requirements apply, like 4k, start address multiple of 64, output of ar_shmem_alloc() in, physical address lsw, alignment requirements apply, like 4k, start address multiple of 64, input for ar_shmem_map()

**`uint32_t pa_msw`**

out, physical address msw, alignment requirements apply, like 4k, start address multiple of 64, output of ar_shmem_alloc() in, physical address lsw, alignment requirements apply, like 4k start address multiple of 64, input for ar_shmem_map()

**`void *vaddr`**

out, virtual address 64bit/32bit, alignment requirements apply, like 4k, start address multiple of 64, input for ar_shmem_alloc()

**`uint64_t metadata`**

out opt, pointer address to metadata structure defined by each platform for ar_shmem_alloc()

**`uint8_t num_sys_id`**

in, number of subsystem IDs provided with ar_shmem_alloc()/ar_shmem_map() call.

**`ar_shmem_proc_info *sys_id`**

in, pointer to array of size num_sys_id for sub-system Ids provided in ar_osal_sys_id.h, used to allocate shared memory between the given list of sys_id provided with ar_shmem_alloc()/ar_shmem_map() call.

**`uint32_t platform_info`**

in opt, optional field for passing platform specific data to OSAL, this can be used for example to communicate some heap properties provided only for ar_shmem_alloc()

**`uint32_t flags`**

in, Bit field for flags.  1 — hardware accelerator enabled, use AR_SHMEM_HW_ACCELERATOR_ENABLED 0 — hardware accelerator disabled, use AR_SHMEM_HW_ACCELERATOR_DISABLED To set this bit, use AR_SHMEM_BIT_MASK_HW_ACCELERATOR_FLAG and AR_SHMEM_SHIFT_HW_ACCELERATOR_FLAG All other bits are reserved; must be set to 0.

**`struct ar_shmem_hyp_assign_phys_addr_t`**

*#include <ar_osal_shmem.h>*Shared memory physical address and size details for hyp assign.

Public Members

**`uint64_t phys_addr`**

64-bit physical address.

**`size_t size`**

size in bytes for the buffer pointed by phys_addr

**`struct ar_shmem_hyp_assign_dest_sys_info_t`**

*#include <ar_osal_shmem.h>*Destination sub system id details and permission required for hyp assign.

Public Members

**`uint64_t dest_sys_id`**

destination sub system id, refer to ar_osal_sys_id.h

**`ar_shmem_hyp_assign_dest_sys_perm dest_perm`**

destination permissions

**`struct ar_shmem_hyp_assign_phys_info_t`**

*#include <ar_osal_shmem.h>*Hyp assign physical memory info structure.

Public Members

**`ar_shmem_hyp_assign_phys_addr *phys_addr_list`**

list of hyp_assign_phys_addr structures.

**`uint32_t phys_addr_list_size`**

number of phys_addr_list entries.

**`uint64_t *src_sys_list`**

source sub system Id list, refer to ar_osal_sys_id.h for sys ids.

**`uint32_t src_sys_list_size`**

number of src_sys_list entries.

**`ar_shmem_hyp_assign_dest_sys_info *dest_sys_list`**

destination sys list hyp_assign_dest_sys_info.

**`uint32_t dest_sys_list_size`**

number of destination sys list/dest_sys_list entires.

**`uint64_t metadata`**

in opt, pointer address to metadata structure defined by platform during ar_shmem_alloc() call.

## ar_osal_string

Defines public APIs for string operations.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`ar_sprintf`(`str_dest`, `str_dest_size`, `format`, `...`)**

ar_sprintf Write formated data to a string.

ar_sscanf Read formated data from a string.

**Parameters:**

- **[in_out]** – str_dest: Destination string buffer.
- **str_dest_size** – **[in]** Size in bytes.
- **format** – **[in]** Format control string.
- **...** – **[in]** : variable arguments.
- **str_src** – **[in]** Stored string buffer.
- **format** – **[in]** Format control string.
- **...** – **[in]** : variable arguments.

**Returns:**

Number of characters written to the buffer(null terminator not counted). Destination is appended with null terminator always, if data is greater than the destination buffer size, truncation will occur with appended null terminator.

**Returns:**

Number of fields successfully converted and assigned, the return value does not include fields that were read but not assigned. A return value of 0 indicates that no fields were assigned.

**`ar_sscanf`(`str_src`, `format`, `...`)**

Functions

**`size_t ar_strlen`(`const char_t *str`, `size_t size`)**

ar_strlen Get the length of the string.

**Parameters:**

- **str** – **[in]** NULL terminated string buffer pointer.
- **size** – **[in]** String buffer size in bytes.

**Returns:**

Number of characters in the string, not including the terminating null character. If there is no null terminator in the buffer, provided string buffer size is returned to indicate the error.

**`int32_t ar_strcpy`(`char_t *str_dest`, `size_t str_dest_size`, `const char_t *str_src`, `size_t cpy_size`)**

ar_strcpy Copies character from source to destination string.

**Parameters:**

- **[in_out]** – str_dest: Destination string buffer.
- **str_dest_size** – **[in]** Size in characters.
- **str_src** – **[in]** Source string to copy from.
- **cpy_size** – **[in]** Size in characters to copy from source string.

**Returns:**

0 — Success Nonzero — Failure note: Always null terminator is appended to the destination and string truncation will occur if destination size is smaller or equal to characters copy size.

**`int32_t ar_strcmp`(`const char_t *str1`, `const char_t *str2`, `size_t num`)**

ar_strcmp Compare characters in two given strings.

**Parameters:**

- **str1** – **[in]** Null terminated string 1
- **str2** – **[in]** Null terminated string 2
- **num** – **[in]** number of characters to compare.

**Returns:**

< 0 str1 < str2 0 str1 == str2  0 str1 > str2

**`int32_t ar_strcat`(`char_t *str_dest`, `size_t str_dest_size`, `const char_t *str_src`, `size_t apnd_size`)**

ar_strcat Append character from source to destination string.

**Parameters:**

- **[in_out]** – str_dest: Destination string buffer.
- **str_dest_size** – **[in]** Size in characters.
- **str_src** – **[in]** Source string to copy from.
- **apnd_size** – **[in]** Size in characters to append from source string.

**Returns:**

0 — Success Nonzero — Failure note: Always null terminator is appended to the destination after concatenation and string truncation will occur if destination size is smaller or equal to source.

**`char_t *ar_strstr`(`const char_t *str`, `const char_t *str_search`)**

ar_strstr Search string in string.

**Parameters:**

- **str** – **[in]** Null terminated string
- **str_search** – **[in]** Null terminated string to search for.

**Returns:**

Pointer to the first occurrence of str_search in str. NULL- if not found.

## ar_osal_thread

Defines public APIs for thread.

**Copyright** Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

**`struct ar_osal_thread_attr_t`**

*#include <ar_osal_thread.h>*Thread attributes.

Public Members

**`char_t *thread_name`**

Pointer to the thread name

**`uint32_t stack_size`**

Size of the thread stack

**`int32_t priority`**

Thread priority
