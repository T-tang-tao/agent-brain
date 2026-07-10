---
层级: 认知层
分类: 00-AgentBase / paradigm
状态: 已发布
版本: v1.0.0
创建: 2026-07-10
标签: loop-engineering, automation, orchestration, paradigm
---

# Loop Engineering(循环工程)

> L4 抽象层。设计目标驱动的迭代闭环,让 Agent 自主持续地把活干完。

## 一句话定义

**Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead.**

> 循环工程是取代你自己作为提示 Agent 的人。你设计那个做这件事的系统。

— Addy Osmani, [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) (2026-06-07)

## 起源与时间线

| 时间 | 人物 | 贡献 |
|------|------|------|
| 2022 | Princeton + Google | 提出 **ReAct 模式**(Reason + Act),loop 的理论基础 |
| 2025 下半年 | Reflexion 论文 | 失败后用自然语言反思,把反思存进记忆,改进下一次尝试 |
| 2026-05-06 | **Boris Cherny**(Anthropic,Claude Code 负责人) | 访谈:"I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do." |
| 2026-06 | **Peter Steinberger**(OpenClaw 创建者) | 推文:"You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."(790 万浏览) |
| 2026-06-07 | **Addy Osmani**(Google Chrome 前工程负责人) | 发表长文 [Loop Engineering](https://addyosmani.com/blog/loop-engineering/),**正式命名 + 系统化定义** |

## Loop 的本质

在 Agent 语境里,**loop(循环)** 指不断重复的周期:

```
Agent 执行一个动作
       ↓
   观察环境反馈
       ↓
  根据反馈决定下一步
       ↓
   终止条件被满足? ──否──→ (回到执行)
       ↓是
     停止
```

与链式(chain)的区别:

| 维度 | Chain | Loop |
|------|-------|------|
| 路径 | 线性(A→B→C) | 动态(A→B→失败→重试 B 或换 A) |
| 决策 | 顺序写死 | 根据反馈调整 |
| 终止 | 步骤跑完即结束 | 满足终止条件才结束 |
| 适用 | 已知流程 | 需要反复试错的任务 |

## 五要素 + 一个状态

一个完整的 loop 需要 5 个组件 + 1 个状态文件:

| # | 要素 | 在 loop 中的作用 |
|---|------|----------------|
| 1 | **Automations** | 定时发现和分诊任务 |
| 2 | **Worktrees** | 并行隔离,防止文件冲突 |
| 3 | **Skills** | 沉淀项目知识,避免每次重新解释 |
| 4 | **Plugins / Connectors** | 接外部工具(MCP / 内部系统) |
| 5 | **Sub-agents** | 写一个,另一个查(避免自我评分) |
| 6 | **State** | 状态文件,记录做了什么、下一步做什么 |

### 五要素在两个 Runtime 中的对应

| 要素 | Codex | Claude Code |
|------|-------|-------------|
| Automations | Automations tab + `/goal` | Scheduled tasks, `/loop`, `/goal`, hooks, GitHub Actions |
| Worktrees | Built-in worktree per thread | `git worktree`, `--worktree`, `isolation: worktree` |
| Skills | `SKILL.md`, `$name` 触发 | `SKILL.md`, description 自动匹配 |
| Plugins / Connectors | Connectors (MCP) + plugins | MCP servers + plugins |
| Sub-agents | TOML in `.codex/agents/` | `.claude/agents/`, agent teams |
| State | Markdown / Linear via MCP | `AGENTS.md`, progress 文件 |

## 三大核心(Addy Osmani)

1. **可验证的停止条件** — 不是"做得更好",而是"测试通过"
2. **反馈闭环** — 每轮结束后自己检查,继续或停止
3. **状态记忆** — 外部文件,不是模型上下文

## 三大陷阱

| 陷阱 | 表现 | 对策 |
|------|------|------|
| **理解债(comprehension debt)** | Loop 越顺,你越不读自己代码 | 定期 review loop 产物 |
| **认知投降(cognitive surrender)** | 放弃判断,照单全收 loop 输出 | 保持批判性,设计 loop 时带着判断力 |
| **Token 黑洞** | Loop 无脑跑下去,账单无限增长 | 设置最大迭代次数 + token 预算 |

## 适用 vs 不适用

| ✅ 适用 | ❌ 不适用 |
|--------|----------|
| 高度重复的日常任务 | 一次性探索任务 |
| 存在强验证器(测试/lint/type check) | 无客观验证标准(架构合理性/可读性) |
| 风险可控(内部工具/一次性报告) | 生产环境核心代码 |
| Token 预算充足 | 个人开发者 / 预算有限 |

## 与本知识库资产对应

| Loop 要素 | 本知识库资产 |
|----------|------------|
| Automations | 根 `AGENTS.md` § 6.2 生命周期管理;`03-Prompts/hermes-agent-prompt.md` |
| Worktrees | 知识库暂无专门文档(可补充) |
| Skills | `01-Skills/` 7 个技能集(1730 文件) |
| Plugins / Connectors | `02-Plugins/` + `04-MCP/` |
| Sub-agents | 根 `AGENTS.md` § 4 编排 |
| State | `AGENTS.md` + `99-Roadmap.md` |

## 一个具体的 loop 实例(Addy Osmani 模板)

```text
1. Automation 每天早上跑:
   prompt = "调用 $triage 技能,读昨天的 CI failures、open issues、recent commits"
   产物写入 progress.md 或 Linear

2. 对每个发现项:
   a. 开一个独立 worktree
   b. 派 sub-agent A(实施者)写修复
   c. 派 sub-agent B(审查者)对照 skill 规范审查 A 的产出
   d. 通过 → 提交 PR,更新 Linear ticket
   e. 不通过 → 回到 a

3. 无法处理的任务 → 进 Triage inbox 等人工

4. progress.md 记录每天的尝试、结果、未完项
   (明天早上的 run 自动从这里接续)
```

## 中文社区的反对声音

[CSDN 评论](https://blog.csdn.net/2601_96073073/article/details/162460627) 认为这是"新名词包装":

- 三大主角动机不纯(Boris 推广自家产品、Peter 蹭热度、Addy 抢定义权)
- 本质就是 cron + 循环调用 agent
- 过度包装,实务上意义有限
- 三件真正重要的事:可验证的停止条件、反馈闭环、状态记忆

**取舍**:概念可以借,但不要被新词绑架。重点是**三核心**(停止/反馈/状态)+ **三陷阱**(理解债/认知投降/Token 黑洞)的实操。

## 与三层架构的映射

| 层 | 抽象 | Loop 中的位置 |
|----|------|--------------|
| L1 Prompt | 单次表达 | Loop 内每一轮仍需要 Prompt |
| L2 Context | 信息环境 | State 文件 + Skills 提供 |
| L3 Harness | 运行环境 | Worktrees + Plugins + Sub-agents |
| **L4 Loop** | 迭代闭环 | **包含前三层,加上 Automations** |

## 相关

- [00-工程范式总览.md](./00-工程范式总览.md) — 四层范式完整对照
- [Addy Osmani 原文](https://addyosmani.com/blog/loop-engineering/) — 概念源头
- [`../../01-Skills/loop-engineering/SKILL.md`](../../01-Skills/loop-engineering/SKILL.md) — 设计 loop 的强制 Skill
- [`../../02-Plugins/`](../../02-Plugins/README.md) — Loop 用到的 plugin adapter