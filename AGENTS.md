# AGENTS.md — Agent 环境部署、编排与管理指南

> 本文件指导如何基于知识库(`00-AgentBase/`)搭建、部署、编排**并持续管理** Agent 环境。
>
> 知识库管理员规范(入库标准 + 管理流程)见 [`00-AgentBase/AGENTS.md`](./00-AgentBase/AGENTS.md)。

---

## 0. 架构总览

```
┌──────────────────────────────────────────────────────────┐
│                    整体架构                                │
│                                                          │
│  ┌─────────────────────┐                                 │
│  │  00-AgentBase/      │  大脑:知识库                     │
│  │  Agent 知识库        │  Agent 是什么、怎么搭、怎么管     │
│  │  (AGENTS.md=管理员) │  入库标准+管理流程:编译、审查、更新 │
│  └──────────┬──────────┘                                 │
│             │ 提供认知                                    │
│             ▼                                            │
│  ┌─────────────────────┐                                 │
│  │  根目录 AGENTS.md    │  手脚:部署、编排与管理指南       │
│  │  (本文件)            │  基于知识库搭建、编排并管理 Agent │
│  └──────────┬──────────┘                                 │
│             │ 指导获取/生成/管理                            │
│             ▼                                            │
│  ┌─────────────────────────────────────────────────┐    │
│  │  01-Skills/  02-Plugins/  03-Prompts/           │    │
│  │  04-MCP/     05-Boundaries/ 06-Migration/       │    │
│  │  工具箱:已生成好的资产,拿来即用,持续维护          │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

三层关系:

| 层 | 角色 | 内容 |
|---|---|---|
| `00-AgentBase/` | **大脑** | Agent 相关的所有知识。人类看懂,Agent 当 wiki 读 |
| 根目录 `AGENTS.md` | **手脚** | 部署、编排与管理指南。基于知识库搭建、编排并持续管理 Agent |
| `01-06/` | **工具箱** | 已生成好的 skill、已获取的 plugin、验证过的 prompt,拿来即用,持续维护 |

本文件覆盖 Agent 生命周期的三个阶段:

| 阶段 | 章节 | 做什么 |
|------|------|--------|
| **部署** | § 1-3 | 前置条件、部署流程、资产获取 |
| **编排** | § 4-5 | 组装组件、验证可用性 |
| **管理** | § 6 | Runtime 切换、生命周期、配置、资产盘点、监控排障 |

---

## 0.1 项目级目录规范(`.agent/`)

每个**使用知识库的项目**都应在项目根按统一规范创建 `.agent/` 目录和 `AGENTS.md`:

```
你的项目/
├── AGENTS.md          ← 项目指令(项目根,所有 Runtime 都能读)
├── .agent/            ← 项目级资产(统一目录,跨 Runtime 一致)
│   ├── skills/
│   ├── agents/
│   ├── plugins/
│   ├── prompts/
│   ├── mcp/
│   ├── hooks/
│   └── memory/
└── 你的项目文件...
```

**为什么统一目录名**:
- 换 Runtime 不需要改目录结构
- 团队成员各自维护不同 Runtime,但项目结构一致
- 部署脚本可复用

**完整规范**:[`00-AgentBase/runtime/00-项目级配置.md`](./00-AgentBase/runtime/00-项目级配置.md)

---

## 1. 前置条件

搭建 Agent 环境前,先从知识库获取认知:

1. 读 [`00-AgentBase/01-AgentBase总览.md`](./00-AgentBase/01-AgentBase总览.md) — 理解知识库结构(Agent 基础概念见 [`00-human/`](./00-AgentBase/00-human/README.md))
2. 读 [`00-AgentBase/03-知识地图.md`](./00-AgentBase/03-知识地图.md) — 理解七大模块
3. 读 [`00-AgentBase/runtime/01-Agent运行时与CLI.md`](./00-AgentBase/runtime/01-Agent运行时与CLI.md) — 选择运行时
4. 读 [`00-AgentBase/runtime/02-Hermes-Agent/`](./00-AgentBase/runtime/02-Hermes-Agent/README.md) — 选择具体工具(含安装/配置/安全等 11 篇专题)
5. 读 [`00-AgentBase/runtime/03-ClaudeCode/`](./00-AgentBase/runtime/03-ClaudeCode/README.md) — Anthropic 官方 CLI 工具(含安装/配置/工具/技能/记忆/子代理/MCP/Hooks/权限/IDE集成/架构等 12 篇专题)
6. 读 [`00-AgentBase/runtime/04-Codex-CLI/`](./00-AgentBase/runtime/04-Codex-CLI/README.md) — OpenAI 官方 CLI 工具(含安装/配置/安全审批/MCP/自定义技能/架构等 7 篇专题)

环境要求:

- **运行时**:根据知识库 runtime 模块的指导选择(Claude Code / Codex / Hermes / 其他)
- **权限**:文件读写、Shell 执行、网络访问(按需)
- **依赖**:Node.js / Python / Rust(根据选择的 runtime 和工具确定)

---

## 2. 部署流程

```
① 获取认知(从 00 知识库)
  理解 Agent 组成 → 选择 runtime → 确定需要哪些模块
         ↓
② 安装运行时(从 00 runtime 模块获取指导)
  安装 CLI / Harness → 配置身份认证 → 验证基础可用
         ↓
③ 获取实践资产(从 01-06 工具箱)
  Skills:  自己生成 or 获取别人已做好的
  Plugins: 安装现成的
  Prompts: 拿验证过的模板
  MCP:     配置 server
         ↓
④ 编排组装(本文件 § 4)
  把 skill/plugin/prompt/mcp 组装成可运行的 Agent
         ↓
⑤ 设置安全边界(从 05-Boundaries 获取规则)
  配置护栏 → 设置权限分级 → 定义确认策略
         ↓
⑥ 验证(本文件 § 5)
  跑通最小任务 → 验证边界生效 → 确认知识库可被检索
         ↓
⑦ 持续管理(本文件 § 6)
  Runtime 切换/更新 → 配置调整 → 资产维护 → 监控排障
```

---

## 3. 实践层资产获取

### 3.1 `01-Skills/` — 技能

本目录是所有技能的**唯一规范源**(Canonical Source)。**技能平铺存放,不分子目录**——`global/` 和 `projects/` 已合并到顶层。部署、分类标准、更新流程详见 [`01-Skills/AGENTS.md`](./01-Skills/AGENTS.md)。

**核心理念**:
- 源只有一份:修改只在 `01-Skills/` 中改,然后同步到各 Runtime
- **不分类,让 AI 决定部署位置**:技能本身没有"全局"或"项目级"属性,这是部署时的判断。AI 根据上下文决定部署到 Personal(`~/.claude/skills/`)、Project(`.claude/skills/`)还是 Plugin
- 拒绝默认垃圾技能:Runtime 自带技能若不需要一律禁用,只用 `01-Skills/` 的

**获取方式**:
- 自己生成:基于知识库 `00-AgentBase/behavior/` 的认知,编写 skill 定义文件
- 获取现成:从社区/市场获取别人已做好的 skill(如 superpowers),放入 `01-Skills/` 顶层

**使用方式**:按 `01-Skills/AGENTS.md` §3.1 的 AI 决策流程,执行部署并验证

**认知来源**:[`00-AgentBase/behavior/`](./00-AgentBase/behavior/) — Skill 是什么、怎么设计

### 3.2 `02-Plugins/` — 插件

**获取方式**:
- 安装现成的:按插件文档安装,配置模板存入本目录
- 自己封装:基于知识库 `00-AgentBase/tools/` 的认知,封装自定义插件

**使用方式**:在 Agent 运行时加载,扩展工具能力

**认知来源**:[`00-AgentBase/tools/`](./00-AgentBase/tools/) — Plugin 是什么、怎么配

### 3.3 `03-Prompts/` — 提示词

**获取方式**:
- 拿验证过的:经过实际使用验证有效的 prompt 模板
- 自己编写:基于知识库 `00-AgentBase/behavior/` 的认知

**使用方式**:作为 Agent 的 System Prompt 或任务 Prompt 模板

**认知来源**:[`00-AgentBase/behavior/`](./00-AgentBase/behavior/) — Prompt 的作用和设计原则

### 3.4 `04-MCP/` — MCP Server

**获取方式**:
- 配置现成 server:按 MCP server 文档配置,连接信息存入本目录
- 自己开发:基于知识库 `00-AgentBase/tools/` 的认知

**使用方式**:在 Agent 运行时连接 MCP server,获取工具能力

**认知来源**:[`00-AgentBase/tools/`](./00-AgentBase/tools/) — MCP 协议是什么

### 3.5 `05-Boundaries/` — 安全边界

**获取方式**:
- 基于知识库 `00-AgentBase/safety/` 的认知,编写具体边界规则
- 参考通用安全策略模板

**使用方式**:作为 Agent 的护栏配置,约束行为范围

**认知来源**:[`00-AgentBase/safety/01-Agent边界与限制.md`](./00-AgentBase/safety/01-Agent边界与限制.md)

### 3.6 `06-Migration/` — 迁移

**获取方式**:
- 在实际迁移过程中记录步骤,沉淀为 playbook
- 参考知识库 `00-AgentBase/runtime/` 的工具对比

**使用方式**:版本升级或平台切换时按步骤执行

**认知来源**:[`00-AgentBase/runtime/`](./00-AgentBase/runtime/) — 迁移的本质和工具差异

---

## 4. 编排

把工具箱里的资产组装成可运行的 Agent:

```
┌─────────────── Agent 编排 ───────────────┐
│                                          │
│  Runtime(CLI/Harness)                    │
│    ├── System Prompt(03-Prompts/)        │
│    ├── Skills(01-Skills/)                │
│    ├── Tools                             │
│    │   ├── Built-in                      │
│    │   ├── Plugins(02-Plugins/)          │
│    │   └── MCP Servers(04-MCP/)          │
│    ├── Knowledge(00-AgentBase/ as wiki)  │
│    └── Boundaries(05-Boundaries/)        │
│                                          │
└──────────────────────────────────────────┘
```

编排步骤:

1. **确定 Runtime**:从知识库选择 CLI/Harness
2. **配置 Prompt**:从 `03-Prompts/` 选择或编写 System Prompt
3. **加载 Skills**:从 `01-Skills/` 选择需要的技能
4. **接入 Tools**:加载 `02-Plugins/` 插件 + 连接 `04-MCP/` server
5. **挂载知识库**:将 `00-AgentBase/` 作为 Agent 的 wiki,供其检索
6. **设置边界**:从 `05-Boundaries/` 加载护栏配置
7. **验证**:跑通最小任务(见 § 5)

---

## 5. 部署验证

部署完成后,逐项验证:

- [ ] Runtime 可启动,基础对话正常
- [ ] 至少 1 个 Skill 可被调用并执行
- [ ] 至少 1 个 Plugin/MCP Tool 可被调用
- [ ] Prompt 模板加载正确,Agent 行为符合预期
- [ ] 边界规则生效:禁止操作被拦截
- [ ] 知识库可被检索:Agent 能引用 `00-AgentBase/` 中的内容
- [ ] 无敏感信息泄露(密钥、PII)

验证失败时:
- Runtime 问题 → 查 `00-AgentBase/runtime/`
- 工具问题 → 查对应 `02-Plugins/` 或 `04-MCP/` 的排障
- 行为问题 → 查 `03-Prompts/` 模板是否正确
- 安全问题 → 查 `05-Boundaries/` 规则是否生效

---

## 6. Agent 管理

Agent 环境部署完成后,需要持续管理:Runtime 切换、版本更新、配置调整、资产维护、监控排障。

### 6.1 Runtime 管理

知识库 runtime 模块收录了多种 Agent 运行时,各有适用场景:

| Runtime | 适用场景 | 认知来源 |
|---------|----------|----------|
| Claude Code | 多表面(终端/IDE/Web)、丰富工具生态、Agentic 循环、Hooks/子代理 | [`03-ClaudeCode/`](./00-AgentBase/runtime/03-ClaudeCode/README.md) |
| Codex CLI | OpenAI 生态、安全审批流程、自定义技能 | [`04-Codex-CLI/`](./00-AgentBase/runtime/04-Codex-CLI/README.md) |
| Hermes Agent | 轻量级、消息网关、定时任务、自定义工作流 | [`02-Hermes-Agent/`](./00-AgentBase/runtime/02-Hermes-Agent/README.md) |

管理操作:

| 操作 | 说明 |
|------|------|
| **安装** | 按各 runtime 专题文档的安装部署章节执行 |
| **更新** | Claude Code 自动更新(可配 `stable`/`latest` 渠道);Codex/Hermes 需手动更新 |
| **切换** | 不同 runtime 可共存,按项目需求选择。切换时注意工具等价性和配置差异 |
| **卸载** | 参见各 runtime 专题文档的卸载章节 |
| **迁移** | 参考 [`06-Migration/`](./06-Migration/) 和知识库 runtime 模块的迁移指导 |

> **类比**:Runtime 像"操作系统"——Claude Code 是功能丰富的桌面 OS,Codex 是安全优先的服务器版,Hermes 是轻量嵌入式。它们可以装在同一台机器上,按场景选择启动哪个。

### 6.2 生命周期管理

| 操作 | Claude Code | Codex CLI | Hermes Agent |
|------|-------------|-----------|--------------|
| 启动 | `claude` | `codex` | 参见 Hermes 文档 |
| 后台运行 | `claude --bg` | 参见 Codex 文档 | 参见 Hermes 文档 |
| 会话恢复 | `claude -c` / `claude -r` | 参见 Codex 文档 | 参见 Hermes 文档 |
| 健康检查 | `claude doctor` | 参见 Codex 文档 | 参见 Hermes 文档 |
| 定时任务 | Routines / Desktop scheduled | 参见 Codex 文档 | Cron 系统 |

> 各 runtime 的具体命令参见其专题文档,此处仅做跨 runtime 对照。

### 6.3 配置管理

跨 runtime 的配置对照:

| 配置项 | Claude Code | Codex CLI | Hermes Agent |
|--------|-------------|-----------|--------------|
| 项目配置 | `.claude/settings.json` | `.codex/` | Hermes 配置文件 |
| 用户配置 | `~/.claude/` | `~/.codex/` | Hermes 用户配置 |
| 权限规则 | `permissions.allow/deny` | 审批策略 | 安全机制 |
| 持久指令 | `CLAUDE.md` | `AGENTS.md` 兼容 | 系统提示 |
| MCP 配置 | `.mcp.json` / `~/.claude.json` | MCP server 配置 | MCP 集成 |
| 技能 | `.claude/skills/` | 自定义技能 | 技能系统 |

**管理原则**:

- 项目级配置纳入版本控制,团队成员共享
- 敏感信息(API key、token)放 local 配置(`.gitignore`)
- 切换 runtime 时,对照上表确认配置等价性
- 配置变更后验证 Agent 行为(见 § 5)

### 6.4 资产清单管理

定期盘点 `01-06/` 实践层资产,维护可用性:

| 目录 | 内容 | 盘点频率 | 每项应标注 |
|------|------|----------|------------|
| `01-Skills/` | 可复用技能 | 新增/删除时 | 适用 runtime、来源、版本、状态 |
| `02-Plugins/` | 插件配置 | 新增/删除时 | 适用 runtime、来源、版本、状态 |
| `03-Prompts/` | 提示词模板 | 新增/删除时 | 适用场景、来源、状态 |
| `04-MCP/` | MCP server 配置 | 新增/删除时 | 适用 runtime、传输方式、状态 |
| `05-Boundaries/` | 安全边界规则 | 定期审查 | 适用 runtime、严格程度 |
| `06-Migration/` | 迁移 playbook | 迁移完成后 | 源/目标 runtime、版本 |

资产状态标记:

| 状态 | 含义 |
|------|------|
| `验证中` | 刚获取/生成,尚未验证可用性 |
| `可用` | 已通过 § 5 验证,可投入编排 |
| `弃用` | 不再维护,待清理 |

### 6.5 监控与排障

| 问题类型 | 排查方向 | 知识库参考 |
|----------|----------|------------|
| Runtime 无法启动 | 安装问题、认证失败、依赖缺失 | 对应 runtime 专题的安装部署章节 |
| 工具调用失败 | 权限规则、MCP 连接、插件加载 | 对应 runtime 工具系统 + [`04-MCP/`](./04-MCP/) |
| Agent 行为异常 | Prompt 模板、技能加载、记忆内容 | [`03-Prompts/`](./03-Prompts/) + [`01-Skills/`](./01-Skills/) |
| 安全边界未生效 | 权限规则、边界配置 | [`05-Boundaries/`](./05-Boundaries/) |
| 性能问题 | 上下文过大、工具过多、模型选择 | 对应 runtime 的架构设计章节 |

诊断命令对照:

| Runtime | 诊断 |
|---------|------|
| Claude Code | `claude doctor`、`claude --debug` |
| Codex CLI | 参见 [`04-Codex-CLI/`](./00-AgentBase/runtime/04-Codex-CLI/README.md) |
| Hermes Agent | 参见 [`02-Hermes-Agent/`](./00-AgentBase/runtime/02-Hermes-Agent/README.md) |

### 6.6 版本升级管理

Runtime 版本升级流程:

1. **查阅变更日志**:对应 runtime 专题文档或官方 CHANGELOG
2. **评估影响范围**:是否破坏现有配置、技能、MCP 兼容性
3. **在测试环境验证**:克隆配置,升级后跑通 § 5 验证清单
4. **记录到迁移日志**:如有 breaking change,更新 [`06-Migration/`](./06-Migration/) playbook
5. **灰度推广**:先个人环境,再团队环境
6. **回滚准备**:记录当前版本号,确保可快速回退

---

## 7. 防信息孤岛

### 7.1 连接要求

每篇文档发布时必须同时满足:

- **入口 ≥ 1**:被索引、知识地图、或至少 1 篇文档引用
- **出口 ≥ 1**:文档末尾有相关链接(总览文档除外)
- **零死链**:所有内部链接指向真实存在的文件

### 7.2 双向引用

A 引用 B 时,B 必须回引 A。例外:目录索引和知识地图作为导航枢纽,不需要被全部回引。

### 7.3 孤岛巡检

定期执行(每月):
1. 遍历所有 `.md` 文件
2. 检查无入口(孤岛)→ 补充引用或弃用
3. 检查无出口(死胡同)→ 补充相关链接
4. 检查死链 → 修复或删除

---

## 8. 版本管理

### 8.1 语义化版本

- **X**(主版本):架构调整、环境重建、职责范围扩展
- **Y**(次版本):新增 skill/plugin/prompt、新增 runtime 专题
- **Z**(修订):配置微调、错别字

### 8.2 Git 提交规范

```
deploy:   安装 Codex CLI 并配置基础环境       # 部署
orchestrate: 编排 code-review skill          # 编排
manage:   将 Claude Code 升级到 stable 渠道    # 管理
docs(00): 新增 Agent 运行时概念说明            # 知识库入库(见 00/AGENTS.md)
docs(01): 沉淀 Skill 定义模板至实践层          # 资产沉淀
chore:    更新知识地图索引
```

---

## 9. 安全与合规

### 9.1 禁止内容

- ❌ 真实密钥 / Token / 密码
- ❌ 个人隐私信息(PII)
- ❌ 未授权的第三方版权材料
- ❌ 内部未公开接口

### 9.2 敏感操作审计

以下操作需记录到 `99-Roadmap.md`:
- 删除已发布文档或资产
- 调整目录结构
- 修改部署配置
- 迁移运行时
- Runtime 版本升级(主版本)

---

## 10. 自检清单

每次部署、编排或管理操作前过一遍:

**部署阶段**:
- [ ] 已从知识库获取必要认知(读了 00 对应模块)?
- [ ] Runtime 已安装并验证可用?
- [ ] 需要的 skill/plugin/prompt/mcp 已就位?

**编排阶段**:
- [ ] 编排组装完成,各组件引用正确?
- [ ] 边界规则已配置并生效?
- [ ] 部署验证全部通过?

**管理阶段**:
- [ ] 资产清单已盘点,状态标注完整?
- [ ] Runtime 版本已确认,更新渠道已配置?
- [ ] 配置已纳入版本控制(项目级),敏感信息已隔离(local)?
- [ ] 监控排障路径已建立(知道该查哪个知识库章节)?

**通用**:
- [ ] 新资产已关联到知识库对应概念?
- [ ] 无敏感信息泄露?

---

> **维护责任人**:Agent Environment Operator
> **最后更新**:2026-07-09
> **文档版本**:v4.0.0(新增 Agent 管理章节,职责从部署编排扩展为部署+编排+管理)
