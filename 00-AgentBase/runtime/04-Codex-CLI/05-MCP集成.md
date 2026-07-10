# Codex MCP 集成

> Codex CLI 的 MCP 服务器配置：STDIO 与 HTTP 两种传输方式、OAuth 认证、工具过滤、按工具审批与插件提供 MCP。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / runtime / 04-Codex-CLI |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | codex, mcp, stdio, http, oauth, tool-filtering |

---

## MCP 概述

MCP（Model Context Protocol）是 Codex CLI 扩展工具能力的核心机制。通过连接外部 MCP 服务器，Codex 可以获得任意的自定义工具——数据库查询、API 调用、文件系统操作等。

```
┌─────────────┐      MCP 协议       ┌──────────────────┐
│  Codex CLI  │ ←──────────────────→ │  MCP Server      │
│  (MCP Host) │   STDIO / HTTP      │  (工具提供方)     │
└─────────────┘                      └──────────────────┘
```

## 两种传输方式

### STDIO 服务器

通过子进程通信，适合本地工具：

```toml
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
env = {}
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `command` | 是 | 启动命令 |
| `args` | 否 | 命令参数列表 |
| `env` | 否 | 环境变量映射 |

> **特点**：进程级通信，低延迟，适合本地工具。服务器生命周期由 Codex 管理。

### HTTP 服务器

通过 HTTP 通信，适合远程服务和 API：

```toml
[mcp_servers.github]
type = "http"
url = "https://mcp.github.com/sse"
```

或使用 Streamable HTTP：

```toml
[mcp_servers.remote-api]
type = "streamable-http"
url = "https://api.example.com/mcp"
```

| 字段 | 必需 | 说明 |
|------|------|------|
| `type` | 是 | `http` 或 `streamable-http` |
| `url` | 是 | 服务器 URL |
| `bearer_token` | 否 | Bearer Token 认证 |

> **特点**：跨网络通信，适合远程服务。可复用已有 HTTP 基础设施。

## CLI 添加 MCP 服务器

除了手动编辑配置文件，Codex 提供 CLI 命令快速添加：

```bash
# 添加 STDIO 服务器
codex mcp add <name> -- <command> [args...]

# 添加 HTTP 服务器
codex mcp add <name> --transport http --url <url>

# 列出已配置的服务器
codex mcp list

# 删除服务器
codex mcp remove <name>
```

示例：

```bash
# 添加文件系统 MCP 服务器
codex mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem /tmp

# 添加 GitHub MCP 服务器
codex mcp add github --transport http --url https://mcp.github.com/sse
```

## OAuth 认证

对于需要 OAuth 认证的 MCP 服务器：

```toml
[mcp_servers.google-drive]
type = "http"
url = "https://mcp.google-drive.example.com"
oauth = true
```

首次连接时，Codex 会引导用户完成 OAuth 授权流程，获取的 token 自动存储和刷新。

> **适用场景**：Google Drive、Notion、Slack 等需要 OAuth 的第三方服务。

## 工具过滤

MCP 服务器可能提供大量工具，但不是所有工具都需要暴露给 Agent。Codex 支持两种过滤方式：

### enabled_tools（白名单）

```toml
[mcp_servers.database]
command = "npx"
args = ["-y", "@mcp/postgres-server"]
enabled_tools = ["query", "list_tables"]    # 只暴露这两个工具
```

### disabled_tools（黑名单）

```toml
[mcp_servers.fs]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem"]
disabled_tools = ["delete_file", "move_file"]  # 隐藏危险工具
```

| 过滤方式 | 效果 | 适用场景 |
|----------|------|----------|
| `enabled_tools` | 只暴露列出的工具 | 最小权限原则 |
| `disabled_tools` | 隐藏列出的工具 | 排除危险工具 |

> **最佳实践**：优先用 `enabled_tools`（白名单），遵循最小权限原则。

## 按工具审批

配合 `granular` 审批策略，可以按工具配置审批行为：

```toml
approval_policy = "granular"

[mcp_servers.database]
command = "npx"
args = ["-y", "@mcp/postgres-server"]
enabled_tools = ["query", "list_tables", "delete_table"]

# 按工具配置审批
[mcp_servers.database.tool_approval]
query = "auto"           # 自动批准
list_tables = "auto"     # 自动批准
delete_table = "always"  # 总是需要确认
```

## 插件提供 MCP

Codex 插件可以自带 MCP 服务器，安装插件后自动注册：

```bash
# 安装插件
codex plugins install my-plugin

# 插件自带的 MCP 服务器自动可用
```

插件提供的 MCP 服务器在 `[mcp_servers]` 中以插件名命名空间自动注册，无需手动配置。

> **类比**：像 VS Code 扩展——安装即用，不需要手动配置服务器地址和认证。

## 完整 MCP 配置示例

```toml
# ~/.codex/config.toml

# 本地文件系统工具
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
enabled_tools = ["read_file", "write_file", "list_directory"]

# 远程 GitHub 工具
[mcp_servers.github]
type = "http"
url = "https://mcp.github.com/sse"

# 本地数据库工具（细粒度审批）
[mcp_servers.database]
command = "npx"
args = ["-y", "@mcp/postgres-server"]
enabled_tools = ["query", "list_tables", "delete_table"]

# Google Drive（OAuth）
[mcp_servers.gdrive]
type = "http"
url = "https://mcp.gdrive.example.com"
oauth = true
```

## 与 Hermes/Claude Code 的对比

| 特性 | Codex CLI | Hermes Agent | Claude Code |
|------|-----------|--------------|-------------|
| STDIO 支持 | 有 | 有 | 有 |
| HTTP 支持 | 有 | 有 | 有 |
| OAuth | 有 | 有 | 有 |
| 工具过滤 | 有（enabled/disabled） | 有（check_fn 门控） | 有 |
| 按工具审批 | 有（granular 策略） | 有 | 有 |
| 插件提供 MCP | 有 | 有（Plugin 系统） | 有 |
| 内置 MCP 目录 | 无（手动配置） | 有（agentskills.io） | 有 |

## 相关文件

- [Codex CLI 概述](./01-概述.md) — MCP 在核心特性中的位置
- [Codex 配置体系](./03-配置体系.md) — config.toml 中的 MCP 配置
- [Codex 安全与审批](./04-安全与审批.md) — granular 审批策略
- [Codex 自定义与技能](./06-自定义与技能.md) — MCP 在自定义构建顺序中的位置
- [Hermes MCP 集成](../02-Hermes-Agent/07-MCP集成.md) — Hermes 的 MCP 实现对比
- [概念全景辨析](../../02-概念全景辨析.md) — MCP 协议概念辨析
