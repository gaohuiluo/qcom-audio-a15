# 音频故障排查

本章给出用于音频日志记录与调试的命令。

## 抓取日志

用户空间日志和内核音频驱动日志都有助于定位问题。

### 用户空间日志

抓取用户空间日志：

```shell
ssh root@ip-addr
mount -o remount,rw /
cat /var/log/user.log
```

更多说明参见 [用户空间日志](https://docs.qualcomm.com/doc/80-70030-12/topic/userspace_logs.html)。

### 内核音频驱动日志

抓取内核日志：

```shell
ssh root@ip-addr
dmesg
```

禁用某个特定文件的内核日志：

```shell
echo -n "file <filename> -p" > /sys/kernel/debug/dynamic_debug/control
```

### 动态内核日志

动态日志默认是关闭的。要启用它，需要加上 `CONFIG_DYNAMIC_DEBUG` 内核配置，重新编译，并重新刷写设备。

启用音频的动态内核日志：

```shell
ssh root@ip-addr
mount -o rw,remount /
mount -t debugfs none /sys/kernel/debug
echo -n "file <filename> +p" > /sys/kernel/debug/dynamic_debug/control
```

更多说明参见 [启用动态调试](https://docs.qualcomm.com/doc/80-70030-12/topic/enable_kernel_debugging.html#enable-dynamic-debug)。

## 分析日志

针对播放和录制用例，分析用户空间日志和内核音频驱动日志。

### 播放日志

下面的日志片段展示了播放用例所采集到的信息。

```text
//打开低延迟播放流。各流类型的详情见 sources/audio/opensource/arpal-lx/inc/PalDefs.h
2022-04-28T18:02:08.748280+00:00 pipewire: pal_stream_open: 224: Enter, stream type:1

//确认后端设备、采样率、位宽、声道数等
2022-04-28T18:02:08.748627+00:00 pipewire: setDeviceMediaConfig: 1056: CODEC_DMA-LPAIF_WSA-RX-0 rate ch fmt data_fmt 48000 2 2 1

//启动播放流
2022-04-28T18:02:08.751947+00:00 pipewire: pal_stream_start: 338: Enter. Stream handle 0xffff94001040K

//借助 kvh2xml.h 文件映射元数据，得到播放用例的详情
2022-04-28T18:02:08.853157+00:00 pipewire: metadata_print: 82 key:0xa1000000, value:0xa100000e//PCM_LL_PLAYBACK
2022-04-28T18:02:08.853395+00:00 pipewire: metadata_print: 82 key:0xab000000, value:0x1
2022-04-28T18:02:08.853660+00:00 pipewire: metadata_print: 82 key:0xa2000000, value:0xa2000001//Speaker
2022-04-28T18:02:08.853881+00:00 pipewire: metadata_print: 82 key:0xac000000, value:0xac000002//DEVICEPP_RX_AUDIO_MBDRC

//确认为播放用例打开的图
2022-04-28T18:02:08.856934+00:00 pipewire: print_graph_alias: 2334 GKV Alias 142 | StreamRX_PCM_LL_Playback_DeviceRX_Speaker_Instance_Instance_1_DevicePP_Rx_Audio_MBDRC
//调用 graph_open
2022-04-28T18:02:08.859509+00:00 pipewire: graph_open: 709 graph_handle 0x47534c

//配置硬件端点模块
2022-04-28T18:02:08.864386+00:00 pipewire: configure_hw_ep_media_config: 636 entry mod tag c0000004 miid 43b1 mid 7001023
2022-04-28T18:02:08.864495+00:00 pipewire: configure_hw_ep_media_config: 664 rate 48000 bw 16 ch 2, data_fmt 1
2022-04-28T18:02:08.864603+00:00 pipewire: configure_hw_ep_media_config: 676 exit, ret 0

//graph_start 入口
2022-04-28T18:02:08.867234+00:00 pipewire: graph_start: 899 entry graph_handle 0x47534c
//流已启动
2022-04-28T18:02:08.867864+00:00 pipewire: pal_stream_start: 387: Exit. status 0

//graph_stop 入口
2022-04-28T18:02:25.037338+00:00 pipewire: graph_stop: 928 entry graph_handle 0x47534c
//播放完成后停止 PAL 流
2022-04-28T18:02:25.039923+00:00 pipewire: pal_stream_stop: 441: Exit. status 0

//graph_close 入口
2022-04-28T18:02:25.050944+00:00 pipewire: graph_close: 762 entry handle 0x47534c
//关闭 PAL 流
2022-04-28T18:02:25.054510+00:00 pipewire: pal_stream_close: 322: Exit. status 0
```

### 录制日志

下面的日志片段展示了录制用例所采集到的信息。

```text
//为 PAL_STREAM_RAW 打开录制流。该流类型的详情见 sources/audio/opensource/arpal-lx/inc/PalDefs.h
Apr 29 09:23:11 pipewire[862]: pal_stream_open: 224: Enter, stream type:9

//确认后端设备、采样率、位宽、声道数等
Apr 29 09:23:11 pipewire[862]: setDeviceMediaConfig: 1056: CODEC_DMA-LPAIF_VA-TX-0 rate ch fmt data_fmt 48000 1 2 1

//启动录制流
Apr 29 09:23:11 pipewire[862]: pal_stream_start: 338: Enter. Stream handle 0xffff6c001040K

//graph_open 入口
Apr 29 09:23:11 pipewire[862]: graph_open: 709 graph_handle 0x47534c

//用于识别用例的元数据详情
Apr 29 09:23:11 pipewire[862]: metadata_print: 82 key:0xb1000000, value:0xb1000009//RAW_RECORD
Apr 29 09:23:11 pipewire[862]: metadata_print: 82 key:0xa3000000, value:0xa3000004//HANDSETMIC

//确认为录制用例打开的图
Apr 29 09:23:11 pipewire[862]: print_graph_alias: 2334 GKV Alias 29 | DeviceTX_Handset_Mic_StreamTX_RAW_Record

//配置硬件端点模块
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 636 entry mod tag c0000005 miid 43af mid 7001024
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 664 rate 48000 bw 16 ch 1, data_fmt 1
Apr 29 09:23:11 pipewire[862]: configure_hw_ep_media_config: 676 exit, ret 0

//graph_start 入口
Apr 29 09:23:11 pipewire[862]: graph_start: 899 entry graph_handle 0x47534c
//录制流已启动
Apr 29 09:23:11 pipewire[862]: pal_stream_start: 387: Exit. status 0

//graph_stop 入口
Apr 29 09:23:26 pipewire[862]: graph_stop: 928 entry graph_handle 0x47534c
//用户停止录制后停止 PAL 流
Apr 29 09:23:26 pipewire[862]: D: [regular2] pal-source.c: pal_stream_stop returned 0

//关闭 PAL 流
Apr 29 09:23:26 pipewire[862]: pal_stream_close: 284: Enter. Stream handle :0xffff6c001040K
//graph_close 入口
Apr 29 09:23:26 pipewire[862]: graph_close: 762 entry handle 0x47534c
//关闭 PAL 流
Apr 29 09:23:26 pipewire[862]: pal_stream_close: 322: Exit. status 0
```
