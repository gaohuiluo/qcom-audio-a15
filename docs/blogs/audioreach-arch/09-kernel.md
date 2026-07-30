# 第 9 篇 内核篇：audio-kernel-ar 承载 GPR 与数据搬运

前面八篇走完了用户态到 DSP 的完整链路，但有一段一直被略过：**GPR 包和 PCM 数据到底
怎么跨过用户态、内核、再到 DSP？** 这一篇看内核模块 `audio-kernel-ar`，
它是连接“APPS 用户态”与“DSP”的物理桥梁。

内核这层做三件事：**承载 GPR 传输**（ipc/）、**管理 DSP 生命周期与共享内存**（dsp/）、
**接入 ALSA/ASoC 声卡与编解码**（asoc/ + soc/）。

## 一、GPR 在内核：gpr-lite + audio-pkt

第 7 篇讲 GPR 用户态发包时，`gpr_lx` datalink 最终要把包交给内核。内核侧的对接就是
`ipc/` 下这几个文件：

| 文件 | 作用 |
|------|------|
| `gpr-lite.c` | 内核 GPR 核心：基于 **rpmsg/glink** 收发 GPR 包，按 dst_port 派发 |
| `audio-pkt.c` | 字符设备（`/dev/...`），把用户态与内核 GPR 打通 |
| `audio-cc-ipc.c` | 音频相关的跨核 IPC 辅助 |

### gpr-lite.c：基于 rpmsg 的跨核传输

内核 GPR 是一个 **rpmsg 驱动**（`gpr-lite.c`）。
rpmsg 是 Linux 的远程处理器消息框架，底层就是高通的 **glink**（跨处理器共享内存通道）。
发包很直接：

```c
// gpr-lite.c:85
int gpr_send_pkt(struct gpr_device *adev, struct gpr_pkt *pkt)
{
    ...
    ret = rpmsg_trysend(gpr->ch, pkt, pkt_size);   // 通过 rpmsg/glink 发到 DSP
}
```

收包走 rpmsg 回调 `gpr_callback`（`gpr-lite.c:252`），
**这正是第 7 篇 GPR 路由在内核的镜像**——按 `dst_port` 派发：

```c
svc_id = hdr->dst_port;
svc = idr_find(&gpr->svcs_idr, svc_id);     // 按 dst_port 查注册的服务
if (svc && svc->dev.driver)
    adrv = to_gpr_driver(svc->dev.driver);   // 派发给对应内核 GPR 驱动
else
    svc = idr_find(&gpr->svcs_idr, GPR_SVC_MAX);  // 兜底：audio passthrough
```

内核里每个用 GPR 的模块（如 `spf-core`）都注册成一个 `gpr_device`，占一个 port（svc_id），
DSP 回来的包按 port 找到它。**GPR 的 domain+port 寻址模型在用户态、内核、DSP 三处保持
一致**——这就是它“通用”的价值。

### audio-pkt.c：用户态的入口

`gpr_lx`（用户态）要把包递进内核，靠的是 `audio-pkt.c`
（`audio-pkt.c`）注册的字符设备。它提供
`file_operations`（open/read/write），用户态 GSL/GPR 打开 `/dev/aud_pasthru_adsp` 之类
的节点，`write` 下发包、`read` 收包。内部它持有一个 `gpr_device`，把用户态的字节流接到
内核 GPR：

```
用户态 GSL/GPR(gpr_lx)
   │ write(/dev/...)                    read(/dev/...)
   ▼                                        ▲
audio-pkt.c (字符设备, 持 gpr_device)
   │ gpr_send_pkt                        gpr_callback
   ▼                                        ▲
gpr-lite.c (rpmsg 驱动)
   │ rpmsg_trysend ═══ glink/共享内存 ═══ DSP 的 GPR
```

## 二、DSP 生命周期与就绪：dsp/

DSP 是独立子系统，要加载固件、探测就绪、处理崩溃重启。`dsp/` 目录管这些：

| 文件 | 作用 |
|------|------|
| `adsp-loader.c` | 加载 ADSP 固件镜像 |
| `spf-core.c` | 探测 SPF/APM 是否就绪 |
| `audio_notifier.c` / `audio_ssr.c` / `audio_pdr.c` | SSR/PDR 通知：DSP 崩溃/重启/子进程域恢复 |
| `msm_audio_ion.c` | **共享内存分配（ION/DMA-BUF + SMMU）** |
| `audio_prm.c` | 音频电源/资源管理（时钟、供电） |
| `q6_init.c` | 各 q6 音频驱动的初始化汇总 |

### spf-core：APM 就绪握手

系统起来后，用户态要确认 DSP 上的 APM 活了才能建图。`spf-core.c`
（`spf-core.c:159`）用一条 GPR 命令探测：

```c
#define APM_CMD_GET_SPF_STATE      0x01001021
#define APM_CMD_RSP_GET_SPF_STATE  0x02001007

bool spf_core_is_apm_ready(void)   // 发 GET_SPF_STATE，等 RSP，回 ready/not
```

这解释了开机时序：**固件加载（adsp-loader）→ APM 起来 → spf_core 探测 ready → 用户态
才开始 gsl_open 建图。** 顺序错了图就建不起来。

### msm_audio_ion：数据面共享内存的真身

第 6 篇说 GSL 用共享内存传 PCM 数据、只把地址通过 GPR 告诉 DSP。那块内存就是
`msm_audio_ion.c`（`msm_audio_ion.c`）分配的：

- 用 **ION / DMA-BUF** 分配物理连续（或 SMMU 映射）的内存。
- 通过 **SMMU/IOMMU** 把这块内存映射到 DSP 的地址空间（`smmu_enabled`、`smmu_sid_bits`），
  于是 DSP 能直接读写它——这就是第 6 篇 `gsl_shmem_alloc_data.spf_addr` 的来源。

**控制面（GPR 包）走 glink 消息通道，数据面（PCM）走 ION 共享内存 + SMMU 映射**——
两条通道在内核这层彻底落地。这也是为什么大块 PCM 数据不会挤爆 GPR 消息通道。

## 三、ASoC 声卡：ALSA 的另一端

第 4/5 篇里，PAL 通过 tinyALSA 操作 pcm/mixer 节点，AGM plugin 接管。但 ALSA 框架本身
需要一个**声卡驱动**来注册这些 pcm 设备和 mixer control——这就是 `asoc/` 的活。

- **machine 驱动**（`kona.c`、`lahaina.c`、`holi.c`、`bengal.c` 等，按平台命名）：
  用 ASoC 的 **DPCM（Dynamic PCM）** 模型注册前端（FE）和后端（BE）DAI link
  （`snd_soc_dai_link`）。第 4 篇 PAL 写的 `FE_CONNECT` 把前端连到后端，对应的正是这里
  定义的 FE/BE 拓扑。
- **`msm_common.c`**：各平台共用的初始化与 BE hw_params 配置逻辑。
- **codecs/**：编解码器驱动。
- **port-config 头**（`kona-port-config.h` 等）：定义各平台的 I2S/Slimbus/TDM 端口配置。

### soc/：底层总线

`soc/` 是更底层的总线与引脚：

- `soundwire.c` / `swr-mstr-ctrl.c`：**SoundWire** 总线主控（现代高通平台连接 codec/
  smart speaker 的主力总线）。
- `pinctrl-lpi.c`：**LPI（Low Power Island）** 引脚控制——低功耗音频（如语音唤醒待机）
  下仍能驱动麦克风的引脚域。呼应第 7 篇 GPR 的 island 模式、第 2 篇的语音唤醒路径。
- `regmap-swr.c` / `pinctrl-wcd.c`：codec 寄存器访问与引脚控制。

## 四、内核视角的全链路

把内核这层嵌回整条链路：

```
用户态 PAL ─ tinyALSA(pcm/mixer) ─► [内核 ASoC machine: FE/BE DPCM] ─► AGM plugin
用户态 GSL/GPR ─► [内核 audio-pkt(字符设备)] ─► [gpr-lite(rpmsg)] ═glink═► DSP GPR ─► APM
PCM 数据 ─► [msm_audio_ion: ION+SMMU 分配&映射] ═共享内存═► DSP 直接读写
DSP 崩溃 ─► [audio_notifier/ssr/pdr] ─► 通知用户态 ─► 各层 SSR 恢复(第2/6篇)
开机 ─► [adsp-loader 加载固件] ─► [spf-core 探测 APM ready] ─► 允许建图
```

## 系列收尾：一条链路，七次“降档”

九篇走下来，AudioReach 的骨架可以浓缩成一句话——**同一条链路，每层把抽象降一档**：

1. **PAL**：用例意图 → Stream/Session/Device（第 2-4 篇）
2. **AGM**：会话/设备 → 合并 metadata 成 GKV/CKV，映射到图操作（第 5 篇）
3. **GSL+ACDB**：GKV/CKV → 从数据库求解出子图/模块/连接/标定（第 6 篇）
4. **GPR**：图命令 → domain+port 寻址的通用包（第 7 篇）
5. **内核**：GPR 包 → rpmsg/glink 传输；PCM → ION/SMMU 共享内存（本篇）
6. **SPF**：命令 → 实例化 Container 和 Module，图真正运行（第 8 篇）
7. **Module(CAPI)**：`process()` → 一帧帧地处理 PCM

贯穿始终的三对核心概念，建议记牢：

- **GKV 定拓扑 / CKV·TKV 定参数**——图是什么样、参数是多少，分别由谁决定。
- **控制面（mixer/GPR 命令）/ 数据面（共享内存）**——命令和数据走两条路。
- **数据驱动**——拓扑与标定在 ACDB，模块在 AMDB，**改用例/调音/加算法基本不改框架代码**。

理解了这三对概念和“逐层降档”的结构，再去读任何一层的具体代码，都能很快定位自己
在整条链路的哪个位置。

## 小结

- 内核 `ipc/`：`gpr-lite.c` 基于 rpmsg/glink 承载 GPR 跨核传输并按 dst_port 派发，
  `audio-pkt.c` 用字符设备把用户态接进内核 GPR——domain+port 模型三层一致。
- 内核 `dsp/`：`adsp-loader` 加载固件、`spf-core` 探测 APM 就绪、`audio_notifier/ssr/pdr`
  处理 DSP 重启、`msm_audio_ion` 用 ION+SMMU 分配并映射数据面共享内存。
- 内核 `asoc/` + `soc/`：machine 驱动用 DPCM 注册 FE/BE DAI link（对应 PAL 的 FE_CONNECT），
  SoundWire/LPI 引脚等底层总线支撑常规与低功耗音频。
- 控制面走 glink 消息、数据面走 ION 共享内存，两条通道在内核落地。

至此，从 PAL 的 `pal_stream_open` 到 DSP 里 CAPI 模块的 `process()`，整条 AudioReach
链路就串通了。
