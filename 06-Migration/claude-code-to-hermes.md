# Claude Code → Hermes 迁移 Playbook

> 把 Claude Code CLI Agent 配置迁移到 Hermes Agent 的完整步骤。Hermes 更适合消息网关 + 定时任务,Claude Code 更适合 IDE 集成 + 交互式开发。

## 何时迁移

迁移场景:

- ✅ **适合迁移**:任务以"接收消息 → 处理 → 回复"为主
- ✅ **适合迁移**:需要 cron 定时触发
- ✅ **适合迁移**:需要多 agent 协同
- ❌ **不必迁移**:本地 IDE 交互式开发
- ❌ **不必迁移**:单 agent 完成所有工作
- ❌ **不必迁移**:严重依赖 Claude Code 专属特性(Hooks、subagent)

## 迁移来源 vs 目标

| 维度 | 来源:Claude Code | 目标:Hermes |
|------|-------------------|--------------|
| 配置目录 | `~/.claude/` | `~/.hermes/` |
| 配置文件 | `~/.claude.json` | `~/.hermes/config.yaml` |
| Skills 目录 | `~/.claude/skills/` | `~/.hermes/skills/` |
| Plugins 目录 | `~/.claude/plugins/` | `~/.hermes/plugins/` |
| MCP 配置 | `~/.claude.json` 内嵌 | `~/.hermes/mcp.json` |
| System Prompt | `CLAUDE.md` | 每个 agent 的 `prompt` 字段 |
| Hooks | `~/.claude/settings.json` | middleware(`config.yaml`) |
| 记忆 | CLAUDE.md / memory tools | ephemeral default / `memory://` |

## 需要迁移的内容

### 1. Skills

```bash
# Claude Code: ~/.claude/skills/kb-init/
# 目标:Hermes 用相对路径引用本知识库,而不是复制

# 方式 A:符号链接(可双向同步)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.hermes\skills\kb-init" -Target "${KB_ROOT}\01-Skills\global\kb-init"

# 方式 B:复制(完全独立,断绝同步)
Copy-Item -Recurse "${KB_ROOT}\01-Skills\global\kb-init" "$env:USERPROFILE\.hermes\skills\kb-init"
```

**选择依据**:

- 链接:想保持单一来源,但 Hermes 启动慢一点
- 复制:想 Hermes 完全独立,但更新要手动同步

### 2. Plugins

Claude Code Plugin (`.claude-plugin/plugin.json`) 不能直接用于 Hermes。需要:

```bash
# 从 02-Plugins/ 取(已为 Claude Code 格式)
# 但 Hermes 不识别 plugin.json,需要拆开:
# - skills/ → 直接复制到 ~/.hermes/skills/
# - plugin.json 元数据 → 写到 agent config 的 description / keywords 字段
```

详见 [`02-Plugins/ui-ux-pro-max/README.md`](../02-Plugins/ui-ux-pro-max/README.md)。

### 3. MCP Server

Claude Code:
```json
// ~/.claude.json
{
  "mcpServers": {
    "filesystem-kb": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\valut\\trade\\agent"]
    }
  }
}
```

Hermes:
```json
// ~/.hermes/mcp.json
{
  "servers": {
    "filesystem-kb": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "D:\\valut\\trade\\agent"]
    }
  }
}
```

差异:`mcpServers` → `servers`。其他基本一致。

### 4. System Prompt

Claude Code 通过 `CLAUDE.md` 加载,全局或项目级。

Hermes 通过 agent config 的 `prompt_file` 加载,每个 agent 一份。

迁移:

```bash
# Claude Code:
#   复制到项目根 CLAUDE.md 或 ~/.claude/CLAUDE.md
# Hermes:
#   复制到 agent config 中的 prompt_file 路径
#   每个 agent 一份,不复用全局 prompt

cp ${KB_ROOT}/03-Prompts/claude-code-agent-prompt.md ~/.hermes/agents/kb-manager/prompt.md
```

### 5. Hooks

Claude Code 的 Hooks 系统 ↔ Hermes 的 middleware。

| Claude Code Hook | Hermes 等价 | 差异 |
|------------------|-------------|------|
| `PreToolUse` | middleware: `before_tool` | 触发时机一致 |
| `PostToolUse` | middleware: `after_tool` | 触发时机一致 |
| `SessionStart` | middleware: `on_session_start` | 一致 |
| `SessionEnd` | middleware: `on_session_end` | 一致 |
| `Notification` | middleware: `on_notify` | 一致 |

迁移示例(Claude Code):

```json
// ~/.claude/settings.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "echo 'About to run bash'"}]
    }]
  }
}
```

迁移到 Hermes:

```yaml
# ~/.hermes/config.yaml
middlewares:
  before_tool:
    - name: log_bash
      tool_matcher: bash
      action: log
```

### 6. 记忆

Claude Code 用 CLAUDE.md / 项目级 memory。Hermes 默认 ephemeral。

迁移:

```bash
# Claude Code CLAUDE.md → Hermes 长记忆
cp ~/.claude/CLAUDE.md ~/.hermes/memory/persistent.md

# Hermes 配置引用
echo "memory:
  long_term: file://~/.hermes/memory/" >> ~/.hermes/config.yaml
```

### 7. 权限配置

Claude Code 用 `permissions.allow/deny` 字段:

```json
{
  "permissions": {
    "allow": ["Read", "Glob", "Grep"],
    "deny": ["Bash(rm -rf:*)", "WebFetch"]
  }
}
```

Hermes 用工具 allowlist:

```yaml
# ~/.hermes/config.yaml
agents:
  kb-manager:
    tools:
      allow: [file_read, glob, grep]
      deny: [bash(rm -rf:*), web_fetch_internal]
```

迁移策略:

- `allow` → `allow`(直接转)
- `deny` → `deny`(直接转)
- Hermes 没有交互式审批 UI,**所以 deny 列表要更严格**

## 不兼容项清单

| 项 | Claude Code | Hermes | 处理 |
|----|-------------|--------|------|
| `/plugin install` | 命令 | 无 | 手动安装 |
| `/agents` 子代理 | 子进程 | 独立 agent + 消息 | 重构 |
| Hooks 系统 | 配置驱动 | middleware(YAML) | 重写 |
| IDE 集成(VSCode/JetBrains) | 完整 | 不支持 | 放弃 |
| 交互式审批 UI | 有 | 无 | 强化 deny 列表 |
| Plan mode | 有 | 无 | 用 spec 替代 |
| Skills vs Plugins | 区分 | 不区分(都是 skills) | 合并 |
| Context 压缩 | 自动 | 手动配置 | 调 middlewares |

## 工具替换关系

| Claude Code | Hermes | 备注 |
|-------------|--------|------|
| `Read` | `file_read` | 直接对应 |
| `Write` | `file_write` | 直接对应 |
| `Edit` | `file_edit` | 直接对应 |
| `Bash` | `bash` | Hermes 默认禁用,需 allowlist |
| `Glob` | `glob` | 直接对应 |
| `Grep` | `grep` | 直接对应 |
| `WebFetch` | `web_fetch` | Hermes 默认禁用 |
| `WebSearch` | `web_search` | Hermes 默认禁用 |
| `Task` (subagent) | 消息分发到独立 agent | 完全不同 |
| `TodoWrite` | `todo` (内置) | 直接对应 |
| MCP 工具 | MCP 工具 | 直接对应 |

## 迁移步骤

### 步骤 1:备份

```bash
# 备份当前 Claude Code 配置
$backup = "${env:USERPROFILE}\.claude_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Recurse "$env:USERPROFILE\.claude" $backup
Copy-Item "$env:USERPROFILE\.claude.json" "${backup}.json"
```

### 步骤 2:安装 Hermes

详见 [`../00-AgentBase/runtime/02-Hermes-Agent/02-安装部署.md`](../00-AgentBase/runtime/02-Hermes-Agent/02-安装部署.md)。

### 步骤 3:迁移 Skills

按上文 §1 的两种方式选一个。

### 步骤 4:迁移 Plugins

从 `02-Plugins/` 取适配器,把 skills/ 复制到 `~/.hermes/skills/`。

### 步骤 5:迁移 MCP

复制 `~/.claude.json` 的 mcpServers 到 `~/.hermes/mcp.json`,改 key 名为 `servers`。

### 步骤 6:迁移 Prompt

每个 Claude Code 项目级 CLAUDE.md → Hermes 一个 agent config:

```yaml
# ~/.hermes/agents/<project>.yaml
name: <project>
prompt_file: ~/.hermes/agents/<project>/prompt.md
tools:
  allow: [file_read, file_write, glob, grep, todo]
  deny: [bash(rm:*), bash(format:*)]
mcp_servers: [filesystem-kb, obsidian-kb]
```

### 步骤 7:迁移 Hooks

按上文 §5 表格转。

### 步骤 8:验证

对每个 agent 跑测试任务:

- [ ] 读 ${KB_ROOT} 文件 → 成功
- [ ] 写 01-Skills/ 新文件 → 成功
- [ ] 调 filesystem MCP → 成功
- [ ] 不允许的命令被拦截 → 确认拦截
- [ ] Cron 触发 → 确认执行

### 步骤 9:并行运行(推荐)

保留 Claude Code 1-2 周,与 Hermes 并行运行:

- 复杂开发任务 → Claude Code(交互式)
- 定时任务 → Hermes(cron)
- 消息处理 → Hermes

逐步把 Claude Code 任务迁过去。

## 回滚方案

如果迁移有问题:

```bash
# 1. 停 Hermes
Stop-Process -Name hermes -Force

# 2. 恢复 Claude Code 配置
Remove-Item -Recurse -Force "$env:USERPROFILE\.claude"
Move-Item "$backup" "$env:USERPROFILE\.claude"
Move-Item "${backup}.json" "$env:USERPROFILE\.claude.json"

# 3. 验证 Claude Code 还能用
claude --version
claude -c  # 恢复上次会话
```

## 验证清单

迁移后必须验证:

- [ ] 所有 skills 在 Hermes 中可被识别
- [ ] 所有 MCP server 在 Hermes 中可连接
- [ ] 每个 agent 的 system prompt 生效
- [ ] 权限 deny 列表生效(尝试 deny 的工具被拦截)
- [ ] Hooks/middleware 触发符合预期
- [ ] 长期记忆可写入、可读取、可删除
- [ ] Cron 任务按预期时间触发
- [ ] 消息接收 → 处理 → 回复 闭环正常
- [ ] 与 Claude Code 并行运行时无冲突(独立配置目录)

## 相关

- [`../00-AgentBase/runtime/02-Hermes-Agent/`](../00-AgentBase/runtime/02-Hermes-Agent/README.md) — Hermes 完整文档
- [`../00-AgentBase/runtime/03-ClaudeCode/`](../00-AgentBase/runtime/03-ClaudeCode/README.md) — Claude Code 完整文档
- [`../03-Prompts/hermes-agent-prompt.md`](../03-Prompts/hermes-agent-prompt.md) — Hermes 系统 prompt
- [`../05-Boundaries/`](../05-Boundaries/README.md) — 迁移后的边界规则