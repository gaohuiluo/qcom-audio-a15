# 第 6 篇 GSL + ACDB：图求解与标定

AGM 交出 `gsl_open(GKV, CKV)` 后，就轮到本篇的主角。**GSL（Graph Service Layer）是
AudioReach 真正的“图编译器 + 链接器”**：它拿着两组 key-value，去 **ACDB** 这个数据库
查出图由哪些子图组成、怎么连接、每个模块用什么标定，然后把这张图打包成命令发给 DSP。

如果说前面几层在做“描述用例”，那么从 GSL 开始才真正在“构建图”。

## 一、两个输入：GKV 与 CKV

GSL 的一切都围绕两个 key vector（[gsl_intf.h:273](../audioreach-graphservices/gsl/api/gsl_intf.h#L273)）：

```c
struct gsl_key_vector {
    uint32_t num_kvps;
    struct gsl_key_value_pair *kvp;   // 一组 <key, value>
};
```

- **GKV（Graph Key Vector）**：决定**图的拓扑**——用哪些子图、怎么连。
- **CKV（Calibration Key Vector）**：决定**标定数据**——同一张图，不同 CKV 可以是不同
  的调音（比如不同音量档、不同设备特性）。

**同一个 GKV 决定“图长什么样”，CKV 决定“图里参数是多少”。** 这就是第 4、5 篇一路
传下来的 GKV/CKV 在此兑现。

## 二、ACDB：图与标定的数据库

ACDB（Audio Calibration Database）是一套二进制数据库 + 查询引擎
（[acdb/](../audioreach-graphservices/acdb/)），对外只有一个入口：`acdb_ioctl(cmd, req, rsp)`。
GSL 通过一系列命令向它查询：

| ACDB 命令 | 查什么 |
|-----------|--------|
| `ACDB_CMD_GET_GRAPH` | 给定 GKV → 返回子图列表及其连接关系 |
| `ACDB_CMD_GET_SUBGRAPH_CONNECTIONS` | 子图之间怎么连 |
| `ACDB_CMD_GET_SUBGRAPH_DATA` | 子图内部：容器、模块、连接、默认配置 |
| `ACDB_CMD_GET_SUBGRAPH_CALIBRATION_DATA_NONPERSIST` | 子图标定数据（按 CKV） |
| `ACDB_CMD_GET_SUBGRAPH_PROCIDS` | 子图运行在哪个处理器（proc domain） |
| `ACDB_CMD_GET_TAGGED_MODULES` | 按 tag 找模块实例（配合 TKV 调参） |
| `ACDB_CMD_GET_HW_ACCEL_SUBGRAPH_INFO` | 硬件加速（如 CMA 内存）相关信息 |

### GKV → 子图：图求解第一步

`gsl_acdb_get_graph`（[gsl_graph.c:1565](../audioreach-graphservices/gsl/src/gsl_graph.c#L1565)）
就是把 GKV 丢给 ACDB，拿回子图及连接：

```c
cmd_struct.num_keys        = gkv->num_kvps;
cmd_struct.graph_key_vector = (AcdbKeyValuePair *)gkv->kvp;
// 第一次调用 size=0，让 ACDB 回填所需大小；分配后再查一次拿数据（典型两段式 ioctl）
rc = acdb_ioctl(ACDB_CMD_GET_GRAPH, &cmd_struct, cmd_struct_size, &rsp_struct, ...);
```

返回的 `AcdbGetGraphRsp`（[acdb.h](../audioreach-graphservices/acdb/api/acdb.h#L258)）里是
一组 `AcdbSubgraph`，每个含 `sg_id` 和它的目标子图列表 `dst_sg_ids[]`——**这就是一张
有向图：节点是子图，边是连接。** 拿到 0 个子图也是合法的（不在 DSP 上开任何东西）。

> 数据来自哪里？ACDB 里的图定义由离线工具 **ARC（AudioReach Creator / QACT）** 生成。
> 音频工程师用图形工具画出用例的模块拓扑、设好标定，导出成 `.acdb` 文件放进
> `/vendor/etc/acdbdata/`。**改拓扑/调音 = 改 ACDB 文件，不改代码**——这是 AudioReach
> 数据驱动的最终落点。

## 三、GSL 的核心对象

GSL 内部三层对象（[gsl/src/](../audioreach-graphservices/gsl/src/)）：

| 对象 | 文件 | 角色 |
|------|------|------|
| **graph** | `gsl_graph.c` | 一次 `gsl_open` 对应一个 graph，聚合多个 GKV 节点与子图 |
| **subgraph** | `gsl_subgraph.c` / `gsl_subgraph_pool.c` | 子图对象，可跨 graph 复用（子图池） |
| **datapath** | `gsl_datapath.c` | 数据面：读写缓冲、共享内存映射 |

外加几个基础设施：`gsl_shmem_mgr.c`（共享内存管理）、`gsl_msg_builder.c`（构造发往 DSP
的消息）、`gsl_mdf_utils.c`（多 DSP/multi-domain 支持）、`gsl_spf_ss_state.c`（SSR 状态）。

### 子图池：为什么子图能复用

`gsl_subgraph_pool.c` 维护一个**全局子图池**。多路用例常常共享同一个子图（比如都用
同一个扬声器后端子图）。GSL 用引用计数管理：同一个 `sg_id` 只在 DSP 上开一次，第二个
用户来了就复用并加引用。**这直接对应第 3 篇 RM 的共享后端、第 2 篇 Device 单例——
从上到下，“共享”这件事在每一层都有对应机制。**

## 四、图求解与下发：gsl_open 全流程

`gsl_open` → `gsl_graph_open`（[gsl_graph.c:4651](../audioreach-graphservices/gsl/src/gsl_graph.c#L4651)）
→ 对每个 GKV 节点 `gsl_graph_open_single_gkv`（[gsl_graph.c:3290](../audioreach-graphservices/gsl/src/gsl_graph.c#L3290)）。
单个 GKV 的求解过程：

```
gsl_graph_open_single_gkv
  ├─ gsl_acdb_get_graph(gkv)                 // ① GKV → 子图列表+连接 (ACDB_CMD_GET_GRAPH)
  ├─ gsl_graph_open_sgids_and_connections    // ② 剪枝：去掉已开的子图(子图池)，算出真正要开的
  │     ├─ ACDB_CMD_GET_SUBGRAPH_DATA        //    查每个子图内部：容器/模块/连接
  │     ├─ ACDB_CMD_GET_SUBGRAPH_PROCIDS     //    查子图在哪个处理器
  │     └─ ACDB_CMD_GET_..._CALIBRATION_DATA //    按 CKV 查标定
  ├─ gsl_msg_alloc(APM_CMD_GRAPH_OPEN, ...)  // ③ 构造发往 DSP APM 的 GRAPH_OPEN 消息
  └─ 通过 GPR 下发到 DSP                       // ④ (下一篇)
```

第 ③ 步是关键交接点（[gsl_graph.c:3198](../audioreach-graphservices/gsl/src/gsl_graph.c#L3198)）：

```c
rc = gsl_msg_alloc(APM_CMD_GRAPH_OPEN, graph->src_port, ...);
```

GSL 把“求解出来的图”（子图 + 模块 + 连接 + 标定）打包成一条 **APM_CMD_GRAPH_OPEN**
消息——`APM` 就是 DSP 侧的图管理器（第 8 篇）。这条消息通过 **GPR**（第 7 篇）跨核送到
DSP，DSP 的 APM 收到后才真正实例化图。

**注意 proc domain**：`ACDB_CMD_GET_SUBGRAPH_PROCIDS` 告诉 GSL 每个子图跑在哪个处理器
（ADSP / CDSP / APPS…）。这意味着**一张图可以横跨多个处理器**，GSL 要把对应子图的
GRAPH_OPEN 发往不同 domain——这是 `gsl_mdf_utils.c`（Multi-DSP Framework）的活。

## 五、数据面：共享内存与读写

控制面走 APM 命令，**数据面走共享内存**。`gsl_datapath.c` + `gsl_shmem_mgr.c` 负责：

- 分配 DSP 可访问的共享内存（`gsl_shmem_alloc_data`，含 `spf_addr` 即 DSP 侧地址）。
- 把外部（客户端）内存映射进来（`gsl_shmem_map_extern_mem`），并做 LRU 缓存避免反复
  映射（[gsl_datapath.c](../audioreach-graphservices/gsl/src/gsl_datapath.c) 的 `ext_mem_cache`）。
- `gsl_write`/`gsl_read` 把数据缓冲的**共享内存句柄**通过数据命令发给 DSP，DSP 直接
  读写该内存，避免拷贝。

所以第 2 篇说的“数据面走共享内存”，到这里才是真正实现：PCM 数据不经过 GPR 命令通道，
而是放在双方都能访问的物理内存里，GPR 只传“数据在哪、多大”。

## 六、GSL 还负责

- **RTC（Real-Time Calibration）**：`gsl_rtc.c` / `gsl_rtc_main.c` 支持在线调音——QACT
  工具连上设备，实时改标定、看效果，不用重启用例。这是音频工程师日常调音的通道。
- **动态模块加载**：`gsl_dynamic_module_mgr.c` 配合 DSP 侧 AMDB 加载非内建模块。
- **DLS（Data Logging Service）**：`gsl_dls_client.c` 抓 DSP 内部数据流用于调试。
- **SSR 处理**：`gsl_spf_ss_state.c` 跟踪各 DSP 子系统状态，崩溃重启时重建图。

## 小结

- GSL 是真正的 graph solver：输入 GKV（拓扑）+ CKV（标定），通过 `acdb_ioctl` 系列命令
  从 ACDB 查出子图、连接、模块、proc domain 与标定数据。
- ACDB 是数据库，图拓扑与标定由离线工具（ARC/QACT）生成为 `.acdb` 文件——**改用例/调音
  改数据不改码**，这是数据驱动的终点。
- GSL 三层对象 graph/subgraph/datapath；子图池实现跨用例复用，与上层“共享”机制一脉相承。
- 求解结果打包成 `APM_CMD_GRAPH_OPEN`，经 GPR 下发；子图可横跨多处理器（MDF）。
- 数据面走共享内存（gsl_shmem_mgr），GPR 只传地址与大小；RTC 提供在线调音通道。

下一篇讲这条“下发通道”本身——GPR 如何把 APM 命令打成包，按 domain/port 跨处理器路由。
