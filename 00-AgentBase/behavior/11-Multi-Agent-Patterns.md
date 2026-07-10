# Multi-Agent 架构模式

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | multi-agent, supervisor, swarm, hierarchical, latent-briefing, bdi |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

**Sub-agent 的存在目的是隔离 context,不是模拟组织角色。** 三大主导模式:supervisor / swarm / hierarchical。选哪个看协调需求,不看"组织结构像不像样"。

---

## 1. 为什么需要多 Agent

| 原因 | 描述 |
|---|---|
| **Context 瓶颈** | 单 agent context 装不下所有任务信息,出现 lost-in-middle / 注意力稀缺 / poisoning |
| **并行加速** | 独立子任务并行,总时长 ≈ 最长子任务,而非求和 |
| **专业化** | 每个 agent 只装自己所需的 system prompt + 工具 + context,注意力不被无关配置稀释 |

**Token 经济现实**:多 agent 系统 token 成本远高于单 agent。要"先测单 agent 基线,再决定要不要拆"。模型升级往往比加 agent 收益更大。

---

## 2. 三大主导模式

### 2.1 Supervisor / Orchestrator(中心化)

```
User → Supervisor → [Specialist₁, Specialist₂, Specialist₃] → 聚合 → Output
```

**适用**:
- 任务有清晰分解
- 需要跨域协调
- 需要人在环监督

**权衡**:
- ✅ 严格工作流、易接入 human-in-the-loop
- ❌ Supervisor context 成瓶颈
- ❌ Supervisor 失败级联到所有 worker
- ❌ **Telephone game 问题**:Supervisor 转述子 Agent 响应,失真(LangGraph 基准显示未优化版本比优化版差 ~50%)

**Telephone game 缓解**:`forward_message` 工具让子 Agent 直接回用户,绕过 Supervisor 转述。

### 2.2 Peer-to-Peer / Swarm(去中心化)

任意 agent 可通过显式 handoff 把控制权转给另一个。

**适用**:
- 探索性任务
- 死板规划反而碍事
- 子 Agent 能独立完成响应

**权衡**:
- ✅ 灵活、消除转述失真
- ❌ 全局状态难追踪
- ❌ 调试复杂

### 2.3 Hierarchical(分层)

多层抽象(strategy / planning / execution),每层有自己的 context。

**适用**:
- 大型项目
- 分层抽象明显(战略 / 战术 / 执行)
- 每层关注点不同

**权衡**:
- ✅ 清晰关注点分离
- ❌ 多层传递会放大失真
- ❌ Token 消耗最大

---

## 3. 关键设计原则

无论哪种模式,所有多 agent 系统都应围绕:

- **显式协调协议** — 不能靠"希望"对齐
- **抵抗谄媚的共识机制** — Sycophancy 是大模型默认行为,要硬约束
- **失败处理防止级联** — 一个 worker 挂了不能拖垮全部

---

## 4. Latent Briefing(KV 共享)

### 4.1 问题

分层多 agent 系统常"为同一 context 付两次钱":

- Orchestrator 累积长轨迹
- Worker 收到窄文本 handoff(subtask prompt + 文档片段)

**缓解方案对比**:

| 方案 | 弱点 |
|---|---|
| LLM 摘要 | 高延迟、信息有损、不能保证保留下一子任务所需 |
| RAG 检索 | 依赖 chunking + embedding,可能漏掉跨块 / 跨步依赖 |
| **传完整轨迹** | 成本随每次 worker 调用放大,无关 context 降级 worker 质量 |

### 4.2 解决思路

**Latent Briefing** = 在表征层(worker 模型的 KV cache)共享 memory,而不是文本层。

核心:**Attention Matching (AM) KV cache compaction** — 让小 cache 的 attention 输出逼近完整 cache。

针对多 agent 推理的三个修改:
1. 用 **task-guided query vectors**(从当前 worker prompt 派生)
2. 聚合分数到 **shared global mask**(而不是 per-head 独立子集)
3. 用 **median + τ × MAD** 鲁棒阈值(不是固定 top-k per head)

### 4.3 适用条件

| 满足 | 不满足 |
|---|---|
| 能拿到 worker 模型内部 KV tensors | API-only 栈(用 summary/RAG 替代) |
| Orchestrator 已有任务特定 state 要传给 worker | 只是文档检索问题 |
| 想避免 worker 重复处理 orchestrator 已推理过的内容 | 一般 prefix caching 足够 |

### 4.4 公开结果

参考结果:长文档 QA 上报告显著 worker token 减少 + 总 token 节省 + 低位单数秒级 compaction 开销。**作为 workload-specific evidence,不是普适保证**。

---

## 5. BDI 心智模型(简)

**BDI** = Belief-Desire-Intention,形式化 agent 心智状态。

### 5.1 何时用

- 需要**可解释推理链**(审计 / 法规合规)
- 多 agent 平台间**语义互操作**
- 跟踪信念 / 愿望 / 意图的时序演化
- 神经符号 AI(LLM + 形式逻辑)集成

**何时不用**:普通上下文 / 记忆管理(用 `04-记忆机制.md` 就够)。

### 5.2 核心概念

| 类别 | 类型 | 含义 |
|---|---|---|
| **Endurants(持续状态)** | Belief | agent 持有的世界事实 |
| | Desire | agent 想实现的目标,必须链回 belief |
| | Intention | agent 承诺执行的计划,必须 fulfill desire |
| **Perdurants(过程事件)** | BeliefProcess | 感知 → belief 形成 |
| | DesireProcess | belief → 动机生成 |
| | IntentionProcess | 选定 desire → 承诺 |

### 5.3 认知链模式

用双向属性把 B/D/I 串成有向链:

```turtle
:Belief_store_open a bdi:Belief ;
    bdi:motivates :Desire_buy_groceries .

:Desire_buy_groceries a bdi:Desire ;
    bdi:isMotivatedBy :Belief_store_open .

:Intention_go_shopping a bdi:Intention ;
    bdi:fulfils :Desire_buy_groceries ;
    bdi:isSupportedBy :Belief_store_open .
```

**价值**:
- 前向推理(下一步该做什么)
- 后向追溯(为什么这样做)

---

## 6. 协调失败模式

| 失败 | 原因 | 缓解 |
|---|---|---|
| **Telephone game** | Supervisor 转述失真 | forward_message 绕过 / 切到 swarm |
| **Cascading failure** | Worker 失败级联 | 显式失败处理 + 隔离 context |
| **Consensus by sycophancy** | 多个 agent 互相迎合 | 硬约束(独立 verifier / 评分制) |
| **Context drift across handoff** | 关键信息在传递中丢失 | structured handoff 文件 + provenance |
| **Token explosion** | 递归调用放大 context | Latent Briefing 或 deep context partitioning |

---

## 7. 与本知识库其他章节的关系

- **09-Context-Engineering.md**:Sub-agent 隔离是 context 优化的高阶实现
- **10-Filesystem-Context.md**:Sub-agent 之间用 shared files 通信,而非共享 memory
- **04-记忆机制(Memory).md**:跨 session 持久化用 memory;同 session 跨 agent 用 shared files
- **13-Harness-Engineering.md**:Surface 分类对 supervisor/worker 适用
- **12-Tool-Design.md**:Worker 工具集要最小化、专一化

---

## 8. 工程化检查清单

- [ ] 多 agent 真的必要?已对比单 agent + 更好模型
- [ ] Supervisor 是否有 `forward_message` 避免 telephone game?
- [ ] 协调协议是否显式定义(不靠"希望")?
- [ ] Worker 失败是否被隔离(不级联)?
- [ ] 子 Agent context 是否独立,不互相污染?
- [ ] Sub-agent 通信用 shared files 还是有显式 protocol?
- [ ] KV 共享条件满足吗(能拿内部 tensors)?
- [ ] 共识机制是否抗 sycophancy(独立 verifier)?
- [ ] BDI 形式化只在需要审计 / 互操作时用,不滥用?

---

## 9. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| 任务略复杂 | 立刻拆 5 个 sub-agent | 先单 agent + 好模型,看瓶颈 |
| Supervisor 转述 | 让 Supervisor 总结 worker 结果 | forward_message 直达 |
| Worker 互相迎合 | 投票选最高分 | 独立 verifier 评分 |
| 多 Agent 共享同一 memory | 全员写同一库 | Sub-agent 用 shared files 通信 |
| 任务规划多 Agent 写一段 | 各自独立思考,无协议 | 显式 handoff 协议 + provenance |
| 跨 session 共享 | 用 sub-agent 通信 | 用 memory(跨 session) |

---

## 10. 相关知识

- [上下文工程总论](./09-Context-Engineering.md)— context 物理约束
- [文件系统 Context](./10-Filesystem-Context.md)— sub-agent 通信
- [Harness 工程](./13-Harness-Engineering.md)— surface 分类
- [记忆机制](./04-记忆机制(Memory).md)— 跨 session vs 同 session 区分
- [Tool 设计](./12-Tool-Design.md)— Worker 工具最小化