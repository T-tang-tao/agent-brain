---
name: filesystem-mcp
type: mcp-server
用途: 让 agent 访问受限文件系统
适用 agent: Claude Code / Codex / Hermes(都支持)
status: 可用
---

# Filesystem MCP Server 配置

## 用途

MCP Filesystem Server 让 Agent 能读写限定目录的文件。在本知识库场景下:

- ✅ **允许**:读 `${KB_ROOT}` 全部、写 `${KB_ROOT}/01-Skills` / `02-Plugins` / `03-Prompts` / `99-Roadmap.md`
- ❌ **禁止**:写 `${KB_ROOT}/.obsidian/`、写 `${KB_ROOT}/00-AgentBase/`(需特殊审批)、访问 `C:\` 根目录

## Claude Code 配置

`~/.claude.json`:

```json
{
  "mcpServers": {
    "filesystem-kb": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:\\valut\\trade\\agent"
      ],
      "env": {}
    }
  }
}
```

## Codex CLI 配置

`~/.codex/config.toml`:

```toml
[mcp_servers.filesystem-kb]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "D:\\valut\\trade\\agent"]
```

## Hermes Agent 配置

`~/.hermes/mcp.json`:

```json
{
  "servers": {
    "filesystem-kb": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\valut\\trade\\agent"]
    }
  }
}
```

## 暴露的工具

启用后 Agent 可用工具:

| 工具 | 用途 |
|------|------|
| `read_file` | 读文件 |
| `read_text_file` | 读文本(带编码) |
| `read_multiple_files` | 批量读 |
| `write_file` | 写文件 |
| `edit_file` | 编辑文件 |
| `create_directory` | 建目录 |
| `list_directory` | 列目录 |
| `list_allowed_directories` | 看允许范围 |
| `directory_tree` | 树形结构 |
| `move_file` | 移动 |
| `search_files` | 文件名搜索 |
| `get_file_info` | 文件元数据 |
| `list_directory_with_sizes` | 列大小 |

## 风险边界

⚠️ **filesystem MCP 工具的范围是物理路径,不是逻辑目录**:

- 即使配置里写了 `D:\valut\trade\agent`,Agent 仍可访问 `${KB_ROOT}/00-AgentBase/` 等任何子目录
- 必须配合 [`../05-Boundaries/file-edit-policy.md`](../05-Boundaries/file-edit-policy.md) 做逻辑限制
- 建议在 system prompt 中明确告知 agent 哪些路径禁止写

## 验证

启动 Runtime 后,Agent 应能:

```text
> 读 ${KB_ROOT}/01-Skills/kb-init/SKILL.md 的前 10 行
```

返回前 10 行内容。

如果报错 "Permission denied",检查:

1. MCP server 是否启动(`~/.claude.json` 路径正确)
2. Node.js 是否安装(`npx` 可用)
3. 路径分隔符(Windows 用 `\\` 或 `/` 都可,MCP 内部处理)

## 迁移注意事项

| 字段 | Claude Code | Codex | Hermes |
|------|-------------|-------|--------|
| 配置文件 | `~/.claude.json` | `~/.codex/config.toml` | `~/.hermes/mcp.json` |
| 配置语法 | JSON | TOML | JSON |
| 路径分隔 | `\\` 或 `/` | `\\` 或 `/` | `\\` 或 `/` |
| 启动方式 | Runtime 启动时 | Runtime 启动时 | Runtime 启动时 |

## 相关

- [obsidian-mcp.md](./obsidian-mcp.md) — Obsidian vault 专用 MCP
- [`../05-Boundaries/file-edit-policy.md`](../05-Boundaries/file-edit-policy.md) — 文件编辑边界