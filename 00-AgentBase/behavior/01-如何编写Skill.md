# 如何编写 Skill

> Skill 是 Agent 按需加载的操作手册——不是代码,不是百科全书,而是指导 Agent 如何完成特定任务的结构化指令。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-09 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | skill, progressive-disclosure, yaml, frontmatter |

---

## 一句话理解

Skill 是一个 Markdown 文件,通过 YAML frontmatter 告诉 Agent"什么时候用我",通过正文告诉 Agent"用我时该怎么做"。本质是精心组织的提示词,不是可执行程序。

## Skill 的物理结构

每个 Skill 是一个**目录**,以 `SKILL.md` 为入口,可包含可选的支持文件:

```
my-skill/
├── SKILL.md           # 主指令文件(必需)
├── templates/         # 模板文件(可选)
│   └── report.md
├── references/        # 参考资料(可选)
│   └── style-guide.md
├── examples/          # 示例输出(可选)
│   └── sample.md
└── scripts/           # 可执行脚本(可选)
    └── validate.sh
```

> **类比**:Skill 像一本操作手册。SKILL.md 是手册正文(翻到就能照做),references 是附录(需要时才查),templates 是空白表格(拿来填)。

## SKILL.md 的组成

SKILL.md 由两部分组成:YAML frontmatter(告诉 Agent 什么时候用)和 Markdown 正文(告诉 Agent 怎么做)。

### YAML Frontmatter

放在 `---` 之间,位于文件最顶部:

```yaml
---
name: my-skill
description: 简短描述,告诉 Agent 什么时候使用此技能
version: 1.0.0
---
```

| 字段 | 必需 | 作用 |
|------|------|------|
| `name` | 是 | 技能名称,小写字母+数字+连字符,成为 `/slash-command` |
| `description` | 是 | 功能描述,**给模型读的触发器**,不是给人读的说明 |
| `version` | 否 | 版本号 |
| `platforms` | 否 | 限制操作系统:`[macos, linux, windows]` |
| `allowed-tools` | 否 | 限制此技能可使用的工具(Claude Code) |
| `metadata` | 否 | 平台特定扩展(Hermes 的条件激活、环境变量等) |

### Markdown 正文

正文是 Agent 被调用时遵循的指令,建议采用以下结构:

```markdown
# 技能标题

## When to Use
(何时使用此技能——具体的触发场景)

## Procedure
(操作步骤——按顺序列出 Agent 应该做什么)

## Pitfalls
(常见陷阱——容易踩的坑和避坑方法)

## Verification
(验证方法——如何确认任务完成)
```

## 核心原理:渐进式披露

Skill 不是一次性全部加载,而是分三级,逐级深入:

```
┌─────────────────────────────────────────────────────────┐
│  Level 0:元数据                                          │
│  始终加载 · 约 100 token · 所有 Skill 的 name+description │
│  Agent 从目录中判断哪些技能可能相关                         │
├─────────────────────────────────────────────────────────┤
│  Level 1:完整指令                                        │
│  按需加载 · < 5,000 token · SKILL.md 的 Markdown 正文    │
│  Agent 判断某个技能相关时,才读取完整指令                    │
├─────────────────────────────────────────────────────────┤
│  Level 2:支持文件                                        │
│  按需加载 · 大小不限 · references/templates/scripts       │
│  只有 SKILL.md 中明确引用时,Agent 才读取这些文件           │
└─────────────────────────────────────────────────────────┘
```

> **类比**:像翻书架。先看书名和摘要(Level 0),决定要哪本;再翻到正文(Level 1),按步骤做;遇到需要查的细节,才翻附录(Level 2)。没翻开的书不占脑力。

**关键含义**:你的 Skill 能否被使用,完全取决于 Level 0——那大约 100 个 token 的 name 和 description。description 模糊,Skill 就永远不会被调用。

## 核心原则:过程与知识分离

这是编写 Skill 最重要的设计原则:

| 类型 | 属于 | 放哪里 | 类比 |
|------|------|--------|------|
| **过程**(Process) | Agent 应该遵循的有序步骤 | SKILL.md 正文 | 食谱:"第一步打鸡蛋,第二步加面粉" |
| **知识**(Context) | 背景信息、规则、领域知识、参考数据 | references/ 目录 | 百科:"面粉的品种、鸡蛋的营养成分" |

为什么分开?当 SKILL.md 同时充当知识库时,模型必须自行判断哪些是指令、哪些是背景,而它不总能做对。

> **写法**:SKILL.md 要写得像食谱,不像百科全书。食谱告诉你"做什么",百科告诉你"为什么"。

## Description 怎么写

description 不是给人读的说明,是给模型读的触发器。

| 写法 | 示例 | 效果 |
|------|------|------|
| 糟糕 | `A skill for handling CSV files` | "处理"太模糊,Agent 不知道何时调用 |
| 良好 | `Parse, validate, and transform CSV files. Use when importing data from CSV, exporting reports, or fixing encoding issues.` | 具体场景,Agent 能精确匹配 |

原则:
- 写出**具体的触发场景**,不是泛泛的功能描述
- 用"Use when…"句式,列出 2-3 个典型场景
- 避免"helps with""handles"等模糊动词

## 两种 Skill 类型

| 类型 | 定义 | 典型场景 | 特点 |
|------|------|----------|------|
| 能力提升型 | 帮 Agent 做到原本做不到/做不一致的事 | 精确 PDF 解析、特定格式图表生成 | 可能随模型改进而变得不必要 |
| 编码偏好型 | 把 Agent 已能做的事按团队流程串联 | NDA 审查流程、周报起草流程 | 更持久,价值取决于对工作流的忠实度 |

编码偏好型 Skill 的核心价值不是"做对了没有",而是"每次都以同样的方式做对"——**一致性**。

## 编写流程

```
1. 确定技能目标:解决什么问题?是能力提升还是编码偏好?
2. 写 name:小写+连字符,简短,成为斜杠命令
3. 写 description:具体触发场景,Use when... 句式
4. 写正文:When to Use → Procedure → Pitfalls → Verification
5. 分离知识:背景资料、参考数据移到 references/
6. 补充支持文件:模板放 templates/,示例放 examples/
7. 验证:在干净环境中实际调用,确认 Agent 按预期执行
```

## 常见错误

### 错误 1:SKILL.md 写成百科全书

把所有领域知识塞进正文,导致 Agent 分不清指令和背景。

**修正**:正文只写"做什么",知识移到 references/。

### 错误 2:Description 太模糊

写"helps with documents",Agent 永远不会调用。

**修正**:写具体场景,"Use when working with PDF files and need to extract text and tables"。

### 错误 3:正文太长

超过 5,000 token,加载成本高,Agent 难以遵循。

**修正**:精简正文,细节移到 references/ 按需加载。

### 错误 4:过程和知识混在一起

正文里既写"第一步做什么",又插入大段背景解释。

**修正**:正文是食谱(步骤),references 是百科(知识)。

## 与其他概念的区别

| 概念 | 解决的问题 | 形态 |
|------|----------|------|
| Skill | 这类任务应该怎么做 | SKILL.md(流程指令) |
| Prompt | Agent 当前如何行为 | 提示词文本 |
| Plugin | 如何扩展宿主系统 | 扩展包(可能含 skill) |
| Knowledge Base | 可以查什么资料 | wiki/文档/RAG |

详见 [概念全景辨析](../02-概念全景辨析.md)。

## 相关文件

- [概念全景辨析](../02-概念全景辨析.md) — Skill 与 Tool/MCP/Plugin/Prompt 的区别
- [Hermes 技能系统](../runtime/02-Hermes-Agent/05-技能系统.md) — Hermes 中 Skill 的实现细节(条件激活、/learn、技能包)
- [Agent 知识库设计](../knowledge/01-Agent知识库设计.md) — 知识区和资产区为什么要分开
- [LLM Wiki 架构理念](../knowledge/03-LLM-Wiki架构理念.md) — 渐进式披露的理论根基
- [知识库管理员规范](../AGENTS.md) — 入库标准和管理流程
