# ui-ux-pro-max Claude Plugin Adapter

> 这是 ui-ux-pro-max 的 Claude Code Plugin 适配器。**它不复制内容**,只引用 canonical source。

## Canonical Source

[`../../01-Skills/ui-ux-pro-max/`](../../01-Skills/ui-ux-pro-max/)

## 安装

### 方式 A:作为项目级 Plugin(推荐用于开发项目)

```bash
# 1. 在项目根目录创建 plugin 软链接(或整个 plugin 适配器拷贝过来)
ln -s "${KB_ROOT}/02-Plugins/ui-ux-pro-max" ./.claude/plugins/ui-ux-pro-max

# 2. Claude Code 会自动发现 .claude-plugin/plugin.json
```

### 方式 B:作为全局 Plugin

```bash
# 复制 plugin 适配器到全局 plugins 目录
mkdir -p ~/.claude/plugins
cp -r "${KB_ROOT}/02-Plugins/ui-ux-pro-max" ~/.claude/plugins/ui-ux-pro-max

# 关键:plugin.json 中 skills 路径是相对路径 "../../01-Skills/ui-ux-pro-max/skills/"
# 如果 kb 在 /A,plugins 在 /B,相对路径会失效。两种方案:
# 方案 1:在 ~/.claude/plugins/ui-ux-pro-max/ 下创建符号链接指向 canonical
#   ln -s /A/01-Skills/ui-ux-pro-max/skills ~/.claude/plugins/ui-ux-pro-max/skills
# 方案 2:plugin.json 改成绝对路径(失去可移植性)
```

## 文件清单

```
02-Plugins/ui-ux-pro-max/
├── README.md                  ← 本文件(部署说明)
└── .claude-plugin/
    └── plugin.json            ← Plugin 元数据,skills 路径指向 01-Skills/
```

## 验证

```bash
# 检查 plugin 被识别
ls ~/.claude/plugins/ui-ux-pro-max/.claude-plugin/plugin.json

# 检查 skills 路径可达
ls ${KB_ROOT}/01-Skills/ui-ux-pro-max/skills/ui-ux-pro-max/SKILL.md
```

## 更新

源仓库更新时:

```bash
cd ${KB_ROOT}/01-Skills/ui-ux-pro-max
git pull origin main  # 如果源仓库在 git 里
# 重新生成 CSV/字体 → 复制到 skills/ → plugin adapter 自动指向新内容
```

## 相关

- [Canonical SKILL.md](../../../01-Skills/ui-ux-pro-max/SKILL.md)
- [跨 Runtime 安装指南](../../../01-Skills/ui-ux-pro-max/references/installation-per-runtime.md)
