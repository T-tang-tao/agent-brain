# Deploy — 部署细节与脚本引用

> 本文件定义 `project-init` Step 5 的部署细节、桥接策略、`.gitignore` 模板,以及与现有部署脚本的关系。

## 0. 部署总览

```
Step 5.1: 创建 .agent/ 7 子目录
Step 5.2: 软链/复制选中 skill 到 .agent/skills/
Step 5.3: 按 Runtime 桥接到原生目录
Step 5.4: 写推荐的 .gitignore
Step 5.5: 输出部署报告
```

## 1. 目录创建

固定 7 个子目录,与 `00-AgentBase/runtime/00-项目级配置.md` §1.1 一致:

```
.agent/
├── skills/         # 项目级 skill
├── agents/         # 项目级子代理
├── plugins/        # 项目级插件
├── prompts/        # 项目级 prompt 模板
├── mcp/            # 项目级 MCP 配置
├── hooks/          # 项目级 hooks
└── memory/         # 项目级长期记忆
```

**实现**:`scripts/scaffold.ps1` 调用:

```powershell
$dirs = @("skills", "agents", "plugins", "prompts", "mcp", "hooks", "memory")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path ".\.agent\$dir" -Force | Out-Null
}
```

## 2. Skill 软链/复制

### 2.1 默认:软链(junction)

跨 Runtime 共享、源更新自动生效:

```powershell
foreach ($skill in $selectedSkills) {
    $src = Join-Path $KB_ROOT "01-Skills\$skill"
    $dst = ".\.agent\skills\$skill"
    if (-not (Test-Path $dst)) {
        New-Item -ItemType Junction -Path $dst -Target (Resolve-Path $src) | Out-Null
    }
}
```

**Windows junction 不需要管理员权限**,推荐用 junction 而不是 symbolic link。

### 2.2 备选:复制

发布/部署场景(避免运行时对知识库的写权限依赖):

```powershell
Copy-Item -Recurse -Force "$KB_ROOT\01-Skills\$skill" ".\.agent\skills\$skill"
```

**只在用户明确说"复制而不是软链"时使用**。

### 2.3 大项目:项目专属 skill

如果用户有项目专属 skill,放在 `.agent/skills/<name>/`,不进知识库。

V1 不做项目专属 skill 的自动识别,留给用户手动放。

## 3. Runtime 桥接

### 3.1 Claude Code

```powershell
New-Item -ItemType Directory -Path ".\.claude" -Force | Out-Null

# 删除已有(避免 junction 冲突)
if (Test-Path ".\.claude\skills") { Remove-Item ".\.claude\skills" -Recurse -Force }
if (Test-Path ".\.claude\agents") { Remove-Item ".\.claude\agents" -Recurse -Force }
if (Test-Path ".\.claude\hooks")  { Remove-Path ".\.claude\hooks"  -Recurse -Force }

# 创建 junction
New-Item -ItemType Junction -Path ".\.claude\skills" -Target "..\.agent\skills" | Out-Null
New-Item -ItemType Junction -Path ".\.claude\agents" -Target "..\.agent\agents" | Out-Null
New-Item -ItemType Junction -Path ".\.claude\hooks"  -Target "..\.agent\hooks"  | Out-Null
```

**`.mcp.json` 单独处理**:`.agent/mcp/claude-code.json` → `.mcp.json`(复制,不是软链)

```powershell
if (Test-Path ".\.agent\mcp\claude-code.json") {
    Copy-Item -Force ".\.agent\mcp\claude-code.json" ".\.mcp.json"
}
```

### 3.2 Codex CLI

```powershell
New-Item -ItemType Directory -Path ".\.codex" -Force | Out-Null

# 优先用 junction(简化版,与 Claude Code 一致)
if (Test-Path ".\.codex\skills") { Remove-Item ".\.codex\skills" -Recurse -Force }
New-Item -ItemType Junction -Path ".\.codex\skills" -Target "..\.agent\skills" | Out-Null
```

**更优方案**:用 `external_dirs` 配置,不动目录结构:

```toml
# .codex/config.toml
[skills]
external_dirs = ["./.agent/skills"]
```

V1 用 junction(简化),V2 可加 `external_dirs` 选项。

### 3.3 Hermes Agent

Hermes 用配置文件,不动目录:

```yaml
# ~/.hermes/config.yaml(全局,影响所有项目)
skills:
  external_dirs:
    - ~/.claude/skills  # 复用 Claude Code 的
    - <绝对路径>/.agent/skills
```

**实现**:V1 输出 YAML 片段让用户自己合并,V2 可自动写入。

### 3.4 Trae

```powershell
New-Item -ItemType Directory -Path ".\.trae" -Force | Out-Null
if (Test-Path ".\.trae\skills") { Remove-Item ".\.trae\skills" -Recurse -Force }
if (Test-Path ".\.trae\AGENTS.md") { Remove-Item ".\.trae\AGENTS.md" -Force }
New-Item -ItemType Junction -Path ".\.trae\skills"   -Target "..\.agent\skills" | Out-Null
New-Item -ItemType Junction -Path ".\.trae\AGENTS.md" -Target "..\AGENTS.md"    | Out-Null
```

### 3.5 multi Runtime

对每个检测到的 Runtime 重复对应步骤,避免重复操作 `.agent/` 本身。

## 4. `.gitignore` 模板

写入项目根 `.gitignore`(不覆盖,只 append):

```gitignore
# .agent/ 项目级 Agent 配置
# 推荐:选择性入库
.agent/cache/
.agent/memory/.session/
.agent/mcp/*-local.json
# 这些入 .git:
# .agent/skills/         # 团队共享
# .agent/agents/
# .agent/prompts/
# .agent/hooks/
# AGENTS.md
```

**判断标准**(可向用户说明):
- 可重建的(从资产层生成) → 不入库
- 团队约定的(项目说明、规范) → 入库
- 含密钥的(MCP 配置、个人记忆) → 不入库

## 5. 与现有脚本的关系

### 5.1 引用但不重写

`00-AgentBase/runtime/00-项目级配置.md` §5 的 `deploy-assets.ps1` 是更通用的部署脚本(从 KB 资产层部署)。

**本 Skill 的 `scripts/scaffold.ps1` 范围更小**:
- 只在项目内创建 `.agent/` 和 `AGENTS.md`
- 不涉及从 KB 资产层全量复制
- 假设 skill 已经被 `01-Skills/AGENTS.md` §3 的部署流程管理

### 5.2 复用现有脚本

V2 可重构为引用:

```powershell
# 从 KB 资产层部署
& "$KB_ROOT\00-AgentBase\runtime\deploy-assets.ps1" -Runtime $primary
```

但 V1 不引入这个依赖,保持本 Skill 自包含。

## 6. 部署报告输出

Step 5.5 输出:

```
✓ 创建 .agent/ 目录(skills/ agents/ plugins/ prompts/ mcp/ hooks/ memory/)
✓ 软链 skills:
  - .agent/skills/agents-md-author → ${KB_ROOT}\01-Skills\agents-md-author
  - .agent/skills/superpowers → ${KB_ROOT}\01-Skills\superpowers
  - .agent/skills/ui-ux-pro-max → ${KB_ROOT}\01-Skills\ui-ux-pro-max
✓ 桥接到 claude-code:.claude/skills → .agent/skills
✓ 写入 .gitignore(3 项)
✓ AGENTS.md 已生成(7 段,约 80 行)

下一步:
1. 启动 Claude Code 验证 AGENTS.md 被加载
2. 试着问 "如何跑测试",检查 superpowers skill 是否被识别
3. 如果要加项目专属 skill,放在 .agent/skills/<name>/
```

## 7. 故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| `New-Item Junction` 失败:权限不足 | Windows junction 在某些情况下需要管理员 | 改为复制,或提示用户开开发者模式 |
| `.claude/skills` 已存在但不是 junction | 之前用过 Claude Code | 先 Remove-Item 再建 junction |
| `external_dirs` 配置不生效 | Codex 配置路径错误 | 检查 `~/.codex/config.toml` 路径 |
| 软链生效但 skill 不被识别 | junction 目标相对路径错 | 用绝对路径或 `..\.agent\skills` |
| `.gitignore` 写错位置 | 不是项目根 | 用 `Resolve-Path .` 确认 |
| 用户取消部署 | 按 Ctrl+C | 已创建的 `.agent/` 和 `AGENTS.md` 保留(用户可手动回滚) |
