# Agent 评估方法(Evaluation)

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v2.0.0 |
| 创建 | 2026-07-09 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼 + 旧版评估体系) |
| 标签 | evaluation, rubric, llm-as-judge, regression, monitoring, quality-gate |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) · 上一版(2026-07-09) |

---

## 一句话理解

Agent 评估 ≠ 传统软件测试。Agent 路径非确定、可能多条都对,核心是**评估"产出"而非"路径"** — 用多维 rubric + 确定性检查 + LLM-as-judge + 持续监控组合,任何一项不能替代其他。

---

## 1. 核心原则

| 原则 | 含义 |
|---|---|
| **Outcome over path** | Agent 可能走不同路径都到正确答案,评结果不评步骤 |
| **Multi-dimensional rubrics** | 一维分数掩盖关键失败,各维度独立打分 |
| **Deterministic first** | 有机器可检结构先跑确定性检查,再让 LLM judge |
| **Model-judged after stable** | 确定性检查 + rubric 稳定后才用 LLM-as-judge |
| **Realistic budgets** | 用生产级 token / tool call 预算评估,不用无限资源 |

**关键发现**:token 用量、tool 调用次数、模型选择 = 性能方差的主要驱动。**模型升级往往比加 token 收益更大**。

---

## 2. 五大评估挑战

| 挑战 | 表现 | 对策 |
|---|---|---|
| **非确定性** | 同一 query 两次结果不同 | 多次运行取分布 |
| **多有效路径** | 3 步 vs 10 步都到正确 | 评结果不评步骤 |
| **Context 依赖失败** | 简单成功,复杂失败 | 简单 / 中 / 复杂 / 极复杂全覆盖 |
| **维度间不平衡** | 准确率高但效率低 | 多维独立打分,加权聚合 |
| **评分体系游戏化** | 优化评分而非真实目标 | 多维 + 独立 verifier |

---

## 3. 评估方法组合

### 3.1 确定性检查(Deterministic Checks)

**先用** — 快、便宜、客观、可解释。

适用:
- Schema 有效性
- 重复 key 检测
- Rubric 数学一致性(权重和 = 1?)
- Manifest 同步状态
- 必填证据路径存在
- 检索状态码

**失败即快速熔断**,不让 LLM judge 在错误结构上浪费 token。

### 3.2 多维 Rubric(Multi-Dimensional Rubrics)

**核心维度**(权重按用例调整):

| 维度 | 适用 |
|---|---|
| 事实准确性 | 知识类任务(权重高) |
| 完整性 | 研究类任务(权重高) |
| 引用准确性 | 信任敏感场景 |
| 来源质量 | 权威性输出 |
| 工具效率 | 成本敏感系统 |

**分数映射**:每个维度 0.0-1.0,加权聚合。**保留各维度分数**,不只是总评 — 改进点靠 breakdown 定位。

**通过阈值**:通用 0.7,高风险场景 0.9。

### 3.3 LLM-as-Judge(规模化)

**构造 judge prompt**:清晰任务描述、待评输出、可选 ground truth、显式评分级别描述、结构化判断(给 reasoning)。

**关键约束**:
- 用**与被评 agent 不同的模型家族**(避免 self-enhancement bias)
- LLM judge 用于主观偏好 / 大规模集
- 边缘案例路由到 human review

### 3.4 人工评估(Human-in-the-Loop)

**触发**:
- 边缘案例
- 不寻常 query
- 生产流量随机抽样

**价值**:人能看到 hallucination、系统性失败、微妙偏差,自动化抓不到。

**反馈循环**:人评发现系统性模式 → 反哺自动评估标准。

### 3.5 终态评估(End-State Evaluation)

**适用**:mutate 持久状态的 Agent(文件、数据库、配置)。

**做法**:不评过程,断言终态:

```python
def evaluate(agent_output):
    # 让 agent 跑完,然后断言最终状态
    expected_files = ["result.yaml", "log.md"]
    assert all(os.path.exists(f) for f in expected_files)
    assert "decision" in parse_yaml("result.yaml")
    return Score(...)
```

---

## 4. 高级 LLM-as-Judge 技术

### 4.1 两种主要方式

| 方式 | 适用 | 注意点 |
|---|---|---|
| **Direct Scoring**(单响应打分量表) | 客观标准(事实性、指令遵循、有害性) | 标尺校准漂移,不一致解读 |
| **Pairwise Comparison**(两响应比较选优) | 主观偏好(语气、风格、说服力) | Position bias、length bias |

**关键事实**:Pairwise 与人类偏好的相关性常高于 Direct Scoring(用于主观任务)。

### 4.2 必须缓解的五大偏差

| 偏差 | 表现 | 缓解 |
|---|---|---|
| **Position bias** | 第一位响应被偏爱 | 交换位置评两次,多数表决 |
| **Length bias** | 越长分数越高 | 显式提示忽略长度,做 length-normalized 评分 |
| **Self-enhancement bias** | 模型评自己输出偏高 | 评估用不同模型家族 |
| **Verbosity bias** | 过度细节高分 | rubric 扣无关细节 |
| **Authority bias** | 自信语气高分 | 要求引用证据 + 事实核查层 |

### 4.3 指标选型框架

| 任务类型 | 主要指标 | 次要 |
|---|---|---|
| 二分类(通过/失败) | Recall, Precision, F1 | Cohen's kappa |
| 有序量表(1-5) | Spearman's rho, Kendall's tau | 加权 Cohen's kappa |
| 成对偏好 | Agreement rate, Position consistency | 置信度校准 |
| 多标签 | Macro-F1, Micro-F1 | 每标签 P/R |

**优先看系统性偏差模式,而不是绝对一致率**。Judge 在某维度稳定与人分歧,比随机噪声更糟糕。

---

## 5. 测试集设计

**代表性样本**:
- 简单 / 中 / 复杂 / 极复杂
- 跨工具集
- 跨交互长度
- 跨领域

**生产监控**:
- 持续运行小规模评估集
- 检测回归(指标下降 > X% 触发 alert)
- 用户反馈信号(点赞 / 投诉)作为外部校准

---

## 6. 与本知识库其他章节的关系

- **13-Harness-Engineering.md**:Evaluator 是 Locked 表面;自治循环依赖稳定 eval
- **09-Context-Engineering.md**:Context 失败模式有对应评测方法
- **11-Multi-Agent-Patterns.md**:多 agent 系统必须对比单 agent + 好模型基线
- **14-LLM-Project-Development.md**:评估是 project-level 决策的硬输入

---

## 7. 工程化检查清单

- [ ] 是否优先跑确定性检查(再 LLM judge)?
- [ ] Rubric 是否多维(不只一个总分)?
- [ ] LLM judge 用的是与 agent 不同的模型家族?
- [ ] 是否有 length / position / self-enhancement bias 缓解?
- [ ] 终态评估用于 mutate 持久状态的 agent?
- [ ] 测试集覆盖简单 / 中 / 复杂 / 极复杂?
- [ ] 生产监控 + 回归告警已配置?
- [ ] Human review 用于边缘案例?
- [ ] 评估预算接近生产实际(不是无限)?
- [ ] 评估结果保留 breakdown,不只是总分?

---

## 8. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| Agent 偶尔答错 | 平均准确率 95% 就上线 | 各维度独立,关注失败分布 |
| LLM judge 评自家模型 | Self-enhancement bias | 评估用不同模型家族 |
| 评"是否调用了 3 次工具" | 强加路径约束 | 评"是否达到正确结果" |
| 跑一次评估 | 单次结果就上线 | 多次运行取分布 |
| 优化评分 | 单一指标被 game | 多维 + 独立 verifier |
| 没生产监控 | 上线后无信号 | 持续小评估集 + 回归告警 |
| 用 LLM judge 评 schema | 浪费 token | 确定性检查先跑 |

---

## 9. 相关知识

- [Harness 工程](./13-Harness-Engineering.md)— Evaluator 是 Locked 表面
- [上下文工程总论](./09-Context-Engineering.md)— 失败模式有评测方法
- [LLM 项目开发](./14-LLM-Project-Development.md)
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)

---

## 10. 变更记录

- v2.0.0 (2026-07-10):基于 evaluation + advanced-evaluation 提炼,引入五大方法组合、四大挑战、五大 LLM-judge 偏差、指标选型框架;扩展 v1.0.0 的单维评分模型
- v1.0.0 (2026-07-09):初版,单维评分 + LLM-as-judge 基础