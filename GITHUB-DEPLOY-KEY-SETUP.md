# GitHub部署密钥配置指南

## 🔑 部署密钥信息

**项目**: 越南摩托汽车网站  
**GitHub仓库**: https://github.com/zuozhu625/vietmoto.git  
**密钥类型**: ED25519  
**生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

## 📋 GitHub配置步骤

### 1. 复制公钥内容
```bash
cat /root/越南摩托汽车网站/deploy_key.pub
```

**公钥内容**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB91d75kXwJVzHVVKtg1jBhRcpN6aifBzQw43NUgesg9 vietmoto-deploy@github.com
```

### 2. 在GitHub仓库中添加部署密钥

1. 访问仓库: https://github.com/zuozhu625/vietmoto.git
2. 点击 **Settings** 标签页
3. 在左侧菜单中选择 **Deploy keys**
4. 点击 **Add deploy key** 按钮
5. 填写以下信息:
   - **Title**: `VietMoto Deploy Key`
   - **Key**: 粘贴上面的公钥内容
   - **Allow write access**: ✅ 勾选（允许推送）
6. 点击 **Add key** 保存

### 3. 测试部署连接
```bash
# 测试SSH连接
ssh -F /root/越南摩托汽车网站/ssh_config -T git@github.com-vietmoto

# 执行部署
cd /root/越南摩托汽车网站
./git-deploy.sh
```

## 📁 生成的文件

- `deploy_key` - 私钥文件（保密，不要分享）
- `deploy_key.pub` - 公钥文件（添加到GitHub）
- `ssh_config` - SSH配置文件
- `git-deploy.sh` - 自动部署脚本

## 🚀 使用方法

### 自动部署到GitHub
```bash
cd /root/越南摩托汽车网站
./git-deploy.sh
```

### 手动推送
```bash
cd /root/越南摩托汽车网站
git add .
git commit -m "更新内容"
GIT_SSH_COMMAND="ssh -F ssh_config" git push origin master
```

## 🔒 安全注意事项

1. **私钥安全**: `deploy_key` 文件包含私钥，请妥善保管，不要泄露
2. **权限设置**: 私钥文件权限已设置为 600（仅所有者可读写）
3. **定期更新**: 建议定期更换部署密钥以提高安全性

## 🛠️ 故障排除

### 权限被拒绝错误
```bash
# 检查密钥权限
ls -la deploy_key*

# 重新设置权限
chmod 600 deploy_key
chmod 644 deploy_key.pub
```

### SSH连接测试
```bash
# 测试GitHub连接
ssh -F ssh_config -T git@github.com-vietmoto
```

### 查看Git配置
```bash
git remote -v
git config --list
```

---

**配置完成后，您就可以使用 `./git-deploy.sh` 脚本自动部署项目到GitHub仓库了！**
