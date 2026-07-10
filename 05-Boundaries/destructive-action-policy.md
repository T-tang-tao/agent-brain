# Destructive Action Policy

> 破坏性操作边界。删除 / 覆盖 / 合并 / 重置等操作必须参考本策略。

## 规则名称

`destructive-action-policy`

## 适用范围

- 所有 agent
- 所有破坏性操作:删除 / 覆盖 / 重置 / 合并 / 强制推送 / 数据库迁移 / 配置恢复出厂
- 所有 Runtime(Claude Code / Codex / Hermes)

## 允许的行为

✅ Agent 可自主执行:

- **删除新建的空文件**(创建后 5 分钟内,未引用)
- **删除临时缓存**:`.tmp/`、`node_modules/`(在 `.gitignore` 内)、`__pycache__/`
- **删除废弃标记的资产**:status = 弃用 + 创建时间 > 30 天

## 需要确认的行为

⚠️ 必须先问用户,给出明确影响清单后执行:

- **删除任何带内容的文件**:必须先列出影响
- **删除目录**(非空)
- **覆盖已有文件**(非空):先备份到 .bak
- **git reset --hard** / **git checkout .** / **git clean -fd**:任何 reset 操作
- **git push -f**:强制推送
- **git merge --no-ff**:合并(可能产生冲突)
- **Drop database table / schema**
- **改主分支名 / 删分支**
- **恢复出厂配置**(rm -rf ~/.claude / 类似)
- **重装 Runtime**:卸载 + 重装

## 禁止的行为

❌ 任何情况下禁止:

- **`rm -rf` 不带具体路径**:必须明确列路径
- **`DROP DATABASE` 不带 WHERE 子句**
- **`rm -rf /` / `rm -rf ~` / `rm -rf C:\\`**:任何根目录递归删除
- **`git push --force` 到 main / master / 任何保护分支**
- **`git filter-branch` / `git filter-repo`**:改写历史
- **删除 `.obsidian/` 任何文件**
- **删除 `.git/`**:会丢失所有版本控制
- **在生产数据库上跑 migration**:必须人工
- **调用 "一键清空" 类 API**:如清空回收站、清空日志、清空交易记录
- **未经授权的物理操作**:格式化 U 盘、卸载硬盘

## 备份规则

任何 [需确认] 类操作前必须:

```powershell
# 1. 先备份(自动)
$backup = "${path}_bak_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item -Recurse "${path}" "${backup}"
Write-Output "Backed up to: ${backup}"

# 2. 列出将受影响的内容
Get-ChildItem -Recurse "${path}" | Select-Object FullName, Length | Format-Table

# 3. 询问用户(给影响清单 + 回滚方式)
"将删除 47 个文件,共 1.2MB。备份在 ${backup}。继续吗?"

# 4. 等用户明确 yes 才执行
```

## 风险说明

| 操作 | 风险 | 可恢复性 |
|------|------|----------|
| `rm -rf` 文件 | 数据丢失 | 难(需备份) |
| `git push -f` | 覆盖他人 commit | 极难(需联系所有人) |
| `DROP TABLE` | 表数据清空 | 难(需备份) |
| 覆盖配置文件 | 服务中断 | 易(改回即可) |
| 卸载 Runtime | 配置丢失 | 中(备份可恢复) |
| 格式化磁盘 | 全部数据 | 极难(需专业恢复) |

## Agent 执行说明

1. **判断操作**:删除 / 覆盖 / 重置?
2. **判断范围**:单文件 / 目录 / 整个系统?
3. **判断可逆性**:有备份可恢复?能 git revert?能重装?
4. **执行前**:
   - 自动备份(用户没拒绝的情况下)
   - 列出影响清单
   - 询问用户
5. **执行后**:
   - 验证效果
   - 给出回滚命令

## 例子

### 允许

```text
> 删除 D:\temp\test.txt 这个我刚建的空文件
```

✅ 直接删(文件 < 5min,空)

### 需确认 + 备份

```text
> 删掉 D:\valut\trade\agent\01-Skills\projects\ui-ux-pro-max 整个目录,我要重新拉
```

⚠️ "将删除 229 个文件,共 12MB。备份到 `..._bak_2026-07-09_153022`?继续吗?"

### 禁止

```text
> 把 D:\valut\trade\agent\.git 删了,占空间
```

❌ "禁止。删 `.git/` 会丢失所有版本历史。建议 `git gc` 压缩,或用 `git worktree` 清理未引用的对象。"

## 回滚模板

任何破坏性操作后,记录到 `99-Roadmap.md`:

```markdown
## YYYY-MM-DD HH:MM — 破坏性操作

- **动作**: <具体动作>
- **影响范围**: <文件 / 行数 / 字节>
- **备份位置**: <路径>
- **回滚命令**: <如 Remove-Item ...; Move-Item backup ...>
- **已验证**: <是/否 + 验证方式>
```

## 相关知识

- [`file-edit-policy.md`](./file-edit-policy.md)
- [`shell-command-policy.md`](./shell-command-policy.md)
- [`../00-AgentBase/safety/01-Agent边界与限制.md`](../00-AgentBase/safety/01-Agent边界与限制.md)