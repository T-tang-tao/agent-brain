# Hermes MCP 集成

> Hermes Agent 的 MCP(Model Context Protocol)集成——连接外部工具服务器扩展能力。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / runtime / 02-Hermes-Agent |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | hermes, mcp, model-context-protocol |

---

## MCP 提供什么

MCP(Model Context Protocol)让 Hermes 无需等待核心工具更新即可接入外部工具生态：

- 无需先写原生 Hermes 工具即可访问外部工具生态
- 本地 stdio 服务器和远程 HTTP MCP 服务器在同一配置中
- 启动时自动工具发现和注册
- 支持 MCP resources 和 prompts 的实用工具包装
- 按服务器过滤，只暴露实际需要的工具

> 类比：MCP 像"USB 接口"——任何符合协议的设备（工具服务器）都能即插即用，Hermes 不用为每个工具单独开发驱动。

## 两种 MCP 服务器

### Stdio 服务器

本地子进程，通过 stdin/stdout 通信：

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

### HTTP 服务器

远程端点，直接连接：

```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer ***"
```

### OAuth 认证的 HTTP 服务器

设置 `auth: oauth`，Hermes 处理 OAuth 2.1 的发现、动态客户端注册、PKCE、令牌交换和刷新。

支持远程/无头主机：paste-back 方式或 SSH 端口转发。

## mTLS / 客户端证书

支持三种形式：

| 形式 | 格式 | 说明 |
|---|---|---|
| 单个合并 PEM 路径 | `"path/to/combined.pem"` | 证书与私钥合并在一个文件 |
| [cert, key] 二元组 | `["cert.pem", "key.pem"]` | 证书与私钥分离 |
| [cert, key, password] 三元组 | `["cert.pem", "key.pem", "passphrase"]` | 加密私钥需密码解密 |

## 目录：一键安装

Hermes 内置精选 MCP 目录（Nous 审核合并），默认禁用：

```bash
hermes mcp              # 交互式选择器
hermes mcp catalog      # 纯文本列表
hermes mcp install n8n  # 按名安装
```

安装时支持：API key 配置、OAuth 认证、工具选择清单。

## 信任模型

安装目录条目会运行清单指定的操作（git clone、bootstrap 命令、MCP 服务器代码）。清单通过 PR 审核把关，但用户仍应在安装前阅读清单。

> 类比：像应用商店——平台审核把关（PR 审核），但安装前读权限说明仍是用户责任。

## 工具命名规范

Hermes 给 MCP 工具加前缀避免冲突：

```
mcp_<server_name>_<tool_name>
```

示例：

| MCP 工具 | 命名 |
|---|---|
| filesystem 服务的 read_file | `mcp_filesystem_read_file` |
| github 服务的 create-issue | `mcp_github_create-issue` |

## MCP 实用工具

当服务器支持时，Hermes 还注册以下实用工具：

| 工具 | 作用 |
|---|---|
| `list_resources` | 列出服务器暴露的资源 |
| `read_resource` | 读取指定资源内容 |
| `list_prompts` | 列出服务器提供的 prompt 模板 |
| `get_prompt` | 获取指定 prompt |

这些是**能力感知**的——只在服务器实际支持时注册，不会注入无效工具。

## 按服务器过滤

可配置只暴露特定工具，减少模型工具足迹：

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    tools:
      include: ["create-issue", "list-repos"]
```

> 这呼应 Hermes "核心是窄腰，能力在边缘"原则——只暴露实际需要的工具，避免污染 prompt 缓存。

## 内存回收

浏览器类 MCP 服务器（如 Playwright）会常驻 Chromium，占用大量内存。可配置空闲超时和最大生命周期自动回收：

```yaml
idle_timeout_seconds: 900     # 15 分钟无调用后回收
max_lifetime_seconds: 86400   # 至少每天回收一次
```

## 内置预设

```bash
hermes mcp add --preset codex
```

一行添加 Codex CLI 的 MCP 服务器，预设已包含正确配置。

## 配置参考

常用配置键：

| 键 | 说明 |
|---|---|
| `command` | stdio 服务器的启动命令 |
| `args` | 命令参数列表 |
| `env` | 环境变量（凭证过滤作用域） |
| `url` | HTTP 服务器的端点 URL |
| `headers` | HTTP 请求头（如 Authorization） |
| `client_cert` | mTLS 客户端证书配置 |
| `timeout` | 工具调用超时 |
| `connect_timeout` | 连接建立超时 |
| `idle_timeout_seconds` | 空闲回收超时 |
| `max_lifetime_seconds` | 最大生命周期 |
| `enabled` | 是否启用该服务器 |
| `supports_parallel_tool_calls` | 是否支持并行工具调用 |
| `tools` | 工具过滤配置（include 列表） |

## 相关文件

- [Hermes Agent](./01-概述.md) — 足迹阶梯中的 MCP 层
- [Hermes 工具与工具集](./04-工具与工具集.md) — 工具体系
- [Hermes 安全机制](./10-安全机制.md) — MCP 凭证过滤
- [概念全景辨析](../../02-概念全景辨析.md) — MCP 概念辨析
- [知识库 Schema](../../AGENTS.md) — 入库规范
