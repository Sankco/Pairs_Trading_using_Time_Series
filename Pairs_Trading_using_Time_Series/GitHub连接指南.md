# GitHub连接设置指南

## 1. 配置Git用户信息

首先配置你的Git用户信息（替换为你的GitHub用户名和邮箱）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的邮箱@example.com"
```

## 2. 选择连接方式

### 方式A: HTTPS连接（推荐新手）

1. **克隆仓库**：
```bash
git clone https://github.com/用户名/仓库名.git
```

2. **首次推送时输入凭据**：
```bash
git push origin main
```
系统会提示输入GitHub用户名和Personal Access Token

3. **创建Personal Access Token**：
   - 访问 GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token"
   - 选择权限：repo, workflow, write:packages
   - 复制生成的token（只显示一次）

### 方式B: SSH连接（推荐经验用户）

1. **生成SSH密钥**：
```bash
ssh-keygen -t ed25519 -C "你的邮箱@example.com"
```
按Enter使用默认路径，可以设置密码（推荐）

2. **启动SSH agent**：
```bash
# Windows (在Git Bash中)
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 或在PowerShell中
Start-Service ssh-agent
ssh-add C:\Users\你的用户名\.ssh\id_ed25519
```

3. **添加SSH密钥到GitHub**：
```bash
# 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# 或在Windows中
type C:\Users\你的用户名\.ssh\id_ed25519.pub
```
   - 访问 GitHub.com → Settings → SSH and GPG keys
   - 点击 "New SSH key"
   - 粘贴公钥内容

4. **测试SSH连接**：
```bash
ssh -T git@github.com
```

## 3. 初始化现有项目到GitHub

如果你想把当前项目上传到GitHub：

1. **在GitHub上创建新仓库**（不要初始化README）

2. **在项目目录中初始化Git**：
```bash
git init
git add .
git commit -m "Initial commit"
```

3. **连接到GitHub仓库**：
```bash
# HTTPS方式
git remote add origin https://github.com/用户名/仓库名.git

# 或SSH方式
git remote add origin git@github.com:用户名/仓库名.git
```

4. **推送代码**：
```bash
git branch -M main
git push -u origin main
```

## 4. 常用Git命令

```bash
# 查看状态
git status

# 添加文件
git add 文件名
git add .  # 添加所有文件

# 提交更改
git commit -m "提交信息"

# 推送到GitHub
git push

# 拉取最新更改
git pull

# 查看提交历史
git log --oneline

# 切换分支
git checkout 分支名
git checkout -b 新分支名  # 创建并切换
```

## 5. 项目专用设置

对于你的Pairs Trading项目，建议的仓库结构：

```
Pairs_Trading_using_Time_Series/
├── .gitignore          # 忽略不需要跟踪的文件
├── README.md           # 项目说明
├── requirements.txt    # Python依赖
├── src/               # 源代码
├── data/              # 数据文件（可能需要在.gitignore中排除）
├── notebooks/         # Jupyter notebooks
└── docs/              # 文档
```

## 6. 重要提示

- **不要上传敏感信息**：API密钥、密码等
- **使用.gitignore**：排除临时文件、数据文件等
- **定期备份**：经常提交和推送代码
- **写好提交信息**：清楚描述每次更改的内容

## 故障排除

### 问题1: Git命令未找到
重新打开终端或重启计算机

### 问题2: 权限被拒绝
确保使用正确的Personal Access Token或SSH密钥

### 问题3: 远程仓库不存在
检查仓库URL是否正确，确保仓库已创建

### 问题4: 合并冲突
```bash
git status  # 查看冲突文件
# 手动编辑解决冲突
git add 解决冲突的文件
git commit -m "解决合并冲突"
``` 