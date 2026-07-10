# 跨 Runtime 技能管理

> 同一个技能,不同 runtime 的安装方式、存储位置、全局/项目级范围都不一样。本文档讲清楚怎么管。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-09 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | skill, runtime, cross-platform, adapter, global, project |

---

## 一句话理解

技能的**源**只有一份,但**部署方式**因 runtime 而异。用"规范源 + 适配层"模式管理:一个 canonical source,多个 runtime adapter,互不干扰。

## 问题是什么

你写了一个 Skill,想在 Claude Code、Codex、Hermes 里都用。但:

| 维度 | Claude Code | Codex | Hermes | Cursor |
|------|-------------|-------|--------|--------|
| **技能形态** | Plugin 或 `~/.claude/skills/` | Plugin | `~/.hermes/skills/` | Plugin |
| **全局位置** | `~/.claude/skills/` | marketplace 安装 | `~/.hermes/skills/` | marketplace 安装 |
| **项目级位置** | `.claude/skills/` | — | `external_dirs` 配置 | — |
| **安装方式** | `/plugin install` | `/plugins` | 复制目录 / 配置 | `/add-plugin` |
| **指令文件** | `CLAUDE.md` | `AGENTS.md` | config.yaml | `.cursor/rules` |
| **加载机制** | 启动时扫描三个目录 | plugin 系统加载 | 启动时扫描 + `external_dirs` | plugin 系统加载 |

直接复制到每个 runtime 的目录?能跑,但改一次要同步 N 处,早晚出错。

## 解决方案:规范源 + 适配层

> **类比**:USB 标准。设备(Skill 源)只有一个,但通过不同的转接头(Runtime Adapter),插到不同接口上。

### 架构图

```
                    ┌─────────────────┐
                    │  Canonical Source │
                    │  (规范源)         │
                    │                  │
                    │  skills/         │
                    │  ├── skill-a/   │
                    │  │   └── SKILL.md│
                    │  └── skill-b/   │
                    │      └── SKILL.md│
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │ Claude Adapter│ │ Codex Adapter│ │ Hermes Adapter│
     │              │ │              │ │              │
     │.claude-plugin│ │.codex-plugin │ │ config.yaml  │
     │  plugin.json │ │              │ │ external_dirs│
     │  CLAUDE.md   │ │  AGENTS.md   │ │              │
     └──────────────┘ └──────────────┘ └──────────────┘
              │              │              │
              ▼              ▼              ▼
     /plugin install   /plugins         复制/软链
```

### 三层职责

| 层 | 职责 | 内容 |
|----|------|------|
| **规范源** | 唯一真相源 | `skills/` 目录下的 SKILL.md 文件,标准格式 |
| **适配层** | 翻译/打包 | runtime 特定的配置(`.claude-plugin/plugin.json`、`config.yaml` 等) |
| **部署层** | 实际安装 | 复制到 runtime 的技能目录,或通过 marketplace 安装 |

### 适配层做什么

每个 runtime 适配层只需要做三件事:

1. **清单声明**:告诉 runtime "这里有个技能包"(如 `plugin.json`)
2. **指令加载**:告诉 runtime 怎么加载技能(如 `CLAUDE.md`、`AGENTS.md`)
3. **工具映射**:把通用动作语言映射到 runtime 特定工具名(如 `references/codex-tools.md`)

### 参考实现:Superpowers

Superpowers 就是这个模式的典范:

```
superpowers/
├── skills/                # 规范源(13 个 SKILL.md)
├── .claude-plugin/        # Claude Code 适配
├── .codex-plugin/         # Codex 适配
├── .cursor-plugin/        # Cursor 适配
├── .kimi-plugin/          # Kimi 适配
├── .opencode/             # OpenCode 适配
├── .pi/extensions/        # Pi 适配
├── hooks/                 # 跨 runtime 钩子
└── scripts/               # 同步脚本(把规范源同步到各适配层)
```

## 全局 vs 项目级

### 分类原则

| 类型 | 适合全局 | 适合项目级 |
|------|---------|-----------|
| 跨项目通用方法论 | TDD、debugging、code review、brainstorming | — |
| 底层能力增强 | 通用工具链配置、常用 prompt 模板 | — |
| 项目特定流程 | — | 该项目独有的 skill |
| 临时实验 | — | 放项目里,验证后再提升为全局 |

### 各 Runtime 全局/项目级对照

| Runtime | 全局位置 | 项目级位置 | 优先级 |
|---------|---------|-----------|--------|
| Claude Code | `~/.claude/skills/`(Personal)或 Plugin | `.claude/skills/`(Project) | Enterprise > Personal > Project > Plugin |
| Codex | Plugin 安装默认全局 | — | — |
| Hermes | `~/.hermes/skills/` | `external_dirs` 配置项目路径 | 全局 > external_dirs |
| Cursor | Plugin 安装默认全局 | — | — |
| Kimi Code | Plugin 安装默认全局 | — | — |

### Claude Code 三级目录

Claude Code 启动时扫描三个目录,优先级从高到低:

```
~/.claude/skills/        # Personal(全局,所有项目生效)
.claude/skills/          # Project(当前项目生效)
Plugin 提供              # Plugin 安装的技能
```

> 同名技能,高优先级覆盖低优先级。这让你可以在项目级覆盖全局技能的行为。

### Hermes external_dirs

Hermes 通过 `config.yaml` 的 `external_dirs` 配置项目级技能:

```yaml
skills:
  external_dirs:
    - /path/to/project/.hermes/skills
    - /path/to/team/shared-skills
```

全局技能在 `~/.hermes/skills/`,项目技能通过 `external_dirs` 追加。

## 自己的技能怎么跨 Runtime

如果你自己写了一个技能,想跨 runtime 使用:

### 方式一:符号链接(推荐,本地开发)

```bash
# 规范源放在知识库的 01-Skills/my-skill/
# 软链到各 runtime 的全局目录

# Claude Code
ln -s /path/to/01-Skills/my-skill ~/.claude/skills/my-skill

# Hermes
ln -s /path/to/01-Skills/my-skill ~/.hermes/skills/my-skill
```

优点:改一处,全部生效。缺点:Windows 上符号链接需要管理员权限。

### 方式二:适配层打包(推荐,分发)

仿照 Superpowers,创建 runtime 适配目录:

```
my-skill/
├── skills/
│   └── my-skill/
│       └── SKILL.md          # 规范源
├── .claude-plugin/
│   └── plugin.json           # Claude Code 清单
├── .codex-plugin/            # Codex 适配
└── scripts/
    └── sync.sh               # 同步脚本
```

### 方式三:Marketplace 发布(推荐,公开分发)

注册到 runtime 的 marketplace,用户通过 `/plugin install` 一键安装。

## 常见误区

### 误区 1:每个 runtime 复制一份技能源

改一次要同步 N 处,早晚遗漏。

**修正**:规范源只有一份,用符号链接或适配层同步。

### 误区 2:把项目级技能放全局

导致其他项目也被不相关的技能干扰。

**修正**:项目特定的技能放项目目录(`.claude/skills/` 或 `external_dirs`)。

### 误区 3:把全局技能放项目里

换项目就用不了了。

**修正**:跨项目通用的技能放全局(`~/.claude/skills/` 或 `~/.hermes/skills/`)。

### 误区 4:技能源和 runtime 配置混在一起

SKILL.md 和 `plugin.json` 混在一个目录,难以跨 runtime 复用。

**修正**:规范源(`skills/`)和适配层(`.xxx-plugin/`)分离。

## 与其他概念的关系

| 概念 | 解决的问题 | 和跨 Runtime 技能管理的关系 |
|------|----------|---------------------------|
| Skill | 任务怎么做 | 跨 runtime 管理的对象 |
| Plugin | 怎么扩展宿主 | Skill 的 runtime 适配形态之一 |
| Runtime | 在哪里跑 | 决定了适配层长什么样 |
| Marketplace | 怎么分发 | Plugin 的分发渠道 |

详见 [概念全景辨析](../02-概念全景辨析.md)。

## 相关文件

- [如何编写 Skill](./01-如何编写Skill.md) — Skill 标准格式和编写规范
- [概念全景辨析](../02-概念全景辨析.md) — Skill vs Plugin vs MCP 的区别
- [Superpowers 技能引用](../../01-Skills/superpowers/SKILL.md) — 跨 runtime 技能集的参考实现
- [Superpowers 安装详情](../../01-Skills/superpowers/references/installation-per-runtime.md) — 各 runtime 安装方式
- [Hermes Agent 专题](../runtime/02-Hermes-Agent/README.md) — Hermes 中 Skill 的实现细节
