# 知识库类型参考表

> 本文件供 kb-init 技能在 Step 2(确定知识库类型)时参考。实际以头脑风暴结果为准。

## 类型对照

| 类型 | 典型目录骨架 | 核心特点 |
|------|-------------|----------|
| 编程/项目 | `docs/` `architecture/` `api/` `guides/` `decisions/` | 需要 repo 文件、架构决策记录、API 文档 |
| 产品开发 | `vision/` `requirements/` `design/` `features/` `milestones/` `decisions/` `retrospectives/` `changelog/` | 跟踪从想法到发布的全生命周期,实时进度用工具查 |
| 交易/量化 | `strategies/` `factors/` `risk/` `backtest/` `research/` | 实时数据不写入,策略/因子/风控是静态知识 |
| 学术/研究 | `papers/` `notes/` `concepts/` `reviews/` `references/` | 论文摘录、概念定义、文献综述 |
| 客服/文档 | `faq/` `policies/` `products/` `troubleshooting/` | 权威来源、版本控制、引用溯源 |
| 个人助手 | `preferences/` `habits/` `projects/` `journal/` `contacts/` | 隐私边界、可删除、可纠正 |
| 通用/混合 | 根据用户实际需求定制 | 不套模板,按头脑风暴结果设计 |

## 参考目录结构示例

### 编程/项目知识库

```
my-project-wiki/
├── AGENTS.md
├── README.md
├── 00-目录索引.md
├── architecture/      # 架构决策、设计文档
├── api/               # API 文档
├── guides/            # 操作指南
├── decisions/         # ADR(架构决策记录)
├── troubleshooting/   # 踩坑记录、排障
└── raw/               # 原始资料(可选)
```

### 产品开发知识库

```
product-dev-wiki/
├── AGENTS.md
├── README.md
├── 00-目录索引.md
├── vision/            # 产品愿景、路线图(长期方向)
├── requirements/      # 需求文档(PRD、用户故事)
├── design/            # 设计决策(架构、技术选型)
├── features/          # 功能规格(每个 feature 的详细 spec)
├── milestones/        # 里程碑与版本规划
├── decisions/         # 决策记录(ADR)
├── retrospectives/    # 复盘与经验教训
├── changelog/         # 版本变更记录
└── raw/               # 原始资料(可选)
```

**与编程/项目库的区别**:

| 维度 | 编程/项目库 | 产品开发库 |
|------|------------|-----------|
| 视角 | 代码为中心(架构/API/排障) | 产品为中心(愿景/需求/发布) |
| 读者 | 开发者(需理解代码) | 全团队(需理解产品方向) |
| 时间轴 | 当前状态(代码怎么工作) | 全生命周期(从想法到发布到复盘) |
| 典型文档 | API 文档、架构图、排障指南 | PRD、路线图、功能 spec、changelog |

> 如果团队既要管产品方向又要管代码细节,设计混合结构:在产品开发骨架上增加 `architecture/` `api/` 目录。

### 交易/量化知识库

```
trading-wiki/
├── AGENTS.md
├── README.md
├── 00-目录索引.md
├── strategies/        # 策略说明(静态知识)
├── factors/           # 因子定义
├── risk/              # 风控规则
├── backtest/          # 回测记录与经验
├── research/          # 研究笔记
├── market-structure/  # 市场结构认知
└── raw/               # 原始资料(可选)
```

### 学术/研究知识库

```
research-wiki/
├── AGENTS.md
├── README.md
├── 00-目录索引.md
├── concepts/          # 概念定义
├── papers/            # 论文摘录与笔记
├── reviews/           # 文献综述
├── references/        # 参考资料索引
├── methods/           # 研究方法
└── raw/               # 原始资料(可选)
```

## 关键区分原则

- **编程库**:代码需要精确路径、调用关系和当前文件状态,不能只靠向量检索
- **产品开发库**:产品方向/需求/设计是静态知识;实时进度(Sprint 状态、bug 数、CI 结果)用工具查,不写入库
- **交易库**:实时状态(价格、订单、账户)不写入,用工具/API 查询
- **学术库**:强调引用溯源,矛盾信息以权威来源仲裁
- **客服库**:强调版本控制,避免编造,更新机制要明确
- **个人助手**:Memory 只保存未来有用的长期信息,不应把所有对话都记住

## 通用:00-human 人类入门区

无论哪种类型的知识库,都可以考虑建立 `00-human/` 目录,存放:

- 人类需要但 Agent 不需要读的**基础认知**(概念解释、类比、误解澄清、学习路径)
- Agent 天生就懂这些概念,读这些内容只浪费上下文窗口

```
任何知识库/
├── 00-human/            # 人类入门(Agent 不读)
│   ├── README.md        # 这个目录是什么、怎么读
│   ├── 01-入门.md       # 基础概念、类比
│   ├── 02-术语速览.md    # 关键术语一句话解释
│   └── 03-常见误解.md    # 误解与澄清
├── ...                  # 其他模块只保留 Agent 需要的结构化信息
```

判断标准:如果一段内容是在**教人类理解一个概念**(而不是记录项目特定的规则或约定),就放 `00-human/`。

> 参考:本知识库自身的 `00-AgentBase/00-human/` 是一个完整实现。
