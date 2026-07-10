# Safety — 安全

> 知识地图模块:**Safety** — Permission、Boundary、Verification(Evaluation 和 Observability 已移至 behavior)

## 这个目录放什么

关于 Agent 安全边界的认知:
- Agent 为什么需要边界
- 工具权限 / 文件编辑 / Shell / 外部 API 的边界
- 什么时候必须问人、什么时候可以自主
- 验证的重要性

> **关于 Evaluation 和 Observability**:之前归在本目录,现已移至 [behavior/05-评估方法(Evaluation)](../behavior/05-评估方法(Evaluation).md) 和 [behavior/06-可观测性(Observability)](../behavior/06-可观测性(Observability).md)——它们本质是 Agent 行为质量的度量和审计手段,不是"安全"本身。

## 已有文档

| 文档 | 回答什么 |
|------|----------|
| `01-Agent边界与限制.md` | Agent 为什么需要边界?哪些操作要确认?什么时候必须问人? |

## 未来计划

- 权限分级模型设计
- 降级与回滚策略
- 边界规则的版本化与审计