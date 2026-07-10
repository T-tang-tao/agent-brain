# Runtime 多 Agent 使用指南

> 本文件讲**怎么用**多 Agent,不是讲差异。
>
> 包含两部分:
> 1. **同一个 Runtime 内**:怎么调用内置子代理 + 怎么自定义子代理
> 2. **跨 Runtime 协作**:不同 Runtime 怎么配合(共享文件、共享 Prompt、MCP 桥接)
>
> 各 Runtime 子代理机制的细节已在对应专题文档中说明,本文件聚焦**动手**。

---

## 0. 一句话总览

| Runtime | 多 Agent 机制 | 关键命令/文件 |
|---------|--------------|---------------|
| **Claude Code** | Subagents | `.claude/agents/<name>.md` |
| **Codex CLI** | Subagents(实验) | `~/.codex/config.toml` 启用 `multi_agent = true` |
| **Hermes Agent** | `delegate_task` 工具 | 直接调用工具 |

**核心结论**:已经用了哪个 Runtime,就先用哪个 Runtime 的多 Agent 能力——零额外成本。

---

# 第一部分:同一个 Runtime 内使用多 Agent

## 1. Claude Code 子代理(最成熟)

### 1.1 零配置使用:让 Claude Code 自动选

直接告诉 Claude Code,**Claude Code 会按 description 自动匹配最合适的子代理**:

> "用 Explore 找出这个项目里所有调用 Stripe API 的地方"
>
> "用 general-purpose 子代理并行研究 3 个方案的优劣"
>
> "调研完成后用 Plan 子代理做架构设计"

### 1.2 创建自定义子代理(项目级)

**步骤 1**:创建目录
```bash
mkdir -p .claude/agents
```

**步骤 2**:创建文件 `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: 审查代码变更,重点关注安全和性能。涉及代码 review、安全审查、PR 检查时使用。
tools: [Read, Grep, Glob]
disallowedTools: [Bash]
model: sonnet
permissionMode: plan
memory: true
---

你是资深代码审查专家。重点关注:
1. 安全漏洞(SQL 注入、XSS、命令注入)
2. 性能瓶颈(N+1 查询、内存泄漏)
3. 代码可维护性(命名、复杂度、重复)
```

**字段说明**(全部可选,未指定则继承父级):

| 字段 | 用途 |
|------|------|
| `name` | 子代理唯一标识(必填) |
| `description` | 触发条件描述,Claude 用它决定何时调用 |
| `tools` | 工具白名单(只允许这些) |
| `disallowedTools` | 工具黑名单(禁止这些,**优先级高于白名单**) |
| `model` | 指定模型(haiku/sonnet/opus/inherit) |
| `permissionMode` | inherit/plan/default/acceptEdits |
| `memory` | true = 跨会话持久记忆 |
| `background` | true = 后台运行(默认 v2.1.198+) |
| `maxTurns` | 最大轮次 |
| `skills` | 预加载技能列表 |
| `mcpServers` | 允许的 MCP 服务器 |

**步骤 3**:测试

直接在 Claude Code 中说:

> "用 code-reviewer 审查 src/payment.py"

Claude Code 会:
1. 匹配 `description` 中的"代码审查"
2. 加载子代理定义
3. 在**独立上下文**中执行
4. 只返回摘要给主对话

### 1.3 创建子代理(用户级,跨项目)

把文件放在 `~/.claude/agents/` 而不是 `.claude/agents/`——所有项目都能用。

### 1.4 完整工作流示例

场景:**新功能开发 + 代码审查**

```bash
# 项目根目录
mkdir -p .claude/agents
```

`.claude/agents/code-reviewer.md`(只读审查):
```yaml
---
name: code-reviewer
description: 审查代码变更,关注安全和性能
tools: [Read, Grep, Glob, Bash]   # 允许 bash 因为 git diff
model: sonnet
permissionMode: default            # 询问后再编辑
---
```

`.claude/agents/test-runner.md`(跑测试):
```yaml
---
name: test-runner
description: 跑测试套件,返回失败摘要
tools: [Bash, Read]
model: haiku                       # 简单任务用便宜模型
background: true                   # 后台跑,不阻塞主对话
---
```

主对话工作流:
> 1. 写代码
> 2. "用 test-runner 跑测试"
> 3. "用 code-reviewer 审查我的改动"
> 4. 根据反馈修复

### 1.5 常用模式

| 模式 | 配置 | 用途 |
|------|------|------|
| **隔离高量输出** | `tools: [Read]` + `background: true` | 日志分析、跑测试 |
| **只读审查** | `permissionMode: plan` | 安全审计、PR review |
| **便宜搜索** | `model: haiku` | 简单 grep、文件查找 |
| **嵌套分工** | 子代理 A 调用子代理 B | 复杂任务层层分解 |
| **Fork 探索** | 显式 Fork 当前对话 | 在分支上实验方案 |

**禁用**:
- 禁用特定子代理:`permissions.deny` 加 `Agent(code-reviewer)`
- 禁用全部:禁用 Agent 工具

---

## 2. Codex CLI 子代理(实验性)

### 2.1 启用配置

编辑 `~/.codex/config.toml`:

```toml
[features]
multi_agent = true    # 启用多 Agent 功能
```

⚠️ **实验性功能**,API 可能变化。生产环境慎用。

### 2.2 使用

启用后,Codex 主 Agent 会**自动**对子任务委派给子 Agent。无需特殊命令。

如需主动让 Codex 委派,在 Prompt 中显式说:

> "用子代理并行调研 3 个方向,完成后报告"

### 2.3 适用场景

| 场景 | 说明 |
|------|------|
| 并行任务 | 多个子 Agent 同时处理独立任务 |
| 上下文隔离 | 子任务不污染主对话 |
| 专业化 | 不同子 Agent 配置不同工具集 |

**完整文档**:[Codex 自定义与技能 - Subagents](./04-Codex-CLI/06-自定义与技能.md#subagents)

---

## 3. Hermes Agent 委托

### 3.1 机制

通过 `delegate_task` 工具把任务委托给子 Agent。子 Agent 在独立上下文中运行,完成后返回结果。

### 3.2 使用方式

```python
# Hermes Agent 配置
tool_sets:
  - delegation    # 启用子代理委托
```

主 Agent 在需要时**直接调用** `delegate_task` 工具:

```python
result = delegate_task(
    task="分析最近一周的错误日志",
    agent_id="log-analyzer"   # 可选,指定哪个子 Agent
)
```

### 3.3 适用场景

- **并行工作流**:多个独立子 Agent 同时跑
- **零上下文成本**:把多步管道压缩成单轮调用(通过 Python 脚本调用 RPC)
- **任务规划**:配合 `todo`、`clarify` 做端到端流程

**完整文档**:[Hermes 工具与工具集 - Agent 编排](./02-Hermes-Agent/04-工具与工具集.md#agent-编排)

---

# 第二部分:跨 Runtime 协作

> 何时需要跨 Runtime:
> - 同一个项目,不同阶段用不同 Runtime(如开发用 Claude Code,部署用 Hermes)
> - 不同 Runtime 各有所长,想组合使用
> - 项目跨团队,有人用 Claude Code 有人用 Codex

## 4. 跨 Runtime 协作的四种方式

| 方式 | 适用 | 复杂度 |
|------|------|--------|
| **共享文件** | 用文件系统传递状态 | 低 |
| **共享 Prompt** | 通过 git 同步共享 `AGENTS.md` 等指令 | 低 |
| **共享 MCP Server** | 同一个 MCP server 给多个 Runtime 接入 | 中 |
| **混合编排** | Runtime A 调用 Runtime B(用 RPC) | 高 |

## 5. 方式 1:共享文件(最简单)

**思路**:不同 Runtime 通过读写同一组文件,完成状态交接。

```
Claude Code 写入 .trae/state.json
        ↓
   (文件系统)
        ↓
Hermes Agent 读取 .trae/state.json
        ↓
  Hermes 继续处理
```

**实施**:
1. 定义一份交接 schema(如 `.trae/state.json`)
2. Runtime A 写完任务后,导出到这份 schema
3. Runtime B 启动时,读取这份 schema,继续工作

**适用场景**:
- 长时间任务分多阶段,每阶段换 Runtime
- 开发 → 部署:Claude Code 完成后,Hermes 接力做 CI/CD

## 6. 方式 2:共享 Prompt(中等)

**思路**:用 git 管理项目级指令文件,所有 Runtime 都能引用。

**实施**:
1. 仓库根放 `AGENTS.md`(或 `CLAUDE.md` / `.codex/AGENTS.md`)
2. 所有 Runtime 都读这份文件(根据各自约定)
3. 团队成员改文件 → git push → 所有 Runtime 下次启动时自动获取最新版本

**关键文件对应**:

| Runtime | 默认读取 | 优先级 |
|---------|----------|--------|
| Claude Code | `CLAUDE.md` 或 `AGENTS.md` | 项目根 + 父目录 |
| Codex CLI | `AGENTS.md` | 项目根 |
| Hermes Agent | 系统提示配置 | 项目级配置文件 |

**建议**:用 `AGENTS.md`(通用),同时为 Claude Code 保留 `CLAUDE.md`(Anthropic 习惯)。

## 7. 方式 3:共享 MCP Server(强大)

**思路**:多个 Runtime 都连接同一个 MCP server,共享工具能力。

```
Claude Code ─┐
Codex CLI  ─┼─→ 同一个 MCP server ─→ 数据库 / API / 工具
Hermes     ─┘
```

**实施**:
1. 部署 MCP server(如 `mcp-filesystem`、`mcp-postgres`)
2. 在每个 Runtime 中配置连接:

**Claude Code**:`~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "shared-db": {
      "command": "mcp-postgres",
      "args": ["--dsn", "postgresql://..."]
    }
  }
}
```

**Codex CLI**:`~/.codex/config.toml`:
```toml
[mcp_servers.shared-db]
command = "mcp-postgres"
args = ["--dsn", "postgresql://..."]
```

**Hermes**:见 `runtime/02-Hermes-Agent/06-MCP集成.md`

**好处**:
- 一次部署,所有 Runtime 都能用
- 工具行为一致,跨 Runtime 结果可对比
- 容易切换 Runtime

## 8. 方式 4:混合编排(高级)

**思路**:一个 Runtime 作为"主管",通过 RPC/HTTP 调用其他 Runtime。

```
┌──────────────┐
│  Claude Code │ (主管,负责规划)
└──────┬───────┘
       │ 调用 API
       ▼
┌──────────────┐
│  Codex CLI   │ (执行者,做代码审查)
└──────────────┘
```

**实施**:
1. 启动 Codex CLI 的 API 模式(`codex serve`)
2. Claude Code 用 `WebFetch` 工具调用 Codex API
3. 互相交换任务和结果

**适用场景**:
- Claude Code 规划,Codex 执行代码审查
- Hermes 做定时任务,Claude Code 临时介入复杂任务

**注意**:
- 需要两边都开 API 服务
- 网络/进程管理变复杂
- 仅在确实需要时使用

## 9. 跨 Runtime 协作的反模式

| 反模式 | 后果 | 替代 |
|--------|------|------|
| 同一项目同时跑两个 Runtime 监控同一文件 | 冲突 | 用 git 分支隔离 |
| 各 Runtime 用各自的 AGENTS.md 不共享 | 行为不一致 | 共享 `AGENTS.md`,Runtime-specific 用 `CLAUDE.md` 之类 |
| 用 RPC 让 Runtime 频繁互相调用 | 网络开销爆炸 | 批量调度,减少调用次数 |
| 在一个 Runtime 里调用另一个 Runtime 的子代理 | 维护噩梦 | 用 MCP 统一工具,不要调用 Runtime |

## 10. 何时不要跨 Runtime

| 场景 | 建议 |
|------|------|
| 个人项目,只用一个 Runtime | 不要折腾 |
| 团队成员各用各的,但任务独立 | 共享 MCP 即可 |
| 任务需要 Runtime 间的频繁状态同步 | 用更上层编排框架(LangGraph、AgentScope) |
| 生产级多租户 | 直接用 AgentScope |

**核心原则**:**一个 Runtime 能解决就用一个 Runtime。** 跨 Runtime 是高级选项,不是默认选项。

---

# 第三部分:搭建检查清单

## 11. 单 Runtime 搭建清单

### 11.1 Claude Code
- [ ] 决定要建哪些自定义子代理(每个子代理一个职责)
- [ ] 在 `.claude/agents/` 创建子代理定义文件
- [ ] 每个子代理写明 `description`(触发条件)+ `tools`(权限范围)
- [ ] 关键子代理设独立模型(简单任务用 haiku)
- [ ] 测试:让 Claude Code 调用,验证独立权限和上下文隔离
- [ ] 配置 Hooks(`SubagentStart` / `SubagentStop`)做日志/审计
- [ ] 按需禁用不需要的 Runtime 默认技能

### 11.2 Codex CLI
- [ ] 在 `~/.codex/config.toml` 启用 `multi_agent = true`
- [ ] 接受"实验性"标注,生产环境慎用
- [ ] 测试:让 Codex 委派子 Agent,观察隔离效果

### 11.3 Hermes Agent
- [ ] 启用 `delegation` 工具集
- [ ] 必要时编写 Python 脚本通过 RPC 调用
- [ ] 测试:用 `delegate_task` 工具

## 12. 跨 Runtime 搭建清单

- [ ] 明确协作模式(共享文件 / 共享 Prompt / MCP / 混合编排)
- [ ] 定义交接 schema(如 `.trae/state.json`)或共享 `AGENTS.md`
- [ ] 部署 MCP server,在各 Runtime 配置连接
- [ ] 测试:在 Runtime A 触发 → Runtime B 接收 → 状态正确
- [ ] 配置网络/进程管理(如果是混合编排)
- [ ] 监控:看 trace 日志,确保交接无误

---

## 相关文件

### 本模块

- [Agent 运行时与 CLI 综述](./01-Agent运行时与CLI.md)
- [Runtime README](./README.md)

### 各 Runtime 子代理使用文档

- [Claude Code 子代理系统(完整)](./03-ClaudeCode/07-子代理系统.md)
- [Claude Code 工具系统 - Agent 工具](./03-ClaudeCode/04-工具系统.md)
- [Codex 自定义与技能 - Subagents](./04-Codex-CLI/06-自定义与技能.md#subagents)
- [Hermes 工具与工具集](./02-Hermes-Agent/04-工具与工具集.md)

### 相关知识

- [如何编写 Skill](../../behavior/01-如何编写Skill.md)
- [跨 Runtime 技能管理](../../behavior/02-跨Runtime技能管理.md)
- [规划循环](../../behavior/03-规划循环(Planner).md)
- [根目录 AGENTS.md - 部署、编排与管理](../../../AGENTS.md)

---

> **维护责任人**:Agent Knowledge Base Admin
> **最后更新**:2026-07-10
> **版本**:v1.0.0(从"对比"改为"使用",聚焦动手)