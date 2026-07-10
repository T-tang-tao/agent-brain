---
name: loop-engineering
description: "设计 Agent Loop(自动化循环系统)。触发词:设计 loop / 跑循环 / 自动化循环 / 定时跑 / 持续跑 / 让 agent 自己干 / 设计目标驱动 / loop engineering / 循环工程 / 跑 cron / 设自动化任务 / loop 模板。强制规则:必须有可验证停止条件(不是"做得更好")、必须有反馈闭环、状态写入外部文件而非上下文、避免三大陷阱(理解债/认知投降/Token 黑洞)、五要素齐全(Automations/Worktrees/Skills/Plugins/Sub-agents)+ State + Surface 分类(Locked/Editable/Append-only/Human-controlled)。"
version: 2.0.0
status: 可用
level: project
imported: 2026-07-10
updated: 2026-07-10
---

# Loop Engineering Skill

设计 Agent 自动化循环系统。

## 触发

- "设计 loop" / "跑循环" / "自动化循环" / "定时跑"
- "让 agent 自己干" / "loop engineering" / "循环工程"
- "设自动化任务" / "跑 cron" / "loop 模板"

## 强制规则

1. **可验证停止条件**。不是"做得更好",而是"测试通过 / lint clean / 命令 X 退出码 0 / 标量指标达阈值"。
2. **反馈闭环**。每轮结束后自己检查结果,继续或停止。
3. **状态写外部文件**(progress.md / AGENTS.md / Linear),**不写模型上下文**。
4. **最大迭代次数 + token 预算**,避免 Token 黑洞。
5. **批判性**,不要"认知投降"(照单全收 loop 输出)。
6. **四类表面(Surface)必须显式分类** — 见下方"七要素 + 一状态"。

## 七要素 + 一状态

按 [`references/five-elements.md`](./references/five-elements.md) + 表面分类检查:

| # | 要素 | 必选 | 表面分类 |
|---|------|------|---------|
| 1 | Automations(定时触发) | ✅ | Editable(调度参数)/ Human-controlled(生产 cron) |
| 2 | Worktrees(并行隔离) | 并行时 | Editable(单 worktree 内) |
| 3 | Skills(沉淀知识) | ✅ | Append-only(沉淀的经验)/ Editable(草稿) |
| 4 | Plugins/Connectors(外部工具) | 按需 | Locked(只读) |
| 5 | Sub-agents(写与审查分离) | 高风险时 | 见下条 |
| 6 | **Surface 分类(Locked / Editable / Append-only / Human-controlled)** | ✅ | **不可省略 — 防 reward hacking** |
| 7 | State(状态文件) | ✅ | Append-only(结果日志)/ Editable(进度) |

**Surface 分类是防 reward hacking 的核心机制**。Agent 写代码 + 自己改 eval = cheating,必须用表面切分挡住。详见 [`00-AgentBase/behavior/13-Harness-Engineering.md`](../../00-AgentBase/behavior/13-Harness-Engineering.md) § 1。

| 表面 | 例子 | 规则 |
|---|---|---|
| **Locked** | Eval 指标、rubric、验证脚本、合并策略 | Agent 可读、可提议改,**不能用改过的规则给自己打分** |
| **Editable** | skill 草稿、实验文件、prompt、待测 config | 循环内可改 |
| **Append-only** | 结果日志、研究线索、被拒的想法 | 只能追加,不能改写 |
| **Human-controlled** | 合并、生产部署、密钥、破坏性操作 | **必须显式人工批准** |

## Procedure

### 1. 评估适用性

对照 [`references/three-pitfalls.md`](./references/three-pitfalls.md) 判断任务是否值得做 loop:

| ✅ 适用 | ❌ 不适用 |
|--------|----------|
| 高度重复 | 一次性探索 |
| 强验证器 | 无客观验证 |
| 风险可控 | 生产核心 |
| Token 充足 | 预算紧张 |

不适用 → 拒绝或建议用 L1-L3(直接 prompt / 上下文 / harness)。

### 2. 设计 loop

按 [`references/template.md`](./references/template.md) 模板设计:

```
[Automation 触发]
   ↓
[读 State 文件]
   ↓
[分类 Surface:本次任务改什么?Locked 不动]
   ↓
[Worktree 隔离(可选)]
   ↓
[Sub-agent A 执行(只改 Editable)]
   ↓
[反馈验证(用 Locked eval)]
   ↓
[Sub-agent B 审查(可选,独立 verifier)]
   ↓
[Append-only 日志追加]
   ↓
[满足停止条件? → 是 → 停;否 → 回到执行]
```

### 3. 实现

按 Runtime 选择实现:

- **Claude Code**:`/loop` / `/goal` / hooks / GitHub Actions
- **Codex**: Automations tab + `/goal` + sub-agents TOML
- **Hermes**: cron + 中间件

### 4. 验证

对照 [`references/three-pitfalls.md`](./references/three-pitfalls.md) § 验证清单。

## Pitfalls

- ❌ 停止条件是模糊目标(无验证器)
- ❌ 状态存在对话上下文,而不是文件
- ❌ 没有最大迭代次数,允许无限循环
- ❌ 同一 agent 自己写 + 自己审查(自我评分)
- ❌ 并行 agent 没 worktree 隔离,文件冲突
- ❌ 用户不读 loop 产物(理解债膨胀)
- ❌ **Agent 自己改自己的 eval**(必须放 Locked 表面)
- ❌ **关键约束放 context 中间**(U 型注意力曲线导致中段被忽略)— 关键参数、停止条件、surface 分类放 SKILL.md 首尾

## Verification

完成 loop 设计后验证:

- [ ] 停止条件可被自动验证(测试/lint/退出码/标量指标)
- [ ] **四类表面显式分类**,Locked 表面 Agent 只读
- [ ] **关键约束(停止条件、surface 规则)放 SKILL.md 首尾,不在中间**
- [ ] **State 文件路径明确**(写到磁盘,不进 context)
- [ ] **Append-only 日志**:每轮追加,不覆盖
- [ ] 最大迭代次数已设
- [ ] Token 预算已设
- [ ] Sub-agent 写与审查分离(若适用)
- [ ] Worktree 隔离已配(若并行)
- [ ] 用户 review 节奏已定
- [ ] **Context 预算控制**:SKILL.md < 200 行,详细进 references/(按需加载)

## 上下文工程约束(本 SKILL 自身)

- **关键约束放首尾**:停止条件、表面分类、验证清单都已放在文档首尾
- **按需加载**:详细内容(five-elements / three-pitfalls / template)在 references/,只有关键词触发时读
- **总长 < 200 行**:本文件只放触发词 + 硬规则 + 流程骨架,详细靠引用
- 参考: [`00-AgentBase/behavior/09-Context-Engineering.md`](../../00-AgentBase/behavior/09-Context-Engineering.md) § 3 四大装配原则

## 详细参考

- **五要素详解**: [`references/five-elements.md`](./references/five-elements.md)
- **三陷阱详解**: [`references/three-pitfalls.md`](./references/three-pitfalls.md)
- **loop 模板**: [`references/template.md`](./references/template.md)
- **Surface 分类与 reward hacking**: [`00-AgentBase/behavior/13-Harness-Engineering.md`](../../00-AgentBase/behavior/13-Harness-Engineering.md)
- **Context 工程总论**: [`00-AgentBase/behavior/09-Context-Engineering.md`](../../00-AgentBase/behavior/09-Context-Engineering.md)
- **理论背景**: `00-AgentBase/knowledge/05-Loop-Engineering.md`
- **原文**: [addyosmani.com/blog/loop-engineering/](https://addyosmani.com/blog/loop-engineering/)