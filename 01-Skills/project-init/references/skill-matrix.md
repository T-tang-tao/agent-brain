# Skill Matrix — 项目类型 → 推荐 Skill 映射

> 本文件定义 `project-init` Step 3 的匹配规则,把项目标签映射到 KB 里的 skill 组合。

## 0. 映射总表

| 项目标签 | 必选 | 推荐 | 可选 |
|----------|------|------|------|
| `web` / `frontend` | `agents-md-author`, `superpowers` | `ui-ux-pro-max` | `baoyu-skills`(若有 UI 文档需求) |
| `backend` / `api` | `agents-md-author`, `superpowers` | `development-agent` | - |
| `agent` / `ai-app` | `agents-md-author`, `superpowers` | `agents-md-author`(核心), `loop-engineering` | `anthropics-skills`(Claude API) |
| `内容` / `内容创作` | `agents-md-author`, `baoyu-skills` | - | `superpowers`(若有发布脚本) |
| `数据` / `data` | `agents-md-author`, `superpowers` | `development-agent` | `anthropics-skills`(PDF/Excel) |
| `obsidian` | `agents-md-author`, `kepano-obsidian-skills` | - | - |
| `docs` / `文档` | `agents-md-author`, `anthropics-skills` | - | - |
| `通用` | `agents-md-author`, `superpowers` | `development-agent` | - |

## 1. 必选说明

**所有项目都必选 `agents-md-author`**:
- 强制遵守 AGENTS.md 编写规范(不写"为什么"段、不重复 KB 内容、< 500 行等)
- 任何时候改 AGENTS.md 都自动调用

**大多数项目必选 `superpowers`**(除非标签是 `内容` 或 `obsidian`):
- `superpowers` 是开发方法论集(TDD、调试、code review、brainstorming)
- 跨编程语言、跨 Runtime 通用
- 包含 13 个子 skill,brainstorming 是入口

## 2. 详细推荐理由

### 2.1 `web` / `frontend`

- **`ui-ux-pro-max`**:UI/UX 设计技能集(7 个子 skill),含设计系统、组件库、字体规范
- **`superpowers`**:前端也要写测试(组件测试、E2E)、debug(浏览器调试)
- **可选 `baoyu-skills`**:如果项目需要写 UI 文档、营销页面设计

### 2.2 `backend` / `api`

- **`superpowers`**:API 设计、数据库迁移、测试都涉及
- **`development-agent`**:专注开发的 Agent 工作协议(任务派发、代码评审、验证)
- 不推荐 `ui-ux-pro-max`(后端不写 UI)

### 2.3 `agent` / `ai-app`

- **`agents-md-author`**:必选,Agent 项目 AGENTS.md 必须严格(避免 Agent 误操作)
- **`loop-engineering`**:Agent Loop 设计(自动化循环系统),含五要素 + 三陷阱
- **`anthropics-skills`**:如果用 Claude API,含 `claude-api` skill
- **`superpowers`**:调试 Agent Loop 需要 TDD 方法

### 2.4 `内容` / `内容创作`

- **`baoyu-skills`**:20+ 子 skill 覆盖小红书、信息图、公众号、AI 生图等中文场景
- **`superpowers`**:可选,如果项目也有自动化脚本
- 不推荐 `ui-ux-pro-max`、`loop-engineering`

### 2.5 `数据` / `data`

- **`superpowers`**:数据处理也要 TDD(数据管道测试、SQL 测试)
- **`development-agent`**:数据工程也是开发
- **`anthropics-skills`**:可选,如果产出 Excel/PDF 报表

### 2.6 `obsidian`

- **`kepano-obsidian-skills`**:Obsidian 官方维护的 5 个 skill(markdown / bases / canvas / cli / defuddle)
- 不推荐 `superpowers`(Obsidian 插件开发不属于通用开发方法论范畴)

### 2.7 `docs` / `文档`

- **`anthropics-skills`**:含 docx / pdf / pptx / xlsx 文档技能
- 不需要 `superpowers`(纯文档处理)

### 2.8 `通用`

- **`superpowers`**:通用开发方法论
- **`development-agent`**:如果项目有任何代码,加上这个

## 3. 阶段修饰

按 Q3 的阶段可以加额外 skill:

| 阶段 | 额外推荐 |
|------|----------|
| `mvp` | 不加,够用就好 |
| `增长` | `superpowers` 全套(13 子 skill 全部加载) |
| `稳定` | `superpowers` 全套 + 严格边界规则模板(从 `05-Boundaries/`) |

## 4. 自定义选择

用户可以拒绝推荐,手动指定 skill 列表。支持的语法:

- "只要 superpowers"
- "加 baoyu-skills"
- "去掉 ui-ux-pro-max"
- "按 superpowers + development-agent 来"

AI 根据用户原话调整,不需要走完整问卷。

## 5. 不推荐给新项目的 Skill

| Skill | 原因 |
|-------|------|
| `kb-init` | 那是给知识库自身的,不是项目 |
| `agents-md-author` 单独 | 这是 project-init 必选,不需要单独选 |
| `kimi-webbridge` | 浏览器自动化专用,看场景 |
| 单个 baoyu 子 skill | project-init 选 baoyu-skills 整体 |
| 单个 ui-ux 子 skill | project-init 选 ui-ux-pro-max 整体 |

## 6. 输出格式

Step 3 输出推荐列表给用户确认:

```yaml
recommended_skills:
  required:
    - agents-md-author   # AGENTS.md 规范
    - superpowers        # 开发方法论
  recommended:
    - ui-ux-pro-max      # UI/UX 设计
  optional:
    - baoyu-skills       # 若需要内容/文档
  bridge_runtime:
    - claude-code        # 当前检测到的 Runtime
```

**必须用户确认后再部署**。
