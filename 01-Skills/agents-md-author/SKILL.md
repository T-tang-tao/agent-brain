---
name: agents-md-author
description: "编写 / 修改 / 优化 / 审查 AGENTS.md。触发词:改 AGENTS.md / 写 AGENTS / 重写 AGENTS / 优化 AGENTS.md / 新建 AGENTS.md / 别解释为什么 / 直接执行 / 删掉那段解释 / 不写原因。强制规则:AGENTS.md 是 context 的扩展,关键约束放最前(< 100 行达首尾注意力区)、不写"为什么"段落(放 99-Roadmap.md)、不重复知识库已有内容、用祈使句、用结构化表格、引用而非重复、边界规则覆盖三类(允许/确认/禁止)、单文件 < 500 行、关键约束不写中间(防 U 型注意力曲线)。"
version: 2.1.0
status: 可用
level: project
imported: 2026-07-09
updated: 2026-07-10
---

# AGENTS.md Author

编写 AGENTS.md 时强制遵循简洁规范。

## 触发

- 改 / 写 / 重写 / 优化 AGENTS.md
- "别解释为什么" / "不写原因" / "直接执行"
- 任何修改 AGENTS.md 的请求

## 强制规则(关键约束,放最前)

1. **AGENTS.md 是 context 的扩展**。Runtime 启动时自动加载,是模型最先看到的内容。关键约束放**最前面**(防 U 型注意力曲线 — 中段会被忽略 10-40%)。详见 [`00-AgentBase/behavior/09-Context-Engineering.md`](../../00-AgentBase/behavior/09-Context-Engineering.md) § 2。
2. **不写"为什么"段落**。决策理由放 `99-Roadmap.md`。
3. **不重复知识库已有内容**。引用即可。
4. **用祈使句**。规则不要用"我们认为"开头。
5. **表格用结构化数据**,不用散文。
6. **引用而非重复**。`[`link`](./path)` 优于内联。**链接格式**:`[`显示文字`](相对路径.md)`。**禁止** Obsidian wikilink `[[path]]`、裸 `[path]`、绝对路径。详见 [00-AgentBase/AGENTS.md](../../00-AgentBase/AGENTS.md) § 3.1。
7. **边界规则覆盖三类**:`✅ 允许` / `⚠️ 需确认` / `❌ 禁止`。
8. **单文件 < 500 行**。超长拆 references/。
9. **关键约束不写中间**。首尾是 attention sink,中间容易被丢。

## 七要素齐全(AGENTS.md 必备)

按 [`00-AgentBase/behavior/13-Harness-Engineering.md`](../../00-AgentBase/behavior/13-Harness-Engineering.md) 的四类表面切分:

| 段落 | 表面分类 | 必选 |
|------|---------|------|
| 强制规则 / 触发词 | **Locked**(Agent 必读) | ✅ |
| 边界规则(允许/确认/禁止) | **Locked**(防越界) | ✅ |
| Procedure 步骤 | Editable(可优化) | ✅ |
| Verification 自检清单 | Locked | ✅ |
| "为什么"决策理由 | **不放 AGENTS.md**,放 99-Roadmap.md | ✅ |
| 引用知识库章节 | 链接(不复制内容) | ✅ |
| 详细参考 / 反模式 | references/(按需加载) | 按需 |

## Procedure

### 1. 识别意图

| 意图 | 行动 |
|------|------|
| 完全重写 | 复制 [`templates.md`](./references/templates.md) 完整模板 |
| 修改某章节 | 直接 SearchReplace |
| 删除冗余段落 | 按 [`rules.md`](./references/rules.md) § 1 检查清单 |
| 跨多个 AGENTS.md 统一 | 先改根,再同步;决策走 99-Roadmap.md |

### 2. 写

按强制规则 1-9 写。**关键约束放首屏**(前 100 行),Procedure 骨架放中段,Verification 放结尾。

### 3. 自检

对照 [`rules.md`](./references/rules.md) § 1 检查清单逐项过。任意一条不满足,立即修正。

## Pitfalls

- ❌ "为什么"段落占据 30% 篇幅
- ❌ 关键约束放文档中间(被 U 型注意力曲线忽略)
- ❌ 重复知识库内容(浪费 context,稀释信号)
- ❌ 单文件 > 500 行(超出有效注意力容量)
- ❌ 缺边界规则三分类
- ❌ 决策理由散落各章(应统一在 99-Roadmap.md)

## Verification

写完 AGENTS.md 后逐项验证:

- [ ] 关键约束(规则 / 边界)在**前 100 行**?
- [ ] 0 个"为什么"段落(决策全在 99-Roadmap.md)?
- [ ] 知识库内容只引用,不复制?
- [ ] 祈使句不用"我们认为"开头?
- [ ] 表格覆盖结构化数据?
- [ ] 边界规则三分类齐全(允许/确认/禁止)?
- [ ] 单文件 < 500 行?
- [ ] 详细 reference 拆到 references/?
- [ ] Verification 自检清单在结尾?

## 上下文工程约束(本 SKILL 自身)

- **关键约束(规则 1-9)放最前** — 文档头 30 行
- **Verification 自检放最末** — 文档尾部
- **总长 < 200 行**:SKILL.md 只放触发 + 规则 + 流程,详细靠引用 references/
- 参考: [`00-AgentBase/behavior/09-Context-Engineering.md`](../../00-AgentBase/behavior/09-Context-Engineering.md) § 3 四大装配原则

## 详细参考

- **强制规则 + 反模式**: [`references/rules.md`](./references/rules.md)
- **完整 / 最小模板**: [`references/templates.md`](./references/templates.md)
- **理论背景**: `00-AgentBase/knowledge/04-如何编写AGENTS.md`
- **相关知识**: [`00-AgentBase/behavior/09-Context-Engineering.md`](../../00-AgentBase/behavior/09-Context-Engineering.md) § 3
- **决策日志**: `99-Roadmap.md`