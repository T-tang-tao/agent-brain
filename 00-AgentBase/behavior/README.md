# Behavior — 行为

> 知识地图模块:**Behavior** — Prompt、Skill、Planner、Memory、Evaluation、Observability

## 这个目录放什么

关于 Agent 行为机制的全部认知:
- **Prompt**:当前怎么行动
- **Skill**:某类任务怎么做
- **Planner**:规划-执行-反思循环(ReAct / Plan-and-Execute / Reflection)
- **Memory**:短期/长期/实体/知识图谱(从 knowledge 移过来)
- **Evaluation**:系统性度量 Agent 表现
- **Observability**:日志/追踪/监控/告警(从 safety 移过来)

| 编号 | 文档 | 回答什么 |
|------|------|----------|
| 01 | [如何编写 Skill](./01-如何编写Skill.md) | 怎么编写一个 Skill?格式是什么? |
| 02 | [跨 Runtime 技能管理](./02-跨Runtime技能管理.md) | 同一个技能在不同 runtime 里怎么管理? |
| 03 | [规划循环(Planner)](./03-规划循环(Planner).md) | Agent 的规划循环有几种模式?ReAct / Plan-Execute / Reflection 怎么选? |
| 04 | [记忆机制(Memory)](./04-记忆机制(Memory).md) | 五层记忆体系(working / short-term / long-term / entity / temporal KG)+ 框架选型 + 整合策略 |
| 05 | [评估方法(Evaluation)](./05-评估方法(Evaluation).md) | 多维 rubric + 确定性检查 + LLM-as-judge + 五大偏差缓解 |
| 06 | [可观测性(Observability)](./06-可观测性(Observability).md) | 怎么让 Agent 行为可审计?日志、追踪、监控、告警 + Context 健康度信号 |
| 08 | [Agent 架构模式](./08-Agent架构模式.md) | 最小 Agent 回路 + 多 Agent 模式 + BDI 心智模型 |
| 09 | [上下文工程](./09-Context-Engineering.md) | U 型注意力曲线 + 五种失败模式 + 装配原则 + 压缩优化 |
| 10 | [文件系统 Context](./10-Filesystem-Context.md) | 五大 Filesystem Pattern(scratch pad / plan persistence / sub-agent 通信 / 动态加载 / 即时发现) |
| 11 | [Multi-Agent 架构模式](./11-Multi-Agent-Patterns.md) | 三大主导模式(supervisor / swarm / hierarchical)+ Latent Briefing + BDI |
| 12 | [Agent Tool 设计](./12-Tool-Design.md) | 合并原则 + 架构降级 + Description 必答四问 + Schema 一致性 |
| 13 | [Harness 工程](./13-Harness-Engineering.md) | 四类表面 + 紧反馈循环 + 持久状态 + 搜索纪律 + 自改进循环 |
| 14 | [LLM 项目开发方法论](./14-LLM-Project-Development.md) | Task-Model Fit 6/6 + 5 阶段流水线 + 成本估算 + 单 vs 多 Agent |
| 15 | [托管 Agent 基础设施](./15-Hosted-Agents.md) | 三层架构 + 沙箱三件套(镜像 / 预热池 / 快照)+ Server-First 框架 |

## 与根级文档的关系

- 根级 `02-概念全景辨析.md` 已覆盖概念辨析(Skill 是什么、和 Tool/MCP 的区别)
- 本目录展开行为层面的深入认知(怎么写、怎么设计、怎么评估)
- Hermes 中 Skill 的实现细节见 [Hermes 技能系统](../runtime/02-Hermes-Agent/05-技能系统.md)

## 未来计划

- System Prompt 的设计原则
- Planner 模式在各 Runtime 的实现差异
- 评估自动化与基准测试套件