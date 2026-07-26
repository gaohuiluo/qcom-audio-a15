# Enable TinyALSA-based applications

TinyALSA is a library that wraps the ALSA kernel interface into APIs that
clients can invoke. It also gives a plug-in interface to emulate ALSA
APIs.

Find TinyALSA source code at:

`build-qcom-wayland/workspace/sources/tinyalsa` and

`build-qcom-wayland/workspace/sources/tinycompress`.

The following figure shows the TinyALSA plug-in architecture.

![tinyalsa_plugin_architecture.svg](../images/tinyalsa-tinyalsa_plugin_architecture.svg)

*TinyALSA plug-in architecture*

The ALSA framework in the kernel exposes card and device nodes for PCM,
compress, and mixer.

PCM, mixer, and compress plug-ins are TinyALSA plug-ins. They route all
PCM, mixer, and compress calls from the application to plug-in specific
implementation.

The plug-ins create a virtual sound card with PCM, compress, and mixer
nodes. Virtual nodes map to on-device `.so` files (dynamically
loadable shared objects).

The virtual sound card configuration is in
the `card-defs.xml` file. This file is in the `/etc/` folder
on the device.

## TinyALSA APIs

The following are common TinyALSA APIs. See the
[open source TinyALSA
documentation](https://github.com/tinyalsa/tinyalsa/blob/master/include/tinyalsa/pcm.h)
for a complete description of all APIs.

### pcm_open

Opens a PCM audio device for input and output operations.
Initializes a PCM device for communication, allowing
read/write operations in audio data.

```cpp
struct pcm *pcm_open(
     unsigned int card,
     unsigned int device,
     unsigned int flags,
     struct pcm_config *config)
```

**Parameters**

| card | Card number. |
| --- | --- |
| device | Device number in the chosen card. |
| flags | Flags to configure the PCM device. |
| config | Structure variable that specifies audio stream parameters. |

**Return value**

`pcm* handle`

### pcm_is_ready

Checks if the PCM device is ready for input and output operations.

```java
int pcm_is_ready(struct pcm *pcm)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |

**Return value**

- Non-zero if the PCM device is ready
- 0 if the PCM device isn’t ready

### pcm_prepare

Prepares audio device input and output operations.

```java
int pcm_prepare(
     struct pcm *pcm)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

### pcm_start

Starts the PCM audio device for input and output operations.

```java
int pcm_start(
     struct pcm *pcm)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

### pcm_write

Writes audio data to the audio PCM device. Takes audio data as
input and sends it to the PCM device for playback or processing.

```cpp
int pcm_write(
     struct pcm *pcm,
     const void *data,
     unsigned int count)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |
| data | Audio data to write. |
| count | Number of audio frames to write. |

**Return value**

- 0 on success
- Error code on failure

### pcm_read

Gets audio data from the PCM device, which allows the application
to capture audio data from a microphone.

```cpp
int pcm_read(
     struct pcm *pcm,
     void *data,
     unsigned int count)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |
| data | Audio data to read. |
| count | Number of audio frames to read. |

**Return value**

- 0 on success
- Error code on failure

### pcm_stop

Stops the PCM audio device from further input and output
operations.

```java
int pcm_stop(
     struct pcm *pcm)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

### pcm_close

Closes the PCM audio device. This releases the resources
associated with the PCM device and releases the memory.

```java
int pcm_close(
     struct pcm *pcm)
```

**Parameters**

| pcm | Pointer to the open PCM device. |
| --- | --- |

**Return value**

- 0 on success
- Error code on failure

## Configure TinyALSA

For audio use cases from TinyALSA, configure the virtual mixer
controls.

These controls, created by the mixer plug-in, set up audio use case
graphs and modules. Most are byte array-based and are configured using the
`mixer_ctl_set_array` API. Metadata (referred to as ‘PCM100 metadata’)
is set using key-value (KV) pairs. For implementation details, see the
`set_agm_audio_intf_metadata` API in `build-qcom-wayland/workspace/sources/qcom-agm/opensource/agm/plugins/tinyalsa/test/agmmixer.c`.

```cpp
/**
            * Key Vector pair
            */
            struct agm_key_value {
            uint32_t key; /**< key */
            uint32_t value; /**< value */
            };
            /*Sample allocation for the key value pair*/
            gkv = calloc(num_gkv, sizeof(struct agm_key_value));
            ckv = calloc(num_ckv, sizeof(struct agm_key_value));
```

Sample code for the TinyALSA-based agmplay and agmcap utilities can be
found at:

`build-qcom-wayland/workspace/sources/qcom-agm/opensource/agm/plugins/tinyalsa/test`.

To enable and execute audio use cases from TinyALSA:

1. Set the audio interface (backend) device configuration, including sample rate, channels, format, and data format.

   ```python
   'CODEC_DMA-LPAIF_WSA-RX-0 rate ch fmt' 48000 2 2(PCM_16)
   ```
2. Set the metadata, including graph keys, cal keys for the device, and DevicePP.

   ```python
   'CODEC_DMA-LPAIF_WSA-RX-0 metadata' bytes
   ```
3. Set the control to indicate that follow-on mixer configurations will set the metadata for the stream and StreamPP subgraphs. Zero indicates that subsequent commands are for the stream.

   ```python
   'PCM100 control' Zero
                       'PCM100 metadata' bytes
   ```
4. Set the control to indicate that follow on mixer configurations will set the metadata for the DevicePP and stream-device subgraphs. `CODEC_DMA-LPAIF_WSA-RX-0` indicates that the subsequent commands are for stream-device. `CODEC_DMA-LPAIF_WSA-RX-0` is one of the audio interfaces registered with the ALSA ASOC framework. A list of all audio interfaces can be found at `/proc/asound/pcm`.

   ```python
   'PCM100 control' CODEC_DMA-LPAIF_WSA-RX-0
                       'PCM100 metadata' bytes
   ```
5. Retrieve all tags, module ID, and instance IDs associated with a given session between the stream and audio interface.

   ```python
   'PCM100 getTaggedInfo' bytes
   ```
6. Set the control to indicate that follow on mixer configurations will set the parameters for modules on the stream subgraph.

   ```python
   'PCM100 control' Zero
                       'PCM100 setParam' bytes
   ```
7. Set the control to indicate that follow on mixer configurations will set the parameters for modules on the StreamDevice and DevicePP subgraphs.

   ```python
   'PCM100 control' CODEC_DMA-LPAIF_WSA-RX-0
                       'PCM100 setParam' bytes
   ```
8. Connect the frontend (stream) with the backend (codec/audio interface).

   ```python
   'PCM100 connect'CODEC_DMA-LPAIF_WSA-RX-0
   ```
9. Open the PCM device.

   ```
   pcm_open
   ```
10. Prepare the audio device for input and output operations.

   ```
   pcm_prepare
   ```
11. Start the PCM audio device for input and output operations.

   ```
   pcm_start
   ```
12. Write and read audio data from the audio PCM device.

   ```
   pcm_write/pcm_read
   ```
13. Stop the PCM device.

   ```
   pcm_stop
   ```
14. Close the PCM audio device.

   ```
   pcm_close
   ```

All mixer controls for a virtual device can be fetched using:

```java
ssh root@ip-addr
```

```css
systemctl stop pipewire
```

```python
tinymix set -D 100
```
