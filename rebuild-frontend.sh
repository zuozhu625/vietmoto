#!/bin/bash

# 自动重新构建前端脚本
# 当有新的测评或问答生成时，重新构建前端以生成新的静态页面

echo "🔄 开始重新构建前端..."

# 等待后端API就绪
echo "⏳ 等待后端API就绪..."
for i in {1..10}; do
  if curl -s http://localhost:4001/health > /dev/null 2>&1; then
    echo "✅ 后端API已就绪"
    break
  fi
  sleep 1
done

cd /root/越南摩托汽车网站/frontend

# 构建前端
npm run build > /tmp/frontend_rebuild.log 2>&1

if [ $? -eq 0 ]; then
  echo "✅ 前端构建成功"
  
  # 复制到生产环境
  echo "📦 复制文件到生产环境..."
  rm -rf /var/www/vietnam-moto-auto/frontend/dist/*
  cp -r dist/* /var/www/vietnam-moto-auto/frontend/dist/
  
  if [ $? -eq 0 ]; then
    echo "✅ 前端已更新到生产环境"
    echo "📊 时间: $(date '+%Y-%m-%d %H:%M:%S')"
  else
    echo "❌ 复制文件失败"
    exit 1
  fi
else
  echo "❌ 前端构建失败"
  tail -20 /tmp/frontend_rebuild.log
  exit 1
fi

