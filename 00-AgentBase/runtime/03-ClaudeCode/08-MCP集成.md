# Claude Code MCP 集成

> Claude Code 的 Model Context Protocol 集成——通过四种传输方式连接数百种外部工具与数据源,无需把数据拷进对话即可扩展 Agent 能力。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / runtime |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-09 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | claude-code, mcp, model-context-protocol, integration |

---

## MCP 提供什么

MCP(Model Context Protocol)让 Claude Code 无需内置即可接入外部工具生态:

- 连接数百种外部工具和数据源
- **无需把数据拷进对话**——工具在远端处理,只返回结果
- 本地子进程和远程服务在同一配置中统一管理
- 支持工具、资源和 prompt 模板三类能力
- Claude Code 自身也可作为 MCP server 暴露能力给其他 host

> 类比:MCP 像"USB 接口"——任何符合协议的设备都能即插即用,Claude Code 不用为每个工具单独开发驱动。

## 四种传输方式

| 传输类型 | 适用场景 | 特点 |
|----------|----------|------|
| **HTTP** | 远程服务器(推荐) | 标准请求-响应,支持 OAuth |
| **SSE** | 旧式远程服务器 | 已废弃,被 HTTP 取代 |
| **stdio** | 本地子进程 | 通过 stdin/stdout 通信 |
| **WebSocket** | 持久双向连接 | 长连接,实时推送 |

> 类比:HTTP 像"寄信"(一问一答),stdio 像"面对面交谈"(进程间管道),WebSocket 像"打电话"(持续双向通话)。

## 安装命令

```bash
# HTTP 远程服务器
claude mcp add --transport http <name> <url>

# stdio 本地进程(注意 -- 分隔符)
claude mcp add --transport stdio <name> -- <command> [args...]

# 示例
claude mcp add --transport stdio github -- npx -y @modelcontextprotocol/server-github
```

`--` 分隔符在 stdio 模式下必不可少——它告诉 CLI 后面的参数属于被启动的命令,而非 `claude mcp` 自身的选项。

## MCP 作用域

三种作用域决定服务器配置的可见范围,优先级从高到低:

| 作用域 | 存储位置 | 共享方式 |
|--------|----------|----------|
| **Local**(默认) | 当前项目 | 仅当前项目可见 |
| **Project** | `.mcp.json` | 提交到 git,团队共享 |
| **User** | `~/.claude.json` | 跨所有项目可见 |

> 类比:像 Linux 配置优先级——本地覆盖 > 项目配置 > 用户全局,从窄到宽逐级被覆盖。

## .mcp.json 配置文件

Project 作用域配置,提交到 git 供团队共享:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com/sse",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    },
    "local-db": {
      "type": "stdio", "command": "node", "args": ["./mcp/db-server.js"]
    }
  }
}
```

支持 `${VAR}` 语法展开环境变量——配置只放占位符,实际值从环境注入,避免密钥泄露到仓库。

## 认证

| 方式 | 说明 |
|------|------|
| **OAuth** | `/mcp` 面板触发登录,或 `claude mcp login <name>` / `claude mcp logout <name>`。处理 OAuth 2.1 全流程(发现、PKCE、令牌刷新) |
| **自定义头** | 用 `headersHelper` 指定脚本,每次请求动态生成头部(如时效性签名 token) |

## 管理命令

| 命令 | 作用 |
|------|------|
| `claude mcp list` | 列出所有已配置服务器 |
| `claude mcp get <name>` | 查看单个服务器详情 |
| `claude mcp remove <name>` | 移除服务器 |
| `/mcp`(会话内) | 交互式管理面板 |

## 动态工具更新与自动重连

| 机制 | 说明 |
|------|------|
| **动态工具更新** | 服务器发 `list_changed` 通知,Claude Code 自动刷新工具列表,无需重启会话 |
| **自动重连** | HTTP/SSE 断线后指数退避重连(5 次:1s→2s→4s→8s→16s),stdio 进程崩溃不自动重启 |
| **Push 频道** | 基于 `claude/channel` capability,`--channels` 标志订阅,服务器可主动推送消息 |

插件也可内置 MCP 服务器配置——安装插件即自动注册,无需单独配置。

## MCP 工具命名

Claude Code 给 MCP 工具加前缀避免命名冲突:

```
mcp__<server>__<tool>
```

| MCP 工具 | 命名 |
|----------|------|
| github 服务的 create_issue | `mcp__github__create_issue` |
| filesystem 服务的 read_file | `mcp__filesystem__read_file` |

> 这个命名规范在 Hooks 的 matcher 中也用于匹配 MCP 工具,详见 [Hooks 系统](./09-Hooks系统.md)。

## 工具搜索(Tool Search)

默认启用的优化机制:

- **延迟加载**——MCP 工具在首次需要时才真正加载
- 按需发现——只在 Claude 决定调用时才拉取工具 schema
- 可扩展到大量服务器而不过度膨胀上下文

> 类比:像 lazy loading——用到哪个加载哪个,让 Claude Code 管理数十个 MCP 服务器而不撑爆上下文。

## MCP 资源与 Prompt

除工具外,MCP 还暴露资源和 prompt 模板:

| 能力 | 工具 | 作用 |
|------|------|------|
| 资源列表 | `ListMcpResourcesTool` | 列出服务器暴露的资源 |
| 资源读取 | `ReadMcpResourceTool` | 读取指定资源内容 |
| Prompt 模板 | 执行 MCP prompt | 作为命令调用服务器提供的 prompt |

## 输出限制与托管 MCP

| 配置 | 作用 |
|------|------|
| 10,000 token | 输出超过此值触发警告 |
| `MAX_MCP_OUTPUT_TOKENS` | 环境变量,自定义输出上限 |
| `allowedMcpServers` | 企业白名单——允许的 MCP 服务器 |
| `deniedMcpServers` | 企业黑名单——禁止的 MCP 服务器 |
| `allowManagedMcpServersOnly` | 只允许托管服务器,禁止用户自配 |

`CLAUDE_PROJECT_DIR` 环境变量会传递给 stdio 服务器——让本地 MCP 进程知道当前项目根目录。

## 相关文件

- [Claude Code](./01-概述.md) — MCP 在整体架构中的位置
- [Claude Code 配置体系](./03-配置体系.md) — MCP 服务器配置
- [Claude Code 工具系统](./04-工具系统.md) — MCP 工具与内置工具的关系
- [Claude Code Hooks 系统](./09-Hooks系统.md) — 用 matcher 匹配 MCP 工具
- [概念全景辨析](../../02-概念全景辨析.md) — MCP 概念辨析
- [知识库 Schema](../../AGENTS.md) — 入库规范
