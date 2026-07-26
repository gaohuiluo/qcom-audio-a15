# Customize audio graph

Each audio use case is a graph with subgraphs of
a specific type. Each subgraph has one or more functional
software blocks (referred to as modules) that perform a specific
function.

## Audio graph terms

| **Use case** | A graph of modules from source endpoint(s) to sink endpoint(s) that meets the product defined use case. |
| --- | --- |
| **Graph** | A logical interpretation of a group of one or more subgraphs connected together to create a specific use case. |
| **Subgraph** | A logical abstraction for a group of modules that connect and are manipulated as a single entity. |
| **Container** | Object that allows the system designer to group and run audio processing modules together in a single software thread. |
| **Module** | The smallest independent processing unit in the signal processing framework. |
| **Key value (KV) pair** | The individual key and associated values in a key vector. For example, a key can be a sound device and a value can be headphone, speaker, or some other sound device. |
| **Key vector** | Uniquely identifies a graph or subgraph through a set of KV pairs. |
| **Graph key vector (GKV)** | GKV is a unique identifier that gets a graph, which is represented by KV pairs. The graph or system designer associates a set of unique <keys> and <values> when creating a subgraph from the QACT UI canvas. |
| **Calibration key vector (CKV)** | CKV is a unique identifier that gets calibration data, which is represented by KV pairs. The graph or system designer associates a set of unique <keys> and <values> when storing calibration data. |
| **Tag and tag key vector (TKV)** | A tag is an identifier that sets runtime parameters for one or more modules. It allows updating module configurations (for example, enabling/disabling features like echo cancellation or equalization) in a graph at runtime. |

## Graph segments

An audio use case has the following segments.

The front-end
represents stream and streamPP subgraphs, while the back-end
represents the per-stream per-device (PSPD), devicePP, and device subgraphs.

| **Stream** | Gives a data write/read interface and performs decoding and encoding of compressed data. |
| --- | --- |
| **StreamPP** | Has stream-based processing modules (for example, equalizer). |
| **PSPD** | Has a module to convert the stream media format to the device media format. |
| **DevicePP** | Has processing modules for sound device tuning. |
| **Device** | Hardware endpoint such as CodecDMA (SoundWire), I2S, or TDM port. |

Once a front-end connects to a back-end using a routing mixer control,
the full GKV forms by concatenating the subgraph GKVs and the CKVs
assigned using mixer controls. Upon opening the front-end PCM or compress
device, AGM invokes GSL APIs with concatenated GKVs and CKVs to set up
the graph in SPF and apply calibration. At the same time, AGM opens a
kernel PCM device corresponding to the connected back-ends to begin
audio peripheral setup.

## Sample audio graph

The following figure shows an example audio graph for a playback scenario.

![sample_audio_graph.svg](../images/agm-sample_audio_graph.svg)

*Sample audio graph for playback*

In this graph:

1. The stream subgraph has a write shared memory endpoint, PCM decoder, and PCM converter. The client passes PCM samples to write shared memory endpoint.
2. If conversion is necessary, the PCM converter converts PCM samples to a format supported by the stream-specific postprocessing modules.
3. Output of the stream subgraph is fed into the stream-device subgraph, which has the media format converter (MFC). MFC converts the stream-subgraph PCM to the device-subgraph PCM format.
4. After conversion, output of the stream-device subgraph is fed into the device PP subgraph for device-specific postprocessing. A mixer is placed at the beginning of subgraph to mix input streams.
5. Output of the devicePP subgraph is then fed into the device subgraph, which has a hardware endpoint module such as an I2S driver.

The following is the GKV for this example graph:

```xml
GKV1: <StreamRX1 KVs, StreamRX2 PP KVs, StreamRX1DeviceRX KVs, DeviceRX PP KVs, DeviceRX KVs>

GKV2: <StreamRX2 KVs, StreamRX2 PP KVs, StreamRX2DeviceRX KVs, DeviceRX PP KVs, DeviceRX KVs>
```

### Audio graph manager

The audio graph manager (AGM) gives interfaces to allow TinyALSA-based mixer controls and
PCM/compress plug-ins to interact and enable audio use cases.
AGM runs as part of the PipeWire service that runs in the user space.

AGM gives APIs for mixer plug-ins and PCM/compress APIs to set up
audio use cases. It maintains many ALSA clients to set up use cases.
AGM also manages front-end to back-end connections.

The following figure shows the AGM block at a high level.

![AGM_service_blocks.svg](../images/agm-AGM_service_blocks.svg)

*High-level AGM software block*

| Object | Description |
| --- | --- |
| **Session** | A session object is an audio playback or capture session. Invoking session-specific mixer controls or APIs creates sessions. Gives APIs for TinyALSA plug-ins to configure streams and manages state transitions of graph and device objects. |
| **Graph** | A graph object is an audio use case. Interacts with GSL to open, manage, and close graphs. Gives APIs for graph creation, manages graphs, and configures stream and device endpoints. |
| **Device** | A device object is an ALSA device from the ALSA sound card. Enumerates available audio interfaces and gives device APIs for transitioning device states. |

### AudioReach graph services

The AudioReach™ Signal Processing Framework graph services (ARGS) consists of the graph service layer
(GSL), generic packet router (GPR), and acdb management layer (AML). It
handles initialization and creation of graphs, and creation of
packets for sending series of commands to the SPF.

| Component | Description |
| --- | --- |
| **GSL** | The graph service layer (GSL) is a software driver for SPF which manages graphs, subgraphs, buffers, and configurations. Loads and initializes graphs using graph key vectors (GKVs). Handles data commands and SPF module calibration. |
| **GPR** | The generic packet router (GPR) routes audio message packets across SPF and the graph service library. Handles commands for constructing audio graphs and processing audio. |
| **AML** | The acdb management layer (AML) gives get/set APIs to get and adjust data in acdb files. Gives data abstractions and organization for how the audio driver and its components consume the calibration data. |

## Audio calibration database

acdb is a static database on the Apps processor. It has
all tuning/calibration parameters for the LPAI. The `*.acdb` file format
organizes calibration data for various audio modules for various use cases.

Edit this file format using QACT (a PC tool) and
place it on the device file system in the `/etc/acdbdata/` folder. During
use case initialization or device switch, the AML queries the acdb
database with a specified GKV and pushes the device calibration data to SPF.

### Signal processing framework

Signal processing framework (SPF) runs in the LPAI subsystem and performs audio data processing.

The following figure gives a high-level overview of the functional
blocks used in SPF.

![spf_blocks.svg](../images/agm-spf_blocks.svg)

*High-level SPF software block*

| Component | Description |
| --- | --- |
| **APM** | Audio processing manager (APM) sets up and manages the use case graphs in the SPF. It gives the standard APIs to the graph management library and APM client to set up and configure audio use cases. |
| **Modules** | A module is a functional block in the SPF. It performs real-time audio processing in the LPAI subsystem. |
| **Containers** | A container is a framework implementation that runs a group of data processing modules together in the same software thread. Each container runs in its own software thread. |
