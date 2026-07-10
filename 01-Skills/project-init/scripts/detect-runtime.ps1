# detect-runtime.ps1 — 检测当前 Agent Runtime
# 用法:powershell .\detect-runtime.ps1
# 输出:JSON 对象 { primary, all, signals, kb_root_match }

[CmdletBinding()]
param(
    [string]$KbRoot = $(if ($env:KB_ROOT) { $env:KB_ROOT } else { "D:\valut\agent" })
)

$ErrorActionPreference = "Stop"

# 1. KB_ROOT 保护
$resolvedKbRoot = $null
try { $resolvedKbRoot = (Resolve-Path $KbRoot -ErrorAction Stop).Path } catch {}
$resolvedPwd = (Resolve-Path .).Path
$kbRootMatch = $false
if ($resolvedKbRoot -and $resolvedPwd -eq $resolvedKbRoot) {
    $kbRootMatch = $true
    Write-Error "当前目录是知识库根 ($resolvedKbRoot)。project-init 用于初始化项目级 Agent 环境,请使用 kb-init 初始化知识库。"
    exit 1
}

# 2. 检测环境变量
$envSignals = [ordered]@{}
$envMap = [ordered]@{
    "CLAUDE_CODE"        = "claude-code"
    "CLAUDE_PROJECT_DIR" = "claude-code"
    "CODEX"              = "codex"
    "CODEX_HOME"         = "codex"
    "HERMES"             = "hermes"
    "HERMES_HOME"        = "hermes"
    "TRAE_HOME"          = "trae"
}
foreach ($key in $envMap.Keys) {
    $val = Get-Item "Env:\$key" -ErrorAction SilentlyContinue
    if ($val) {
        $rt = $envMap[$key]
        $envSignals[$rt] = $val.Value
    }
}

# 3. 检测项目目录的原生配置目录
$dirSignals = [ordered]@{}
$dirMap = [ordered]@{
    ".claude" = "claude-code"
    ".codex"  = "codex"
    ".hermes" = "hermes"
    ".trae"   = "trae"
}
foreach ($dir in $dirMap.Keys) {
    if (Test-Path ".\$dir") {
        $dirSignals[$dirMap[$dir]] = ".\$dir"
    }
}

# 4. 检测用户配置目录
$userSignals = [ordered]@{}
$userMap = [ordered]@{
    "$env:USERPROFILE\.claude" = "claude-code"
    "$env:USERPROFILE\.codex"  = "codex"
    "$env:USERPROFILE\.hermes" = "hermes"
    "$env:USERPROFILE\.trae"   = "trae"
}
foreach ($path in $userMap.Keys) {
    if ($path -and (Test-Path $path)) {
        $userSignals[$userMap[$path]] = $path
    }
}

# 5. 合并结果(环境变量 > 项目目录 > 用户目录)
$all = [ordered]@{}
foreach ($rt in @("claude-code", "codex", "hermes", "trae")) {
    if ($envSignals.Contains($rt))      { $all[$rt] = "env"   }
    elseif ($dirSignals.Contains($rt))  { $all[$rt] = "dir"   }
    elseif ($userSignals.Contains($rt)) { $all[$rt] = "user"  }
}

# 6. 输出 JSON
$primary = if ($all.Count -gt 0) { @($all.Keys)[0] } else { "unknown" }

$result = [ordered]@{
    primary      = $primary
    all          = @($all.Keys)
    signals      = [ordered]@{
        env  = $envSignals
        dir  = $dirSignals
        user = $userSignals
    }
    kb_root_match = $kbRootMatch
}

$result | ConvertTo-Json -Depth 3 -Compress
