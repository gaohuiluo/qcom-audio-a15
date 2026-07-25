# 通用音频处理（CAPI）接口

- capi.h
- capi_types.h
- capi_events.h
- capi_properties.h

## capi.h

通用音频处理接口 v2 头文件。

本文件定义了一个通用的 C 接口，可以封装种类繁多的音频处理模块，使控制代码能够以统一的方式对待它们。

Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_t capi_t`**

**`typedef struct capi_vtbl_t capi_vtbl_t`**

**`typedef capi_err_t (*capi_get_static_properties_f)(capi_proplist_t *init_set_proplist, capi_proplist_t *static_proplist)`**

按如下方式查询属性：与实例无关的模块静态属性；以及可静态查询的属性集合中的任何属性。

设置或获取属性时发生的错误必须按以下方式处理：如果模块不支持该属性，则必须在错误码中设置 CAPI_EUNSUPPORTED 标志，并且该属性的 actual_data_len 字段必须置为零。其余属性仍必须继续处理（而不是遇到不支持的属性时就退出）。

**相关数据类型** capi_proplist_t

**详细说明** 此函数用于查询模块创建实例所需的内存。函数必须填充 static_proplist 中各属性的数据。

作为此函数的输入，客户端必须传入它传给 capi_init_f() 的属性列表。模块可以使用 init_set_proplist 中的属性值来计算其内存需求。

传给 capi_init_f() 调用的相同属性也会传给本函数，以便模块计算内存需求。

Error code — Failure（见相应章节）

**依赖项** 无。

**Param init_set_proplist:**

**[in]** 指向在 capi_init_f() 调用中传入的相同属性的指针。

**Param static_proplist:**

**[out]** 指向属性列表结构的指针。客户端填入其需要属性值的属性 ID。客户端还会为负载分配内存。模块必须在这块内存中填入相关信息。

**Return:**

CAPI_EOK — Success

**`typedef capi_err_t (*capi_init_f)(capi_t *_pif, capi_proplist_t *init_set_proplist)`**

实例化模块以建立虚函数表，同时分配模块所需的任何内存。

**相关数据类型** capi_t capi_proplist_t

**详细说明** 模块内部的状态必须同时初始化。

对于在 init_set_proplist 参数中传入的任何不支持的属性 ID，函数会打印一条消息并继续处理其他属性 ID。

除 CAPI_EOK 外，本函数返回的所有返回码都被视为 FATAL（致命）。

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。内存已由客户端根据 CAPI_INIT_MEMORY_REQUIREMENT 属性返回的大小分配。

**Param init_set_proplist:**

**[in]** 指向由服务设置、用于初始化过程中的属性的指针。

**Return:**

CAPI_EOK — Success

**`struct capi_vtbl_t`**

*#include <capi.h>*用于 CAPI 兼容对象的纯 C 实现的函数表。

对象必须在其实例结构中将指向函数表的指针作为第一个元素。此结构就是所有此类对象的函数表类型。

Public Members

**`capi_err_t (*process)(capi_t *_pif, capi_stream_data_t *input[], capi_stream_data_t *output[])`**

通用函数，处理所有输入端口上的输入数据，并在所有输出端口上提供输出。

**相关数据类型** capi_t capi_stream_data_t

**详细说明** 每次调用 capi_vtbl_t::process() 时，模块的行为取决于它为 CAPI_REQUIRES_DATA_BUFFERING 属性返回的值。关于该行为的说明，请参见 CAPI_REQUIRES_DATA_BUFFERING 的注释。

本函数中不允许有调试消息。

模块必须对以下各项进行 NULL 检查，并且仅在它们非 NULL 时才使用：input；output；capi_stream_data_t 中的 capi_buf_t；capi_buf_t 中的 data 缓冲区。

对于由 capi_vtbl_t::process() 调用引发的某些事件，不得填充输出缓冲区。请查看事件定义中的此项限制。

Error code — Failure（见相应章节）

**依赖项** 必须已使用 CAPI_INPUT_MEDIA_FORMAT 属性在每个输入端口上设置了有效的输入媒体类型。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Param input:**

**[inout]** 指向每个输入端口输入数据的指针数组。数组长度即输入端口数量。客户端使用 CAPI_PORT_NUM_INFO 属性设置输入端口数量。函数必须修改 actual_data_len 字段以指明消耗了多少字节。取决于 stream_data_version（在 capi_stream_flags_t 中），实际结构可以是 capi_stream_data_t 的某个版本（例如 capi_stream_data_t 或 capi_stream_data_v2_t）。input[] 中的某些元素可以为 NULL。当 CAPI_PORT_NUM_INFO 与当前活动端口之间不匹配时会出现这种情况。NULL 元素必须被忽略。

**Param output:**

**[out]** 指向每个输出端口输出数据的指针数组。客户端使用 CAPI_PORT_NUM_INFO 属性设置输出端口数量。函数设置 actual_data_len 字段以指明生成了多少字节。取决于 stream_data_version（在 capi_stream_flags_t 中），实际结构可以是 capi_stream_data_t 的某个版本（例如 capi_stream_data_t 或 capi_stream_data_v2_t）。对于单输入/单输出模块，框架通常在调用 process 之前用输入的标志、时间戳和元数据来分配输出的标志、时间戳和元数据。元数据仅在 capi_stream_data_v2_t 及以后版本中可用。如果模块存在延迟，它必须重置输出的 capi_stream_data_t（或 capi_stream_data_v2_t），并在延迟结束后再将其设置回来。output[] 中的某些元素可以为 NULL。当 CAPI_PORT_NUM_INFO 与当前活动端口之间不匹配时会出现这种情况。NULL 元素必须被忽略。

**Return:**

CAPI_EOK — Success

**`capi_err_t (*end)(capi_t *_pif)`**

释放模块分配的任何内存。

调用此函数后，_pif 不再是有效的 CAPI 对象。使用后不要再调用任何 CAPI 函数。

**相关数据类型** capi_t

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Return:**

CAPI_EOK — Success

**`capi_err_t (*set_param)(capi_t *_pif, uint32_t param_id, const capi_port_info_t *port_info_ptr, capi_buf_t *params_ptr)`**

根据唯一的参数 ID 设置参数值。

**相关数据类型** capi_t capi_port_info_t capi_buf_t

**详细说明** 参数指针的 actual_data_len 字段必须至少为参数结构的大小。因此，对于每个调参参数 ID，必须执行以下检查：

if (params_ptr->actual_data_len >= sizeof(gain_struct_t)) { : : } else { MSG_1(MSG_SSID_QDSP6, DBG_ERROR_PRIO,"CAPI Libname Set, Bad param size %lu",params_ptr->actual_data_len); return AR_ENEEDMORE; }

可选地，可以打印某些参数值以进行调参验证。

 在此代码示例中，gain_struct 仅为示例。请根据参数 ID 使用正确的结构。

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Param param_id:**

**[in]** 要设置其值的参数的 ID。

**Param port_info_ptr:**

**[in]** 指向本函数必须操作的端口信息的指针。如果未提供有效的端口索引，则说明端口索引对该 param_id 无关紧要、该 param_id 适用于所有端口，或者端口索引可能是参数负载的一部分。

**Param params_ptr:**

**[in]** 指向包含参数值的缓冲区的指针。缓冲区中数据的格式取决于具体实现。

**Return:**

CAPI_EOK — Success

**`capi_err_t (*get_param)(capi_t *_pif, uint32_t param_id, const capi_port_info_t *port_info_ptr, capi_buf_t *params_ptr)`**

根据唯一的参数 ID 获取参数值。

**相关数据类型** capi_t capi_port_info_t capi_buf_t

**详细说明** 参数指针的 max_data_len 字段必须至少为参数结构的大小。因此，对于每个调参参数 ID，必须执行以下检查。

if (params_ptr->max_data_len >= sizeof(gain_struct_t)) { : : } else { MSG_1(MSG_SSID_QDSP6, DBG_ERROR_PRIO,"CAPI Libname Get, Bad param size %lu",params_ptr->max_data_len); return AR_ENEEDMORE; }

返回之前，必须用写入缓冲区的字节数填充 actual_data_len 字段。

可选地，可以打印某些参数值以进行调参验证。

 在此代码示例中，gain_struct 仅为示例。请根据参数 ID 使用正确的结构。

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Param param_id:**

**[in]** 在本函数中传入其值的参数的参数 ID。例如：  CAPI_LIBNAME_ENABLE CAPI_LIBNAME_FILTER_COEFF

**Param port_info_ptr:**

**[in]** 指向本函数必须操作的端口信息的指针。如果端口索引无效，则说明端口索引对该 param_id 无关紧要、该 param_id 适用于所有端口，或者端口信息可能是参数负载的一部分。

**Param params_ptr:**

**[out]** 指向要填入参数值的缓冲区的指针。格式取决于具体实现。

**Return:**

CAPI_EOK — Success

**`capi_err_t (*set_properties)(capi_t *_pif, capi_proplist_t *proplist_ptr)`**

设置一组属性值。可选地，可以打印某些属性值以进行调试。

设置或获取属性时发生的错误必须按以下方式处理：如果模块不支持该属性，则必须在错误码中设置 CAPI_EUNSUPPORTED 标志，并且该属性的 actual_data_len 字段必须置为零。其余属性仍必须继续处理（而不是遇到不支持的属性时就退出）。

**相关数据类型** capi_t capi_proplist_t

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Param proplist_ptr:**

**[in]** 指向属性值列表的指针。

**Return:**

CAPI_EOK — Success

**`capi_err_t (*get_properties)(capi_t *_pif, capi_proplist_t *proplist_ptr)`**

获取一组属性值。

设置或获取属性时发生的错误必须按以下方式处理：如果模块不支持该属性，则必须在错误码中设置 CAPI_EUNSUPPORTED 标志，并且该属性的 actual_data_len 字段必须置为零。其余属性仍必须继续处理（而不是遇到不支持的属性时就退出）。

**相关数据类型** capi_t capi_proplist_t

Error code — Failure（见相应章节）

**依赖项** 无。

**Param _pif:**

**[inout]** 指向模块对象的指针。

**Param proplist_ptr:**

**[out]** 指向空结构列表的指针，这些结构必须根据所提供的属性 ID 填入相应的属性值。客户端必须填写这些结构的某些元素作为模块的输入。这些元素必须在结构定义中明确指出。

**Return:**

CAPI_EOK — Success

**`struct capi_t`**

*#include <capi.h>*虚函数表 capi_vtbl_t 的纯 C 接口封装。

此 capi_t 结构在调用者看来就是一个虚函数表。实例结构中的虚函数表后面还跟着其他结构元素，但这些对 CAPI 对象的使用者是不可见的。此 capi_t 结构是唯一公开可见的部分。

Public Members

**`const capi_vtbl_t *vtbl_ptr`**

指向虚函数表的指针。

## capi_types.h

本文件定义了通用音频处理接口的基本数据类型。

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Defines

**`CAPI_INVALID_VAL`**

Typedefs

**`typedef struct capi_buf_t capi_buf_t`**

**`typedef struct capi_data_format_header_t capi_data_format_header_t`**

**`typedef struct capi_port_info_t capi_port_info_t`**

**`struct capi_buf_t`**

*#include <capi_types.h>*包含传入 CAPI 函数的输入缓冲区、输出缓冲区、属性负载、事件负载以及参数。

Public Members

**`int8_t *data_ptr`**

指向原始数据的数据指针。对齐方式取决于原始数据的格式。

**`uint32_t actual_data_len`**

有效数据的长度（以字节为单位）。

对于输入缓冲区：@vtspstrbul 调用者用缓冲区中有效数据的字节数填充此字段。被调用者用它读取的数据字节数填充此字段。

对于输出缓冲区：@vtspstrbul 调用者不初始化此字段。被调用者用它填入的数据字节数填充此字段。

**`uint32_t max_data_len`**

缓冲区分配的总大小（以字节为单位）。

调用者始终填充此值，被调用者不会修改它。

**`union capi_stream_flags_t`**

*#include <capi_types.h>*随每个输入缓冲区传入、且必须由模块为每个输出缓冲区填充的标志。这些标志仅适用于与之关联的缓冲区。

marker_eos 和 end_of_frame 标志与元数据密切相关。实现 #INTF_EXTN_METADATA 的模块必须负责设置/清除/传播 marker_eos 和 end_of_frame。对于其他模块，框架负责处理 end_of_frame 和 marker_eos。如果框架处理 marker_eos/end_of_frame 的方式不能满足模块的需求，则该模块必须实现 #INTF_EXTN_METADATA 扩展并自行处理这些标志。

Public Members

**`uint32_t is_timestamp_valid`**

指定时间戳是否有效。

对于 SISO 模块，框架将时间戳及相关标志（timestamp valid、continue）从输入传播到输出。

@valuesbul 0 — Not valid 1 — Valid

**`uint32_t end_of_frame`**

指定缓冲区是否具有帧结束。

@valuesbul 0 — end_of_frame is not marked 1 — end_of_frame is marked

当设置了 end_of_frame 时，即使未达到阈值，模块也必须尝试处理给定的数据。否则，数据可能会被丢弃。

对于 raw-compressed-data，end_of_frame 通常表示缓冲区包含整数个已编码帧。

end_of_frame 也会在出现不连续（时间戳不连续、EOS）时被设置。

如果模块未实现 #INTF_EXTN_METADATA 扩展，则它不得写入此标志。

#INTF_EXTN_METADATA 中的框架回调不负责处理 end_of_frame。因此，支持 #INTF_EXTN_METADATA 扩展的模块也必须负责设置/清除/传播此标志。

**`uint32_t marker_eos`**

表示这是来自上游端口的最后一份有效数据。

EOS 有两种类型：flushing（冲刷）和 non-flushing（非冲刷）。此标志涉及冲刷型 EOS。

冲刷型 EOS 会将所有数据从模块中抽取出来。@vtspstrbul 对于解码器，这是通过在无输入的情况下反复调用模块来实现的。对于通用模块，这是通过推入相当于算法延迟量的零数据（零数据量 = 等于算法延迟量的零样本数）来实现的。多端口模块必须在内部负责处理冲刷。

非冲刷型 EOS 仅通过元数据来指示（不设置 marker_eos）。

marker_eos 伴随着 EOS 元数据。

典型的冲刷型 EOS 传播过程如下：在模块输入端给出 EOS。输入上设置 marker_eos 标志。EOS 元数据出现在输入端口的元数据列表中。EOS 经历算法延迟或缓冲延迟（如适用）。输入上设置 marker_eos 标志。EOS 元数据移入模块内部，输入端口的元数据列表被清空。EOS 到达输出、被销毁，或被转换为非冲刷型 EOS。marker_eos 标志移到输出。输入的 marker_eos 被清除，内部元数据列表被清空。当 EOS 移到输出时，输出上的 marker_eos 被设置，输出端口的元数据列表被填充。

在输入端口上，每当有新的 EOS 到达，或者上一个 EOS 因延迟而滞留在模块内部时，marker_eos 都会被设置。仅当输出列表中存在 EOS 元数据时，输出的 marker_eos 才会被设置。

对于未实现 INTF_EXTN_METADATA 的模块，marker_eos 的处理由框架负责。对于其他模块，包括 marker_eos 处理在内的 EOS 元数据传播，由 #INTF_EXTN_METADATA 中的 #intf_extn_param_id_metadata_handler_t::metadata_propagate() 负责。但对于创建/销毁/克隆等操作，模块必须自行设置/清除 marker_eos。

**`uint32_t marker_1`**

服务用来跟踪数据的数据标记 1。

模块必须将此标记从输入端口传播到从该端口获取输入的任何输出端口。

**`uint32_t marker_2`**

服务用来跟踪数据的数据标记 2。

模块必须将此标记从输入端口传播到从该端口获取输入的任何输出端口。

**`uint32_t marker_3`**

服务用来跟踪数据的数据标记 3。

模块必须将此标记从输入端口传播到从该端口获取输入的任何输出端口。

**`uint32_t erasure`**

显式地发出因下溢导致的擦除（erasure）信号。

@valuesbul 0 — No erasure 1 — Erasure

此标志在解码器中触发擦除处理。某些实现会在发出擦除信号时将此标志推给模块。

**`uint32_t stream_data_version`**

capi_stream_data_t 结构的版本。

版本在 capi_stream_version_t 中定义：@vtspstrbul 00 — capi_stream_data_t 01 — capi_stream_data_v2_t 10 — Reserved 11 — Reserved

**`uint32_t ts_continue`**

如果设置了 timestamp continue 标志，则不得读取 timestamp 字段。应基于先前设置的时间戳继续推算时间戳值。如果先前的时间戳值无效，则此标志不适用。如果 ts_continue 被复位且 ts_valid 被设置，则同步到输入时间戳。此字段应仅用于 raw compressed 数据格式。

@valuesbul 0 — ts_continue is set as FALSE 1 — ts_continue is set as TRUE

**`uint32_t reserved`**

保留供将来使用。对于输入端口，模块必须忽略此值。

**`struct capi_stream_flags_t`**

定义这些标志。

**`uint32_t word`**

完整的 32 位字，便于一次性读取或写入整个字。

**`struct capi_stream_data_t`**

*#include <capi_types.h>*用于一路流的数据结构。

Public Members

**`capi_stream_flags_t flags`**

指示流属性的标志。关于这些标志的更多信息，请参见 capi_stream_flags_t。

**`int64_t timestamp`**

第一个数据样本的时间戳，以微秒为单位。

时间原点不固定；必须从第一个缓冲区的时间戳推断出来。允许为负值。

**`capi_buf_t *buf_ptr`**

指向 CAPI 缓冲区元素数组的指针。

对于去交织非打包（deinterleaved unpacked）的未压缩数据，每个通道使用一个缓冲区。对于 CAPI_DEINTERLEAVED_RAW_COMPRESSED，使用媒体格式中指定数量的缓冲区。对于所有其他情况，仅使用一个缓冲区。

**`uint32_t bufs_num`**

buf_ptr 数组中缓冲区元素的数量。

对于去交织非打包的未压缩数据，此值等于流中的通道数。对于 CAPI_V2_DEINTERLEAVED_RAW_COMPRESSED，使用媒体格式中指定数量的缓冲区。对于所有其他情况，所有数据都放在一个缓冲区中，因此此字段设为 1。

**`struct capi_stream_data_v2_t`**

*#include <capi_types.h>*用于一路流的数据结构的版本 2。

Public Members

**`capi_stream_flags_t flags`**

指示流属性的标志。

关于这些标志的更多信息，请参见 capi_stream_flags_t。

**`int64_t timestamp`**

第一个数据样本的时间戳，以微秒为单位。

时间原点不固定；必须从第一个缓冲区的时间戳推断出来。允许为负值。

**`capi_buf_t *buf_ptr`**

指向 CAPI 缓冲区元素数组的指针。

对于去交织非打包的未压缩数据，每个通道使用一个缓冲区。对于 CAPI_V2_DEINTERLEAVED_RAW_COMPRESSED，使用媒体格式中指定数量的缓冲区。对于所有其他情况，仅使用一个缓冲区。

**`uint32_t bufs_num`**

buf_ptr 数组中缓冲区元素的数量。

对于去交织非打包的未压缩数据，此值等于流中的通道数。对于所有其他情况，所有数据都放在一个缓冲区中，因此此字段设为 1。

**`module_cmn_md_list_t *metadata_list_ptr`**

指向元数据列表的指针。此列表中的对象指针类型为 #module_cmn_md_t。

**`struct capi_data_format_header_t`**

*#include <capi_types.h>*传入模块的数据格式的头结构。此头之后紧跟相应的媒体格式负载。

Public Members

**`data_format_t data_format`**

指示数据的表示格式。负载的其余部分取决于数据格式。

**`struct capi_set_get_media_format_t`**

*#include <capi_types.h>*用于设置和获取媒体格式的头结构。此头之后紧跟相应的媒体格式负载。

Public Members

**`capi_data_format_header_t format_header`**

媒体格式的头。

**`struct capi_standard_data_format_t`**

*#include <capi_types.h>*用于 CAPI_FIXED_POINT、CAPI_FLOATING_POINT 和 CAPI_IEC61937_PACKETIZED 数据格式的负载结构。

Public Members

**`uint32_t bitstream_format`**

有效类型为 media_fmt_api.h 中定义的 MEDIA_FMT_ID_*。

**`uint32_t num_channels`**

通道数。

**`uint32_t bits_per_sample`**

用于存储每个样本的位数。

此值应解释为以位为单位的样本字长。例如，如果数据是打包在 24 位中的 24 位音频，则此值为 24。如果数据是打包在 32 位中的 24 位音频，则此值为

**`uint32_t q_factor`**

数据定点表示中的小数位数。

如果数据是浮点数，则此字段必须设为 CAPI_DATA_FORMAT_INVALID_VAL。

**`uint32_t sampling_rate`**

采样率，以每秒样本数为单位。

**`uint32_t data_is_signed`**

指定数据是否有符号。

@valuesbul 1 — Signed 0 — Unsigned

**`capi_interleaving_t data_interleaving`**

指示数据是否交织。此值对打包（packetized）数据无关紧要。

@valuesbul CAPI_INTERLEAVED CAPI_DEINTERLEAVED_PACKED CAPI_DEINTERLEAVED_UNPACKED

**`uint16_t channel_type[CAPI_MAX_CHANNELS]`**

针对每个 num_channels 的通道类型数组。

media_fmt_api.h 中定义的 PCM_CHANNEL_* 类型。

**`struct capi_standard_data_format_v2_t`**

*#include <capi_types.h>*用于 CAPI_FIXED_POINT、CAPI_FLOATING_POINT 和 CAPI_IEC61937_PACKETIZED 数据格式的媒体格式版本 2 负载。

Public Members

**`uint32_t minor_version`**

此负载的次版本号。

**`uint32_t bitstream_format`**

有效类型为 media_fmt_api.h 中定义的 MEDIA_FMT_ID_*。

**`uint32_t num_channels`**

通道数。

**`uint32_t bits_per_sample`**

用于存储每个样本的位数。

此值应解释为以位为单位的样本字长。例如，如果数据是打包在 24 位中的 24 位音频，则此值为 如果数据是打包在 32 位中的 24 位音频，则此值为 32。

**`uint32_t q_factor`**

数据定点表示中的小数位数。

如果数据是浮点数，则此字段必须设为 CAPI_DATA_FORMAT_INVALID_VAL。

**`uint32_t sampling_rate`**

采样率，以每秒样本数为单位。

**`uint32_t data_is_signed`**

指定数据是否有符号。

@valuesbul 1 — Signed 0 — Unsigned

**`capi_interleaving_t data_interleaving`**

指示数据是否交织。此值对打包数据无关紧要。

@valuesbul CAPI_INTERLEAVED CAPI_DEINTERLEAVED_PACKED CAPI_DEINTERLEAVED_UNPACKED

**`capi_channel_type_t channel_type[0]`**

通道类型负载为可变长度，取决于通道数。此负载包含每个 num_channels 的通道类型。

media_fmt_api.h 中定义的 PCM_CHANNEL_* 类型

**`struct capi_raw_compressed_data_format_t`**

*#include <capi_types.h>*用于 RAW_COMPRESSED 数据格式的负载头。

此结构之后紧跟着 media_fmt_api.h 或特定解码器 API 文件中为该特定数据格式定义的媒体格式结构。

Public Members

**`uint32_t bitstream_format`**

有效类型为 media_fmt_api.h 中定义的 MEDIA_FMT_ID_*。

**`struct capi_channel_mask_t`**

*#include <capi_types.h>*Public Members

**`uint32_t channel_mask_lsw`**

通道掩码的 LSW（低有效字）。

**`uint32_t channel_mask_msw`**

通道掩码的 MSW（高有效字）。

**`struct capi_deinterleaved_raw_compressed_data_format_t`**

*#include <capi_types.h>*用于 DEINTERLEAVED_RAW_COMPRESSED 数据格式的负载头。与 raw compressed 不同，此结构之后没有媒体格式特定的负载，只跟随通道掩码。

Public Members

**`uint32_t minor_version`**

此负载的次版本号。目前仅支持版本 1。

**`uint32_t bitstream_format`**

有效类型为 media_fmt_api.h 中定义的 MEDIA_FMT_ID_*。

**`uint32_t bufs_num`**

缓冲区数量。

**`struct capi_port_info_t`**

*#include <capi_types.h>*带有数据端口信息的负载结构头。

控制端口不使用此结构。控制端口通过接口扩展来处理。

Public Members

**[`bool_t`](args_arosal.md) `is_valid`**

指示 port_index 是否有效。

@valuesbul 0 — Not valid 1 — Valid

**[`bool_t`](args_arosal.md) `is_input_port`**

指示端口的类型。

@valuesbul TRUE — Input port FALSE — Output port

**`uint32_t port_index`**

标识端口。

索引值必须是从零开始的连续数字。输入端口和输出端口有各自独立的序列。例如，如果一个模块有三个输入端口和两个输出端口：@vtspstrbul 输入端口的索引值为 0、1 和 2。输出端口的索引值为 0 和 1。

当调用 capi_vtbl_t::process() 时：@vtspstrbul input[0] 中的数据对应输入端口 0。input[1] 中的数据对应输入端口 1。以此类推。输出端口 0 必须将数据填入 output[0]。输出端口 1 必须将数据填入 output[1]。以此类推。

## capi_events.h

本文件定义了模块可以使用 CAPI 接口触发的事件。

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_event_info_t capi_event_info_t`**

**`struct capi_event_info_t`**

*#include <capi_events.h>*包含关于事件的信息。

Public Members

**`capi_port_info_t port_info`**

触发此事件所针对的端口。

对于不特定于任何端口的事件，或者当负载包含端口信息时，将此字段设为无效值。

**`capi_buf_t payload`**

存放事件负载的缓冲区。

**`struct capi_event_KPPS_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_KPPS 事件的负载。

Public Members

**`uint32_t KPPS`**

模块的每秒千包（Kilo packets per second）需求。

**`struct capi_event_bandwidth_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_BANDWIDTH 事件的负载。

Public Members

**`uint32_t code_bandwidth`**

模块的代码带宽（以每秒字节数为单位）。

**`uint32_t data_bandwidth`**

模块的数据带宽（以每秒字节数为单位）。

**`struct capi_event_data_to_dsp_client_t`**

*#include <capi_events.h>*已弃用。参见 capi_event_data_to_dsp_client_v2_t。

用于 CAPI_EVENT_DATA_TO_DSP_CLIENT 事件的负载。

Public Members

**`uint32_t param_id`**

指示负载中所存在数据的类型。

**`uint32_t token`**

可选的令牌，用于指示附加信息，例如实例标识符。

**`capi_buf_t payload`**

包含负载的缓冲区。

一旦回调返回，即可安全地销毁或重用此缓冲区。

**`struct capi_event_dynamic_inplace_change_t`**

*#include <capi_events.h>*已弃用。

用于 CAPI_EVENT_DYNAMIC_INPLACE_CHANGE 事件的负载。

Public Members

**`uint32_t is_inplace`**

@valuesbul 0 — Indicates module changed to non-inplace Non zero — Indicates module changed to inplace

**`struct capi_event_data_to_dsp_client_v2_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_DATA_TO_DSP_CLIENT_V2 事件的负载。

Public Members

**`uint64_t dest_address`**

此事件要发送到的地址。必须使用注册期间提供的地址。

**`uint32_t token`**

可选的令牌，用于指示附加信息，例如实例标识符。

**`uint32_t event_id`**

标识事件。

**`capi_buf_t payload`**

包含负载的缓冲区。

一旦回调返回，即可安全地销毁或重用此缓冲区。

**`struct capi_event_data_to_dsp_service_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_DATA_TO_DSP_SERVICE 事件的负载。

Public Members

**`uint32_t param_id`**

指示负载中所存在数据的类型。

**`uint32_t token`**

可选的令牌，用于指示附加信息，例如实例标识符。

**`capi_buf_t payload`**

包含负载的缓冲区。

一旦回调返回，即可安全地销毁或重用此缓冲区。

**`struct capi_event_get_data_from_dsp_service_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_GET_DATA_FROM_DSP_SERVICE 事件的负载。

Public Members

**`uint32_t param_id`**

指示从框架所需数据的类型。

**`uint32_t token`**

可选的令牌，用于指示附加信息，例如实例标识符。

**`capi_buf_t payload`**

包含负载的缓冲区。

一旦回调返回，即可安全地销毁或重用此缓冲区。

**`struct capi_event_process_state_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_PROCESS_STATE 事件的负载。

Public Members

**[`bool_t`](args_arosal.md) `is_enabled`**

指定模块是否启用。如果模块被禁用，则不会调用其 capi_vtbl_t::process() 函数。

@valuesbul 0 — Disabled 1 — Enabled (Default)

**`struct capi_event_algorithmic_delay_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_ALGORITHMIC_DELAY 事件的负载。

Public Members

**`uint32_t delay_in_us`**

由模块引起的算法延迟，以微秒为单位。

此值**不得**包含缓冲延迟。否则，元数据偏移调整将被错误计算。

**`struct capi_event_headroom_t`**

*#include <capi_events.h>*已弃用。请改用控制链路。

用于 CAPI_EVENT_HEADROOM 事件的负载。

Public Members

**`uint32_t headroom_in_millibels`**

模块的余量（headroom）需求。默认值为零。

**`struct capi_port_data_threshold_change_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_PORT_DATA_THRESHOLD_CHANGE 事件的负载。

Public Members

**`uint32_t new_threshold_in_bytes`**

端口的阈值。

**`struct capi_library_base_t`**

*#include <capi_events.h>*作为每个库虚函数表第一个元素的函数指针。

Public Members

**`uint32_t (*get_interface_id)(void *obj_ptr)`**

返回与此对象所实现接口相关联的 ID。

**`void (*end)(void *obj_ptr)`**

反初始化对象并释放与之关联的内存。此调用之后，对象指针不再有效。

**`struct capi_event_get_library_instance_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_GET_LIBRARY_INSTANCE 事件的负载。

Public Members

**`uint32_t id`**

标识库。

**`void *ptr`**

指向库实例的指针。

**`struct capi_event_dlinfo_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_GET_DLINFO 事件的负载。

Public Members

**`uint32_t is_dl`**

指示 SO 文件是否为动态加载。

@valuesbul TRUE — File is dynamically loaded FALSE — Otherwise

此负载的其余部分仅在 SO 文件被加载时适用。

**`uint32_t load_addr_lsw`**

SO 文件加载到的物理地址的低 32 位。

**`uint32_t load_addr_msw`**

SO 文件加载到的物理地址的高 32 位。

由 load_addr_lsw 和 load_addr_msw 组成的 64 位数值必须按 32 字节对齐，并且必须已被预先映射。

**`uint32_t load_size`**

已加载 SO 文件的大小（以字节为单位）。

**`struct capi_event_hw_accl_proc_delay_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_HW_ACCL_PROC_DELAY 事件的负载。

Public Members

**`uint32_t delay_in_us`**

模块的硬件需求。默认值为 0。

**`struct capi_event_island_vote_t`**

*#include <capi_events.h>*用于 CAPI_EVENT_ISLAND_VOTE 事件的负载。

Public Members

**`uint32_t island_vote`**

置于 LPI 容器中的模块的孤岛（island）投票。

@valuesbul 0 — Vote for island entry 1 — Vote against island entry

## capi_properties.h

本文件定义了在通用音频处理接口中获取和设置属性所用的数据结构和 ID。

Copyright (c) Qualcomm Innovation Center, Inc. All Rights Reserved. SPDX-License-Identifier: BSD-3-Clause-Clear

Typedefs

**`typedef struct capi_prop_t capi_prop_t`**

**`typedef struct capi_param_persistence_info_t capi_param_persistence_info_t`**

**`struct capi_prop_t`**

*#include <capi_properties.h>*包含可发送给模块的属性。

属性用于通用的 set 和 get 命令，这些命令与底层模块无关。

Public Members

**`capi_property_id_t id`**

标识正在发送的属性。

**`capi_buf_t payload`**

负载缓冲区。

对于 capi_vtbl_t::set_properties() 调用，缓冲区必须包含与属性值对应的负载，并且必须足够大以容纳 set_properties() 调用的负载。

**`capi_port_info_t port_info`**

关于该属性所适用端口的信息。

如果该属性适用于任何端口，则必须在端口信息中将 is_valid 标志设为 FALSE。

**`struct capi_proplist_t`**

*#include <capi_properties.h>*包含 CAPI 属性列表。此结构可用于向模块发送属性列表或查询属性。

Public Members

**`uint32_t props_num`**

数组中元素的数量。

**`capi_prop_t *prop_ptr`**

CAPI 属性元素数组。

**`struct capi_init_memory_requirement_t`**

*#include <capi_properties.h>*用于 CAPI_INIT_MEMORY_REQUIREMENT 属性的负载。

Public Members

**`uint32_t size_in_bytes`**

内存量。

**`struct capi_stack_size_t`**

*#include <capi_properties.h>*用于 CAPI_STACK_SIZE 属性的负载。

Public Members

**`uint32_t size_in_bytes`**

栈的大小。

**`struct capi_max_metadata_size_t`**

*#include <capi_properties.h>*已弃用。参见 #module_cmn_md_t。

用于 CAPI_MAX_METADATA_SIZE 属性的负载。

Public Members

**`uint32_t output_port_index`**

此属性所适用的输出端口的索引。

**`uint32_t size_in_bytes`**

元数据的大小。

**`struct capi_is_inplace_t`**

*#include <capi_properties.h>*用于 CAPI_IS_INPLACE 属性的负载。

Public Members

**[`bool_t`](args_arosal.md) `is_inplace`**

指示模块是否能够进行原地（in-place）处理。

@valuesbul 0 — Does not support in-place processing 1 — Supports in-place processing

**`struct capi_requires_data_buffering_t`**

*#include <capi_properties.h>*用于 CAPI_REQUIRES_DATA_BUFFERING 属性的负载。

Public Members

**[`bool_t`](args_arosal.md) `requires_data_buffering`**

指定数据缓冲是否设为 TRUE。

**`struct capi_is_elementary_t`**

*#include <capi_properties.h>*用于 CAPI_IS_ELEMENTARY 属性的负载。

Public Members

**[`bool_t`](args_arosal.md) `is_elementary`**

指示模块是否可以作为基本（elementary）模块运行。

@valuesbul 0 — This module is an elementary module 1 — This module is not an elementary module

**`struct capi_min_port_num_info_t`**

*#include <capi_properties.h>*用于 CAPI_MIN_PORT_NUM_INFO 属性的负载。

Public Members

**`uint32_t num_min_input_ports`**

最小输入端口数。

**`uint32_t num_min_output_ports`**

最小输出端口数。

**`struct capi_event_callback_info_t`**

*#include <capi_properties.h>*用于 CAPI_EVENT_CALLBACK_INFO 属性的负载。

Public Members

**`capi_event_cb_f event_cb`**

用于触发事件的回调函数。

**`void *event_context`**

用作此回调函数上下文的不透明指针值。

**`struct capi_port_num_info_t`**

*#include <capi_properties.h>*用于 CAPI_PORT_NUM_INFO 属性的负载。

Public Members

**`uint32_t num_input_ports`**

输入端口数。

**`uint32_t num_output_ports`**

输出端口数。

**`struct capi_heap_id_t`**

*#include <capi_properties.h>*用于 CAPI_HEAP_ID 属性的负载。

Public Members

**`uint32_t heap_id`**

用于分配内存的堆 ID。

**`struct capi_metadata_t`**

*#include <capi_properties.h>*已弃用。参见 #module_cmn_md_t。

用于 CAPI_METADATA 属性的负载。

Public Members

**`capi_buf_t payload`**

包含元数据。

**`struct capi_port_data_threshold_t`**

*#include <capi_properties.h>*用于 CAPI_PORT_DATA_THRESHOLD 属性的负载。

Public Members

**`uint32_t threshold_in_bytes`**

输入或输出端口的阈值。

**`struct capi_output_media_format_size_t`**

*#include <capi_properties.h>*用于 CAPI_OUTPUT_MEDIA_FORMAT_SIZE 属性的负载。

Public Members

**`uint32_t size_in_bytes`**

输出端口媒体格式负载的大小。

**`struct capi_num_needed_framework_extensions_t`**

*#include <capi_properties.h>*用于 CAPI_NUM_NEEDED_FRAMEWORK_EXTENSIONS 属性的负载。

Public Members

**`uint32_t num_extensions`**

框架扩展的数量。

**`struct capi_framework_extension_id_t`**

*#include <capi_properties.h>*用于 CAPI_NEEDED_FRAMEWORK_EXTENSIONS 属性的负载。

Public Members

**`uint32_t id`**

标识框架扩展。

**`struct capi_log_code_t`**

*#include <capi_properties.h>*用于 CAPI_LOG_CODE 属性的负载。

Public Members

**`uint32_t code`**

用于记录模块数据的代码。

**`struct capi_session_identifier_t`**

*#include <capi_properties.h>*已弃用。用于 CAPI_SESSION_IDENTIFIER 属性的负载。

Public Members

**`uint16_t service_id`**

标识包含该模块的服务。

此 ID 是一个不透明值，不保证向后兼容。因此，模块不应基于此值来决定其行为。

**`uint16_t session_id`**

标识由 service_id 所指示服务内的会话。

模块可以将此值与 service_id 结合使用，以生成唯一 ID，用于在同一服务会话内建立模块间通信或用于调试消息。

**`struct capi_custom_property_t`**

*#include <capi_properties.h>*用于 CAPI_CUSTOM_PROPERTY 属性的负载。

Public Members

**`uint32_t secondary_prop_id`**

次级属性 ID，指示负载其余部分的格式。

此 ID 之后紧跟着由服务定义的自定义负载。如果模块不支持某个自定义属性或次级属性 ID，则它必须在 capi_prop_t 的 payload.actual_data_len 中返回 0。

**`struct capi_interface_extns_list_t`**

*#include <capi_properties.h>*用于 CAPI_INTERFACE_EXTENSIONS 属性的负载。

此结构之后紧跟着一个包含 num_extensions 个元素的 capi_interface_extn_desc_t 结构数组。

Public Members

**`uint32_t num_extensions`**

客户端正在查询的接口扩展的数量。客户端必须提供此值。

**`struct capi_interface_extn_desc_t`**

*#include <capi_properties.h>*一个包含 capi_interface_extns_list_t::num_extensions 个元素的数组中每个元素的数据类型（用于 CAPI_INTERFACE_EXTENSIONS 属性）。

Public Members

**`uint32_t id`**

标识正在查询的接口扩展。客户端必须提供此值。

**[`bool_t`](args_arosal.md) `is_supported`**

指示是否支持此扩展。

@valuesbul 0 — Not supported 1 — Supported

模块必须提供此值。

**`capi_buf_t capabilities`**

可选缓冲区，包含一个可用于进一步协商与此扩展相关能力的结构。

该结构在接口扩展文件中定义。如果它未在该文件中定义，则说明该接口扩展没有能力结构。

**`struct capi_register_event_to_dsp_client_t`**

*#include <capi_properties.h>*用于 CAPI_REGISTER_EVENT_DATA_TO_DSP_CLIENT_V2 事件的负载。

Public Members

**`uint32_t event_id`**

标识要注册的事件。

**[`bool_t`](args_arosal.md) `is_registered`**

指示是否存在已注册该事件的客户端。

@valuesbul TRUE — Event is registered FALSE — Event is not registered

**`struct capi_register_event_to_dsp_client_v2_t`**

*#include <capi_properties.h>*用于 CAPI_REGISTER_EVENT_DATA_TO_DSP_CLIENT_V2 事件的负载。

Public Members

**`uint64_t dest_address`**

此事件必须发送到的地址。

**`uint32_t token`**

触发此事件时要使用的令牌。

**`uint32_t event_id`**

标识要注册的事件。

**[`bool_t`](args_arosal.md) `is_register`**

指示是否存在已注册此事件的客户端。

@valuesbul 0 — FALSE (event is not registered) 1 — TRUE (event is registered)

**`capi_buf_t event_cfg`**

事件配置。数据根据事件 ID 进行解释。

**`struct capi_param_persistence_info_t`**

*#include <capi_properties.h>*CAPI_PARAM_PERSISTENCE_INFO 属性的负载头。此结构之后紧跟着参数 ID 负载。

Public Members

**[`bool_t`](args_arosal.md) `is_register`**

指示该属性用于内存的注册还是注销。

@valuesbul TRUE — Registration FALSE — Deregistration

**`capi_persistence_type_t mem_type`**

指示与后续参数 ID 负载关联的持久化内存的类型。

@valuesbul CAPI_PERSISTENT_MEM CAPI_GLOBAL_PERSISTENT

**`uint32_t param_id`**

标识参数。

**`struct capi_module_instance_id_t`**

*#include <capi_properties.h>*用于 CAPI_MODULE_INSTANCE_ID 属性的负载。

Public Members

**`uint32_t module_id`**

标识模块。

**`uint32_t module_instance_id`**

标识模块实例。

**`struct capi_logging_info_t`**

*#include <capi_properties.h>*用于 CAPI_LOGGING_INFO 属性的负载。

Public Members

**`uint32_t log_id`**

模块的有效日志 ID。

任何用此 ID 打印的消息都能唯一标识来自该模块此实例的消息。

**`uint32_t log_id_mask`**

在 log_id 字段中保留供模块修改的位。

模块可以在诸如 EOS 或 flush 等不连续期间使用这些位来更改日志 ID。

**`struct capi_module_version_info_t`**

*#include <capi_properties.h>*用于 #CAPI_MODULE_VERSION 属性的负载。

Public Members

**`uint16_t version_major`**

模块的主版本号

**`uint16_t version_minor`**

模块的次版本号
