# 上下文工程(Context Engineering)

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | context, attention, optimization, degradation, compression |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

上下文工程 = **为单次推理组装"最小高信号 token 集"** 的工程学科。模型在推理中途无法补充注意力,所以每个 token 都在挤占预算;目标是最大化单位 token 效用,不是堆信息。

---

## 1. 基础:Context 是什么

Context = 模型在一次推理中可见的全部状态:

- System instructions
- Tool definitions(JSON schema 通常比纯文本膨胀 2-3 倍)
- Retrieved documents(RAG 结果、文件内容)
- Message history(对话 + scratchpad)
- Tool outputs(往往是 agent context 的最大占用者)

**核心立场**:Context 是**有限的注意力预算**,不是存储桶。

---

## 2. 注意力机制:三大约束

| 约束 | 性质 | 工程含义 |
|---|---|---|
| **硬 token 限制** | 模型架构定死的窗口 | 超过直接截断 |
| **有效容量上限** | 名义窗口之下,实际能稳定召回的 token 数 | 假设有效容量远低于标称窗口,直到在自己任务上实测 |
| **U 型注意力曲线** | 开头和结尾位置召回率高,中间位置召回率低 10-40% | 关键约束放首尾,中间放可丢失的内容 |

**U 型曲线的成因**:第一个 token(BOS)会变成"attention sink",吸走大量注意力预算,导致中间 token 欠关注。这个 >4K token 时显著。

---

## 3. 四大装配原则

设计 context 时强制遵循:

1. **Informativity over exhaustiveness** — 只放对当前决策有用的;其他内容设计成"按需检索"
2. **Position-aware placement** — 关键约束放首尾,绝不放中间
3. **Progressive disclosure** — 启动时只加载 skill 名称 + 描述;被触发后才加载完整内容
4. **Iterative curation** — 每次把内容喂给模型前都要重新审视,不是写一次就完事

**信号密度测试**:对每段 context,问"删掉这段,模型输出会变吗?"——不会就删。冗余内容不仅浪费 token,还会**主动稀释**对高信号内容的注意力。

---

## 4. Context 五种失败模式(可识别 + 可恢复)

Context 退化是**连续的**,不是二值的。当作工程问题处理,有明确信号和对策。

### 4.1 Lost-in-Middle(信息存在但被忽略)

- **检测**:正确信息在 context 里但模型输出与之矛盾 / "忘记"早期指令
- **机制**:U 型曲线;长文档中段信息召回率低
- **对策**:
  - 关键信息放首尾
  - 长文档前置摘要 + 附加结论
  - 加 section header / 结构标记当 attention anchor

### 4.2 Context Poisoning(错误信息自我强化)

- **检测**:输出质量突然降级、工具调用错位、纠错后仍持续 hallucination
- **机制**:hallucination / tool error / 错误检索结果进入 context 后被反复引用,下游决策全部基于错误前提
- **对策**:
  - **不叠加修正** — 截断到污染点之前,或重启用已验证 context
  - 追踪 claim provenance,检测到污染立即熔断
  - 验证所有外部输入后再入 context

### 4.3 Context Distraction(无关信息争抢注意力)

- **检测**:即便只有一个无关文档,任务性能也显著降级
- **机制**:阶跃函数(不是线性)— 一个 distractor 就够;模型无法"跳过"
- **对策**:
  - 加载前做相关性过滤
  - 把"可能用到但当前不需要"的内容放工具后面,**按需检索**而不是预先加载

### 4.4 Context Confusion(多任务混在 context)

- **检测**:工具调用不符合当前任务、约束被错位套用
- **机制**:context 里混了多种任务类型 / 切换目标,模型合并了错误约束
- **对策**:
  - 显式任务分段,不同任务用独立 context window(用 sub-agent 隔离)

### 4.5 Context Clash(多个正确但矛盾的来源)

- **检测**:模型无法判定哪个版本 / 视角生效
- **机制**:版本冲突、视角冲突、多源检索结果矛盾
- **对策**:
  - 显式标出矛盾,定 source precedence
  - 旧版本在进入 context 前过滤

---

## 5. 优化:Context 预算与压缩

### 5.1 三大目标

| 目标 | 指标 | 备注 |
|---|---|---|
| 减少 token 总量 | tokens/request | 不是单一追求 |
| 提高信号密度 | useful info / total tokens | 信号密度测试 |
| **优化 tokens-per-task** | 完成任务的累计 token | **真正应该优化的目标** |

### 5.2 优化技术

| 技术 | 做法 | 适用场景 |
|---|---|---|
| **Compaction(压缩)** | 在接近限制时总结 context | 长会话 |
| **Observation masking(观察遮罩)** | 工具输出处理后用引用代替原文 | 工具输出占大头时 |
| **Prefix caching** | 复用跨请求的 KV blocks | System prompt + 静态前缀 |
| **Context partitioning** | 拆工作到独立 sub-agent | 多任务、context 太大 |

### 5.3 压缩(Compaction)要点

压缩是**强制手段**(会话耗尽时),但要注意:

- 正确优化目标是 **tokens-per-task**,不是 tokens-per-request
- 结构化摘要(显式 sections:files / decisions / next steps)保留的信息 > 激进压缩
- **Artifact trail integrity 是所有压缩方法最弱的维度** — 设计时要保留可追溯性
- handoff 摘要标准 sections:**Session Intent / Files Modified / Decisions Made / Current State / Next Steps / Open Questions**

---

## 6. 渐进式披露(Progressive Disclosure)三层次

实现 context 按需加载,避免一次性堆进窗口:

1. **Skill 选择层** — 启动时只加载 name + description;激活时再加载完整 SKILL.md
2. **文档加载层** — 先加载摘要,需要时再加载具体 section
3. **工具结果保留** — 近期结果保留完整;远期结果压缩或驱逐

**关键原则**:激活时**全量加载**而不是部分加载。部分加载造成混乱缺口,降低推理质量。

---

## 7. 工具输出与历史管理

| 场景 | 策略 |
|---|---|
| Tool output 占大头 | 一次处理后用引用代替原文(masking) |
| 长会话 Message history | 监控增长;定期 compaction |
| 早期 tool calls 的原始结果 | 用 compact summary / 文件引用替代 |
| 过期 tool outputs | 驱逐或压缩,释放注意力 |

---

## 8. 工程化检查清单

设计 context 时强制自检:

- [ ] 关键约束放首尾,没放中间?
- [ ] 加载的内容删掉会改变模型输出吗?(信号密度测试)
- [ ] 工具集是否最小化?有没有合并重叠工具?
- [ ] 长文档是否前置摘要 + 附加结论?
- [ ] 是否有"按需检索"机制,把可选内容从 context 挪到工具后?
- [ ] 是否避免了部分加载(要么全量,要么不加载)?
- [ ] Chunking 切在自然语义边界,不是任意字符数?
- [ ] Tool outputs 是不是被 observation masking 收缩过?
- [ ] 跨任务切换时是否启用独立 context(sub-agent)?
- [ ] 多个正确但矛盾的来源是否标了 precedence?

---

## 9. 与本知识库其他章节的关系

- **harness-engineering**(13 章):Context 预算和隔离是 harness 设计的子集
- **multi-agent-patterns**(11 章):Context 隔离正是 sub-agent 的主要目的
- **memory-systems**(并入 04 章):跨 session 持久 context 用 memory,不是塞当前 context
- **filesystem-context**(10 章):把大容量内容从 context 挪到文件系统
- **tool-design**(12 章):精简工具集是减少 context 占用最直接的办法
- **evaluation**(05 章):Context 相关的失败模式有评测方法可量化

---

## 10. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| System prompt | 平铺一长段,关键约束放中间 | XML/Markdown 分 section,关键约束放首尾 |
| 工具集 | 5 个工具功能重叠 | 合并到 1-2 个清晰边界的工具 |
| 文档检索 | 把 5 个相关文档全塞进 context | 1 个摘要 + 1 个直击问题的详情,其余放工具后面 |
| 长会话 | 历史原样保留到结束 | 周期性 compact,旧 tool outputs 替换为引用 |
| 多任务 | 同一 context 切换任务 | 任务分段,sub-agent 独立 context |
| 错误恢复 | 叠加修正"模型,刚才那个答案是错的,正确是..." | 截断到错误前,重启用干净 context |

---

## 11. 相关知识

- [Harness 工程](./13-Harness-Engineering.md)— context 隔离、harness 表面
- [文件系统 Context](./10-Filesystem-Context.md)— 把大容量内容挪出 context
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)— sub-agent 隔离 context
- [记忆机制](./04-记忆机制(Memory).md)— 跨 session 持久化
- [Tool 设计](./12-Tool-Design.md)— 减少工具集膨胀
- [规划循环](./03-规划循环(Planner).md)— context 在循环中的角色