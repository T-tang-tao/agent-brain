# Loop 设计模板

> 用这个模板设计一个 loop。三个版本:完整版(企业级)/ 最小版(个人)/ Yaml 配置(直接可执行)。

## 完整版(企业级,5 要素齐全)

```yaml
# loop-config.yaml
name: daily-triage-loop
description: 每天早上自动分诊 CI 失败、open issues、recent commits
owner: <你的名字>
created: 2026-07-10

# === 触发 ===
trigger:
  type: schedule
  schedule: "0 9 * * *"  # 每天早上 9 点
  timezone: Asia/Shanghai

# === 状态 ===
state:
  file: ./progress.md
  format: markdown
  atomic_write: true

# === 技能 ===
skills:
  - $triage-skill      # 调用 triage 技能
  - $code-review-skill # 必要时调用审查

# === 工作流 ===
workflow:
  - step: read_state
    action: 读 progress.md,获取昨日未完成项

  - step: discovery
    action: 调用 $triage-skill
    inputs:
      - ci_failures: last 24h
      - open_issues: priority>=P1
      - recent_commits: last 24h

  - step: prioritize
    action: 按 P1/P2/P3 排序,生成今日任务列表

  - step: process_items
    for_each: item in task_list
    parallel: true
    isolation: worktree
    sub_agents:
      - name: implementer
        model: sonnet
        role: 写修复或新功能
      - name: reviewer
        model: sonnet
        role: 对照 skills 审查产出

  - step: feedback_loop
    action: 验证 reviewer 通过才 commit
    validator:
      - "npm test 退出码 0"
      - "lint 退出码 0"

  - step: update_state
    action: 更新 progress.md

# === 停止条件 ===
stop_conditions:
  success:
    - "今日所有 P1 完成"
  failure:
    - "连续 3 次相同错误"
    - "reviewer 拒绝 > 5 次"
  limits:
    max_iterations: 20
    max_total_tokens: 1000000
    max_runtime_minutes: 120

# === 升级路径 ===
escalation:
  on_failure: write to triage inbox for human
  on_budget_exceeded: stop and notify
  on_unclear: ask user

# === 监控 ===
monitoring:
  log_to: ./loop.log
  notify_on_failure: true
  dashboard: optional
```

## 最小版(个人/单文件)

```yaml
name: my-loop
trigger:
  type: schedule
  schedule: "every 30 minutes"
state:
  file: progress.md
workflow:
  - step: 读 progress.md
  - step: 跑任务
  - step: 验证
  - step: 写回 progress.md
stop_conditions:
  - "测试通过"
  - "超过 10 次"
```

## 实际代码片段(Claude Code)

```bash
# 用 /goal 命令(可验证停止)
/goal "所有 npm test 通过且 lint 退出码 0"

# 用 /loop 命令(定时)
claude --loop "5m" "检查 CI failures,跑 triage"

# GitHub Actions(永久后台)
# .github/workflows/loop.yml
name: Daily Triage Loop
on:
  schedule:
    - cron: '0 9 * * *'
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            调用 $triage-skill,处理昨日 CI failures
            更新 progress.md
            把待处理项写进 Linear
```

## 实际代码片段(Codex TOML)

```toml
# .codex/agents/implementer.toml
name = "implementer"
description = "实施者:写代码"
instructions = """
你是实施者。读 progress.md,完成当前任务,写测试。
完成后交给 reviewer。
"""
model = "sonnet"
reasoning_effort = "high"

# .codex/agents/reviewer.toml
name = "reviewer"
description = "审查者:对照规范审"
instructions = """
你是审查者。读 implementer 的产出,对照 skills 规范审查。
只输出 PASS 或 FAIL + 原因。
"""
model = "sonnet"
```

## 实际代码片段(Hermes)

```python
# hermes-loop.py
import schedule, time

def run_loop():
    state = read_state('./progress.md')
    next_task = state.get('next_task')
    if not next_task:
        return
    
    # 实施
    result = sub_agent_a(next_task)
    
    # 审查
    if sub_agent_b(result) == 'PASS':
        update_state('./progress.md', done=next_task)
    else:
        update_state('./progress.md', retry=next_task)

schedule.every(30).minutes.do(run_loop)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 选择哪个版本

| 场景 | 用哪个 |
|------|--------|
| 5 人以下小团队 / 个人 | 最小版 |
| 10-50 人公司,日常任务 | 完整版 |
| 大型企业,关键生产任务 | 完整版 + 完整监控 + 多人 review |

## 实施 checklist

部署前:

- [ ] trigger 已测试(手动跑一次看是否启动)
- [ ] state 文件路径可写
- [ ] stop conditions 已验证可触发
- [ ] escalation 路径清晰
- [ ] 监控/日志已配

部署后第一周:

- [ ] 每天 review 一次输出
- [ ] 验证 token 成本符合预期
- [ ] 收集失败案例,调整 stop conditions
- [ ] 调优 priority 排序

持续:

- [ ] 每月审查一次 loop 是否仍合适
- [ ] 用户是否还读产物(comprehension debt 检测)
- [ ] 团队纪律是否在(认知投降检测)