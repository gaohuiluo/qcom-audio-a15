# Common Audio Processing (CAPI) Interfaces

- capi.h
- capi_types.h
- capi_events.h
- capi_properties.h

## capi.h

Common Audio Processing Interface v2 header file.

This file defines a generalized C interface that can wrap a wide variety of audio processing modules, so that they can be treated the same way by control code.

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_t capi_t`**

**`typedef struct capi_vtbl_t capi_vtbl_t`**

**`typedef capi_err_t (*capi_get_static_properties_f)(capi_proplist_t *init_set_proplist, capi_proplist_t *static_proplist)`**

Queries for properties as follows: Static properties of the module that are independent of the instance Any property that is part of the set of properties that can be statically queried

Errors that occur when setting or getting a property must be handled in the following way: If the property is not supported by the module, the CAPI_EUNSUPPORTED flag must be set in the error code and the actual_data_len field for that property must be set to zero. The rest of the properties must still be processed (rather than exiting when an unsupported property is encountered).   **Associated data types**capi_proplist_t

**Detailed description** This function is used to query the memory requirements of the module to create an instance. The function must fill in the data for the properties in the static_proplist.

As an input to this function, the client must pass in the property list that it passes to capi_init_f(). The module can use the property values in init_set_proplist to calculate its memory requirements.

The same properties that are sent to the module in the call to capi_init_f() are also sent to this function to enable the module to calculate the memory requirement.

Error code — Failure (see Section )

**Dependencies** None.

**Param init_set_proplist:**

**[in]** Pointer to the same properties that are sent in the call to capi_init_f().

**Param static_proplist:**

**[out]** Pointer to the property list structure. The client fills in the property IDs for which it needs property values. The client also allocates the memory for the payloads. The module must fill in the information in this memory.

**Return:**

CAPI_EOK — Success

**`typedef capi_err_t (*capi_init_f)(capi_t *_pif, capi_proplist_t *init_set_proplist)`**

Instantiates the module to set up the virtual function table, and also allocates any memory required by the module.

**Associated data types**capi_t capi_proplist_t

**Detailed description** States within the module must be initialized at the same time.

For any unsupported property ID passed in the init_set_proplist parameter, the function prints a message and continues processing other property IDs.

All return codes returned by this function, except CAPI_EOK, are considered to be FATAL.

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object. The memory has been allocated by the client based on the size returned in the CAPI_INIT_MEMORY_REQUIREMENT property.

**Param init_set_proplist:**

**[in]** Pointer to the properties set by the service to be used while initializing.

**Return:**

CAPI_EOK — Success

**`struct capi_vtbl_t`**

*#include <capi.h>*Function table for plain C implementations of CAPI-compliant objects.

Objects must have a pointer to a function table as the first element in their instance structure. This structure is the function table type for all such objects.

Public Members

**`capi_err_t (*process)(capi_t *_pif, capi_stream_data_t *input[], capi_stream_data_t *output[])`**

Generic function that processes input data on all input ports and provides output on all output ports.

**Associated data types**capi_t capi_stream_data_t

**Detailed description** On each call to capi_vtbl_t::process(), the behavior of the module depends on the value it returned for the CAPI_REQUIRES_DATA_BUFFERING property. For a description of the behavior, see the comments for CAPI_REQUIRES_DATA_BUFFERING.

No debug messages are allowed in this function.

Modules must make a NULL check for the following and use them only if they are not NULL: input output capi_buf_t in capi_stream_data_t data buffer in capi_buf_t

For some events that result from a capi_vtbl_t::process() call, the output buffer must not be filled. Check the event definition for this restriction.

Error code — Failure (see Section )

**Dependencies** A valid input media type must have been set on each input port using the CAPI_INPUT_MEDIA_FORMAT property.

**Param _pif:**

**[inout]** Pointer to the module object.

**Param input:**

**[inout]** Array of pointers to the input data for each input port. The length of the array is the number of input ports. The client sets the number of input ports using the CAPI_PORT_NUM_INFO property. The function must modify the actual_data_len field to indicate how many bytes were consumed. Depending on stream_data_version (in capi_stream_flags_t), the actual structure can be a version of capi_stream_data_t (like capi_stream_data_t or capi_stream_data_v2_t). Some elements of input[] can be NULL. This occurs when there is mismatch between CAPI_PORT_NUM_INFO and the currently active ports. NULL elements must be ignored.

**Param output:**

**[out]** Array of pointers to the output data for each output port. The client sets the number of output ports using the CAPI_PORT_NUM_INFO property. The function sets the actual_data_len field to indicate how many bytes were generated. Depending on stream_data_version (in capi_stream_flags_t), the actual structure can be a version of capi_stream_data_t (like capi_stream_data_t or capi_stream_data_v2_t). For single input/single output modules, the framework typically assigns the output flags, timestamp, and metadata with input flags, timestamp, and metadata before calling process. Metadata is only available in capi_stream_data_v2_t and later. If the module has delay, it must reset the output capi_stream_data_t (or capi_stream_data_v2_t) and set it back after the delay is over. Some elements of output[] can be NULL. This occurs when there is mismatch between CAPI_PORT_NUM_INFO and the currently active ports. NULL elements must be ignored.

**Return:**

CAPI_EOK — Success

**`capi_err_t (*end)(capi_t *_pif)`**

Frees any memory allocated by the module.

After calling this function, _pif is no longer a valid CAPI object. Do not call any CAPI functions after using it. **Associated data types**capi_t

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object.

**Return:**

CAPI_EOK — Success

**`capi_err_t (*set_param)(capi_t *_pif, uint32_t param_id, const capi_port_info_t *port_info_ptr, capi_buf_t *params_ptr)`**

Sets a parameter value based on a unique parameter ID.

**Associated data types**capi_t capi_port_info_t capi_buf_t

**Detailed description** The actual_data_len field of the parameter pointer must be at least the size of the parameter structure. Therefore, the following check must be performed for each tuning parameter ID:

if (params_ptr->actual_data_len >= sizeof(gain_struct_t)) { : : } else { MSG_1(MSG_SSID_QDSP6, DBG_ERROR_PRIO,"CAPI Libname Set, Bad param size %lu",params_ptr->actual_data_len); return AR_ENEEDMORE; }

Optionally, some parameter values can be printed for tuning verification.

 In this code sample, gain_struct is an example only. Use the correct structure based on the parameter ID.

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object.

**Param param_id:**

**[in]** ID of the parameter whose value is to be set.

**Param port_info_ptr:**

**[in]** Pointer to the information about the port on which this function must operate. If a valid port index is not provided, the port index does not matter for the param_id, the param_id is applicable to all ports, or the port index might be part of the parameter payload.

**Param params_ptr:**

**[in]** Pointer to the buffer containing the value of the parameter. The format of the data in the buffer depends on the implementation.

**Return:**

CAPI_EOK — Success

**`capi_err_t (*get_param)(capi_t *_pif, uint32_t param_id, const capi_port_info_t *port_info_ptr, capi_buf_t *params_ptr)`**

Gets a parameter value based on a unique parameter ID.

**Associated data types**capi_t capi_port_info_t capi_buf_t

**Detailed description** The max_data_len field of the parameter pointer must be at least the size of the parameter structure. Therefore, the following check must be performed for each tuning parameter ID.

if (params_ptr->max_data_len >= sizeof(gain_struct_t)) { : : } else { MSG_1(MSG_SSID_QDSP6, DBG_ERROR_PRIO,"CAPI Libname Get, Bad param size %lu",params_ptr->max_data_len); return AR_ENEEDMORE; }

Before returning, the actual_data_len field must be filled with the number of bytes written into the buffer.

Optionally, some parameter values can be printed for tuning verification.

 In this code sample, gain_struct is an example only. Use the correct structure based on the parameter ID.

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object.

**Param param_id:**

**[in]** Parameter ID of the parameter whose value is being passed in this function. For example:  CAPI_LIBNAME_ENABLE CAPI_LIBNAME_FILTER_COEFF

**Param port_info_ptr:**

**[in]** Pointer to the information about the port on which this function must operate. If the port index is invalid, either the port index does not matter for the param_id, the param_id is applicable to all ports, or the port information might be part of the parameter payload.

**Param params_ptr:**

**[out]** Pointer to the buffer to be filled with the value of the parameter. The format depends on the implementation.

**Return:**

CAPI_EOK — Success

**`capi_err_t (*set_properties)(capi_t *_pif, capi_proplist_t *proplist_ptr)`**

Sets a list of property values. Optionally, some property values can be printed for debugging.

Errors that occur when setting or getting a property must be handled in the following way: If the property is not supported by the module, the CAPI_EUNSUPPORTED flag must be set in the error code and the actual_data_len field for that property must be set to zero. The rest of the properties must still be processed (rather than exiting when an unsupported property is encountered).   **Associated data types**capi_t capi_proplist_t

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object.

**Param proplist_ptr:**

**[in]** Pointer to the list of property values.

**Return:**

CAPI_EOK — Success

**`capi_err_t (*get_properties)(capi_t *_pif, capi_proplist_t *proplist_ptr)`**

Gets a list of property values.

Errors that occur when setting or getting a property must be handled in the following way: If the property is not supported by the module, the CAPI_EUNSUPPORTED flag must be set in the error code and the actual_data_len field for that property must be set to zero. The rest of the properties must still be processed (rather than exiting when an unsupported property is encountered).   **Associated data types**capi_t capi_proplist_t

Error code — Failure (see Section )

**Dependencies** None.

**Param _pif:**

**[inout]** Pointer to the module object.

**Param proplist_ptr:**

**[out]** Pointer to the list of empty structures that must be filled with the appropriate property values, which are based on the property IDs provided. The client must fill some elements of the structures as input to the module. These elements must be explicitly indicated in the structure definition.

**Return:**

CAPI_EOK — Success

**`struct capi_t`**

*#include <capi.h>*Plain C interface wrapper for the virtual function table, capi_vtbl_t.

This capi_t structure appears to the caller as a virtual function table. The virtual function table in the instance structure is followed by other structure elements, but those are invisible to the users of the CAPI object. This capi_t structure is all that is publicly visible.

Public Members

**`const capi_vtbl_t *vtbl_ptr`**

Pointer to the virtual function table.

## capi_types.h

This file defines the basic data types for the Common Audio Processing Interface.

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`CAPI_INVALID_VAL`**

Typedefs

**`typedef struct capi_buf_t capi_buf_t`**

**`typedef struct capi_data_format_header_t capi_data_format_header_t`**

**`typedef struct capi_port_info_t capi_port_info_t`**

**`struct capi_buf_t`**

*#include <capi_types.h>*Contains input buffers, output buffers, property payloads, event payloads, and parameters that are passed into the CAPI functions.

Public Members

**`int8_t *data_ptr`**

Data pointer to the raw data. The alignment depends on the format of the raw data.

**`uint32_t actual_data_len`**

Length of the valid data (in bytes).

For input buffers: @vtspstrbul The caller fills this field with the number of bytes of valid data in the buffer. The callee fills this field with the number of bytes of data it read.

For output buffers: @vtspstrbul The caller leaves this field uninitialized. The callee fills it with the number of bytes of data it filled.

**`uint32_t max_data_len`**

Total allocated size of the buffer (in bytes).

The caller always fills this value, and the callee does not modify it.

**`union capi_stream_flags_t`**

*#include <capi_types.h>*Flags that are passed with every input buffer and must be filled by the module for every output buffer. These flags apply only to the buffer with which they are associated.

marker_eos and end_of_frame flags are closely associated with metadata. Modules that implement #INTF_EXTN_METADATA must take care of setting/clearing/propagating marker_eos and end_of_frame. For other modules, the framework takes care of end_of_frame and marker_eos. If the framework’s method of handling marker_eos/end_of_frame does not address a module’s requirements, the module must implement the #INTF_EXTN_METADATA extension and handle these flags.

Public Members

**`uint32_t is_timestamp_valid`**

Specifies whether the timestamp is valid.

For SISO modules the framework propagates timestamp and related flags (timestamp valid, continue) from input to output.

@valuesbul 0 — Not valid 1 — Valid

**`uint32_t end_of_frame`**

Specifies whether the buffer has an end of frame.

@valuesbul 0 — end_of_frame is not marked 1 — end_of_frame is marked

When end_of_frame is set, the modules must try to process given data even if the threshold is not met. Otherwise, data might be dropped.

For raw-compressed-data, end_of_frame usually indicates that the buffer has integral number of encoded frames.

end_of_frame is also set for discontinuities (timestamp discontinuity, EOS).

If a module does not implement the #INTF_EXTN_METADATA extension, then it must not write to this flag.

Framework callbacks in #INTF_EXTN_METADATA, don’t take care of end_of_frame. Therefore, modules that support the #INTF_EXTN_METADATA extension must also take care of setting/clearing/propagating of this flag.

**`uint32_t marker_eos`**

Indicates that this data is the last valid data from the upstream port.

There are two types of EOS, flushing and non-flushing. This flag pertains to flushing EOS.

Flushing EOS extracts all the data out of the modules. @vtspstrbul For decoders, this is achieved by repeatedly calling the module without input. For generic modules, this is achieved by pushing zeroes worth algorithm delay (zeroes worth = zero samples equal to the amount of algorithmic delay). Multi-port modules must take care of flushing internally.

Non-flushing EOS is indicated only through metadata (marker_eos is not set).

marker_eos is accompanied by EOS metadata.

Typical Flushing EOS propagation works as follows: EOS is given at the input of a module. marker_eos flag is set on the input. EOS metadata is present in the input port metadata list. EOS undergoes algorithmic or buffering delay (if applicable). marker_eos flag is set on the input. EOS metadata moves internal to the module and the input port metadata list is cleared. EOS goes to output, gets destroyed, or gets converted to non-flushing EOS. The marker_eos flag moves to output. Input marker_eos is cleared and the internal metadata list is cleared. In case EOS moves to output, marker_eos on output is set and the output port metadata list is populated.

On the input port, marker_eos is set whenever a new EOS arrives or when the previous EOS is stuck inside the module due to delays. Output marker_eos is set only when there is EOS metadata in the output list.

marker_eos handling is taken care of by the framework, for modules that don’t implement INTF_EXTN_METADATA. For others, EOS metdata propagation including marker_eos handling, is taken care of by #intf_extn_param_id_metadata_handler_t::metadata_propagate() in #INTF_EXTN_METADATA. However, for create/destroy/clone etc., the module must set/clear marker_eos.

**`uint32_t marker_1`**

Data marker 1 the service uses to track data.

The module must propagate this marker from the input port to any output port that gets input from this port.

**`uint32_t marker_2`**

Data marker 2 the service uses to track data.

The module must propagate this marker from the input port to any output port that gets input from this port.

**`uint32_t marker_3`**

Data marker 3 the service uses to track data.

The module must propagate this marker from the input port to any output port that gets input from this port.

**`uint32_t erasure`**

Explicitly signals erasure due to underflow.

@valuesbul 0 — No erasure 1 — Erasure

This flag triggers erasure handling in decoders. Some implementations push this flag to the modules while signaling erasure.

**`uint32_t stream_data_version`**

Version of the capi_stream_data_t structure.

Versions are defined in capi_stream_version_t: @vtspstrbul 00 — capi_stream_data_t 01 — capi_stream_data_v2_t 10 — Reserved 11 — Reserved

**`uint32_t ts_continue`**

If the timestamp continue flag is set, then the timestamp field must not be read. Timestamp values based on previously set timestamp must continue. If the previous timestamp value is invalid, then this flag doesn’t apply. If ts_continue is reset and ts_valid is set, sync to the input timestamp. This field should be used only for raw compressed data formats.

@valuesbul 0 — ts_continue is set as FALSE 1 — ts_continue is set as TRUE

**`uint32_t reserved`**

Reserved for future use. The module must ignore this value for input ports.

**`struct capi_stream_flags_t`**

Defines the flags.

**`uint32_t word`**

Entire 32-bit word for easy access to read or write the entire word in one shot.

**`struct capi_stream_data_t`**

*#include <capi_types.h>*Data structure for one stream.

Public Members

**`capi_stream_flags_t flags`**

Flags that indicate the stream properties. For more information on the flags, see capi_stream_flags_t.

**`int64_t timestamp`**

Timestamp of the first data sample, in microseconds.

The time origin is not fixed; it must be inferred from the timestamp of the first buffer. Negative values are allowed.

**`capi_buf_t *buf_ptr`**

Pointer to the array of CAPI buffer elements.

For deinterleaved unpacked uncompressed data, one buffer is to be used per channel. For CAPI_DEINTERLEAVED_RAW_COMPRESSED, as many buffers are used as specified in the media format. For all other cases, only one buffer is to be used.

**`uint32_t bufs_num`**

Number of buffer elements in the buf_ptr array.

For deinterleaved unpacked uncompressed data, this is equal to the number of channels in the stream. For CAPI_V2_DEINTERLEAVED_RAW_COMPRESSED, as many buffers are used as specified in the media format. For all other cases, all the data is put in one buffer, so this field is set to 1.

**`struct capi_stream_data_v2_t`**

*#include <capi_types.h>*Version 2 of the data structure for one stream.

Public Members

**`capi_stream_flags_t flags`**

Flags that indicate the stream properties.

For more information on the flags, see capi_stream_flags_t.

**`int64_t timestamp`**

Timestamp of the first data sample, in microseconds.

The time origin is not fixed; it must be inferred from the timestamp of the first buffer. Negative values are allowed.

**`capi_buf_t *buf_ptr`**

Pointer to the array of CAPI buffer elements.

For deinterleaved unpacked uncompressed data, one buffer is to be used per channel. For CAPI_V2_DEINTERLEAVED_RAW_COMPRESSED, as many buffers are used as specified in the media format. For all other cases, only one buffer is to be used.

**`uint32_t bufs_num`**

Number of buffer elements in the buf_ptr array.

For deinterleaved unpacked uncompressed data, this is equal to the number of channels in the stream. For all other cases, all the data is put in one buffer, so this field is set to 1.

**`module_cmn_md_list_t *metadata_list_ptr`**

Pointer to the list of metadata. The object pointer in this list is of type #module_cmn_md_t.

**`struct capi_data_format_header_t`**

*#include <capi_types.h>*Header structure for a data format that is passed into the module. Following this header is the appropriate media format payload.

Public Members

**`data_format_t data_format`**

Indicates the format in which the data is represented. The rest of the payload depends on the data format.

**`struct capi_set_get_media_format_t`**

*#include <capi_types.h>*Header structure used to set and get a media format. Following this header is the appropriate media format payload.

Public Members

**`capi_data_format_header_t format_header`**

Header of the media format.

**`struct capi_standard_data_format_t`**

*#include <capi_types.h>*Payload structure for the CAPI_FIXED_POINT, CAPI_FLOATING_POINT, and CAPI_IEC61937_PACKETIZED data formats.

Public Members

**`uint32_t bitstream_format`**

Valid types are MEDIA_FMT_ID_* as defined in media_fmt_api.h.

**`uint32_t num_channels`**

Number of channels.

**`uint32_t bits_per_sample`**

Number of bits used to store each sample.

This value should be interpreted as the sample word size in bits. For example, if the data is 24-bit audio packed in 24 bits, this value is 24. If the data is 24-bit audio packed in 32 bits, this value is

**`uint32_t q_factor`**

Number of fractional bits in the fixed point representation of the data.

If the data is floating point, this field must be set to CAPI_DATA_FORMAT_INVALID_VAL.

**`uint32_t sampling_rate`**

Sampling rate in samples per second.

**`uint32_t data_is_signed`**

Specifies whether data is signed.

@valuesbul 1 — Signed 0 — Unsigned

**`capi_interleaving_t data_interleaving`**

Indicates whether the data is interleaved. This value is not relevant for packetized data.

@valuesbul CAPI_INTERLEAVED CAPI_DEINTERLEAVED_PACKED CAPI_DEINTERLEAVED_UNPACKED

**`uint16_t channel_type[CAPI_MAX_CHANNELS]`**

Array of channel types for each num_channels.

PCM_CHANNEL_* types as defined in media_fmt_api.h.

**`struct capi_standard_data_format_v2_t`**

*#include <capi_types.h>*Media format version 2 payload for the CAPI_FIXED_POINT, CAPI_FLOATING_POINT, and CAPI_IEC61937_PACKETIZED data formats.

Public Members

**`uint32_t minor_version`**

Minor version for this payload.

**`uint32_t bitstream_format`**

Valid types are MEDIA_FMT_ID_* as defined in media_fmt_api.h.

**`uint32_t num_channels`**

Number of channels.

**`uint32_t bits_per_sample`**

Number of bits used to store each sample.

This value should be interpreted as the sample word size in bits. For example, if the data is 24-bit audio packed in 24 bits, this value is If the data is 24-bit audio packed in 32 bits, this value is 32.

**`uint32_t q_factor`**

Number of fractional bits in the fixed point representation of the data.

If the data is floating point, this field must be set to CAPI_DATA_FORMAT_INVALID_VAL.

**`uint32_t sampling_rate`**

Sampling rate in samples per second.

**`uint32_t data_is_signed`**

Specifies whether data is signed.

@valuesbul 1 — Signed 0 — Unsigned

**`capi_interleaving_t data_interleaving`**

Indicates whether the data is interleaved. This value is not relevant for packetized data.

@valuesbul CAPI_INTERLEAVED CAPI_DEINTERLEAVED_PACKED CAPI_DEINTERLEAVED_UNPACKED

**`capi_channel_type_t channel_type[0]`**

Channel type payload is of variable length and depends on the number of channels. This payload has channel types for each of the num_channels.

PCM_CHANNEL_* types as defined in media_fmt_api.h

**`struct capi_raw_compressed_data_format_t`**

*#include <capi_types.h>*Payload header for the RAW_COMPRESSED data format.

Following this structure is the media format structure for the specific data format as defined in media_fmt_api.h or specific decoder API file.

Public Members

**`uint32_t bitstream_format`**

Valid types are MEDIA_FMT_ID_* as defined in media_fmt_api.h.

**`struct capi_channel_mask_t`**

*#include <capi_types.h>*Public Members

**`uint32_t channel_mask_lsw`**

LSW of the channel mask.

**`uint32_t channel_mask_msw`**

MSW of the channel mask.

**`struct capi_deinterleaved_raw_compressed_data_format_t`**

*#include <capi_types.h>*Payload header for the DEINTERLEAVED_RAW_COMPRESSED data format. Unlike raw compressed, there is no media format specific payload following this struct, only channel mask follows.

Public Members

**`uint32_t minor_version`**

Minor version for this payload. Only version 1 supported currently.

**`uint32_t bitstream_format`**

Valid types are MEDIA_FMT_ID_* as defined in media_fmt_api.h.

**`uint32_t bufs_num`**

Number of buffers.

**`struct capi_port_info_t`**

*#include <capi_types.h>*Payload structure header with data port information.

Control ports do not use this structure. Control ports are handled through interface extensions.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_valid`**

Indicates whether port_index is valid.

@valuesbul 0 — Not valid 1 — Valid

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_input_port`**

Indicates the type of port.

@valuesbul TRUE — Input port FALSE — Output port

**`uint32_t port_index`**

Identifies the port.

Index values must be sequential numbers starting from zero. There are separate sequences for input and output ports. For example, if a module has three input ports and two output ports: @vtspstrbul The input ports have index values of 0, 1, and 2. The output ports have index values of 0 and 1.

When capi_vtbl_t::process() is called: @vtspstrbul Data in input[0] is for input port 0. Data in input[1] is for input port 1. And so on. Output port 0 must fill data into output[0]. Output port 1 must fill data into output[1]. And so on.

## capi_events.h

This file defines the events that can be raised by a module using the CAPI interface.

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_event_info_t capi_event_info_t`**

**`struct capi_event_info_t`**

*#include <capi_events.h>*Contains information about an event.

Public Members

**`capi_port_info_t port_info`**

Port for which this event is raised.

Set this field to an invalid value for events that are not specific to any port or if the payload contains the port information.

**`capi_buf_t payload`**

Buffer that holds the payload for the event.

**`struct capi_event_KPPS_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_KPPS event.

Public Members

**`uint32_t KPPS`**

Kilo packets per second requirement of the module.

**`struct capi_event_bandwidth_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_BANDWIDTH event.

Public Members

**`uint32_t code_bandwidth`**

Code bandwidth of the module (in bytes per second).

**`uint32_t data_bandwidth`**

Data bandwidth of the module (in bytes per second).

**`struct capi_event_data_to_dsp_client_t`**

*#include <capi_events.h>*Deprecated. See capi_event_data_to_dsp_client_v2_t.

Payload for the CAPI_EVENT_DATA_TO_DSP_CLIENT event.

Public Members

**`uint32_t param_id`**

Indicates the type of data that is present in the payload.

**`uint32_t token`**

Optional token that indicates additional information, such as an instance identifier.

**`capi_buf_t payload`**

Buffer that contains the payload.

This buffer can be safely destroyed or reused once the callback returns.

**`struct capi_event_dynamic_inplace_change_t`**

*#include <capi_events.h>*Deprecated.

Payload for the CAPI_EVENT_DYNAMIC_INPLACE_CHANGE event.

Public Members

**`uint32_t is_inplace`**

@valuesbul 0 — Indicates module changed to non-inplace Non zero — Indicates module changed to inplace

**`struct capi_event_data_to_dsp_client_v2_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_DATA_TO_DSP_CLIENT_V2 event.

Public Members

**`uint64_t dest_address`**

Address to which this event is to be sent. The address that was provided during registration must be used.

**`uint32_t token`**

Optional token that indicates additional information, such as an instance identifier.

**`uint32_t event_id`**

Identifies the event.

**`capi_buf_t payload`**

Buffer that contains the payload.

This buffer can be safely destroyed or reused once the callback returns.

**`struct capi_event_data_to_dsp_service_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_DATA_TO_DSP_SERVICE event.

Public Members

**`uint32_t param_id`**

Indicates the type of data that is present in the payload.

**`uint32_t token`**

Optional token that indicates additional information, such as an instance identifier.

**`capi_buf_t payload`**

Buffer that contains the payload.

This buffer can be safely destroyed or reused once the callback returns.

**`struct capi_event_get_data_from_dsp_service_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_GET_DATA_FROM_DSP_SERVICE event.

Public Members

**`uint32_t param_id`**

Indicates the type of data that is required from the framework.

**`uint32_t token`**

Optional token that indicates additional information, such as an instance identifier.

**`capi_buf_t payload`**

Buffer that contains the payload.

This buffer can be safely destroyed or reused once the callback returns.

**`struct capi_event_process_state_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_PROCESS_STATE event.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_enabled`**

Specifies whether the module is enabled. If a module is disabled, its capi_vtbl_t::process() function is not called.

@valuesbul 0 — Disabled 1 — Enabled (Default)

**`struct capi_event_algorithmic_delay_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_ALGORITHMIC_DELAY event.

Public Members

**`uint32_t delay_in_us`**

Algorithmic delay in microseconds caused by the module.

This value **must not** include a buffering delay. Otherwise, metadata offset adjustments will be calculated incorrectly.

**`struct capi_event_headroom_t`**

*#include <capi_events.h>*Deprecated. Use control links instead.

Payload for the CAPI_EVENT_HEADROOM event.

Public Members

**`uint32_t headroom_in_millibels`**

Headroom requirement of the module. The default is zero.

**`struct capi_port_data_threshold_change_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_PORT_DATA_THRESHOLD_CHANGE event.

Public Members

**`uint32_t new_threshold_in_bytes`**

Value of the threshold for a port.

**`struct capi_library_base_t`**

*#include <capi_events.h>*Function pointers that are the first element of every library virtual function table.

Public Members

**`uint32_t (*get_interface_id)(void *obj_ptr)`**

Returns the ID associated with the interface that this object implements.

**`void (*end)(void *obj_ptr)`**

De-initializes the object and frees the memory associated with it. The object pointer is not valid after this call.

**`struct capi_event_get_library_instance_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_GET_LIBRARY_INSTANCE event.

Public Members

**`uint32_t id`**

Identifies the library.

**`void *ptr`**

Pointer to the instance of the library.

**`struct capi_event_dlinfo_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_GET_DLINFO event.

Public Members

**`uint32_t is_dl`**

Indicates whether the SO file is dynamically loaded.

@valuesbul TRUE — File is dynamically loaded FALSE — Otherwise

The rest of this payload is applicable only if the SO file is loaded.

**`uint32_t load_addr_lsw`**

Lower 32 bits of the physical address where the SO file is loaded.

**`uint32_t load_addr_msw`**

Upper 32 bits of the physical address where the SO file is loaded.

The 64-bit number formed by load_addr_lsw and load_addr_msw must be 32-byte aligned and must have been previously mapped.

**`uint32_t load_size`**

Size (in bytes) of the loaded SO file.

**`struct capi_event_hw_accl_proc_delay_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_HW_ACCL_PROC_DELAY event.

Public Members

**`uint32_t delay_in_us`**

Hardware requirement of the module. Default value is 0.

**`struct capi_event_island_vote_t`**

*#include <capi_events.h>*Payload for the CAPI_EVENT_ISLAND_VOTE event.

Public Members

**`uint32_t island_vote`**

Island vote of the module placed in an LPI container.

@valuesbul 0 — Vote for island entry 1 — Vote against island entry

## capi_properties.h

This file defines the data structures and ids for getting and setting properties in the Common Audio Processing Interface.

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_prop_t capi_prop_t`**

**`typedef struct capi_param_persistence_info_t capi_param_persistence_info_t`**

**`struct capi_prop_t`**

*#include <capi_properties.h>*Contains properties that can be sent to a module.

Properties are used for generic set and get commands, which are independent of the underlying module.

Public Members

**`capi_property_id_t id`**

Identifies the property that is being sent.

**`capi_buf_t payload`**

Payload buffer.

The buffer must contain the payload corresponding to the property value for the capi_vtbl_t::set_properties() call, and it must be sufficiently large to contain the payload for the set_properties() call.

**`capi_port_info_t port_info`**

Information about the port for which the property is applicable.

If the property is applicable to any port, the is_valid flag must be set to FALSE in the port information

**`struct capi_proplist_t`**

*#include <capi_properties.h>*Contains a list of CAPI properties. This structure can be used to send a list of properties to the module or query for the properties.

Public Members

**`uint32_t props_num`**

Number of elements in the array.

**`capi_prop_t *prop_ptr`**

Array of CAPI property elements.

**`struct capi_init_memory_requirement_t`**

*#include <capi_properties.h>*Payload for the CAPI_INIT_MEMORY_REQUIREMENT property.

Public Members

**`uint32_t size_in_bytes`**

Amount of memory.

**`struct capi_stack_size_t`**

*#include <capi_properties.h>*Payload for the CAPI_STACK_SIZE property.

Public Members

**`uint32_t size_in_bytes`**

Size of the stack.

**`struct capi_max_metadata_size_t`**

*#include <capi_properties.h>*Deprecated. see #module_cmn_md_t.

Payload for the CAPI_MAX_METADATA_SIZE property.

Public Members

**`uint32_t output_port_index`**

Index of the output port for which this property applies.

**`uint32_t size_in_bytes`**

Size of the metadata.

**`struct capi_is_inplace_t`**

*#include <capi_properties.h>*Payload for the CAPI_IS_INPLACE property.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_inplace`**

Indicates whether a module is capable of doing in-place processing.

@valuesbul 0 — Does not support in-place processing 1 — Supports in-place processing

**`struct capi_requires_data_buffering_t`**

*#include <capi_properties.h>*Payload for the CAPI_REQUIRES_DATA_BUFFERING property.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `requires_data_buffering`**

Specifies whether data buffering is set to TRUE.

**`struct capi_is_elementary_t`**

*#include <capi_properties.h>*Payload for the CAPI_IS_ELEMENTARY property.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_elementary`**

Indicates whether the module can operate as an elementary module.

@valuesbul 0 — This module is an elementary module 1 — This module is not an elementary module

**`struct capi_min_port_num_info_t`**

*#include <capi_properties.h>*Payload for the CAPI_MIN_PORT_NUM_INFO property.

Public Members

**`uint32_t num_min_input_ports`**

Mininum number of input ports.

**`uint32_t num_min_output_ports`**

Mininum number of output ports.

**`struct capi_event_callback_info_t`**

*#include <capi_properties.h>*Payload for the CAPI_EVENT_CALLBACK_INFO property.

Public Members

**`capi_event_cb_f event_cb`**

Callback function used to raise an event.

**`void *event_context`**

Opaque pointer value used as the context for this callback function.

**`struct capi_port_num_info_t`**

*#include <capi_properties.h>*Payload for the CAPI_PORT_NUM_INFO property.

Public Members

**`uint32_t num_input_ports`**

Number of input ports.

**`uint32_t num_output_ports`**

Number of output ports.

**`struct capi_heap_id_t`**

*#include <capi_properties.h>*Payload for the CAPI_HEAP_ID property.

Public Members

**`uint32_t heap_id`**

Heap ID for allocating memory.

**`struct capi_metadata_t`**

*#include <capi_properties.h>*Deprecated. See #module_cmn_md_t.

Payload for the CAPI_METADATA property.

Public Members

**`capi_buf_t payload`**

Contains the metadata.

**`struct capi_port_data_threshold_t`**

*#include <capi_properties.h>*Payload for the CAPI_PORT_DATA_THRESHOLD property.

Public Members

**`uint32_t threshold_in_bytes`**

Threshold of an input or output port.

**`struct capi_output_media_format_size_t`**

*#include <capi_properties.h>*Payload for the CAPI_OUTPUT_MEDIA_FORMAT_SIZE property.

Public Members

**`uint32_t size_in_bytes`**

Size of the media format payload for an output port.

**`struct capi_num_needed_framework_extensions_t`**

*#include <capi_properties.h>*Payload for the CAPI_NUM_NEEDED_FRAMEWORK_EXTENSIONS property.

Public Members

**`uint32_t num_extensions`**

Number of framework extensions.

**`struct capi_framework_extension_id_t`**

*#include <capi_properties.h>*Payload for the CAPI_NEEDED_FRAMEWORK_EXTENSIONS property.

Public Members

**`uint32_t id`**

Identifies the framework extension.

**`struct capi_log_code_t`**

*#include <capi_properties.h>*Payload for the CAPI_LOG_CODE property.

Public Members

**`uint32_t code`**

Code for logging module data.

**`struct capi_session_identifier_t`**

*#include <capi_properties.h>*Deprecated. Payload for the CAPI_SESSION_IDENTIFIER property.

Public Members

**`uint16_t service_id`**

Identifies the service in which the module is contained.

This ID is an opaque value that is not guaranteed to be backward compatible. As such, modules are not to determine their behavior based on this value.

**`uint16_t session_id`**

Identifies the session within the service as indicated by service_id.

Modules can use this value together with service_id to generate unique IDs for setting up intermodule communication within the same service session or for debug messaging.

**`struct capi_custom_property_t`**

*#include <capi_properties.h>*Payload for the CAPI_CUSTOM_PROPERTY property.

Public Members

**`uint32_t secondary_prop_id`**

Secondary property ID that indicates the format of the rest of the payload.

Following this ID is the custom payload defined by the service. If a module does not support a custom property or a secondary property ID, it must return 0 in payload.actual_data_len of capi_prop_t.

**`struct capi_interface_extns_list_t`**

*#include <capi_properties.h>*Payload for the CAPI_INTERFACE_EXTENSIONS property.

Following this structure is an array of capi_interface_extn_desc_t structures with num_extensions elements.

Public Members

**`uint32_t num_extensions`**

Number of interface extensions for which the client is querying. The client must provide this value.

**`struct capi_interface_extn_desc_t`**

*#include <capi_properties.h>*Data type of each element in an array of capi_interface_extns_list_t::num_extensions elements (for the CAPI_INTERFACE_EXTENSIONS property).

Public Members

**`uint32_t id`**

Identifies the interface extension being queried. The client must provide this value.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_supported`**

Indicates whether this extension is supported.

@valuesbul 0 — Not supported 1 — Supported

The module must provide this value.

**`capi_buf_t capabilities`**

Optional buffer containing a structure that can be used for further negotiation of capabilities related to this extension.

The structure is defined in the interface extension file. If it is not defined in this file, the interface extension does not have a capabilities structure.

**`struct capi_register_event_to_dsp_client_t`**

*#include <capi_properties.h>*Payload for the CAPI_REGISTER_EVENT_DATA_TO_DSP_CLIENT_V2 event.

Public Members

**`uint32_t event_id`**

Identifies the event to be registered.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_registered`**

Indicates whether a registered client exists for the event.

@valuesbul TRUE — Event is registered FALSE — Event is not registered

**`struct capi_register_event_to_dsp_client_v2_t`**

*#include <capi_properties.h>*Payload for the CAPI_REGISTER_EVENT_DATA_TO_DSP_CLIENT_V2 event.

Public Members

**`uint64_t dest_address`**

Address to which this event must be sent.

**`uint32_t token`**

Token to be used when raising this event.

**`uint32_t event_id`**

Identifies the event to be registered.

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_register`**

Indicates whether a registered client exists for this event.

@valuesbul 0 — FALSE (event is not registered) 1 — TRUE (event is registered)

**`capi_buf_t event_cfg`**

Event configuration. Data is interpreted based on the event ID.

**`struct capi_param_persistence_info_t`**

*#include <capi_properties.h>*Payload header of the CAPI_PARAM_PERSISTENCE_INFO property. Following this structure is the parameter ID payload.

Public Members

**[`bool_t`](args_arosal.html#_CPPv46bool_t) `is_register`**

Indicates whether the property is intended for registration or deregistration of memory.

@valuesbul TRUE — Registration FALSE — Deregistration

**`capi_persistence_type_t mem_type`**

Indicates the type of persistence memory associated with the parameter ID payload that follows.

@valuesbul CAPI_PERSISTENT_MEM CAPI_GLOBAL_PERSISTENT

**`uint32_t param_id`**

Identifies the parameter.

**`struct capi_module_instance_id_t`**

*#include <capi_properties.h>*Payload for the CAPI_MODULE_INSTANCE_ID property.

Public Members

**`uint32_t module_id`**

Identifies the module.

**`uint32_t module_instance_id`**

Identifies the module instance.

**`struct capi_logging_info_t`**

*#include <capi_properties.h>*Payload for the CAPI_LOGGING_INFO property.

Public Members

**`uint32_t log_id`**

Valid log ID for the module.

Any message printed with this ID uniquely identifies messages from this instance of the module.

**`uint32_t log_id_mask`**

Bits reserved in the log_id field for the module to modify.

The module can use these bits for changing the log ID during a discontinuity such as EOS or flush.

**`struct capi_module_version_info_t`**

*#include <capi_properties.h>*Payload for the #CAPI_MODULE_VERSION property.

Public Members

**`uint16_t version_major`**

Major version of the module

**`uint16_t version_minor`**

Minor version of the module
