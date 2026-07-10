# Plugins

> 这里存放**已部署就绪**的 plugin 适配器。区别于 `01-Skills/` 的内容:01-Skills 是 canonical source,02-Plugins 是部署形态——把同一份内容打包成不同 Runtime 期待的 plugin 结构(Claude Plugin / Codex Plugin / Marketplace 等)。

## 这个目录放什么

- **Plugin adapter**:把 canonical skill 打包成 Runtime 期待的 plugin 格式
- **plugin.json / marketplace.json** 元数据
- **跨 Runtime 适配规则**:同一份 skills/ 如何转成 .codex-plugin/ / .cursor-plugin/
- **plugin 部署说明**:安装方式、配置项、验证清单

## 这个目录不放什么

- ❌ **不要复制 skill 内容**——内容唯一来源是 `01-Skills/`,重复存放会产生同步问题
- ❌ **不要写 Plugin 概念教程**——见 `../00-AgentBase/02-概念全景辨析`
- ❌ **不要放运行时自带 plugin**——只用本知识库管理的

## 适配原则

每个 plugin 适配器必须满足:

1. **单向引用**:plugin 只引用 `01-Skills/` 中的目录,不复制内容
2. **符号链接或路径引用**:Claude Plugin 支持 `"skills": "./path/to/skills"`,直接指向 canonical
3. **元数据独立**:plugin.json 中的 version / keywords / author 与 SKILL.md 保持一致
4. **多 Runtime 一份**:同一份内容可以打包成 Claude / Codex / Cursor 三种 plugin,放在子目录分开

## 已收录 Plugin 适配器

| Plugin | Runtime | canonical source | 状态 |
|--------|---------|------------------|------|
| [ui-ux-pro-max/](./ui-ux-pro-max/) | Claude Code | `../../01-Skills/ui-ux-pro-max/` | 可用 |
| [superpowers/](./superpowers/) | Claude Code | `../../01-Skills/superpowers/` | 可用 |
| [kb-init/](./kb-init/) | 通用 Skills | `../../01-Skills/kb-init/` | 可用 |