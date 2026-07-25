# POSAL API’s

## posal_cache

This file contains utilities for cache operations.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef` `void` `*``posal_mem_addr_t`**

## posal_data_log

Posal data log apis.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`SPF_LOG_PREFIX`**

Typedefs

**`typedef` `enum` `posal_data_log_format_t` `posal_data_log_format_t`**

Log data formats.

**`typedef` `enum` `posal_data_log_mode_t` `posal_data_log_mode_t`**

**`typedef` `struct` `posal_data_log_pcm_info_t` `posal_data_log_pcm_info_t`**

PCM data information for the logging utility user.

**`typedef` `struct` `posal_data_log_fmt_info_t` `posal_data_log_fmt_info_t`**

Format of the data being logged: PCM or bitstream.

**`typedef` `struct` `posal_data_log_info_t` `posal_data_log_info_t`**

Log header and data payload information for the logging utility user.

Enums

**`enum` `posal_data_log_format_t`**

Log data formats.

*Values:*

**`enumerator` `LOG_DATA_FMT_PCM`**

PCM data format.

**`enumerator` `LOG_DATA_FMT_BITSTREAM`**

Bitstream data format.

**`enumerator` `LOG_DATA_FMT_RAW`**

Raw data format.

**`enum` `posal_data_log_mode_t`**

*Values:*

**`enumerator` `LOG_DEFAULT`**

**`enumerator` `LOG_IMMEDIATE`**

Functions

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_data_log_code_status`(`uint32_t` `log_code`)**

This function checks if the cog code is enabled .

**Dependencies**None

**Returns:**

TRUE if the log code is enabled and FALSE if it is disabled.

**`uint32_t` `posal_data_log_get_max_buf_size`()**

This function gives the maximum packet size allowed for logging.

**Dependencies**None

**`void` `*``posal_data_log_alloc`(`uint32_t` `buf_Size`, `uint32_t` `log_code`, `posal_data_log_format_t` `data_fmt`)**

Allocates a log packet for PCM/bitstream data logging.

**Associated data types**#log_data_format  **Dependencies**None.

**Parameters:**

- **buf_Size** – **[in]** Size of the data payload, excluding the log header.
- **log_code** – **[in]** Log code for this log packet.
- **data_fmt** – **[in]** PCM or bitstream data format.

**Returns:**

Pointer to payload of the allocated log packet. Returns NULL if buffer allocation fails or log code is disabled.

**`ar_result_t` `posal_data_log_commit`(`void` `*``log_pkt_payload_ptr`, `posal_data_log_info_t` `*``log_info_ptr`)**

Populates the log header and data payload of an allocated log packet and commits the packet for logging.

****Nonzero — Failure  **Dependencies**None

**Parameters:**

- **log_pkt_payload_ptr** – **[in]** Pointer to payload of the allocated log packet.
- **log_tap_id** – **[in]** Tap point ID of the log packet.
- **session_id** – **[in]** Session ID of the log packet.
- **buf_size** – **[in]** Payload size of the log packet.

**Returns:**

0 — Success

**`ar_result_t` `posal_data_log_alloc_commit`(`posal_data_log_info_t` `*``log_info_ptr`)**

Allocates the log packet, populates the log header and data payload, and commits the packet for logging.

**Associated data types**#log_info  ****Nonzero — Failure  **Dependencies**None

**Parameters:**

**log_info_ptr** – **[in]** Pointer to the object containing the log header and data payload information for the logging utility client.

**Returns:**

0 — Success

**`void` `posal_data_log_free`(`void` `*``log_pkt_payload_ptr`)**

This function frees the data log buffer in case of error scenerio.

**Dependencies**None

**Parameters:**

**log_ptr** – **[in]** : payload of the data log buffer to be freed

**Returns:**

None.

**`struct` `posal_data_log_pcm_info_t`**

*#include <posal_data_log.h>*PCM data information for the logging utility user.

Public Members

**`uint32_t` `sampling_rate`**

PCM sampling rate. 8000 Hz, 48000 Hz, etc.

**`uint16_t` `num_channels`**

Number of channels in the PCM stream.

**`uint8_t` `bits_per_sample`**

Bits per sample for the PCM data.

**`uint8_t` `interleaved`**

Specifies whether the data is interleaved.

**`uint8_t` `q_factor`**

q factor information for log packet.

**`uint8_t` `data_format`**

data_format information for log packet.

**`uint16_t` `*``channel_mapping`**

Array of channel mappings.

**`struct` `posal_data_log_fmt_info_t`**

*#include <posal_data_log.h>*Format of the data being logged: PCM or bitstream.

Public Members

**`posal_data_log_pcm_info_t` `pcm_data_fmt`**

Format of the PCM data.

**`uint32_t` `media_fmt_id`**

Format of the bitstream data.

**`struct` `posal_data_log_info_t`**

*#include <posal_data_log.h>*Log header and data payload information for the logging utility user.

Public Members

**`uint32_t` `log_code`**

log code for the log packet.

**`int8_t` `*``buf_ptr`**

Pointer to the buffer to be logged.

**`uint32_t` `buf_size`**

Size of the payload to be logged, in bytes.

**`uint32_t` `session_id`**

Session ID for the log packet.

**`uint32_t` `log_tap_id`**

GUID for the tap point.

**`uint64_t` `log_time_stamp`**

Timestamp in microseconds.

**`posal_data_log_format_t` `data_fmt`**

Data format for the log packet.

**`posal_data_log_fmt_info_t` `data_info`**

Pointer to the data packet information.

**`uint32_t` `*``seq_number_ptr`**

Reference to sequence number variable shared by client.

## posal_globalstate

This file contains the global state structure for the posal environment. This state includes system-wide information such as the number of active threads and malloc counters.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

**`struct` `posal_mem_stats_t`**

*#include <posal_globalstate.h>*Memory usage statistics obtained during a test case run.

Public Members

**`uint32_t` `num_mallocs`**

Total number of memory allocations up to the current point in the test.

**`uint32_t` `num_frees`**

Total number of times memory is freed to the current point in the test.

**`uint32_t` `curr_heap`**

Current heap usage at the current point in the test.

**`uint32_t` `peak_heap`**

Peak heap usage up to the current point in the test.

**`struct` `posal_globalstate_t`**

*#include <posal_globalstate.h>*Global structure used to track resources, such as threads and queues. This structure is intended for use in such tasks as debugging and checking for leaks.

Public Members

**`posal_mem_stats_t` `avs_stats``[``POSAL_HEAP_MGR_MAX_NUM_HEAPS` `+` `1``]`**

Heap statistics for Audio-Voice Subsystem (AVS) threads.

This number comprises one default heap plus the #POSAL_HEAP_MGR_MAX_NUM_HEAPS non-default heap.

**`posal_mem_stats_t` `non_avs_stats`**

Heap statistics for non-AVS threads.

**`volatile` `int32_t` `nSimulatedMallocFailCount`**

If the failure count > 0, counts memory allocations down to zero, and then simulates out-of-memory. This count is used for testing.

**`posal_atomic_word_t` `nMsgQs`**

Counter of queues to help generate unique names.

**`posal_atomic_word_t` `nMemRegions`**

Counter of the number of memory regions in a system.

**`posal_mutex_t` `mutex`**

Mutex for thread safety of this structure.

**`posal_memorymap_client_t` `*``mem_map_client_list``[``POSAL_MEMORY_MAP_MAX_CLIENTS``]`**

Linked list of memory map clients in the system.

**`uint32_t` `num_registered_memmap_clients`**

**`volatile` `uint32_t` `bEnableQLogging`**

Logs the commands going into queues and coming out of queues.

**`volatile` `uint32_t` `uSvcUpStatus`**

Specifies whether the aDSP static services are up and ready.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_global_init_done`**

Flag to set if global init is done.

**`struct` `posal_memorymap_client_t`**

*#include <posal_globalstate.h>*Maintains a linked list of clients registered with posal_memorymap.

Public Members

**`posal_memorymap_node_t` `*``pMemMapListNode`**

List of memory map nodes for this client.

**`posal_mutex_t` `mClientMutex`**

Mutex to access the list.

**`uint32_t` `client_id`**

Client ID.

## posal_heapmgr

This file contains utilities for memory allocation and release. This file provides memory allocation functions and macros for both C and C++.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_internal_inline

Internal definitions. Helps optimize by making inline calls. Must not be used by shared libraries due to backward compatibility concerns.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`static` `inline` `uint32_t` `posal_channel_wait_inline`(`posal_channel_t` `pChannel`, `uint32_t` `unEnableBitfield`)**

**`static` `inline` `uint32_t` `posal_channel_poll_inline`(`posal_channel_t` `pChannel`, `uint32_t` `unEnableBitfield`)**

**`static` `inline` [`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_island_get_island_status_inline`(`void`)**

**`static` `inline` `void` `posal_mutex_unlock_inline`(`posal_mutex_t` `posal_mutex`)**

**`static` `inline` `void` `posal_mutex_lock_inline`(`posal_mutex_t` `posal_mutex`)**

**`static` `inline` `posal_channel_t` `posal_signal_get_channel_inline`(`posal_signal_t` `p_signal`)**

**`static` `inline` `uint32_t` `posal_signal_get_channel_bit_inline`(`posal_signal_t` `p_signal`)**

**`static` `inline` `void` `posal_signal_clear_inline`(`posal_signal_t` `p_signal`)**

**`static` `inline` [`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_signal_is_set_inline`(`posal_signal_t` `p_signal`)**

**`struct` `posal_channel_internal_t`**

*#include <posal_internal_inline.h>*Public Members

**`qurt_signal2_t` `anysig`**

Any 32-bit signal channel.

**`uint32_t` `unBitsUsedMask`**

Mask bookkeeping for used bits.  1 — Used 0 — Available

**`struct` `posal_signal_internal_t`**

*#include <posal_internal_inline.h>*Signal to be triggered by events, or used to trigger events. The signal coalesces on a channel bit. The only way to receive a signal is through its associated channel.

Public Members

**`posal_channel_internal_t` `*``pChannel`**

Pointer to the associated channel.

**`uint32_t` `unMyChannelBit`**

Channel bitfield of this signal.

## posal_island

This file contains island utilities’ declarations.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Enums

**`enum` `posal_island_heap_t`**

*Values:*

**`enumerator` `POSAL_ISLAND_HEAP_Q6_TCM`**

**`enumerator` `POSAL_ISLAND_HEAP_LPASS_TCM`**

**`enumerator` `POSAL_ISLAND_HEAP_LLC`**

**`enumerator` `POSAL_ISLAND_HEAP_NUM_SUPPORTED`**

Functions

**`POSAL_HEAP_ID` `posal_private_get_island_heap_id_v2`(`uint32_t` `island_heap_type`)**

Private Api for getting island heap id

**`posal_mem_t` `posal_private_get_mem_type_from_heap_type`(`uint32_t` `island_heap_type`)**

Private Api for getting posal mem type

**`ar_result_t` `posal_island_trigger_island_exit`(`void`)**

This function process island exit.

**Dependencies**None.

**Returns:**

Indication of success (0) or failure (nonzero).

**`static` `inline` `ar_result_t` `posal_island_trigger_island_exit_inline`(`void`)**

Inline function to exit island when USES_AUDIO_IN_ISLAND is not defined

**Dependencies**None.

**Returns:**

Indication of success (0) or failure (nonzero).

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_island_get_island_status`(`void`)**

This function Get island mode status.

Returns a value indicating whether the underlying system is executing in island mode.

**Dependencies**None.

**Returns:**

0 - Normal mode. 1 - Island mode.

**`static` `inline` `POSAL_HEAP_ID` `posal_get_island_heap_id`(`void`)**

**`static` `inline` `POSAL_HEAP_ID` `posal_get_island_heap_id_v2`(`posal_island_heap_t` `heap_type`)**

**`static` `inline` `POSAL_HEAP_ID` `posal_get_heap_id`(`posal_mem_t` `mem_type`)**

**`static` `inline` `posal_mem_t` `posal_get_mem_type_from_heap_type`(`posal_island_heap_t` `heap_type`)**

Variables

**`POSAL_HEAP_ID` `spf_mem_island_heap_id`**

Default island heap = Q6 TCM by default.

## posal_memorymap

This file contains utilities for memory mapping and unmapping of shared memory.

**Copyright**Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

**`struct` `posal_memorymap_node_t`**

*#include <posal_memorymap.h>*Public Members

**`uint32_t` `shmem_id`**

A unique identifier to map with this shared memory regions

**`uint32_t` `MemPool`**

Memory pool from which the memory region is created.

**`uint16_t` `unNumContPhysReg`**

Number of physical memory regions in this node.

**`int16_t` `ref_count`**

Reference count that the client can increment to lock this memory map handle.

Unmapping can only be performed if ref_count reaches zero.

The client must decrement ref_count when it does not use this memory map handle.

**`uint32_t` `mapping_mode`**

Specifies whether the mapping is physical or virtual, or if it is a physical offset.

**`uint32_t` `reserved`**

reserved field to ensure this structure size is 64 bytes aligned.

**`posal_memorymap_node_t` `*``pNext`**

Pointer to the next node in the linked list.

@tblsubhd{If unNumContPhysReg is greater than 1} In addition to the number of posal_memorymap_region_record_t structures following this structure, one more ContPhysReg follows to represent the master region for all ContPhysRegs (called the *virtual memory region*).

When freeing the regions, all of the following space is also freed.

**`struct` `posal_memorymap_shm_region_t`**

*#include <posal_memorymap.h>*Contiguous shared memory region, with the start address and size.

Public Members

**`uint32_t` `shm_addr_lsw`**

Lower 32 bits of the shared memory address of the memory region to map.

**`uint32_t` `shm_addr_msw`**

Upper 32 bits of the shared memory address of the memory region to map.

The 64-bit number formed by shm_addr_lsw and shm_addr_msw word must be contiguous memory, and it must be 4 KB aligned.

For a 32-bit shared memory address, this field must be set to 0. For a 36-bit shared memory address, bits 31 to 4 must be set to 0. For a 64-bit shared memory address, any 32 bit value.

**`uint32_t` `mem_size`**

Size of the shared memory region.

Number of bytes in the shared memory region.

Multiples of 4 KB

Underlying operating system must always map the regions as virtual contiguous memory, but the memory size must be in multiples of 4 KB to avoid gaps in the virtually contiguous mapped memory.

**`struct` `posal_memorymap_mem_region_attrib_t`**

*#include <posal_memorymap.h>*Memory mapped region attributes.

Public Members

**`uint32_t` `base_phy_addr_lsw`**

Lower 32 bits of the 64-bit memory region start (base) physical address.

**`uint32_t` `base_phy_addr_msw`**

Upper 32 bits of the 64-bitmemory region start (base) physical address.

The 64-bit number formed by mem_reg_base_phy_addr_lsw and mem_reg_base_phy_addr_msw word must be contiguous memory, and it must be 4 KB aligned.

For a 32-bit shared memory address, this field must be set to 0. For a 36-bit shared memory address, bits 31 to 4 must be set to 0. For a 64-bit shared memory address, any 32-bit value.

**`uint32_t` `mem_reg_size`**

Size of the shared memory region.

Number of bytes in the shared memory region.

Multiples of 4 KB

Underlying operating system must always map the regions as virtual contiguous memory, but the memory size must be in multiples of 4 KB to avoid gaps in the virtually contiguous mapped memory.

**`uint32_t` `base_virt_addr`**

Memory region start (base) virtual address.

**`uint32_t` `req_virt_adrr`**

Virtual address that corresponds to the requested physical address.

**`uint32_t` `rem_reg_size`**

Remaining memory region size from the requested physical address, including the requested physical address:

([mem_reg_base_phy_addr_msw,mem_reg_base_phy_addr_lsw] + mem_reg_size - [requested physical address])

**`struct` `posal_mem_map_v2_input_args_t`**

*#include <posal_memorymap.h>*Public Members

**`uint32_t` `unique_shmem_id_24bit`**

**`uint32_t` `client_token`**

Unique shared memory Id only LSB 24 Bits must be valid. if unique shm id is set, this will be returned as the mem map handle in the output arguments.

**`posal_memorymap_shm_region_t` `*``shm_mem_reg_ptr`**

Posal memorymap driver’s registered client token

**`uint16_t` `num_shm_reg`**

Pointer to an array of shared memory regions to map.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_cached`**

Number of shared memory regions in the array.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_offset_map`**

Indicates if mem is cached or uncached

**`POSAL_MEMORYPOOLTYPE` `pool_id`**

Indicates if the mapping is offset based as opposed to pointer based.

**`POSAL_HEAP_ID` `heap_id`**

Memory pool ID to which this region is mapped.

## posal_mutex

This file contains mutex utilites. Recursive mutexes are always used for thread-safe programming.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void` `posal_mutex_lock`(`posal_mutex_t` `posal_mutex`)**

Locks a mutex. Recursive mutexes are always used.

**Associated data types**posal_mutex_t  **Dependencies**Before calling this function, the object must be created and initialized.

**Parameters:**

**posal_mutex** – **[in]** mutex object handle.

**Returns:**

None.

**`ar_result_t` `posal_mutex_try_lock`(`posal_mutex_t` `posal_mutex`)**

Attempts to lock a mutex. If the mutex is already locked and unavailable, a failure is returned.

**Associated data types**posal_mutex_t  **Dependencies**Before calling this function, the object must be created and initialized.

**Parameters:**

**posal_mutex** – **[in]** mutex object handle.

**Returns:**

An indication of success (0) or failure (nonzero).

**`void` `posal_mutex_unlock`(`posal_mutex_t` `posal_mutex`)**

Unlocks a mutex. Recursive mutexes are always used.

**Associated data types**posal_mutex_t  **Dependencies**Before calling this function, the object must be created and initialized.

**Parameters:**

**posal_mutex** – **[in]** mutex object handle.

**Returns:**

None.

## posal_power_mgr

Lite Wrapper for PM. Mainly to serve profiling. goal is not to hide MMPM/PM details.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`PM_SERVER_CLIENT_TOKEN_PREFIX`**

**`PM_SERVER_CLIENT_TOKEN_LENGTH`**

**`PM_SERVER_CLIENT_NAME_LENGTH`**

**`PM_SERVER_CLIENT_NAME_MAX_LENGTH`**

Typedefs

**`typedef` `void` `*``posal_pm_handle_t`**

**`typedef` `enum` `posal_pm_mode_t` `posal_pm_mode_t`**

PM island types

**`typedef` `enum` `posal_pm_island_type_t` `posal_pm_island_type_t`**

PM island Vote

**`typedef` `enum` `posal_pm_island_vote_type_t` `posal_pm_island_vote_type_t`**

**`typedef` `enum` `posal_pm_cpu_lpr_id_t` `posal_pm_cpu_lpr_id_t`**

PM CPU LPR Vote type

**`typedef` `enum` `posal_pm_cpu_lpr_vote_type_t` `posal_pm_cpu_lpr_vote_type_t`**

Register information

**`typedef` `struct` `posal_pm_register_t` `posal_pm_register_t`**

**`typedef` `struct` `posal_pm_mpps_t` `posal_pm_mpps_t`**

**`typedef` `struct` `posal_pm_bw_t` `posal_pm_bw_t`**

**`typedef` `struct` `posal_pm_sleep_latency_t` `posal_pm_sleep_latency_t`**

**`typedef` `struct` `posal_pm_island_vote_t` `posal_pm_island_vote_t`**

**`typedef` `struct` `posal_pm_cpu_lpr_vote_t` `posal_pm_cpu_lpr_vote_t`**

**`typedef` `struct` `posal_pm_resources_t` `posal_pm_resources_t`**

**`typedef` `struct` `posal_pm_request_info_t` `posal_pm_request_info_t`**

**`typedef` `struct` `posal_pm_release_info_t` `posal_pm_release_info_t`**

Enums

**`enum` `posal_pm_mode_t`**

*Values:*

**`enumerator` `PM_MODE_DEFAULT`**

Non-island, non-suppressible

**`enumerator` `PM_MODE_ISLAND`**

Island, suppressible

**`enumerator` `PM_MODE_ISLAND_DUTY_CYCLE`**

Not an Island container but only BW votes are suppressible (Mainly used in BT A2DP use case)

**`enum` `posal_pm_island_type_t`**

*Values:*

**`enumerator` `PM_ISLAND_TYPE_DEFAULT`**

**`enumerator` `PM_ISLAND_TYPE_LOW_POWER`**

< default island type island type to enter STD island

**`enumerator` `PM_ISLAND_TYPE_LOW_POWER_2`**

island type to enter LLC island

**`enum` `posal_pm_island_vote_type_t`**

*Values:*

**`enumerator` `PM_ISLAND_VOTE_ENTRY`**

Island vote to be casted for island entry state

**`enumerator` `PM_ISLAND_VOTE_EXIT`**

Island vote to be casted for island exit sate

**`enumerator` `PM_ISLAND_VOTE_DONT_CARE`**

Island vote to be casted for island dont care state

**`enum` `posal_pm_cpu_lpr_id_t`**

*Values:*

**`enumerator` `PM_LPR_CPU_SS_SLEEP`**

**`enumerator` `PM_LPR_CPU_MAX`**

**`enum` `posal_pm_cpu_lpr_vote_type_t`**

*Values:*

**`enumerator` `PM_VOTE_FOR_CPU_LPR_SUB_SYSTEM_SLEEP`**

**`enumerator` `PM_VOTE_AGAINST_CPU_LPR_SUB_SYSTEM_SLEEP`**

**`enumerator` `PM_VOTE_NUM_CPU_LPR`**

Functions

**`ar_result_t` `posal_power_mgr_request`(`posal_pm_request_info_t` `*``request_info_ptr`)**

Sends request to ADSPPM

**Dependencies**None.

**Returns:**

returns error code.

**`ar_result_t` `posal_power_mgr_release`(`posal_pm_release_info_t` `*``release_info_ptr`)**

Sends release to ADSPPM

**Dependencies**None.

**Returns:**

returns error code.

**`ar_result_t` `posal_power_mgr_register`(`posal_pm_register_t` `register_info`, `posal_pm_handle_t` `*``pm_handle_pptr`, `posal_signal_t` `wait_signal`, `uint32_t` `log_id`)**

Registers for kpps and bw

**Dependencies**None.

**Returns:**

returns error code.

**`ar_result_t` `posal_power_mgr_deregister`(`posal_pm_handle_t` `*``pm_handle_pptr`, `uint32_t` `log_id`)**

Deregisters with ADSPPM

**Dependencies**None.

**Returns:**

returns error code.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_power_mgr_is_registered`(`posal_pm_handle_t` `pm_handle_ptr`)**

returns true if the client is registered.

**`ar_result_t` `posal_power_mgr_request_max_out`(`posal_pm_handle_t` `pm_handle_ptr`, `posal_signal_t` `wait_signal`, `uint32_t` `log_id`)**

bumps up the bus and Q6 clocks.

**`ar_result_t` `posal_power_mgr_release_max_out`(`posal_pm_handle_t` `pm_handle_ptr`, `uint32_t` `log_id`, `uint32_t` `delay_ms`)**

releases the bus and Q6 clocks.

**`void` `posal_power_mgr_init`()**

initalises structures and mutex (if any)

**`void` `posal_power_mgr_deinit`()**

de-initalises structures and mutex (if any)

**`ar_result_t` `posal_power_mgr_send_command`(`uint32_t` `msg_opcode`, `void` `*``payload_ptr`, `uint32_t` `payload_size`)**

To Send message commands to PM SERVER

**`struct` `posal_pm_register_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_mode_t` `mode`**

PM mode

**`posal_pm_island_type_t` `island_type`**

Island type

**`struct` `posal_pm_mpps_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

**`uint32_t` `value`**

**`uint64_t` `floor_clk`**

**`struct` `posal_pm_bw_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

**`uint32_t` `value`**

**`struct` `posal_pm_sleep_latency_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

**`uint32_t` `value`**

**`struct` `posal_pm_island_vote_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

**`posal_pm_island_vote_type_t` `island_vote_type`**

**`posal_pm_island_type_t` `island_type`**

**`struct` `posal_pm_cpu_lpr_vote_t`**

*#include <posal_power_mgr.h>*Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

**`posal_pm_cpu_lpr_id_t` `lpr_id`**

**`posal_pm_cpu_lpr_vote_type_t` `cpu_lpr_vote_type`**

**`struct` `posal_pm_resources_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_mpps_t` `mpps`**

**`posal_pm_bw_t` `bw`**

**`posal_pm_sleep_latency_t` `sleep_latency`**

**`posal_pm_island_vote_t` `island_vote`**

**`posal_pm_cpu_lpr_vote_t` `cpu_lpr_vote``[``PM_LPR_CPU_MAX``]`**

**`struct` `posal_pm_request_info_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_handle_t` `pm_handle_ptr`**

**`uint32_t` `client_log_id`**

**`posal_signal_t` `wait_signal_ptr`**

**`posal_pm_resources_t` `resources`**

**`struct` `posal_pm_release_info_t`**

*#include <posal_power_mgr.h>*Public Members

**`posal_pm_handle_t` `pm_handle_ptr`**

**`uint32_t` `client_log_id`**

**`posal_signal_t` `wait_signal_ptr`**

**`uint32_t` `delay_ms`**

**`posal_pm_resources_t` `resources`**

## posal_root_msg

Defines

**`POSAL_ROOT_VA_NUM_ARGS_IMPL`(`a`, `b`, `c`, `d`, `e`, `f`, `g`, `h`, `i`, `j`, `_N`, `...`)**

**`POSAL_ROOT_VA_NUM_ARGS`(`...`)**

**`POSAL_ROOT_TOKENPASTE`(`x`, `y`)**

**`POSAL_ROOT_MSG_x`(`_N`)**

**`POSAL_ROOT_MSG`(`xx_ss_mask`, `xx_fmt`, `...`)**

**`POSAL_ROOT_MSG_ISLAND`(`xx_ss_mask`, `xx_fmt`, `...`)**

## posal_signal

This file contains signal utilities.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_thread

This file contains utilities for threads. Threads must be joined to avoid memory leaks. This file provides functions to create and destroy threads, and to change thread priorities.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_thread_profiling

This file contains PUBLIC utilities for thread profiling.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`ar_result_t` `posal_thread_profiling_get_stack_info`(`uint32_t` `tid`, `uint32_t` `*``current_stack_usage_ptr`, `uint32_t` `*``stack_size_ptr`)**

## posal_bufpool

Header file for buffer pool functionality for small allocations.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`POSAL_BUFPOOL_INVALID_HANDLE`**

Typedefs

**`typedef` `enum` `posal_bufpool_align_t` `posal_bufpool_align_t`**

Enums

**`enum` `posal_bufpool_align_t`**

*Values:*

**`enumerator` `FOUR_BYTE_ALIGN`**

**`enumerator` `EIGHT_BYTE_ALIGN`**

Functions

**`uint32_t` `posal_bufpool_pool_create`(`uint16_t` `node_size`, `POSAL_HEAP_ID` `heap_id`, `uint32_t` `num_arrays`, `posal_bufpool_align_t` `alignment`, `uint16_t` `nodes_per_arr`)**

**`void` `*``posal_bufpool_get_node`(`uint32_t` `pool_handle`)**

**`void` `posal_bufpool_return_node`(`void` `*``node_ptr`)**

**`void` `posal_bufpool_pool_destroy`(`uint32_t` `pool_handle`)**

**`void` `posal_bufpool_pool_reset_to_base`(`uint32_t` `pool_handle`)**

**`void` `posal_bufpool_pool_free_unused_lists`(`uint32_t` `pool_handle`)**

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `posal_bufpool_is_address_in_bufpool`(`void` `*``ptr`, `uint32_t` `pool_handle`)**

**`uint32_t` `posal_bufpool_profile_all_mem_usage`()**

**`ar_result_t` `posal_bufpool_profile_mem_usage`(`uint32_t` `pool_handle`, `uint32_t` `*``bytes_used_ptr`, `uint32_t` `*``bytes_allocated_ptr`)**

## posal_condvar

This file contains the ConditionVariables utilities.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_err_fatal

Contains API to call force crash.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void` `posal_err_fatal`(`const` `char` `*``err_str`)**

## posal

This is the top-level include file for the posal utilities. This file includes all header files required for using posal functions. The user of posal should only include this file to call the posal functions.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`void` `posal_init`(`void`)**

**`void` `posal_deinit`(`void`)**

**`static` `inline` `uint32_t` `posal_cmn_divide`(`uint32_t` `num`, `uint32_t` `den`)**

## posal_inline_mutex

Typedefs

**`typedef` `qurt_mutex_t` `posal_inline_mutex_t`**

Functions

**`static` `inline` `ar_result_t` `posal_inline_mutex_init`(`posal_inline_mutex_t` `*``pposal_mutex`)**

Initializes a mutex. Recursive mutexes are always used.

**Associated data types**posal_mutex_t  ****Nonzero — Failure  **Dependencies**None.

**Parameters:**

**posal_mutex** – **[in]** pointer to the mutex object handle.

**Returns:**

0 — Success

**`static` `inline` `void` `posal_inline_mutex_deinit`(`posal_inline_mutex_t` `*``pposal_mutex`)**

Deinits a mutex. This function must be called for each corresponding posal_mutex_init() function to clean up all resources.

**Associated data types**posal_mutex_t  **Dependencies**The object must have been created and initialized before calling this function.

**Parameters:**

**pposal_mutex** – **[in]** Pointer to the mutex to destroy.

**Returns:**

None.

## posal_interrupt

This file contains utilities for registering with interrupts.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_memory

This file contains utilities for memory allocation and release. This file provides memory allocation functions and macros for both C and C++.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_mem_prof

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef` `struct` `posal_mem_prof_marker_t` `posal_mem_prof_marker_t`**

Structure to mark memory for tracking profiling (appended at the end of the momory) Hash node structure to hold heap-id to memory count mapping

**`typedef` `struct` `posal_mem_prof_node_t` `posal_mem_prof_node_t`**

Enum to indicate whether memory profiling started or not

**`typedef` `enum` `posal_mem_prof_state_t` `posal_mem_prof_state_t`**

Posal memory profiling main structure

**`typedef` `struct` `posal_mem_prof_t` `posal_mem_prof_t`**

Enums

**`enum` `posal_mem_prof_state_t`**

*Values:*

**`enumerator` `POSAL_MEM_PROF_STOPPED`**

**`enumerator` `POSAL_MEM_PROF_STARTED`**

Functions

**`ar_result_t` `posal_mem_prof_init`(`POSAL_HEAP_ID` `heap_id`)**

Initializes posal memory profiler, creates mutex.

**Dependencies**None

**Parameters:**

**heapId** – **[in]** ID of the heap from which to allocate memory.

**Returns:**

Result.

**`ar_result_t` `posal_mem_prof_start`()**

Starts posal memory profiling, creates hashtable needed to store the heapid to mem count mapping.

**Dependencies**None

**Parameters:**

**None** –

**Returns:**

Result.

**`ar_result_t` `posal_mem_prof_stop`()**

Stops posal memory profiling, destroys hashtable needed to store the heapid to memory count mapping.

**Dependencies**None

**Parameters:**

**None** –

**Returns:**

Result.

**`void` `posal_mem_prof_deinit`()**

Deinits posal memory profiling, destroys profiling mutex.

**Dependencies**None

**Parameters:**

**None** –

**Returns:**

Result.

**`void` `posal_mem_prof_pre_process_malloc`(`POSAL_HEAP_ID` `orig_heap_id`, `POSAL_HEAP_ID` `*``heap_id_ptr`, `uint32_t` `*``bytes_ptr`)**

Extracts heap id from original heap id, updates bytes required.

**Dependencies**None

**Parameters:**

- **orig_heap_id** – **[in]** Heap id sent by the client.
- **heap_id_ptr** – **[in]** Pointer to heap id which stores extracted from orig_heap_id.
- **heap_id_ptr** – **[in]** Pointer to bytes to be allocated, if profiling has started, this will be + sizeof(uint64_t)

**Returns:**

None.

**`void` `posal_mem_prof_post_process_malloc`(`void` `*``ptr`, `POSAL_HEAP_ID` `orig_heap_id`, [`bool_t`](args_arosal.html#_CPPv46bool_t) `is_mem_tracked`)**

Updates heap id and magic number at the tail of the allocation, updates statistics if profiling is enabled.

**Dependencies**None

**Parameters:**

- **ptr** – **[in]** Pointer to the newly allocated memory.
- **orig_heap_id** – **[in]** Heap id sent by the client.
- **is_mem_tracked** – **[in]** Boolean to indicate of memory was tracked while allocation.

**Returns:**

None.

**`void` `posal_mem_prof_process_free`(`void` `*``ptr`)**

Extracts heapid and mem size from the ptr, updates statistics.

**Dependencies**None

**Parameters:**

**ptr** – **[in]** Pointer to the newly allocated memory.

**Returns:**

None.

**`void` `posal_mem_prof_query`(`POSAL_HEAP_ID` `heap_id`, `uint32_t` `*``mem_usage_ptr`)**

Updates the mem usage query asked by a client if the statistics exists.

**Dependencies**None

**Parameters:**

- **heap_id** – **[in]** Heap id of the query.
- **mem_usage_ptr** – **[in]** Pointer to which query update needs to be done.

**Returns:**

None.

**`uint32_t` `posal_mem_prof_get_mem_size`(`void` `*``ptr`, `POSAL_HEAP_ID` `heap_id`)**

Use to get the memory size from a pointer.

**Dependencies**None

**Parameters:**

- **ptr** – **[in]** Pointer of the allocated memory.
- **heap_id** – **[in]** Heap id of the query.

**Returns:**

Block size of the memory

**`struct` `posal_mem_prof_marker_t`**

*#include <posal_mem_prof.h>*Structure to mark memory for tracking profiling (appended at the end of the momory)

Public Members

**`POSAL_HEAP_ID` `heap_id`**

Heap ID of the memory allocated

**`uint32_t` `magic_number`**

Magic number to verify mem tracking

**`struct` `posal_mem_prof_node_t`**

*#include <posal_mem_prof.h>*Public Members

**`spf_hash_node_t` `hash_node`**

Hash node

**`POSAL_HEAP_ID` `heap_id`**

Key - heap id is used as a key to hashnode

**`uint32_t` `mem_count`**

Value - Count of memory allocations in Bytes

**`struct` `posal_mem_prof_t`**

*#include <posal_mem_prof.h>*Public Members

**`spf_hashtable_t` `mem_ht`**

Hash table to hold heap id to memory count mapping

**`POSAL_HEAP_ID` `heap_id`**

Heap id to be used by posal memory profiler

**`posal_mutex_t` `prof_mutex`**

Mutex to be used by posal memory profiler

**`posal_mem_prof_state_t` `mem_prof_status`**

Flag to indicate whether profiling started or not

## posal_nmutex

This file contains normal mutex utilities.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

## posal_queue

This file contains the queue utilities. Queues must be created and added to a channel before they can be used. Queues are pushed from the back and can be popped from either front(FIFO) or back(LIFO). Queues must be destroyed when they are no longer needed.

**Copyright**Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

Functions

**`uint32_t` `posal_queue_get_queue_fullness`(`posal_queue_t` `*``q_ptr`)**

function to get the fullness of queue

It returns the current number of element in the queue

**`struct` `posal_queue_init_attr_t`**

*#include <posal_queue.h>*Structure containing the attributes to be associated with type posal_queue_t

Public Members

**[`char_t`](args_arosal.html#_CPPv46char_t) `name``[``POSAL_DEFAULT_NAME_LEN``]`**

Name of the queue.

**`int32_t` `max_nodes`**

Max number of queue nodes.

**`int32_t` `prealloc_nodes`**

Number of preallocated nodes

**`POSAL_HEAP_ID` `heap_id`**

Heap ID from which nodes are to be allocated.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_priority_queue`**

FALSE: default FIFO queue, TRUE: Priority queue.

## posal_rtld

This file contains the Run-Time Linking (rtld) utilities.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`POSAL_RTLD_LAZY`**

**`POSAL_RTLD_NOW`**

**`RTLD_DI_LOAD_ADDR`**

ideally dlfcn.h must define these macros. but in some targets they are not defined. this is a work-around.

**`RTLD_DI_LOAD_SIZE`**

Functions

**`void` `*``posal_dlopen`(`const` `char` `*``name`, `int` `flags`)**

Opens the specified dynamic lib

**Associated data types**const char*, int  **Dependencies**None.

**Parameters:**

- **name** – **[in]** Name of the file to be opened
- **flags** – **[in]** Flags for to indicate how the file should be opened. Possible values are POSAL_RTLD_LAZY and POSAL_RTLD_NOW

**Returns:**

Returns a pointer to the opened dynamic library, or 0 on failure

**`void` `*``posal_dlopenbuf`(`const` `char` `*``name`, `const` `char` `*``buf`, `int` `len`, `int` `flags`)**

Opens the specified dynamic lib located in the given buffer

**Associated data types**const char*, const char*, int  **Dependencies**None.

**Parameters:**

- **name** – **[in]** Name of the file to be opened
- **buf** – **[in]** Buffer of the dynamic library
- **flags** – **[in]** Flags for to indicate how the file should be opened. Possible values are POSAL_RTLD_LAZY and POSAL_RTLD_NOW

**Returns:**

Returns a pointer to the opened dynamic library, or 0 on failure

**`int` `posal_dlclose`(`void` `*``handle`)**

Closes the specified dynamic lib

**Associated data types**void *  **Dependencies**None.

**Parameters:**

**handle** – **[in]** The handle of the dl to be closed

**Returns:**

0 — Success

**`void` `*``posal_dlsym`(`void` `*``handle`, `const` `char` `*``name`)**

Gets the pointer to the symbol within the dnamic lib

**Associated data types**void *, const char *  **Dependencies**None.

**Parameters:**

- **handle** – **[in]** The handle of the dl with the symbol needed
- **name** – **[in]** The name of the symbol

**Returns:**

Returns a pointer to the requested symbol, or 0 on failure

**`char` `*``posal_dlerror`(`void`)**

Gives the string of the error if there is a problem in one of the dl functions

**Dependencies**None.

**Returns:**

Returns a pointer to error string

**`int` `posal_dlinfo`(`void` `*``handle`, `int` `request`, `void` `*``p`)**

Gets info about the dynamic lib based on the request

**Associated data types**void *, int, void *  **Dependencies**None.

**Parameters:**

- **handle** – **[in]** The handle of the dl in question
- **request** – **[in]** The value of the request
- **p** – **[out]** The output of the request

**Returns:**

0 — Success

## posal_std

This file contains standard C functions.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`AR_STD_MIN`(`a`, `b`)**

**`AR_STD_MAX`(`a`, `b`)**

Functions

**`uint32_t` `posal_strlcpy`([`char_t`](args_arosal.html#_CPPv46char_t) `*``dest_ptr`, `const` [`char_t`](args_arosal.html#_CPPv46char_t) `*``src_ptr`, `uint32_t` `dest_len`)**

Copies the string from source pointer to a destination pointer.

**Dependencies**None.

**Parameters:**

- **dest_ptr** – **[in]** Pointer to the destination string.
- **src_ptr** – **[in]** Pointer to the source string.
- **dest_len** – **[in]** Length of the destination buffer.

**Returns:**

src_len — Source string size.

**`uint32_t` `posal_strnlen`(`const` [`char_t`](args_arosal.html#_CPPv46char_t) `*``src_ptr`, `uint32_t` `size`)**

Determines the length of a string with a fixed maximum size.

**Dependencies**None.

**Parameters:**

- **src_ptr** – **[in]** Pointer to the destination string.
- **size** – **[in]** Pointer to the source string.

**Returns:**

string length.

**`int32_t` `posal_strncmp`(`const` `char` `*``s1`, `uint32_t` `s1_size`, `const` `char` `*``s2`, `uint32_t` `s2_size`)**

Compares two strings, character wise bounded by length of the strings.

**Dependencies**None.

**Parameters:**

- **s1** – **[in]** Pointer to the destination string.
- **s1_size** – **[in]** Pointer to the source string.
- **s2** – **[in]** Length of the destination buffer.
- **s2_size** – **[in]** Pointer to the destination string.

**Returns:**

<0 - if the first character that doesnt match has lower ASCII value in s1 than in s2 0 - if two strings are same >0 - if the first character that doesnt match has greater ASCII value in s1 than in s2

**`void` `*``posal_memcpy`(`void` `*``dst`, `uint32_t` `dst_size`, `const` `void` `*``src`, `uint32_t` `src_size`)**

Copies src_size bytes from source pointer to the destination pointer. The number of bytes actually copied is bounded by dst_size, this avoids destination memory corruption if dst_size is less than src_size.

**Dependencies**None.

**Parameters:**

- **dst** – **[in]** - destination pointer.
- **dst_size** – **[in]** - size of destination pointer in bytes.
- **src** – **[in]** - source pointer
- **src_size** – **[in]** - number of bytes to be copied from the source pointer.

**Returns:**

returns copy of destination pointer.

**`void` `*``posal_memset`(`void` `*``dst`, `int32_t` `c`, `uint32_t` `num_bytes`)**

Sets the first size bytes of the memory pointed by dst to the value ‘c’ [interpreted as unsigned char].

**Dependencies**None.

**Parameters:**

- **dst** – **[in]** - destination pointer
- **c** – **[in]** - Value to be set. Pass as int32 but interpreted as unsigned char.
- **num_bytes** – **[in]** - number of bytes to be set to value ‘c’

**Returns:**

returns a copy of the input pointer.

**`int32_t` `posal_snprintf`([`char_t`](args_arosal.html#_CPPv46char_t) `*``dst`, `uint32_t` `size`, `const` [`char_t`](args_arosal.html#_CPPv46char_t) `*``format`, `...`)**

Prints formated string in the destination pointer, the maximum number of characters printed is bounded by the size.

**Dependencies**None.

**Parameters:**

- **dst** – **[in]** - destination pointer where the string is printed.
- **size** – **[in]** - maximum number of characters that could be printed.
- **format** – **[in]** - pointer to the format string.

**Returns:**

Number of character that have been actually printed.

## posal_thread_prio

This file contains the structures and function declarations that will be exposed to the framework to be invoked in order to retrieve the thread priority.

**Copyright**Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef` `enum` `spf_thread_prio_id_t` `spf_thread_prio_id_t`**

**`typedef` `struct` `prio_query_t` `prio_query_t`**

prio_query_t struct holds a (static_req_id, thread priority, frame duration) indicating the correct thread priority for a given frame duration (measured in microseconds) OR a req ID (indicates static/dynamic).

Enums

**`enum` `spf_thread_prio_id_t`**

*Values:*

**`enumerator` `SPF_THREAD_DYN_ID`**

**`enumerator` `SPF_THREAD_STAT_APM_ID`**

**`enumerator` `SPF_THREAD_STAT_CNTR_ID`**

**`enumerator` `SPF_THREAD_STAT_AMDB_ID`**

**`enumerator` `SPF_THREAD_STAT_IST_ID`**

**`enumerator` `SPF_THREAD_STAT_PRM_ID`**

**`enumerator` `SPF_THREAD_STAT_PM_SERVER_ID`**

**`enumerator` `SPF_THREAD_STAT_VOICE_TIMER_ID`**

**`enumerator` `SPF_THREAD_STAT_VCPM_ID`**

**`enumerator` `SPF_THREAD_STAT_ASPS_ID`**

**`enumerator` `SPF_THREAD_STAT_DLS_ID`**

**`enumerator` `SPF_THREAD_STAT_ID_MAX`**

Functions

**`ar_result_t` `posal_thread_calc_prio`(`prio_query_t` `*``prio_query_ptr`, `posal_thread_prio_t` `*``thread_prio_ptr`)**

**`ar_result_t` `posal_thread_determine_attributes`(`prio_query_t` `*``prio_query_ptr`, `posal_thread_prio_t` `*``thread_prio_ptr`, `uint32_t` `*``sched_policy_ptr`, `uint32_t` `*``cpu_set_ptr`)**

**`posal_thread_prio_t` `posal_thread_get_floor_prio`(`spf_thread_prio_id_t` `prio_id`)**

Gets a default low priority for the passed in prio_id. Currently only implemented for SPF_THREAD_STAT_CNTR_ID.

**`struct` `prio_query_t`**

*#include <posal_thread_prio.h>*prio_query_t struct holds a (static_req_id, thread priority, frame duration) indicating the correct thread priority for a given frame duration (measured in microseconds) OR a req ID (indicates static/dynamic).

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_interrupt_trig`**

**`spf_thread_prio_id_t` `static_req_id`**

**`uint32_t` `frame_duration_us`**
