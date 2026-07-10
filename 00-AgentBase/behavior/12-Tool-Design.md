# Agent Tool 设计

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | tool, schema, mcp, consolidation, namespace, error-recovery |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

Agent-facing 工具 = **确定性与非确定性之间的合同**。和人类 API 不同,Agent 不能读文档问问题,只能从 description 推断意图并生成匹配调用。**每个含糊都是失败模式,prompt 调不回来**。

---

## 1. 三大核心原则

### 1.1 合并优于拆分(Consolidation)

> "If a human engineer cannot definitively say which tool should be used in a given situation, an agent cannot be expected to do better."

- 多个重叠窄工具 → 合并成一个端到端工作流工具
- 反例:不要 `list_users` + `list_events` + `create_event` 三个;要 `schedule_event`(内部查可用性 + 预定)
- 优势:消除选择歧义、减少 description 占 context、去掉 chain 顺序负担

**何时不合并**:
- 行为本质不同
- 必须独立调用
- 合并后参数爆炸,反而难调

### 1.2 架构降级(Architectural Reduction)

把"合并原则"推到极致:**移除大多数专门工具,只暴露原始通用能力**(filesystem / shell),让 Agent 用标准 Unix 工具自己组合。

**何时降级优于复杂**:
- 数据层有良好文档、结构一致
- 模型推理能力足够
- 维护复杂工具的 scaffold 时间 > 实际收益

**何时不降级**:
- 数据层混乱、缺文档
- 领域需专门知识模型缺
- 安全约束必须限制 Agent 行动
- 操作确实从结构化工作流中受益

### 1.3 Description = Prompt

**工具 description 不是给人类读的文档**,是被注入 agent context 的指令。每个字要么帮 Agent 选对,要么误导它选错。

---

## 2. Description 必备四问

每个工具 description 必须回答:

1. **做什么** — "列出今日所有事件"(不要"管理事件的工具")
2. **何时用** — 直接触发("用户问价格") + 间接信号("需要当前市场费率")
3. **接受什么输入** — 每个参数的 type / 约束 / 默认值 / 格式示例
4. **返回什么** — 输出结构、字段、错误情况

**反模式**:"Search the database"(含糊)+ 神秘参数名 → Agent 瞎猜 → 错误调用

---

## 3. Schema 一致性

| 要素 | 规则 | 反例 |
|---|---|---|
| 命名 | `verb_noun` 模式(get_customer, create_order) | getInfo, doIt |
| 参数名 | 全工具统一(customer_id 永远是 customer_id) | 有时 id 有时 identifier |
| 返回字段 | 跨工具一致 | user_name vs customerName vs uname |
| 命名空间 | 按域前缀(db_*, web_*, file_*) | 扁平列表,Agent 难路由 |

**命名空间价值**:Agent 看名字能路由到一组,不必评估全部。规模越大收益越高。

---

## 4. 响应格式选项

工具应提供简洁 / 详细两种格式:

- **concise** — 只回核心字段,适合确认 / 列表
- **detailed** — 完整对象,适合需完整 context 决策

Description 文档化何时用哪种,让 Agent 学会选。

---

## 5. 错误消息设计

错误消息有两个受众:开发者调试、Agent 自纠。

**对 Agent,错误必须 actionable**:

- ❌ `"failed"` — 零恢复信号
- ✅ `"Customer not found. Available: ['C001', 'C002']. Retry with one of these IDs."`

**应包含**:
- 重试指引(可重试时)
- 修正后的格式示例(输入错时)
- 缺失字段(请求不全时)

---

## 6. 默认值

设默认值匹配常见用例:

- 减少 Agent 参数负担
- 防止漏参数错误
- 让 Agent 不必理解所有选项也能成功调用

---

## 7. MCP 设计要点

MCP server 是工具聚合层,设计原则继承上述全部:

- 一个 MCP server 暴露的工具集应该**主题一致**(全是数据库、全是 web)
- 工具命名跨 server 一致
- 错误消息统一格式
- Description 包含 server 来源标识

---

## 8. 减少工具集的实战信号

工具集臃肿的标志:
- Agent 选错工具频率高
- Description 总 token > 2000
- 多个工具功能有重叠
- 用户反馈"我以为它会调用 X,它调用了 Y"

**对策**:合并 + 降级 + 删冗余。**17 个工具 → Agent 选错一半**;**3 个工具 → 几乎不选错**。

---

## 9. 与本知识库其他章节的关系

- **09-Context-Engineering.md**:合并工具是减少 context 占用的最直接方式
- **11-Multi-Agent-Patterns.md**:Worker 工具集最小化、专一化
- **13-Harness-Engineering.md**:Tool 调用是 harness 的可执行表面
- **10-Filesystem-Context.md**:降级到 filesystem + 标准工具的根据

---

## 10. 工程化检查清单

- [ ] 工具 description 是否回答了四问(做啥 / 何时用 / 输啥 / 出啥)?
- [ ] 是否有重叠工具可以合并?
- [ ] 命名是否符合 `verb_noun` + 命名空间?
- [ ] 参数名是否跨工具一致?
- [ ] 错误消息是否 actionable,提供重试 / 修正指引?
- [ ] 是否有简洁 / 详细两种响应格式?
- [ ] 是否有不必要的工具可以删?
- [ ] 默认值是否合理(匹配常见用例)?
- [ ] 工具集总 description token 是否在 2000 以内?
- [ ] 是否考虑降级到 filesystem + 标准工具?

---

## 11. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| 17 个工具,Agent 选错一半 | 继续加,调 prompt | 合并到 3-5 个清晰边界工具 |
| Description 含糊 | "Search the database" | "Search products by name/ID; returns matching items with price/stock; format: {sku, name, stock}" |
| 错误只说 failed | Agent 卡住 | "Field 'customer_id' missing. Required. Example: 12345" |
| 工具命名混乱 | getInfo, doIt, search2 | get_customer, search_orders, list_invoices |
| 全部 detailed | 列表场景也返回大对象 | 提供 concise / detailed 选项,Agent 选 |
| 数据层有良好文档 | 写专门工具读 schema | 暴露 filesystem,Agent 用 cat/grep 探索 |

---

## 12. 相关知识

- [上下文工程总论](./09-Context-Engineering.md)— 工具膨胀占 context
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)— Worker 工具最小化
- [Harness 工程](./13-Harness-Engineering.md)— Tool 调用是可执行表面
- [文件系统 Context](./10-Filesystem-Context.md)— 架构降级的备选