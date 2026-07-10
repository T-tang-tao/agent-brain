# Claude Code IDE 与平台集成

> 同一引擎,多种入口——终端 CLI、VS Code、JetBrains、桌面应用、Web 浏览器、移动端、CI/CD、Slack。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / runtime |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-09 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | claude-code, ide, platform, ci-cd, integration |

---

## 多表面架构

所有表面连接同一 Claude Code 引擎,CLAUDE.md、设置和 MCP 服务器跨表面通用:

| 表面 | 形态 | 特点 |
|------|------|------|
| **终端 CLI** | 命令行交互 | 全功能,支持管道、脚本、CI |
| **VS Code** | 编辑器扩展 | 内联 diff、@提及、方案审查、对话历史 |
| **JetBrains** | IDE 插件 | 交互式 diff、选择上下文共享 |
| **桌面应用** | 独立应用 | 可视化 diff、多会话并行、定时任务 |
| **Web** | 浏览器 | 无需本地环境,长任务,并行任务 |
| **移动端** | iOS 应用 | 远程控制,随时继续 |

> **类比**:像"同一部电影的多种观影方式"——IMAX(桌面应用)、手机(移动端)、流媒体(Web)、影院终端(CLI)——内容一样,体验不同。

## 终端 CLI

全功能的命令行界面,遵循 Unix 哲学:

| 能力 | 说明 |
|------|------|
| 交互式会话 | `claude` 启动,支持多轮对话 |
| 非交互式查询 | `claude -p "query"` 查询后退出 |
| 管道处理 | `cat file \| claude -p "query"` |
| 会话恢复 | `claude -c` 继续,`claude -r "<id>"` 按 ID 恢复 |
| 斜杠命令 | `/help`、`/config`、`/mcp`、`/plan`、`/init` 等 |
| 后台代理 | `claude --bg "task"` 启动后台会话 |

## VS Code 集成

通过 VS Code 扩展提供编辑器内体验:

| 功能 | 说明 |
|------|------|
| 内联 diff | 代码变更以 diff 形式直接在编辑器中展示 |
| @提及 | 在对话中 `@文件名` 引用文件 |
| 方案审查 | plan 模式的方案在编辑器中审查 |
| 对话历史 | 查看和管理历史对话 |
| 权限模式切换 | 底部状态栏点击模式指示器 |

安装:在扩展商店搜索 "Claude Code",或 `Cmd+Shift+X` / `Ctrl+Shift+X`。

## JetBrains 集成

支持 IntelliJ IDEA、PyCharm、WebStorm 等 JetBrains IDE:

- 从 JetBrains Marketplace 安装插件
- 需要单独安装 Claude Code CLI
- 在 IDE 终端中运行,`Shift+Tab` 切换权限模式
- 交互式 diff 查看和选择上下文共享

## 桌面应用

独立应用,在 IDE 或终端之外运行:

| 功能 | 说明 |
|------|------|
| 可视化 diff | 图形化查看代码变更 |
| 多会话并行 | 并排运行多个会话 |
| 定时任务 | Desktop scheduled tasks,本地文件直接访问 |
| 会话移交 | `/desktop` 从终端移交到桌面应用 |

支持 macOS(Intel + Apple Silicon)、Windows(x64 + ARM64)。

## Web 浏览器

在浏览器中运行,无需本地环境:

| 场景 | 说明 |
|------|------|
| 长任务 | 启动后离开,完成后回来检查 |
| 远程仓库 | 处理不在本地的仓库 |
| 并行任务 | 同时运行多个任务 |

入口:[claude.ai/code](https://claude.ai/code)

## 移动端与远程控制

| 功能 | 说明 |
|------|------|
| Remote Control | 从手机或浏览器继续本地会话 |
| Dispatch | 从手机发任务,桌面应用创建会话 |
| Teleport | `claude --teleport` 将 Web/iOS 任务拉入终端 |
| Push 通知 | 长任务完成后推送到手机 |

## CI/CD 集成

| 平台 | 用途 |
|------|------|
| **GitHub Actions** | 自动 PR 审查、issue 分拣、代码审查 |
| **GitLab CI/CD** | 同上,GitLab 平台 |
| **GitHub Code Review** | 每个 PR 自动代码审查 |
| **Slack** | `@Claude` 提及,bug 报告转化为 PR |

```bash
# CI 中的非交互式用法(仅示意)
claude -p "review these changed files for security issues"
```

## 定时任务

| 类型 | 运行位置 | 特点 |
|------|----------|------|
| **Routines** | Anthropic 云端基础设施 | 电脑关机也运行,可触发于 API 调用或 GitHub 事件 |
| **Desktop 定时任务** | 本地机器 | 直接访问本地文件和工具 |
| **`/loop`** | CLI 会话内 | 快速轮询,会话内重复提示 |

## 会话跨表面迁移

会话不绑定单一表面,可在环境间移动:

```
终端会话 → /desktop → 桌面应用(可视化 diff)
终端会话 → Remote Control → 手机/浏览器继续
Web 任务 → claude --teleport → 终端继续
Slack @Claude → 自动创建 PR
```

## CLI 关键标志

| 标志 | 作用 |
|------|------|
| `--add-dir` | 添加额外工作目录 |
| `--agent` | 指定会话使用的 Agent |
| `--agents` | 动态定义子代理(JSON) |
| `--permission-mode` | 设置权限模式 |
| `--allowedTools` | 预批准工具列表 |
| `--disallowedTools` | 拒绝工具列表 |
| `--append-system-prompt` | 追加系统提示 |
| `--model` | 指定模型 |
| `--effort` | 设置努力级别(low/medium/high/xhigh/max) |
| `--max-turns` | 限制 agentic 轮数(非交互模式) |
| `--max-budget-usd` | 限制 API 花费上限 |
| `--bare` | 最小模式,跳过自动发现 |
| `--bg` | 后台代理启动 |

## 相关文件

- [Claude Code 概述](./01-概述.md) — 多表面架构概览
- [Claude Code 安装部署](./02-安装部署.md) — 各平台安装
- [Claude Code 配置体系](./03-配置体系.md) — 跨表面配置
- [Claude Code 架构设计](./12-架构设计.md) — 引擎内部结构
- [Agent 运行时与 CLI](../01-Agent运行时与CLI.md) — Runtime 通用概念
- [知识地图](../../03-知识地图.md) — Claude Code 在全景中的位置
- [根目录 AGENTS.md](../../../AGENTS.md) — 部署、编排与管理指南
