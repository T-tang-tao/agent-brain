# MCP

这里存放可落地的 MCP 配置、MCP server 说明和连接方案。

## 这个目录放什么

本目录未来可以放：

- GitHub MCP；
- filesystem MCP；
- Obsidian vault MCP；
- trading data MCP；
- MCP server template；
- MCP config examples。

## 这个目录不放什么

这里不写 MCP 的基础概念教程。

概念解释见：

- [../00-AgentBase/02-概念全景辨析]

## MCP 资产应包含什么

每个 MCP 资产建议包含：

- server 名称；
- 用途；
- 暴露的 tools；
- 暴露的 resources；
- 暴露的 prompts；
- 鉴权方式；
- 适用 agent；
- 风险边界；
- 配置示例；
- 迁移注意事项。

## 后续计划

第一阶段只建立目录。后续根据实际需要补充 MCP 配置和 server 说明。

## 已收录 MCP Server

| Server | 用途 | 适用 Runtime | 状态 |
|--------|------|--------------|------|
| [filesystem-mcp](./filesystem-mcp.md) | 通用文件读写,限定在 ${KB_ROOT} | Claude Code / Codex / Hermes | 可用 |
| [obsidian-mcp](./obsidian-mcp.md) | Obsidian vault 操作(双链/元数据) | Claude Code / Codex / Hermes | 可用 |
