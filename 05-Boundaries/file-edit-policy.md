# File Edit Policy

> 文件编辑边界。Agent 修改任何文件前必须参考本策略。

## 规则名称

`file-edit-policy`

## 适用范围

- 所有 agent(Claude Code / Codex / Hermes)
- 所有文件编辑操作(Write / SearchReplace / Edit)
- 整个文件系统的任何目录

## 允许的行为

✅ Agent 可自主执行:

- **读所有文件**(Read / Grep / Glob):知识库内所有 markdown / json / csv / yaml
- **写实践层目录**:`01-Skills/`、`02-Plugins/`、`03-Prompts/`、`04-MCP/`、`06-Migration/`
- **写 `99-Roadmap.md`**:追加条目(不删除已有条目)
- **创建新文件**:在任何实践层目录下创建新 .md / .json / .csv 文件
- **修改 SKILL.md frontmatter**:版本号、status 字段

## 需要确认的行为

⚠️ 必须先问用户,得到明确 yes 才执行:

- **写 `00-AgentBase/`**:认知层文档变更需要用户确认,因为这些是"知识库管理员"的依据
- **修改 `AGENTS.md`**(任何 AGENTS.md):管理规范变更
- **修改 `.gitignore` / `.env`**:影响仓库行为
- **修改 `README.md`**:对外可见
- **修改 `.obsidian/`**:破坏 Obsidian 配置
- **删除任何文件**:即使是"废弃"文件

## 禁止的行为

❌ 任何情况下禁止:

- **覆盖 `00-AgentBase/` 而没有备份**:必须先 cp 一份 .bak
- **删除 `.obsidian/` 下任何文件**:Obsidian 客户端配置
- **把密钥/token 写入任何 .md**:用环境变量或 .gitignore 保护
- **把实时数据写入知识库**:价格、订单、账户余额等
- **修改 `01-Skills/*/skills/` 下原始内容**:这是源仓库快照,通过更新流程改,不直接编辑
- **创建空目录的乱放文件**:写完必须有意义、有引用

## 风险说明

| 风险 | 触发 | 后果 |
|------|------|------|
| 知识库索引失效 | 改 `AGENTS.md` / `README.md` 不更新引用 | 用户找不到内容 |
| Obsidian 崩溃 | 改 `.obsidian/*.json` | 客户端配置错乱 |
| 信息孤岛 | 写新文件不引用 | 新内容变成孤岛 |
| 密钥泄露 | 写 `.env` 到知识库 | 公网可见 |
| 实时污染 | 写价格/订单到策略笔记 | 数据陈旧、决策错误 |

## Agent 执行说明

1. **判断路径**:当前要改的文件路径属于哪类?
   - `00-AgentBase/` → [需确认]
   - `01-Skills/02-Plugins/03-Prompts/04-MCP/06-Migration/` → [允许]
   - `.obsidian/` → [禁止]
   - 其他 → 默认 [需确认]
2. **判断动作**:创建 / 修改 / 删除?
   - 创建新文件 → [允许](在实践层)
   - 修改已有 → 看具体路径分类
   - 删除 → [需确认]
3. **判断内容**:是否含密钥 / 实时数据 / PII?
   - 是 → [禁止] + 建议替代方案
4. **执行 + 验证**:
   - 写完 Read 一下,确认内容正确
   - 改完 Grep 一下,确认引用没断
5. **报告**:简短说明改了什么、影响什么

## 例子

### 允许

```text
> 在 01-Skills/kb-init/references/ 下加一个新文件 types-addendum.md
```

✅ 直接执行 + 报告

### 需确认

```text
> 我想改 00-AgentBase/AGENTS.md 的 §4 编排部分
```

⚠️ "这是认知层变更,我建议先备份(cp 到 .bak)再改,确认吗?"

### 禁止

```text
> 把我的 OpenAI API key 写进 00-AgentBase/runtime/03-ClaudeCode/02-安装部署.md 方便以后看
```

❌ "禁止。密钥绝不写入知识库。建议用环境变量 OPENAI_API_KEY + 文档里只写配置方式不写值。"

## 相关知识

- [`shell-command-policy.md`](./shell-command-policy.md) — 命令执行边界
- [`destructive-action-policy.md`](./destructive-action-policy.md) — 删除/覆盖边界
- [`../00-AgentBase/safety/01-Agent边界与限制.md`](../00-AgentBase/safety/01-Agent边界与限制.md) — 概念基础