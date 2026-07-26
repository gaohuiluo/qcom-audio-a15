# Troubleshoot audio

This section gives commands for audio logging and debugging.

## Capture logs

User space and kernel audio driver logs can help find issues.

| **User space logs** | To capture user space logs: ssh root@ip-addr mount -o remount,rw / cat /var/log/user.log   See [User space logs](https://docs.qualcomm.com/doc/80-70030-12/topic/userspace_logs.html) for more instructions. |
| --- | --- |
| **Kernel audio driver logs** | To capture kernel logs: ssh root@ip-addr dmesg     To disable kernel logs in a specific file: echo -n "file <filename> -p" > /sys/kernel/debug/dynamic_debug/control |
| **Dynamic kernel logs** | Dynamic logging is disabled by default. To enable it, add the `CONFIG_DYNAMIC_DEBUG` kernel configuration, recompile, and re-flash the device.  To enable audio dynamic kernel logs: ssh root@ip-addr mount -o rw,remount / mount -t debugfs none /sys/kernel/debug echo -n "file <filename> +p" > /sys/kernel/debug/dynamic_debug/control    See [Enable dynamic debug](https://docs.qualcomm.com/doc/80-70030-12/topic/enable_kernel_debugging.html#enable-dynamic-debug) for more instructions. |

## Analyze logs

Analyze user space and kernel audio driver logs for playback and record
use cases.

### Playback logs

The following log snippet shows the information collected for the
playback use case.

```cpp
//Open Low latency Playback stream. Details of each stream type can be found at sources/audio/opensource/arpal-lx/inc/PalDefs.h
2022-04-28T18:02:08.748280+00:00 pipewire: pal_stream_open: 224: Enter, stream type:1

//Verify the backend device, sample rate, bitwidth, channels etc
2022-04-28T18:02:08.748627+00:00 pipewire: setDeviceMediaConfig: 1056: CODEC_DMA-LPAIF_WSA-RX-0 rate ch fmt data_fmt 48000 2 2 1

//Start playback stream
2022-04-28T18:02:08.751947+00:00 pipewire: pal_stream_start: 338: Enter. Stream handle 0xffff94001040K

//Map the metadata with kvh2xml.h file for playback use case details.
2022-04-28T18:02:08.853157+00:00 pipewire: metadata_print: 82 key:0xa1000000, value:0xa100000e//PCM_LL_PLAYBACK
2022-04-28T18:02:08.853395+00:00 pipewire: metadata_print: 82 key:0xab000000, value:0x1
2022-04-28T18:02:08.853660+00:00 pipewire: metadata_print: 82 key:0xa2000000, value:0xa2000001//Speaker
2022-04-28T18:02:08.853881+00:00 pipewire: metadata_print: 82 key:0xac000000, value:0xac000002//DEVICEPP_RX_AUDIO_MBDRC

//Verify the graph opened for playback use case
2022-04-28T18:02:08.856934+00:00 pipewire: print_graph_alias: 2334 GKV Alias 142 | StreamRX_PCM_LL_Playback_DeviceRX_Speaker_Instance_Instance_1_DevicePP_Rx_Audio_MBDRC
//graph_open called
2022-04-28T18:02:08.859509+00:00 pipewire: graph_open: 709 graph_handle 0x47534c

//Configure hardware endpoint module
2022-04-28T18:02:08.864386+00:00 pipewire: configure_hw_ep_media_config: 636 entry mod tag c0000004 miid 43b1 mid 7001023
2022-04-28T18:02:08.864495+00:00 pipewire: configure_hw_ep_media_config: 664 rate 48000 bw 16 ch 2, data_fmt 1
2022-04-28T18:02:08.864603+00:00 pipewire: configure_hw_ep_media_config: 676 exit, ret 0

//graph_start entry
2022-04-28T18:02:08.867234+00:00 pipewire: graph_start: 899 entry graph_handle 0x47534c
//Stream started
2022-04-28T18:02:08.867864+00:00 pipewire: pal_stream_start: 387: Exit. status 0

//graph_stop entry
2022-04-28T18:02:25.037338+00:00 pipewire: graph_stop: 928 entry graph_handle 0x47534c
//Stop the PAL stream once playback completes
2022-04-28T18:02:25.039923+00:00 pipewire: pal_stream_stop: 441: Exit. status 0

//graph_close entry
2022-04-28T18:02:25.050944+00:00 pipewire: graph_close: 762 entry handle 0x47534c
//Close the PAL stream
2022-04-28T18:02:25.054510+00:00 pipewire: pal_stream_close: 322: Exit. status 0
```

### Record logs

The following log snippet shows the information collected for the
record use case.

```cpp
//Open Recording stream for PAL_STREAM_RAW. Details of stream type can be found at sources/audio/opensource/arpal-lx/inc/PalDefs.h
Apr 29 09:23:11 pipewire[862]: pal_stream_open: 224: Enter, stream type:9

//Verify the backend device, sample rate, bitwidth, channels etc
Apr 29 09:23:11 pipewire[862]: setDeviceMediaConfig: 1056: CODEC_DMA-LPAIF_VA-TX-0 rate ch fmt data_fmt 48000 1 2 1

//Start recording stream
Apr 29 09:23:11 pipewire[862]: pal_stream_start: 338: Enter. Stream handle 0xffff6c001040K

//graph_open entry
Apr 29 09:23:11 pipewire[862]: graph_open: 709 graph_handle 0x47534c

//Metadata details to identify the use case
Apr 29 09:23:11 pipewire[862]: metadata_print: 82 key:0xb1000000, value:0xb1000009//RAW_RECORD
Apr 29 09:23:11 pipewire[862]: metadata_print: 82 key:0xa3000000, value:0xa3000004//HANDSETMIC

//Verify the graph opened for recording use case
Apr 29 09:23:11 pipewire[862]: print_graph_alias: 2334 GKV Alias 29 | DeviceTX_Handset_Mic_StreamTX_RAW_Record

//Configure hardware endpoint module
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 636 entry mod tag c0000005 miid 43af mid 7001024
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 664 rate 48000 bw 16 ch 1, data_fmt 1
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 676 exit, ret 0

//graph_start entry
Apr 29 09:23:11 pipewire[862]: graph_start: 899 entry graph_handle 0x47534c
//Stream recording started
Apr 29 09:23:11 pipewire[862]: pal_stream_start: 387: Exit. status 0

//graph_stop entry
Apr 29 09:23:26 pipewire[862]: graph_stop: 928 entry graph_handle 0x47534c
//Stop the PAL stream once user stops recording
Apr 29 09:23:26 pipewire[862]: D: [regular2] pal-source.c: pal_stream_stop returned 0

//Close the PAL stream
Apr 29 09:23:26 pipewire[862]: pal_stream_close: 284: Enter. Stream handle :0xffff6c001040K
//graph_close entry
Apr 29 09:23:26 pipewire[862]: graph_close: 762 entry handle 0x47534c
//Close the PAL stream
Apr 29 09:23:26 pipewire[862]: pal_stream_close: 322: Exit. status 0
```
