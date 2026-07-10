# Runtime — 运行时

> 知识地图模块:**Runtime** — Agent CLI 的安装、部署与使用(运维视角);Runtime 提供的机制能力(可观测、记忆、规划循环等)见 [behavior/](../behavior/README.md)

## 这个目录放什么

关于 Agent 运行环境的认知(运维视角):
- Agent Runtime / Harness / CLI 是什么
- 不同 Runtime 的安装、配置与使用
- 主流 Agent 工具(Hermes / Claude Code / Codex)的具体认知
- **项目级配置**:资产层 → Runtime 项目级目录的部署映射

## 已有文档

### 通用概念

| 文档 | 回答什么 |
|------|----------|
| `00-项目级配置.md` | 怎么把资产层(`01-Skills/` 等)的技能/MCP 部署到 Runtime 项目级目录(`.trae/` `.claude/` `.hermes/` 等)? |
| `01-Agent运行时与CLI.md` | Runtime / Harness / CLI 是什么?为什么同一个模型在不同 CLI 表现不同? |
| `05-多Agent使用指南.md` | 三个 Runtime 的多 Agent **使用**指南:单 Runtime 内怎么用 + 跨 Runtime 怎么协作 |

### 专题子目录

| 子目录 | 内容 |
|--------|------|
| `02-Hermes-Agent/` | Hermes Agent 完整知识库(11 篇专题文档:概述/安装/配置/工具/技能/记忆/MCP/网关/Cron/安全/架构) |
| `03-ClaudeCode/` | Claude Code 完整知识库(12 篇专题文档:概述/安装/配置/工具/技能/记忆/子代理/MCP/Hooks/权限安全/IDE集成/架构) |
| `04-Codex-CLI/` | Codex CLI 完整知识库(7 篇专题文档:概述/安装/配置/安全审批/MCP/自定义技能/架构) |

## 未来计划

- Context Manager 的压缩与保留策略
- Permission System 的分级设计
- Sandbox 与隔离机制
- 各 Runtime 项目级配置的对比矩阵