# Agent 架构模式

## 一句话解释

Agent 架构模式描述一个 Agent 如何从目标出发,经过规划、工具调用、观察反馈和验证,最终完成任务。

模型只是推理核心。真正的 Agent 由模型、运行时、工具、上下文、记忆、边界和验证共同组成。

## 最小 Agent 回路

```text
目标
  ↓
理解上下文
  ↓
规划下一步
  ↓
调用工具或生成答案
  ↓
观察结果
  ↓
修正计划
  ↓
验证完成
```

这个回路是否能稳定运行,比单次回答质量更重要。

## 常见架构模式

| 模式 | 适用场景 | 优点 | 风险 |
|---|---|---|---|
| 单轮问答 | 简单解释、翻译、总结 | 成本低、延迟短 | 无法处理长任务 |
| 工具调用 Agent | 查询、读写文件、调用 API | 能接触外部世界 | 工具边界和错误处理复杂 |
| ReAct | 边想边查边做 | 适合探索型任务 | 容易循环、上下文膨胀 |
| Plan-and-Execute | 明确目标、多步骤任务 | 结构清晰、便于审计 | 计划过早固定会失真 |
| Reflection | 生成后自检修正 | 提升复杂任务质量 | 可能把错误解释得更像真的 |
| Multi-Agent | 分工、评审、并行探索 | 能处理大任务 | 协调成本和状态冲突高 |
| Workflow + Agent | 固定流程中嵌入智能判断 | 稳定可控 | 灵活性受流程限制 |
| Human-in-the-loop | 高风险操作、需求不清 | 安全、可追责 | 速度慢、体验依赖人 |

## Agent 与 Workflow 的组合

真实系统通常不是“纯 Agent”或“纯 Workflow”,而是组合:

| 部分 | 用 Workflow | 用 Agent |
|---|---|---|
| 权限校验 | 是 | 否 |
| 任务分派 | 是 | 可选 |
| 文件检索 | 可选 | 是 |
| 代码修改 | 可选 | 是 |
| 发布审批 | 是 | 否 |
| 异常解释 | 可选 | 是 |

原则:确定性、合规性、可审计的步骤交给 Workflow;需要理解、判断、综合、生成的步骤交给 Agent。

## 角色拆分

复杂 Agent 系统可以按职责拆分:

| 角色 | 职责 |
|---|---|
| Coordinator | 拆任务、分派、汇总、做最终取舍 |
| Researcher | 检索资料、阅读代码、收集证据 |
| Implementer | 执行改动、运行验证 |
| Reviewer | 找缺陷、评估风险 |
| Operator | 部署、监控、回滚 |
| Memory Curator | 判断哪些经验值得长期保存 |

不要为了“多 Agent”而多 Agent。只有当任务能明确分工、结果可合并、并行能减少风险或时间时才拆。

## 状态管理

Agent 系统至少要管理四类状态:

| 状态 | 内容 | 常见位置 |
|---|---|---|
| 会话状态 | 当前任务、上下文、工具结果 | Runtime 上下文 |
| 工作状态 | 当前计划、待办、阻塞点 | plan / task board |
| 长期记忆 | 用户偏好、项目经验、稳定规则 | memory / wiki |
| 外部系统状态 | 文件、数据库、任务、工单 | 工具或 MCP 暴露 |

状态不清会导致重复执行、误判完成、覆盖他人工作。

## 架构选择原则

1. 能用单轮解决的,不要引入 Agent 回路。
2. 能用固定 Workflow 保证正确性的,不要交给自由生成。
3. 需要读写外部世界时,先设计工具边界和权限。
4. 需要长期复用时,把经验沉淀为 Skill 或知识库。
5. 高风险动作必须有人类确认或可回滚机制。
6. 多 Agent 先定义交付物格式,再分工。

## 常见失败模式

| 失败模式 | 表现 | 防线 |
|---|---|---|
| 目标漂移 | 做着做着偏离原需求 | 计划和完成定义 |
| 工具滥用 | 能回答的问题也频繁调用工具 | 工具选择规则 |
| 上下文污染 | 旧任务、无关文件影响判断 | 上下文裁剪 |
| 过度自主 | 需求不清也直接改 | 澄清策略 |
| 验证缺失 | 只改不测 | 完成检查清单 |
| 状态冲突 | 多 Agent 覆盖彼此结果 | 所有权和锁定规则 |

## 相关文件

- [规划循环](./03-规划循环(Planner).md)
- [记忆机制](./04-记忆机制(Memory).md)
- [开发型 Agent 工作协议](./07-开发型Agent工作协议.md)
- [多 Agent 使用指南](../runtime/05-多Agent使用指南.md)
- [Agent 边界与限制](../safety/01-Agent边界与限制.md)

---

## 多 Agent 架构(Multi-Agent Patterns)

当单 Agent context 装不下任务,或子任务可并行,考虑多 Agent。**核心原则:sub-agent 的存在目的是隔离 context,不是模拟组织角色。**

三大主导模式:

| 模式 | 适用 | 代价 |
  |---|---|---|
  | **Supervisor / Orchestrator** | 任务有清晰分解,需人在环 | Supervisor context 成瓶颈,Telephone game 失真 |
  | **Peer-to-Peer / Swarm** | 探索性 / 子 Agent 能独立完成响应 | 全局状态难追踪,调试复杂 |
  | **Hierarchical** | 大型项目,关注点分层 | 多层传递放大失真,token 消耗最大 |

**Telephone game 缓解**:Supervisor 转述子 Agent 响应会失真 ~50%(LangGraph 基准)。用 orward_message 工具让子 Agent 直达用户,绕过 Supervisor。

**Latent Briefing**(KV 共享):用 worker 模型的 KV cache 共享 orchestrator 状态,避免传完整轨迹的 token 爆炸。

完整内容见 [Multi-Agent 架构模式](./11-Multi-Agent-Patterns.md)。

## 心智模型(Mental States)

需要可解释推理链或语义互操作时,用 **BDI(Belief-Desire-Intention)** 形式化心智状态:

- **Belief**:agent 持有的世界事实
- **Desire**:agent 想实现的目标(必须链回 belief)
- **Intention**:agent 承诺执行的计划(必须 fulfill desire)

认知链用双向属性(motivates / isMotivatedBy、ulfils / isFulfilledBy)支持前向推理 + 后向追溯。

**适用**:审计 / 法规合规 / 多 agent 平台语义互操作 / 神经符号 AI。**不适用**:普通上下文管理(用 [Context 总论](./09-Context-Engineering.md) 就够)。

## 子 Agent 引入决策

**默认单 Agent + 好模型**。拆多 Agent 之前必须证明:

- 任务超过单 context 容量
- 子任务可清晰并行
- 收益 > 多 Agent 的 token 倍增 + 协调开销

**经验法则**:多 Agent token 成本可比单 Agent 高数倍。如果加 Agent 没带来 2 倍以上质量提升,就是浪费。模型升级往往比加 Agent 收益更大。
- [Agent 边界与限制](../safety/01-Agent边界与限制.md)