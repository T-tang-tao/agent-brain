---
name: obsidian-mcp
type: mcp-server
用途: 让 agent 直接读写 Obsidian vault
适用 agent: Claude Code(强支持)/ Codex / Hermes
status: 可用
---

# Obsidian MCP Server 配置

## 用途

Obsidian MCP 让 Agent 能:

- 读 vault 笔记(`${KB_ROOT}/*.md`)
- 写 vault 笔记
- 创建/删除/重命名笔记
- 解析 Obsidian 链接(`[..]`)和 frontmatter
- 搜索 vault 内容

适用场景:

- 让 Agent 主动更新知识库
- 让 Agent 解析 Obsidian 双链网络
- 让 Agent 维护 `.obsidian/` 配置(但本知识库默认禁止)

## Claude Code 配置

`~/.claude.json`:

```json
{
  "mcpServers": {
    "obsidian-kb": {
      "command": "npx",
      "args": [
        "-y",
        "obsidian-mcp-server",
        "--vault-path",
        "D:\\valut\\trade\\agent"
      ],
      "env": {}
    }
  }
}
```

⚠️ **注意**:`obsidian-mcp-server` 是社区实现,不是 Anthropic 官方。GitHub 上搜索 `mcp obsidian` 选 star 数最多的一个。常见的有:

- `cyanheads/obsidian-mcp-server`(活跃)
- `anpigon/mcp-server-obsidian`(轻量)

具体参数以所选实现为准。

## Codex 配置

`~/.codex/config.toml`:

```toml
[mcp_servers.obsidian-kb]
command = "npx"
args = ["-y", "obsidian-mcp-server", "--vault-path", "D:\\valut\\trade\\agent"]
```

## 暴露的工具(典型)

| 工具 | 用途 |
|------|------|
| `read_note` | 读笔记 |
| `write_note` | 写笔记 |
| `create_note` | 建新笔记 |
| `delete_note` | 删笔记 |
| `list_notes` | 列笔记(可按目录/标签) |
| `search_notes` | 全文搜索 |
| `get_note_metadata` | 读 frontmatter |
| `update_note_metadata` | 改 frontmatter |
| `resolve_links` | 解析 `[link]` |

## 风险边界

⚠️ **`.obsidian/` 目录是 Obsidian 配置文件**:

- 修改可能破坏 Obsidian 客户端状态
- Agent 默认禁止写 `.obsidian/`,只能读
- 详见 [`../05-Boundaries/file-edit-policy.md`](../05-Boundaries/file-edit-policy.md) §3

## 与 filesystem-mcp 的取舍

| 维度 | filesystem-mcp | obsidian-mcp |
|------|----------------|--------------|
| 解析 Obsidian 链接 | ❌ | ✅ |
| 解析 frontmatter | ❌ | ✅ |
| 范围限制 | 物理路径 | 物理路径(可加 vault 概念) |
| 通用性 | 任何文件 | 仅 markdown |
| 推荐场景 | 通用文件操作 | Obsidian vault 操作 |

**推荐组合**:两个 MCP 都装,filesystem 用于通用操作,obsidian 用于 vault 特定操作。

## 验证

```text
> 列出 ${KB_ROOT} 下所有 markdown 文件
```

Agent 应返回笔记列表(含子目录)。

```text
> 读 ${KB_ROOT}/00-AgentBase/AGENTS.md 的元数据
```

应返回 frontmatter(如果有)+ 元信息。

## 迁移注意事项

- 社区 MCP 实现质量参差不齐,选前看 GitHub star / 最近 commit / issue 数
- Obsidian MCP 通常不支持并发写(同一文件被多个 agent 同时改会冲突)
- 写操作建议配 git,改前 commit 一下

## 相关

- [filesystem-mcp.md](./filesystem-mcp.md) — 通用文件 MCP
- [`../05-Boundaries/file-edit-policy.md`](../05-Boundaries/file-edit-policy.md) — 写边界