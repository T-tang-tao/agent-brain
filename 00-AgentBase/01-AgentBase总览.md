# AgentBase 总览

> `00-AgentBase/` 是 Agent 相关的**完整知识库**，是整个系统的**大脑**。
>
> 人类在这里看懂 Agent，Agent 在这里检索认知，部署指南（根目录 AGENTS.md）基于这里的知识去搭建环境。
>
> **人类入门**请从 [00-human/](./00-human/README.md) 开始；以下内容面向已具备基础认知的读者和 Agent。

## 知识库定位

| 读者 | 在这里找什么 |
|------|-------------|
| 人类 | `00-human/` 入门 → 根级总览 → 七大模块深入 |
| Agent | 目录结构、写作约定、模块职责（本文件 + `03-知识地图.md`） |
| 部署 | 根目录 AGENTS.md 基于本知识库搭建、编排、管理 Agent 环境 |

## 知识库目录结构

根级放总览（不归属单一模块），`00-human/` 放人类入门，七个子目录**直接对应知识地图的七大模块**，各目录内部独立编号：

```text
00-AgentBase/
│
│  ── 根级：总览 ──
├── 00-目录索引.md           # 导航
├── 01-AgentBase总览.md       # 本文件（结构 + 入口）
├── 02-概念全景辨析.md         # 跨模块概念边界（项目特定）
├── 03-知识地图.md             # 全景导航
│
│  ── 人类入门（Agent 不需要读） ──
├── 00-human/        # 人类基础认知:Agent 是什么、术语速览、常见误解、使用指南
│
│  ── 七大模块（对应知识地图） ──
├── model/          # Model：理解、推理、生成、决策
├── runtime/        # Runtime：CLI、Harness、Context、Permission
├── tools/          # Tools：Built-in、MCP、Custom
├── knowledge/      # Knowledge：Wiki、RAG、Memory、Project Docs
├── behavior/       # Behavior：Prompt、Skill、Policy
└── safety/         # Safety：Permission、Boundary、Verification
```

## 快速入口

**Agent 直接从这里开始：**

1. 本文件 — 目录结构 + 模块职责
2. [03-知识地图] — 全景导航
3. [00-目录索引] — 按模块查找具体文档
4. [AGENTS.md] — 入库标准和管理流程

**人类从这里开始：**

1. [00-human/README](./00-human/README.md) → 01 → 02 → 03 → 04
2. 本文件 — 了解结构
3. [03-知识地图] — 看全局

## 编号规则

- **根级**：00-03 连续编号，表示总览类（定义、辨析、导航）
- **00-human**：01-04 连续编号，人类入门内容
- **子目录**：各目录内部从 01 起独立编号，互不影响

## 这个目录放什么

**只放概念解释**，不放可执行资产：

| 模块 | 职责 |
|------|------|
| `00-human/` | 人类基础认知（Agent 不读） |
| `model/` | 模型的认知 |
| `runtime/` | 运行时、CLI、Harness 的认知 |
| `tools/` | 工具体系的认知 |
| `knowledge/` | 知识库、Wiki、RAG、Memory 的认知 |
| `behavior/` | Prompt、Skill、Policy 的认知 |
| `safety/` | 边界、权限、验证的认知 |

## 这个目录不放什么

可执行资产放实践层（`01-` 之后）：

| 资产类型 | 去哪里找 |
|----------|----------|
| Skill 文件 | `../01-Skills/` |
| Plugin 配置 | `../02-Plugins/` |
| Prompt 模板 | `../03-Prompts/` |
| MCP 配置 | `../04-MCP/` |
| 边界规则 | `../05-Boundaries/` |
| 迁移 playbook | `../06-Migration/` |

## 相关文件

- [00-目录索引](./00-目录索引.md)
- [02-概念全景辨析](./02-概念全景辨析.md)
- [03-知识地图](./03-知识地图.md)
- [00-human 人类入门](./00-human/README.md)
- [AGENTS.md 管理员规范](./AGENTS.md)
- [runtime/01-Agent运行时与CLI](./runtime/01-Agent运行时与CLI.md)
- [model/01-Agent-模型-Workflow的区别](./model/01-Agent-模型-Workflow的区别.md)
- [knowledge/01-Agent知识库设计](./knowledge/01-Agent知识库设计.md)
- [safety/01-Agent边界与限制](./safety/01-Agent边界与限制.md)
