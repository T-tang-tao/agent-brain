# Agent Wiki


它同时面向两类读者：

1. **人类新手**：先理解 Agent 是什么、Agent CLI 是什么、MCP、Skill、Plugin、Prompt、知识库分别是什么。
2. **未来 Agent**：让 Hermes Agent、Claude Code CLI Agent、Codex Agent 等在新环境中能读取这里的知识、规则、模板和迁移资产。

## 目录分工

本目录分为两类区域：

| 目录               | 类型  | 用途                                              |
| ---------------- | --- | ----------------------------------------------- |
| `00-AgentBase/`  | 知识区 | 解释 Agent 相关基础概念以及实践、理论，作为系统化 wiki               |
| `01-Skills/`     | 资产区 | 存放可直接使用或迁移的 skill                               |
| `02-Plugins/`    | 资产区 | 存放可直接使用或迁移的 plugin 资产                           |
| `03-Prompts/`    | 资产区 | 存放可复制使用的 agent prompt 模板                        |
| `04-MCP/`        | 资产区 | 存放 MCP 配置、MCP server 说明和连接方案                    |
| `05-Boundaries/` | 资产区 | 存放可执行的 agent 边界规则                               |
| `06-Migration/`  | 资产区 | 存放 Hermes、Claude Code、Codex 等 agent 迁移 playbook |

核心原则：

> `00-AgentBase/` 写知识解释；`01-*` 之后放可直接落地使用的资产。

如果想知道Agent知识库，先读 `00-AgentBase/`。  
如果要执行、迁移、复用，则去对应资产目录。

## 推荐阅读顺序

1. [00-目录索引](00-AgentBase/00-目录索引.md) — 看目录结构
2. [01-AgentBase总览](00-AgentBase/01-AgentBase总览.md) — 一句话理解整个知识库
3. [02-概念全景辨析](00-AgentBase/02-概念全景辨析.md) — 核心概念边界
4. [runtime/01-Agent运行时与CLI](00-AgentBase/runtime/01-Agent运行时与CLI.md) — Runtime 综述
5. [runtime/03-ClaudeCode](00-AgentBase/runtime/03-ClaudeCode/README.md) — Claude Code 专题(或 02-Hermes-Agent、04-Codex-CLI 任选)
6. [01-Agent边界与限制](00-AgentBase/safety/01-Agent边界与限制.md) — 边界
7. [01-Agent知识库设计](00-AgentBase/knowledge/01-Agent知识库设计.md) — 知识库本身
8. [03-知识地图](00-AgentBase/03-知识地图.md) — 回看全局

## 给未来 Agent 的说明

如果你是未来迁移进来的 agent，请先读取：

- [00-目录索引](00-AgentBase/00-目录索引.md)
- [03-知识地图](00-AgentBase/03-知识地图.md)
- 当前任务相关的资产区 README

不要把 `01-*` 之后的资产目录当成概念教程。概念解释统一在 `00-AgentBase/`。

## 当前阶段(2026-07-09)

知识库架构已完成 95%。各区状态:

| 区 | 内容 | 状态 |
|----|------|------|
| `00-AgentBase/` | 80+ 篇认知文档 | ✅ 完成 |
| `01-Skills/` | 9+ 个技能(kb-init / superpowers / ui-ux-pro-max / kimi-webbridge / agents-md-author / loop-engineering + 3 个第三方镜像) | ✅ 完成 |
| `02-Plugins/` | 3 个 plugin adapter | ✅ 完成 |
| `03-Prompts/` | 5 个 prompt 模板 | ✅ 完成 |
| `04-MCP/` | filesystem + obsidian MCP 配置 | ✅ 完成 |
| `05-Boundaries/` | 8 个边界策略 | ✅ 完成 |
| `06-Migration/` | 1 个 playbook(Claude Code → Hermes) | 🟡 进行中 |
| `99-Roadmap.md` | 进度 + 决策日志 + 审计 | ✅ 完成 |

**唯一未完成**:第七阶段"真实部署验证"——把上述资产装到 Claude Code / Hermes 里跑通。

详细路线、决策日志、敏感操作审计见 [99-Roadmap](99-Roadmap.md)。

## 快速开始

如果你想:

- **理解 Agent 是什么** → 读 [01-AgentBase总览](00-AgentBase/01-AgentBase总览.md)
- **初始化一个新知识库** → 触发 `kb-init` 技能
- **找开发方法论** → 看 [superpowers/SKILL.md](01-Skills/superpowers/SKILL.md)
- **做 UI/UX 设计** → 看 [ui-ux-pro-max/SKILL.md](01-Skills/ui-ux-pro-max/SKILL.md)
- **配置 Agent 系统 prompt** → 复制 [claude-code-agent-prompt.md](03-Prompts/claude-code-agent-prompt.md)
- **设置 Agent 边界规则** → 复制 [05-Boundaries/](05-Boundaries/) 下对应策略
- **跨 Runtime 迁移** → 跟 [claude-code-to-hermes.md](06-Migration/claude-code-to-hermes.md) 走

## 下次继续做什么

打开 `99-Roadmap.md` 看第七阶段:把 kb-init 部署到 Claude Code,验证"初始化知识库"触发流程。

