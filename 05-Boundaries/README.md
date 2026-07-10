# Boundaries

这里存放可直接给 Agent 使用的边界规则、权限策略和限制规范。

## 这个目录放什么

本目录未来可以放：

- file edit policy；
- shell command policy；
- external API policy；
- memory write policy；
- destructive action policy；
- trading agent risk boundary。

## 这个目录不放什么

这里不写 Agent 边界的基础概念教程。

概念解释见：

- [[../00-AgentBase/safety/01-Agent边界与限制]]

## 模板

- [[_boundary-policy-template]]

## 边界规则应包含什么

建议包含：

- 规则名称；
- 适用范围；
- 允许行为；
- 需要确认的行为；
- 禁止行为；
- 风险说明；
- Agent 执行说明；
- 例子。

## 后续计划

第一阶段提供模板。后续逐步补充实际可执行边界规则。

## 已收录边界策略

| 策略 | 适用范围 | 优先级 | 状态 |
|------|----------|--------|------|
| [file-edit-policy](./file-edit-policy.md) | 文件读/写/删 | HIGH | 可用 |
| [shell-command-policy](./shell-command-policy.md) | PowerShell / Bash | HIGH | 可用 |
| [external-api-policy](./external-api-policy.md) | WebFetch / WebSearch / 任何 HTTP | HIGH | 可用 |
| [memory-write-policy](./memory-write-policy.md) | 长期/短期记忆 / RAG | HIGH | 可用 |
| [destructive-action-policy](./destructive-action-policy.md) | 删除 / 覆盖 / 重置 | CRITICAL | 可用 |
| [trading-risk-boundary](./trading-risk-boundary.md) | 交易/资金操作 | CRITICAL | 可用 |
| [_boundary-policy-template](./_boundary-policy-template.md) | 编写新策略的模板 | — | 可用 |

## 策略优先级

```text
trading-risk-boundary     ← CRITICAL(资金)
        ↓
destructive-action-policy ← CRITICAL(不可逆)
        ↓
file / shell / api / memory ← HIGH(可逆但需审批)
```
