# 🚀 GitHub部署与版本控制指南

## 📋 项目概述

**项目名称**: 越南摩托汽车网站 (VietMoto)  
**GitHub仓库**: https://github.com/zuozhu625/vietmoto.git  
**部署时间**: 2025-10-23 19:47:00  
**项目状态**: ✅ 已成功上传到GitHub

## 🔑 部署密钥配置

### 生成的SSH密钥信息
- **密钥类型**: ED25519
- **密钥用途**: GitHub部署专用
- **公钥文件**: `deploy_key.pub`
- **私钥文件**: `deploy_key` (已加入.gitignore)

### GitHub Deploy Key配置步骤

1. **访问仓库设置**
   ```
   https://github.com/zuozhu625/vietmoto/settings/keys
   ```

2. **添加部署密钥**
   - 点击 "Add deploy key"
   - Title: `VietMoto Deploy Key`
   - Key: 复制 `deploy_key.pub` 的内容
   - ✅ 勾选 "Allow write access"

3. **公钥内容**
   ```
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB91d75kXwJVzHVVKtg1jBhRcpN6aifBzQw43NUgesg9 vietmoto-deploy@github.com
   ```

## 📁 项目结构

```
越南摩托汽车网站/
├── backend/                    # 后端服务
│   ├── src/                   # 源代码
│   ├── database/              # 数据库文件
│   └── package.json           # 依赖配置
├── frontend/                  # 前端应用 (Astro)
├── docs/                      # 项目文档
├── nginx/                     # Nginx配置
├── systemd/                   # 系统服务配置
├── scripts/                   # 部署脚本
├── database/                  # 数据库迁移
├── deploy.sh                  # 主部署脚本
├── git-deploy.sh             # Git部署脚本
└── .gitignore                # Git忽略文件
```

## 🛠️ 部署命令

### 自动部署到GitHub
```bash
cd /root/越南摩托汽车网站
./git-deploy.sh
```

### 手动Git操作
```bash
# 添加文件
git add .

# 提交更改
git commit -m "更新描述"

# 推送到GitHub
GIT_SSH_COMMAND="ssh -F ssh_config" git push origin master
```

### 生产环境部署
```bash
# 完整部署
./deploy.sh

# 快速部署
./quick-deploy.sh

# 保持数据库部署
./deploy-keep-db.sh
```

## 📊 上传统计

### 文件统计
- **总文件数**: 161个文件
- **代码行数**: 72,951行
- **主要组件**:
  - 后端TypeScript文件: 45个
  - 前端组件: 1个子模块
  - 文档文件: 14个
  - 配置文件: 12个
  - 脚本文件: 15个

### 主要目录
| 目录 | 文件数 | 描述 |
|------|--------|------|
| `backend/src/` | 45+ | 后端源代码 |
| `docs/` | 14 | 项目文档 |
| `backend/src/scripts/` | 20+ | 数据导入脚本 |
| `backend/src/scripts/crawlers/` | 15+ | 爬虫脚本 |
| `nginx/` | 1 | Web服务器配置 |
| `systemd/` | 1 | 系统服务配置 |

## 🔄 版本控制工作流

### 开发流程
1. **本地开发**
   ```bash
   # 修改代码
   git add .
   git commit -m "功能描述"
   ```

2. **推送到GitHub**
   ```bash
   ./git-deploy.sh
   ```

3. **生产部署**
   ```bash
   ./deploy.sh
   ```

### 分支策略
- **master**: 主分支，生产环境代码
- **develop**: 开发分支（可选）
- **feature/***: 功能分支（可选）

## 🔒 安全配置

### 敏感文件保护
以下文件已加入 `.gitignore`:
```
# SSH密钥和部署文件
deploy_key
deploy_key.pub
ssh_config
*.private
*.secret

# 环境变量
.env
.env.local
.env.production

# 数据库文件
*.db
*.sqlite
*.sqlite3
```

### 权限设置
```bash
# 密钥文件权限
chmod 600 deploy_key
chmod 644 deploy_key.pub

# 脚本执行权限
chmod +x *.sh
```

## 📋 部署检查清单

### 部署前检查
- [ ] 代码已提交到Git
- [ ] 环境变量已配置
- [ ] 数据库已备份
- [ ] 依赖包已安装
- [ ] 配置文件已更新

### 部署后验证
- [ ] 服务正常启动
- [ ] API接口可访问
- [ ] 前端页面正常
- [ ] 数据库连接正常
- [ ] SSL证书有效

## 🚨 故障排除

### 常见问题

1. **SSH连接失败**
   ```bash
   # 测试连接
   ssh -F ssh_config -T git@github.com-vietmoto
   
   # 检查密钥权限
   ls -la deploy_key*
   ```

2. **推送被拒绝**
   ```bash
   # 检查远程地址
   git remote -v
   
   # 重新设置远程地址
   git remote set-url origin git@github.com-vietmoto:zuozhu625/vietmoto.git
   ```

3. **部署失败**
   ```bash
   # 检查服务状态
   systemctl status vietnam-moto-backend
   
   # 查看日志
   journalctl -u vietnam-moto-backend -f
   ```

## 📞 支持信息

### 相关文档
- [项目架构文档](./项目架构开发文档.md)
- [生产环境部署文档](./生产环境部署文档.md)
- [后端服务开发文档](./后端服务开发文档.md)

### 联系方式
- **项目维护**: VietMoto Team
- **技术支持**: vietmoto-deploy@github.com
- **GitHub Issues**: https://github.com/zuozhu625/vietmoto/issues

---

## 🎉 部署成功！

✅ **项目已成功上传到GitHub仓库**  
🔗 **仓库地址**: https://github.com/zuozhu625/vietmoto.git  
📅 **部署时间**: 2025-10-23 19:47:00  
🚀 **状态**: 生产就绪

现在您可以通过GitHub进行版本控制，并使用提供的脚本进行自动化部署！
