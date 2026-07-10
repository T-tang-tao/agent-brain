# 文件系统 Context(Filesystem-Based Context)

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | filesystem, scratchpad, offloading, handoff, just-in-time |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

Context window 是有限的,任务往往需要超出窗口的信息。**用文件系统当 context 的"溢出层"** —— 写一次、持久存、按需取,作为统一接口应对任意规模。

---

## 1. 为什么是文件系统,不是 RAG/KG

| 方案 | 优势 | 代价 |
|---|---|---|
| 全塞 context | 实现最简单 | 必爆 |
| RAG(向量检索) | 语义匹配 | 丢失结构;关系信息丢;调 embedding 难 |
| Knowledge Graph | 保留结构关系 | 大量工程投入 |
| **Filesystem + grep/glob** | 通用接口、保留原文、Agent 可理解 | 依赖 Agent 知道何时去取 |

> **核心原则**:**保留索引,不复制内容**。强标识符(如 `customer_pricing_rates.json`)比弱标识符(`data/file1.json`)对 Agent 友好得多。

---

## 2. 四大 Context 失败模式与文件系统对策

| 失败模式 | 描述 | 文件系统对策 |
|---|---|---|
| **Missing context**(信息缺失) | 需要的上下文不在可见窗口 | 持久化工具输出和中间结果到文件 |
| **Under-retrieved context**(取少了) | 取到的内容没包含所需信息 | 文件结构化:grep 友好格式、清晰 section header |
| **Over-retrieved context**(取多了) | 远超需要,浪费 token + 降级注意力 | 把大量内容挪到文件,只回传紧凑引用 |
| **Buried context**(埋深了) | 信息分散在很多文件里,不好找 | glob(结构) + grep(精确) + 语义搜索(概念)组合 |

---

## 3. 静态 vs 动态 Context 的权衡

**静态 context**(system prompt / 工具定义 / 关键规则) = 昂贵资产:

- 每次 turn 都占 token,与任务相关性无关
- Agent 能力越多,静态 context 越长,越挤占动态信息空间

**动态发现**(dynamic discovery)原则:

- 静态里只放最少的指针(name、一句话描述、文件路径)
- 用搜索工具按需加载完整内容
- 更省 token,通常响应质量也更高(减少 context 中的矛盾和无关信息)

**取舍**:动态发现依赖模型自己判断"什么时候该取更多"。前沿模型做得不错,弱模型可能不会触发加载。**有疑问时,关键安全/正确性约束放静态**。

---

## 4. 五大 Filesystem Pattern

### 4.1 Filesystem as Scratch Pad(草稿纸)

**场景**:单次 web search / DB query 就能把几千 token 倒进 message history,持续占用整个会话。

**做法**:

1. 把原始输出写到 scratch 文件
2. 提取简短摘要(200 token 以内)
3. 返回 `[Output written to path. Summary: ...]`
4. Agent 用 grep 搜索或 read_file 限定行范围取所需

```python
def handle_tool_output(output, threshold=2000):
    if len(output) < threshold:
        return output
    path = f"scratch/{tool}_{ts}.txt"
    write_file(path, output)
    return f"[Output written to {path}. Summary: {extract_summary(output, 200)}]"
```

**关键**:用 grep 按 pattern 搜索 + read_file 按行范围取 — 既保留原文备查,又只在 active context 留 ~100 token。

### 4.2 Plan Persistence(计划持久化)

**场景**:长时任务,计划随 context 漂移或被总结掉,Agent 偏离目标。

**做法**:把计划写成 YAML,既能读又能解析:

```yaml
# scratch/current_plan.yaml
objective: "Refactor authentication module"
status: in_progress
steps:
  - id: 1
    action: "Audit current JWT handling"
    status: completed
  - id: 2
    action: "Extract token service"
    status: in_progress
```

Agent 任何时刻重读计划 → 恢复对目标和进度的感知。

### 4.3 Sub-Agent Communication(子代理通信)

**场景**:Supervisor/Worker 多 Agent 架构,worker 之间需要共享信息,但不应有直接消息传递。

**做法**:用共享文件当通信媒介。

- Worker 写中间结果到 `shared/task_N.yaml`
- Supervisor 读取并更新 `shared/state.json`
- 避免把 worker 的全部 context 复制到 supervisor

### 4.4 Dynamic Skill Loading(动态技能加载)

**场景**:几十个 skill 候选,但当前任务只需要 1-2 个。

**做法**:

- 启动时只加载所有 skill 的 name + description 到 context
- 被触发时再加载完整 SKILL.md
- 不用预加载全部 — 浪费 token

### 4.5 Just-In-Time Discovery(即时发现)

**场景**:Agent 不知道自己要什么,需要根据当前问题动态查找相关文件。

**做法**:

- 强命名约定 + 清晰目录结构
- `ls` / `glob` 找候选
- `grep` 按关键字锁定
- `read_file` 限定行范围取目标

---

## 5. 路径与命名约定

| 模式 | 例子 | 适用 |
|---|---|---|
| 强命名 | `customer_pricing_rates.json` | 关键文件,Agent 应能凭名字找到 |
| 弱命名 | `data/file1.json` | 临时 / 内部用 |
| 时间戳 | `scratch/search_2026-07-10.txt` | 一次性工具输出 |
| 版本号 | `plan_v2.yaml` | 计划、配置迭代 |
| 任务 ID | `shared/task_NNN.yaml` | 多 Agent 共享 |

---

## 6. 清理策略

Filesystem 不是垃圾桶,**需要清理规则**:

- **临时 scratch**:任务结束或超过 N 天自动清理
- **共享文件**:任务完成 → 归档到 `archive/YYYY-MM/`
- **日志**:append-only,定期 rotate
- **版本**:旧 plan 留作历史,不删除(可能用于回溯)

---

## 7. 与其他章节的关系

- **09-Context-Engineering.md**:Filesystem 是 context 优化的物理实现层
- **11-Multi-Agent-Patterns.md**:Sub-agent 通信靠 shared files
- **04-记忆机制(Memory).md**:跨 session 持久化用 memory;同 session 大容量用 filesystem
- **13-Harness-Engineering.md**:Append-only 日志 + scratchpad 是 harness 表面分类的具体形态

---

## 8. 工程化检查清单

- [ ] 工具输出超过阈值(默认 2000 token)是否写入文件 + 返回摘要?
- [ ] 关键文件用强命名,Agent 不需要 search 也能定位?
- [ ] 长任务计划是否持久化到 YAML/JSON?
- [ ] Sub-agent 之间用 shared files 通信,而不是直接传递 context?
- [ ] Skill / 文档按 progressive disclosure 加载,不全量预载?
- [ ] 临时文件有清理策略(任务结束 / 超期)?
- [ ] 共享文件有归档规则,不是无限增长?
- [ ] grep-friendly 格式优先(行号、独立 sections)?

---

## 9. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| Web search 5MB 输出 | 全部塞 message history | 写文件,返回 200 token 摘要 + 路径 |
| 长任务 200 步 | 计划只在 context 里 | 写 `plan.yaml`,每步重新读 |
| 10 个 worker 并行 | 都把结果发给 supervisor | 写 `shared/task_N.yaml`,supervisor 按需取 |
| 50 个 skill | 全量加载到 context | 启动只加载 name + description |
| 找日志里的错误 | 全文读 10MB 文件 | grep "ERROR" → 行号 → read_file 限定行 |

---

## 10. 相关知识

- [上下文工程总论](./09-Context-Engineering.md)
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)
- [记忆机制](./04-记忆机制(Memory).md)
- [Harness 工程](./13-Harness-Engineering.md)