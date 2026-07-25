# 图服务层（Graph Service Layer）

定义图服务层（GSL）的公共 API

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

宏定义（Defines）

**`GSL_MAX_NUM_OF_ACDB_FILES`**

acdb 文件的最大数量

**`GSL_MAX_LEN_OF_ACDB_FILENAME`**

文件名的最大长度

**`GSL_ATTRIBUTES_DATA_MODE_MASK`**

保留 3 个比特用于指定数据模式

**`GSL_DATA_MODE_SHMEM`**

共享内存模式

**`GSL_DATA_MODE_BLOCKING`**

堆内存模式，阻塞

**`GSL_DATA_MODE_NON_BLOCKING`**

堆内存模式，非阻塞

**`GSL_DATA_MODE_PUSH_PULL`**

推挽（push-pull）模式

**`GSL_DATA_MODE_EXTERN_MEM`**

外部内存模式，用 2 个比特控制数据通路的建立

**`GSL_ATTRIBUTES_DATAPATH_SETUP_MASK`**

数据通路建立标志的移位量

**`GSL_ATTRIBUTES_DATAPATH_SETUP_SHIFT`**

当需要把内存缓冲区的分配与将这些缓冲区共享给 DSP 这两件事分开时，使用这些标志。例如：以无 GKV 且推挽模式打开图时，该用例的端点 IID 尚不可知，因此无法把 shmem 发送给 DSP。

默认情况下会把缓冲区分配与共享内存建立一起完成；必须先分配缓冲区才能建立 shmem。客户端负责按正确顺序调用它们，即必须先分配 shmem 才能向 SPF 供给。分配缓冲区并在 SPF EP 上完成建立。

**`GSL_DATAPATH_SETUP_DEFAULT`**

分配缓冲区，但不在 SPF 端点上建立 shmem

**`GSL_DATAPATH_SETUP_ALLOC_SHMEM_ONLY`**

仅在 SPF 端点上建立 shmem。使用此标志时 GSL 会忽略发送的其他参数，因为在用此标志调用之前，数据通路必须已经用 ALLOC_SHMEM_ONLY 配置过。

对于基于数据包（packet-based）的模式，此操作为空操作（no-op）

**`GSL_DATAPATH_SETUP_SPF_PROVISION_ONLY`**

用于指示某个给定缓冲区是最后一个缓冲区，缓冲区被渲染后客户端将收到通知

**`GSL_BUFF_FLAG_EOS`**

若缓冲区带有有效时间戳则为 true

**`GSL_BUFF_FLAG_TS_VALID`**

用于指示某个缓冲区是一帧中的最后一个

**`GSL_BUFF_FLAG_EOF`**

用于指示某个缓冲区是媒体格式；当此标志被置位时，缓冲区将仅包含媒体格式数据

**`GSL_BUFF_FLAG_MEDIA_FORMAT`**

**`GSL_EVENT_SRC_MODULE_ID_GSL`**

用于标识事件源自 GSL 而非 Spf 的 module_id

Typedefs

**`typedef` `void` `*``gsl_handle_t`**

返回给客户端的不透明句柄

**`typedef` `void` `*``gsl_acdb_handle_t`**

返回给客户端的不透明 acdb 句柄

**`typedef` `uint32_t` `(``*``gsl_global_cb_func_ptr``)``(``enum` `gsl_global_event_ids` `event_id``,` `void` `*``event_payload``,` `size_t` `event_payload_sz``,` `void` `*``client_data``)`**

用于向客户端通知全局事件的回调。

全局事件是指不绑定到某个特定 gsl 图句柄的事件。

**Param event_id:**

**[in]** 指示全局事件 id

**Param event_payload:**

**[in]** 特定于该事件 id 的负载

**Param event_payload_sz:**

**[in]** 特定于该事件 id 的负载的大小

**Param client_data:**

**[in]** 不透明的客户端数据

**`typedef` `void` `(``*``gsl_cb_func_ptr``)``(``struct` `gsl_event_cb_params` `*``event_params``,` `void` `*``client_data``)`**

向客户端通知事件的回调函数签名。

**Param event_params:**

**[in]** 保存所有与事件相关的信息

**Param client_data:**

**[in]** 在注册回调时提供的客户端数据

**`typedef` `uint32_t` `gsl_mem_id_t`**

**`typedef` `enum` `gsl_cshm_cache_type` `gsl_cshm_cache_type_t`**

**`typedef` `enum` `gsl_subsystem` `gsl_subsystem_t`**

**`typedef` `struct` `gsl_cshm_info` `gsl_cshm_info_t`**

枚举（Enums）

**`enum` `gsl_cmd_id`**

可传递给 gsl_ioctl 的命令

*取值：*

**`enumerator` `GSL_CMD_START`**

启动一个图

**`enumerator` `GSL_CMD_PREPARE`**

可选，可在 GSL_CMD_START 之前调用，以开始初始化 DSP 中的模块

**`enumerator` `GSL_CMD_FLUSH`**

刷新（flush）一个图，会使该图丢弃所有未处理的缓冲区

**`enumerator` `GSL_CMD_STOP`**

停止图，停止处理数据并复位到初始状态。可选负载：struct gsl_cmd_properties。GRAPH_STOP 仅下发给 property_ID 与 property_values 相匹配的那些子图

**`enumerator` `GSL_CMD_ADD_GRAPH`**

基于一个新的图键向量，向已有图中添加一个新图。负载：struct gsl_cmd_graph_select

**`enumerator` `GSL_CMD_REMOVE_GRAPH`**

基于一个图键向量移除已有的图。负载：struct gsl_cmd_remove_graph

**`enumerator` `GSL_CMD_CHANGE_GRAPH`**

基于一个新的图键向量修改已有的图。负载：struct gsl_cmd_graph_select

**`enumerator` `GSL_CMD_QUERY_GRAPH_DELAY`**

获取与某个图关联的通路延迟

**`enumerator` `GSL_CMD_CONFIGURE_WRITE_PARAMS`**

配置用于写数据交换的参数。负载：struct gsl_cmd_configure_read_write_params

**`enumerator` `GSL_CMD_CONFIGURE_READ_PARAMS`**

配置用于读数据交换的参数。负载：struct gsl_cmd_configure_read_write_params

**`enumerator` `GSL_CMD_EOS`**

在播放数据流中插入 EOS 标记，该 EOS 标记会在所有成功写入 GSL 的数据之后立即插入流中。当 EOS 标记之前的所有缓冲区都播放完毕后，GSL 会向客户端生成一个 EOS 事件。注意：如果在下发此命令时有一个 gsl_write 操作处于挂起状态，则挂起的 gsl_write 中传入的缓冲区不保证会被播放出来。

**`enumerator` `GSL_CMD_GET_WRITE_BUFF_INFO`**

获取用于共享内存模式写操作的缓冲区指针和大小。负载：struct gsl_cmd_get_shmem_buf_info 由客户端发送，并由 GSL 写入。

**`enumerator` `GSL_CMD_GET_READ_BUFF_INFO`**

获取用于共享内存模式读操作的缓冲区指针和大小。负载：struct gsl_cmd_get_shmem_buf_info 由客户端发送，并由 GSL 写入。

**`enumerator` `GSL_CMD_GET_WRITE_POS_BUFF_INFO`**

获取用于在推挽模式下同步写操作的位置缓冲区（position buffer）的指针和大小。负载：struct gsl_cmd_get_shmem_buf_info 由客户端发送，并由 GSL 写入。

**`enumerator` `GSL_CMD_GET_READ_POS_BUFF_INFO`**

获取用于在推挽模式下同步读操作的位置缓冲区（position buffer）的指针和大小。负载：struct gsl_cmd_get_shmem_buf_info 由客户端发送，并由 GSL 写入。

**`enumerator` `GSL_CMD_REGISTER_CUSTOM_EVENT`**

向某个 spf 模块注册一个自定义事件。负载：struct gsl_cmd_register_custom_event

**`enumerator` `GSL_CMD_FREE_READ_BUFF`**

释放某个图的所有读缓冲区

**`enumerator` `GSL_CMD_FREE_WRITE_BUFF`**

释放某个图的所有写缓冲区

**`enumerator` `GSL_CMD_SUSPEND`**

挂起图，停止处理数据，但不复位到初始状态。如果一个子图被多个图共享，则：只要至少有一个图处于 START，该公共子图就保持 START。如果没有任何图处于 START，而其中一个图处于 STOP，则该公共子图进入 STOP 状态。只有当所有图都下发 SUSPEND 时，该公共子图才会进入 SUSPEND 状态。

**`enumerator` `GSL_CMD_CLOSE_WITH_PROPS`**

基于属性关闭图中的子图子集。负载：struct gsl_cmd_properties。GRAPH_STOP 仅下发给 property_ID 与 property_values 相匹配的那些子图

**`enumerator` `GSL_CMD_MAX`**

**`enum` `gsl_event_id`**

将由 GSL 通知给客户端的事件

*取值：*

**`enumerator` `GSL_EVENT_ID_EOS`**

流结束（End of stream）事件，指示在客户端调用 GSL_CMD_EOS 之前写入 GSL 的所有数据都已播放完毕。负载：struct gsl_event_eos_payload

**`enumerator` `GSL_EVENT_ID_READ_DONE`**

指示作为 read 调用一部分提供的缓冲区已被填充。负载：struct gsl_event_read_write_done_payload

**`enumerator` `GSL_EVENT_ID_WRITE_DONE`**

指示作为 write 一部分提供的缓冲区已被消费。负载：struct gsl_event_read_write_done_payload

**`enumerator` `GSL_EVENT_ID_BUFFER_AVAIL`**

仅在非阻塞模式下发送，指示缓冲区已变为可供客户端写入

**`enumerator` `GSL_EVENT_ID_MAX`**

**`enum` `gsl_global_event_ids`**

可通过全局回调抛出的全局事件

*取值：*

**`enumerator` `GSL_GLOBAL_EVENT_AUDIO_SVC_UP`**

指示某个音频服务已启动，例如可能是由于 SSR 之后重启所致。负载：NULL

**`enumerator` `GSL_GLOBAL_EVENT_AUDIO_SVC_DN`**

指示某个音频服务已停止，例如可能是由于 SSR 所致。负载：struct gsl_global_event_svc_dn_payload

**`enumerator` `GSL_GLOBAL_EVENT_MAX`**

**`enum` `gsl_data_dir`**

标识数据方向

*取值：*

**`enumerator` `GSL_DATA_DIR_READ`**

指示数据由 gsl 提供给客户端

**`enumerator` `GSL_DATA_DIR_WRITE`**

指示数据由客户端提供给 gsl

**`enum` `gsl_eos_render_status_t`**

从 Spf 返回的 EOS 渲染状态

*取值：*

**`enumerator` `GSL_EOS_RENDERED`**

**`enumerator` `GSL_EOS_DROPPED`**

**`enum` `gsl_cshm_cache_type`**

*取值：*

**`enumerator` `GSL_CSHM_CACHED`**

0，带缓存（cached）。

**`enumerator` `GSL_CSHM_UNCACHED`**

1，不带缓存（uncached）。

**`enum` `gsl_subsystem`**

*取值：*

**`enumerator` `GSL_SS_INVALID`**

无效子系统。

**`enumerator` `GSL_SS_MODEM_DSP`**

用于 MODEM DSP 子系统。

**`enumerator` `GSL_SS_APPS`**

用于 APPS 子系统。

**`enumerator` `GSL_SS_SENSOR_DSP`**

用于 SENSOR DSP 子系统。

**`enumerator` `GSL_SS_COMPUTE_DSP`**

用于 COMPUTE DSP 子系统。

**`enumerator` `GSL_SS_CC_DSP`**

用于伴随芯片 DSP（Companion chip DSP，CC_DSP）子系统。

**`enumerator` `GSL_SS_ADSP`**

用于 ADSP 子系统。

函数（Functions）

**`void` `gsl_get_version`(`uint32_t` `*``major`, `uint32_t` `*``minor`)**

返回 GSL 版本。

**参数：**

- **major** – **[out]** 每当当前版本与旧版本不向后兼容时，主版本号递增
- **minor** – **[out]** 每当当前版本相较旧版本增加了特性但仍与其向后兼容时，次版本号递增

**`int32_t` `gsl_init`(`struct` `gsl_init_data` `*``init_data`)**

初始化 GSL，必须在任何其他 GSL 调用之前调用。

**参数：**

**init_data** – **[in]** 初始化期间使用的数据

**`int32_t` `gsl_cshm_init`(`uint32_t` `num_client`)**

初始化 GSL cshm，必须在任何其他 cshm 调用之前调用。

**参数：**

**num_client** – **[in]** 要初始化的客户端数量。若为 0，则使用默认值 CSHM_DEFAULT_INIT_CLIENT_NUM。

**`int32_t` `gsl_cshm_deinit`(`void`)**

反初始化 GSL cshm，必须在 gsl_deinit() 之后调用

**`void` `gsl_deinit`(`void`)**

反初始化 GSL，此后不应再调用任何 GSL API

**`int32_t` `gsl_register_global_event_cb`(`gsl_global_cb_func_ptr` `global_cb`, `void` `*``client_data`)**

为 GSL 注册一个全局回调函数。

**参数：**

- **global_cb** – **[in]** 用于通知诸如 SSR 之类全局事件的回调函数指针
- **client_data** – **[in]** 不透明的客户端数据，每当回调被调用时都会被回传给客户端

**`int32_t` `gsl_open`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `const` `struct` `gsl_key_vector` `*``cal_key_vect`, `gsl_handle_t` `*``graph_handle`)**

将用 graph_key_vector 指定的图加载到 DSP。不会重新加载已经加载过的图。

**参数：**

- **graph_key_vect** – **[in]** 用于标识该图。
- **cal_key_vect** – **[in]** 可选，用于标识要发送给该图的校准数据，设为 NULL 表示不发送任何校准
- **graph_handle** – **[out]** 成功时返回图句柄，否则为 null

**返回值：**

成功返回 GSL_EOK，否则返回错误码

**`int32_t` `gsl_close`(`gsl_handle_t` `graph_handle`)**

关闭用 graph_handle 指定的图。

**参数：**

**graph_handle** – **[in]** 要关闭的图的句柄

**返回值：**

成功返回 GSL_EOK，否则返回错误码

**`int32_t` `gsl_set_cal`(`gsl_handle_t` `graph_handle`, `const` `struct` `gsl_key_vector` `*``graph_key_vect`, `const` `struct` `gsl_key_vector` `*``cal_key_vect`)**

将某个给定图的校准数据推送到 DSP，必须在图启动之前调用。在 GSL_CMD_CHANGE_GRAPH 的情况下无需调用此 API，因为校准会在图变更操作自身过程中被设置。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **graph_key_vect** – **[in]** 可选，标识需要应用此校准的图的那一部分。对于 SSMD 场景，graph_handle 可能包含多个图键向量。此时，客户端可以提供需要设置此校准的具体图键向量。graph_key_vector 输入应与 graph_handle 所拥有的某个 GKV 相匹配。如果此参数为 NULL，则 GSL 将 prior_ckv 设置为 gsl_open() 期间所给定的那个。
- **cal_key_vect** – **[in]** 用于标识校准数据。

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_config`(`gsl_handle_t` `graph_handle`, `const` `struct` `gsl_key_vector` `*``graph_key_vect`, `uint32_t` `tag`, `const` `struct` `gsl_key_vector` `*``tag_key_vect`)**

在指定的图上设置一个配置负载，该负载存储在 acdb 中。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **graph_key_vect** – **[in]** 可选，标识需要应用此配置的图的那一部分。对于 SSMD 场景，graph_handle 可能包含多个图键向量。此时，客户端可以提供需要设置此校准的具体图键向量。graph_key_vector 输入应与 graph_handle 所拥有的某个 GKV 相匹配。
- **tag** – **[in]** 标识 acdb 中的一项能力
- **tag_key_vect** – **[in]** 标识数据库中的一个负载

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_custom_config`(`gsl_handle_t` `graph_handle`, `const` `uint8_t` `*``payload`, `const` `uint32_t` `payload_size`)**

在指定的图上设置一个自定义配置参数，负载由调用者提供。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **payload** – **[in]** 由调用者自定义、将被发送给模块的负载，负载结构必须始终符合 SPF 定义的 OOB 结构格式
- **payload_size** – **[in]** 负载缓冲区的大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_tagged_custom_config`(`gsl_handle_t` `graph_handle`, `uint32_t` `tag`, `const` `uint8_t` `*``payload`, `const` `size_t` `payload_size`)**

在指定的图上设置一个自定义配置参数，负载由调用者提供。调用者还提供 tag ID，以便 gsl 能在 ACDB 中查找该负载需要发送到的模块 IID。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **tag** – **[in]** 标识与该 tag ID 相匹配的模块实例
- **payload** – **[in]** 由调用者自定义、将被发送给模块的负载，负载结构必须始终符合 SPF 定义的格式 {MIID, PID, Size, Error Code, Variable payload}
- **payload_size** – **[in]** 负载缓冲区的大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_tagged_custom_config_persist`(`gsl_handle_t` `graph_handle`, `uint32_t` `tag`, `const` `uint8_t` `*``payload`, `const` `uint32_t` `payload_size`)**

以持久化方式在指定的图上设置一个自定义配置参数，负载由调用者提供。调用者还提供 tag ID，以便 gsl 能在 ACDB 中查找该负载需要发送到的模块 IID。限制：负载只能包含发往单个 MID 的单个 PID。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **tag** – **[in]** 标识与该 tag ID 相匹配的模块实例
- **payload** – **[in]** 由调用者自定义、将被发送给模块的负载，负载结构必须始终符合 SPF 定义的格式 {MIID, PID, Size, Error Code, Variable payload}
- **payload_size** – **[in]** 负载缓冲区的大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_get_custom_config`(`gsl_handle_t` `graph_handle`, `uint8_t` `*``payload`, `uint32_t` `size`)**

获取指定图的配置参数，由调用者提供负载。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回
- **payload** – **[inout]** 包含模块 id 和参数 id 的缓冲区，其中带有将被填入参数数据的空白区域
- **size** – **[inout]** 保存为 payload 传入的客户端缓冲区大小。返回时将保存实际写入的字节数。

**返回值：**

成功返回 EOK，否则返回错误码。注意 EOK 并不意味着我们获取到了有效数据，缓冲区有可能没有为某个给定参数预留足够空间。客户端在读取数据前应检查缓冲区内部的错误码。

**`int32_t` `gsl_get_tagged_custom_config`(`gsl_handle_t` `graph_handle`, `uint32_t` `tag`, `uint8_t` `*``payload`, `uint32_t` `*``size`)**

从由某个 tag 指定的模块获取指定图的配置参数，调用者提供已填入 PID 的负载。GSL 会把 MID 填入负载。限制：一次只能查找单个模块上的单个参数。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回
- **tag** – **[in]** GSL 用于查找 MID 的 tag
- **payload** – **[inout]** 包含参数 id 的缓冲区，其中带有将被填入参数数据的空白区域
- **size** – **[inout]** 保存为 payload 传入的客户端缓冲区大小。返回时将保存实际写入的字节数。

**返回值：**

成功返回 EOK，否则返回错误码。注意 EOK 并不意味着我们获取到了有效数据，缓冲区有可能没有为某个给定参数预留足够空间。客户端在读取数据前应检查缓冲区内部的错误码。

**`int32_t` `gsl_ioctl`(`gsl_handle_t` `graph_handle`, `enum` `gsl_cmd_id` `cmd_id`, `void` `*``cmd_payload`, `size_t` `cmd_payload_sz`)**

向 GSL 发送命令以控制 Spf 中的图。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **cmd_id** – **[in]** 标识命令
- **cmd_payload** – **[inout]** 特定于命令的参数
- **cmd_payload_sz** – **[in]** cmd_payload 的大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_read`(`gsl_handle_t` `graph_handle`, `uint32_t` `tag`, `struct` `gsl_buff` `*``buff`, `uint32_t` `*``filled_size`)**

从 Spf 接收数据缓冲区。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **tag** – **[in]** 用于标识 Spf 中要从其读取缓冲区的模块
- **buff** – **[inout]** 数据将被拷贝到的缓冲区
- **filled_size** – **[out]** GSL 实际填入缓冲区的字节数

**返回值：**

成功返回 EOK；当因图关闭、停止或刷新而使缓冲区未排入 spf 队列时返回 AR_EABORTED（非致命错误）；否则返回错误码

**`int32_t` `gsl_write`(`gsl_handle_t` `graph_handle`, `uint32_t` `tag`, `struct` `gsl_buff` `*``buff`, `uint32_t` `*``consumed_size`)**

向 Spf 写入数据缓冲区。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **tag** – **[in]** 用于标识 Spf 中要向其写入缓冲区的模块
- **buff** – **[in]** 包含将被写入数据的缓冲区
- **consumed_size** – **[out]** GSL 实际消费的字节数

**返回值：**

成功返回 EOK；当因图关闭、停止或刷新而使缓冲区未排入 spf 队列时返回 AR_EABORTED（非致命错误）；否则返回错误码

**`int32_t` `gsl_register_event_cb`(`gsl_handle_t` `graph_handle`, `gsl_cb_func_ptr` `cb`, `void` `*``client_data`)**

向 Spf 注册一个事件回调函数。

**参数：**

- **graph_handle** – **[in]** 从 gsl_open 返回的图句柄
- **cb** – **[in]** 指向回调函数的指针
- **client_data** – **[in]** 将在回调中传给客户端的不透明数据

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_get_tagged_data`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `uint32_t` `tag`, `struct` `gsl_key_vector` `*``tag_key_vect`, `uint8_t` `*``payload`, `size_t` `*``payload_size`)**

在数据库中查询与给定 tag 和 tkv 关联的数据。此 API 用于以 {IID, PID, Size, ErrorCode, variable length payload} 的形式获取 spf 模块数据。

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **tag** – **[in]** 用于标识某种能力
- **tag_key_vect** – **[in]** 用于在 acdb 中标识某个特定负载的标签键向量
- **payload** – **[inout]** 指向负载将被拷贝到的缓冲区的指针
- **payload_size** – **[inout]** 保存为 payload 传入的客户端缓冲区大小，返回时将保存实际写入缓冲区的数据大小。

**返回值：**

成功返回 EOK，否则返回错误码。如果所提供的 payload_size 不足以容纳输出数据，将返回错误码 AR_ENEEDMORE，并将 payload_size 设置为预期大小。

**`int32_t` `gsl_get_tagged_module_info`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `uint32_t` `tag`, `struct` `gsl_module_id_info` `*``*``module_info`, `uint32_t` `*``module_info_size`)**

在数据库中查询 module_iid 到 module_id 的映射数据。

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **tag** – **[in]** 标识 ACDB 中被系统设计者用此 tag 标记的一组模块
- **module_info** – **[out]** 模块信息将被拷贝到此处。GSL 会动态分配内存以容纳与该 tag 相匹配的 num_modules 个模块的 module_info。客户端负责在使用后释放该内存。
- **module_info_size** – **[out]** 保存写入 module_info 缓冲区的数据大小

**返回值：**

成功返回 EOK，否则返回错误码。

**`int32_t` `gsl_get_tags_with_module_info`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `void` `*``tag_module_info`, `size_t` `*``tag_module_info_size`)**

给定一个图键向量，在数据库中查询所有 tag 以及对应的 module_iid 和 module_id 映射。

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **tag_module_info** – **[inout]** tag 模块信息将被拷贝到此处。GSL 客户端会调用此 API 两次，第一次调用时 tag_module_info 设为 NULL，GSL 仅填充大小 *tag_module_info_size。随后 GSL 客户端分配内存并将其设为 tag_module_info，再第二次调用该 API，tag 模块信息就被拷贝到该内存中。负载格式为 “struct gsl_tag_module_info”
- **tag_module_info_size** – **[inout]** 用于由客户端提供 tag_module_info 的大小（以字节计），并在客户端所传大小过小时由 gsl 输出预期大小

**返回值：**

成功返回 EOK，否则返回错误码。

**`int32_t` `gsl_enable_acdb_persistence`(`uint8_t` `enable_flag`)**

为设置到 ACDB 的校准启用持久化

**参数：**

**enable_flag** – **[in]** 1 表示启用，0 表示禁用

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_cal_data_to_acdb`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `const` `struct` `gsl_key_vector` `*``cal_key_vect`, `uint8_t` `*``payload`, `uint32_t` `payload_size`)**

将自定义校准存储到 ACDB。

更多文档参见 acdb.h 中的 ACDB_CMD_SET_CAL_DATA

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **cal_key_vect** – **[in]** 用于在 acdb 中标识某个条目的标签键向量
- **payload** – **[in]** 指向包含自定义校准的缓冲区的指针
- **payload_size** – **[in]** 保存为 payload 传入的客户端缓冲区大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_get_cal_data_from_acdb`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `const` `struct` `gsl_key_vector` `*``cal_key_vect`, `uint32_t` `num_modules`, `uint8_t` `*``param_list`, `void` `*``payload`, `uint32_t` `*``payload_size`)**

从 ACDB 检索自定义校准。

更多文档参见 acdb.h 中的 ACDB_CMD_GET_CAL_DATA

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **cal_key_vect** – **[in]** 用于在 acdb 中标识某个条目的标签键向量
- **num_modules** – **[in]** param_list 中的模块实例数量
- **param_list** – **[in]** 要获取数据的模块实例列表及其参数
- **payload** – **[out]** 指向大小为返回的 payload_size 的缓冲区的指针，用于容纳返回的校准
- **payload_size** – **[inout]** 保存为 payload 传入的客户端缓冲区大小。客户端会调用此 API 两次，一次用于填充此负载大小，第二次用于填充负载，此时已为 payload 分配了返回 payload_size 大小的内存

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_tag_data_to_acdb`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `uint32_t` `tag_id`, `const` `struct` `gsl_key_vector` `*``tag_key_vect`, `uint8_t` `*``payload`, `uint32_t` `payload_size`)**

将自定义 tag 存储到 ACDB。

更多文档参见 acdb.h 中的 ACDB_CMD_SET_TAG_DATA

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **tag_id** – **[in]** 要设置的 tag ID
- **tag_key_vect** – **[in]** 用于在 acdb 中标识某个条目的标签键向量
- **payload** – **[in]** 指向包含自定义 tag 数据的缓冲区的指针
- **payload_size** – **[in]** 保存为 payload 传入的客户端缓冲区大小

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_get_tag_data_from_acdb`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `uint32_t` `tag_id`, `const` `struct` `gsl_key_vector` `*``tag_key_vect`, `uint32_t` `num_modules`, `uint8_t` `*``param_list`, `void` `*``payload`, `uint32_t` `*``payload_size`)**

从 ACDB 检索自定义 tag。

更多文档参见 acdb.h 中的 ACDB_CMD_GET_TAG_DATA

**参数：**

- **graph_key_vect** – **[in]** 图键向量
- **tag_id** – **[in]** 要检索数据的 tag ID
- **tag_key_vect** – **[in]** 用于在 acdb 中标识某个条目的标签键向量
- **num_modules** – **[in]** param_list 中的模块实例数量
- **param_list** – **[in]** 要获取数据的模块实例列表及其参数
- **payload** – **[out]** 指向大小为返回的 payload_size 的缓冲区的指针，用于容纳返回的 tag 数据
- **payload_size** – **[inout]** 保存为 payload 传入的客户端缓冲区大小。客户端会调用此 API 两次，一次用于填充此负载大小，第二次用于填充负载，此时已为 payload 分配了返回 payload_size 大小的内存

**返回值：**

成功返回 EOK，否则返回错误码

**`int32_t` `gsl_set_temp_path_to_acdb`(`uint32_t` `path_length`, `const` `char` `*``temp_path`)**

更新 AML 用于 reinit/delta 持久化功能的读/写临时路径。

**参数：**

- **cmd_id** – **[in]** 命令 ID 为 ACDB_CMD_SET_TEMP_PATH。
- **cmd** – **[in]** 一个不超过 255 个字符、以 null 结尾的字符数组

**返回值：**

- AR_EOK — 命令执行成功。AR_EBADPARAM — 提供了无效的输入参数。AR_EFAILED — 命令执行失败。

**`int32_t` `gsl_get_processed_buff_cnt`(`gsl_handle_t` `graph_handle`, `enum` `gsl_data_dir` `dir`, `uint32_t` `*``cnt`)**

获取 GSL 已处理数据缓冲区的持续递增计数。

对于播放情形，返回 Spf 已确认（ack）的缓冲区数量。对于采集情形，返回从 Spf 接收到的缓冲区数量。

**参数：**

- **graph_handle** – **[in]** 图句柄
- **dir** – **[in]** 指示返回写缓冲区计数还是读缓冲区计数
- **cnt** – **[out]** 持续递增的缓冲区计数，达到 SIZE_MAX 后回绕归零

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_avail_buffer_size`(`gsl_handle_t` `graph_handle`, `enum` `gsl_data_dir` `dir`, `uint32_t` `*``bytes`)**

获取可供写入（播放）/读取（采集）的可用缓冲区大小（以字节计）

对于播放情形，返回供 GSL 客户端写入的空缓冲区大小（以字节计）。对于采集情形，返回 GSL 客户端可排入 SPF 队列以供读取的缓冲区大小（以字节计）。

**参数：**

- **graph_handle** – **[in]** 图句柄
- **dir** – **[in]** 指示返回可写还是可读的可用缓冲区大小
- **bytes** – **[out]** 可供写入（播放）/读取（采集）的缓冲区大小（以字节计）

**返回值：**

成功返回 AR_EOK，否则返回错误码。

**`int32_t` `gsl_get_driver_data`(`const` `uint32_t` `module_id`, `const` `struct` `gsl_key_vector` `*``key_vect`, `void` `*``data_payload`, `uint32_t` `*``data_payload_size`)**

获取驱动数据。

此 API 供 GSL 客户端调用，用于查询它们存储在 ACDB 中的任何驱动特定数据

**参数：**

- **module_id** – **[in]** 客户端定义的 module_id，数据在 acdb 中以其为键存储
- **key_vect** – **[in]** 可选，用于查找数据的键向量
- **data_payload** – **[in]** 数据将返回到的缓冲区，客户端负责为该缓冲区分配内存。如果设为 NULL，则输出数据的大小会返回在 data_payload_size 中
- **data_payload_size** – **[inout]** 输入时包含 data_payload 的大小，输出时将保存实际写入的大小

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_graph_tkvs`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `struct` `gsl_tag_key_vector_list` `*``data_payload`)**

获取所有 tag/TKV 变体。

检索在 ACDB 中为某个给定图键向量所定义的所有 tag 和标签键向量变体

**参数：**

- **graph_key_vect** – **[in]** 要在 ACDB 中为其查找 tag 和 TKV 对的 GKV
- **data_payload** – **[inout]** 数据将返回到的缓冲区，客户端负责为该缓冲区分配内存。如果 data_payload->key_vector_list 设为 NULL，则输出数据的大小会返回在 data_payload->list_size 中。

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_graph_ckvs`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `struct` `gsl_key_vector_list` `*``data_payload`)**

获取给定 GKV 的所有 CKV。

查询某个给定图键向量下的所有 SPF 模块校准键向量。

**参数：**

- **graph_key_vect** – **[in]** 要在 ACDB 中为其查找 CKV 的 GKV
- **data_payload** – **[inout]** 数据将返回到的缓冲区，客户端负责为该缓冲区分配内存。如果 data_payload->key_vector_list 设为 NULL，则输出数据的大小会返回在 data_payload->list_size 中。

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_driver_module_kvs`(`uint32_t` `driver_id`, `struct` `gsl_key_vector_list` `*``data_payload`)**

获取驱动模块所使用的 KV。

在 ACDB 中查询某个特定驱动模块所使用的所有驱动键向量

**参数：**

- **driver_id** – **[in]** 用于标识驱动模块的 uint32_t
- **data_payload** – **[inout]** 数据将返回到的缓冲区，客户端负责为该缓冲区分配内存。如果 data_payload->key_vector_list 设为 NULL，则输出数据的大小会返回在 data_payload->list_size 中。

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_supported_gkvs`(`uint32_t` `*``key_ids`, `const` `uint32_t` `num_key_ids`, `struct` `gsl_key_vector_list` `*``data_payload`)**

获取所有以所提供的 key ID 为子集的 GKV。

在 ACDB 中查询所有以所提供 key id 为子集的图键向量。如果一个图键向量匹配该 key id 子集，则它支持某些能力。如果该子集包含零个 key，则此 api 将返回 ACDB 中定义的所有图键向量。

**参数：**

- **key_ids** – **[in]** 指向要查询的 key ID 集合的指针。由客户端管理
- **num_key_ids** – **[in]** key_ids 中的条目数量
- **data_payload** – **[inout]** 数据将返回到的缓冲区，客户端负责为该缓冲区分配内存。如果 data_payload->key_vector_list 设为 NULL，则输出数据的大小会返回在 data_payload->list_size 中。

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_get_graph_alias`(`const` `struct` `gsl_key_vector` `*``graph_key_vect`, `char` `*``alias`, `uint32_t` `*``alias_len`)**

获取某个 GKV 的人类可读别名

为提高可读性，检索图键向量的一个别名。该别名包括用例 ID，其后跟一个带有键和值名称的人类可读图键向量。字符串长度限制为 255 字节。

此 API 需调用两次：一次用于获取大小，一次用于获取字符串。

**参数：**

- **graph_key_vect** – **[in]** 要为其查找别名的 GKV
- **alias** – **[inout]** 包含别名的字符串。客户端负责为该缓冲区分配内存。如果设为 NULL，则输出数据的大小会返回在 alias_len 中。
- **alias_len** – **[inout]** 字符串的长度，包含 null 结尾字符。输入时包含 alias 已分配的大小，输出时将保存实际写入的大小

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_add_database`(`struct` `gsl_acdb_data_files` `*``acdb_data_files`, `struct` `gsl_acdb_file` `*``writable_file_path`, `gsl_acdb_handle_t` `*``acdb_handle`)**

添加 acdb 数据库

通过在运行时添加数据库文件（*.acdb 和 *.qwsp）来扩展数据库。

**参数：**

- **acdb_data_files** – **[in]** 包含 *.acdb 和 *.qwsp 的数据库文件路径列表
- **writable_file_path** – **[in]** delta 数据文件路径和临时文件
- **[in/out]** – acdb_handle：所提供数据库的句柄

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_remove_database`(`gsl_acdb_handle_t` `acdb_handle`)**

移除 acdb 数据库

通过在运行时移除与给定数据库句柄关联的所有数据来收缩数据库。这包括数据库文件（*.qwsp 和 .acdb）以及堆数据

**参数：**

**acdb_handle** – **[in]** 要移除的数据库的句柄

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_cshm_alloc`(`uint32_t` `size`, `gsl_cshm_info_t` `*``info`)**

为外部客户端分配共享内存。向 SPF 发送 APM_CMD_GLOBAL_SHARED_MEM_MAP_REGIONS 命令以映射所分配的内存。

**参数：**

- **size** – **[in]** 要分配的字节数
- **[in/out]** – info：要分配的共享内存的属性。所分配内存的 fd 和 mem_id

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_cshm_dealloc`(`gsl_mem_id_t` `mem_id`)**

为外部客户端释放共享内存。向 SPF 发送 APM_CMD_GLOBAL_SHARED_MEM_UNMAP_REGIONS 命令以取消映射要释放的内存。

**参数：**

**mem_id** – **[in]** 要释放的共享内存的标识符

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`int32_t` `gsl_cshm_msg`(`gsl_mem_id_t` `mem_id`, `uint32_t` `offset`, `uint32_t` `length`, `uint32_t` `miid`, `uint32_t` `prop_flag`)**

就针对共享内存块的特定操作，向运行在 SPF 中的模块发送通知。该操作对 gsl 而言是不透明的。向 SPF 发送 AR_SPF_MSG_GLOBAL_SH_MEM 命令，使其转发给自定义模块。

**参数：**

- **mem_id** – **[in]** 要释放的共享内存的标识符
- **offset** – **[in]** 该内存块起始处相对于内存的偏移（以字节计）。这是相对于所分配的整块共享内存的起点而言的
- **length** – **[in]** 该内存块的大小。
- **miid** – **[in]** 此调用所面向模块的模块实例 ID（Module Instance ID）。若 miid 无效/不活动，则返回错误。
- **prop_flag** – **[in]** 为此调用提供附加信息的标志。Bit 0 – 释放内存位，用于表达客户端是否希望模块释放/停止使用一块先前告知过的内存。0 – 默认，不是释放消息。1 – 此时若 length 为零，则要求模块释放用 mem_id 映射给它的整块内存；若 length 非零，则要求模块仅释放该内存块。

**返回值：**

成功返回 AR_EOK，否则返回错误码

**`struct` `gsl_key_value_pair`**

*#include <gsl_intf.h>*键向量中的单个条目

公共成员

**`uint32_t` `key`**

键

**`uint32_t` `value`**

值

**`struct` `gsl_key_vector`**

*#include <gsl_intf.h>*一个完整的键向量

公共成员

**`uint32_t` `num_kvps`**

键值对数量

**`struct` `gsl_key_value_pair` `*``kvp`**

键值对向量

**`struct` `gsl_key_vector_array`**

*#include <gsl_intf.h>*一个带零长数组的键向量。

公共成员

**`uint32_t` `num_keys`**

键数量

**`struct` `gsl_key_value_pair` `kvp``[``]`**

键值对数组。

**`struct` `gsl_key_vector_list`**

*#include <gsl_intf.h>*一个键向量列表

公共成员

**`uint32_t` `num_key_vectors`**

< 键向量列表中的键向量数量；键向量列表的大小（以字节计）

**`uint32_t` `list_size`**

以 [#keys, kvPair+,…, #keys, kvPair+] 格式排列的键向量列表

**`struct` `gsl_key_vector_array` `*``key_vector_list`**

**`struct` `gsl_tag_key_vector`**

*#include <gsl_intf.h>*一个带零长数组的标签键向量

公共成员

**`uint32_t` `tag_id`**

< 模块标签标识符；键数量

**`uint32_t` `num_keys`**

图键值对

**`struct` `gsl_key_value_pair` `kvp``[``]`**

**`struct` `gsl_tag_key_vector_list`**

*#include <gsl_intf.h>*一个标签键向量列表

公共成员

**`uint32_t` `num_key_vectors`**

< 键向量列表中的键向量数量；键向量列表的大小（以字节计）

**`uint32_t` `list_size`**

以 [#keys, kvPair+,…, #keys, kvPair+] 格式排列的键向量列表

**`struct` `gsl_tag_key_vector` `*``key_vector_list`**

**`struct` `gsl_cmd_properties`**

*#include <gsl_intf.h>*GSL_CMD_STOP ioctl 的命令负载。用于匹配将应用该命令的图的各部分的属性。此结构体用于与 gsl_subgraph_driver_props.h 中定义的属性进行匹配

公共成员

**`struct` `gsl_key_vector` `gkv`**

用于限定操作范围的图键向量

**`uint32_t` `property_id`**

子图的属性 ID

**`uint32_t` `num_property_values`**

子图属性 ID 的值的数量

**`uint32_t` `*``property_values`**

指向 property values[num_property_values] 的指针。如果子图的属性值匹配此集合中的任一值，则该命令将在该子图上执行

**`struct` `gsl_cmd_configure_read_write_params`**

*#include <gsl_intf.h>*GSL_CMD_CONFIGURE_WRITE_PARAMS 和 GSL_CMD_CONFIGURE_READ_PARAMS 的命令负载

公共成员

**`uint32_t` `buff_size`**

单个缓冲区中的最大字节数。读/写操作所取的缓冲区大小应为 buff_size 的整数倍。

**`uint32_t` `num_buffs`**

GSL 将用于数据交换的缓冲区数量

**`uint32_t` `start_threshold`**

在写的情况下，等到从客户端收到的字节数超过（ABOVE）此值后再向 SPF 下发 START；在读的情况下，等到客户端已读取了这么多字节后再向 SPF 下发 START。设为 0 表示立即启动

**`uint32_t` `stop_threshold`**

待定（TBD），目前不支持

**`uint32_t` `attributes`**

用于指示数据传输属性的位域，下面是所定义的字段：data_mode（Bits 0,1,2）：为 GSL_DATA_MODE_SHMEM、GSL_DATA_MODE_BLOCKING、GSL_DATA_MODE_NON_BLOCKING、GSL_DATA_MODE_PUSH_PULL、GSL_DATA_MODE_EXTERN_MEM 之一。datapath_setup（Bits 3,4）：为 GSL_DATAPATH_SETUP_DEFAULT、GSL_DATAPATH_SETUP_ALLOC_SHMEM_ONLY、GSL_DATAPATH_SETUP_SPF_PROVISION_ONLY 之一

**`uint32_t` `shmem_ep_tag`**

可选 tag，用于在首次 gsl_graph_read 之前对读缓冲区排队。当设为 0 时，在首次 gsl_graph_read 调用之前不对缓冲区排队

**`uint32_t` `platform_info`**

可选字段，用于向 GSL 传递平台特定数据，例如可用于向 osal 层传达某些堆属性。对于没有任何特定平台数据的客户端必须设为 0。

**`uint32_t` `max_metadata_size`**

**`struct` `gsl_cmd_graph_select`**

*#include <gsl_intf.h>*GSL_CMD_ADD_GRAPH 和 GSL_CMD_CHANGE_GRAPH 的命令负载

公共成员

**`struct` `gsl_key_vector` `graph_key_vector`**

用于查找新图。在 GSL_CMD_CHANGE_GRAPH 的情况下，旧图将被拆除，新图将被建立。在 GSL_CMD_ADD_GRAPH 的情况下，新图被建立而不拆除旧图

**`struct` `gsl_key_vector` `cal_key_vect`**

用于查找将设置到新图上的校准数据

**`struct` `gsl_cmd_remove_graph`**

*#include <gsl_intf.h>*GSL_CMD_REMOVE_GRAPH 的命令负载

公共成员

**`struct` `gsl_key_vector` `graph_key_vector`**

用于查找将被移除的图

**`struct` `gsl_shmem_buf`**

*#include <gsl_intf.h>*GSL_CMD_GET_WRITE_BUFF_INFO 和 GSL_CMD_GET_READ_BUFF_INFO 的命令负载。GSL 写入调用者创建的负载。调用者负责提供足够的内存以容纳所有缓冲区的地址。

公共成员

**`uint8_t` `*``addr`**

缓冲区地址

**`uint64_t` `metadata`**

每个缓冲区的元数据

**`struct` `gsl_cmd_get_shmem_buf_info`**

*#include <gsl_intf.h>*公共成员

**`uint32_t` `size`**

缓冲区大小，所有缓冲区大小相同

**`uint32_t` `num_buffs`**

缓冲区数量

**`struct` `gsl_shmem_buf` `*``buffs`**

缓冲区列表，包含 num_buffs 个条目

**`struct` `gsl_cmd_register_custom_event`**

*#include <gsl_intf.h>*GSL_CMD_REGISTER_CUSTOM_EVENT 的命令负载

公共成员

**`uint32_t` `module_instance_id`**

模块的有效实例 ID

**`uint32_t` `event_id`**

模块的有效事件 ID

**`uint32_t` `event_config_payload_size`**

基于 module_instance_id/event_id 组合的事件配置数据大小。> 0 字节，且至少为 4 字节的整数倍

**`uint32_t` `is_register`**

1 - 注册该事件；0 - 注销该事件

**`uint8_t` `event_config_payload``[``]`**

模块特定的事件注册负载

**`struct` `gsl_acdb_file`**

*#include <gsl_intf.h>*保存单个 acdb 文件的路径，此结构体应与 ACDB API 所期望的按位匹配

公共成员

**`uint32_t` `fileNameLen`**

完整文件路径名长度

**`char` `fileName``[``GSL_MAX_LEN_OF_ACDB_FILENAME``]`**

保存 ACDB 文件路径和名称的数组，长度不能超过 256 个字符，包括 NULL 结尾字符

**`struct` `gsl_acdb_data_files`**

*#include <gsl_intf.h>*保存 ACDB 文件列表，此结构体应与 ACDB API 所期望的按位匹配

公共成员

**`uint32_t` `num_files`**

ACDB 文件数量

**`struct` `gsl_acdb_file` `acdbFiles``[``GSL_MAX_NUM_OF_ACDB_FILES``]`**

ACDB 文件完整路径数组

**`struct` `gsl_init_data`**

*#include <gsl_intf.h>*gsl_init 的参数

公共成员

**`struct` `gsl_acdb_data_files` `*``acdb_files`**

要传给 acdb 的 acdb 文件，设为 NULL 意味着将使用 acdb_addr 来访问数据

**`struct` `gsl_acdb_file` `*``acdb_delta_file`**

acdb delta 文件的路径

**`const` `void` `*``acdb_addr`**

acdb 镜像地址

**`uint32_t` `max_num_ready_checks`**

指示 GSL 应检查 spf 是否就绪的次数，gsl_init 调用会阻塞直到 spf 就绪。若此字段设为 0，则跳过 spf 就绪检查

**`uint32_t` `ready_check_interval_ms`**

GSL 在重新尝试检查 Spf 就绪之前等待的时间量（以 ms 计）

**`struct` `gsl_extern_alloc_buff_info`**

*#include <gsl_intf.h>*公共成员

**`uint64_t` `alloc_handle`**

标识外部内存分配的唯一句柄

**`uint32_t` `alloc_size`**

该分配的大小（以字节计）

**`uint32_t` `offset`**

数据缓冲区在该分配内的偏移（以字节计）

**`struct` `gsl_buff`**

*#include <gsl_intf.h>*用于向 gsl_read 和 gsl_write 传递缓冲区信息的结构体，也用作 GSL_EVENT_ID_READ_DONE 和 GSL_EVENT_ID_WRITE_DONE 的返回负载

公共成员

**`uint64_t` `timestamp`**

时间戳（以微秒计）

**`uint32_t` `flags`**

位掩码标志，例如 GSL_BUFF_FLAG_EOS

**`uint32_t` `size`**

缓冲区大小（以字节计）

**`uint8_t` `*``addr`**

数据缓冲区。在外部内存模式下不使用

**`uint32_t` `metadata_size`**

元数据缓冲区大小（以字节计）

**`uint8_t` `*``metadata`**

元数据缓冲区。可包含多个元数据

**`struct` `gsl_extern_alloc_buff_info` `alloc_info`**

外部内存模式信息

**`struct` `gsl_module_id_info_entry`**

*#include <gsl_intf.h>*将单个模块的模块实例 id 映射到模块 id

公共成员

**`uint32_t` `module_id`**

模块 id

**`uint32_t` `module_iid`**

全局唯一的模块实例 id

**`struct` `gsl_module_id_info`**

*#include <gsl_intf.h>*用于向客户端返回模块信息数据

公共成员

**`uint32_t` `num_modules`**

下面模块列表中的条目数量

**`struct` `gsl_module_id_info_entry` `module_entry``[``]`**

模块列表

**`struct` `gsl_tag_module_info_entry`**

*#include <gsl_intf.h>*将 tag_id 映射到模块信息（mid 和 miid）的结构体

公共成员

**`uint32_t` `tag_id`**

模块的 tag id

**`uint32_t` `num_modules`**

与该 tag_id 相匹配的模块数量

**`struct` `gsl_module_id_info_entry` `module_entry``[``]`**

模块列表

**`struct` `gsl_tag_module_info`**

*#include <gsl_intf.h>*给定一个图键向量，用于向客户端返回 tag 和模块信息数据

公共成员

**`uint32_t` `num_tags`**

tag 数量

**`uint8_t` `tag_module_entry``[``]`**

类型为 struct gsl_tag_module_info_entry 的可变负载

**`struct` `gsl_event_read_write_done_payload`**

*#include <gsl_intf.h>*随 GSL_EVENT_ID_READ_DONE 和 GSL_EVENT_ID_WRITE_DONE 事件传给客户端的事件负载

公共成员

**`uint32_t` `tag`**

用于读/写该缓冲区的 tag

**`uint32_t` `status`**

数据缓冲区状态，如 ar_osal_error.h 中所定义

**`uint32_t` `md_status`**

元数据状态，如 ar_osal_error.h 中所定义

**`struct` `gsl_buff` `buff`**

传给 gsl_read/gsl_write 的缓冲区

**`struct` `gsl_event_eos_payload`**

*#include <gsl_intf.h>*随 GSL_EVENT_ID_EOS 传给客户端的事件负载

公共成员

**`uint32_t` `module_instance_id`**

抛出该 EOS 事件的模块实例 id，当被丢弃时为无效值（0）。

**`enum` `gsl_eos_render_status_t` `render_status`**

指示最后一个采样是被渲染还是被丢弃

**`struct` `gsl_global_event_svc_dn_payload`**

*#include <gsl_intf.h>*随 GSL_GLOBAL_EVENT_AUDIO_SVC_DN 传给客户端的事件负载

公共成员

**`uint32_t` `num_handles`**

图句柄数量

**`gsl_handle_t` `*``handle_list`**

受音频服务停止影响的图句柄列表，客户端负责关闭这些句柄，并在收到音频服务启动通知后重新打开它们

**`struct` `gsl_event_cb_params`**

*#include <gsl_intf.h>*将在事件回调中传给客户端的数据

公共成员

**`uint32_t` `source_module_id`**

标识生成该事件的模块

**`uint32_t` `event_id`**

标识该事件，在 GSL 内部事件的情况下它将保存来自 enum gsl_event_id 的一个值

**`uint32_t` `event_payload_size`**

下面负载的大小

**`void` `*``event_payload`**

与该事件关联的负载（如有）

**`struct` `gsl_cshm_info`**

*#include <gsl_intf.h>*公共成员

**`gsl_cshm_cache_type_t` `type`**

带缓存或不带缓存的内存类型。

**`gsl_subsystem_t` `subsystem_mask`**

允许在多个 DSP 之间路由共享内存访问。

**`int32_t` `flag`**

共享内存分配的标志。

**`uint64_t` `fd`**

映射内存区域的文件描述符。

**`gsl_mem_id_t` `mem_id`**

唯一的 GSL 内存标识符。
