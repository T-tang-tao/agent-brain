# Claude Code Hooks 系统

> Claude Code 的生命周期钩子机制——在会话、轮次、工具调用等 20+ 关键节点自动执行自定义命令、HTTP 请求或 LLM 判断,实现硬约束与自动化。

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / runtime |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-09 |
| 作者 | Agent Knowledge Base Admin |
| 标签 | claude-code, hooks, lifecycle, automation |

---

## 什么是 Hooks

Hooks 是用户定义的 Shell 命令、HTTP 端点或 LLM prompt,在 Claude Code 生命周期的特定节点**自动执行**:

- 生命周期事件在固定节点触发
- matcher 过滤只处理关心的工具/场景
- handler 接收 JSON 输入,执行自定义逻辑

> 类比:Hooks 像 Git 的 pre-commit / post-merge 钩子——在固定生命周期点自动运行脚本。但 Claude Code 的 Hook 事件远比 Git 丰富(20+)。

## Hook 生命周期

```
事件触发 → matcher 过滤 → handler 运行(JSON 输入) → 决策输出
```

三层结构:事件决定**何时**触发,matcher 决定**是否**处理,handler 决定**做什么**。

## Hook 事件

20+ 生命周期事件,覆盖从会话到工具调用的全链路:

| 事件 | 触发时机 | 事件 | 触发时机 |
|------|----------|------|----------|
| `SessionStart` | 会话开始 | `TaskCompleted` | 任务完成 |
| `UserPromptSubmit` | 用户提交提示词 | `Stop` | Agent 停止(一轮结束) |
| `PreToolUse` | 工具调用前 | `StopFailure` | 停止失败 |
| `PermissionRequest` | 请求权限时 | `TeammateIdle` | 协作队友空闲 |
| `PostToolUse` | 工具调用成功后 | `InstructionsLoaded` | 指令加载完成 |
| `PostToolUseFailure` | 工具调用失败后 | `ConfigChange` | 配置变更 |
| `PermissionDenied` | 权限被拒绝时 | `CwdChanged` | 工作目录切换 |
| `Notification` | 发送通知时 | `FileChanged` | 文件变更 |
| `SubagentStart` | 子代理启动 | `PreCompact` | 上下文压缩前 |
| `SubagentStop` | 子代理停止 | `PostCompact` | 上下文压缩后 |
| `TaskCreated` | 任务创建 | `SessionEnd` | 会话结束 |
| `Elicitation` | 触发用户输入请求 | `ElicitationResult` | 用户输入返回结果 |
| `WorktreeCreate` | 创建 worktree | `WorktreeRemove` | 移除 worktree |

## 三种节奏

| 节奏 | 频率 | 典型事件 |
|------|------|----------|
| 每会话一次 | 每个会话 1 次 | `SessionStart` / `SessionEnd` |
| 每轮一次 | 每轮对话 1 次 | `UserPromptSubmit` / `Stop` |
| 每次工具调用 | 每次工具调用 1 次 | `PreToolUse` / `PostToolUse` |

> 类比:像三层闹钟——会话级是"上班打卡",轮次级是"每节课铃",工具级是"每次按键"。频率越高,handler 必须越轻量。

## 配置结构

三层嵌套:Hook 事件 → matcher 组 → handler 列表:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{ "type": "command", "command": "./scripts/pre-bash.sh" }]
    }]
  }
}
```

## Hook 配置位置

| 位置 | 作用域 |
|------|--------|
| `~/.claude/settings.json` | 用户级(跨所有项目) |
| `.claude/settings.json` | 项目级(提交到 git) |
| `.claude/settings.local.json` | 本地级(不提交) |
| Managed policy | 企业级强制 |
| 插件 `hooks/` 目录 | 插件提供 |
| Skill / Agent frontmatter | 技能或子代理内嵌 |

> 类比:像 nginx 配置的层叠——企业策略 > 用户全局 > 项目共享 > 本地覆盖,从宽到窄逐级叠加生效。

## Matcher 模式

matcher 决定 Hook 是否对当前工具调用生效:

| 模式 | 写法 | 匹配 |
|------|------|------|
| 全部 | `"*"` | 所有工具 |
| 精确匹配 | `"Bash"` | 仅 Bash 工具 |
| 列表匹配 | `"Bash\|Write\|Edit"` | 三者之一 |
| 正则匹配 | 含特殊字符时按正则解析 | 按正则规则 |

MCP 工具用 `mcp__<server>__<tool>` 格式,matcher 同样适用——`mcp__github__create_issue` 精确匹配,`mcp__.*__write.*` 正则匹配所有服务器的 write 类工具。

> 这个命名规范与 [MCP 集成](./08-MCP集成.md)的工具命名一致。

## 四种 Handler 类型

| 类型 | 字段值 | 执行方式 |
|------|--------|----------|
| **命令** | `type: "command"` | 执行 Shell 命令(JSON 通过 stdin 传入) |
| **HTTP** | `type: "http"` | 发送 HTTP 请求(JSON 作为 POST body) |
| **Prompt** | `type: "prompt"` | LLM 评估,返回 JSON 决策 |
| **Agent** | `type: "agent"` | 子代理评估,适合需工具调用的复杂判断 |

## Hook 输入与输出

| 退出码 | 含义 |
|--------|------|
| `0` | 允许,继续执行 |
| `2` | 阻止,拦截当前操作 |
| 其他 | 非致命错误,记录但继续 |

handler 也可返回 JSON 做决策控制:`{ "decision": "allow", "reason": "..." }`,decision 可为 `allow` / `deny` / `ask`。

## if 字段

`if` 用权限规则语法过滤触发条件:

```json
{ "if": "Bash(rm *)", "hooks": [...] }
```

表示"仅当 Bash 命令匹配 `rm *` 时"才触发。避免无关场景也触发 handler。

## PreToolUse 决策控制

PreToolUse 是最强大的 Hook——可在工具执行**前**做决策:

| 决策 | 效果 |
|------|------|
| `allow` | 允许工具调用 |
| `deny` | 阻止工具调用 |
| `ask` | 转为手动确认 |

这让"禁止删除生产数据库""禁止提交到 main 分支"等硬约束成为可能——不需要 Claude 自觉,而是系统级强制。

## Stop Hook

Stop Hook 在 Agent 一轮结束时触发:可向上下文**追加内容**(让 Claude 继续工作),或**阻止停止**(强制继续直到满足条件)。

> 类比:像"质检员"——产品下线前检查,不合格就退回流水线继续加工。

## 高级 Hook 类型

| 类型 | 说明 |
|------|------|
| **异步 Hook** | 标记为 async,在后台运行不阻塞主循环——适用于日志、通知等不依赖结果的操作 |
| **Prompt Hook** | `type: "prompt"`,把上下文交给 LLM 判断语义(如"提交信息是否规范"),返回 JSON 决策 |
| **Agent Hook** | `type: "agent"`,生成临时子代理审查当前操作(如"代码是否有漏洞"),适合需工具调用的复杂判断 |

## 安全考量

| 风险 | 说明 |
|------|------|
| **权限继承** | Hook 以用户权限运行,能做的事和用户一样多 |
| **输入校验** | 必须校验 stdin 的 JSON 输入,防止注入 |
| **命令注入** | 避免把未转义的用户输入拼进 Shell 命令 |
| **敏感数据** | Hook 输入可能含文件内容,注意日志脱敏 |

> Hooks 拥有与用户同等的权限——恶意 Hook 配置可造成与手动执行命令同等的破坏。安装第三方插件 Hook 时务必审查,详见 [权限与安全](./10-权限与安全.md)。

## 相关文件

- [Claude Code](./01-概述.md) — Hooks 在整体架构中的位置
- [Claude Code 配置体系](./03-配置体系.md) — Hook 配置文件位置
- [Claude Code 工具系统](./04-工具系统.md) — PreToolUse 控制工具调用
- [Claude Code 子代理系统](./07-子代理系统.md) — SubagentStart/Stop 事件与 agent 类 Hook
- [Claude Code 权限与安全](./10-权限与安全.md) — Hook 安全考量与权限分级
- [根目录 AGENTS.md](../../../AGENTS.md) — 部署、编排与管理指南
