# superpowers Claude Plugin Adapter

> superpowers 的 Claude Code Plugin 适配器。**不复制内容**,只引用 canonical source。

## Canonical Source

[`../../01-Skills/superpowers/`](../../01-Skills/superpowers/)

## 安装

```bash
# 项目级
ln -s "${KB_ROOT}/02-Plugins/superpowers" ./.claude/plugins/superpowers

# 或全局(注意 skills/ 相对路径)
mkdir -p ~/.claude/plugins
cp -r "${KB_ROOT}/02-Plugins/superpowers" ~/.claude/plugins/superpowers
ln -s ${KB_ROOT}/01-Skills/superpowers/skills ~/.claude/plugins/superpowers/skills
```

## 验证

```bash
ls ${KB_ROOT}/01-Skills/superpowers/skills/brainstorming/SKILL.md
```

## 相关

- [Canonical SKILL.md](../../../01-Skills/superpowers/SKILL.md)
- [跨 Runtime 安装指南](../../../01-Skills/superpowers/references/installation-per-runtime.md)
