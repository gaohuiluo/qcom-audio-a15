# 高通 AudioReach 音频架构详解

> 这是一篇写给中级 Android 音频工程师的走读笔记。它不展开 AOSP framework(AudioFlinger / AudioPolicy)那一半,而是聚焦高通自己的 vendor 音频栈:**AHAL → PAL → AGM → GraphServices → SPF(DSP)**。代码基线是 Android 15 与 AudioReach 开源线(CodeLinaro)。
>
> 文中会出现一些 API 和结构体,但它们只是佐证——真正想让你记住的是**每一层在解决什么问题、为什么这么设计**。看完你应该能在脑子里把一条音频从 App 一直画到扬声器。

---

## 开篇:先换一个思维方式

如果你写过或读过老的音频 HAL(比如 `hardware/qcom/audio`),你对"音频怎么走"的印象大概是这样的:一条播放流该经过哪些处理、连到哪个设备、用什么采样率,这些逻辑**硬编码在 C 代码里**。想加一条新路径,往往意味着改代码、重新编译、刷机验证。

AudioReach 把这件事彻底翻转了。它的核心主张只有一句话:

> **"数据怎么流"不再写在代码里,而是画成一张图(graph),存进一个数据库(ACDB);运行时用一串 key-value 去数据库里把图查出来,下发给 DSP 去执行。**

这句话是理解整套架构的总纲。一旦接受了"处理流水线是数据、不是代码"这个前提,后面所有看似绕的设计——虚拟声卡、mixer 控件传参、GKV 查表——都会变得顺理成章。

顺着这个主张,你只需要抓住三条主线,就抓住了全局:

| 主线 | 一句话 | 谁负责 |
|------|--------|--------|
| **usecase 抽象** | 播放、录音、通话、热词……每种用途抽象成一个 Stream | PAL |
| **路由决策** | 这个 usecase 该连到哪个物理设备、走哪个 backend | PAL 的 ResourceManager + XML 配置 |
| **图(graph)** | DSP 上实际的处理流水线,由一串 key-value 从数据库查出 | AGM → GSL → ACDB → SPF |

再浓缩一点,记住这句话就够开始了:**PAL 决定"用途和设备",AGM 与 GSL 决定"DSP 图长什么样",ACDB 是那本图册,SPF 是 DSP 上真正干活的引擎。**

---

## 一、全景图:六层是怎么摞起来的

在深入每一层之前,先看一眼整个栈的形状。从上到下,一条音频要穿过六层,每一层只做一件事,然后把问题递给下一层:

```
┌──────────────────────────────────────────────────────────────┐
│  AOSP Framework(本文不展开)                                    │
│  AudioFlinger 混音 / AudioPolicy 路由策略 → libaudiohal(AIDL 客户端)│
└──────────────────────────────────────────────────────────────┘
        │ AIDL: android.hardware.audio.core (IModule/IStreamOut/IStreamIn)
        ▼
┌──────────────────────────────────────────────────────────────┐
│  AHAL(Audio HAL,AIDL)          ahal-aidl/audio/aidl/          │
│  Module / StreamOut / StreamIn   把 AIDL 请求变成 PAL 调用        │
└──────────────────────────────────────────────────────────────┘
        │ PAL C API: pal_stream_open / _start / _write ...
        │ (跨进程时经 HIDL IPAL 桥,见第三章)
        ▼
┌──────────────────────────────────────────────────────────────┐
│ ★ PAL(Platform Audio Layer)     pal/          路由 & usecase 核心 │
│   Stream(用途) + Device(设备) + Session(会话)                    │
│   ResourceManager(路由决策,读 XML)                              │
└──────────────────────────────────────────────────────────────┘
        │ 两条下行路(见第四章):
        │  ① PCM 类:tinyalsa(pcm_/mixer_)→ AGM tinyalsa 插件
        │  ② 非隧道类:直接调 agm_session_* API
        ▼
┌──────────────────────────────────────────────────────────────┐
│  AGM(Audio Graph Manager)        agm/                          │
│   session ↔ graph 映射;合并 GKV/CKV metadata;调 GSL            │
└──────────────────────────────────────────────────────────────┘
        │ GSL API: gsl_open(GKV,CKV) / gsl_ioctl / gsl_write
        ▼
┌──────────────────────────────────────────────────────────────┐
│  GraphServices                    graphservices/               │
│   GSL(图服务)+ ACDB(图&校准数据库)+ GPR(包路由协议)          │
└──────────────────────────────────────────────────────────────┘
        │ GPR 包(APM_CMD_GRAPH_OPEN ...)经内核 rpmsg/GLINK
        ▼
┌──────────────────────────────────────────────────────────────┐
│  内核 audio-kernel-ar/  +  DSP 侧 ar-engine/(SPF)              │
│   ipc/gpr-lite.c(rpmsg)→ ADSP 上的 SPF/APM 实例化图并运行       │
└──────────────────────────────────────────────────────────────┘
```

这张图值得多看两眼,因为它揭示了一个重要的分工:**越往上越"懂业务",越往下越"懂硬件"。** framework 关心的是"用户在放音乐还是打电话";PAL 关心的是"这个用途配哪个设备";再往下,AGM 和 GraphServices 已经完全不谈业务了,它们只关心"这张图的键是什么、怎么把它变成 DSP 能懂的命令包";到了内核和 DSP,连图是什么都不重要了,只剩下"把这个包送过去、把这块共享内存里的样本算完"。

每一层的职责和它在代码里的位置,可以对照下表速查:

| 层 | 目录 | 进程 | 核心职责 |
|----|------|------|----------|
| AHAL | `ahal-aidl/audio/aidl/` | audioserver 侧 HAL 进程 | 实现 AIDL 接口,翻译成 PAL 调用 |
| PAL | `pal/` | 通常独立 PAL 服务进程 | usecase 抽象、路由决策、会话管理 |
| AGM | `agm/` | 与 PAL 同进程(库)或独立服务 | session→graph 映射、GKV/CKV 合并 |
| GraphServices | `graphservices/` | 同 AGM 进程(库) | GSL 图服务、ACDB 数据库、GPR 打包 |
| 内核驱动 | `audio-kernel-ar/` | Kernel | ASoC 声卡 + GPR/rpmsg 传输 |
| SPF 引擎 | `ar-engine/` | ADSP(Hexagon) | DSP 上真正跑图的框架 |
| 配置/校准 | `ar-conf/` | 数据文件 | ACDB 二进制、kvh2xml.h 常量定义 |

接下来我们从最关键的一层——PAL——开始,逐层往下走。

---

## 二、PAL:路由与 usecase 的核心

如果只允许你精读一层,那应该是 PAL(Platform Audio Layer)。它是理解高通音频的钥匙,因为"用途"和"设备"这两个业务概念在这里第一次被明确地分开,又在这里被重新缝合。

PAL 的设计哲学是**三个概念的解耦**:

- **Stream** 代表一种**用途**(usecase):低延迟播放、深缓冲播放、压缩 offload、通话、热词唤醒……每一种用途都有自己对延迟、功耗、缓冲的偏好。
- **Device** 代表一个**物理设备**:扬声器、听筒、有线耳机、USB、蓝牙……
- **Session** 代表一次**到下层的会话**,也就是通往 AGM 和 DSP 图的那条通道。

三者的关系很直白:一个 Stream 关联一个 Session 和一到多个 Device,而把它们按规则连起来的,是一个叫 `ResourceManager` 的全局单例。为什么要这样拆?因为用途和设备本来就是正交的——同一首音乐(一个 Stream)可以在播放中途从扬声器切到蓝牙耳机(换 Device)而不用重开;同一个扬声器(一个 Device)也可能同时被音乐和提示音两条流共用。把它们拆开,运行时改路由才成为可能,而"运行时无缝切设备"正是 AudioReach 相对老 HAL 的一大卖点。

### 2.1 对外只有一套 C 接口,就是一条生命周期线

AHAL 看到的 PAL,是一组 `extern "C"` 的 C 接口(定义在 `pal/inc/PalApi.h`)。不用去背每个函数的签名,因为它们整齐地排成一条**生命周期主线**:

> **`open` → `start` → `write`/`read` → `stop` → `close`**

`pal_stream_open` 打开一条流:传入描述用途的属性和一组初始设备,拿回一个不透明句柄。之后 `pal_stream_start` 启动数据路径,播放用 `pal_stream_write` 灌数据、录音用 `pal_stream_read` 取数据,最后 `stop` 加 `close` 收场。在这条主线之外,还有三个"运行时旋钮":`pal_stream_set_device`(切设备,即上面说的无缝切换)、`pal_stream_set_param`(改参数)、`pal_stream_set_volume`(调音量)。

那个句柄 `pal_stream_handle_t` 本质上就是个 `uint64_t`,实现里其实是把内部的 `Stream*` 指针 `reinterpret_cast` 过去而已——记住这点,后面看控制流时就知道句柄背后是谁在干活。

### 2.2 打开一条流,到底要描述清楚什么

`pal_stream_open` 最重要的入参是一个"流属性"描述符(`pal_stream_attributes`)。与其罗列它的每个字段,不如理解它想回答的三个问题:

1. **这是什么用途?** —— 由一个 usecase 类型枚举决定,比如低延迟、深缓冲、压缩 offload、通话、语音唤醒。
2. **数据往哪个方向流?** —— 输出(播放)、输入(录音),还是双向(通话)。
3. **媒体格式是什么?** —— 采样率、位宽、格式、声道布局,输入侧和输出侧可以各自描述。

usecase 类型这个枚举尤其值得记,因为它直接决定了 PAL 会 new 出哪种 Stream 子类、最终配出哪种 DSP 图。几个最常见的:

| usecase | 特点 |
|---------|------|
| `LOW_LATENCY` | 低延迟,给游戏、导航用,功耗偏高 |
| `DEEP_BUFFER` | 深缓冲,给音乐用,低功耗但延迟高 |
| `COMPRESSED` | 压缩 offload,MP3/AAC 直接丢给 DSP 解码,省电 |
| `VOICE_CALL` | 电话通话 |
| `VOICE_UI` | 语音唤醒 / 热词(SVA) |
| `PCM_OFFLOAD` | PCM offload |
| `NON_TUNNEL` | 非隧道,纯 host 转码,不接任何物理设备 |

设备则用另一个描述符(`pal_device`)表达,核心是一个设备 id(如 `PAL_DEVICE_OUT_SPEAKER`)加上该设备侧的媒体配置。设备 id 的编号有个小规律:输出设备从一个 `OUT_MIN` 起排(听筒、扬声器、有线耳机、蓝牙 A2DP、USB……),输入设备紧接着从 `IN_MIN` 起排(各种 mic)。知道这个规律,读日志里的设备号时就不至于抓瞎。

### 2.3 内部类模型:三个概念如何落成对象

把上面三个概念落到 C++ 对象上,是这样一张关系图:

```
        ┌─────────────┐   持有   ┌──────────────┐
        │   Stream    │─────────▶│   Session    │──▶ tinyalsa / AGM
        │ (usecase)   │          └──────────────┘
        │             │  持有 1..N ┌──────────────┐
        │             │──────────▶│   Device     │(单例,按 id 共享)
        └─────────────┘          └──────────────┘
              ▲ 全都向
              │ ResourceManager(单例)拿资源、问路由
        ┌─────────────────────────────────────────┐
        │  ResourceManager:读 XML、管声卡/mixer、  │
        │  并发/优先级决策、SSR 恢复                 │
        └─────────────────────────────────────────┘
```

**Stream**(`pal/stream/`)是抽象基类,一个 `Stream::create()` 工厂按 usecase 类型 new 出具体子类:`StreamPCM` 管普通 PCM 播放录音、`StreamCompress` 管 offload、`StreamSoundTrigger` 管热词、`StreamInCall` 管通话、`StreamNonTunnel` 管转码,等等。每个 Stream 对象自己维护一个状态机(IDLE / INIT / OPENED / STARTED / PAUSED / STOPPED),这也是为什么前面那条生命周期主线能被严格约束——状态不对的调用会被直接挡回。

**Device**(`pal/device/`)最需要留意的是它的**单例语义**:`Device::getInstance()` 保证同一个物理设备全局只有一个实例。原因很现实——一个扬声器可能被多条流同时使用,所以设备内部维护一个引用计数,最后一个用户离开时才真正关闭。子类就是各种具体设备:`Speaker`、`Handset`、`Headphone`、`Bluetooth`、`USBAudio`,还有一个特别的 `SpeakerProtection`(扬声器保护,带 VI 电流电压反馈)。

**Session**(`pal/session/`)是通往下层的会话,子类分两大流派:走 tinyalsa 的(`SessionAlsaPcm`、`SessionAlsaCompress`、`SessionAlsaVoice`)和直连 AGM 的(`SessionAgm`)。这两条路的区别是第四章的重头戏。这里还藏着一个关键辅助类 `PayloadBuilder`——它负责**把平台配置翻译成 GKV/CKV/TKV 这些键值向量**以及模块参数 payload,是"配置"与"图"之间的翻译官,后面会反复见到它。

**ResourceManager**(`pal/resource_manager/ResourceManager.cpp`,一个 500KB+ 的巨型单例)是整个 PAL 的路由中枢。它解析平台 XML、持有那张"虚拟声卡"的 mixer 句柄、维护活跃流注册表、在多条流之间协商设备配置、拿全局图锁、并在 DSP 崩溃(SSR)时负责恢复。几乎所有对象都要回头找它拿资源、问路由。

### 2.4 路由的真相在 XML 里,不在代码里

这是 PAL 和老 HAL 最本质的区别,也呼应了开篇那句总纲:**改路由,常常只需要改 XML,不动一行 C 代码。** 关键配置在 `pal/configs/<平台>/`(例如 `qcm6490`)下:

- `resourcemanager_*.xml` 声明系统里有哪些设备、哪些 backend、每个设备支持哪些 usecase、并发时谁的优先级更高。
- `mixer_paths_*.xml` 描述每条路由要拨哪些 ALSA mixer 开关——你可以把它理解成"选这条路,要合上哪几个继电器"。
- `usecaseKvManager.xml` 记录 usecase 到 key vector 的映射。

所以走读 PAL 有一条铁律:**先读 XML,再读 `ResourceManager.cpp`。** 反过来一头扎进代码,很容易在几十万行里迷路,却找不到"这条流为什么走了这个设备"的答案——因为答案根本不在代码里。

---

## 三、AHAL:从 AIDL 接口下到 PAL

PAL 之上是 AHAL(Audio HAL)。它的职责说起来很朴素:**把 framework 通过 AIDL 发来的请求,翻译成 PAL 的 C 调用。** 但这中间有两个值得讲清楚的点——数据是怎么高效传下来的,以及在这份开源快照里"进入 PAL"的真实入口在哪。

### 3.1 AHAL 是 AIDL 的服务端

从 Android 13 起,音频 HAL 从 HIDL 迁到了 **AIDL**。framework 侧的 `libaudiohal` 是客户端,AHAL 是服务端,实现 `IModule`(代表一个音频模块)、`IStreamOut`(输出流)、`IStreamIn`(输入流)这几个核心接口。启动时,`main.cpp` 会为每个 audio-policy 模块注册一个 `Module` binder,framework 后续所有请求都从这里进来。

以打开一条输出流为例,`Module::openOutputStream` 做的事按顺序是:校验端口配置、检查 offload / non-blocking 之类的标志、建立一个 `StreamContext`(关键——里面含有下面要讲的 FMQ)、把 FMQ 的描述符回给客户端,最后按 flag 选出具体的流实现(MMAP 流、offload 流,或普通 primary 流)。

### 3.2 播放数据不走 binder,走共享内存队列

这是 AIDL HAL 一个容易被忽略但很重要的设计:**PCM 数据不是每次都通过 binder 调用传的**,而是走 **FMQ(Fast Message Queue,共享内存里的无锁队列)加一个专用 worker 线程**。binder 只用来传很小的控制命令。

一次播放的数据流动大致是这样:

```
framework                  AHAL worker 线程            下层
  │ 写 PCM 到 DataMQ           │                          │
  │ 发 burst 命令(CommandMQ)  │                          │
  │─────────────────────────▶│ cycle() 收到 burst        │
  │                          │ dataMQ->read() 取出 PCM   │
  │                          │ mDriver->transfer(buf) ───▶│ 写入 PAL / tinyalsa
  │◀── ReplyMQ 回 fmqByteCount│                          │
```

`StreamContext` 持有三条队列各司其职:`CommandMQ` 传命令、`ReplyMQ` 传回执、`DataMQ` 传真正的 PCM 样本。framework 把数据写进 DataMQ 后只发一个"burst"命令,worker 线程被唤醒、从队列取数据、交给下层驱动。如果是 MMAP 模式,则连 DataMQ 都省了,直接用一块共享 ashmem 区域。这套设计的目的只有一个:**让高频的数据搬运绕开 binder 的开销**——这个"控制走 IPC、数据走共享内存"的思路,你会发现从 AHAL 一直贯穿到内核。

### 3.3 一个关于本仓库的重要事实:进入 PAL 的真实入口

这里要澄清一个很容易让人卡住的点。**本仓库 `ahal-aidl/` 里检出的 AIDL 实现,其实是 AOSP 的参考 HAL,它直接驱动 tinyalsa,并不集成 PAL**——你在整个 `ahal-aidl/` 目录里搜不到任何一处 `pal_stream_*` 调用。真正调用 PAL 的、量产用的 vendor AHAL,不在这份快照里。

那在这份开源代码里,音频到底怎么"进入 PAL"?答案是 PAL 自带的一座 **HIDL 桥**,位于 `pal/ipc/HwBinders/`。它的接口定义(`IPAL.hal`)几乎是 PAL C API 的 1:1 镜像——PAL 有 `pal_stream_open`,它就有 `ipc_pal_stream_open`,一一对应。这座桥分两半:跑在 HAL 进程里的**客户端**把调用打包成 binder 发出去,跑在 PAL 服务进程里的**服务端**收到后再调用真正的 `pal_stream_open/start/write`。

所以在本仓库语境下,完整链路是:**AHAL →(HIDL IPAL binder 跨进程)→ PAL 服务进程 → `Pal.cpp` 的 C API**。而把 AIDL 类型(采样率、声道、格式、设备)翻译成 PAL 那套流属性描述符的活儿,由那个"缺席的 vendor AHAL"或这座桥的客户端来完成。理解这一点,才不会在找不到 `pal_` 调用时怀疑自己看错了代码。

---

## 四、PAL 如何连到 AGM:全书最关键的一环

很多人是在这里卡住的:PAL 的 Session 明明只调了 tinyalsa 的 `pcm_open` 和 `mixer_ctl_set_array`,这不就是往一张声卡上写数据吗?它是怎么就把一张图"下发"到 DSP 的?

答案是一个相当巧妙的**插件机制**,想通它,整条链就串起来了。

### 4.1 两条下行路径

PAL 往下走有两条路,绝大多数场景走第一条。

**路径①:PCM / Compress / Voice —— 经 tinyalsa 插件间接到 AGM**

`SessionAlsaPcm` 全程只用标准 tinyalsa 原语,而且它操作的对象是一张**虚拟声卡**:

```cpp
// SessionAlsaPcm::start() 里
pcm = pcm_open(rm->getVirtualSndCard(), pcmDevIds.at(0), PCM_OUT, &config);
pcm_start(pcm);
// 参数/校准通过 mixer 控件下发
ctl = mixer_get_ctl_by_name(mixer, tagCntrlName);
mixer_ctl_set_array(ctl, tagConfig, ...);
```

注意 `getVirtualSndCard()`——这张声卡**不是真硬件**,而是 AGM 的 tinyalsa 插件(`agm/plugins/tinyalsa/` 下的 `agm_pcm_plugin.c` 和 `agm_mixer_plugin.c`)**冒充**出来的一张 ALSA 声卡。于是 PAL 以为自己在操作声卡,实际每一个 tinyalsa 调用都被插件接住、转译成了 AGM 的 API 调用:

```
PAL SessionAlsaPcm
   │ pcm_open / pcm_start / mixer_ctl_set_array   (标准 tinyalsa 调用)
   ▼
AGM tinyalsa 插件(冒充声卡)
   │ agm_pcm_plugin.c:  pcm_open  → agm_session_open
   │                    pcm_start → agm_session_prepare + agm_session_start
   │                    pcm_write → agm_session_write
   │ agm_mixer_plugin.c: mixer 控件 → agm_session_set_metadata / agm_set_params_with_tag
   ▼
AGM 真正的 API(agm_session_*)
```

这里有一个必须点破的**关键洞察**:PAL 用 `PayloadBuilder` 算出来的那串 GKV/CKV(图的键值),是被打包成 **ALSA mixer 控件的 TLV 数据块**、搭着 mixer 控件这趟"车"传下去的,再由 AGM 的 mixer 插件解包还原成 `agm_session_set_metadata()` 调用。换句话说,"图该长什么样"这个信息,是伪装成"拨一个 mixer 开关"的动作偷偷送到 AGM 的。想不通这一层,就会一直以为 PAL 直接连了硬件。

**路径②:非隧道 / ACDB —— 直接调 AGM API**

相比之下第二条路很直白:`SessionAgm` 直接 `#include <agm/agm_api.h>`,不经过 tinyalsa,按 `set_metadata → open → prepare → start` 的顺序直接调 AGM。它用于非隧道转码这类不接物理设备的场景。

### 4.2 端到端控制流:一次 open + 一次 start

把上面的机制放进真实调用里,以"扬声器 PCM 播放"为例,一次 `pal_stream_open` 加一次 `pal_stream_start` 大致是这样展开的:

```
【pal_stream_open】
1. Pal.cpp: 校验 attributes,拿 ResourceManager 单例
2. Stream::create() —switch(type)→ new StreamPCM
3. StreamPCM 构造:
     - Session::makeSession() → new SessionAlsaPcm
     - Device::getInstance(SPEAKER) → 拿到共享的 Speaker 实例
     - rm->registerStream() + rm->updateDeviceConfig()  (和其他活跃流协商设备配置)
4. StreamPCM::open():
     - mDevices[i]->open()                         (使能设备)
     - rm->lockGraph(); session->open(this)         (加全局图锁)
5. SessionAlsaPcm::open():
     - 从 RM 拿前端 PCM 设备号 + 后端 AIF 名
     - PayloadBuilder 算出 GKV/CKV
       → 通过 mixer 控件写下去(此时 AGM 插件会 agm_session_set_metadata)
6. 返回 *stream_handle = (uint64_t)StreamPCM*

【pal_stream_start】
1. Pal.cpp: isActiveStream 校验;increaseStreamUserCounter
2. StreamPCM::start():
     - rm->lockGraph()
     - mDevices[i]->start()      (设备启动)
     - session->prepare(this); session->start(this)
3. SessionAlsaPcm::start():
     - pcm_open(虚拟声卡, ...)   → AGM 插件 → agm_session_open
     - mixer 下发 tag/cal 配置    → AGM 插件 → agm_set_params_with_tag
     - pcm_start(pcm)            → AGM 插件 → agm_session_prepare + agm_session_start
```

读这段的窍门,是始终记得右边那一列——**每一个 tinyalsa 调用,背后都对应一个 AGM 动作**。open 阶段最重要的事是把 GKV/CKV 通过 mixer 送下去(图的"设计蓝图"在这时就交给 AGM 了),start 阶段才真正让图跑起来。

之后的数据路径就顺理成章了:`pal_stream_write(buf)` → `SessionAlsaPcm` → `pcm_write` → AGM 插件 → `agm_session_write` → 图的写端点 → 共享内存 → DSP。

---

## 五、AGM:把 session 变成 graph

AGM(Audio Graph Manager)的职责单一而清晰:**接收一个 session 加设备的描述,把它映射成一张 DSP 图,再通过 GSL 打开并驱动数据。** 它是"业务描述"和"图"之间的中转站。代码上分四块:`agm/service/` 是核心逻辑,`agm/ipc/` 是跨进程接口,`agm/plugins/` 就是第四章那两个假装成声卡的插件,`agm/public_headers/` 是对外 API。

### 5.1 两个核心概念:session 与 AIF

AGM 的对外 API(`agm_api.h`)延续了和 PAL 一样的生命周期形状:`open` / `prepare` / `start` / `write` / `read` / `stop` / `close`。真正需要新理解的是它把"一路音频"拆成了两端:

- **session** 是**前端**——对应一路流的那个前端 PCM 设备。
- **AIF**(Audio Interface)是**后端**——对应物理接口,比如扬声器的那个 backend。

一次完整的连接,就是把某个 session 连到某个 AIF 上。这个前后端的划分不是 AGM 发明来炫技的,它直接对应 DSP 图里"流侧子图"和"设备侧子图"的分界,后面查 ACDB、设 metadata 时都要分别针对 session 和 AIF 来做。

还有一个贯穿全栈的动作藏在 API 里:`agm_session_set_metadata`——**GKV/CKV 就是从这个函数进入 AGM 的**。以及 `agm_set_params_with_tag`,它让你能"用一个 tag 定位到图里的某个模块、给它设参数"(比如调某一级的增益),而不用关心那个模块在图里的具体位置。

### 5.2 GKV / CKV:图的两把钥匙

前面反复提到 GKV/CKV,这里正式讲清楚它们是什么。它们**不是**通过某个专门的结构体参数传进来的,而是打包进 `agm_session_set_metadata()` 的那团**不透明 metadata 数据块**里。AGM 内部把它解出来,得到两个关键的 key vector:

- **GKV(Graph Key Vector)** 是一串 key-value,例如 `{STREAMRX=PCM, DEVICERX=SPEAKER, SAMPLERATE=48000}`。它是**去 ACDB 里查"用哪张图"的主键**——图的拓扑结构由它决定。
- **CKV(Calibration Key Vector)** 决定给这张图**灌哪一套校准数据**,比如当前音量档位对应的增益曲线、扬声器保护参数等。

一句话记牢它俩的分工:**GKV 决定"图长什么样",CKV 决定"往图里灌什么校准值"。** 图的形状和图的参数,被干净地分成了两把钥匙。

那这些 key(`STREAMRX`、`DEVICERX`、`SAMPLERATE`……)本身又是从哪来的?它们是一批预定义的常量,定义在 `ar-conf/qcom/kvh2xml.h` 里,PC 上的调音工具和 DSP 两端共享同一份定义——这保证了 AP 侧算出来的键,DSP 侧能对得上号。

### 5.3 合并 metadata,再交给 GSL

一路音频的 metadata 其实来自好几处:session 自己的、设备(AIF)的、以及 session-aif 连接的。AGM 的 `session_obj` 会先把这几份**合并**成最终的一套 GKV/CKV(`session_get_merged_metadata()` 调 `metadata_merge()`),这样图的流侧和设备侧才能拼成一张完整的图。

合并完之后,`graph.c` 就调用 GSL,把 AGM 的生命周期一一翻译成图操作:

```c
// agm/service/src/graph.c
gsl_open(&gkv, &ckv, &graph_handle);       // 传 GKV/CKV,把图加载到 DSP
gsl_ioctl(graph_handle, GSL_CMD_PREPARE, ...);
gsl_ioctl(graph_handle, GSL_CMD_START,   ...);
gsl_write(graph_handle, ..., buf, &size);  // 数据下发
gsl_ioctl(graph_handle, GSL_CMD_STOP,    ...);
```

至此 AGM 完成了它的全部使命:**session 的每一个生命周期动作(open/prepare/start/write/stop),都被一一映射成了 GSL 的图操作。** 它自己不碰图的内容,只负责"翻译"和"驱动"。

---

## 六、GraphServices:图服务、校准库、包路由

`graphservices/` 是整个控制面的核心库,由三个子件配合完成。记住一个比喻就不会乱:**GSL 是大脑,ACDB 是图册,GPR 是邮差。**

### 6.1 GSL:拿着钥匙去查图、再把命令发出去

GSL(Graph Service Layer)是 AGM 之下的图服务库。它做的事,可以用一条流水线概括:

> **拿到 GKV → 去 ACDB 查出图的定义和校准 → 翻译成一串 APM 命令 → 打包成 GPR 包发给 DSP。**

对外它同样是熟悉的生命周期接口:`gsl_open`(用 GKV/CKV 把图加载到 DSP)、`gsl_ioctl`(用命令 id 控制图,如 START / PREPARE / STOP / FLUSH / CHANGE_GRAPH)、`gsl_write`/`gsl_read`(数据)、`gsl_set_cal`(下发校准)。

对内,一次 `gsl_open()` 最终会变成什么?它会分配一个 **GPR 包**、填上操作码 `APM_CMD_GRAPH_OPEN`(0x01001000)和目标处理器(ADSP),然后交给 GPR 异步发出去、等 DSP 回包。也就是说,**"打开一张图"这个高层动作,落到线上就是一个带地址的命令包。**

这里还要引入两个会一直用到的概念:

- **subgraph(子图)**:一张完整的图是由若干子图串起来的,每个子图有自己的 `sg_id`。前面说的"流侧子图 + 设备侧子图"就是这个意思。
- **module instance(模块实例)**:用一对 id 标识——`MID` 是模块的"类"(这是个什么算法),`MIID` 是它在**当前这张运行图里的全局唯一实例**。给模块设参数时,先用 tag 查到 MIID,再对着这个实例下发。类比一下:MID 像"类名",MIID 像"对象地址"。

### 6.2 ACDB:那本可以查询的图册

ACDB(Audio Calibration Database)就是那本"图册"。它的行为可以精简成一句话:**输入一个 key vector,返回图的拓扑加校准数据。** 它对外只有一个入口函数 `acdb_ioctl()`,靠不同的命令 id 区分要查什么,其中最核心的几个:

| 命令 | 作用 |
|------|------|
| `GET_GRAPH` | **最核心**:输入 GKV,输出子图序列,也就是图的拓扑 |
| `GET_SUBGRAPH_DATA` | 子图内部的容器与模块连接数据 |
| `GET_SUBGRAPH_CALIBRATION_DATA` | 按 CKV 取出校准数据块 |
| `GET_TAGGED_MODULES` | 把 tag 解析成 MIID |
| `GET_AMDB_*` | 查 AMDB:告诉 SPF 该加载哪些模块库 |

要强调的是,ACDB 里的数据本身**不是代码里的逻辑,而是一份编译好的二进制**,放在 `ar-conf/.../acdbdata/acdb_cal.acdb`,由高通的 QACT 调音工具生成。这正是开篇总纲的落地:图和校准是"数据",调音师用工具改这份数据,不需要动代码。GKV/CKV 里用到的那些 key 常量,则来自前面提过的 `kvh2xml.h`。

(顺带一提,`acdb/ats/` 下的 ATS(Audio Tuning Service)是给 PC 上 QACT 用的 socket 服务,让调音师能实时读写校准——它只在调试调音时出现,量产的数据流里不参与。)

### 6.3 GPR:AP 与 DSP 之间的邮政系统

GPR(Generic Packet Router)是 AP 和 DSP 之间的消息协议,把它想象成一套"带地址的邮政系统"最贴切。每个 GPR 包头上都有两组关键地址:

- **domain** 选**哪个处理器**(AP / ADSP / CDSP / Modem)。
- **port** 选处理器内部**哪个具体服务**(注册在 GPR 上的模块或客户端)。

再加上一个 `opcode` 说明"这个包要干什么、payload 怎么解读"(比如 `APM_CMD_GRAPH_OPEN`),一个包就齐活了。用法也就三步:服务先用 `__gpr_cmd_register` 注册自己的 port 和回调,发送方用 `__gpr_cmd_async_send` 发包,收到包的一方在回调里处理。

那这些包怎么真正离开用户态、进内核?GPR 的 Linux 数据链路(`gpr_lx.c`)会打开一个字符设备 `/dev/aud_pasthru_adsp`(还有 modem、apps 版本),往里读写 GPR 包;同时起一个 `receiver_thread` 阻塞在 `read()` 上,等 DSP 回包、再派发给注册的回调。到这里,控制面就交接给内核了。

---

## 七、内核与 DSP:包最终怎么落到 SPF

控制面交给内核之后,故事的最后两站是:内核负责**运输**,DSP 负责**执行**。

### 7.1 内核:两条通道,分工明确

GPR 包从用户态到 DSP,内核里主要经过三个文件:

- `ipc/audio-pkt.c` 是**字符设备的壳**。它创建 `/dev/aud_pasthru_*` 节点,把用户态(GSL 的 `gpr_lx`)写来的 GPR 包转发到内核 GPR 总线,反向也一样。它还懂共享内存相关的操作码,配合 `msm_audio_ion` 做缓冲区映射。
- `ipc/gpr-lite.c` 是**内核里的 GPR 总线**,本质是一个 **rpmsg 驱动**。它调 `rpmsg_trysend()`,把 GPR 包通过 **rpmsg over GLINK/SMD** 送到 DSP;内部按 `dst_port` 路由,并跟踪 Q6/modem 子系统的状态(用于 SSR 恢复)。
- `dsp/spf-core.c` 代表内核眼里的 SPF/APM 实例,负责探活(问一句"SPF 起来了吗");旁边的 `msm_audio_ion*.c` 用 ION / DMA-buf 分配数据面要用的共享内存。

另外 `asoc/` 目录是给用户态的那张 ALSA/ASoC 门面:各 SoC 的 machine 驱动(`kona.c`、`lahaina.c`、`holi.c` 等)注册出 ALSA 的 PCM/mixer 设备——**这就是第四章那张"虚拟声卡"在内核侧的落点**;`codecs/` 则是各种编解码芯片驱动。

到这里可以把贯穿全栈的那条主线收个尾了——**控制面和数据面从头到尾是分开走的**:

1. **控制面**:AGM/GSL 打开 `/dev/aud_pasthru_adsp`,写 GPR 命令包 → `audio-pkt.c` → `gpr-lite.c` → rpmsg → DSP。
2. **数据面**:PCM 样本**不逐字节走 binder 或 GPR**,而是放在 ION / DMA-buf 共享内存里,命令包里只传一个"数据在哪块内存"的引用。

这正是从 AHAL 的 FMQ 一路延续下来的同一个思想:**小而频繁的控制走消息通道,大块数据走共享内存。**

### 7.2 DSP 侧:SPF 如何让一张图"活"起来

`ar-engine/` 是跑在 ADSP(Hexagon)上的 **SPF(Signal Processing Framework)**,编译成 `libspf.so` 动态加载。它就是 GSL 那些 APM/GPR 命令的**接收方和执行方**。它的结构是清晰的三层:

```
APM(Audio Processing Manager)—— 图的总管,处理 GRAPH_OPEN/PREPARE/START
  └── Container(容器)—— 执行与线程的封装,持有线程和缓冲,调度模块 process()
        └── CAPI Module(模块)—— 真正的算法,统一 vtable 接口
```

- **APM** 是图的总管,接收 `APM_CMD_GRAPH_OPEN` 之类的命令,负责把图搭起来。
- **Container(容器)** 是模块的执行载体,自带线程和调度。不同类型的容器对应不同诉求:`gen_cntr` 通用、`spl_cntr` 专攻低延迟、`wear_cntr` 服务可穿戴的低功耗、`olc` 管 offload。图的哪个子图该放进哪种容器,是由 ACDB 里的图定义决定的。
- **CAPI(Common Audio Processing Interface)** 是每个算法模块实现的**统一 C vtable**——核心就是一个 `process(输入, 输出)` 加上一组 set/get 参数的方法。框架用同一套接口对待所有算法,不管你是均衡器还是回声消除。每个模块以 GUID(也就是 MID)向 **AMDB**(模块注册表)注册,APM 需要时按 GUID 把对应的库加载进来。

把它串起来,一张图在 DSP 上"活过来"的过程就是:APM 收到 `GRAPH_OPEN`,按命令里的子图定义**实例化出容器和模块**,灌入校准,收到 `GRAPH_START` 后,容器的线程开始调度模块链,一帧帧地处理共享内存里的音频数据,最后从图的输出端点送往编解码器,扬声器发声。

---

## 八、把整条链完整走一遍(以播放为例)

学到这里,你应该能不看图就把一条播放流从头讲到尾了。对照下面这张全链路图检验一下自己:

```
App: AudioTrack.write(pcm)
  │  (AOSP framework: AudioFlinger 混音 → libaudiohal)
  ▼
AHAL  StreamOut::write → FMQ → worker → PAL C API
  │  pal_stream_write(handle, buf)     (跨进程时经 HIDL IPAL)
  ▼
PAL   StreamPCM → SessionAlsaPcm → pcm_write(虚拟声卡)
  │
  ▼
AGM   (tinyalsa 插件拦截) agm_session_write → graph.c
  │  合并后的 GKV/CKV 早在 open 时已下发
  ▼
GSL   gsl_write → 构造 GPR 包 → __gpr_cmd_async_send
  │
  ▼
内核  audio-pkt.c → gpr-lite.c → rpmsg/GLINK
  │  (PCM 数据走 ION 共享内存,只传引用)
  ▼
DSP   SPF/APM → 容器调度 → CAPI 模块链处理 → 输出到编解码器 → 扬声器发声
```

如果这张图里每一跳你都知道"这一层为什么存在、它把问题变成了什么再往下递",那这篇文章的目的就达到了。两句话作为全文的落点:

- **一条主线**:framework 说"要放音乐",PAL 把它翻译成"用途 + 设备",AGM/GSL 把它翻译成"一串键",ACDB 把键翻译成"一张图",SPF 把图翻译成"真正跑起来的算法链"。抽象在逐层下降,直到落地成 DSP 上的样本运算。
- **一个贯穿的原则**:控制走命令包、数据走共享内存,两条通道从 AHAL 到内核始终分离。

---

## 九、核心概念速查表

回头查名词时用这张表,配合前文的解释一起看:

| 概念 | 全称 | 一句话 |
|------|------|--------|
| **Stream** | — | PAL 里的一种 usecase(播放/录音/通话/热词) |
| **Device** | — | PAL 里的物理设备,按 id 全局单例共享 |
| **Session** | — | PAL 到下层的会话,分 tinyalsa 型和直连 AGM 型 |
| **AIF** | Audio Interface | AGM 里的后端(物理接口) |
| **GKV** | Graph Key Vector | 一串 kv,查 ACDB 图定义的主键,决定"用哪张图" |
| **CKV** | Calibration Key Vector | 决定"灌哪套校准" |
| **TKV** | Tag Key Vector | 按 tag 给某个模块设参数 |
| **MID/MIID** | Module (Instance) ID | 模块的类 / 运行图中的唯一实例 |
| **ACDB** | Audio Calibration Database | 图册 + 校准库,`acdb_ioctl` 查询 |
| **GSL** | Graph Service Layer | 图服务:GKV→查 ACDB→发 APM 命令 |
| **GPR** | Generic Packet Router | AP↔DSP 的带地址包路由协议 |
| **APM** | Audio Processing Manager | SPF 里的图总管 |
| **SPF** | Signal Processing Framework | DSP 上的处理框架(`libspf.so`) |
| **CAPI** | Common Audio Processing Interface | 每个 DSP 模块的统一 vtable |
| **AMDB** | Audio Module Database | 模块注册表,告诉 SPF 加载哪些库 |
| **SSR** | SubSystem Restart | DSP 崩溃重启,各层都有恢复逻辑 |

---

## 十、动手走读建议

如果你打算自己扒一遍代码,下面是一条能少走弯路的路线:

1. **从 PAL 入手,先追一条最简单的链**:`pal_stream_open(PAL_STREAM_LOW_LATENCY)` → `StreamPCM` → `Speaker` → `SessionAlsaPcm`。把这条链走通,骨架就有了。
2. **先读 XML,再读 `ResourceManager.cpp`**。路由的真相在 `pal/configs/<平台>/` 的 `resourcemanager_*.xml` 和 `mixer_paths_*.xml` 里,不在代码里。
3. **重点攻克"插件桥"这一层**(第四章)。PAL 只调 tinyalsa,是 AGM 插件冒充了声卡——想不通这一层,就会一直以为 PAL 直接连了硬件。
4. **把 GKV/CKV 当作贯穿全栈的线索**。PAL 的 `PayloadBuilder` 生成它,AGM 合并它,GSL 拿它查 ACDB,SPF 按查出的图执行。用 `grep` 追 `STREAMRX` / `DEVICERX` 这些 key,能看到它在每一层的样子。
5. **善用 grep 追调用链**,例如:
   ```bash
   grep -rn "pal_stream_open" pal/ --include=*.cpp
   grep -rn "gsl_open" agm/service/src/
   grep -rn "agm_session_open" agm/plugins/tinyalsa/src/
   ```
6. **官方 README 值得先扫一遍**:`pal/README.md`、`agm/README.md`、`ar-engine/README.md`。

---

*本文基于 CodeLinaro 开源代码走读整理,聚焦 vendor 栈的结构与核心机制。具体 API 签名、行号会随版本微调,一切以你手上的实际代码为准。*
