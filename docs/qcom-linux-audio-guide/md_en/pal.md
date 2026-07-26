# Customize at PAL level

## PipeWire PAL plug-in

The PipeWire PAL plug-in loads PAL. It allows the
client to configure the audio devices and invoke various audio use
cases.

The following are the components of the PipeWire PAL plug-in:

| **Card** | Represents a sound card, which is a group of supported profiles, ports, sinks, and sources. Card module uses include:  Load/unload PAL Create/free a port supported by PAL Create/free PAL card Create/free sinks or sources - Sinks are the playback path - Sources are the capture path |
| --- | --- |
| **Sink** | Configures the audio playback path. Sink module uses include:  Open/close a playback session based on the configuration specified by the module-pal-card Create/free the sink thread for writing data for a PAL playback session Set volume support Get latency support Routing support |
| **Source** | Configures the audio capture path.  Source module uses include:  Open/close a PAL record session based on the configuration specified by module-pal-card Create/free PA sources Create source thread for reading data from a PAL record session Routing support |

## PAL APIs

PAL provides higher-level audio APIs to access
audio hardware and drivers. This allows audio features
including:

- Audio playback and record in PCM and compressed formats with various pre/postprocessing modules. This includes latency and power-sensitive use cases.
- Hardware accelerated encoding/decoding of audio formats.

Clients can interface with PAL using various APIs for controlling and
configuring sessions and devices. PAL performs the following operations:

- Configures mixer controls to set up hardware codec devices and stream configurations
- Invokes TinyALSA APIs to open/start audio sessions

The PAL resource manager tracks all active sessions and devices to
enable concurrencies. It parses and loads configuration of the following
platform XML files:

- `Resource_manager.xml` – Device-to-backend mapping and policy making attributes
- `Card-defs.xml` – Virtual PCM and compress nodes, and their options

The PAL payload builder constructs the metadata
payload for use case graphs. For more information about graphs, see [Customize audio graphs](https://docs.qualcomm.com/doc/80-70030-16/topic/agm.html#customize-audio-graph).

PulseAudio uses the same PAL APIs for different audio use cases. Find the
source code for the PAL module at:

`build-qcom-wayland/workspace/sources/qcom-pal/opensource/arpal-lx`

The following file gives all APIs exposed by the PAL module:

`build-qcom-wayland/workspace/sources/qcom-pal/opensource/arpal-lx/inc/PalApi.h`

The following are common PAL APIs.

### pal_init

Initializes PAL, parses the related configuration files, and stores
them in a local structure for use.

```cpp
int32_t pal_init( )
```

**Parameters**

None

**Return value**

- 0 on success
- Error code on failure

### pal_deinit

De-initializes PAL and frees up the resources allocated during
initialization.

```java
void pal_deinit()
```

**Parameters**

None

**Return value**

None

### pal_stream_open

Opens a stream with the specified configuration such as source/sink
devices, media configuration, etc. Returns the stream handle upon
success.

```cpp
int32_t pal_stream_open(
     struct pal_stream_attributes *attributes,
     uint32_t no_of_devices,
     struct pal_device *devices,
     uint32_t no_of_modifiers,
     struct modifier_kv *modifiers,
     pal_stream_callback cb,
     uint64_t cookie,
     pal_stream_handle_t **stream_handle)
```

**Parameters**

| attributes | Valid stream attributes obtained from pal_stream_open. |
| --- | --- |
| no_of_devices | Number of audio devices with which to first start the stream. |
| devices | Array of pal_devices. Bases the size of the array on the number of devices specified by the client in no_of_devices. |
| no_of_modifiers | Number of modifiers. |
| modifiers | Array of modifiers. Modifiers add more key-value pairs. |
| cb | Callback function associated with the stream. This callback function notifies any event. |
| cookie | Client data associated with the stream. The callback function returns this cookie. |
| stream_handle | Updates with the valid stream handle if the operation is successful. |

**Return value**

- 0 on success
- Error code on failure

### pal_stream_start

Starts a stream.

```cpp
int32_t pal_stream_start(
     pal_stream_handle_t *stream_handle)
```

**Parameters**

| stream_handle | Valid stream handle from pal_stream_open. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

### pal_stream_read

Reads the audio buffer captured from the audio source device.

```cpp
ssize_t pal_stream_read(
     pal_stream_handle_t *stream_handle,
     struct pal_buffer *buf)
```

**Parameters**

| stream_handle | Valid stream handle from pal_stream_open. |
| --- | --- |
| buf | Pointer to pal_buffer that has audio samples and metadata. |

**Return value**

- Number of bytes read
- Error code on failure

### pal_stream_write

Writes the audio buffer for stream rendering over a sink device.

```cpp
ssize_t pal_stream_write(
     pal_stream_handle_t *stream_handle,
     struct pal_buffer *buf)
```

**Parameters**

| stream_handle | Valid stream handle from pal_stream_open. |
| --- | --- |
| buf | Pointer to pal_buffer that has audio samples and metadata. |

**Return value**

- Number of bytes written
- Error code on failure

### pal_stream_stop

Stops a stream.

```cpp
int32_t pal_stream_stop(
     pal_stream_handle_t *stream_handle)
```

**Parameters**

| stream_handle | Valid stream handle from pal_stream_open. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

### pal_stream_close

Closes a stream.

```cpp
int32_t pal_stream_close(
     pal_stream_handle_t *stream_handle)
```

**Parameters**

| stream_handle | Valid stream handle from pal_stream_open. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

## Configuration files

Configure audio use cases at the PAL level by using the `mixer_paths`, `resourcemanager`, and `usecasekvmanager` XML files.

The following table shows the configuration files for different hardware
versions:

| Variant | Sound card name | Conf file | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Core Kit (Qualcomm RB3 Platform) | qcm6490-rb3-snd-card | qcm6490-rb3-snd-card.conf | mixer_paths_qcm6490_rb3.xml | resourcemanager_qcm6490_rb3.xml |
| Vision Kit | qcm6490-vision-snd-card | qcm6490-vision-snd-card.conf | mixer_paths_qcm6490_vision.xml | resourcemanager_qcm6490_vision.xml |
| Video Collab Kit | qcm6490-vc-snd-card | qcm6490-vc-snd-card.conf | mixer_paths_qcm6490_vc.xml | resourcemanager_qcm6490_vc.xml |

| Variant | Sound card name | Conf file | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Core Kit (RB8) | qcs9075-rb8-snd-card | qcs9075-rb8-snd-card.conf | mixer_paths_qcs9075_rb8.xml | resourcemanager_qcs9075_rb8.xml |

| Variant | Sound card name | Conf file | mixer_paths.xml | ResourceManager.xml |
| --- | --- | --- | --- | --- |
| Dragonwing IQ-8275 Beta Evaluation Kit | qcs8300-ridesx-snd-card | qcs8300-ridesx-snd-card.conf | mixer_paths_qcs8300_ridesx.xml | resourcemanager_qcs8300_ridesx.xml |

### Customize mixer paths XML file

Mixer control is a control variable exposed from the ALSA mixer to the
user space. It allows the user space to access set and get functions and
pass parameters to the ALSA mixer.

For example, the following is the entry for enabling the mono speaker
device in the `mixer_path.xml` file. When playback triggers and the
device selected is a speaker, the following mixer controls run
with the help of the audio route helper class.

```xml
<path name="speaker">
<!--Mixer controls related to speaker need to be defined here-->
</path>
```

The platform uses the `mixer_paths_<sound-card-name>.xml` file as the mixer path.
This file is in the `/etc/` folder on the target.

### Customize resource manager XML file

The `Resourcemanager.xml` file includes all possible devices, use cases, and
combinations. It also includes other configurations, module
parameters, and global parameters.

The following is an example for a speaker device entry in the
resource manager XML file. It has all configurations for the
speaker device such as back-end name, channels, sample-rate, bit-width,
etc.

```xml
<out-device>
     <id>PAL_DEVICE_OUT_SPEAKER</id>
     <back_end_name>CODEC_DMA-LPAIF_WSA-RX-0</back_end_name>
     <max_channels>2</max_channels>
     <channels>2</channels>
     <samplerate>48000</samplerate>
     <bit_width>16</bit_width>
     <snd_device_name>speaker</snd_device_name>
</out-device>
```

### Customize usecasekvmanager XML file

The `Usecasekvmanager.xml` file has the GKV details for each use case. PAL uses this
XML file to get the KV configuration for each use case and
then uses that configuration to get graph information from
the acdb files. This file is in the `/etc` folder on the device.

The following is an example of one stream and device graph key vector
configuration.

**Stream KV**

```xml
<stream type="PAL_STREAM_LOW_LATENCY">
     <keys_and_values Direction="RX" Instance="1">
     <!-- STREAMRX - PCM_LL_PLAYBACK -->
     <graph_kv key="0xA1000000" value="0xA100000E"/>
     <!-- INSTANCE - INSTANCE_1 -->
     <graph_kv key="0xAB000000" value="0x1"/>
</keys_and_values>
```

**Device KV**

```xml
<!-- Speaker Device -->
<device id="PAL_DEVICE_OUT_SPEAKER">
     <keys_and_values>
     <!-- DEVICERX - SPEAKER -->
     <graph_kv key="0xA2000000" value="0xA2000001"/>
     </keys_and_values>
</device>
```

**DevicePP KV**

```xml
<!-- OUT Speaker DevicePPs -->
<devicepp id="PAL_DEVICE_OUT_SPEAKER">
<keys_and_values StreamType="PAL_STREAM_COMPRESSED,PAL_STREAM_LOW_LATENCY">
     <!-- DEVICERX - SPEAKER -->
     <graph_kv key="0xA2000000" value="0xA2000001"/>
     <!-- DEVICEPP_RX - DEVICEPP_RX_AUDIO_MBDRC -->
     <graph_kv key="0xAC000000" value="0xAC000002"/>
</keys_and_values>
```
