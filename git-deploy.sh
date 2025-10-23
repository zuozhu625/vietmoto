#!/bin/bash

# 越南摩托汽车网站 - GitHub部署脚本
# 使用部署密钥推送到GitHub仓库

set -e

PROJECT_DIR="/root/越南摩托汽车网站"
DEPLOY_KEY="$PROJECT_DIR/deploy_key"
SSH_CONFIG="$PROJECT_DIR/ssh_config"

echo "🚀 开始部署到GitHub仓库..."

# 检查部署密钥是否存在
if [ ! -f "$DEPLOY_KEY" ]; then
    echo "❌ 错误: 部署密钥不存在: $DEPLOY_KEY"
    exit 1
fi

# 设置正确的密钥权限
chmod 600 "$DEPLOY_KEY"
chmod 644 "$DEPLOY_KEY.pub"

# 进入项目目录
cd "$PROJECT_DIR"

# 配置Git用户信息（如果未配置）
git config user.name "VietMoto Deploy" 2>/dev/null || git config user.name "VietMoto Deploy"
git config user.email "vietmoto-deploy@github.com" 2>/dev/null || git config user.email "vietmoto-deploy@github.com"

# 添加所有文件到Git
echo "📦 添加文件到Git..."
git add .

# 检查是否有更改需要提交
if git diff --staged --quiet; then
    echo "ℹ️  没有新的更改需要提交"
else
    # 提交更改
    COMMIT_MSG="部署更新 - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "💾 提交更改: $COMMIT_MSG"
    git commit -m "$COMMIT_MSG"
fi

# 使用SSH配置推送到GitHub
echo "🔄 推送到GitHub仓库..."
GIT_SSH_COMMAND="ssh -F $SSH_CONFIG" git push -u origin master

echo "✅ 成功部署到GitHub仓库!"
echo "🔗 仓库地址: https://github.com/zuozhu625/vietmoto.git"
