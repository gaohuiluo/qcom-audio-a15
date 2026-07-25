# Graph Service Layer

Defines public APIs for Graph Service Layer (GSL)

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause

Defines

**`GSL_MAX_NUM_OF_ACDB_FILES`**

maximum number of acdb files

**`GSL_MAX_LEN_OF_ACDB_FILENAME`**

maxumum lengh of filename

**`GSL_ATTRIBUTES_DATA_MODE_MASK`**

keep 3 bits for specifying the data mode

**`GSL_DATA_MODE_SHMEM`**

shared memory mode

**`GSL_DATA_MODE_BLOCKING`**

heap memory mode blocking

**`GSL_DATA_MODE_NON_BLOCKING`**

heap memory mode non-blocking

**`GSL_DATA_MODE_PUSH_PULL`**

push-pull mode

**`GSL_DATA_MODE_EXTERN_MEM`**

external memory mode 2 bits to control datapath set up

**`GSL_ATTRIBUTES_DATAPATH_SETUP_MASK`**

shift amount for datapath setup flags

**`GSL_ATTRIBUTES_DATAPATH_SETUP_SHIFT`**

use these flags when it is necessary to separate the allocation of memory buffers from sharing those buffers with DSP Example: opening graph with no GKV and push pull mode, the endpoint IID for the use case is not yet known, so cannot send shmem to DSP.

default does allocation of buffers and shared mem setup together buffers must be allocated first before shmem can be set up Client is responsible for calling these in the correct order, i.e. shmem must be allocated before provisioning SPF allocate buffers and set them up on SPF EP

**`GSL_DATAPATH_SETUP_DEFAULT`**

allocate buffers, do not set up shmem on SPF endpoint

**`GSL_DATAPATH_SETUP_ALLOC_SHMEM_ONLY`**

set up shmem on SPF endpoint only GSL ignores other params sent when this flag is used, since the datapath must be configured with ALLOC_SHMEM_ONLY before calling with this flag

for packet-based modes, this operation is a no-op

**`GSL_DATAPATH_SETUP_SPF_PROVISION_ONLY`**

used to indicate a given buffer is the final buffer, client will get notified once the buffer has been rendered

**`GSL_BUFF_FLAG_EOS`**

true if buffer has a valid timestamp

**`GSL_BUFF_FLAG_TS_VALID`**

used to indicate a buffer is the last in a frame

**`GSL_BUFF_FLAG_EOF`**

used to indicate a buffer is media format, when this flag is set, buffer will contain the media format data only

**`GSL_BUFF_FLAG_MEDIA_FORMAT`**

**`GSL_EVENT_SRC_MODULE_ID_GSL`**

The source module_id for events originating from GSL and not from Spf

Typedefs

**`typedef void *gsl_handle_t`**

opaque handle that is returned to client

**`typedef void *gsl_acdb_handle_t`**

opaque acdb handle that is returned to client

**`typedef uint32_t (*gsl_global_cb_func_ptr)(enum gsl_global_event_ids event_id, void *event_payload, size_t event_payload_sz, void *client_data)`**

callback used to notify global events to client.

Global events are events that are not bound to a specific gsl graph handle.

**Param event_id:**

**[in]** indicates the global event id

**Param event_payload:**

**[in]** event id specific payload

**Param event_payload_sz:**

**[in]** size of the event id specific payload

**Param client_data:**

**[in]** opaque client data

**`typedef void (*gsl_cb_func_ptr)(struct gsl_event_cb_params *event_params, void *client_data)`**

Callback function signature for events to client.

**Param event_params:**

**[in]** holds all event related info

**Param client_data:**

**[in]** client data that was provided during cb registration

**`typedef uint32_t gsl_mem_id_t`**

**`typedef enum gsl_cshm_cache_type gsl_cshm_cache_type_t`**

**`typedef enum gsl_subsystem gsl_subsystem_t`**

**`typedef struct gsl_cshm_info gsl_cshm_info_t`**

Enums

**`enum gsl_cmd_id`**

Commands that can be passed to gsl_ioctl

*Values:*

**`enumerator GSL_CMD_START`**

Start a graph

**`enumerator GSL_CMD_PREPARE`**

Optional, can be called before GSL_CMD_START to start initializing modules in the DSP

**`enumerator GSL_CMD_FLUSH`**

Flush a graph, causes graph to drop all unprocessed buffers

**`enumerator GSL_CMD_STOP`**

Stop graph, stop processing data and reset to initial state Optional Payload: struct gsl_cmd_properties GRAPH_STOP is issued only to those subgraphs with matching property_ID and property_values

**`enumerator GSL_CMD_ADD_GRAPH`**

Add a new graph to an existing graph based on a new graph key vector. Payload: struct gsl_cmd_graph_select

**`enumerator GSL_CMD_REMOVE_GRAPH`**

Remove existing graph based on a graph key vector Payload: struct gsl_cmd_remove_graph

**`enumerator GSL_CMD_CHANGE_GRAPH`**

Modify existing graph based on a new graph key vector Payload: struct gsl_cmd_graph_select

**`enumerator GSL_CMD_QUERY_GRAPH_DELAY`**

Get the path delay associated with a graph

**`enumerator GSL_CMD_CONFIGURE_WRITE_PARAMS`**

Configure parameters used for write data exchange Payload: struct gsl_cmd_configure_read_write_params

**`enumerator GSL_CMD_CONFIGURE_READ_PARAMS`**

Configure parameters used for read data exchange Payload: struct gsl_cmd_configure_read_write_params

**`enumerator GSL_CMD_EOS`**

Insert EOS marker in playback data stream, the EOS marker is inserted in the stream immediately after all the data successfully written to GSL. Once all the buffers before the EOS marker are played out, GSL generates an EOS event to client. Note: If a gsl_write operation is pending when this command is issued the buffer passed in the pending gsl_write is not gauranteed to be played out.

**`enumerator GSL_CMD_GET_WRITE_BUFF_INFO`**

Get buffer pointers and sizes for use in shared memory mode write operations Payload: struct gsl_cmd_get_shmem_buf_info will be sent from client and will get written to by GSL.

**`enumerator GSL_CMD_GET_READ_BUFF_INFO`**

Get buffer pointers and sizes for use in shared memory mode read operations Payload: struct gsl_cmd_get_shmem_buf_info will be sent from client and will get written to by GSL.

**`enumerator GSL_CMD_GET_WRITE_POS_BUFF_INFO`**

Get pointer and size of position buffer used to synchronize writes in push/pull mode Payload: struct gsl_cmd_get_shmem_buf_info will be sent from client and will get written to by GSL.

**`enumerator GSL_CMD_GET_READ_POS_BUFF_INFO`**

Get pointer and size of position buffer used to synchronize reads in push/pull mode Payload: struct gsl_cmd_get_shmem_buf_info will be sent from client and will get written to by GSL.

**`enumerator GSL_CMD_REGISTER_CUSTOM_EVENT`**

Register a custom event with a spf module Payload: struct gsl_cmd_register_custom_event

**`enumerator GSL_CMD_FREE_READ_BUFF`**

Free all read buffers for a graph

**`enumerator GSL_CMD_FREE_WRITE_BUFF`**

Free all write buffers for a graph

**`enumerator GSL_CMD_SUSPEND`**

Suspend graph, stop processing data but does not reset to initial state If a subgraph is shared with multiple graphs then :- The common subgraph remains in START if at least one graph is in START. If none of the of graph is in START and one of the graph is in STOP then common subgraph goes to STOP state. Common subgraph goes to SUSPEND state only when all the graphs issue SUSPEND.

**`enumerator GSL_CMD_CLOSE_WITH_PROPS`**

Close subset of subgraphs in the graph based on properties Payload: struct gsl_cmd_properties GRAPH_STOP is issued only to those subgraphs with matching property_ID and property_values

**`enumerator GSL_CMD_MAX`**

**`enum gsl_event_id`**

Events that will be notified to client from GSL

*Values:*

**`enumerator GSL_EVENT_ID_EOS`**

End of stream event, indicates that all data written to GSL prior to client calling GSL_CMD_EOS has been played out Payload: struct gsl_event_eos_payload

**`enumerator GSL_EVENT_ID_READ_DONE`**

Indicates buffer provided as part of read call has been filled Payload: struct gsl_event_read_write_done_payload

**`enumerator GSL_EVENT_ID_WRITE_DONE`**

Indicates buffer provided as part of write has been consumed Payload: struct gsl_event_read_write_done_payload

**`enumerator GSL_EVENT_ID_BUFFER_AVAIL`**

Sent in non-blocking mode only, indicates that buffer has become available for client to write to

**`enumerator GSL_EVENT_ID_MAX`**

**`enum gsl_global_event_ids`**

Global events that can be raised through the global callback

*Values:*

**`enumerator GSL_GLOBAL_EVENT_AUDIO_SVC_UP`**

Indicates that an audio service is up, this can happen for example due to restart after SSR. payload: NULL

**`enumerator GSL_GLOBAL_EVENT_AUDIO_SVC_DN`**

Indicates that an audio service is down, this can happen for example due to SSR. payload: struct gsl_global_event_svc_dn_payload

**`enumerator GSL_GLOBAL_EVENT_MAX`**

**`enum gsl_data_dir`**

Identifies data direction

*Values:*

**`enumerator GSL_DATA_DIR_READ`**

Indicates data is provided from gsl to client

**`enumerator GSL_DATA_DIR_WRITE`**

Indicates data is provided from client to gsl

**`enum gsl_eos_render_status_t`**

EOS rendered status returned from Spf

*Values:*

**`enumerator GSL_EOS_RENDERED`**

**`enumerator GSL_EOS_DROPPED`**

**`enum gsl_cshm_cache_type`**

*Values:*

**`enumerator GSL_CSHM_CACHED`**

0 cached.

**`enumerator GSL_CSHM_UNCACHED`**

1 uncached.

**`enum gsl_subsystem`**

*Values:*

**`enumerator GSL_SS_INVALID`**

Invalid sub system.

**`enumerator GSL_SS_MODEM_DSP`**

Used for MODEM DSP sub system.

**`enumerator GSL_SS_APPS`**

Used for APPS sub system.

**`enumerator GSL_SS_SENSOR_DSP`**

Used for SENSOR DSP sub system.

**`enumerator GSL_SS_COMPUTE_DSP`**

Used for COMPUTE DSP sub system.

**`enumerator GSL_SS_CC_DSP`**

Used for Companion chip DSP (CC_DSP) sub system.

**`enumerator GSL_SS_ADSP`**

Used for ADSP sub system.

Functions

**`void gsl_get_version`(`uint32_t *major`, `uint32_t *minor`)**

Returns the GSL version.

**Parameters:**

- **major** – **[out]** the major version is incremented whenever the current version is NOT backwards compatible with previous version
- **minor** – **[out]** the minor version is incremented whenever the current version has additional features to the previous version but is backwards compatible with it

**`int32_t gsl_init`(`struct gsl_init_data *init_data`)**

Initialize GSL, must be called before any other GSL calls.

**Parameters:**

**init_data** – **[in]** data used during initialization

**`int32_t gsl_cshm_init`(`uint32_t num_client`)**

Initialize GSL cshm, must be called before any other cshm calls.

**Parameters:**

**num_client** – **[in]** number of clients to be intialized with. If 0, then default value of CSHM_DEFAULT_INIT_CLIENT_NUM will be used.

**`int32_t gsl_cshm_deinit`(`void`)**

De-Initialize GSL cshm, must be called after gsl_deinit()

**`void gsl_deinit`(`void`)**

De-initialize GSL, no GSL APIs should be called after this

**`int32_t gsl_register_global_event_cb`(`gsl_global_cb_func_ptr global_cb`, `void *client_data`)**

Register a global callback function for GSL.

**Parameters:**

- **global_cb** – **[in]** callback function pointer used to notify global events such as SSR
- **client_data** – **[in]** opaque client data that will be passed back to client whenever the callback is invoked

**`int32_t gsl_open`(`const struct gsl_key_vector *graph_key_vect`, `const struct gsl_key_vector *cal_key_vect`, `gsl_handle_t *graph_handle`)**

Load a graph that is specified using graph_key_vector to the DSP. Does not reload graphs which are already loaded.

**Parameters:**

- **graph_key_vect** – **[in]** used to identify the graph.
- **cal_key_vect** – **[in]** OPTIONAL used to identify calibration data to be sent to the graph, setting to NULL means dont send any calibration
- **graph_handle** – **[out]** graph handle on success, null otherwise

**Returns:**

GSL_EOK on success, error code otherwise

**`int32_t gsl_close`(`gsl_handle_t graph_handle`)**

Close a graph that was specified using the graph_handle.

**Parameters:**

**graph_handle** – **[in]** Handle of the graph to close

**Returns:**

GSL_EOK on success, error code otherwise

**`int32_t gsl_set_cal`(`gsl_handle_t graph_handle`, `const struct gsl_key_vector *graph_key_vect`, `const struct gsl_key_vector *cal_key_vect`)**

Push calibration data for a given graph to DSP, Must be called before a graph is started. This API need not be called in the case of GSL_CMD_CHANGE_GRAPH as the calibration will be set during the graph change operation itself.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **graph_key_vect** – **[in]** OPTIONAL identifies the portion of the graph to which this calibration needs to be applied to. For SSMD scenarios, graph_handle can contain more than one graph key vector. In such cases, clients can provide specific graph key vector to which this calibration needs to be set. The graph_key_vector input should match to one of the GKVs that the graph_handle has. If this parameter is NULL, then GSL sets the prior_ckv to the one that was given during gsl_open().
- **cal_key_vect** – **[in]** used to identify the cal data.

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_config`(`gsl_handle_t graph_handle`, `const struct gsl_key_vector *graph_key_vect`, `uint32_t tag`, `const struct gsl_key_vector *tag_key_vect`)**

Set a configuration payload on a specified graph, the payload is stored in acdb.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **graph_key_vect** – **[in]** OPTIONAL identifies the portion of the graph to which this config needs to be applied. For SSMD scenarios, graph_handle can contain more than one graph key vector. In such cases, clients can provide specific graph key vector to which this calibration needs to be set. The graph_key_vector input should match to one of the GKVs that the graph_handle has.
- **tag** – **[in]** identifies a capability in acdb
- **tag_key_vect** – **[in]** identifies a payload in the database

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_custom_config`(`gsl_handle_t graph_handle`, `const uint8_t *payload`, `const uint32_t payload_size`)**

Set a custom configuration parameter on a specified graph, the payload is provided from the caller.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **payload** – **[in]** custom caller defined payload that will get sent to the module, payload structure shall be always according to OOB sturcutre format defined by SPF
- **payload_size** – **[in]** the size of the payload buffer

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_tagged_custom_config`(`gsl_handle_t graph_handle`, `uint32_t tag`, `const uint8_t *payload`, `const size_t payload_size`)**

Set a custom configuration parameter on a specified graph, the payload is provided from the caller. Caller also provides tag ID so gsl can look up ACDB for the module IID to which this payload needs to be sent to.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **tag** – **[in]** identifies a module instance matching the tag ID
- **payload** – **[in]** custom caller defined payload that gets sent to the module, payload structure shall be always according to format defined by SPF {MIID, PID, Size, Error Code, Variable payload}
- **payload_size** – **[in]** the size of the payload buffer

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_tagged_custom_config_persist`(`gsl_handle_t graph_handle`, `uint32_t tag`, `const uint8_t *payload`, `const uint32_t payload_size`)**

Persistent set a custom configuration parameter on a specified graph, the payload is provided from the caller. Caller also provides tag ID so gsl can look up ACDB for the module IID to which this payload needs to be sent to. LIMITATION: The payload can contain only a single PID that is destined to a single MID.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **tag** – **[in]** identifies a module instance matching the tag ID
- **payload** – **[in]** custom caller defined payload that gets sent to the module, payload structure shall be always according to format defined by SPF {MIID, PID, Size, Error Code, Variable payload}
- **payload_size** – **[in]** the size of the payload buffer

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_get_custom_config`(`gsl_handle_t graph_handle`, `uint8_t *payload`, `uint32_t size`)**

Get the configuration parameter for a specified graph, caller provides a payload.

**Parameters:**

- **graph_handle** – **[in]** returned from gsl_open
- **payload** – **[inout]** Buffer that contains the module ids and param ids along with empty areas that will be filled with parameter data
- **size** – **[inout]** holds the size of the client buffer passed in for payload. On return will hold actual bytes written.

**Returns:**

EOK on success, error code otherwise. Note that EOK does not mean we got valid data, it is possible that the buffer did not contain enough space for a given parameter. The client should check the error codes inside the buffer before reading the data.

**`int32_t gsl_get_tagged_custom_config`(`gsl_handle_t graph_handle`, `uint32_t tag`, `uint8_t *payload`, `uint32_t *size`)**

Get the configuration parameter for a specified graph from the module that is specified by a tag, caller provides a payload with the PIDs populated. GSL will populate the MIDS into the payload. LIMITATION: Only a single parameter on a single module can be looked up at a time.

**Parameters:**

- **graph_handle** – **[in]** returned from gsl_open
- **tag** – **[in]** tag used by GSL to lookup the MIDs
- **payload** – **[inout]** Buffer that contains param ids along with empty areas that will be filled with parameter data
- **size** – **[inout]** holds the size of the client buffer passed in for payload. On return will hold actual bytes written.

**Returns:**

EOK on success, error code otherwise. Note that EOK does not mean we got valid data, it is possible that the buffer did not contain enough space for a given parameter. The client should check the error codes inside the buffer before reading the data.

**`int32_t gsl_ioctl`(`gsl_handle_t graph_handle`, `enum gsl_cmd_id cmd_id`, `void *cmd_payload`, `size_t cmd_payload_sz`)**

Send commands to GSL for controlling Graphs in Spf.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **cmd_id** – **[in]** identifies the command
- **cmd_payload** – **[inout]** command specific parameters
- **cmd_payload_sz** – **[in]** size of cmd_payload

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_read`(`gsl_handle_t graph_handle`, `uint32_t tag`, `struct gsl_buff *buff`, `uint32_t *filled_size`)**

Receive data buffers from Spf.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **tag** – **[in]** used to identify the module in Spf to read buffers from
- **buff** – **[inout]** buffer where data will be copied to
- **filled_size** – **[out]** actual number of bytes filled into the buffer by GSL

**Returns:**

EOK on success, AR_EABORTED when buffer is not queued to spf because of graph close, stop, or flush (non-fatal error), error code otherwise

**`int32_t gsl_write`(`gsl_handle_t graph_handle`, `uint32_t tag`, `struct gsl_buff *buff`, `uint32_t *consumed_size`)**

Write data buffers to Spf.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **tag** – **[in]** used to identify the module in Spf to write buffers to
- **buff** – **[in]** buffer containing data that will be written
- **consumed_size** – **[out]** actual number of bytes consumed by GSL

**Returns:**

EOK on success, AR_EABORTED when buffer is not queued to spf because of graph close, stop, or flush (non-fatal error), error code otherwise

**`int32_t gsl_register_event_cb`(`gsl_handle_t graph_handle`, `gsl_cb_func_ptr cb`, `void *client_data`)**

Register an event callback function with Spf.

**Parameters:**

- **graph_handle** – **[in]** graph handle returned from gsl_open
- **cb** – **[in]** pointer to callback function
- **client_data** – **[in]** opaque data that will be passed to client in the callback

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_get_tagged_data`(`const struct gsl_key_vector *graph_key_vect`, `uint32_t tag`, `struct gsl_key_vector *tag_key_vect`, `uint8_t *payload`, `size_t *payload_size`)**

Query database for data associated with a given tag and tkv. This API is used to get spf module data in the form {IID, PID, Size, ErrorCode, variable length payload}.

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **tag** – **[in]** used to identify a certain capability
- **tag_key_vect** – **[in]** tag key vector used to identify a specific payload in acdb
- **payload** – **[inout]** pointer to a buffer where the payload will be copied to
- **payload_size** – **[inout]** holds the size of the client buffer passed in for payload and on return will hold the size of the actual data written to the buffer.

**Returns:**

EOK on success, error code otherwise. In-case the provided payload_size is not big enough to hold output data the error code AR_ENEEDMORE will be returned and payload_size will be set to expected size.

**`int32_t gsl_get_tagged_module_info`(`const struct gsl_key_vector *graph_key_vect`, `uint32_t tag`, `struct gsl_module_id_info **module_info`, `uint32_t *module_info_size`)**

Query database for module_iid to module_id mapping data.

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **tag** – **[in]** identifies a set of modules in ACDB that were tagged with with this tag by system designer
- **module_info** – **[out]** module info will be copied here. GSL dynamically allocates memory to hold module_info for the num_modules matching the tag. Client is responsible to free the memory after use.
- **module_info_size** – **[out]** holds the size of the data written to the module_info buffer

**Returns:**

EOK on success, error code otherwise.

**`int32_t gsl_get_tags_with_module_info`(`const struct gsl_key_vector *graph_key_vect`, `void *tag_module_info`, `size_t *tag_module_info_size`)**

Query database for all tags and corresponding module_iid and module_id mapping given a graph key vector.

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **tag_module_info** – **[inout]** tag module info will be copied here. GSL clients would call this API twice, first call tag_module_info is set to NULL and GSL fills only the size - *tag_module_info_size. GSL clients then allocate memory set it to tag_module_info and call the API again for the second time and the tag module info gets copied into that memory. The payload is in the format “struct gsl_tag_module_info”
- **tag_module_info_size** – **[inout]** used to provide the size (in bytes) of tag_module_info from client and output the expected size from gsl in-case size passed from client was too small

**Returns:**

EOK on success, error code otherwise.

**`int32_t gsl_enable_acdb_persistence`(`uint8_t enable_flag`)**

enable persistence for cals set to ACDB

**Parameters:**

**enable_flag** – **[in]** 1 means enable, 0 is disable

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_cal_data_to_acdb`(`const struct gsl_key_vector *graph_key_vect`, `const struct gsl_key_vector *cal_key_vect`, `uint8_t *payload`, `uint32_t payload_size`)**

Store custom calibration to ACDB.

see ACDB_CMD_SET_CAL_DATA in acdb.h for more documentation

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **cal_key_vect** – **[in]** tag key vector used to identify an entry in acdb
- **payload** – **[in]** pointer to a buffer containing custom calibration
- **payload_size** – **[in]** holds the size of the client buffer passed in for payload

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_get_cal_data_from_acdb`(`const struct gsl_key_vector *graph_key_vect`, `const struct gsl_key_vector *cal_key_vect`, `uint32_t num_modules`, `uint8_t *param_list`, `void *payload`, `uint32_t *payload_size`)**

Retrieve custom calibration from ACDB.

see ACDB_CMD_GET_CAL_DATA in acdb.h for more documentation

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **cal_key_vect** – **[in]** tag key vector used to identify an entry in acdb
- **num_modules** – **[in]** The number of module instances in the param_list
- **param_list** – **[in]** List of module instances plus their parameters to get data for
- **payload** – **[out]** pointer to a buffer of returned payload_size to hold returned calibration
- **payload_size** – **[inout]** holds the size of the client buffer passed in for payload. Client will call this API twice, once to fill this payload size and the second time to fill payload, with memory of returned payload_size allocated for payload

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_tag_data_to_acdb`(`const struct gsl_key_vector *graph_key_vect`, `uint32_t tag_id`, `const struct gsl_key_vector *tag_key_vect`, `uint8_t *payload`, `uint32_t payload_size`)**

Store custom tag to ACDB.

see ACDB_CMD_SET_TAG_DATA in acdb.h for more documentation

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **tag_id** – **[in]** tag ID to be set
- **tag_key_vect** – **[in]** tag key vector used to identify an entry in acdb
- **payload** – **[in]** pointer to a buffer containing custom tag data
- **payload_size** – **[in]** holds the size of the client buffer passed in for payload

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_get_tag_data_from_acdb`(`const struct gsl_key_vector *graph_key_vect`, `uint32_t tag_id`, `const struct gsl_key_vector *tag_key_vect`, `uint32_t num_modules`, `uint8_t *param_list`, `void *payload`, `uint32_t *payload_size`)**

Retrieve custom tag from ACDB.

see ACDB_CMD_GET_TAG_DATA in acdb.h for more documentation

**Parameters:**

- **graph_key_vect** – **[in]** graph key vector
- **tag_id** – **[in]** tag ID for data to retrieve
- **tag_key_vect** – **[in]** tag key vector used to identify an entry in acdb
- **num_modules** – **[in]** The number of module instances in the param_list
- **param_list** – **[in]** List of module instances plus their parameters to get data for
- **payload** – **[out]** pointer to a buffer of returned payload_size to hold returned tag data
- **payload_size** – **[inout]** holds the size of the client buffer passed in for payload. Client will call this API twice, once to fill this payload size and the second time to fill payload, with memory of returned payload_size allocated for payload

**Returns:**

EOK on success, error code otherwise

**`int32_t gsl_set_temp_path_to_acdb`(`uint32_t path_length`, `const char *temp_path`)**

Updates the read/write temporary path that AML uses for the reinit/delta persistence functionality.

**Parameters:**

- **cmd_id** – **[in]** Command ID is ACDB_CMD_SET_TEMP_PATH.
- **cmd** – **[in]** a null terminated char array of under 255 chars

**Returns:**

- AR_EOK — Command executed successfully. AR_EBADPARAM — Invalid input parameters were provided. AR_EFAILED — Command execution failed.

**`int32_t gsl_get_processed_buff_cnt`(`gsl_handle_t graph_handle`, `enum gsl_data_dir dir`, `uint32_t *cnt`)**

Get an ever increasing count of data buffers processed by GSL.

For playback case returns the number of buffers acked by Spf. For capture case returns the number of buffers received from Spf.

**Parameters:**

- **graph_handle** – **[in]** graph handle
- **dir** – **[in]** indicates whether to return the write or read buffer counts
- **cnt** – **[out]** An ever increasing count of buffers, the number wraps back to zero once it reaches SIZE_MAX

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_avail_buffer_size`(`gsl_handle_t graph_handle`, `enum gsl_data_dir dir`, `uint32_t *bytes`)**

Get the size of available buffer (in bytes) ready to be written (playback) / read (capture)

For playback case, returns the size of empty buffer (in bytes) for GSL clients to write. For capture case, returns the size of buffer (in bytes) that GSL clients can queue to SPF for read.

**Parameters:**

- **graph_handle** – **[in]** graph handle
- **dir** – **[in]** indicates whether to return write or read available buffer size
- **bytes** – **[out]** buffer size (in bytes) ready to be written (playback) / read (capture)

**Returns:**

AR_EOK in success, error code otherwise.

**`int32_t gsl_get_driver_data`(`const uint32_t module_id`, `const struct gsl_key_vector *key_vect`, `void *data_payload`, `uint32_t *data_payload_size`)**

Get driver data.

This API is to be called by GSL clients for querying any driver specific data that they stored in ACDB

**Parameters:**

- **module_id** – **[in]** client defined module_id against which data is stored in acdb
- **key_vect** – **[in]** OPTIONAL key vector used to look up data
- **data_payload** – **[in]** buffer where data will be returned, client is responsible to allocate memory for this buffer. If this is set to NULL the size of the output data will be returned in data_payload_size
- **data_payload_size** – **[inout]** on input it containes the size of data_payload, on output will have the size actually written

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_graph_tkvs`(`const struct gsl_key_vector *graph_key_vect`, `struct gsl_tag_key_vector_list *data_payload`)**

Get all tag/TKV variations.

Retrieves all tag and tag key vector variations which are defined for a given graph key vector in ACDB

**Parameters:**

- **graph_key_vect** – **[in]** GKV to find tag & TKV pairs in ACDB for
- **data_payload** – **[inout]** buffer where data will be returned, client is responsible to allocate memory for this buffer. If data_payload->key_vector_list is set to NULL, the size of the output data will be returned in data_payload->list_size.

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_graph_ckvs`(`const struct gsl_key_vector *graph_key_vect`, `struct gsl_key_vector_list *data_payload`)**

Get all CKVs for given GKV.

Queries for all SPF module calibration key vectors under a given graph key vector.

**Parameters:**

- **graph_key_vect** – **[in]** GKV to find CKVs in ACDB for
- **data_payload** – **[inout]** buffer where data will be returned, client is responsible to allocate memory for this buffer. If data_payload->key_vector_list is set to NULL, the size of the output data will be returned in data_payload->list_size.

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_driver_module_kvs`(`uint32_t driver_id`, `struct gsl_key_vector_list *data_payload`)**

Get KVs used by driver module.

Queries ACDB for all driver key vectors used by a particular driver module

**Parameters:**

- **driver_id** – **[in]** uint32_t identifying the driver module
- **data_payload** – **[inout]** buffer where data will be returned, client is responsible to allocate memory for this buffer. If data_payload->key_vector_list is set to NULL, the size of the output data will be returned in data_payload->list_size.

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_supported_gkvs`(`uint32_t *key_ids`, `const uint32_t num_key_ids`, `struct gsl_key_vector_list *data_payload`)**

Get all GKVs that contain the provided key IDs as a subset.

Queries ACDB for all graph key vectors that contain the provided key ids as a subset. A graph key vector supports certain capabiliies if it matches the key id subset. If the subset contains zero keys, this api will return all the graph key vectors defined in ACDB.

**Parameters:**

- **key_ids** – **[in]** pointer to the set of key IDs to query. Client-managed
- **num_key_ids** – **[in]** number of entries in key_ids
- **data_payload** – **[inout]** buffer where data will be returned, client is responsible to allocate memory for this buffer. If data_payload->key_vector_list is set to NULL, the size of the output data will be returned in data_payload->list_size.

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_get_graph_alias`(`const struct gsl_key_vector *graph_key_vect`, `char *alias`, `uint32_t *alias_len`)**

get human-readable alias for a GKV

Retrieves an alias of the graph key vector for readability. The alias includes the the usecase ID followed by a human readable graph key vector with names for keys and values. The string length is limited to 255 bytes.

API is to be called twice: once to get the size, and once to get the string.

**Parameters:**

- **graph_key_vect** – **[in]** GKV to find alias for
- **alias** – **[inout]** string containing the alias. Client is responsible to allocate memory for this buffer. If this is set to NULL the size of the output data will be returned in alias_len.
- **alias_len** – **[inout]** The length of the string including the null terminating character. on input it containes the allocated size of alias, on output will have the size actually written

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_add_database`(`struct gsl_acdb_data_files *acdb_data_files`, `struct gsl_acdb_file *writable_file_path`, `gsl_acdb_handle_t *acdb_handle`)**

add acdb database

Extends the database by adding database files (*.acdb and *.qwsp) at runtime.

**Parameters:**

- **acdb_data_files** – **[in]** A list of database file paths containing *.acdb and *.qwsp
- **writable_file_path** – **[in]** The delta data file path and temp files
- **[in/out]** – acdb_handle: A handle to the database provided

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_remove_database`(`gsl_acdb_handle_t acdb_handle`)**

remove acdb database

Shrinks the database by removing all data associated with the given database handle at runtime. This includes database files (*.qwsp and .acdb) and heap data

**Parameters:**

**acdb_handle** – **[in]** A handle to the database to remove

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_cshm_alloc`(`uint32_t size`, `gsl_cshm_info_t *info`)**

Allocates shared memory for external clients. Send APM_CMD_GLOBAL_SHARED_MEM_MAP_REGIONS commands to SPF to map allocated memory.

**Parameters:**

- **size** – **[in]** number of bytes to be allocated
- **[in/out]** – info: properties of shared memory to be allocated. fd and mem_id of allocated memory

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_cshm_dealloc`(`gsl_mem_id_t mem_id`)**

Deallocates shared memory for external clients. Send APM_CMD_GLOBAL_SHARED_MEM_UNMAP_REGIONS commands to SPF to unmap memory to be deallocated.

**Parameters:**

**mem_id** – **[in]** identifier to shared memory to be deallocated

**Returns:**

AR_EOK in success, error code otherwise

**`int32_t gsl_cshm_msg`(`gsl_mem_id_t mem_id`, `uint32_t offset`, `uint32_t length`, `uint32_t miid`, `uint32_t prop_flag`)**

Send notification to module running in SPF w.r.t particular operation on shared memory block. Operation is opaque to gsl. AR_SPF_MSG_GLOBAL_SH_MEM commands to SPF to forwards it to custom module.

**Parameters:**

- **mem_id** – **[in]** identifier to shared memory to be deallocated
- **offset** – **[in]** Offset (in bytes) from where the chunk of memory starts. This is relative to the beginning of the total shared memory allocated
- **length** – **[in]** Size of the chunk of memory.
- **miid** – **[in]** Module Instance ID of the module to which this call is intended for. In case of invalid/inactive miid, error is returned.
- **prop_flag** – **[in]** Flags to provide additional information for this call Bit 0 – Release memory Bit used to convey if client wants the module to release/stop using a chunk of previously informed memory. 0 – Default. Not a release message. 1 – Here, if length is zero, module is asked to release entire memory mapped to it with mem_id. If length is non-zero, the module is asked to release this chunck only.

**Returns:**

AR_EOK in success, error code otherwise

**`struct gsl_key_value_pair`**

*#include <gsl_intf.h>*a single entry in a key vector

Public Members

**`uint32_t key`**

key

**`uint32_t value`**

value

**`struct gsl_key_vector`**

*#include <gsl_intf.h>*a complete key vector

Public Members

**`uint32_t num_kvps`**

number of key value pairs

**`struct gsl_key_value_pair *kvp`**

vector of key value pairs

**`struct gsl_key_vector_array`**

*#include <gsl_intf.h>*a key vector with a zero sized array.

Public Members

**`uint32_t num_keys`**

number of keys

**`struct gsl_key_value_pair kvp[]`**

array of key value pairs.

**`struct gsl_key_vector_list`**

*#include <gsl_intf.h>*a key vector list

Public Members

**`uint32_t num_key_vectors`**

< number of key vectors in the key vector list size of the key vector list in bytes

**`uint32_t list_size`**

list of key vectors in the format of [#keys, kvPair+,…, #keys, kvPair+]

**`struct gsl_key_vector_array *key_vector_list`**

**`struct gsl_tag_key_vector`**

*#include <gsl_intf.h>*a tag key vector with a zero sized array

Public Members

**`uint32_t tag_id`**

< the module tag identifier number of keys

**`uint32_t num_keys`**

graph key value pair

**`struct gsl_key_value_pair kvp[]`**

**`struct gsl_tag_key_vector_list`**

*#include <gsl_intf.h>*a tag key vector list

Public Members

**`uint32_t num_key_vectors`**

< number of key vectors in the key vector list size of the key vector list in bytes

**`uint32_t list_size`**

list of key vectors in the format of [#keys, kvPair+,…, #keys, kvPair+]

**`struct gsl_tag_key_vector *key_vector_list`**

**`struct gsl_cmd_properties`**

*#include <gsl_intf.h>*Command payload for GSL_CMD_STOP ioctl. Properties used to match portions of the graph on which the command will be applied. This structure is used to match against the properties defined in gsl_subgraph_driver_props.h

Public Members

**`struct gsl_key_vector gkv`**

graph key vector to limit the scope of the operation

**`uint32_t property_id`**

property ID of the subgraph(s)

**`uint32_t num_property_values`**

number of values for the subgraph property ID

**`uint32_t *property_values`**

Pointer to property values[num_property_values]. If subgraph’s property value matches to any of the values in this set, the command will be carried out on that subgraph

**`struct gsl_cmd_configure_read_write_params`**

*#include <gsl_intf.h>*Cmd payload for GSL_CMD_CONFIGURE_WRITE_PARAMS and GSL_CMD_CONFIGURE_READ_PARAMS

Public Members

**`uint32_t buff_size`**

max number of bytes in a single buffer. Read/Write operations shall take buffers such that the size is a multiple of buff_size.

**`uint32_t num_buffs`**

number of buffers GSL will use for data exchange

**`uint32_t start_threshold`**

In case of write, wait till number of bytes received from client goes ABOVE this value before issuing START to SPF In case of read, wait till client has read this many bytes before issuing START to SPF Set to 0 for immediate start

**`uint32_t stop_threshold`**

TBD, currently not supported

**`uint32_t attributes`**

Bitfield used to indicate attributes for data transfers, below are the defined fields: data_mode(Bits 0,1,2): One of GSL_DATA_MODE_SHMEM, GSL_DATA_MODE_BLOCKING, GSL_DATA_MODE_NON_BLOCKING, GSL_DATA_MODE_PUSH_PULL, GSL_DATA_MODE_EXTERN_MEM datapath_setup(Bits 3,4): one of GSL_DATAPATH_SETUP_DEFAULT, GSL_DATAPATH_SETUP_ALLOC_SHMEM_ONLY, GSL_DATAPATH_SETUP_SPF_PROVISION_ONLY

**`uint32_t shmem_ep_tag`**

Optional tag used to queue read buffers before first gsl_graph_read When set to 0, buffers are not queued until first gsl_graph_read call

**`uint32_t platform_info`**

Optional field for passing platform specific data to GSL, this can be used for example to communicate some heap properties to osal layer. Must be set to 0 for clients that dont have any specific platform data.

**`uint32_t max_metadata_size`**

**`struct gsl_cmd_graph_select`**

*#include <gsl_intf.h>*Cmd payload for GSL_CMD_ADD_GRAPH and GSL_CMD_CHANGE_GRAPH

Public Members

**`struct gsl_key_vector graph_key_vector`**

Used to lookup the new graph. In the case of GSL_CMD_CHANGE_GRAPH the old graph will be torn down and the new graph will be setup. In the case of GSL_CMD_ADD_GRAPH the new graph is setup without tearing down the old graph

**`struct gsl_key_vector cal_key_vect`**

Used to lookup the calibration data that will be set on the new graph

**`struct gsl_cmd_remove_graph`**

*#include <gsl_intf.h>*Cmd payload for GSL_CMD_REMOVE_GRAPH

Public Members

**`struct gsl_key_vector graph_key_vector`**

Used to lookup the graph that will be removed

**`struct gsl_shmem_buf`**

*#include <gsl_intf.h>*Cmd payload for GSL_CMD_GET_WRITE_BUFF_INFO and GSL_CMD_GET_READ_BUFF_INFO. GSL writes to the payload created by the caller. Caller is responsible to provide the appropriate amount of memory to hold addresses for all buffers.

Public Members

**`uint8_t *addr`**

buffer address

**`uint64_t metadata`**

per buffer metadata

**`struct gsl_cmd_get_shmem_buf_info`**

*#include <gsl_intf.h>*Public Members

**`uint32_t size`**

buffer size, all buffers have the same size

**`uint32_t num_buffs`**

number of buffers

**`struct gsl_shmem_buf *buffs`**

list of buffs, containts num_buffs entries

**`struct gsl_cmd_register_custom_event`**

*#include <gsl_intf.h>*Cmd payload for GSL_CMD_REGISTER_CUSTOM_EVENT

Public Members

**`uint32_t module_instance_id`**

Valid instance ID of module

**`uint32_t event_id`**

Valid event ID of the module

**`uint32_t event_config_payload_size`**

Size of the event config data based upon the module_instance_id/event_id combination. > 0 bytes, in multiples of 4 bytes atleast

**`uint32_t is_register`**

1 - to register the event 0 - to de-register the event

**`uint8_t event_config_payload[]`**

module specifc event registration payload

**`struct gsl_acdb_file`**

*#include <gsl_intf.h>*Holds the path of single acdb file, this struct should be bitwise matching against what ACDB APIs expect

Public Members

**`uint32_t fileNameLen`**

Full file path name length

**`char fileName[GSL_MAX_LEN_OF_ACDB_FILENAME]`**

Array that holds the ACDB file path and name, which cannot exceed 256 characters, including the NULL-termiated character

**`struct gsl_acdb_data_files`**

*#include <gsl_intf.h>*Holds list of ACDB files, this struct should be bitwise matching against what ACDB APIs expect

Public Members

**`uint32_t num_files`**

Number of ACDB files

**`struct gsl_acdb_file acdbFiles[GSL_MAX_NUM_OF_ACDB_FILES]`**

Array of ACDB file full paths

**`struct gsl_init_data`**

*#include <gsl_intf.h>*Argument for gsl_init

Public Members

**`struct gsl_acdb_data_files *acdb_files`**

acdb files to pass to acdb, setting this NULL means acdb_addr will be used to acces the data

**`struct gsl_acdb_file *acdb_delta_file`**

path of acdb delta file

**`const void *acdb_addr`**

acdb image address

**`uint32_t max_num_ready_checks`**

indicates number of times GSL should check that spf is ready, gsl_init call is blocked until spf is ready. Spf readiness check is skipped in-case this field is set to 0

**`uint32_t ready_check_interval_ms`**

Amount of time in ms that GSL waits before re-attempting to check Spf readiness

**`struct gsl_extern_alloc_buff_info`**

*#include <gsl_intf.h>*Public Members

**`uint64_t alloc_handle`**

unique handle identifying external mem allocation

**`uint32_t alloc_size`**

size in bytes of the allocation

**`uint32_t offset`**

offset of data buffer within the allocation in bytes

**`struct gsl_buff`**

*#include <gsl_intf.h>*Struct for passing buffer info to gsl_read and gsl_write, also used as a return payload for GSL_EVENT_ID_READ_DONE and GSL_EVENT_ID_WRITE_DONE

Public Members

**`uint64_t timestamp`**

timestamp in micro-secs

**`uint32_t flags`**

bitmasked flags for e.g. GSL_BUFF_FLAG_EOS

**`uint32_t size`**

size of buffer in bytes

**`uint8_t *addr`**

data buffer. Not used in extern mem mode

**`uint32_t metadata_size`**

size of metadata buffer in bytes

**`uint8_t *metadata`**

metadata buffer. Can contain multiple metadata

**`struct gsl_extern_alloc_buff_info alloc_info`**

extern mem mode info

**`struct gsl_module_id_info_entry`**

*#include <gsl_intf.h>*Maps the modules instance id to module id for a single module

Public Members

**`uint32_t module_id`**

module id

**`uint32_t module_iid`**

globally unique module instance id

**`struct gsl_module_id_info`**

*#include <gsl_intf.h>*Used to return the module info data to client

Public Members

**`uint32_t num_modules`**

number entries in module list below

**`struct gsl_module_id_info_entry module_entry[]`**

module list

**`struct gsl_tag_module_info_entry`**

*#include <gsl_intf.h>*Structure mapping the tag_id to module info (mid and miid)

Public Members

**`uint32_t tag_id`**

tag id of the module

**`uint32_t num_modules`**

number of modules matching the tag_id

**`struct gsl_module_id_info_entry module_entry[]`**

module list

**`struct gsl_tag_module_info`**

*#include <gsl_intf.h>*Used to return tags and module info data to client given a graph key vector

Public Members

**`uint32_t num_tags`**

number of tags

**`uint8_t tag_module_entry[]`**

variable payload of type struct gsl_tag_module_info_entry

**`struct gsl_event_read_write_done_payload`**

*#include <gsl_intf.h>*Event payload passed to client with GSL_EVENT_ID_READ_DONE and GSL_EVENT_ID_WRITE_DONE events

Public Members

**`uint32_t tag`**

tag that was used to read/write this buffer

**`uint32_t status`**

data buffer status as defined in ar_osal_error.h

**`uint32_t md_status`**

meta-data status as defined in ar_osal_error.h

**`struct gsl_buff buff`**

buffer that was passed to gsl_read/gsl_write

**`struct gsl_event_eos_payload`**

*#include <gsl_intf.h>*Event payload passed to client with GSL_EVENT_ID_EOS

Public Members

**`uint32_t module_instance_id`**

module instance id from which the EOS event was raised, Invalid (0) when dropped.

**`enum gsl_eos_render_status_t render_status`**

Indicates whether the final sample was rendered or dropped

**`struct gsl_global_event_svc_dn_payload`**

*#include <gsl_intf.h>*Event payload passed to client with GSL_GLOBAL_EVENT_AUDIO_SVC_DN

Public Members

**`uint32_t num_handles`**

Number of graph handles

**`gsl_handle_t *handle_list`**

List of graph handles impacted by the audio svc going down, client is responsible to close these and re-open them once it receives the audio svc up notification

**`struct gsl_event_cb_params`**

*#include <gsl_intf.h>*data that will be passed to client in the event callback

Public Members

**`uint32_t source_module_id`**

identifies the module which generated event

**`uint32_t event_id`**

identifies the event, in case of GSL internal events it will hold a value from enum gsl_event_id

**`uint32_t event_payload_size`**

size of payload below

**`void *event_payload`**

payload associated with the event if any

**`struct gsl_cshm_info`**

*#include <gsl_intf.h>*Public Members

**`gsl_cshm_cache_type_t type`**

Cached or uncached memory type.

**`gsl_subsystem_t subsystem_mask`**

Allows rouing shared memory access across multiple DSPs.

**`int32_t flag`**

Flags for shared memory allocation.

**`uint64_t fd`**

File descriptor for mapped memory region.

**`gsl_mem_id_t mem_id`**

Unique GSL memory identifier.
