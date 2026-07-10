# Agent、模型、Workflow 的区别

> 概念解释已迁移至 [00-human/01-Agent是什么-人类入门](../00-human/01-Agent是什么-人类入门.md)。
>
> 本文件保留项目内部分类约定，供 Agent 快速定位。

## 模型分类速查

| 概念 | 本质 | 对应本知识库位置 |
|------|------|-----------------|
| Model | 推理和生成能力 | `model/`（本目录） |
| LLM Call | 单次输入输出 | 不单独建目录，归入 `knowledge/` 讨论 |
| Workflow | 固定步骤自动化 | 不单独建目录，归入 `runtime/` 讨论 |
| Agent | 模型驱动的动态执行循环 | `00-AgentBase/` 全局 |

## 何时用 Agent vs Workflow

```text
如果下一步是固定的，用 Workflow。
如果下一步要根据观察结果决定，用 Agent。
```

详细解释和例子见 [00-human/01-Agent是什么-人类入门](../00-human/01-Agent是什么-人类入门.md)。

## 相关文件

- [00-human/01-Agent是什么](../00-human/01-Agent是什么-人类入门.md) — 完整概念解释
- [01-AgentBase总览](../01-AgentBase总览.md)
- [03-知识地图](../03-知识地图.md)
