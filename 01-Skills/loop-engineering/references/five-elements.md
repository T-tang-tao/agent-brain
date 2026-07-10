# Loop 五要素详解

> 一个完整 loop 需要 5 个组件 + 1 个状态文件。每个要素都有"它在 loop 里做什么、两个 Runtime 怎么实现"两部分。

## 1. Automations(定时触发)

**作用**:让 loop 真正成为 loop,而不是只跑一次的脚本。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | `/loop <间隔>` / `/goal <条件>` / hooks / GitHub Actions / Routines |
| Codex | Automations tab(选项目 + prompt + cadence + 环境) + `/goal` |
| Hermes | cron 表达式 + 中间件 |

**检查清单**:
- [ ] 触发条件明确(时间 / 事件 / webhook)
- [ ] 触发结果有归宿(Triage inbox / Linear / 文件)
- [ ] 失败后会自动归档,不堵塞下次

## 2. Worktrees(并行隔离)

**作用**:多个 agent 同时工作时文件不冲突。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | `git worktree` / `--worktree` flag / subagent `isolation: worktree` |
| Codex | Built-in worktree per thread |
| Hermes | 手动创建 worktree |

**检查清单**:
- [ ] 每个并行 agent 在独立 worktree
- [ ] worktree 用完自动清理
- [ ] worktree 之间共享 git 历史

**何时必选**:
- 多个 agent 同时改同一仓库
- 并行做多个 feature
- 长任务可能与用户手动操作冲突

**何时可省**:
- 单 agent 串行任务
- 任务之间无文件冲突

## 3. Skills(沉淀知识)

**作用**:把项目知识写成 SKILL.md,避免每次 loop 都重新解释。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | `SKILL.md`,description 自动匹配 |
| Codex | `SKILL.md`,`$name` 触发或隐式匹配 |

**检查清单**:
- [ ] description 紧凑、可匹配
- [ ] 技能覆盖项目特有的约定、构建步骤、踩过的坑
- [ ] 技能可被 loop 内 prompt 调用

**为什么关键**:Addy Osmani 的 "intent debt" 概念——agent 每次启动都是冷的,会自己填空(用自信的猜测)。Skill 是写到外部的意图。

## 4. Plugins / Connectors(外部工具)

**作用**:loop 不只是看文件系统,还要接你的真实工具。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | MCP servers + plugins |
| Codex | Connectors (MCP) + plugins |

**检查清单**:
- [ ] 必要的工具已接(issue tracker / DB / staging API / Slack)
- [ ] MCP server 配置在仓库内可复现
- [ ] 权限最小化(只给需要的 scope)

**为什么关键**:这是 "loop 真的能做" 而不是 "loop 告诉你该怎么做" 的分界。

## 5. Sub-agents(写与审查分离)

**作用**:写代码的 agent 不要自己评分自己。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | `.claude/agents/` TOML + agent teams |
| Codex | `.codex/agents/` TOML(每个有 name/description/instructions/optional model) |

**检查清单**:
- [ ] 实施 agent 和审查 agent 是不同的 prompt(甚至不同的 model)
- [ ] 审查 agent 有明确的对标(规范 / 测试 / 既有代码)
- [ ] token 成本:sub-agent 消耗更高,只在值得的地方用

**为什么关键**:这是 loop 在你**不看着的时候**能不出大错的唯一保障。

## 6. State(状态文件)

**作用**:模型会忘记,但磁盘不会。

| Runtime | 实现方式 |
|---------|---------|
| Claude Code | `AGENTS.md` / `progress.md` / 通过 MCP 接 Linear |
| Codex | Markdown 文件 / 通过 connector 接 Linear |

**检查清单**:
- [ ] 文件路径明确,所有 sub-agent 知道去哪读
- [ ] 写入是原子的(避免半写状态)
- [ ] 每次 loop 结束都更新
- [ ] 历史保留(可回溯)

**最小 State 文件结构**:

```markdown
# Progress — <loop 名称>

## 当前迭代
- 轮次: N
- 任务: <当前任务描述>
- 状态: 进行中 / 失败 / 成功

## 已完成
- [时间戳] <完成的任务 1>
- [时间戳] <完成的任务 2>

## 失败记录
- [时间戳] <失败的任务 + 原因 + 重试策略>

## 下一步
- <next action>
```

## 五要素最小组合

如果只能选 3 个最关键的:

| 优先级 | 要素 | 原因 |
|--------|------|------|
| 1 | **Automations** | 没有它就不是 loop,只是单次脚本 |
| 2 | **State** | 没有它 loop 第二天醒来忘记昨天的事 |
| 3 | **Skills** | 没有它 loop 每次重新学习项目 |

Worktrees / Plugins / Sub-agents 是规模化时的必要补充。