---
status: 暂缓
created: 2026-07-09
updated: 2026-07-10
目标名: 00-KnowledgeBase
阻碍: 80+ 文件机械替换风险 + 当前阶段收益不显著
---

# ⚠️ 目录重命名待办(暂缓)

> **历史命名**:当前 `00-AgentBase/` 名字会引起歧义——它不是"Agent 基础概念",而是**完整的 Agent 知识库**(包含概念、运行时、工具、安全、行为等多模块)。
>
> **目标命名**:`00-KnowledgeBase/`(更准确、更不易误读)
>
> **当前决定**:**暂缓**——本目录名歧义已通过 `00-目录索引.md` 解释清楚,机械重命名 80+ 文件的当前收益不显著。
>
> **何时执行**:如下任一情况出现时
> - 团队/跨用户场景,新成员频繁被 `AgentBase` 名称误导
> - 第三方工具(IDE / 静态生成器)不支持以 `AgentBase` 开头的目录命名规范
> - 整体迁移到新结构时一并执行

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-07-09 | 创建待办 | 原 `00-AgentBase/` 名歧义 |
| 2026-07-10 | 暂缓 | 80+ 文件批量替换风险 + 现有 `00-目录索引.md` 已解释清楚 |

## 如果将来要执行

触发条件 + 执行步骤见下方"历史计划"小节(保留作为未来参考)。

## 触发条件

✅ Obsidian 完全退出(任务管理器看不到 `Obsidian.exe`)

✅ 没有其他程序占用 `D:\valut\trade\agent\00-AgentBase`(TRAE / 文件管理器 / 终端本身也算)

## 执行步骤

### 步骤 1:重命名目录

```powershell
Rename-Item -Path 'D:\valut\trade\agent\00-AgentBase' -NewName '00-KnowledgeBase'
```

如果失败用 Robocopy:
```powershell
robocopy 'D:\valut\trade\agent\00-AgentBase' 'D:\valut\trade\agent\00-KnowledgeBase' /E /MOVE /R:3 /W:1
```

### 步骤 2:批量替换 markdown 引用

```powershell
$kb = 'D:\valut\trade\agent'
Get-ChildItem -Recurse -File $kb -Filter *.md | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace '00-AgentBase', '00-KnowledgeBase' | Set-Content $_.FullName -Encoding UTF8
}
```

### 步骤 3:替换标题里的"AgentBase"

```powershell
Get-ChildItem -Recurse -File $kb -Filter *.md | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace 'AgentBase 总览', 'KnowledgeBase 总览' `
                                  -replace 'AgentBase/', 'KnowledgeBase/' `
                                  -replace 'AgentBase 知识库管理员', 'KnowledgeBase 知识库管理员' `
        | Set-Content $_.FullName -Encoding UTF8
}
```

### 步骤 4:验证

```powershell
# 1. 物理目录存在
Test-Path 'D:\valut\trade\agent\00-KnowledgeBase'

# 2. 没有残留旧名字
Get-ChildItem -Recurse -File 'D:\valut\trade\agent' -Filter *.md |
    Select-String -Pattern '00-AgentBase' |
    Select-Object -First 5
# 应该没有结果(或者只有 README-rename-notice.md 本身)

# 3. Obsidian vault 配置同步
# .obsidian/ 里的 app.json 可能引用旧路径
Get-Content 'D:\valut\trade\agent\.obsidian\app.json' -Raw |
    Select-String 'AgentBase'
```

### 步骤 5:删除本文件

```powershell
Remove-Item 'D:\valut\trade\agent\00-KnowledgeBase\README-rename-notice.md'
```

## 涉及的文件数

预估:80+ 个 markdown(00-KnowledgeBase 内)+ 10+ 个跨目录引用(01-Skills/02-Plugins/03-Prompts/04-MCP/05-Boundaries/06-Migration 的 SKILL.md + README)

## 相关

- [`../../99-Roadmap.md`](../../99-Roadmap.md) — 把本任务记入决策日志
- [`../../AGENTS.md`](../../AGENTS.md) — 根 AGENTS.md 也会涉及更新