# External API Policy

> 外部 API 调用边界。任何 HTTP 请求 / WebFetch / API 调用前必须参考本策略。

## 规则名称

`external-api-policy`

## 适用范围

- 所有 agent
- 所有 HTTP 请求:WebFetch / WebSearch / curl / Invoke-WebRequest / MCP HTTP tools
- 所有第三方服务:GitHub / NPM / PyPI / 交易所 / 银行 / 邮件 / 短信

## 允许的行为

✅ Agent 可自主执行:

- **GET 请求到公开 API**:GitHub API / 公共文档 / Wikipedia
- **WebSearch**:搜公开信息
- **WebFetch 公开网页**:博客 / 文档 / 官方 README
- **读自己的 MCP server**:filesystem / obsidian(本地服务)
- **读用户授权过的 API**:OAuth scope 内的只读

## 需要确认的行为

⚠️ 必须先问用户:

- **POST / PUT / DELETE**:任何写操作
- **调任何需要 API key 的 API**:即使只是 GET 也要确认 key 是否可用
- **上传文件**:到任何服务(GitHub gist / Pastebin / S3)
- **发邮件 / 短信 / 通知**:任何 outbound 通讯
- **触发 webhook**:任何回调
- **真实下单 / 转账 / 充值**:金融操作(参见 [`trading-risk-boundary.md`](./trading-risk-boundary.md))
- **调用 rate-limited API 大量请求**:可能触发封禁

## 禁止的行为

❌ 任何情况下禁止:

- **把 API key 放在 URL 里**:`?api_key=xxx`(会进日志)
- **把 API key 写入代码仓库**:即使是 .env 也不行,会被 commit
- **跨用户调用别人授权的 API**:用谁的 key 只能访问谁的数据
- **调用来路不明的服务**:除非用户明确指定
- **抓取明确禁止爬取的页面**:`robots.txt: Disallow` + 站点 TOS 禁止
- **绕过 rate limit**:加 sleep / 用代理绕开限制
- **DoS 任何服务**:即使是误操作也不允许
- **调用未加密 HTTP 服务**:只允许 HTTPS
- **把用户数据传给第三方**:没授权的隐私泄露
- **调用任何"匿名 hack"服务**:Tor exit node / 公共 VPN 出口

## 风险说明

| 风险 | 后果 |
|------|------|
| 密钥泄露 | URL/日志 → 攻击者直接看到 |
| 配额耗尽 | 账号被 ban / 产生费用 |
| 触发风控 | API 被临时封禁 / KYC 触发 |
| 法律风险 | 违反服务条款 / GDPR / CCPA |
| 数据外泄 | 用户隐私传给第三方 |
| 真实交易 | 真钱损失 |

## Agent 执行说明

1. **判断目的**:
   - 读公开信息? → [允许]
   - 写 / 调外部副作用? → [需确认 或 禁止]
2. **判断认证**:
   - 不需要 key? → 看 1
   - 需要 key? → [需确认] + 检查 key 怎么传
3. **判断范围**:
   - 自己账户? → 用户授权后 [允许]
   - 别人账户? → [禁止]
4. **判断副作用**:
   - 副作用不可逆?(下单、发邮件) → [禁止 或 强确认]
   - 副作用可逆?(评论、点赞)? → [需确认]
5. **执行 + 验证**:
   - 看返回码 / 错误
   - 看 rate limit 剩余

## 例子

### 允许

```text
> 用 WebFetch 拉 https://github.com/obra/superpowers 的 README
```

✅ 直接拉

### 需确认

```text
> 我想用 GitHub API 创建一条 issue 提到 bug,标题是 "x is broken"
```

⚠️ "POST 到 GitHub API 需要认证。你提供了 token 吗?放在哪个环境变量?创建后能不能先给你看 draft?"

### 禁止

```text
> 帮我用我的 OKX API key 下个 ETH 多单 0.1
```

❌ "禁止。真实交易不能由 agent 自主执行,即使是 GET 行情都要走 [`trading-risk-boundary.md`](./trading-risk-boundary.md) 的强审批流程。"

## 相关知识

- [`trading-risk-boundary.md`](./trading-risk-boundary.md)
- [`memory-write-policy.md`](./memory-write-policy.md) — 哪些信息可以写到记忆
- [`../00-AgentBase/safety/01-Agent边界与限制.md`](../00-AgentBase/safety/01-Agent边界与限制.md)