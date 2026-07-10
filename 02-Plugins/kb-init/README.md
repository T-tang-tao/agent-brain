# kb-init Skills Adapter(全局)

> kb-init 是单一 skill,不适合做 plugin。改用"全局 Skills 部署"模式。

## Canonical Source

[`../../01-Skills/kb-init/`](../../01-Skills/kb-init/)

## 安装

### Claude Code(全局)

```bash
# 创建软链接(推荐,可双向同步)
mkdir -p ~/.claude/skills
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\kb-init" -Target "${KB_ROOT}\01-Skills\global\kb-init"
```

### Codex CLI

```bash
mkdir -p ~/.codex/skills
cp -r "${KB_ROOT}/01-Skills/kb-init" ~/.codex/skills/kb-init
```

### Hermes Agent

```bash
mkdir -p ~/.hermes/skills
cp -r "${KB_ROOT}/01-Skills/kb-init" ~/.hermes/skills/kb-init
```

## 验证

```bash
# Claude Code
ls ~/.claude/skills/kb-init/SKILL.md

# Codex
ls ~/.codex/skills/kb-init/SKILL.md
```

触发测试:在对应 Runtime 中说"初始化知识库",Agent 应识别并调用 kb-init 技能。

## 相关

- [Canonical SKILL.md](../../01-Skills/kb-init/SKILL.md)
- [跨 Runtime 技能管理](../../00-AgentBase/behavior/02-跨Runtime技能管理.md)
