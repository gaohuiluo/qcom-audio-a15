# 通用包路由器（GPR）API

## 公共 API

本文件包含 GPR API。

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

宏定义（Defines）

**`GPR_HEAP_INDEX_DEFAULT`**

**`GPR_HEAP_INDEX_1`**

类型定义（Typedefs）

**`typedef uint8_t gpr_heap_index_t`**

**`typedef uint32_t (*gpr_callback_fn_t)(gpr_packet_t *packet, void *callback_data)`**

包回调函数的原型。

**关联数据类型**#gpr_packet_t

否则返回错误（参见）—— 包的所有权归还给调用者。

**参数 packet：**

**[in]** 指向传入包的指针。该包保证具有非 NULL 值。

**参数 callback_data：**

**[in]** 服务在注册时提供的、由客户端提供的数据指针。

**返回：**

[AR_EOK](args_arosal.md) —— 成功时，表示被调用方已取得该包的所有权。

**`typedef struct gpr_packet_pool_info_v2_t gpr_packet_pool_info_v2_t`**

**`typedef struct gpr_cmd_gpr_packet_pool_info_t gpr_cmd_gpr_packet_pool_info_t`**

**`typedef struct gpr_cmd_alloc_ext_v2_t gpr_cmd_alloc_ext_v2_t`**

**`struct gpr_packet_pool_info_v2_t`**

*#include <gpr_api.h>*公共成员

**`gpr_heap_index_t heap_index`**

**`uint8_t is_dynamic`**

**`uint16_t reserved`**

**`uint32_t num_packets`**

**`uint32_t packet_size`**

**`struct gpr_cmd_gpr_packet_pool_info_t`**

*#include <gpr_api.h>*包含 __gpr_cmd_get_gpr_packet_info() 的包池信息。

公共成员

**`uint32_t bytes_per_min_size_packet`**

GPR 包的最小尺寸（以字节计）。

**`uint32_t num_min_size_packets`**

初始化时分配的最小尺寸包的数量。

**`uint32_t bytes_per_max_size_packet`**

GPR 包的最大尺寸（以字节计）。

**`uint32_t num_max_size_packets`**

初始化时分配的最大尺寸包的数量。

**`struct gpr_cmd_alloc_ext_t`**

*#include <gpr_api.h>*包含 __gpr_cmd_alloc_ext() 的已分配包信息。

公共成员

**`uint8_t src_domain_id`**

发送方服务的域 ID。

**`uint32_t src_port`**

发送方服务的已注册唯一 ID。

**`uint8_t dst_domain_id`**

接收方服务的域 ID。

**`uint32_t dst_port`**

接收方服务的已注册唯一 ID。

**`uint8_t client_data`**

保留供客户端使用。

**`uint32_t token`**

由发送方附加的值，用于在收到响应消息后确定接收方何时处理命令消息。

**`uint32_t opcode`**

向接收方定义动作和负载结构两者。

**`uint32_t payload_size`**

负载实际所需的字节数。

**`gpr_packet_t **ret_packet`**

指向该函数返回的已格式化包的双重指针。

**`struct gpr_cmd_alloc_ext_v2_t`**

*#include <gpr_api.h>*包含 __gpr_cmd_alloc_ext_v2() 的已分配包信息。

公共成员

**`uint8_t src_domain_id`**

发送方服务的域 ID。

**`uint32_t src_port`**

发送方服务的已注册唯一 ID。

**`uint8_t dst_domain_id`**

接收方服务的域 ID。

**`uint32_t dst_port`**

接收方服务的已注册唯一 ID。

**`uint8_t client_data`**

保留供客户端使用。

**`uint32_t token`**

由发送方附加的值，用于在收到响应消息后确定接收方何时处理命令消息。

**`gpr_heap_index_t heap_index`**

包池的堆索引。‘0’ 为默认值。若不适用，必须设为 0。

**`uint32_t opcode`**

向接收方定义动作和负载结构两者。

**`uint32_t payload_size`**

负载实际所需的字节数。

**`gpr_packet_t **ret_packet`**

指向该函数返回的已格式化包的双重指针。

**`struct gpr_cmd_alloc_send_t`**

*#include <gpr_api.h>*包含 __gpr_cmd_alloc_send() 的已分配包信息。

公共成员

**`uint8_t src_domain_id`**

发送方服务的域 ID。

**`uint32_t src_port`**

发送方服务的已注册唯一 ID。

**`uint8_t dst_domain_id`**

接收方服务的域 ID。

**`uint32_t dst_port`**

接收方服务的已注册唯一 ID。

**`uint8_t client_data`**

保留供客户端使用。

**`uint32_t token`**

由发送方附加的值，用于在收到响应消息后确定接收方何时处理命令消息。

**`uint32_t opcode`**

操作码，向接收方定义动作和负载结构两者。

**`uint32_t payload_size`**

负载实际所需的字节数。

**`void *payload`**

指向要发送的负载的指针。

## 数据链路 API

本文件包含 IPC API。

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

类型定义（Typedefs）

**`typedef struct gpr_to_ipc_vtbl_t gpr_to_ipc_vtbl_t`**

**`typedef struct ipc_to_gpr_vtbl_t ipc_to_gpr_vtbl_t`**

**`struct gpr_to_ipc_vtbl_t`**

*#include <ipc_dl_api.h>*由 GPR 向 IPC 数据链路层暴露的回调函数表。GPR 在数据链路层初始化期间将此表发送给数据链路层。

公共成员

**`uint32_t (*receive)(void *buf, uint32_t length)`**

GPR 的 receive() 回调函数原型。

**详细描述** 当数据链路层收到一个包时，它调用此 GPR 函数来处理该包并将其路由到最终目的地。

**依赖** 无。

**参数 buf：**

**[in]** 指向包的指针。

**参数 length：**

**[in]** 包的大小。

**返回：**

[AR_EOK](args_arosal.md) —— 成功时返回。

**`uint32_t (*send_done)(void *buf, uint32_t length)`**

GPR 的 send_done() 回调函数原型。

**详细描述** 当数据链路层完成一个包的发送时，它使用此函数向 GPR 发出信号以释放该包。

**依赖** 无。

**参数 buf：**

**[in]** 指向包的指针。

**参数 length：**

**[in]** 包的大小。

**返回：**

[AR_EOK](args_arosal.md) —— 成功时返回。

**`struct ipc_to_gpr_vtbl_t`**

*#include <ipc_dl_api.h>*由数据链路层向 GPR 暴露的函数表。这些函数必须由每个数据链路层在 gpr_init() 调用数据链路层初始化时填充。

公共成员

**`uint32_t (*send)(uint32_t domain_id, void *buf, uint32_t length)`**

数据链路层的 send() 函数原型。

**详细描述** 当 GPR 向目的域发送一个包时，它调用对应数据链路层的此函数。

**依赖** 无。

**参数 domain_id：**

**[in]** 包被发往的目的域的 ID。

**参数 buf：**

**[in]** 指向包的指针。

**参数 length：**

**[in]** 包的大小。

**返回：**

[AR_EOK](args_arosal.md) —— 成功时返回。

**`uint32_t (*receive_done)(uint32_t domain_id, void *buf)`**

数据链路层的 receive_done() 函数原型。

**详细描述** 当 GPR 完成处理从数据链路层接收的包时，它将该包返还给数据链路层，由其释放缓冲区。

**依赖** 无。

**参数 domain_id：**

**[in]** 包被发出的源域的 ID。

**参数 buf：**

**[in]** 指向包的指针。

**返回：**

[AR_EOK](args_arosal.md) —— 成功时返回。
