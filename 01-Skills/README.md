# Skills — 个人技能库

> 本目录是所有技能的**唯一规范源**(Canonical Source)。修改只在这里改,然后部署到各 Runtime。

## 目录结构

```text
01-Skills/
├── AGENTS.md              ← 管理规范(部署方式、AI 判断流程、更新流程)
├── README.md              ← 本文件
├── _template.skill.md     ← 新技能模板
│
├── kb-init/               ← 从零初始化知识库
├── agents-md-author/      ← AGENTS.md 编写规范(强制 Skill)
├── loop-engineering/      ← Agent Loop 设计(强制 Skill)
├── superpowers/           ← 跨 Runtime 开发方法论(14 子技能)
├── ui-ux-pro-max/         ← UI/UX 设计情报(7 子技能,229 文件)
├── anthropics-skills/     ← Anthropic 官方(17 子技能,445 文件)
├── baoyu-skills/          ← 宝玉中文内容创作(21 子技能,950 文件)
└── kepano-obsidian-skills/← Obsidian 官方维护者(5 子技能,15 内容+29 git)
```

**技能平铺存放**,不分子目录。**部署位置由 AI 判断**(详见 [AGENTS.md §3.1](./AGENTS.md#31-部署决策由-ai-判断)):

| 部署位置 | 适用场景 |
|----------|----------|
| **Personal**(个人全局) | 个人所有项目都常用的技能(如 kb-init) |
| **Project**(项目级) | 只在当前项目使用的技能 |
| **Plugin**(插件) | 完整技能集,避免污染全局(如 ui-ux-pro-max) |

## 已有技能

| 技能 | 用途 | 文件数 | 入口 |
|------|------|--------|------|
| kb-init | 从零初始化专业个人知识库,头脑风暴定制目录结构和 AGENTS.md | 4 | [kb-init/SKILL.md](./kb-init/SKILL.md) |
| agents-md-author | 编写 / 修改 AGENTS.md 时强制遵循简洁规范(不解释原因、直接执行) | 4 | [agents-md-author/SKILL.md](./agents-md-author/SKILL.md) |
| loop-engineering | 设计 Agent Loop(自动化循环系统),含五要素 + 三陷阱 + 模板 | 5 | [loop-engineering/SKILL.md](./loop-engineering/SKILL.md) |
| superpowers | 跨 Runtime 开发方法论技能集(TDD、调试、代码审查、子代理协作等 14 个技能) | 58 | [superpowers/SKILL.md](./superpowers/SKILL.md) |
| ui-ux-pro-max | UI/UX 设计情报(7 个子技能:核心入口/logo-icon/banner/品牌/设计系统/Tailwind-shadcn/演示文稿) | 229 | [ui-ux-pro-max/SKILL.md](./ui-ux-pro-max/SKILL.md) |
| anthropics-skills | Anthropic 官方 Skills(17 子技能:skill-creator 元技能 + docx/pdf/pptx/xlsx 文档技能 + canvas-design + mcp-builder + claude-api + theme-factory/web-artifacts-builder/webapp-testing 等) | 445 | [anthropics-skills/SKILL.md](./anthropics-skills/SKILL.md) |
| baoyu-skills | 宝玉中文内容创作(21 子技能:小红书图文/信息图/漫画/公众号发布/AI 生图 11 后端 + translate/youtube-transcript) | 950 | [baoyu-skills/SKILL.md](./baoyu-skills/SKILL.md) |
| kepano-obsidian-skills | Obsidian 官方维护者 kepano(5 子技能:markdown/bases/canvas/cli/defuddle) | 15(总 44 含 .git/) | [kepano-obsidian-skills/SKILL.md](./kepano-obsidian-skills/SKILL.md) |
| kimi-webbridge | Kimi WebBridge 浏览器自动化(官方版,本地守护进程 + HTTP API;官方已自动分发到 5 个 Runtime) | 2 | [kimi-webbridge/SKILL.md](./kimi-webbridge/SKILL.md) |
| project-init | 项目级 Agent 环境初始化(搭建 .agent/ + AGENTS.md + 部署推荐 skill) | 7 | [project-init/SKILL.md](./project-init/SKILL.md) |
| development-agent | 开发型 Agent 工作协议(读上下文 → 最小改动 → 验证) | 1 | [development-agent/SKILL.md](./development-agent/SKILL.md) |
| react-best-practices | Vercel 官方 React/Next.js 性能优化指南(70 规则,8 类别) | 77 | [react-best-practices/SKILL.md](./react-best-practices/SKILL.md) |

## 不放什么

- 不写 Skill 的概念教程 → 去 `00-AgentBase/behavior/`
- 不放 Runtime 自带的默认技能 → 一律禁用,只用 `01-Skills/` 的
- 不放概念辨析 → 去 `00-AgentBase/02-概念全景辨析.md`

## 新建技能

1. 复制 [_template.skill.md](_template.skill.md) 为新目录下的 `SKILL.md`
2. 平铺放在 `01-Skills/<skill-name>/`(不分子目录)
3. 编写 frontmatter 和正文
4. 在 [AGENTS.md](./AGENTS.md) § 2 技能注册表登记
5. 由 AI 判断部署位置(详见 AGENTS.md §3.1),执行部署并验证

## 相关文件

- [技能管理规范](./AGENTS.md) — 部署方式、AI 判断流程、更新流程
- [如何编写 Skill](../00-AgentBase/behavior/01-如何编写Skill.md) — 概念教程
- [跨 Runtime 技能管理](../00-AgentBase/behavior/02-跨Runtime技能管理.md) — 跨 Runtime 部署策略
- [概念全景辨析](../00-AgentBase/02-概念全景辨析.md) — Tool / Skill / Plugin 概念辨析
- [根目录 AGENTS.md](../AGENTS.md) — 部署、编排与管理总指南
