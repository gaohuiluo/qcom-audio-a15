# Audio overview

The audio subsystem powered by low-power AI (LPAI) delivers voice UI and
audio experiences. It uses a dedicated hardware-based AI accelerator for
machine learning-based work.

![hw_sw_components.svg](../images/overview-hw_sw_components.svg)

*Audio component overview*

The audio system includes:

- **Application processor** – CPU that handles audio processing tasks. Tasks include:

   - Managing audio record and playback
   - Decoding audio formats
   - Using LPAI for postprocessing tasks
- **Low-Power AI (LPAI)** – Subsystem that runs audio playback/record and voice-activation (VA) algorithms. It integrates with a dedicated Qualcomm® Hexagon™ Processor (QDSP6) and a low-power island (LPI).
- **Audio codec** – Hardware that includes: These convert analog audio to digital, and vice versa.

   - Analog-to-Digital Converter (ADC)
   - Digital-to-Analog Converter (DAC)
- **Speaker AMP and microphone** – Devices that connect over I2S/TDM/SoundWire.

## Architecture

The following figure shows the high-level audio software architecture.

![architecture.svg](../images/overview-architecture.svg)

*High-level audio software architecture*

The following are the major audio software architecture components:

[PipeWire](https://docs.qualcomm.com/doc/80-70030-16/topic/enable-audio.html#enable-pipewire)

PipeWire is a multimedia server for Linux that routes audio between Apps and
hardware. It replaces PulseAudio, offering low-latency, secure, and
flexible media handling for applications.

[Platform Abstraction Layer (PAL)](https://docs.qualcomm.com/doc/80-70030-16/topic/pal.html#pal)

Provides higher-level audio-specific APIs to access the audio
hardware and drivers to enable audio features.

[Audio Graph Manager (AGM)](https://docs.qualcomm.com/doc/80-70030-16/topic/agm.html#agm)

Provides interfaces to allow TinyALSA-based mixer controls and
PCM/compressed plug-ins to interact and enable audio features.

[AudioReach Graph Service (ARGS)](https://docs.qualcomm.com/doc/80-70030-16/topic/agm.html#args)

Consists of the Graph Service Layer (GSL), Generic Packet Router (GPR),
and acdb Management Layer (AML) modules. Handles initialization and
creation of graphs, and creation of packets for sending a series of
commands to the signal processing framework (SPF).

[Audio calibration database (acdb)](https://docs.qualcomm.com/doc/80-70030-16/topic/agm.html#section-rhd-fg4-zbc)

Includes information about various audio use cases such as
graphs, module calibration data, etc. The Apps processor parses acdb
files to get the graph information used by SPF to
enable the use case.

[Signal Processing Framework (SPF)](https://docs.qualcomm.com/doc/80-70030-16/topic/agm.html#spf-sw)

Modular framework that runs on the LPAI DSP. It helps
set up, configure, and run signal processing modules for audio features.
