# 托管 Agent 基础设施(Hosted Agents)

| 字段 | 值 |
|------|-----|
| 层级 | 认知层 |
| 分类 | 00-AgentBase / behavior |
| 状态 | 已发布 |
| 版本 | v1.0.0 |
| 创建 | 2026-07-10 |
| 更新 | 2026-07-10 |
| 作者 | Agent Knowledge Base Admin(基于 muratcankoylan/Agent-Skills-for-Context-Engineering v2.4.0 提炼) |
| 标签 | hosted, sandbox, warm-pool, image-registry, snapshot, multiplayer |
| 来源 | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) |

---

## 一句话理解

Hosted Agent = **跑在远程沙箱里而不是本机的 Agent**。沙箱层 / API 层 / 客户端层三分离,预热池 + 镜像注册表 + 快照三件套消除冷启动延迟。

---

## 1. 何时用 Hosted Agent

- 后台编码 Agent(独立于用户设备运行)
- 多用户协作 Agent 会话
- 多客户端接口(Slack / Web / 浏览器扩展)
- 突破本机资源限制的水平扩展
- Agent 自启子 Agent 做并行工作

---

## 2. 三层架构

| 层 | 职责 | 关注点 |
|---|---|---|
| **Sandbox** | 隔离执行环境 | 镜像注册表 / 预热池 / 快照 |
| **API** | 状态管理 + 客户端协调 | session 持久化、状态机 |
| **Client** | 用户交互界面 | TUI / Web / Slack,只做 thin client |

**关键**:**三层解耦**,沙箱变更不波及客户端。

---

## 3. 沙箱三件套

### 3.1 镜像注册表(Image Registry)

**预构建环境镜像,定期刷新**(每 30 分钟一次是合理节奏):

每个镜像包含:
- 仓库(已知 commit)
- 所有 runtime 依赖
- 初始 setup / build 完成
- App + test suite 跑过一遍的 cache

**Session 启动**:从最新镜像 spin-up 沙箱,仓库最多 30 分钟过时,git sync 很快。

### 3.2 预热池(Warm Pool)

**冷启动是用户挫败感主因**,维护预热沙箱池:

- 用户**开始打字时**就启动预热(预测式预热)
- 新镜像构建完成 → 旧池条目过期 / 重建
- 高流量仓库 → 池大小按用量调

### 3.3 快照(Snapshot)

**关键点文件系统快照**,用于 follow-up prompt 的即时恢复:

- 镜像构建后(基础快照)
- Agent 改完(session 快照)
- 沙箱退出前(可能跟进的备份)

**Rollback / 恢复** 不重跑 setup。

---

## 4. 启动延迟优化

**核心挑战**:用户对延迟敏感,>几秒就觉得"坏了"。

**允许读不等写**:Agent 起步阶段,允许**先读文件**(git sync 完前就开读),**等 git 写时再同步**。这能省 1-3 秒感。

**预测式预热**:用户开始打字就准备沙箱,不是点提交才启动。

**自启子 Agent**:并行子任务用 self-spawning agents,而不是串行。

---

## 5. Git 配置(后台 Agent 特别注意点)

后台 Agent 不绑特定用户,git identity 必须显式配置:

- 用 **GitHub app installation token** 做 clone 鉴权
- Commit / push 时显式设 `user.name` / `user.email`
- Commit 用**提示用户的身份**,不是 app 身份

---

## 6. Agent 框架选型

### 6.1 Server-First

Agent framework 当**服务端**用,TUI / desktop 当 **thin client**:

- 多客户端共享一个后端
- 跨 surface 行为一致
- 插件系统扩展功能不改 client
- 事件驱动架构,实时更新任意客户端

### 6.2 Code as Source of Truth

**Agent 能读自己源码理解行为**,防止 hallucinate 自己的能力 — 这是被低估的失败模式。

### 6.3 插件系统要求

支持 **runtime interception**:

- 监听 `tool.execute.before` / `tool.execute.after`
- 加安全控制不改核心逻辑
- 加可观测性 hook

---

## 7. 多人协作

- **多客户端同步 session 状态**(乐观锁 / CRDT)
- **共享 state 后端**(不要各 client 持自己的 state)
- **权限边界**(谁批准 destructive 操作)

---

## 8. 与本知识库其他章节的关系

- **13-Harness-Engineering.md**:Hosted 基础设施是 harness 的一种实现
- **10-Filesystem-Context.md**:Session 内 filesystem 是沙箱内
- **11-Multi-Agent-Patterns.md**:Self-spawning 是 hosted 场景的实现

---

## 9. 工程化检查清单

- [ ] 沙箱 / API / Client 三层解耦?
- [ ] 镜像定期重建(每 30 分钟节奏)?
- [ ] 预热池有吗?预热触发在用户开始打字时?
- [ ] 关键点有 snapshot?
- [ ] Agent 启动允许读不等写?
- [ ] Git identity 显式配置?
- [ ] 框架 server-first,client thin?
- [ ] Agent 能读自己源码?
- [ ] 插件系统支持 runtime interception?
- [ ] 多人 session 有共享 state 后端?

---

## 10. 相关知识

- [Harness 工程](./13-Harness-Engineering.md)
- [文件系统 Context](./10-Filesystem-Context.md)
- [Multi-Agent 模式](./11-Multi-Agent-Patterns.md)