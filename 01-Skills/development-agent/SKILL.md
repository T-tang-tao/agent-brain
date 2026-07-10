---
name: development-agent
description: >
  Use when working as a development-focused coding agent in a real repository: onboarding a project, clarifying requirements, implementing code changes, reviewing code, or verifying changes. Emphasizes reading context first, minimal changes, contract safety, data isolation, caching, concurrency, generated-code boundaries, and validation.
version: 1.0.0
---

# development-agent — 开发型 Agent 工作协议

## When to Use

- 用户要求从项目中提炼开发规范、补充开发型知识库或资产。
- 用户要求在真实代码库中实现、修复、排查或评审代码。
- 用户要求编写项目级 `AGENTS.md`、开发提示词、开发检查清单。
- 任务涉及接口契约、数据库、缓存、权限、并发、生成代码或验证流程。

## Procedure

1. 先读取项目级规则:根 `AGENTS.md`、子项目 `AGENTS.md`、README、启动和测试说明。
2. 提炼长期稳定事实:项目定位、目录结构、技术栈、模块边界、启动命令、验证命令。
3. 区分三类内容:
   - 项目基线:长期规则和边界。
   - 任务提示词:实现、澄清、评审、排查。
   - 落地清单:新项目接入和资产维护步骤。
4. 执行开发任务时按调用链读代码,优先复用现有模式,只做最小改动。
5. 修改前显式检查风险:接口契约、数据隔离、SQL 注入、缓存失效、并发幂等、审计日志、生成代码。
6. 修改后运行相关验证;无法验证时说明原因。
7. 输出变更内容、修改原因、验证结果和剩余风险。

## Development Checklist

- [ ] 已阅读目标模块及相邻实现。
- [ ] 已确认可改目录和禁止修改目录。
- [ ] 已确认自动生成文件是否禁止手改。
- [ ] 已确认接口契约是否变化。
- [ ] 已确认数据隔离字段或权限范围是否完整。
- [ ] 已确认缓存、锁、队列、任务调度是否受影响。
- [ ] 已确认测试、构建、lint 或最小验证方式。

## Prompt Assets

- [开发任务执行 Prompt](../../03-Prompts/development-task-execution-prompt.md)
- [开发需求澄清 Prompt](../../03-Prompts/development-requirement-clarification-prompt.md)
- [开发代码评审 Prompt](../../03-Prompts/development-code-review-prompt.md)
- [开发项目基线 Prompt](../../03-Prompts/development-project-baseline-prompt.md)

## Knowledge

- [开发型 Agent 工作协议](../../00-AgentBase/behavior/07-开发型Agent工作协议.md)
- [如何编写 AGENTS.md](../../00-AgentBase/knowledge/04-如何编写AGENTS.md)
- [如何编写 Skill](../../00-AgentBase/behavior/01-如何编写Skill.md)
- [规划循环](../../00-AgentBase/behavior/03-规划循环(Planner).md)
