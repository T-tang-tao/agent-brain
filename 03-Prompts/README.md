# Prompts

这里存放可直接复制、迁移、改造的 Agent Prompt。

## 这个目录放什么

本目录未来可以放：

- Hermes Agent system prompt；
- Claude Code CLI agent prompt；
- Codex agent prompt；
- migration agent prompt；
- boundary-aware agent prompt；
- skill writing prompt。

## 这个目录不放什么

这里不写 Prompt 的基础概念教程。

概念解释见：

- [../00-AgentBase/02-概念全景辨析]

## 模板

- [_agent-prompt-template]

## Prompt 资产应包含什么

建议包含：

- 目标；
- 适用 Agent；
- System Prompt；
- 行为要求；
- 工具使用规则；
- 边界规则；
- 输出格式；
- 迁移注意事项。

## 后续计划

第一阶段提供模板。后续根据 Hermes、Claude Code、Codex 的迁移需要补充实际 prompt。

## 已收录 Prompt

| Prompt | 适用 agent | 用途 | 状态 |
|--------|-----------|------|------|
| [claude-code-agent-prompt](./claude-code-agent-prompt.md) | Claude Code CLI | 主系统 prompt,知识库管理 + 通用开发 | 验证中 |
| [hermes-agent-prompt](./hermes-agent-prompt.md) | Hermes Agent | 消息网关 + 定时任务 + 多 agent 协同 | 验证中 |
| [boundary-aware-agent-prompt](./boundary-aware-agent-prompt.md) | 任何 agent | 边界敏感任务(删除/外部调用/资金),叠加 prompt | 验证中 |
| [_agent-prompt-template](./_agent-prompt-template.md) | 任何 | 新 prompt 编写模板 | 可用 |
