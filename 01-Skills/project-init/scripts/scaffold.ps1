# scaffold.ps1 — 项目级 Agent 环境骨架
# 用法:powershell .\scaffold.ps1 -Skills "agents-md-author,superpowers" -Runtimes "claude-code"
# 参数:
#   -Skills    逗号分隔的 skill 列表(必填)
#   -Runtimes  逗号分隔的 Runtime 列表(默认从 detect-runtime 读取)
#   -KbRoot    知识库根(默认 $env:KB_ROOT ?? "D:\valut\agent")
#   -NoGitignore 跳过 .gitignore 写入
#   -CopyInsteadOfLink 复制 skill 而不是软链

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Skills,

    [string]$Runtimes = "",

    [string]$KbRoot = $(if ($env:KB_ROOT) { $env:KB_ROOT } else { "D:\valut\agent" }),

    [switch]$NoGitignore,

    [switch]$CopyInsteadOfLink
)

$ErrorActionPreference = "Stop"

# 当前项目根绝对路径(junction 需要绝对路径)
$pwdAbs = (Resolve-Path .).Path

# 0. 解析参数
$skillList = @()
foreach ($s in ($Skills -split ",")) {
    $t = $s.Trim()
    if ($t) { $skillList += $t }
}
if ($skillList.Count -eq 0) {
    Write-Error "至少需要一个 skill"
    exit 1
}

if (-not $Runtimes) {
    $detectJson = & "$PSScriptRoot\detect-runtime.ps1" -KbRoot $KbRoot 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Runtime 检测失败,请用 -Runtimes 显式指定"
        exit 1
    }
    try {
        $detect = $detectJson | ConvertFrom-Json
    } catch {
        Write-Error "Runtime 检测输出无法解析"
        exit 1
    }
    if ($detect.primary -eq "unknown") {
        Write-Warning "未检测到 Runtime,跳过桥接"
        $runtimeList = @()
    } else {
        $runtimeList = @($detect.all)
    }
} else {
    $runtimeList = @()
    foreach ($r in ($Runtimes -split ",")) {
        $t = $r.Trim()
        if ($t) { $runtimeList += $t }
    }
}

# 1. KB_ROOT 校验
$resolvedKbRoot = (Resolve-Path $KbRoot).Path
$kbSkills = Join-Path $resolvedKbRoot "01-Skills"
if (-not (Test-Path $kbSkills)) {
    Write-Error "知识库 01-Skills/ 不存在:$kbSkills"
    exit 1
}

# 2. 创建 .agent/ 7 子目录
Write-Host ""
Write-Host "[1/5] 创建 .agent/ 目录..."
$dirs = @("skills", "agents", "plugins", "prompts", "mcp", "hooks", "memory")
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Path ".\.agent\$dir" -Force | Out-Null
}
Write-Host "  OK 7 个子目录"

# 3. 软链/复制选中 skill
Write-Host ""
Write-Host "[2/5] 部署 skill..."
foreach ($skill in $skillList) {
    $src = Join-Path $kbSkills $skill
    $dst = ".\.agent\skills\$skill"
    if (-not (Test-Path $src)) {
        Write-Warning "  X $skill 不存在于 $src,跳过"
        continue
    }
    if (Test-Path $dst) {
        Write-Host "  - $skill(已存在)"
        continue
    }
    if ($CopyInsteadOfLink) {
        Copy-Item -Recurse -Path $src -Destination $dst
        Write-Host "  OK $skill(复制)"
    } else {
        New-Item -ItemType Junction -Path $dst -Target (Resolve-Path $src) | Out-Null
        Write-Host "  OK $skill(junction)"
    }
}

# 4. 桥接到 Runtime
Write-Host ""
Write-Host "[3/5] 桥接到 Runtime..."
foreach ($rt in $runtimeList) {
    switch ($rt) {
        "claude-code" {
            New-Item -ItemType Directory -Path ".\.claude" -Force | Out-Null
            foreach ($sub in @("skills", "agents", "hooks")) {
                $target = ".\.claude\$sub"
                if (Test-Path $target) { Remove-Item $target -Recurse -Force }
                New-Item -ItemType Junction -Path $target -Target (Join-Path $pwdAbs ".agent\$sub") | Out-Null
            }
            if (Test-Path ".\.agent\mcp\claude-code.json") {
                Copy-Item -Force ".\.agent\mcp\claude-code.json" ".\.mcp.json"
                Write-Host "  OK claude-code: 桥接 .claude/{skills,agents,hooks} + 复制 .mcp.json"
            } else {
                Write-Host "  OK claude-code: 桥接 .claude/{skills,agents,hooks}"
            }
        }
        "codex" {
            New-Item -ItemType Directory -Path ".\.codex" -Force | Out-Null
            $target = ".\.codex\skills"
            if (Test-Path $target) { Remove-Item $target -Recurse -Force }
            New-Item -ItemType Junction -Path $target -Target (Join-Path $pwdAbs ".agent\skills") | Out-Null
            Write-Host "  OK codex: 桥接 .codex/skills"
        }
        "hermes" {
            $absSkills = (Resolve-Path ".\.agent\skills").Path
            Write-Host "  -> hermes: 请在 ~/.hermes/config.yaml 添加 external_dirs: $absSkills"
        }
        "trae" {
            New-Item -ItemType Directory -Path ".\.trae" -Force | Out-Null
            foreach ($pair in @(@("skills", "..\.agent\skills"), @("AGENTS.md", "..\AGENTS.md"))) {
                $target = ".\.trae\$($pair[0])"
                if (Test-Path $target) { Remove-Item $target -Recurse -Force }
                $absoluteTarget = Join-Path $pwdAbs ($pair[1] -replace "^\.\.\\", "")
            New-Item -ItemType Junction -Path $target -Target $absoluteTarget | Out-Null
            }
            Write-Host "  OK trae: 桥接 .trae/{skills,AGENTS.md}"
        }
        default {
            Write-Warning "  ? 未知 Runtime: $rt(跳过)"
        }
    }
}

# 5. 写 .gitignore
if (-not $NoGitignore) {
    Write-Host ""
    Write-Host "[4/5] 追加 .gitignore..."
    $gitignorePath = ".\.gitignore"
    $appendLines = @(
        "",
        "# .agent/ 项目级 Agent 配置(选择性入库)",
        ".agent/cache/",
        ".agent/memory/.session/",
        ".agent/mcp/*-local.json",
        "# 以下入 .git(团队共享):",
        "# .agent/skills/",
        "# .agent/agents/",
        "# .agent/prompts/",
        "# .agent/hooks/",
        "# AGENTS.md"
    )
    if (Test-Path $gitignorePath) {
        $existing = Get-Content $gitignorePath -Raw
        if ($existing -notmatch "\.agent/cache/") {
            Add-Content -Path $gitignorePath -Value ($appendLines -join "`n")
            Write-Host "  OK .gitignore 已追加 .agent/ 配置"
        } else {
            Write-Host "  - .gitignore 已包含 .agent/ 配置(跳过)"
        }
    } else {
        Set-Content -Path $gitignorePath -Value ($appendLines -join "`n")
        Write-Host "  OK .gitignore 已创建"
    }
}

# 6. 部署报告
Write-Host ""
Write-Host "[5/5] 部署报告"
Write-Host "  - .agent/:7 子目录"
Write-Host "  - skills: $($skillList -join ', ')"
Write-Host "  - runtimes: $($runtimeList -join ', ')"
Write-Host ""
Write-Host "下一步:"
Write-Host "  1. 启动 Runtime 验证 AGENTS.md 被加载"
Write-Host "  2. 测试一个 skill 是否被识别"
Write-Host "  3. 项目专属 skill 放在 .agent/skills/<name>/"
