# _source.md — 源信息

- **上游仓库**:https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
- **作者**:Vercel
- **版本**:1.0.0
- **许可证**:MIT
- **拉取日期**:2026-07-10

## 内容结构

- SKILL.md — 技能入口
- AGENTS.md — 完整规则编译版(可被 Agent 直接加载)
- metadata.json — 元数据
- ules/ — 60+ 独立规则文件,按类别组织

## 覆盖(8 类 40+ 规则,按影响排序)

1. **Eliminating Waterfalls**(Critical)
2. **Bundle Size Optimization**(Critical)
3. **Server-Side Performance**(High)
4. **Client-Side Data Fetching**(Medium-High)
5. **Re-render Optimization**(Medium)
6. **Rendering Performance**(Medium)
7. **JavaScript Micro-optimizations**(Low-Medium)

## 适用范围

- React + Next.js 项目的性能审查
- 写新组件、审查代码时按 8 类规则逐条核对
- 76 个文件,适合代码审查 Agent 按需引用具体规则
