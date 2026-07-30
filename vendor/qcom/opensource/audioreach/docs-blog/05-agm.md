# 第 5 篇 AGM：会话/图/设备编排与 ALSA plugin

PAL 通过 tinyALSA 的 pcm 节点和 mixer control 下发请求。这些请求进内核 ALSA 后，被
一层 **AGM plugin** 截获，转成对 **AGM 服务** 的调用。AGM（Audio Graph Manager）是
连接“ALSA 世界”和“图世界”的枢纽：它对上说 ALSA 的语言，对下调 GSL 的 `gsl_*`。

这一篇讲三块：ALSA plugin 如何进入 AGM、AGM 的会话/设备/图三大对象、以及 graph 如何
映射到 GSL。

## 一、ALSA plugin：ALSA 请求的入口

[agm/plugins/tinyalsa/src/](../../agm/plugins/tinyalsa/src/) 下有三个 plugin，分别接管
ALSA 的三类操作：

| plugin | 接管 | 关键转调 |
|--------|------|----------|
| `agm_mixer_plugin.c` | 所有 mixer control（控制面） | `agm_session_set_metadata` / `agm_session_aif_connect` / `agm_set_params_with_tag` |
| `agm_pcm_plugin.c` | PCM 设备节点（数据面 + 会话生命周期） | `agm_session_open/prepare/start` / `agm_session_write/read` |
| `agm_compress_plugin.c` | compress 节点 | offload 版本的上述调用 |

### mixer plugin：PAL 的 control 变成 AGM 调用

回忆第 4 篇，PAL 写了 `FE_METADATA`、`FE_CONNECT`、`setParamTag` 等 control。
mixer plugin 就是这些 control 的**注册者与处理者**
（[agm_mixer_plugin.c](../../agm/plugins/tinyalsa/src/agm_mixer_plugin.c)）：

```c
// PAL 写 metadata control → plugin 收到 →
ret = agm_session_set_metadata(pcm_idx, tlv_size, payload);          // :1232
// PAL 写 connect control（FE 连 BE）→
ret = agm_session_aif_connect(pcm_idx, be_idx, state);              // :1079
// PAL 写 setParamTag（TKV 参数）→
if (strstr(ctl->name, "setParamTag"))
    ret = agm_set_params_with_tag(pcm_idx, be_idx, payload);        // :1442
```

这就闭合了第 4 篇的链路：**PAL 的 mixer_ctl_set_array → 内核 ALSA → AGM plugin →
agm_session_xxx()。** `pcm_idx` 就是前端号，`be_idx` 是后端号，metadata payload 里
就装着 GKV/CKV。

### pcm plugin：会话与数据

PCM 设备节点的打开/写读被 pcm plugin 转成会话生命周期
（[agm_pcm_plugin.c](../../agm/plugins/tinyalsa/src/agm_pcm_plugin.c)）：

```c
agm_session_open(session_id, sess_mode, &handle);   // :998  打开会话
agm_session_prepare(handle);                        // :646
agm_session_start(handle);                          // :662
agm_session_write(handle, buff, &count);            // :584  数据面
agm_session_read (handle, buff, &count);            // :608
```

**控制面（mixer）和数据面（pcm）在 AGM 这层仍然分开**，但都汇聚到同一个 `session_id`
标识的会话对象上。

## 二、AGM 的三大对象：Session / AIF(Device) / Graph

AGM 内部围绕三个对象组织（[agm/service/src/](../../agm/service/src/)）：

| 对象 | 文件 | 角色 |
|------|------|------|
| **Session** | `session_obj.c` | 一路用例的编排中心，持有 metadata、graph、绑定的 AIF 列表 |
| **AIF / Device** | `device.c` / `device_hw_ep.c` | Audio Interface：后端/硬件端点，持设备 metadata 与媒体配置 |
| **Graph** | `graph.c` / `graph_module.c` | 对 GSL 的封装，一个 graph 对应 DSP 上一张图 |

三者关系：**一个 Session 通过 `agm_session_aif_connect` 绑定一个或多个 AIF；每个
(Session, AIF) 组合的 metadata 合并后，开出一个 Graph。**

### Metadata 合并：GKV 的最终成形

AudioReach 的图由 GKV 唯一确定，而完整的 GKV 是**多来源合并**的结果。看
`session_obj.c` 里遍布的 `metadata_merge`：

```c
// session_obj.c:752 —— 打开图前合并三层 metadata
merged_metadata = metadata_merge(3, &sess_obj->sess_meta,          // 会话级
                                     &aif_obj->sess_aif_meta,      // 会话+AIF 级
                                     &aif_obj->dev_obj->metadata); // 设备级
...
ret = graph_open(merged_metadata, sess_obj, aif_obj->dev_obj, &graph_obj);  // :776
```

这正好对应第 4 篇 PAL 下发的三类 metadata（stream / device / stream-device）。**AGM
把它们按会话/设备维度合并成一个完整的 GKV+CKV，再交给 graph_open。** 这是“图到底长啥样”
的最终决定点（在 APPS 侧）。

## 三、Graph：映射到 GSL

`graph.c` 是对 GSL 的薄封装。它把 AGM 的动作一一映射成 `gsl_*` 调用，命令类操作统一走
`gsl_ioctl`：

```c
// graph.c —— AGM 动作 → GSL 调用
graph_open   →  gsl_open(&gkv, &ckv, &graph_handle);            // :667
graph_prepare→  gsl_ioctl(handle, GSL_CMD_PREPARE, ...);        // :856
graph_start  →  gsl_ioctl(handle, GSL_CMD_START, ...);          // :882
graph_stop   →  gsl_ioctl(handle, GSL_CMD_STOP, ...);           // :948
graph_add    →  gsl_ioctl(handle, GSL_CMD_ADD_GRAPH, ...);      // :1458  动态扩图
graph_change →  gsl_ioctl(handle, GSL_CMD_CHANGE_GRAPH, ...);   // :1697  切换拓扑
set_config   →  gsl_set_config(handle, gkv, ...);              // :1143
write        →  gsl_write(handle, ...);                        // :1359  数据面
read         →  gsl_read(handle, ...);                         // :1404
get_tag_info →  gsl_get_tagged_module_info(gkv, ...);          // :1480
```

几个值得注意的点：

- **`gsl_open` 只吃 GKV + CKV**（[graph.c:667](../../agm/service/src/graph.c#L667)）：
  拓扑（GKV）+ 标定（CKV, Calibration Key Vector）就是图的全部输入。GSL 拿这两个 KV
  去 ACDB 查出实际子图。**AGM 到这里就“交棒”了，它不知道图内部长啥样，那是 GSL+ACDB 的事。**
- **`GSL_CMD_ADD_GRAPH` / `CHANGE_GRAPH`**：支持在运行中往图里加子图、或整体换拓扑——
  这是设备切换、动态后处理挂载的底层能力。
- **回调**：`gsl_register_event_cb(handle, gsl_callback_func, graph_obj)` 注册事件回调，
  DSP 侧的事件（数据就绪、EOS、检测结果）经 GSL 回到 AGM，再经 pcm/mixer plugin 回到 PAL。

### AGM 侧的完整时序

```
PAL(mixer/pcm)      AGM plugin        session_obj        graph.c         GSL
   │ set metadata      │                  │                 │             │
   ├──────────────────►│ agm_session_set_metadata           │             │
   │                   ├─────────────────►│ 存 sess_meta     │             │
   │ aif_connect       │                  │                 │             │
   ├──────────────────►│ agm_session_aif_connect            │             │
   │                   ├─────────────────►│ metadata_merge   │             │
   │                   │                  ├─ graph_open ────►│ gsl_open ──►│ (查ACDB建图)
   │ pcm open          │                  │                 │             │
   ├──────────────────►│ agm_session_open │                 │             │
   │ pcm prepare/start │                  ├─ graph_prepare ─►│ GSL_CMD_PREPARE
   ├──────────────────►│ agm_session_start├─ graph_start ──►│ GSL_CMD_START
   │ pcm write         │                  │                 │             │
   ├──────────────────►│ agm_session_write├─ graph_write ──►│ gsl_write ─►│ (共享内存到DSP)
```

## 四、AGM 还管什么

除了编排，AGM 服务（`agm.c`）还负责：

- **会话池**：`session_obj_get_from_pool` 按 `session_id` 复用会话对象
  （[session_obj.c:356](../../agm/service/src/session_obj.c#L356)），不存在则 `session_obj_create`。
- **回环/组合用例**：`graph_add` 支持把回采（capture）与播放（playback）metadata 合并到
  同一图（[session_obj.c:461](../../agm/service/src/session_obj.c#L461)），实现 loopback、
  EC reference 等。
- **AIF 媒体配置与标定**：`agm_aif_set_media_config` / `agm_session_aif_set_cal` 把后端
  采样率、通道、标定送下去。
- **可选 IPC**：AGM 自己也能作为独立服务，`agm/ipc` 提供 DBus/HwBinder 包装（配置项
  `--with-no-ipc` 可关）。

## 小结

- AGM plugin 是 ALSA 与 AGM 的接缝：mixer plugin 处理控制面（metadata/connect/setParamTag），
  pcm/compress plugin 处理会话生命周期与数据面。
- AGM 内部三大对象 Session / AIF / Graph；`metadata_merge` 把 PAL 下发的三类 metadata
  合并成完整 GKV+CKV，这是 APPS 侧“图长啥样”的最终决定点。
- `graph.c` 把 AGM 动作映射成 `gsl_*`；`gsl_open(GKV, CKV)` 是交棒点——之后图的内部
  结构由 GSL + ACDB 决定。
- ADD_GRAPH/CHANGE_GRAPH 提供运行时扩图/换图能力，是动态路由与后处理挂载的基础。

下一篇进入真正的 graph solver——GSL 如何用 GKV/CKV 从 ACDB 求解出子图、管理共享内存
与数据通路，以及 ACDB 里到底存了什么。
