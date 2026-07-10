# Agent 记忆机制(Memory)

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v2.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼 + 旧版分类体系) |
| 标签 | memory, working, short-term, long-term, entity, knowledge-graph, consolidation |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) · 上一版(2026-07-09) |

---

## 一句话理解

记忆 = 让 Agent **跨 session 持续积累知识、维持身份一致性、按需检索历史** 的持久层。从易失的 context window 到持久存储,选择最浅的层,直到简单层不够用才加深。

---

## 1. 记忆五层(由浅到深)

| 层级 | 持久性 | 实现 | 何时用 |
|---|---|---|---|
| **Working** | 仅当前 context | system prompt 里的 scratchpad | 始终 — 用 attention 友好位置优化 |
| **Short-term** | 当前 session | 文件系统、内存缓存 | 中间工具结果、对话状态 |
| **Long-term** | 跨 session | KV 存储 → 向量库 | 用户偏好、领域知识、实体注册 |
| **Entity** | 跨 session | 实体注册 + 属性 | 维持身份("John Doe" = 跨会话同一人) |
| **Temporal KG** | 跨 session + 历史 | 带 validity 区间的图 | 随时间变化的事实、time-travel 查询、防止 context clash |

**默认选最浅的层**;只有检索质量降级 / 需要多跳推理 / 需要关系遍历 / 需要时序查询时才升到下一层。

---

## 2. 框架选型(主流生产框架)

| 框架 | 架构 | 最适合 | 权衡 |
|---|---|---|---|
| **Mem0** | 向量库 + 图记忆 + 可插拔后端 | 多租户、广泛集成 | 多 Agent 场景不专 |
| **Zep/Graphiti** | 时序知识图、双时态模型 | 企业、需要关系建模 + 时序推理 | 高级功能云端锁定 |
| **Letta** | 自编辑记忆(in-context/core/archival 分层) | 深度 Agent 自省、有状态服务 | 简单场景复杂度高 |
| **Cognee** | 可定制 ECL pipeline 的多层语义图 | 自演进 Agent 记忆、多跳推理 | 摄取阶段处理重 |
| **LangMem** | LangGraph 工作流的记忆工具 | 已在 LangGraph 上的团队 | 强耦合 LangGraph |
| **File-system** | 纯文件 + 命名约定 | 简单 Agent、原型 | 无语义搜索、无关系 |

**选型原则**:
- 要 bi-temporal → Zep/Graphiti
- 要 fast time-to-production → Mem0
- 要深度自省 → Letta
- 要多跳 + 丰富关系 → Cognee
- 要长时任务(>1h)+ 跨 session → 至少 Long-term
- 简单 Agent / 原型 → File-system 起步

---

## 3. 检索策略

| 策略 | 适用 | 局限 |
|---|---|---|
| **Semantic**(embedding 相似度) | 直接事实查询 | 多跳推理降级 |
| **Entity-based**(图遍历) | "关于 X 的一切" | 需要图结构 |
| **Temporal**(validity 过滤) | 随时间变化的事实 | 需要 validity metadata |
| **Hybrid**(语义 + 关键字 + 图) | 最佳综合准确率 | 基础设施最重 |

**关键**:根据查询形状选策略,不要一个通用方法包打天下。

---

## 4. 记忆整合(Memory Consolidation)

记忆无限增长会降级检索质量,必须周期性整合。

**核心原则**:**失效但不删除** — 保留历史以支持时序查询回溯过去状态。

**触发条件**:
- 记忆数量超阈值
- 检索质量降级
- 定时任务

**整合策略**:
- 合并重复 / 相似条目
- 把过时信息打 `valid_until` 标记而不是删
- 频繁访问的提升权重
- 长尾访问的降权或归档

---

## 5. 与 Context 的关系

**永远按需加载记忆到 context,不要预加载全量**。理由:

- 大 context payload 昂贵,降级注意力质量
- 记忆的目的是"必要时候能查到",不是"永远占位置"
- 取到的记忆放 attention 友好位置(开头 / 结尾)

**失败恢复顺序**:
1. Empty retrieval → 放宽搜索条件(去 entity 过滤、扩时间窗);仍空则向用户澄清
2. Stale results → 检查 `valid_until` 时间戳;大量过期则先整合
3. Conflicting facts → 优先 `valid_from` 最新的;置信度低时向用户明示冲突
4. Storage failure → 写入排队重试;**永远不阻塞 Agent 响应**

---

## 6. 与本知识库其他章节的关系

- **09-Context-Engineering.md**:记忆的物理载体是 context,按 U 型曲线位置放置
- **10-Filesystem-Context.md**:同 session 内的"伪记忆"用 filesystem,跨 session 才是真记忆
- **11-Multi-Agent-Patterns.md**:Sub-agent 之间的共享信息用 shared files,而非共享 memory
- **13-Harness-Engineering.md**:Memory 写入可以是 locked / editable 表面 — 决定 Agent 能否改自己的记忆

---

## 7. 升级路径(从浅到深)

| 阶段 | 触发升级的条件 | 升级到 |
|---|---|---|
| **1. 原型** | (起点) | File-system:JSON + timestamp |
| **2. 扩展** | 需要语义搜索 / 多租户隔离 | Mem0 或带 metadata 的向量库 |
| **3. 复杂推理** | 需要关系遍历 / 时序 / 跨会话综合 | Zep/Graphiti |
| **4. 完全自控** | Agent 必须自管记忆 + 深度自省 | Letta 或 Cognee |

**铁律**:**Day-1 不需要时序知识图**。先 File-system,跑通后看真实瓶颈,再加结构。

---

## 8. 工程化检查清单

- [ ] 记忆写入是否记录 `valid_from` / `valid_until` 时间戳?
- [ ] 是否按需加载,而不是预加载到 context?
- [ ] 取出的记忆是否放 attention 友好位置?
- [ ] 整合策略是"失效"而非"删除",保留历史?
- [ ] 整合有触发条件(数量 / 质量 / 定时)?
- [ ] 失败恢复路径明确(空 / 过期 / 冲突 / 存储失败)?
- [ ] 多 Agent 共享用 shared files,不是共享 memory?
- [ ] 记忆写入是 harness 的哪类表面(Locked / Editable)?

---

## 9. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| Agent 跨 session 失忆 | 完全无持久层 | 至少 Long-term KV |
| Day-1 选时序 KG | 复杂度爆炸,运维成本高 | File-system 起步,按需升级 |
| 记忆无限增长 | 从不整合,检索质量降级 | 数量 / 质量阈值触发整合 |
| 加载全量记忆 | 占用全部 context,降级注意力 | 按需检索,放首尾位置 |
| 错误覆盖正确事实 | 直接 update 旧值 | 写新 fact + `valid_until` 旧 fact |
| 共享状态 | 多个 Agent 共享同一 memory 库 | Sub-agent 共享用 shared files |

---

## 10. 相关知识

- [上下文工程总论](./09-Context-Engineering.md)— context 物理约束
- [文件系统 Context](./10-Filesystem-Context.md)— 同 session 内"伪记忆"
- [Harness 工程](./13-Harness-Engineering.md)— 记忆写入的表面分类
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)— 共享信息用 shared files

---

## 11. 变更记录

- v2.0.0 (2026-07-10):基于 memory-systems 提炼,引入五层体系、框架选型表、整合策略、与 context 集成的失败恢复顺序;旧的四类分类(v1.0.0)被并入"按用途分"的视角
- v1.0.0 (2026-07-09):初版,四类分类(短时 / 长时 / 程序 / 声明)