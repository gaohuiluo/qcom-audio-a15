# Generic Packet Router (GPR) APIs

## Public APIs

This file contains GPR APIs.

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`GPR_HEAP_INDEX_DEFAULT`**

**`GPR_HEAP_INDEX_1`**

Typedefs

**`typedef uint8_t gpr_heap_index_t`**

**`typedef uint32_t (*gpr_callback_fn_t)(gpr_packet_t *packet, void *callback_data)`**

Prototype of a packet callback function.

**Associated data types**#gpr_packet_t

Otherwise, an error (see ) — The packet ownership is returned to the caller.

**Param packet:**

**[in]** Pointer to the incoming packet. The packet is guaranteed to have a non-NULL value.

**Param callback_data:**

**[in]** Client-supplied data pointer that the service provided at registration time.

**Return:**

[AR_EOK](args_arosal.html#ar__osal__error_8h_1a0a092831d3ed0214cc9770c6fd3fdc8e) — When successful, indicates that the callee has taken ownership of the packet.

**`typedef struct gpr_packet_pool_info_v2_t gpr_packet_pool_info_v2_t`**

**`typedef struct gpr_cmd_gpr_packet_pool_info_t gpr_cmd_gpr_packet_pool_info_t`**

**`typedef struct gpr_cmd_alloc_ext_v2_t gpr_cmd_alloc_ext_v2_t`**

**`struct gpr_packet_pool_info_v2_t`**

*#include <gpr_api.h>*Public Members

**`gpr_heap_index_t heap_index`**

**`uint8_t is_dynamic`**

**`uint16_t reserved`**

**`uint32_t num_packets`**

**`uint32_t packet_size`**

**`struct gpr_cmd_gpr_packet_pool_info_t`**

*#include <gpr_api.h>*Contains the packet pool information for __gpr_cmd_get_gpr_packet_info().

Public Members

**`uint32_t bytes_per_min_size_packet`**

Minimum size (in bytes) of a GPR packet.

**`uint32_t num_min_size_packets`**

Number of packets of the minimum size allocated at initialization.

**`uint32_t bytes_per_max_size_packet`**

Maximum size (in bytes) of a GPR packet.

**`uint32_t num_max_size_packets`**

Number of packets of the maximum size allocated at initialization.

**`struct gpr_cmd_alloc_ext_t`**

*#include <gpr_api.h>*Contains the allocated packet information for __gpr_cmd_alloc_ext().

Public Members

**`uint8_t src_domain_id`**

Domain ID of the sender service.

**`uint32_t src_port`**

Registered unique ID of the sender service.

**`uint8_t dst_domain_id`**

Domain ID of the receiver service.

**`uint32_t dst_port`**

Registered unique ID of the receiver service.

**`uint8_t client_data`**

Reserved for use by client.

**`uint32_t token`**

Value attached by the sender to determine when command messages are processed by the receiver after they receive response messages.

**`uint32_t opcode`**

Defines both the action and the payload structure to the receiver.

**`uint32_t payload_size`**

Actual number of bytes required for the payload.

**`gpr_packet_t **ret_packet`**

Double pointer to the formatted packet returned by the function.

**`struct gpr_cmd_alloc_ext_v2_t`**

*#include <gpr_api.h>*Contains the allocated packet information for __gpr_cmd_alloc_ext_v2().

Public Members

**`uint8_t src_domain_id`**

Domain ID of the sender service.

**`uint32_t src_port`**

Registered unique ID of the sender service.

**`uint8_t dst_domain_id`**

Domain ID of the receiver service.

**`uint32_t dst_port`**

Registered unique ID of the receiver service.

**`uint8_t client_data`**

Reserved for use by client.

**`uint32_t token`**

Value attached by the sender to determine when command messages are processed by the receiver after they receive response messages.

**`gpr_heap_index_t heap_index`**

heap index of the packet pool. ‘0’ is default value. Must be set to 0 if not applicable.

**`uint32_t opcode`**

Defines both the action and the payload structure to the receiver.

**`uint32_t payload_size`**

Actual number of bytes required for the payload.

**`gpr_packet_t **ret_packet`**

Double pointer to the formatted packet returned by the function.

**`struct gpr_cmd_alloc_send_t`**

*#include <gpr_api.h>*Contains the allocated packet information for __gpr_cmd_alloc_send().

Public Members

**`uint8_t src_domain_id`**

Domain ID of the sender service.

**`uint32_t src_port`**

Registered unique ID of the sender service.

**`uint8_t dst_domain_id`**

Domain ID of the receiver service.

**`uint32_t dst_port`**

Registered unique ID of the receiver service.

**`uint8_t client_data`**

Reserved for use by the client.

**`uint32_t token`**

Value attached by the sender to determine when command messages have been processed by the receiver after having received response messages.

**`uint32_t opcode`**

Operation code defines both the action and the payload structure to the receiver.

**`uint32_t payload_size`**

Actual number of bytes needed for the payload.

**`void *payload`**

Pointer to the payload to send.

## Datalink APIs

This file contains IPC APIs.

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Typedefs

**`typedef struct gpr_to_ipc_vtbl_t gpr_to_ipc_vtbl_t`**

**`typedef struct ipc_to_gpr_vtbl_t ipc_to_gpr_vtbl_t`**

**`struct gpr_to_ipc_vtbl_t`**

*#include <ipc_dl_api.h>*Table of callback functions exposed by the GPR to the IPC data link layers. The GPR sends this table to the data link layers during data link layer initialization.

Public Members

**`uint32_t (*receive)(void *buf, uint32_t length)`**

Prototype of the receive() callback function for the GPR.

**Detailed description** When the data link layer receives a packet, it calls this GPR function to handle and route the packet to its final destination.

**Dependencies** None.

**Param buf:**

**[in]** Pointer to the packet.

**Param length:**

**[in]** Size of the packet.

**Return:**

[AR_EOK](args_arosal.html#ar__osal__error_8h_1a0a092831d3ed0214cc9770c6fd3fdc8e) — When successful.

**`uint32_t (*send_done)(void *buf, uint32_t length)`**

Prototype of the send_done() callback function for the GPR.

**Detailed description** When the data link layer finishes sending a packet, it uses this function to signal the GPR to free the packet.

**Dependencies** None.

**Param buf:**

**[in]** Pointer to the packet.

**Param length:**

**[in]** Size of the packet.

**Return:**

[AR_EOK](args_arosal.html#ar__osal__error_8h_1a0a092831d3ed0214cc9770c6fd3fdc8e) — When successful.

**`struct ipc_to_gpr_vtbl_t`**

*#include <ipc_dl_api.h>*Table of functions exposed by data link layers to the GPR. The functions must be populated by every data link layer when gpr_init() calls for data link layer initialization.

Public Members

**`uint32_t (*send)(uint32_t domain_id, void *buf, uint32_t length)`**

Prototype of the send() function for a data link layer.

**Detailed description** When the GPR sends a packet to a destination domain, it calls this function of the corresponding data link layer.

**Dependencies** None.

**Param domain_id:**

**[in]** ID of the domain to which packet is being sent.

**Param buf:**

**[in]** Pointer to the packet.

**Param length:**

**[in]** Size of the packet.

**Return:**

[AR_EOK](args_arosal.html#ar__osal__error_8h_1a0a092831d3ed0214cc9770c6fd3fdc8e) — When successful.

**`uint32_t (*receive_done)(uint32_t domain_id, void *buf)`**

Prototype of the receive_done() function for a data link layer.

**Detailed description** When the GPR finishes processing a packet it received from the data link layer, it returns the packet to the data link layer for it to free the buffer.

**Dependencies** None.

**Param domain_id:**

**[in]** ID of the domain from which packet was sent.

**Param buf:**

**[in]** Pointer to the packet.

**Return:**

[AR_EOK](args_arosal.html#ar__osal__error_8h_1a0a092831d3ed0214cc9770c6fd3fdc8e) — When successful.
