---
name: project-init
description: >
  Initialize a project-level Agent environment from scratch: scaffold `.agent/` directory
  and `AGENTS.md` in the current project, then deploy recommended skills/plugins/MCPs based
  on the project type. Use when the user says "初始化项目 Agent 环境","初始化项目",
  "搭建项目级 .agent/","init project","init agent env","把知识库里的资产部署到这个项目"
  in a project root (not the knowledge base itself). Detects the current Runtime, runs a
  short AI-guided interview (project purpose / stack / stage / constraints), matches skills
  from KB's `01-Skills/`, generates a 7-section AGENTS.md, then bridges `.agent/` to the
  Runtime's native directory per `00-AgentBase/runtime/00-项目级配置.md`.
version: 1.0.0
status: 可用
level: project
imported: 2026-07-10
updated: 2026-07-10
---

# project-init — 项目级 Agent 环境初始化

> 当用户在一个 **项目目录**(不是知识库)里说"初始化项目 Agent 环境",触发本 Skill。
> 区分 `kb-init`:本 Skill 初始化的是 **项目** 的 `.agent/`,`kb-init` 初始化的是 **知识库** 本身。

## When to Use

**适用**:
- 用户进入一个新项目目录,说"初始化项目"/"搭建项目级 Agent 环境"/"init project"
- 用户想把知识库 `${KB_ROOT}` 里的资产部署到当前项目
- 用户给项目一句话描述,问"这个项目怎么用 Agent"
- git 仓库初始化后,想配套建 Agent 环境

**不适用**(用其他 Skill 或流程):
- 当前目录就是知识库根 `${KB_ROOT}` 本身 → 用 `kb-init`
- 已有 `.agent/`,想加新 skill → 走单 skill 部署(`01-Skills/AGENTS.md` §3)
- 只想要单个 skill 部署 → 不需要本 Skill,直接复制
- 用户要改 AGENTS.md 内容 → 用 `agents-md-author`
- 纯对话任务,无项目结构 → 不需要 Agent 环境

## Inputs

执行前需要以下上下文:
- **当前项目根目录**(PWD)
- **知识库根目录**(`$KB_ROOT`,由调用方提供:环境变量 / CLI 参数 / AI 从上下文推导)
- **当前 Runtime**(自动检测)
- **用户对项目的描述**(可一句话,可详细)

如果用户没给项目描述,按 Step 2 跑问卷。

## Procedure

### Step 1:检测 Runtime

调用 `scripts/detect-runtime.ps1`,识别:

| Runtime | 检测信号 |
|---------|----------|
| `claude-code` | 环境变量 `CLAUDE_CODE` 或目录 `.claude/` |
| `codex` | 环境变量 `CODEX` / `CODEX_HOME` 或目录 `.codex/` |
| `hermes` | 环境变量 `HERMES_HOME` 或目录 `.hermes/` |
| `trae` | 目录 `.trae/` |
| `multi` | 多个 Runtime 同时存在 |
| `unknown` | 都检测不到 |

**关键**:如果当前目录在知识库根 `${KB_ROOT}` 内,**不要**初始化——这是知识库本身,引导用户用 `kb-init`。

详见 [references/runtime-detect.md](./references/runtime-detect.md)。

### Step 2:AI 引导式问卷(可一句给完)

如果用户已经给了项目描述(一句话或多句),直接进 Step 3;否则按 [references/interview.md](./references/interview.md) 跑 4 个核心问题:

1. **项目做什么** — 一句话 + 标签(`web` / `backend` / `数据` / `内容` / `agent` / `通用`)
2. **技术栈** — 主要语言、框架、部署目标
3. **团队规模 / 阶段** — `mvp` / `增长` / `稳定`
4. **边界要求** — 密钥、提交限制、确认策略

每个问题 1 行,用户可一次给完。可跳过,默认"通用 + 待定"。

### Step 3:匹配 skill 组合

按 [references/skill-matrix.md](./references/skill-matrix.md) 的映射表,根据项目标签推荐 skill 组合:

| 项目标签 | 推荐 skill |
|----------|------------|
| `web` / `frontend` | `ui-ux-pro-max` + `superpowers`(TDD/调试) |
| `backend` | `superpowers` + `development-agent` |
| `agent` / `ai-app` | `superpowers` + `agents-md-author` + `loop-engineering` |
| `内容` / `内容创作` | `baoyu-skills` |
| `数据` | `superpowers` + `development-agent` |
| `obsidian` | `kepano-obsidian-skills` |
| `通用` | `superpowers`(可选 `development-agent`) |

**强制包含**:`agents-md-author`(项目级 AGENTS.md 编写规范)。

输出推荐列表,**向用户确认**后再部署。

### Step 4:生成项目级 AGENTS.md

按 `00-AgentBase/runtime/00-项目级配置.md` §2.2 的 7 段模板,根据 Step 2 的回答填充:

1. 项目是什么(一句话)
2. 技术栈
3. 关键约定
4. 常用命令
5. 边界
6. 项目级资产(指向 `.agent/`)
7. 资产来源(指向 `$KB_ROOT`)

**调用 `agents-md-author` 子流程**:本 Skill 不直接写 AGENTS.md,而是委派给 `agents-md-author`,强制遵守"不写'为什么'段、不重复知识库内容、用结构化数据、单文件 < 500 行"等规范。

**写之前先向用户展示草稿**,得到确认再写入。

### Step 5:部署

调用 `scripts/scaffold.ps1`,完成以下动作(详见 [references/deploy.md](./references/deploy.md)):

1. 创建 `.agent/` 7 个子目录(`skills/`、`agents/`、`plugins/`、`prompts/`、`mcp/`、`hooks/`、`memory/`)
2. 从 `$KB_ROOT\01-Skills\` 按 Step 3 选中的列表,软链/复制到 `.agent/skills/`
3. 按当前 Runtime 桥接 `.agent/skills/` 到 Runtime 原生目录:
   - `claude-code`:`.claude/skills/` → `../.agent/skills`(junction)
   - `codex`:`.codex/skills/` → `../.agent/skills`(junction 或 `external_dirs` 配置)
   - `hermes`:写到 `~/.hermes/config.yaml` 的 `external_dirs`
   - `trae`:`.trae/skills/` → `../.agent/skills`(junction)
4. 写 `.agent/AGENTS.md`(项目级 Skill/Plugin/MCP 索引,如需要)
5. 写推荐的 `.gitignore`:`.agent/cache/`、`.agent/memory/.session/`、`.agent/mcp/*-local.json`
6. 输出部署报告(创建了什么、软链了什么、桥接到哪里)

**复用现有脚本**:`00-AgentBase/runtime/00-项目级配置.md` §5 的 `deploy-assets.ps1` 是参考实现,本 Skill 的 `scaffold.ps1` V1 直接内联其核心逻辑,后续可重构为引用。

### Step 6:验证

跑完部署后,逐项验证:

- [ ] `AGENTS.md` 在项目根,7 段齐全
- [ ] `.agent/` 7 个子目录已创建
- [ ] `.agent/skills/<每个选中的 skill>/` 可访问
- [ ] 当前 Runtime 的原生目录已桥接(junction / external_dirs / config)
- [ ] `.gitignore` 推荐项已写入
- [ ] Runtime 启动后能读到 `AGENTS.md`
- [ ] 至少一个选中 skill 能被 Runtime 加载(可手动触发描述测试)
- [ ] 无敏感信息泄露(密钥、PII)

任一项失败,根据 `references/deploy.md` §"故障排查"定位。

## Pitfalls

- **在知识库根目录执行** → Step 1 必须先检测 PWD,不是 `$KB_ROOT` 才继续
- **跳过 AI 引导直接套模板** → 不同项目类型边界/约定差异大,模板不是万能
- **复制而不是软链** → 软链能跨 Runtime 共享、源更新自动生效;复制需手动同步
- **把 Runtime 原生目录当 `.agent/` 用** → 违反"统一目录"原则,换 Runtime 要重命名
- **AGENTS.md 写太长** → 委托 `agents-md-author`,强制 < 500 行
- **忘了 `.gitignore`** → 团队成员拉下来会有 `.agent/cache/` 噪音
- **重复安装 skill 到多个 Runtime** → 在 multi Runtime 下,只装一次到 `.agent/skills/`,桥接 N 次
- **把"实时状态"写进 AGENTS.md** → 价格、订单等运行时数据用工具查,不进文档

## Verification

部署前(检查用户输入):
- [ ] 确认 PWD 不是 `$KB_ROOT`
- [ ] 确认用户已给出(或同意问卷得到)项目描述
- [ ] 确认 Step 3 的 skill 列表用户已确认

部署后(检查产物):
- [ ] `AGENTS.md` 已写入项目根(7 段)
- [ ] `.agent/` 7 个子目录已建
- [ ] 选中 skill 已软链到 `.agent/skills/`
- [ ] Runtime 原生目录已桥接
- [ ] `.gitignore` 已写
- [ ] 验证清单(Step 6)全部勾选

## 相关知识

- [`00-AgentBase/runtime/00-项目级配置.md`](../../00-AgentBase/runtime/00-项目级配置.md) — `.agent/` 目录规范(本 Skill 的核心依据)
- [`01-Skills/kb-init/SKILL.md`](../kb-init/SKILL.md) — 知识库自身初始化(区分用)
- [`01-Skills/agents-md-author/SKILL.md`](../agents-md-author/SKILL.md) — AGENTS.md 编写规范(本 Skill Step 4 委派)
- [`01-Skills/AGENTS.md`](../AGENTS.md) — Skill 入库标准与部署流程
- [`01-Skills/_template.skill.md`](../_template.skill.md) — Skill 编写模板
- [`00-AgentBase/behavior/01-如何编写Skill.md`](../../00-AgentBase/behavior/01-如何编写Skill.md) — Skill 设计原则
