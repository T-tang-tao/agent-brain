# Agent 运行时与 CLI

## 一句话解释

Agent Runtime / Harness / CLI 是把模型连接到工具、文件系统、命令行、权限系统和上下文管理的运行环境。

Claude Code CLI、Codex CLI、Hermes Agent 这类工具，本质上不是模型本身，而是 Agent 的运行时或宿主环境。

## 什么是 Agent Runtime

Agent Runtime 是 Agent 真正运行的环境。

它负责：

- 把用户任务传给模型；
- 给模型提供上下文；
- 暴露可用工具；
- 执行模型请求的工具调用；
- 管理权限；
- 保存对话状态；
- 控制什么时候继续、什么时候停止；
- 处理错误和验证结果。

可以把 Runtime 理解为：

```text
模型的大脑之外，负责身体、手脚、规则和工作台的部分。
```

## 什么是 Agent Harness

Harness 是“代理运行壳”。

它把模型包装成可执行系统：

```text
Model + Tools + Context + Loop + Permissions = Agent Harness
```

很多 Agent 产品的差异，不只在模型，而在 harness。

## 什么是 Agent CLI

Agent CLI 是在命令行里运行的 Agent Runtime。

它通常能：

- 读取项目文件；
- 搜索代码；
- 修改文件；
- 执行 shell 命令；
- 运行测试；
- 调用 MCP 或内置工具；
- 请求用户确认高风险操作；
- 维护上下文；
- 输出任务进度和结果。

## Agent CLI 的本质公式

```text
Agent CLI = Model + Toolset + Filesystem Access + Shell + Context Manager + Permission System + UI
```

其中：

| 组成 | 说明 |
|---|---|
| Model | 负责理解和推理 |
| Toolset | 允许 Agent 读取、编辑、搜索、执行 |
| Filesystem Access | 访问本地项目或工作目录 |
| Shell | 执行命令、测试、构建 |
| Context Manager | 管理长对话、文件内容、历史状态 |
| Permission System | 控制危险操作是否需要确认 |
| UI | 命令行、IDE、Web、桌面应用等交互界面 |

## 为什么同一个模型在不同 CLI 表现不同

同一个模型在不同 Agent CLI 中表现可能很不一样，因为 runtime 不同。

差异可能来自：

- 工具数量不同；
- 工具 schema 不同；
- 文件搜索能力不同；
- 上下文压缩方式不同；
- 权限策略不同；
- 是否支持 Skill；
- 是否支持 MCP；
- 是否支持子 agent；
- 是否自动运行测试；
- 是否能保留长期记忆。

所以不能只问“用了什么模型”，还要问：

```text
这个 Agent 运行在哪个 runtime 里？它有哪些工具？边界是什么？上下文怎么管理？
```

## Agent CLI 和普通聊天界面的区别

| 维度 | 普通聊天界面 | Agent CLI |
|---|---|---|
| 主要能力 | 对话和生成 | 对话 + 工具执行 |
| 文件访问 | 通常有限 | 通常可读写项目文件 |
| 命令执行 | 通常没有 | 通常可执行 shell 命令 |
| 任务循环 | 较弱 | 较强 |
| 权限系统 | 简单 | 更重要 |
| 适合任务 | 问答、写作、解释 | coding、迁移、调试、自动化 |

## 迁移时要关注什么

当把一个 agent 从一个环境迁移到另一个环境时，不要只迁移 prompt。

还要确认：

- 工具是否等价；
- 权限策略是否等价；
- skill 是否能迁移；
- MCP 是否可用；
- 文件系统路径是否相同；
- shell 命令是否相同；
- 上下文管理方式是否不同；
- 记忆和知识库是否能被新 agent 读取。

## 相关文件

- [[../01-AgentBase总览]]
- [[../02-概念全景辨析]]
- [[../03-知识地图]]
- [[../safety/01-Agent边界与限制]]
- [Hermes Agent 专题](./02-Hermes-Agent/01-概述.md) — Hermes Agent 完整认知
- [Claude Code 专题](./03-ClaudeCode/README.md) — Claude Code 完整认知
