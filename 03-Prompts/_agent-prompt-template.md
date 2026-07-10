# Agent Prompt 模板

## 目标

说明这个 prompt 用来让 agent 扮演什么角色、完成什么任务。

## 适用 Agent

- Hermes Agent
- Claude Code CLI Agent
- Codex Agent
- 其他：

## System Prompt

```text
在这里写系统提示词正文。
```

## 行为要求

- 说明 agent 应该如何行动；
- 说明 agent 应该如何处理不确定性；
- 说明 agent 应该如何汇报结果；
- 说明 agent 是否可以自主执行。

## 工具使用规则

- 哪些工具可以使用；
- 什么时候应该使用工具；
- 哪些工具需要确认；
- 工具失败时如何处理。

## 边界规则

- 哪些行为允许；
- 哪些行为需要确认；
- 哪些行为禁止。

可参考：

- [[../00-AgentBase/safety/01-Agent边界与限制]]
- [[../05-Boundaries/_boundary-policy-template]]

## 输出格式

说明 agent 最终应该如何输出。

例如：

- 简短总结；
- 修改文件列表；
- 验证结果；
- 未完成事项；
- 风险提示。

## 迁移注意事项

如果这个 prompt 从某个环境迁移而来，记录：

- 原环境；
- 目标环境；
- 需要替换的工具名；
- 需要调整的权限；
- 不兼容的行为；
- 已验证情况。
