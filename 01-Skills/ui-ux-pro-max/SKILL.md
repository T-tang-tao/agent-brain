---
name: ui-ux-pro-max
version: 2.6.2
description: "UI/UX 设计情报库。覆盖 50+ 视觉风格、161 调色板、57 字体搭配、25 图表类型、99 UX 准则、跨 10+ 技术栈(React/Next.js/Vue/Nuxt/Svelte/SwiftUI/React Native/Flutter/Tailwind/shadcn-ui/HTML/CSS/Angular/Laravel/Three.js 等)的可搜索数据库。适用于设计页面/组件、配色排版选型、UI 评审、可访问性检查、跨平台视觉对齐。"
source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
license: MIT
imported: 2026-07-09
imported-from-commit: main (depth=1)
status: 可用
runtime:
  - Claude Code (Plugin 原生)
  - Codex CLI (通过 .codex-plugin/ 适配)
  - Cursor / Windsurf (社区适配)
  - Antigravity (Plugin)
level: project
---

# UI/UX Pro Max - 设计情报

为 Web 与移动应用提供专业的 UI/UX 设计情报。源仓库是一个 Claude Plugin,本知识库已将其完整离线入库(229 个文件)。

## When to Use

**Must Use**(以下场景必须调用本技能):

- 设计新页面(Landing Page / Dashboard / Admin / SaaS / Mobile App)
- 创建或重构 UI 组件(按钮 / 模态框 / 表单 / 表格 / 图表)
- 选定配色方案、字体系统、间距标准、布局系统
- 评审 UI 代码的用户体验、可访问性、视觉一致性
- 实现导航结构、动画、响应式行为
- 制定产品级设计决策(风格、信息层级、品牌表达)
- 提升界面的感知质量、清晰度、易用性

**Recommended**(以下场景建议调用):

- UI 看起来"不够专业"但原因不明确
- 收到关于可用性或体验的反馈
- 发布前的 UI 质量优化
- 跨平台视觉对齐(Web / iOS / Android)
- 构建设计系统或可复用组件库

**Skip**(以下场景不需要):

- 纯后端逻辑开发
- 仅涉及 API 或数据库设计
- 与界面无关的性能优化
- 基础设施 / DevOps 工作
- 非视觉脚本或自动化任务

**判断准则**:如果任务会改变某个功能的**外观、感觉、动效或交互方式**,就应调用本技能。

## 子技能清单

本技能由 7 个子技能构成,根据任务场景按需加载:

| 子技能 | 路径 | 用途 | 调用时机 |
|--------|------|------|----------|
| **ui-ux-pro-max** | `skills/ui-ux-pro-max/` | 核心:50+ 风格 / 161 配色 / 57 字体 / 161 产品类型 / 99 UX 准则 / 25 图表类型数据库,带优先级规则 | 任何 UI/UX 设计决策的**入口**,先调它再选子技能 |
| **design** | `skills/design/` | logo / icon / banner / CIP(自定义图像生成)等专项设计 | 设计 logo、图标、Banner、海报、社交媒体图 |
| **design-system** | `skills/design-system/` | Design Token / Slide Tokens / 组件规范 | 构建或维护设计系统、生成 token JSON |
| **ui-styling** | `skills/ui-styling/` | Tailwind / shadcn-ui 配置与组件,含 54 个字体文件 | 写 Tailwind 类、调 shadcn 主题、配置响应式 |
| **banner-design** | `skills/banner-design/` | Banner 尺寸与风格规范 | 设计广告 Banner、社交封面 |
| **brand** | `skills/brand/` | 品牌资产组织 / 色彩管理 / Logo 使用 / 视觉识别 | 制定或维护品牌指南、商标规范 |
| **slides** | `skills/slides/` | 演示文稿排版、文案公式、HTML 模板 | 制作 PPT/PDF/HTML 演示文稿 |

## Procedure

### 步骤 1:识别任务类型

根据 When to Use 判断是否需要本技能。如果需要,进入步骤 2。

### 步骤 2:阅读核心入口

打开 `skills/ui-ux-pro-max/SKILL.md`,理解:
- 10 条优先级规则(可访问性 → 触摸交互 → 性能 → 风格 → 布局 → 排版 → 动画 → 表单 → 导航 → 图表)
- 快速参考表(每条规则的关键词)
- 反模式(避免的错误)

### 步骤 3:按需加载子技能

根据具体任务,从子技能清单选择对应子技能,**先读其 SKILL.md 再读 references/**:

- 配色/风格/排版 → `ui-ux-pro-max` 的 `data/` CSV 数据库(可用 Python 脚本搜索)
- 设计系统 token → `design-system` 的 `scripts/`
- Tailwind/shadcn 组件 → `ui-styling` 的 `references/` + 字体文件
- logo/icon/banner → `design` 的 `scripts/` + `references/`
- 品牌指南 → `brand` 的 `templates/` + `references/`
- 演示文稿 → `slides` 的 `references/` + `design-system` 的 slide 数据

### 步骤 4:执行设计决策

按优先级 1→10 顺序应用规则,优先解决 CRITICAL 类问题(可访问性、触摸交互)。

### 步骤 5:验证输出

按 Verification 清单逐项验证。

## Pitfalls

- ❌ **跳过核心入口直接用子技能**:`ui-ux-pro-max/SKILL.md` 的 10 条优先级规则是其他子技能的总纲,先读它
- ❌ **混搭风格**:不要把 flat design 和 skeuomorphic 混用;风格必须一致
- ❌ **用 emoji 当图标**:必须用 SVG icon(图标库见 `ui-ux-pro-max/data/icons.csv`)
- ❌ **固定 px 容器宽度**:响应式断点必须 mobile-first
- ❌ **< 12px 正文字号**:最小 16px(参考 `ui-ux-pro-max` typography rules)
- ❌ **仅靠 hover 交互**:移动端没有 hover,必须有 tap 替代
- ❌ **依赖色彩传达信息**:必须配合 icon/文字(色盲用户友好)
- ❌ **禁用缩放**:viewport meta 不能 `user-scalable=no`
- ❌ **忽视 reduced-motion**:必须尊重 `prefers-reduced-motion`
- ❌ **跨运行时只复制子技能**:整个仓库是耦合的整体,必须作为整体入库
- ❌ **只看 SKILL.md 不读 references/**:references/ 包含具体规则和反模式,跳过会丢质量

## Verification

部署到任何 Runtime 前验证:

- [ ] 229 个文件完整,无遗漏
- [ ] 54 个字体文件(TTF + OFL 许可)在 `skills/ui-styling/canvas-fonts/`
- [ ] 所有 CSV 数据文件(`ui-ux-pro-max/data/`)可被 Python 脚本读取
- [ ] `plugin.json` 元数据保留(version / author / keywords)
- [ ] LICENSE(MIT)保留
- [ ] 7 个子技能的 SKILL.md 全部存在
- [ ] 所有 `references/*.md` 全部存在

部署后验证(在 Agent Runtime 中):

- [ ] Agent 能识别并调用 `ui-ux-pro-max` 技能
- [ ] Agent 能根据场景加载对应子技能
- [ ] Agent 能读 CSV 数据并给出符合优先级规则的设计建议
- [ ] 字体文件能被 design-system 脚本引用

## 安装参考

源仓库是 Claude Plugin,各 Runtime 适配方式见 [`references/installation-per-runtime.md`](./references/installation-per-runtime.md)。

## 来源信息

- **源仓库**: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **官方主页**: https://uupm.cc
- **版本**: v2.6.2
- **作者**: nextlevelbuilder
- **许可证**: MIT(保留在 `LICENSE`)
- **导入时间**: 2026-07-09
- **导入方式**: `git clone --depth 1` → 完整复制 `skills/` 目录(229 文件)→ 归档 `plugin.json` + 原始 `README` + `LICENSE` + `CLAUDE.md`

## 离线使用

✅ **完全离线可用**——所有 229 个文件已完整下载到本目录:

- `skills/` 目录:7 个子技能的所有 SKILL.md / references / scripts / data / 字体文件
- `plugin.json`:Claude Plugin 元数据(版本、作者、关键字)
- `README.source.md` / `README.source.zh.md`:源仓库原始 README(中英)
- `LICENSE`:MIT 许可证原文
- `CLAUDE.source.md`:源仓库的 CLAUDE.md(给 Claude 看的项目指令)

无需联网,直接读本地文件即可使用本技能。


## 已知问题(仓库上游)

源仓库 skills/slides/references/ 与 skills/design/references/slides-* 存在 5 个字节完全相同的重复文件(2026-07-10 校验):

- copywriting-formulas.md = slides-copywriting-formulas.md(2.6 KB)
- html-template.md = slides-html-template.md(9.1 KB)
- layout-patterns.md = slides-layout-patterns.md(3.7 KB)
- slide-strategies.md = slides-strategies.md(2.7 KB)
- create.md = slides-create.md(157 B)

按知识库 §6.5.1「完整长像不修改」铁律,**不在此处删除**;入口请统一读 skills/slides/references/(slides 模块的原始位置),design/references/slides-* 是历史遗留。修复需上游合并。
## 完整目录结构

```
$KB_ROOT/01-Skills/ui-ux-pro-max/
├── SKILL.md (本文件 - 入口)
├── plugin.json (Claude Plugin 元数据)
├── LICENSE (MIT)
├── README.source.md (英文原文)
├── README.source.zh.md (中文原文)
├── CLAUDE.source.md (源仓库 CLAUDE.md)
├── references/
│   └── installation-per-runtime.md (跨 Runtime 部署指南)
└── skills/
    ├── ui-ux-pro-max/ (核心入口)
    │   ├── SKILL.md
    │   ├── data/ (17 个 CSV + 16 栈数据)
    │   └── scripts/ (3 个 Python)
    ├── design/ (logo/icon/banner)
    │   ├── SKILL.md
    │   ├── data/ (CIP/icon/logo CSV)
    │   ├── references/ (18 篇)
    │   └── scripts/ (8 个)
    ├── design-system/ (Design Token)
    │   ├── SKILL.md
    │   ├── data/ (8 个 slide CSV)
    │   ├── references/ (7 篇)
    │   ├── scripts/ (10 个)
    │   └── templates/
    ├── ui-styling/ (Tailwind/shadcn-ui)
    │   ├── SKILL.md
    │   ├── canvas-fonts/ (54 个字体 .ttf + .oft.txt)
    │   ├── references/ (7 篇)
    │   └── scripts/ (2 个 Python)
    ├── banner-design/
    │   ├── SKILL.md
    │   └── references/
    ├── brand/ (品牌)
    │   ├── SKILL.md
    │   ├── references/ (10 篇)
    │   ├── scripts/ (5 个)
    │   └── templates/
    └── slides/ (演示文稿)
        ├── SKILL.md
        └── references/ (5 篇)
```
