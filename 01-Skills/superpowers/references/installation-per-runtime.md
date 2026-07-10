# Superpowers 各 Runtime 安装详情

> 本文件供 superpowers 技能参考,详细说明每个 runtime 的安装方式、全局/项目级区别、更新方法。

## 核心架构:Canonical Source + Runtime Adapters

Superpowers 的仓库结构本身就是跨 runtime 适配的范本:

```
superpowers/
├── skills/                    # 规范源:所有 SKILL.md(13 个技能)
│   ├── brainstorming/SKILL.md
│   ├── test-driven-development/SKILL.md
│   ├── systematic-debugging/SKILL.md
│   ├── ...
├── .claude-plugin/            # Claude Code 适配层
│   └── plugin.json            # 插件清单
├── .codex-plugin/             # Codex 适配层
├── .cursor-plugin/            # Cursor 适配层
├── .kimi-plugin/              # Kimi 适配层
├── .opencode/                 # OpenCode 适配层
├── .pi/extensions/            # Pi 适配层
├── hooks/                     # 会话启动钩子(跨 runtime)
├── scripts/                   # 同步/构建脚本
├── CLAUDE.md                  # Claude Code 指令文件
├── AGENTS.md                  # 通用 Agent 指令文件
└── GEMINI.md                  # Gemini 指令文件(已停止支持)
```

关键设计:**技能源只有一份**(`skills/`),各 runtime 适配层负责把它"翻译"成该 runtime 能识别的格式。

## 各 Runtime 安装详情

### Claude Code

**安装方式**:Plugin(通过 marketplace)

```bash
# 方式一:Anthropic 官方 marketplace(推荐)
/plugin install superpowers@claude-plugins-official

# 方式二:Superpowers 自有 marketplace
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

**全局/项目级**:Plugin 安装默认全局,所有项目生效。无项目级安装。

**更新**:Plugin 更新自动推送,或手动 `/plugin update superpowers`。

**适配层**:`.claude-plugin/plugin.json` 定义插件清单,`CLAUDE.md` 提供指令。

### Codex CLI

**安装方式**:Plugin(通过 marketplace)

```bash
/plugins           # 打开插件搜索
# 搜索 superpowers → Install Plugin
```

**全局/项目级**:marketplace 安装默认全局。

**适配层**:`.codex-plugin/` 目录。

### Codex App

**安装方式**:GUI

1. 打开 Codex App
2. 侧边栏点击 Plugins
3. Coding 分类找到 Superpowers
4. 点击 `+` 安装

### Cursor

**安装方式**:Plugin

```bash
/add-plugin superpowers
# 或在插件 marketplace 搜索 "superpowers"
```

**适配层**:`.cursor-plugin/` 目录。

### Gemini CLI

**安装方式**:Extension

```bash
gemini extensions install https://github.com/obra/superpowers
# 更新
gemini extensions update superpowers
```

> 注意:Google 已于 2026-06-18 停止 Gemini CLI 支持,extension 无法再安装或更新。

### Kimi Code

**安装方式**:Plugin

```bash
# 方式一:GUI
/plugins → Marketplace → Superpowers → 安装

# 方式二:直接从仓库安装
/plugins install https://github.com/obra/superpowers
```

**适配层**:`.kimi-plugin/` 目录,详见 `docs/README.kimi.md`。

### OpenCode

**安装方式**:按 INSTALL.md 指引

```bash
# 告诉 OpenCode:
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

**适配层**:`.opencode/` 目录,详见 `docs/README.opencode.md`。

### Factory Droid

**安装方式**:Plugin

```bash
droid plugin marketplace add https://github.com/obra/superpowers
droid plugin install superpowers@superpowers
```

### Antigravity

**安装方式**:Plugin

```bash
agy plugin install https://github.com/obra/superpowers
# 更新:重新执行同一命令
```

**特点**:Antigravity 运行 plugin 的 session-start hook,Superpowers 从第一条消息就激活。

### Pi

**安装方式**:Package

```bash
pi install git:github.com/obra/superpowers
# 本地开发:
pi -e /path/to/superpowers
```

**特点**:Pi 有原生 skills 支持,不需要兼容性 `Skill` 工具。

### GitHub Copilot CLI

**安装方式**:Plugin

```bash
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

## 全局 vs 项目级:通用原则

| 分类 | 适合全局 | 适合项目级 |
|------|---------|-----------|
| 跨项目通用方法论 | Superpowers(TDD、debugging、code review) | — |
| 项目特定流程 | — | 该项目独有的 skill |
| 底层能力增强 | 通用工具链配置 | — |
| 日常高频使用 | 通用 prompt 模板 | — |

各 runtime 全局安装位置:

| Runtime | 全局位置 | 项目级位置 |
|---------|---------|-----------|
| Claude Code | `~/.claude/skills/`(Personal)或 Plugin 安装 | `.claude/skills/`(Project) |
| Codex | Plugin 安装默认全局 | — |
| Hermes | `~/.hermes/skills/` | `external_dirs` 配置项目路径 |
| Cursor | Plugin 安装默认全局 | — |
| 其他 | 按 runtime 文档 | 按 runtime 文档 |

> Claude Code 优先级:Enterprise > Personal(`~/.claude/skills/`) > Project(`.claude/skills/`) > Plugin
