# UI/UX Pro Max - 跨 Runtime 安装指南

本技能源仓库是一个 Claude Plugin(`nextlevelbuilder/ui-ux-pro-max-skill`),在不同 Runtime 下的部署方式各不相同。

## 通用原则

- **本知识库是 canonical source**:任何 Runtime 都从这里取
- **不能整仓直接拷贝到 Runtime**:Runtime 需要适配器,不能直接挂载源仓库
- **跨 Runtime 适配原则**:见 [`00-AgentBase/behavior/02-跨Runtime技能管理.md`](../../../00-AgentBase/behavior/02-跨Runtime技能管理.md)

## 按 Runtime 部署

### 1. Claude Code (Plugin 首选)

源仓库就是 Claude Plugin,最原生。两种方式:

#### 方式 A:作为 Claude Plugin 安装(推荐)

```bash
# 1. 复制到 .claude/plugins/ 下
mkdir -p ~/.claude/plugins/ui-ux-pro-max
cp -r "$KB_ROOT/01-Skills/ui-ux-pro-max/." ~/.claude/plugins/ui-ux-pro-max/

# 2. 或作为项目级 plugin
mkdir -p <your-project>/.claude/plugins/ui-ux-pro-max
cp -r "$KB_ROOT/01-Skills/ui-ux-pro-max/." <your-project>/.claude/plugins/ui-ux-pro-max/
```

Plugin 包含的元数据(`plugin.json`)会让 Claude Code 自动发现 7 个子技能。

#### 方式 B:作为 Skills 安装(简化版)

只复制 `skills/` 子目录,放弃 plugin 元数据:

```bash
mkdir -p ~/.claude/skills/ui-ux-pro-max
cp -r "$KB_ROOT/01-Skills/ui-ux-pro-max/skills"/* ~/.claude/skills/ui-ux-pro-max/
```

这种方式会把 7 个子技能平铺到 `~/.claude/skills/`,Claude Code 会自动发现。但失去 `plugin.json` 元数据。

### 2. Codex CLI

Codex 不直接支持 Claude Plugin,需要适配器:

```bash
# 1. 创建 .codex-plugin/ 适配器
mkdir -p $KB_ROOT/01-Skills/ui-ux-pro-max/.codex-plugin/
# 创建 plugin.json 的 codex 版本(自定义)

# 2. 链接到 Codex skills 目录
mkdir -p ~/.codex/skills/ui-ux-pro-max
cp -r "$KB_ROOT/01-Skills/ui-ux-pro-max/skills"/* ~/.codex/skills/ui-ux-pro-max/
```

具体 Codex Plugin 适配格式见 [`00-AgentBase/behavior/02-跨Runtime技能管理.md` §3.2](../../../00-AgentBase/behavior/02-跨Runtime技能管理.md)。

### 3. Cursor / Windsurf

这两个 IDE 读取 `.cursorrules` / `.windsurfrules`,不直接支持 Skill 系统。

**适配方案**:

```bash
# 把 SKILL.md 内容提炼为 .cursorrules
cat $KB_ROOT/01-Skills/ui-ux-pro-max/skills/ui-ux-pro-max/SKILL.md > .cursorrules.ui-ux-pro-max
# 提示 Cursor 在相关任务时加载这个 rules
```

### 4. Antigravity (Claude Code 变种)

同 Claude Code 方式,直接以 Plugin 形式安装。

## 字体文件说明

`skills/ui-styling/canvas-fonts/` 包含 70+ 个 .ttf 字体文件 + .OFL.txt 许可证。这些是 SIL Open Font License,可在商业项目中自由使用。

**部署时**:字体文件随 skills/ 一起复制即可,无需额外配置。

## CSV 数据访问

`skills/ui-ux-pro-max/data/*.csv` 是核心数据库,通过 Python 脚本访问:

```python
import csv

# 加载样式数据
with open("$KB_ROOT/01-Skills/ui-ux-pro-max/skills/ui-ux-pro-max/data/styles.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["Style"], row["Keywords"])
```

或用源仓库提供的脚本:

```bash
cd $KB_ROOT/01-Skills/ui-ux-pro-max/skills/ui-ux-pro-max/
python scripts/search.py --query "glassmorphism dashboard"
```

## Python 依赖

部分 scripts/ 下的 Python 脚本需要:
- `Pillow` (图像处理)
- `requests` (HTTP 调用)

安装:

```bash
pip install Pillow requests
```

完整依赖见 `skills/ui-styling/scripts/requirements.txt`。

## 注意事项

- **不要修改 skills/ 下的文件**:这是源仓库快照,修改后无法同步上游更新
- **二次开发**:`$KB_ROOT/01-Skills/ui-ux-pro-max/SKILL.md` 是本知识库的入口文件,只改这里,不改源仓库
- **更新上游**:见 [`$KB_ROOT/01-Skills/AGENTS.md` §7 外部技能更新](../../../AGENTS.md)
