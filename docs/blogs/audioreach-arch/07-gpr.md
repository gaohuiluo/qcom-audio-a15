# 第 7 篇 GPR：通用包路由与跨核传输

GSL 把求解好的图打包成 `APM_CMD_GRAPH_OPEN` 之后，需要一条通道把它送到 DSP。这条通道
就是 **GPR（Generic Packet Router，通用包路由）**。它是 AudioReach 的“传输层”：定义了
一种统一的包格式，用 **domain + port** 寻址，屏蔽底层是 glink、共享内存还是同进程调用。

GPR 的设计目标很纯粹：**让 APPS、ADSP、CDSP、Modem 上的任意服务，都能用同一套 API
互发消息，而不关心对方在哪个处理器、走什么物理链路。**

## 一、包格式：一切皆 gpr_packet

GPR 的核心是一个统一的包头（`gpr_api.h`）。
关键字段（以 alloc 参数结构体为例，包头字段一一对应）：

```c
struct gpr_cmd_alloc_ext_t {
    uint8_t  src_domain_id;   // 发送方处理器
    uint32_t src_port;        // 发送方服务的注册 ID
    uint8_t  dst_domain_id;   // 接收方处理器
    uint32_t dst_port;        // 接收方服务的注册 ID
    uint32_t token;           // 请求/响应配对用
    uint32_t opcode;          // 动作 + payload 结构（如 APM_CMD_GRAPH_OPEN）
    uint32_t payload_size;
    gpr_packet_t **ret_packet;
};
```

三要素决定一次通信：

- **domain_id**：哪个处理器。
- **port**：该处理器上哪个服务/模块实例。
- **opcode**：干什么（动作），同时定义 payload 的结构。

`token` 用于把异步响应和原始请求对上号——GPR 是异步的，发出去不等回复，回复来了靠
token 匹配。

### Domain：处理器全家福

`gpr_ids_domains.h`：

```c
#define GPR_IDS_DOMAIN_ID_MODEM_V    1   // 调制解调器
#define GPR_IDS_DOMAIN_ID_ADSP_V     2   // 音频 DSP（主力）
#define GPR_IDS_DOMAIN_ID_APPS_V     3   // 应用处理器（GSL 就跑在这）
#define GPR_IDS_DOMAIN_ID_SDSP_V     4   // 传感器 DSP
#define GPR_IDS_DOMAIN_ID_CDSP_V     5   // 计算 DSP
#define GPR_IDS_DOMAIN_ID_CC_DSP_V   6
```

这解释了第 6 篇末尾的 MDF（Multi-DSP Framework）：GSL 从 ACDB 查到某子图的 proc domain
是 CDSP，就把该子图的 GRAPH_OPEN 包的 `dst_domain_id` 设为 CDSP。**同一张逻辑图的不同
子图可以发往不同 domain**，GPR 负责各自送达。

### Port：服务的地址

`port` 是服务在某 domain 内的唯一 ID。服务启动时用 `__gpr_cmd_register(src_port, callback_fn, ...)`
（`gpr_drv.c:968`）把自己的 port 和
回调函数登记进 GPR。之后所有 `dst_port` 指向它的包，都会被派发到这个回调。DSP 侧的 APM
就是这样注册一个固定 port，等着接收所有 GRAPH_OPEN。

## 二、发送：alloc + async_send

GSL/客户端发一条命令的两步（`gpr_drv_island.c`）：

```c
__gpr_cmd_alloc_ext(&args);        // 1. 分配一个填好头(domain/port/opcode/token)的包
__gpr_cmd_async_send(packet);      // 2. 异步发出
// 或一步到位：__gpr_cmd_alloc_send()
```

`__gpr_cmd_async_send`（`gpr_drv_island.c:68`）
的路由逻辑非常直接——**按 `dst_domain_id` 查数据链路表**：

```c
uint32_t domain_id = packet->dst_domain_id;
// 越界检查
if (GPR_PL_MAX_DOMAIN_ID_V < domain_id) return AR_EBADPARAM;
// 查该 domain 对应的数据链路，调它的 send
local_gpr_ipc_dl_table[domain_id].fn_ptr->send(...);
```

这就是 GPR 路由的全部秘密：**一张按 domain 索引的数据链路表 `local_gpr_ipc_dl_table[]`，
每个 domain 挂一个数据链路（datalink）驱动。** 发包 = 查表 + 调对应 datalink 的 send。

如果 `src_domain_id == dst_domain_id`（同处理器内），GPR 走本地内存队列直接投递；跨
domain 才走物理链路。

## 三、Datalink：物理链路抽象

GPR 本身不碰硬件，物理传输交给 datalink（`datalinks/gpr_lx/`）。
接口定义在 `ipc_dl_api.h`，是一对 vtable：

```c
// GPR → datalink：发
struct gpr_to_ipc_vtbl_t { uint32_t (*send)(...); ... };
// datalink → GPR：收
struct ipc_to_gpr_vtbl_t { uint32_t (*receive)(void* buf, uint32_t length); ... };
```

- **Linux 侧**：`gpr_lx.c` 是 Linux 用户态 datalink。它对接内核的 **glink/SMD** 之类的
  跨处理器 IPC（通过内核暴露的设备节点），把 GPR 包写进去、从里面读出来。
- **DSP 侧**：DSP 上有对应的 datalink 实现，收到包后交给本地 GPR，再按 `dst_port`
  派发给注册的服务（APM）。

收包路径正好对称：datalink 收到字节 → 调 GPR 的 `receive` → GPR 按 `dst_port` 找到
注册的 `callback_fn` → 投递给该服务。

### 分层示意

```
   APPS (GSL)                          ADSP
┌───────────────┐                  ┌───────────────┐
│ gsl → APM_CMD │                  │  APM (dst_port)│
│  _GRAPH_OPEN  │                  │   callback_fn  │
├───────────────┤                  ├───────────────┤
│ __gpr_cmd_    │  按 dst_domain    │  GPR core     │
│  async_send   │  查 dl_table      │  receive→派发  │
├───────────────┤                  ├───────────────┤
│ datalink(lx)  │                  │ datalink(dsp) │
│  fn_ptr->send │═══ glink/共享内存 ═══► fn_ptr->recv │
└───────────────┘   (内核承载)      └───────────────┘
```

中间那段“glink/共享内存”由 **audio-kernel-ar** 承载（第 9 篇）。

## 四、Island 模式：为什么源码里有一堆 `_island`

留意到核心文件成对出现：`gpr_drv.c` / `gpr_drv_island.c`、`gpr_list.c` / `gpr_list_island.c`。
`_island` 后缀是高通 DSP 的 **island（孤岛/低功耗）模式**——DSP 在极低功耗下只有一小块
内存（island）供电（LPI，Low Power Island）。**island 版本的代码被链接进那块常驻内存，
保证低功耗场景（如语音唤醒待机）下 GPR 仍能收发包**，而不用唤醒整个 DSP。

发送、分配、链表操作这些高频且低功耗必需的路径，都要有 island 版本。这也是第 2 篇
`StreamSoundTrigger` 那条低功耗路径能在 DSP 待机时工作的底层支撑之一。

## 五、GPR 的定位：薄而通用

GPR 刻意做得很薄——它不懂音频，只懂“把带 opcode 的包从 (src_domain, src_port) 送到
(dst_domain, dst_port)”。这带来两个好处：

1. **协议无关**：APM 命令、模块参数、事件回传、数据缓冲通知，全都用同一套 GPR 包，
   只是 opcode 不同。
2. **拓扑无关**：加一个新处理器，只要给它写一个 datalink 挂进 `dl_table`，上层完全不用改。

所以从 GSL 往下看，**GPR 是唯一的“下发管道”**：控制命令（APM/模块参数）走它，数据面
的“缓冲就绪通知”也走它（真正的 PCM 数据在共享内存，见第 6 篇）。

## 小结

- GPR 是通用包路由：用 `gpr_packet` 统一格式，靠 **domain_id（哪个处理器）+ port（哪个
  服务）+ opcode（干什么）** 三要素通信，异步 + token 配对。
- 发送 = `alloc` 填头 + `async_send`；路由就是按 `dst_domain_id` 查 `dl_table` 调对应
  datalink 的 send，同 domain 走本地队列。
- datalink 抽象物理链路（Linux 侧 `gpr_lx` 对接内核 glink），收发 vtable 对称。
- `_island` 版本支撑 DSP 低功耗待机下的收发，是语音唤醒等 LPI 场景的基础。
- GPR 薄而通用：协议无关、拓扑无关，是 GSL 之下唯一的命令下发管道。

下一篇到达终点——DSP 侧的 SPF：APM 收到 GRAPH_OPEN 后如何实例化 Container 和 Module，
让图真正跑起来。
