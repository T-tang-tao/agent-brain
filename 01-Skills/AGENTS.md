# AGENTS.md — 个人技能库管理规范

> 本文件定义 `01-Skills/` 作为**唯一技能规范源**(Canonical Source),并指导如何将技能部署到不同 Runtime。
>
> 部署、编排与管理总指南见 [根目录 AGENTS.md](../AGENTS.md)。

---

## 0. 核心理念

```
┌─────────────────────────────────────────────┐
│         01-Skills/ (规范源 / 唯一真相)        │
│                                             │
│  <skill-name>/           ← 平铺存放          │
│  _template.skill.md      ← 新技能模板        │
│  AGENTS.md               ← 管理规范          │
└──────────────────┬──────────────────────────┘
                   │ 部署(AI 判断目标位置)
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Claude Code   Codex      Hermes
   ~/.claude/    ~/.codex/  ~/.hermes/   ← Personal(个人全局)
   .claude/      项目级     external_dirs ← Project(项目级)
   <plugin>/     <plugin>/  <plugin>/    ← Plugin(插件)
```

**三条铁律**:

1. **源只有一份**:`01-Skills/` 是所有技能的唯一规范源,修改只在这里改
2. **不分类,让 AI 决定部署位置**:技能本身没有"全局"或"项目级"属性,这是**部署时**的判断。AI 根据上下文决定部署到 Personal、Project 还是 Plugin
3. **拒绝默认垃圾技能**:Runtime 自带的技能若不需要一律禁用,只用自己 `01` 下的技能

> **类比**:`01-Skills/` 像"菜谱库"——所有菜谱统一编写和改进。各 Runtime 像"厨房",AI 按需把菜谱复制到不同厨房位置(个人习惯/项目约定/插件)。

---

## 1. 目录结构

```text
01-Skills/
├── AGENTS.md                  ← 本文件:管理规范
├── README.md                  ← 目录说明和技能清单
├── _template.skill.md         ← 新技能模板
│
├── kb-init/                   ← 从零初始化知识库(全局可用)
│   ├── SKILL.md
│   └── references/
│
├── agents-md-author/          ← AGENTS.md 编写规范(强制)
│   ├── SKILL.md
│   └── references/
│       ├── rules.md
│       └── templates.md
│
├── loop-engineering/          ← Agent Loop 设计(强制)
│   ├── SKILL.md
│   └── references/
│       ├── five-elements.md
│       ├── three-pitfalls.md
│       └── template.md
│
├── superpowers/               ← 跨 Runtime 开发方法论(14 子技能)
│   ├── SKILL.md
│   ├── hooks/
│   ├── scripts/
│   ├── skills/                ← 完整离线内容
│   └── references/
│       └── installation-per-runtime.md
│
├── ui-ux-pro-max/             ← UI/UX 设计情报(7 子技能,项目级)
│   ├── SKILL.md
│   ├── plugin.json
│   ├── LICENSE
│   ├── README.source.md
│   ├── references/
│   │   └── installation-per-runtime.md
│   └── skills/                ← 完整离线内容
│
├── anthropics-skills/         ← Anthropic 官方(17 子技能,445 文件)
│   ├── SKILL.md
│   ├── README.md
│   ├── LICENSE
│   ├── .claude-plugin/
│   ├── spec/
│   ├── template/
│   └── skills/                ← 409 文件
│
├── baoyu-skills/              ← 宝玉中文内容创作(21 子技能,950 文件)
│   ├── SKILL.md
│   ├── README.md / README.zh.md
│   ├── CHANGELOG.md
│   ├── CLAUDE.md
│   ├── LICENSE
│   ├── packages/
│   ├── screenshots/
│   └── skills/                ← 474 文件
│
└── kepano-obsidian-skills/    ← Obsidian 官方维护者(5 子技能,15 内容文件+29 git 元数据)
    ├── SKILL.md
    ├── README.md
    ├── LICENSE
    ├── .claude-plugin/
    └── skills/                ← 10 文件
│
└── kimi-webbridge/             ← Kimi WebBridge 浏览器自动化(本地守护进程)
    ├── SKILL.md               ← 本知识库补充入库说明
    └── references/
        └── installation.md    ← 本知识库补充安装部署指南
```

> 决策记录(平铺存放理由):见 [99-Roadmap.md 决策日志](../99-Roadmap.md)。

---

## 2. 技能注册表

每个技能在下表登记基本信息。**分类列取消**——部署目标由 AI 判断。

| 技能 | 用途 | 文件数 | 状态 |
|------|------|--------|------|
| `kb-init` | 从零初始化专业个人知识库 | 4 | 可用 |
| `agents-md-author` | 编写 / 修改 AGENTS.md 时强制遵循简洁规范(不解释原因、直接执行) | 4 | 可用 |
| `loop-engineering` | 设计 Agent Loop(自动化循环系统),含五要素+三陷阱+模板 | 5 | 可用 |
| `superpowers` | 跨 Runtime 开发方法论(14 个子技能) | 58 | 可用 |
| `ui-ux-pro-max` | UI/UX 设计情报(7 个子技能,含 54 个字体) | 229 | 可用 |
| `anthropics-skills` | Anthropic 官方 Skills(17 子技能,4 个生产级文档技能 + skill-creator + canvas-design 等) | 445 | 可用 |
| `baoyu-skills` | 宝玉中文内容创作(21 子技能,小红书/信息图/公众号/AI 生图) | 950 | 可用 |
| `kepano-obsidian-skills` | Obsidian 官方维护者(5 子技能,markdown/bases/canvas/cli/defuddle) | 15(总 44 含 .git/) | 可用 |
| `kimi-webbridge` | Kimi WebBridge 浏览器自动化(官方 SKILL,本地守护进程 + HTTP API,自动分发到 5 个 Runtime) | 2 | 可用 |

| `project-init` | 项目级 Agent 环境初始化(搭建 .agent/ + AGENTS.md + 部署推荐 skill) | 7 | 可用 |
| `development-agent` | 开发型 Agent 工作协议(读上下文 → 最小改动 → 验证) | 1 | 可用 |
| `react-best-practices` | Vercel 官方 React/Next.js 性能优化指南(70 规则,8 类别) | 77 | 可用 |

### 状态定义

| 状态 | 含义 |
|------|------|
| `草稿` | 正在编写,尚未验证 |
| `验证中` | 已完成,正在测试 |
| `可用` | 已验证,可部署 |
| `弃用` | 不再维护,待清理 |

---

## 3. 部署方式

### 3.0 前置:设置知识库根目录

本知识库设计为**可移植**——clone 到任何位置都能用。部署前先设置 `$KB_ROOT` 变量:

```powershell
# 把路径改成你 clone 的实际位置
$KB_ROOT = "D:\your\path\to\agent"

# 验证
Test-Path "$KB_ROOT\01-Skills\AGENTS.md"  # 应输出 True
```

> 后续所有部署命令都用 `$KB_ROOT` 引用,不硬编码路径。换电脑、换目录只需改这一处。

### 3.1 部署决策

AI 根据当前上下文选择部署位置,不用硬分类:

```
技能 SKILL.md 已编写完成
        ↓
  AI 判断当前场景:
  ├─ 个人所有项目都常用?(如知识库初始化)  → 部署到 Personal
  ├─ 只在当前项目用?(如项目特定的部署)    → 部署到 Project
  └─ 跨场景通用+有依赖?(如 superpowers)  → 部署到 Plugin 或 Personal
        ↓
  执行部署
```

AI 判断输入信号:

| 信号 | 部署到 |
|------|--------|
| description 说"所有项目" | Personal / Plugin |
| description 说"特定项目"或绑定技术栈 | Project |
| 完整方法论集(如 superpowers) | Plugin(避免污染全局) |
| 简单工具(无大依赖) | Personal |
| 依赖运行时上下文(如项目目录结构) | Project |

### 3.2 部署到 Claude Code

**Personal(个人全局)**——`~/.claude/skills/`:

```powershell
Copy-Item -Recurse "$KB_ROOT\01-Skills\kb-init" "$env:USERPROFILE\.claude\skills\kb-init"
```

或用软链接(推荐,源改了自动生效):

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\kb-init" -Target "$KB_ROOT\01-Skills\kb-init"
```

**Project(项目级)**——在目标项目根目录执行:

```powershell
Copy-Item -Recurse "$KB_ROOT\01-Skills\superpowers" ".\.claude\skills\superpowers"
```

**Plugin(插件方式)**——适合完整技能集:

```powershell
# 复制到 Claude Code plugin 目录
Copy-Item -Recurse "$KB_ROOT\01-Skills\ui-ux-pro-max" "$env:USERPROFILE\.claude\plugins\ui-ux-pro-max"
```

> Claude Code 自动发现所有三层位置。优先级:Enterprise > Personal(`~/.claude/skills/`) > Project(`.claude/skills/`) > Plugin。

### 3.3 部署到 Codex CLI

**Personal**:

```powershell
Copy-Item -Recurse "$KB_ROOT\01-Skills\kb-init" "$env:USERPROFILE\.codex\skills\kb-init"
```

**Project**:

```powershell
Copy-Item -Recurse "$KB_ROOT\01-Skills\superpowers" ".\.codex\skills\superpowers"
```

> 详见 [Codex 自定义与技能](../00-AgentBase/runtime/04-Codex-CLI/06-自定义与技能.md)。

### 3.4 部署到 Hermes Agent

**Personal**:

```powershell
Copy-Item -Recurse "$KB_ROOT\01-Skills\kb-init" "$env:USERPROFILE\.hermes\skills\kb-init"
```

**Project**:通过 `external_dirs` 配置指向技能目录,或复制到项目内。

> 详见 [Hermes 技能系统](../00-AgentBase/runtime/02-Hermes-Agent/05-技能系统.md)。

### 3.5 部署流程

```
新技能编写完成
  ↓
AI 判断部署位置(Personal/Project/Plugin,见 3.1)
  ↓
按 3.2/3.3/3.4 执行部署
  ↓
更新技能注册表(§ 2)
  ↓
验证:在目标 Runtime 中调用该技能,确认正常工作
```

---

## 4. 拒绝默认垃圾技能

Runtime 安装后会自带一批默认技能/插件。本规范要求:**只使用 `01-Skills/` 中的技能,默认自带的若不需要一律禁用。**

### 4.1 Claude Code

| 操作 | 方法 |
|------|------|
| 禁用所有内置技能 | settings.json: `"disableBundledSkills": true` |
| 禁用特定内置技能 | `permissions.deny` 中加入 `"Skill(技能名)"` |
| 查看 installed skills | `/skills` 或检查 `~/.claude/skills/` |

**推荐配置**(`~/.claude/settings.json`):

```json
{
  "disableBundledSkills": true
}
```

> 禁用后只加载 `~/.claude/skills/` 和 `.claude/skills/` 下的技能——即从 `01-Skills/` 部署的技能。如需个别内置技能(如 `/debug`),用 `permissions.allow` 单独放行。

### 4.2 Codex CLI

通过 `~/.codex/AGENTS.md` 控制加载范围,仅引用 `01-Skills/` 部署的技能。

### 4.3 Hermes Agent

通过配置文件指定 `skills_dir` 为 `~/.hermes/skills/`,只加载手动部署的技能。

### 4.4 清理原则

| 原则 | 说明 |
|------|------|
| **只用 01 的** | 所有技能来自 `01-Skills/`,不接受其他来源 |
| **默认全禁** | 内置技能默认禁用,按需放行 |
| **定期清理** | 检查 Runtime 技能目录,删除非 `01-Skills/` 来源的技能 |
| **Plugin 谨慎** | Plugin 安装的技能会自动加载,非必要不安装第三方 Plugin |

---

## 5. 技能编写规范

### 5.1 标准目录结构

每个技能是一个目录,以 `SKILL.md` 为入口:

```text
my-skill/
├── SKILL.md           # 主指令文件(必需)
├── references/        # 参考资料(可选)
├── templates/         # 模板文件(可选)
├── examples/          # 示例输出(可选)
└── scripts/           # 可执行脚本(可选)
```

### 5.2 SKILL.md 格式

```markdown
---
name: my-skill
description: >
  具体描述技能做什么、何时使用。Claude 用这段话决定是否自动调用。
  Use when... 开头说明触发条件。
version: 1.0.0
---

# my-skill — 一句话标题

## When to Use
- 触发条件列表

## Procedure
1. 步骤一
2. 步骤二

## Pitfalls
- 常见错误

## Verification
- [ ] 验证项
```

### 5.3 编写原则

| 原则 | 说明 |
|------|------|
| **description 写清楚** | Claude 靠这段话判断何时调用,写清"做什么"+"何时用" |
| **正文要具体** | "运行 npm test" 而非"测试你的代码" |
| **不写概念教程** | 概念教程放 `00-AgentBase/behavior/`,这里只放操作手册 |
| **支持文件分离** | 大段参考资料放 `references/`,正文只写核心步骤 |
| **版本管理** | frontmatter 中标注 version,变更时递增 |

### 5.4 新建技能流程

1. 复制 `_template.skill.md` 为新目录下的 `SKILL.md`
2. 放在 `01-Skills/` 下(平铺,不分子目录)
3. 编写 frontmatter 和正文
4. 按需添加 `references/`、`templates/` 等支持文件
5. 在本文件 § 2 技能注册表中登记
6. 更新 `README.md` 的技能清单
7. 由 AI 判断部署位置,执行部署(见 § 3.1)并验证

---

## 6. 外部技能入库

### 6.1 核心原则

收到外部 skill 链接时,把完整内容下载到 `01-Skills/` 下,确保离线可用。

> 禁止只记录安装命令。`/plugin install xxx` 是部署指令,不是技能内容。离线环境无法执行命令。

```
收到链接
  ↓
❌ 只记录安装命令,SKILL.md 里写"/plugin install superpowers@xxx"
  ↓
✅ 下载完整技能内容到本地,整理为标准目录结构,离线可直接使用
```

### 6.2 入库流程

```
① 分析源仓库结构
  访问链接 → 找到 skills/ 目录 → 列出所有技能
  识别:主 SKILL.md、references/、templates/、scripts/、hooks/
         ↓
② 下载全部内容
  逐个下载每个技能的 SKILL.md 和所有支持文件
  保留原始目录结构,不丢文件
         ↓
③ 整理到 01-Skills/
  平铺放入 01-Skills/<skill-name>/(不分子目录)
  保持标准目录结构:skill-name/SKILL.md + references/ 等
         ↓
④ 补充入库信息
  在 SKILL.md frontmatter 中标注来源、版本、协议
  保留原始安装命令作为参考(放在"安装参考"章节,不作为主要使用方式)
         ↓
⑤ 离线验证
  断开网络 → 确认所有文件可访问 → 确认内部链接无死链
  确认技能可被 Runtime 直接加载(不需要联网下载)
         ↓
⑥ 登记
  更新本文件 § 2 技能注册表
  更新 README.md 技能清单
```

### 6.3 目录结构要求

入库后的技能必须包含完整内容,以 superpowers 为例:

```text
01-Skills/superpowers/
├── SKILL.md                          # 入口:技能总览 + 入库信息
├── references/                       # 本技能的参考资料
│   └── installation-per-runtime.md   # 各 runtime 安装方式(参考用)
├── skills/                           # ← 从源仓库下载的完整技能内容
│   ├── brainstorming/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── test-driven-development/
│   ├── systematic-debugging/
│   ├── writing-plans/
│   ├── executing-plans/
│   ├── subagent-driven-development/
│   ├── dispatching-parallel-agents/
│   ├── using-git-worktrees/
│   ├── requesting-code-review/
│   ├── receiving-code-review/
│   ├── finishing-a-development-branch/
│   ├── verification-before-completion/
│   ├── writing-skills/
│   └── using-superpowers/
└── README.md                         # 技能集说明(可选)
```

### 6.4 入库 SKILL.md 模板

入库的技能,其入口 SKILL.md 应包含以下章节:

```markdown
---
name: skill-name
description: >
  原始 description,保留触发场景描述。
version: x.x.x                      # 源仓库版本
source: https://github.com/xxx/xxx   # 源链接
license: MIT                         # 源协议
imported: 2026-07-09                 # 入库日期
---

# skill-name — 一句话标题

## 来源信息
- 仓库:链接
- 版本:x.x.x
- 协议:MIT
- 入库日期:YYYY-MM-DD

## When to Use
(从源 SKILL.md 保留或改写)

## What's Inside
(技能集:列出包含的子技能)

## 离线使用
本技能已完整下载到本地,所有文件在 skills/ 目录下,无需联网即可使用。

## 安装参考
(保留原始安装命令,仅供参考和更新时使用,不作为主要使用方式)

## 相关知识
- [如何编写 Skill](../00-AgentBase/behavior/01-如何编写Skill.md)
- [跨 Runtime 技能管理](../00-AgentBase/behavior/02-跨Runtime技能管理.md)
- [概念全景辨析](../00-AgentBase/02-概念全景辨析.md)
```

### 6.5 禁止行为

| 禁止 | 原因 |
|------|------|
| 只记录 `/plugin install` 命令 | 离线不可用,链接失效即丢失 |
| 只下载入口 SKILL.md,不下载 references/ | 支持文件缺失,技能行为不完整 |
| 改动下载的技能内容(入库时) | 入库是"原样保存",修改在后续维护阶段做 |
| 丢掉源仓库的目录结构 | 破坏技能内部引用,导致死链 |

### 6.5.1 第三方完整仓库的处理铁律

大型第三方 skill 仓库(anthropics / baoyu / kepano / superpowers / ui-ux-pro-max)在本知识库以**完整镜像**形式存在,适用以下铁律:

| 铁律 | 含义 |
|------|------|
| **只读** | `01-Skills/<镜像名>/` 下的源文件禁止手改。需要定制请新建一个独立 skill 包装调用,不要改原镜像 |
| **不修改** | 更新时只走"替换整个目录"流程(§ 6.6),不要增量 patch,避免与源仓库 drift |
| **注释入口** | 镜像根 `SKILL.md` 保留源仓库 SKILL.md 不动,避免混淆"本知识库说明"和"源说明" |
| **规模记录** | 文件数和总大小变化超过 20% 时,在本文件 § 2 技能注册表标注变更日期 |
| **精简镜像备选** | 若完整镜像过大(>200MB),可在 `_archive/skills-mirror/` 留只读副本,主目录只保留入口 SKILL.md |

> 当前未超阈值的镜像:anthropics-skills (13.48MB) / baoyu-skills (50.53MB) / ui-ux-pro-max (7.82MB),均完整保留在主目录。

### 6.6 更新已入库技能

源仓库发布新版本时,按以下流程更新:

```
1. 访问源仓库,确认新版本号和变更内容
2. 下载新版本的完整内容
3. 替换 skills/ 目录下的对应文件
4. 更新入口 SKILL.md 的 version 和 imported 日期
5. 更新本文件 § 2 技能注册表的版本号
6. 由 AI 判断是否需要重新部署到 Runtime
7. 离线验证
```

---

## 7. 更新与同步

### 7.1 修改技能

**只在 `01-Skills/` 中修改**,然后同步到各 Runtime:

```powershell
# 同步 Personal 部署的技能到 Claude Code
Copy-Item -Recurse -Force "$KB_ROOT\01-Skills\kb-init" "$env:USERPROFILE\.claude\skills\kb-init"

# 同步 Project 部署的技能到目标项目
Copy-Item -Recurse -Force "$KB_ROOT\01-Skills\superpowers" ".\.claude\skills\superpowers"
```

> 用软链接部署的无需同步——源改了自动生效。

### 7.2 同步检查

每次修改技能后:

- [ ] 在 `01-Skills/` 中修改完成?
- [ ] 技能注册表已更新(版本号/状态)?
- [ ] AI 已重新判断部署位置,执行同步?
- [ ] 在目标 Runtime 中调用测试通过?

### 7.3 Git 提交规范

```
docs(01): 新增 kb-init 技能              # 新增技能
docs(01): 更新 superpowers 至 v6.0.2    # 更新技能
docs(01): 弃用 old-deploy 技能           # 弃用技能
chore(01): 同步技能到 Claude Code         # 同步部署
```

---

## 8. 防信息孤岛

### 8.1 每个技能必须满足

- **入口 ≥ 1**:被本文件 § 2 技能注册表或 `README.md` 技能清单引用
- **出口 ≥ 1**:`SKILL.md` 末尾有相关知识链接
- **零死链**:所有引用路径指向真实存在的文件

### 8.2 与知识库的关联

每个技能的 `SKILL.md` 应在末尾引用相关的知识库概念:

```markdown
## 相关知识
- [如何编写 Skill](../00-AgentBase/behavior/01-如何编写Skill.md)
- [跨 Runtime 技能管理](../00-AgentBase/behavior/02-跨Runtime技能管理.md)
- [概念全景辨析](../00-AgentBase/02-概念全景辨析.md)
```

---

## 9. 自检清单

每次新增、修改或部署技能前过一遍:

**编写阶段**:
- [ ] 从 `_template.skill.md` 开始?
- [ ] 平铺放在 `01-Skills/` 下(不分子目录)?
- [ ] frontmatter 完整(name/description/version)?
- [ ] 正文具体可执行(非概念教程)?

**登记阶段**:
- [ ] 已在本文件 § 2 技能注册表登记?
- [ ] 已更新 `README.md` 技能清单?
- [ ] 末尾有相关知识链接?

**入库阶段**(外部技能):
- [ ] 完整内容已下载(不只记录安装命令)?
- [ ] 所有支持文件(references/templates/scripts)已下载?
- [ ] 入库 SKILL.md 标注了来源、版本、协议?
- [ ] 离线验证通过(断网可访问所有文件)?
- [ ] 保留了原始安装命令作为参考?

**部署阶段**:
- [ ] AI 已判断部署位置(Personal/Project/Plugin)?
- [ ] 部署到对应 Runtime 目录?
- [ ] 已禁用不需要的 Runtime 默认技能?
- [ ] 在目标 Runtime 中调用验证通过?

**同步阶段**:
- [ ] 源只在 `01-Skills/` 中修改?
- [ ] 已同步到各 Runtime 部署位置?
- [ ] 版本号已更新?

---

> **维护责任人**:Agent Environment Operator
> **最后更新**:2026-07-10
> **文档版本**:v2.1.0(按 agents-md-author 规范精简,移除"为什么"段落,决策理由已移至 99-Roadmap.md)
