# Claude Code 专题

> Anthropic 官方 Agentic 编码工具——终端、IDE、桌面、Web 多表面运行时。

本目录是 Claude Code 的完整认知库,基于 [官方文档](https://code.claude.com/docs/en/overview) 和 [GitHub 仓库](https://github.com/anthropics/claude-code) 编写。

## 文档列表

| 编号 | 文档 | 主题 |
|------|------|------|
| 01 | [概述](./01-概述.md) | Claude Code 是什么?核心特性、多表面架构、四大定制机制 |
| 02 | [安装部署](./02-安装部署.md) | 系统要求、安装方式、认证、更新、版本管理 |
| 03 | [配置体系](./03-配置体系.md) | 配置作用域、settings.json、权限规则、环境变量 |
| 04 | [工具系统](./04-工具系统.md) | 内置工具列表、权限规则语法、工具行为 |
| 05 | [技能系统](./05-技能系统.md) | SKILL.md 格式、frontmatter、动态上下文注入、内置技能 |
| 06 | [记忆系统](./06-记忆系统.md) | CLAUDE.md 文件、Auto Memory、.claude/rules/ 规则 |
| 07 | [子代理系统](./07-子代理系统.md) | 内置子代理、自定义子代理、前台/后台、会话分叉 |
| 08 | [MCP 集成](./08-MCP集成.md) | 四种传输、三种作用域、OAuth、Tool Search |
| 09 | [Hooks 系统](./09-Hooks系统.md) | 26 个生命周期事件、四种处理器类型、决策控制 |
| 10 | [权限与安全](./10-权限与安全.md) | 六种权限模式、权限规则、受保护路径、托管安全 |
| 11 | [IDE 与平台集成](./11-IDE与平台集成.md) | 终端/VS Code/JetBrains/桌面/Web/移动端/CI-CD |
| 12 | [架构设计](./12-架构设计.md) | Agentic 循环、系统提示组装、上下文管理、数据流 |

## 推荐阅读顺序

1. **[概述](./01-概述.md)** — 建立全局认知
2. **[安装部署](./02-安装部署.md)** — 安装 Claude Code
3. **[配置体系](./03-配置体系.md)** — 理解配置结构
4. **[架构设计](./12-架构设计.md)** — 理解内部运作
5. 按需阅读专题文档(工具/技能/记忆/子代理/MCP/Hooks/权限)

## 上级目录

- [Agent 运行时与 CLI](../01-Agent运行时与CLI.md) — Runtime / Harness / CLI 通用概念
- [Runtime 目录](../README.md) — Runtime 模块总览
- [Hermes Agent 专题](../02-Hermes-Agent/README.md) — 另一个 Runtime 实例
