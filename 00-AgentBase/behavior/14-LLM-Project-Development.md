# LLM 项目开发方法论

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | project, pipeline, task-model-fit, cost, iteration, structured-output |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

写代码前先验 **task-model fit**。LLM 不是万能,先跑一次手测,再决定要不要自动化。流水线分阶段,每阶段离散 / 幂等 / 可缓存 / 独立,小步快迭代。

---

## 1. Task-Model Fit:动手前的 6/6 判断

### 1.1 适合 LLM 的特征(Proceed)

| 特征 | 原因 |
|---|---|
| **跨源综合** | LLM 擅长融合多源信息,优于规则系统 |
| **带 rubric 的主观判断** | 评分、评估、分类用 LLM 自然 |
| **自然语言输出** | 目标本身就是可读文本 |
| **容错** | 单个失败不破坏整体,LLM 非确定性可接受 |
| **批量处理** | 项间无状态,context 干净 |
| **训练中已有领域知识** | 减少 prompt 工程开销 |

### 1.2 不适合 LLM 的特征(Stop)

| 特征 | 原因 |
|---|---|
| **精确计算** | 数学 / 计数 / 严格算法不可靠 |
| **实时要求** | 亚秒级响应 LLM 延迟不够 |
| **100% 准确率要求** | Hallucination 风险必然 |
| **依赖专有数据** | 模型 prompt 拿不到 |
| **强顺序依赖** | 每步依赖上一步,误差累积 |
| **确定性输出要求** | 同输入必须同输出,LLM 保证不了 |

### 1.3 强制手测一步

**任何 LLM 项目动手前,先复制一个代表性输入到模型界面,跑一次手测**。问自己:

- 模型有完成任务所需知识吗?
- 能按要求格式输出吗?
- 大规模跑大概什么质量?
- 明显的失败模式有哪些?

**失败的 manual prototype 预言失败的系统**,成功的给出质量基线和 prompt 模板。耗时几分钟,避免几天浪费。

---

## 2. 流水线架构(Staged Pipeline)

把 LLM 项目分阶段,因为**确定性 / 非确定性分离才能快迭代 + 成本可控**。

每阶段必须:
- **Discrete** — 边界清晰,可独立 debug
- **Idempotent** — 重跑产生同样结果
- **Cacheable** — 中间结果落盘,避免重算
- **Independent** — 每阶段可独立运行,选择性重跑

**规范结构**:

```
acquire → prepare → process → parse → render
```

| 阶段 | 性质 | 例子 |
|---|---|---|
| acquire | 确定性 | 拉数据 / 抓网页 / 读文件 |
| prepare | 确定性 | 清洗 / 标准化 / 切块 |
| process | **非确定性** | LLM 调用 |
| parse | 确定性 | 解析 LLM 输出,结构化 |
| render | 确定性 | 生成最终产物(报告 / 文件) |

**优势**:process 阶段失败可重跑,前序阶段缓存复用。

---

## 3. 成本估算

**必做** — 写代码前先估算:

- 单查询平均 token(input / output)
- 总查询次数
- 模型单价(input / output per 1k)
- 月 / 周 / 日成本

**还要估算失败成本**:
- Hallucination 的人工审查时间
- 错误输出的下游影响
- 重新生成的概率

**经验法则**:**模型升级的 ROI 通常 > 加 token**。先用最强模型 + 保守预算,看效果再调。

---

## 4. 单 Agent vs 多 Agent(项目级决策)

**默认单 Agent + 好模型**。拆多 Agent 之前必须证明:

- 任务超过单 context 容量
- 子任务可清晰并行
- 总收益 > 多 Agent 的 token 倍增 + 协调开销

**参考**:多 Agent 系统 token 成本可比单 Agent 高数倍。如果加 Agent 没带来 2 倍以上质量提升,就是浪费。

---

## 5. 结构化输出设计(跨阶段契约)

LLM 输出是字符串,但下游消费者(代码 / 数据库 / 另一个 LLM)需要结构化数据。

**设计原则**:
- 显式格式规范(JSON Schema / Pydantic / TypeScript interface)
- **Parse 阶段独立**(LLM 输出 → 验证 → 修正;不让 LLM 自己保证格式)
- 失败模式定义:格式错误时是 retry / fallback / 人工

```python
class LLMOutput(BaseModel):
    decision: Literal["approve", "reject"]
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
```

**Parse 阶段关键**:
- Schema 验证
- 修复(可自动修的简单错误)
- 失败时显式信号,不要 silent default

---

## 6. Agent 辅助迭代

**让 Agent 帮你建项目本身**:

- 项目骨架 / 模板生成
- 重复代码 / 测试生成
- 文档初稿
- 错误信息翻译
- 代码审查 checklist

**但**:
- Agent 写代码 ≠ Agent 写好代码,人工 review 不可省
- 关键决策(架构、安全边界)人类拿,Agent 辅助实现

---

## 7. 与本知识库其他章节的关系

- **05-评估方法(Evaluation).md**:项目决策的硬输入
- **09-Context-Engineering.md**:流水线 process 阶段的 context 管理
- **11-Multi-Agent-Patterns.md**:项目级拆 agent 的依据
- **13-Harness-Engineering.md**:迭代循环的 harness
- **12-Tool-Design.md**:流水线各阶段的工具

---

## 8. 工程化检查清单

- [ ] 任务跑过 task-model fit 的 6/6 判断?
- [ ] 至少 1 个 manual prototype 验证过?
- [ ] 流水线是 5 阶段(acquire / prepare / process / parse / render)?
- [ ] 每阶段离散 / 幂等 / 可缓存 / 独立?
- [ ] 成本估算(含失败成本)做了?
- [ ] 单 Agent + 好模型先验过,多 Agent 有 ROI 证据?
- [ ] 结构化输出有显式 schema?
- [ ] Parse 阶段独立,失败有显式信号?
- [ ] Agent 辅助迭代部分有人工 review?
- [ ] 关键决策(架构、安全)人类拿,Agent 辅助实现?

---

## 9. 错误案例 vs 正确做法

| 场景 | 错误 | 正确 |
|---|---|---|
| 假设 LLM 能做 | 没跑过手测就自动化 | manual prototype 验证 → 再写代码 |
| 数学计算任务 | 用 LLM 算总和 | 用代码 / DB 算 |
| 100% 准确率要求 | 用 LLM 跑关键决策 | 用确定性代码 + LLM 辅助 |
| 一次大 prompt | 整任务塞单次调用 | 拆 5 阶段,每阶段独立 |
| LLM 拼 JSON 字符串 | 让 LLM 自由输出 | 显式 schema + parse 阶段验证 |
| 没用 cache | 每次重跑 prepare | 中间结果落盘 |
| 多 Agent 起步 | 没测单 Agent 就拆 | 先单 Agent + 好模型,有证据再拆 |
| 拒绝 Agent 辅助 | 全部手写 | Agent 写 boilerplate,人 review |

---

## 10. 相关知识

- [评估方法](./05-评估方法(Evaluation).md)
- [上下文工程总论](./09-Context-Engineering.md)
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)
- [Harness 工程](./13-Harness-Engineering.md)
- [Tool 设计](./12-Tool-Design.md)