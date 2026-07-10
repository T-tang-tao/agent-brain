# Agent Wiki Roadmap

> 这个文件记录 `agent/` 目录的建设路线、决策日志和敏感操作审计。

---

## 当前进度概览(2026-07-09)

| 阶段 | 状态 | 完成度 |
|------|------|--------|
| 第一阶段:AgentBase 基础知识 | ✅ 完成 | 100% |
| 第二阶段:Skills 资产 | ✅ 完成 | 100% |
| 第三阶段:Prompts 资产 | ✅ 完成 | 100% |
| 第四阶段:MCP + Plugins | ✅ 完成 | 100% |
| 第五阶段:Boundaries 边界规则 | ✅ 完成 | 100% |
| 第六阶段:Migration Playbook | 🟡 进行中 | 14%(1/7) |
| 第七阶段:真实部署验证 | ⏸ 未开始 | 0% |

---

## 第一阶段:AgentBase 基础知识 ✅

**目标**:让新手知道 Agent 是什么,理解核心概念间关系。

**产出**:

- ✅ `00-AgentBase/` 完整初版(80+ 篇文档)
- ✅ `00-human/` 给人类看的入门(5 篇)
- ✅ `behavior/` 行为类知识(6 篇:Skill 编写、跨 Runtime、规划循环、记忆、评估、可观测性)
- ✅ `deployment/` `knowledge/` `model/` `runtime/` `safety/` `tools/` 各模块 README
- ✅ `runtime/` 详细:Claude Code 12 篇、Codex 7 篇、Hermes 11 篇
- ✅ 各资产区 README

---

## 第二阶段:Skills 资产 ✅

**目标**:整理可直接使用或迁移的 skill。

**已收录**:

- ✅ `01-Skills/kb-init/` — 知识库初始化(4 文件)
- ✅ `01-Skills/superpowers/` — 跨 Runtime 开发方法论(58 文件)
- ✅ `01-Skills/ui-ux-pro-max/` — UI/UX 设计情报(229 文件)
- ✅ `01-Skills/anthropics-skills/` — Anthropic 官方(444 文件:13 子技能,含 docx/pdf/pptx/xlsx 4 个生产级文档技能 + skill-creator 元技能 + canvas-design + mcp-builder 等)
- ✅ `01-Skills/baoyu-skills/` — 宝玉中文内容创作(949 文件:20+ 子技能,小红书/信息图/公众号/AI 生图 11 后端)
- ✅ `01-Skills/kepano-obsidian-skills/` — Obsidian 官方维护者(43 文件:5 子技能,markdown/bases/canvas/cli/defuddle)

**未收录(候选)**:

- ⏸ `affaan-m/everything-claude-code` — Anthropic 黑客松冠军,25k+ stars,企业级套件
- ⏸ `vercel-labs/agent-skills` — Vercel 官方,Web 开发向
- ✅ `muratcankoylan/Agent-Skills-for-Context-Engineering` — **已提炼入库**(2026-07-10):16 子技能 → `00-AgentBase/behavior/09-15` 9 篇新章节,`01-Skills/context-engineering/` 已删除,内容沉淀为知识
- ⏸ 自建 "中文检索 skill"(基于 jieba + pinyin)

---

## 第三阶段:Prompts 资产 ✅

**目标**:整理可直接复制、迁移、改造的 agent prompt。

**已收录**:

- ✅ `03-Prompts/claude-code-agent-prompt.md` — Claude Code 主系统 prompt
- ✅ `03-Prompts/hermes-agent-prompt.md` — Hermes Agent 系统 prompt
- ✅ `03-Prompts/boundary-aware-agent-prompt.md` — 边界敏感任务叠加 prompt
- ✅ `03-Prompts/_agent-prompt-template.md` — 新 prompt 模板

**未收录(候选)**:

- ⏸ Codex agent prompt
- ⏸ Migration agent prompt(辅助用户跨 Runtime 迁移)
- ⏸ Knowledge-base-auditor prompt(审查知识库死链/孤岛)

---

## 第四阶段:MCP 与 Plugins ✅

**目标**:整理可落地的 MCP 配置、plugin 资产。

**已收录 MCP Server**:

- ✅ `04-MCP/filesystem-mcp.md` — 通用文件读写 MCP
- ✅ `04-MCP/obsidian-mcp.md` — Obsidian vault MCP

**已收录 Plugin Adapter**(02-Plugins/):

- ✅ `02-Plugins/ui-ux-pro-max/` — Claude Code Plugin,引用 `01-Skills/ui-ux-pro-max/`
- ✅ `02-Plugins/superpowers/` — Claude Code Plugin,引用 `01-Skills/superpowers/`
- ✅ `02-Plugins/kb-init/` — 全局 Skills 部署说明

**未收录(候选)**:

- ⏸ `04-MCP/trading-data-mcp.md` — 交易数据 MCP(配合 trading-risk-boundary)
- ⏸ `04-MCP/github-mcp.md` — GitHub 操作 MCP
- ⏸ Codex / Cursor plugin 适配器

---

## 第五阶段:Boundaries 边界规则 ✅

**目标**:整理可直接给 agent 读取并执行的边界规则。

**已收录策略**:

- ✅ `05-Boundaries/file-edit-policy.md` — 文件编辑边界(HIGH)
- ✅ `05-Boundaries/shell-command-policy.md` — 命令执行边界(HIGH)
- ✅ `05-Boundaries/external-api-policy.md` — 外部 API 边界(HIGH)
- ✅ `05-Boundaries/memory-write-policy.md` — 记忆写入边界(HIGH)
- ✅ `05-Boundaries/destructive-action-policy.md` — 破坏性操作(CRITICAL)
- ✅ `05-Boundaries/trading-risk-boundary.md` — 交易资金操作(CRITICAL)
- ✅ `05-Boundaries/_boundary-policy-template.md` — 策略模板

---

## 第六阶段:Migration Playbook 🟡

**目标**:整理跨 Runtime 迁移流程。

**已收录**:

- ✅ `06-Migration/claude-code-to-hermes.md` — Claude Code → Hermes

**未收录(候选)**:

- ⏸ Codex → Claude Code
- ⏸ Hermes → Claude Code
- ⏸ Skill migration checklist(单 skill 跨 runtime)
- ⏸ Prompt migration checklist(单 prompt 跨 runtime)
- ⏸ MCP migration checklist(单 mcp 跨 runtime)
- ⏸ Knowledge base migration checklist(整个 kb 跨机器)

---

## 第七阶段:真实部署验证 ⏸

**目标**:把上面 6 个阶段的资产真的装到一个 Runtime 里跑通。

**待办**:

- ⏸ 安装 Claude Code(参考 `00-AgentBase/runtime/03-ClaudeCode/02-安装部署.md`)
- ⏸ 部署 kb-init 到全局 skills
- ⏸ 部署 ui-ux-pro-max 作为 plugin
- ⏸ 配置 filesystem MCP + obsidian MCP
- ⏸ 配置 CLAUDE.md(用 `03-Prompts/claude-code-agent-prompt.md`)
- ⏸ 跑通最小任务:说"初始化知识库",验证 kb-init 触发
- ⏸ 跑通边界测试:触发 deny 的命令,验证拦截
- ⏸ 性能基线:上下文占用 / 响应延迟

---

## 决策日志

### 2026-07-09 — 知识库架构建立

- **决策**:采用 00 认知层 + 01-06 实践层 双层架构
- **理由**:概念清晰,实践资产统一管理
- **影响**:所有未来内容必须按这个分层放置

### 2026-07-09 — `ui-ux-pro-max` 从全局改为项目级

- **决策**:把 `01-Skills/ui-ux-pro-max/` 移到 `01-Skills/ui-ux-pro-max/`
- **理由**:UI/UX 是开发场景专用,知识库管理/交易策略/文档写作项目不需要
- **影响**:所有引用文件路径更新(AGENTS.md、README.md、SKILL.md、installation-per-runtime.md)

### 2026-07-09 — 引入 `$KB_ROOT` 路径变量

- **决策**:所有文档路径用 `${KB_ROOT}` 而非 `D:\valut\trade\agent` 硬编码
- **理由**:可移植到 Gitee / 其他机器 / 其他盘符
- **影响**:用户首次使用需在 System Prompt 中绑定变量值

### 2026-07-09 — Plugin 适配器 vs Skill 复制

- **决策**:`02-Plugins/` 只放 plugin adapter(引用 01-Skills),不复制内容
- **理由**:单一来源原则,避免同步问题
- **影响**:Claude Code plugin.json 通过相对路径指向 01-Skills/

### 2026-07-09 — `00-AgentBase` 改名为 `00-KnowledgeBase`(待执行)

- **决策**:把认知层目录从 `00-AgentBase/` 改名为 `00-KnowledgeBase/`
- **理由**:`AgentBase` 字面意思是"Agent 基础",但本目录是完整知识库(概念+运行时+工具+安全+行为),命名误导
- **阻碍**:Obsidian 持有目录句柄,无法在 Obsidian 运行中 rename
- **临时方案**:在 `00-AgentBase/README-rename-notice.md` 留重命名步骤
- **执行时机**:明日首次打开 vault 前(Obsidian 关闭后)
- **影响**:涉及 80+ markdown 的引用 + 标题中的 "AgentBase" 字样,需要批量替换

### 2026-07-09 — 入库 anthropics-skills / baoyu-skills / kepano-obsidian-skills

- **决策**:把三个开源技能集拉入 `01-Skills/`(平铺,不分子目录)
- **理由**:响应小红书笔记"十大必装 skill"清单,优先装官方和中文向
- **来源**:
  - `anthropics/skills` — Anthropic 官方 444 文件(13 子技能,含 docx/pdf/pptx/xlsx 4 个生产级文档技能)
  - `JimLiu/baoyu-skills` — 宝玉中文 949 文件(20+ 子技能,小红书/公众号/AI 生图 11 后端)
  - `kepano/obsidian-skills` — Obsidian 维护者 43 文件(5 子技能)
- **影响**:01-Skills 文件总数从 ~290 增至 1727(增加 1437 文件),新增 3 个 SKILL.md 入口
- **修正**:发现 AGENTS.md 现行设计是"平铺不分 global/projects/",新加的三个最初误放在 `projects/` 子目录,已修正回平铺。同时把 `kb-init/superpowers/ui-ux-pro-max` 也都从 `projects/` 移到平铺,删除空 `projects/` 目录

### 2026-07-09 — 新建 agents-md-author Skill + 知识库规范

- **问题**:用户反馈"Agent 写 AGENTS.md 时会生成多余内容,比如不需解释为什么却要解释"
- **决策**:建立"知识库规范 + 强制 Skill"双层机制
  - 知识库: `00-AgentBase/knowledge/04-如何编写AGENTS.md`(沉淀怎么写)
  - 强制 Skill: `01-Skills/agents-md-author/SKILL.md`(触发后强制遵循)
  - System Prompt 加规则: 03-Prompts/claude-code-agent-prompt.md §11
- **原则**:知识库 = 教材(Agent 主动读),Skill = 操作手册(Runtime 强制加载)
- **触发词**: "改 AGENTS.md / 优化 AGENTS / 别解释为什么 / 直接执行" 等
- **预期效果**: 以后改 AGENTS.md,Agent 自动不写"为什么"段落,决策理由自动推到 99-Roadmap.md

### 2026-07-10 — 应用 agents-md-author 规范改写所有 AGENTS.md

- **执行**: 按 Skill 规范改 3 个 AGENTS.md
  - `01-Skills/AGENTS.md` v2.0.0 → v2.1.0: 删"为什么不再分 global/projects"段落(改放决策日志引用 99-Roadmap.md),§ 3.1 改祈使句,§ 6.1 改祈使句
  - `00-AgentBase/AGENTS.md` v3.1.0 → v3.2.0: § 0 视角列表改表格,删除"RAG = 外卖员,LLM Wiki = 农场主"冗余类比,§ 7 编译原则改表格
  - 根 `AGENTS.md` v4.0.0: 无需修改(已是最新较优结构)
- **验证**: 三个文件均通过 agents-md-author 检查清单
  - 0 个"为什么"段落
  - 0 处模糊词
  - 都有边界规则符号

### 2026-07-10 — 入库 Loop Engineering 范式

- **决策**: 把 Loop Engineering 沉淀为知识库 + Skill 双层资产
- **来源**: Addy Osmani 2026-06-07 长文(github chrome 前工程负责人),Boris Cherny / Peter Steinberger 同期讨论
- **知识库**:
  - 新建 `00-AgentBase/knowledge/00-工程范式总览.md`(原 paradigm/00)
  - `00-工程范式总览.md`(L1 Prompt → L2 Context → L3 Harness → L4 Loop 四层关系)
  - `04-Loop-Engineering.md`(定义 + 起源 + 五要素 + 三大核心 + 三大陷阱 + 与本知识库资产对应)
- **Skill**:
  - `01-Skills/loop-engineering/`(强制 Skill,触发后读 references/)
  - SKILL.md 精简 80 行(触发词 + 5 强制规则 + 5 步 Procedure + Verification)
  - references/: five-elements.md(5 要素详解) + three-pitfalls.md(3 陷阱详解) + template.md(3 模板版本)
- **与本知识库资产对应**:
  - Automations → 根 AGENTS.md § 6.2 生命周期管理
  - Skills → 01-Skills/(1730 文件)
  - Plugins/Connectors → 02-Plugins/ + 04-MCP/
  - Sub-agents → 根 AGENTS.md § 4 编排
  - State → 99-Roadmap.md + AGENTS.md
  - **Worktrees 是知识库短板,可作为下一阶段补强**

---

## 敏感操作审计

> 涉及破坏性 / 不可逆 / 影响外部的操作必须在这里追加。

### 2026-07-09 — 移除硬编码路径

- **动作类型**:批量 SearchReplace(8+ 处)
- **影响范围**:01-Skills/AGENTS.md、README.md、SKILL.md
- **可回滚**:`git revert`(如果已 commit)
- **已验证**:文件路径变量替换无残留

### 2026-07-09 — 移动 ui-ux-pro-max 目录

- **动作类型**:Move-Item(目录级)
- **影响范围**:`01-Skills/` 目录结构
- **可回滚**:`Move-Item` 反向操作
- **已验证**:222 文件完整保留

### 2026-07-09 — 添加 5 个空目录的实际资产

- **动作类型**:新增 11 个文件(3 prompts + 3 plugins + 2 mcp + 6 boundaries + 1 migration)
- **影响范围**:02-Plugins/、03-Prompts/、04-MCP/、05-Boundaries/、06-Migration/
- **可回滚**:`git revert` 或单文件删除
- **已验证**:每个新文件内容自洽,引用路径有效

### 2026-07-09 — 计划:目录重命名(未执行)

- **动作类型**:目录结构变更(rename)
- **目标**:`00-AgentBase/` → `00-KnowledgeBase/`
- **状态**:⏸ 待执行,Obsidian 锁定
- **可回滚**:rename 反向操作 + 文档里批量反向替换
- **已记录**:`00-AgentBase/README-rename-notice.md` 含完整步骤

---

## 维护原则

- **概念解释**放在 `00-AgentBase/`
- **可复用资产**放在 `01-06/`
- **新增资产时**回链到对应基础知识文件
- **新增基础知识时**更新 `00-AgentBase/00-目录索引.md` 和 `03-知识地图.md`
- **敏感操作**追加到本文件"敏感操作审计"段
- **重大决策**追加到本文件"决策日志"段


### 2026-07-10 — context-engineering 从 skill 提炼到知识库

- **决策**:把  1-Skills/context-engineering/(58 文件 / 888.8 KB / 16 子技能)从技能形态重构为知识库形态
- **理由**:
  - 16 子技能内容是**参考性认知**,不是操作型 procedure。放 01-Skills 会让 skill 集合越来越大,但触发的场景很窄
  - 应作为**可被检索的知识**,归入  0-AgentBase/behavior/
  - 用户的明确指示:"不应该作为技能,应该作为知识库,然后根据提炼的内容对现在的资产以及其他技能进行优化"
- **执行**:
  - 7 新章节: 9-Context-Engineering / 10-Filesystem-Context / 11-Multi-Agent-Patterns / 12-Tool-Design / 13-Harness-Engineering / 14-LLM-Project-Development / 15-Hosted-Agents
  - 2 重写: 4-记忆机制(Memory) v2.0.0 /  5-评估方法(Evaluation) v2.0.0
  - 2 扩充: 6-可观测性(Observability) 加 "Context 健康度信号" /  8-Agent架构模式 加多 Agent 模式 + BDI + 拆分决策
  - 索引更新: 0-AgentBase/behavior/README.md /  3-知识地图.md /  0-目录索引.md
  - 关联 Skill 优化: 1-Skills/loop-engineering/ v2.0.0(加 surface 分类 + 关键约束放首尾) /  1-Skills/agents-md-author/ v2.0.0(加关键约束放最前 + 引用 09/13)
- **删除**: 1-Skills/context-engineering/ 整目录(58 文件)
- **保留备份**:.uploads/context-engineering-source-backup.md(原 _source.md 信息)
- **影响**:
  - 01-Skills 总文件数从 1730 减至 1672
  - 00-AgentBase/behavior 从 6 篇扩至 14 篇
  - 知识库"Agent 认知"完整度显著提升
- **验证**:
  - 0 个 context-engineering 残留(01-Skills/AGENTS.md、01-Skills/README.md 已清)
  - 16 个原始子技能的关键概念全部映射到新章节
  - loop-engineering 和 agents-md-author 仍指向 00-AgentBase/behavior/ 中的新章节

---

## 敏感操作审计(续)

### 2026-07-10 — 批量改写 9 个知识库章节(behavior/)

- **动作类型**:新建 7 篇 + 重写 2 篇 + 追加 2 篇
- **影响范围**: 0-AgentBase/behavior/(14 篇文档)
- **来源**:muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0
- **可回滚**:.uploads/_behavior_current.md(原 behavior/ 内容快照)+ 16 子技能原文件(.uploads/_ctx_skills_raw.md / .uploads/_ctx_split/)
- **已验证**:每个新章节有 frontmatter(状态/版本/来源)、有"一句话理解"、有"工程化检查清单"、有"相关知识"双向链接

### 2026-07-10 — 升级 2 个 Skill 到 v2.0.0

- **动作类型**:覆盖写 SKILL.md
- **影响范围**: 1-Skills/loop-engineering/SKILL.md /  1-Skills/agents-md-author/SKILL.md
- **核心改动**:
  - loop-engineering:加 surface 分类(7 要素 + 1 状态)、关键约束放首尾、按需加载 references/、总长 < 200 行约束
  - agents-md-author:加 "AGENTS.md 是 context 的扩展"、9 条规则(原 7 + 2 新增)、引用 09-Context-Engineering § 3
- **可回滚**:.uploads/_ctx_skills_raw.md 保留原始思路;用户可手动 diff 还原
- **已验证**:两个 skill description 包含新关键词,trigger 词覆盖未变化

### 2026-07-10 — 删除 01-Skills/context-engineering/ 目录

- **动作类型**:Remove-Item -Recurse -Force(目录级,58 文件)
- **影响范围**: 1-Skills/ 目录结构 + 注册表
- **可回滚**:.uploads/context-engineering-source-backup.md(原 _source.md);16 子技能原文保留在 .uploads/_ctx_skills_raw.md 和 .uploads/_ctx_split/
- **已验证**:
  - 删除前目录 58 文件 / 910,083 字节(888.8 KB)
  - 删除后 Test-Path D:\valut\agent\01-Skills\context-engineering 返回 False
  - 01-Skills/AGENTS.md、01-Skills/README.md 注册表行已移除(0 残留)
  - encoding(LF + 无 BOM)保持


### 2026-07-10 — 链接格式硬规则([](path) 唯一允许)

- **决策**:知识库所有跨文档引用统一使用标准 markdown 链接 ` [显示文字](相对路径.md) `,**禁止**以下三种格式
- **背景**:根目录 README.md 大量使用 [path](裸括号无 URL)或 [[path]](Obsidian wikilink),在普通 markdown 渲染器中无法点击,违反"链接要有用"的基本要求
- **禁止格式**:
  - [[path]] Obsidian wikilink — 双层括号,纯 Obsidian 生态,其它渲染器(GitHub、VSCode、Cmd)不识别
  - [path] 裸括号 — 单层括号无 URL,渲染为普通文本不可点击
  - D:\valut\agent\... 绝对路径 — 换机器即失效
- **推荐格式**:
  - 显示文字 = 文件名(如  3-知识地图),不重复路径前缀
  - URL = 相对当前文件的相对路径(如  0-AgentBase/03-知识地图.md)
  - 完整样例:`[03-知识地图](00-AgentBase/03-知识地图.md)`
- **执行**:
  - 根 README.md:17 个链接全部转成标准格式
  -  0-AgentBase/AGENTS.md § 3.1 加第 7 条核心原则
  -  1-Skills/agents-md-author/SKILL.md v2.0.0 → v2.1.0,规则 6 加链接格式硬规则
- **影响**:所有未来入库文档自动遵循;Obsidian 仍可渲染(标准 markdown 链接兼容)

---

## 敏感操作审计(续)

### 2026-07-10 — 根 README.md 全量链接格式修正

- **动作类型**:SearchReplace(17 处)
- **影响范围**:D:\valut\agent\README.md(8 项阅读顺序 + 2 项 Agent 说明 + 7 项快速开始)
- **原格式**:[00-AgentBase/03-知识地图](裸括号)或 [[path]](wikilink)
- **新格式**:`[03-知识地图](00-AgentBase/03-知识地图.md)`(标准 markdown,显示文字 = 文件名,URL = 相对路径)
- **可回滚**:git revert(本任务未用 git,需手动重写)
- **已验证**:0 个 [text] 残留,17 个有效 [text](url) 链接,无 BOM / LF only