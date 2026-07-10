# Runtime Detect — Runtime 识别方法

> 本文件定义 `scripts/detect-runtime.ps1` 的检测逻辑、优先级、边界情况。

## 0. 检测目标

识别当前项目目录所使用的 Agent Runtime,影响 Step 5 的桥接策略:

| Runtime | 桥接方式 |
|---------|----------|
| `claude-code` | 创建 `.claude/skills` → `../.agent/skills` 软链 |
| `codex` | 创建 `.codex/skills` → `../.agent/skills` 软链(或 `external_dirs` 配置) |
| `hermes` | 写 `~/.hermes/config.yaml` 的 `external_dirs` |
| `trae` | 创建 `.trae/skills` → `../.agent/skills` 软链 + `AGENTS.md` 软链 |

## 1. 检测信号(按优先级)

### 1.1 环境变量(最强)

| 环境变量 | Runtime |
|----------|---------|
| `CLAUDE_CODE` | `claude-code` |
| `CLAUDE_PROJECT_DIR` | `claude-code` |
| `CODEX_HOME` | `codex` |
| `CODEX` | `codex` |
| `HERMES_HOME` | `hermes` |
| `HERMES` | `hermes` |
| `TRAE_HOME` | `trae` |

### 1.2 当前目录的原生配置目录

| 目录 | Runtime |
|------|---------|
| `.claude/` | `claude-code` |
| `.codex/` | `codex` |
| `.hermes/` | `hermes` |
| `.trae/` | `trae` |

### 1.3 用户配置目录

| 路径 | Runtime |
|------|---------|
| `~/.claude/` 存在 | `claude-code`(全局) |
| `~/.codex/` 存在 | `codex`(全局) |
| `~/.hermes/` 存在 | `hermes`(全局) |
| `~/.trae/` 存在 | `trae`(全局) |

## 2. 检测顺序

```
1. 环境变量(最高优先,Runtime 启动时一定会设置)
2. 当前目录的原生目录(项目级配置存在性)
3. 用户配置目录(全局配置存在性)
4. 都不存在 → unknown
```

## 3. multi Runtime 处理

如果检测到多个 Runtime,输出 `multi` 并列出所有,向用户确认:

```
检测到多个 Runtime:
- claude-code(.claude/ 存在)
- codex(.codex/ 存在)
- trae(.trae/ 存在)

选择哪些?(多选,逗号分隔,默认全选)
```

## 4. unknown Runtime 处理

如果一个都没检测到:

```
未检测到任何已知的 Agent Runtime。
将创建 .agent/ 目录,但不桥接到任何 Runtime 原生目录。
稍后安装 Runtime 时,运行 .\scripts\bridge.ps1 -Runtime <name> 桥接。
```

仍然创建 `.agent/` 和 `AGENTS.md`,但跳过桥接步骤。

## 5. 知识库根目录保护

**关键检查**:如果 `$KB_ROOT` 等于当前 PWD,**拒绝执行**,提示用户用 `kb-init` 而不是 `project-init`:

```
错误:当前目录是知识库根 ($KB_ROOT)
project-init 用于初始化项目级 Agent 环境,不是知识库本身。
如需初始化知识库,请使用 kb-init Skill。
```

检查方式(在 `detect-runtime.ps1` 顶部):
```powershell
if (-not $env:KB_ROOT) {
    Write-Error "环境变量 KB_ROOT 未设置。请先设置: `$env:KB_ROOT = '<你的知识库根绝对路径>'"
    exit 1
}
$kbRoot = $env:KB_ROOT
$resolvedKbRoot = (Resolve-Path $kbRoot).Path
$resolvedPwd = (Resolve-Path .).Path
if ($resolvedPwd -eq $resolvedKbRoot) {
    Write-Error "当前目录是知识库根,使用 kb-init 而不是 project-init"
    exit 1
}
```

## 6. 输出格式

检测脚本输出 JSON,供后续步骤消费:

```json
{
  "primary": "codex",
  "all": ["codex", "claude-code"],
  "signals": {
    "env": {"CODEX_HOME": "C:\\Users\\xxx\\.codex"},
    "dirs": [".codex/"],
    "user": ["~/.claude/"]
  },
  "kb_root_match": false
}
```

## 7. 故障排查

| 症状 | 原因 | 处理 |
|------|------|------|
| 总是 unknown | 在新机器上,Runtime 未启动 | 启动一次 Runtime 让它设置环境变量 |
| 检测到 multi 但用户只要一个 | 同时安装了多个 | 用 `multi` 输出让用户选 |
| 软链失败(权限) | Windows 需要开发者模式或管理员 | 提示用户启用开发者模式或用复制代替 |
| KB_ROOT 检测错误 | 知识库克隆到非默认位置 | 用户设置 `$env:KB_ROOT` 环境变量 |
