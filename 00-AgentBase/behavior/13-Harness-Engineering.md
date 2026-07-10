# Harness 工程

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | harness, surface, autonomy, eval, novelty, rollback, self-improvement |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

**Harness 是模型之外的控制层。** 决定 Agent 能编辑什么、如何收到反馈、状态写哪、失败怎么恢复、谁批不可逆操作。**Harness 才是产品,模型只是内核。**

---

## 1. 四类表面(Surface Classification)

| 表面 | 例子 | 规则 |
|---|---|---|
| **Locked** | Eval 指标、rubric、验证脚本、合并策略 | Agent 可读、可提议改,**不能用改过的规则给自己打分** |
| **Editable** | skill 草稿、实验文件、prompt、待测 config | 循环内可改 |
| **Append-only** | 结果日志、研究线索、被拒的想法 | 只能追加,不能改写 |
| **Human-controlled** | 合并、生产部署、密钥、破坏性操作 | **必须显式人工批准** |

**这是防 reward hacking 的核心机制** — Agent 自己改自己的 eval,就是 cheating,必须用 surface 切分挡住。

---

## 2. 紧反馈循环(Autonomy 的前提)

自治能工作的条件:反馈**快、无歧义、难被 game**。

**Karpathy `autoresearch` 极简模式**:
- 一个 editable 文件
- 一个 locked eval 文件
- 固定 wall-clock 预算
- 一个标量指标
- git rollback
- 持久结果日志

**对开放性研究 → skill 类工作**:
- 标量指标换成 locked rubrics
- 加确定性结构检查
- 加 source traceability
- 加 human review 阈值

**核心教训**:**模糊反馈 = 模糊自治**。反馈不清晰,Agent 不知道在优化什么。

---

## 3. 持久状态(Durable State)

长跑 Agent 必须**外化状态** — 计划、源队列、结果、失败、handoff 全写文件,让未来 Agent 接手不靠 chat 历史。

**Prime Intellect 自主 nanoGPT 工作的关键经验**:持久 scratchpad + `THREAD.md` 风格日志用于恢复、监控、审计。

**Append-only 日志记录**:
- 试过什么
- 什么有效 / 失败
- 为什么保留 / 丢弃 / 转入 review
- 检查了哪些上游源
- 下个 Agent 该做什么

---

## 4. 搜索纪律(Search Discipline)

Agent 倾向:利用最近表面、堆复杂度、少做 pruning。

**显式搜索规则**:
1. 定期刷新上游源
2. 大预算开销前做 novelty check
3. **保留被拒尝试**,防止重新发现
4. 多组件栈做 leave-one-out pruning
5. 质量相同时奖励简化
6. 晋升前独立 verification

---

## 5. 机制注册表(Mechanism Registry)

研究 → skill 类系统要**单独追踪已接受机制**,与散文分离。

**机制记录**应含:
- stable `mechanism_id`
- `owning_skill`
- `status`
- activation scenario
- behavior change
- evidence
- failure modes

**Novelty gates** 应对比机制注册表,而不是宽泛语料重叠 — keyword overlap 抓过时措辞,mechanism 比较抓真重复。

---

## 6. 自治治理(Governance)

Agent 可以**准备 PR**,但**治理必须显式**:

- ✅ 可起草改动
- ✅ 可跑检查
- ✅ 可写 PR 摘要
- ❌ **不**可自行 merge / deploy / push(除非用户对**该具体动作**显式授权)

---

## 7. Autoresearch-Style 循环

优化 artifact 对抗稳定 evaluator 的标准模式:

```
读 locked context → 选假设 → 改 allowed surface → commit/checkpoint
→ 跑 evaluator → 记结果 → 更好就保留 → 更差就 rollback
→ 重复
```

**必备属性**:
- Evaluator 在 editable surface 之外
- 反馈节奏固定到能比较尝试
- 失败尝试留审计 trail
- Rollback 便宜
- 有 crash / timeout 策略

---

## 8. 自改进循环(Self-Improvement Loops)

当 **harness / scaffold / workflow 本身成为优化目标** 时,问题从"怎么控制一个 loop"升级到"**怎么让 loop 改自己而不破坏引导它的信号**"。

### 8.1 核心约束

> **"The loop optimizes whatever signal it is given, including the signal's own weaknesses. Design the loop assuming the optimizer will find every gap between the metric and the intent."**

优化器一定会找到信号与意图的间隙。

### 8.2 必须的硬约束

| 约束 | 作用 |
|---|---|
| **Empirical two-split acceptance gate** | 拆出独立验证集,主集和验证集都通过才接受改动 |
| **Filesystem experience archives with raw traces** | 留原始轨迹,防止 context collapse |
| **Runtime-enforced constraints outside every editable surface** | 硬约束在 runtime 层,不能被 editable surface 触碰 |
| **Diversity preservation** | 显式保多样性,防止多样性坍缩到单一模式 |

### 8.3 何时启用自改进

**启用**:
- 任务重复性强、有清晰信号
- 已有可靠 locked evaluator
- 失败模式可观测、可分类

**不启用**:
- 任务每次都不一样
- 没有稳定信号
- 改了之后无法验证收益

### 8.4 诊断自改进循环退化

| 症状 | 根因 | 对策 |
|---|---|---|
| **Reward hacking** | 找到了信号与意图的间隙 | 拆验证集、加硬约束 |
| **Diversity collapse** | 所有候选趋同 | 加显式多样性奖励 |
| **Context collapse** | 历次经验被压缩,丢失有效失败模式 | 留 raw trace,只追加 |
| **Silent stagnation** | 表面指标在动,实质没改进 | 独立 verifier / human review |

---

## 9. 与本知识库其他章节的关系

- **09-Context-Engineering.md**:Harness 决定 context 预算和分配
- **11-Multi-Agent-Patterns.md**:Supervisor/Worker 各自有 surface 切分
- **04-记忆机制(Memory).md**:Memory 写入是 Locked / Editable 表面
- **10-Filesystem-Context.md**:持久状态用 filesystem
- **05-评估方法(Evaluation).md**:Evaluator 是 Locked 表面

---

## 10. 工程化检查清单

- [ ] 是否明确划分四类表面?
- [ ] Locked 表面是否在 Agent 可写范围之外?
- [ ] 反馈循环是否快、无歧义、难 game?
- [ ] 状态是否外化(写文件,不只是 context)?
- [ ] 日志是 append-only 吗?
- [ ] 搜索纪律是否显式(novelty check / leave-one-out pruning)?
- [ ] PR / 合并 / 部署是否需要人工批准?
- [ ] 自改进循环是否满足硬约束(two-split / raw trace / runtime-enforced / diversity)?
- [ ] 是否独立 verifier 防 sycophancy?
- [ ] Rollback 是否便宜(git / snapshot)?

---

## 11. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| Agent 自己改 eval | Eval 跟 editable 混在一起 | Eval 放 locked,Agent 可读不可写 |
| 反馈循环靠 chat 文本 | 状态只在 context,context 没了就丢 | 外化到文件,跨 session 可恢复 |
| 试过 100 次只留最优 | 失败经验丢,下次重新发现 | Append-only 日志保留所有尝试 |
| 自治 PR 自合并 | Agent 部署到生产 | 必须人工批准(用户显式授权例外) |
| 自改 harness 退化成奖励 hacking | 信号和意图间隙被利用 | Two-split + 独立 verifier |
| 多组件堆叠 | 只看总指标,不知道哪个有效 | Leave-one-out pruning |

---

## 12. 相关知识

- [上下文工程总论](./09-Context-Engineering.md)
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)
- [Tool 设计](./12-Tool-Design.md)
- [记忆机制](./04-记忆机制(Memory).md)
- [文件系统 Context](./10-Filesystem-Context.md)
- [评估方法](./05-评估方法(Evaluation).md)