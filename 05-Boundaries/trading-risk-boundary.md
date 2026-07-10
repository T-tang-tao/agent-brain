# Trading Risk Boundary

> 交易/资金操作边界。本策略**优先级最高**。交易 MCP 配置待补(见 `99-Roadmap.md` 第四阶段)。

## 规则名称

`trading-risk-boundary`(优先级:CRITICAL)

## 适用范围

- 所有 agent
- 所有涉及资金/订单/仓位/合约的操作:
  - 下单 / 撤单 / 改单
  - 加仓 / 减仓 / 平仓
  - 充值 / 提现 / 转账
  - API key 管理
  - 策略参数修改(影响实盘)
  - 触发止损 / 止盈
- 适用场景:数字货币 / 股票 / 期货 / 期权 / 外汇 / 银行账户

## 允许的行为

✅ Agent 可自主执行(**仅限于以下场景**):

- **只读查询**:
  - 账户余额 / 持仓 / 委托单(GET)
  - 行情 / K 线 / 深度(GET)
  - 历史成交 / 历史订单(GET)
  - 资金费率 / 持仓量(GET)
- **纸面交易**:`testnet` / `paper trading` / `sandbox` 环境下的所有操作
- **模拟盘演练**:模拟账户下的完整操作
- **本地回测**:本地数据 + 本地策略,不调真实 API

## 需要确认的行为

⚠️ 必须先问用户,**给出完整风险评估**后执行:

- **小额真实下单**:单笔 ≤ 用户设置的最大单笔金额(默认 100 USD 等值)
- **修改策略参数**:影响实盘行为的参数(仓位、止损、止盈)
- **挂止损/止盈单**:订单会真实执行
- **调整杠杆**:从 1x 到更高
- **新增交易对**:在已有账户基础上开新市场
- **任何用真实 API key 的写操作**

## 禁止的行为

❌ **任何情况下禁止**:

- **大额真实下单**:超过"最大单笔金额"(默认 100 USD)
- **全仓/满仓操作**:仓位 > 账户 50%
- **杠杆 > 10x**:极高风险
- **永续合约全仓模式**:可被强平
- **调用提现 API**:任何金额
- **改 API key 权限范围**:增加 scope
- **转账到非白名单地址**
- **删除 API key 而没有备份**
- **在主网跑未回测的策略**:至少要 3 个月历史回测 + 模拟盘 1 个月
- **修改生产策略参数而不通知用户**
- **跳过验证直接下单**:必须先看 quote / 滑点预估
- **市价单大额成交**:大额必须用限价单
- **未确认的 stop-loss 触发**:风控参数变更必须人工
- **在测试中混入真实资金**

## 强制流程(下单前)

任何真实下单前必须:

```text
1. 读 trading-risk-boundary.md(本文件)
2. 判断操作属于 [允许 / 需确认 / 禁止]
3. [需确认] 类必须输出风险评估:
   - 仓位变化(从 X 到 Y,Z% 仓位)
   - 最大亏损估算(基于当前波动率)
   - 影响范围(单账户 / 跨账户 / 跨交易所)
   - 回滚方式(撤单 / 反向下单)
4. 等用户明确 yes
5. 执行 + 立即验证成交结果
6. 记录到 99-Roadmap.md
```

## 风险参数默认值

任何交易 agent 应该配置:

```yaml
max_single_order_usd: 100
max_position_ratio: 0.50  # 最大 50% 仓位
max_leverage: 10
allowed_symbols: []       # 白名单,空=不限制
allowed_exchanges: []     # 白名单
stop_loss_required: true
require_confirmation_above_usd: 100
```

修改这些参数需要走 [`memory-write-policy.md`](./memory-write-policy.md) 的 [需确认] 流程。

## 测试 vs 生产区分

| 维度 | 测试 / 模拟 | 生产 |
|------|--------------|------|
| API endpoint | testnet / sandbox | mainnet |
| API key | 独立 testnet key | 独立 mainnet key(永不共用) |
| 资金 | 测试币 / 模拟资金 | 真实资金 |
| 订单 | 不影响真实市场 | 影响真实市场 |
| Agent 权限 | 可自主 | 强审批 |
| 风险参数 | 较松 | 严格 |

**关键**:testnet key 和 mainnet key **必须分开**,绝不能用同一个 key 跑测试和生产。

## Agent 执行说明

1. **先识别环境**:`endpoint.contains('testnet')` 或 `exchange.sandbox == true` → 模拟
2. **真实环境默认拒绝**:所有 [禁止] 类不要询问,直接拒绝
3. **真实环境 [需确认]**:必须强制走"强制流程"6 步
4. **执行后**:
   - 立即查询成交确认
   - 报告盈亏影响
   - 记录到 99-Roadmap.md

## 例子

### 允许(模拟)

```text
> 在 testnet 下个 BTC 多单 0.01
```

✅ 模拟环境,可执行

### 需确认(小额真实)

```text
> 在 OKX 主网下 BTC-USDT 限价多单 100 USDT
```

⚠️ "真实环境,需确认。风险评估:
- 单笔:100 USDT(未超过默认上限)
- 仓位:占账户 X%(< 50% 上限)
- 杠杆:1x
- 滑点预估:0.05%
- 最大亏损(假设 -10%):10 USDT
- 回滚:挂反向限价单

继续?需要你明确 'yes' 我才执行。"

### 禁止

```text
> 用 50x 杠杆开 BTC 全仓多单
```

❌ "禁止。50x 杠杆 + 全仓 + 主网 = 极高风险,任何 agent 都不应自主执行。即使人工也要严格评估。"

## 审计

所有真实环境操作必须记录到 `99-Roadmap.md`:

```markdown
### YYYY-MM-DD HH:MM — 交易操作

- **exchange**: OKX
- **symbol**: BTC-USDT
- **side**: buy
- **amount**: 100 USDT
- **leverage**: 1x
- **order_id**: 12345678
- **filled_price**: 67543.21
- **risk_acknowledged**: user explicit yes
- **rollback_plan**: place reverse limit order at 67000
```

## 相关知识

- [`external-api-policy.md`](./external-api-policy.md) — 通用 API 边界
- [`memory-write-policy.md`](./memory-write-policy.md) — 策略参数持久化
- [`destructive-action-policy.md`](./destructive-action-policy.md) — 不可逆操作
- [`../04-MCP/`](../04-MCP/README.md) — 交易 MCP 配置(待补)