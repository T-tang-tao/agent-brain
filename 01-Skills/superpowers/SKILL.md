---
name: superpowers
description: >
  Complete software development methodology for coding agents. A composable skills
  library covering brainstorming, TDD, systematic debugging, code review, plan
  writing/execution, git worktrees, and subagent-driven development. Install as
  plugin/marketplace per runtime. Use when starting any development task that
  benefits from structured workflow.
version: 6.0.2
source: https://github.com/obra/superpowers
license: MIT
imported: 2026-07-09
---

# superpowers — 跨 Runtime 开发方法论技能集

## 来源信息

- **仓库**:https://github.com/obra/superpowers
- **作者**:Jesse Vincent / Prime Radiant
- **协议**:MIT
- **版本**:v6.0.2(2026-06-17)
- **入库日期**:2026-07-09

## 离线使用

本技能已完整下载到本地,所有文件在 `skills/` 目录下,无需联网即可使用。

完整目录结构:

```
superpowers/
├── SKILL.md                              # 本文件(入口)
├── references/                           # 入库参考资料
│   └── installation-per-runtime.md       # 各 runtime 安装方式(参考用)
├── skills/                               # ← 完整技能内容(离线可用)
│   ├── brainstorming/                    # SKILL.md + scripts/ + prompts
│   ├── dispatching-parallel-agents/      # SKILL.md
│   ├── executing-plans/                  # SKILL.md
│   ├── finishing-a-development-branch/   # SKILL.md
│   ├── receiving-code-review/            # SKILL.md
│   ├── requesting-code-review/           # SKILL.md + code-reviewer.md
│   ├── subagent-driven-development/      # SKILL.md + scripts/ + prompts
│   ├── systematic-debugging/             # SKILL.md + 8 个参考文件
│   ├── test-driven-development/          # SKILL.md + testing-anti-patterns.md
│   ├── using-git-worktrees/              # SKILL.md
│   ├── using-superpowers/               # SKILL.md + references/(3 个平台适配)
│   ├── verification-before-completion/   # SKILL.md
│   ├── writing-plans/                    # SKILL.md + plan-document-reviewer-prompt.md
│   └── writing-skills/                   # SKILL.md + 5 个参考文件 + examples/
├── hooks/                                # 跨 runtime 会话启动钩子
└── scripts/                              # 版本管理/同步/打包脚本
```

部署方式:把 `skills/` 目录复制到 Runtime 的技能目录,或用软链接指向。

## When to Use

- 开始任何软件开发任务时(brainstorming 会自动触发)
- 需要 TDD 流程时(test-driven-development)
- 需要系统化调试时(systematic-debugging)
- 需要写实现计划 / 执行计划时(writing-plans / executing-plans)
- 需要 code review 时(requesting / receiving-code-review)
- 需要并行子代理开发时(subagent-driven-development)
- 需要 git worktree 隔离开发时(using-git-worktrees)

**不适用**:
- 非编程任务(如知识库初始化、文档写作)
- 已有自己团队的开发流程,不需要 TDD/brainstorming 方法论

## What's Inside

Superpowers 包含 14 个技能,覆盖完整开发流程:

| 阶段 | 技能 | 作用 |
|------|------|------|
| 设计 | brainstorming | 苏格拉底式设计澄清,写代码前先搞清楚要做什么 |
| 规划 | writing-plans | 把设计拆成 2-5 分钟的任务,每个任务有精确文件路径和验证步骤 |
| 隔离 | using-git-worktrees | 创建隔离工作区,新分支上开发 |
| 执行 | executing-plans | 批量执行计划,带人工检查点 |
| 执行 | subagent-driven-development | 每个任务派发子代理,两阶段审查(规范合规 + 代码质量) |
| 执行 | dispatching-parallel-agents | 并发子代理工作流 |
| 测试 | test-driven-development | RED-GREEN-REFACTOR 循环 |
| 调试 | systematic-debugging | 4 阶段根因分析 |
| 调试 | verification-before-completion | 确认真正修复了 |
| 审查 | requesting-code-review | 预审查清单 |
| 审查 | receiving-code-review | 响应反馈 |
| 收尾 | finishing-a-development-branch | 合并/PR/保留/丢弃决策 |
| 元技能 | writing-skills | 如何编写新技能 |
| 元技能 | using-superpowers | 技能系统入口,会话启动时加载 |

## 核心工作流

```
brainstorming(设计澄清)
    ↓
using-git-worktrees(隔离工作区)
    ↓
writing-plans(拆解任务)
    ↓
subagent-driven-development 或 executing-plans(执行)
    ↕
test-driven-development(RED-GREEN-REFACTOR)
    ↓
requesting-code-review(代码审查)
    ↓
finishing-a-development-branch(收尾)
```

## 安装参考

> 以下命令仅供参考和更新时使用。本技能已完整入库,离线部署时直接复制 `skills/` 目录即可。

Superpowers 本身就是跨 runtime 的典范:同一个 `skills/` 源,通过各 runtime 的适配目录部署。

**核心设计**:canonical source(`skills/`)+ runtime adapters(`.claude-plugin/`、`.codex-plugin/` 等)

安装方式因 runtime 而异,详见 `references/installation-per-runtime.md`。

快速安装参考:

| Runtime | 安装命令 | 形态 |
|---------|---------|------|
| Claude Code | `/plugin install superpowers@claude-plugins-official` | Plugin |
| Codex CLI | `/plugins` → 搜索 superpowers | Plugin |
| Codex App | Plugins 面板 → Coding → Superpowers | Plugin |
| Cursor | `/add-plugin superpowers` | Plugin |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` | Extension |
| Kimi Code | `/plugins install https://github.com/obra/superpowers` | Plugin |
| OpenCode | 按 `.opencode/INSTALL.md` 指引 | Plugin |
| Factory Droid | `droid plugin install superpowers@superpowers` | Plugin |
| Antigravity | `agy plugin install https://github.com/obra/superpowers` | Plugin |
| Pi | `pi install git:github.com/obra/superpowers` | Package |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` | Plugin |

## 全局 vs 项目级

Superpowers 适合**全局安装**(跨项目通用方法论)。各 runtime 全局安装方式:

| Runtime | 全局位置 | 说明 |
|---------|---------|------|
| Claude Code | Plugin 安装即为全局 | `/plugin install` 默认全局生效 |
| Codex | Plugin 安装即为全局 | marketplace 安装默认全局 |
| Hermes | `~/.hermes/skills/` | 复制 skills/ 目录或配置 external_dirs |
| 其他 | 按 runtime 文档 | 多数 plugin 安装默认全局 |

详见 `references/installation-per-runtime.md` 和 [跨 Runtime 技能管理](../../../00-AgentBase/behavior/02-跨Runtime技能管理.md)。

## 来源

- **仓库**:https://github.com/obra/superpowers
- **作者**:Jesse Vincent / Prime Radiant
- **协议**:MIT
- **版本**:v6.0.2(2026-06-17)

## 相关知识

- [跨 Runtime 技能管理](../../../00-AgentBase/behavior/02-跨Runtime技能管理.md) — 同一技能源如何适配不同 runtime
- [如何编写 Skill](../../../00-AgentBase/behavior/01-如何编写Skill.md) — Skill 标准格式
- [概念全景辨析](../../../00-AgentBase/02-概念全景辨析.md) — Skill vs Plugin vs MCP 的区别

