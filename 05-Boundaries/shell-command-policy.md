# Shell Command Policy

> Shell 命令执行边界。Agent 跑任何命令前必须参考本策略。

## 规则名称

`shell-command-policy`

## 适用范围

- 所有 agent
- 所有 Shell 命令执行(PowerShell / Bash / Zsh)
- 任何主机(本地 / 远程 / 容器)

## 允许的行为

✅ Agent 可自主执行:

- **只读命令**:`ls`、`cat`、`Get-Content`、`Get-ChildItem`、`head`、`tail`、`grep`、`Select-String`、`find`(限深度)
- **Git 只读**:`git status`、`git log`、`git diff`、`git show`、`git branch -a`
- **包管理查询**:`npm list`、`pip list`、`pip show`
- **服务查询(无副作用)**:`Get-Process`、`netstat -an`、`Get-Service`
- **系统信息**:`Get-Date`、`whoami`、`hostname`、`pwd`
- **环境查看**(不含密钥内容):`echo $HOME`、`Get-ChildItem Env:`

## 需要确认的行为

⚠️ 必须先问用户:

- **Git 写操作**:`git commit`、`git push`、`git merge`、`git rebase`、`git reset --hard`、`git clean -fd`
- **包安装**:`npm install`、`pip install`、`cargo install`、`brew install`
- **进程管理**:`Stop-Process`、`kill`、`taskkill`、`Start-Process`、`Start-Service`
- **网络请求**:`Invoke-WebRequest`、`curl`、`wget`、`ssh`、`scp`
- **写文件命令**:`echo > file`、`Out-File`、`Set-Content`、`>>`、`tee`
- **环境变量修改**:`$env:VAR = value`、`export VAR=value`
- **修改系统配置**:`Set-ExecutionPolicy`、`chmod`、`chown`、`netsh`、`firewall-cmd`
- **执行下载的脚本**:`irm ... | iex`、`curl ... | bash`

## 禁止的行为

❌ 任何情况下禁止:

- **`rm -rf`**:PowerShell 等价 `Remove-Item -Recurse -Force` 也禁止
- **`git push -f` 到主分支**:会覆盖历史
- **`DROP DATABASE` / `DELETE FROM` 不带 WHERE**:数据丢失
- **`chmod 777`**:权限放大
- **`curl ... | bash` / `irm ... | iex`**:不验证就执行远程脚本
- **`mkfs` / `format` / `diskpart`**:格式化磁盘
- **`shutdown` / `restart` / `Stop-Computer`**:关闭主机
- **`reg delete`**:改注册表
- **`net user` / `Add-LocalGroupMember`**:改用户权限
- **`Disable-NetFirewall`**:关防火墙
- **`taskkill /f /im`**:强杀进程无确认
- **`git push --no-verify`**:跳过 hooks
- **任何把密钥 echo 出来的命令**:`echo $API_KEY`、`cat ~/.env`
- **生产数据库迁移命令**:必须人工在 DBA 控制台跑

## 风险说明

| 命令 | 风险 |
|------|------|
| `rm -rf` | 不可恢复的文件删除 |
| `git push -f` | 覆盖他人 commit |
| `DROP DATABASE` | 数据永久丢失 |
| `curl ... | bash` | 执行未审计代码 |
| `chmod 777` | 安全漏洞 |
| `shutdown` | 服务中断 |
| `echo $SECRET` | 密钥泄露到日志 |

## Agent 执行说明

1. **判断命令**:
   - 只读查询? → [允许]
   - 写但可逆? → [需确认]
   - 写不可逆 / 影响外部? → [禁止 或 强确认]
2. **判断目标**:
   - 本地知识库? → 通常 [允许]
   - 远程服务? → [需确认]
   - 生产环境? → [禁止,除非显式授权]
3. **优先 dry-run**:`git status` → `git diff --stat` → 确认 → 执行
4. **避免管道链**:`a | b | c` 难调试,拆开跑
5. **避免 &&**:`a && b && c` 一错全错,用 `;` + 检查每步

## 例子

### 允许

```powershell
> Get-ChildItem D:\valut\trade\agent\01-Skills
```

✅ 直接跑

### 需确认

```powershell
> 我想 git add . && git commit -m "update kb" && git push origin main
```

⚠️ "建议拆开:先 `git status` 看改了什么,确认后 `git add -A`(或指定文件),再 `git commit`,最后单独问要不要 `push`。要继续吗?"

### 禁止

```powershell
> Remove-Item -Recurse -Force D:\valut\trade\agent\01-Skills
```

❌ "禁止。删除整个目录不可逆。即使你认为要重做,也先备份 `Move-Item ... ..._bak_2026-07-09` 再考虑。"

## 相关知识

- [`file-edit-policy.md`](./file-edit-policy.md)
- [`destructive-action-policy.md`](./destructive-action-policy.md)
- [`../00-AgentBase/safety/01-Agent边界与限制.md`](../00-AgentBase/safety/01-Agent边界与限制.md)