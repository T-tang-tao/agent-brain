# Migration

这里存放真正用于迁移 Hermes Agent、Claude Code CLI Agent、Codex Agent、Skill、Prompt、MCP 和知识库的 playbook 与 checklist。

## 这个目录放什么

本目录未来可以放：

- Hermes agent migration playbook；
- Claude Code to Hermes；
- Codex to Hermes；
- skill migration checklist；
- prompt migration checklist；
- MCP migration checklist；
- knowledge base migration checklist。

## 这个目录不放什么

这里不写 Agent、Skill、MCP、Prompt 的基础概念教程。

概念解释见：

- [../00-AgentBase/00-目录索引]

## 迁移资产应包含什么

建议包含：

- 迁移来源；
- 迁移目标；
- 需要迁移的内容；
- 不兼容项；
- 工具替换关系；
- prompt 调整；
- skill 调整；
- MCP 调整；
- 边界规则；
- 验证步骤；
- 回滚方案。

## 后续计划

第一阶段只建立目录。后续开始迁移 Hermes、Claude Code、Codex 等 agent 时，再补充实际 playbook。

## 已收录 Playbook

| Playbook | 迁移方向 | 状态 |
|----------|----------|------|
| [claude-code-to-hermes](./claude-code-to-hermes.md) | Claude Code CLI → Hermes Agent | 可用 |
