#!/bin/bash
# 部署检查清单脚本

echo "╔══════════════════════════════════════════════════════════╗"
echo "║       越南摩托汽车网站 - 部署检查清单 v2.1             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 1. 配置文件检查
echo "📋 1. 配置文件检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查Astro配置
if grep -q "host: '0.0.0.0'" /root/越南摩托汽车网站/frontend/astro.config.mjs; then
    echo "  ✅ astro.config.mjs - host配置正确"
else
    echo "  ❌ astro.config.mjs - 缺少 host: '0.0.0.0' 配置"
fi

# 检查环境变量
if [ -f "/root/越南摩托汽车网站/frontend/.env.production" ]; then
    echo "  ✅ .env.production - 文件存在"
else
    echo "  ❌ .env.production - 文件不存在"
fi

# 检查Nginx配置
if grep -q "server_name 47.237.79.9" /root/越南摩托汽车网站/nginx/vietnam-moto-auto.conf; then
    echo "  ✅ nginx配置 - server_name正确"
else
    echo "  ⚠️ nginx配置 - server_name可能需要修改"
fi

echo ""

# 2. 服务状态检查
echo "🚀 2. 服务状态检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
FRONTEND=$(systemctl is-active vietnam-moto-frontend 2>/dev/null || echo "inactive")
BACKEND=$(systemctl is-active vietnam-moto-backend 2>/dev/null || echo "inactive")
NGINX=$(systemctl is-active nginx 2>/dev/null || echo "inactive")

if [ "$FRONTEND" = "active" ]; then
    echo "  ✅ 前端服务 (4321) - $FRONTEND"
else
    echo "  ❌ 前端服务 (4321) - $FRONTEND"
fi

if [ "$BACKEND" = "active" ]; then
    echo "  ✅ 后端服务 (4001) - $BACKEND"
else
    echo "  ❌ 后端服务 (4001) - $BACKEND"
fi

if [ "$NGINX" = "active" ]; then
    echo "  ✅ Nginx服务 (80) - $NGINX"
else
    echo "  ❌ Nginx服务 (80) - $NGINX"
fi

echo ""

# 3. 端口监听检查
echo "📡 3. 端口监听检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if netstat -tln | grep -q "0.0.0.0:4321"; then
    echo "  ✅ 4321端口 - 监听所有接口 (0.0.0.0)"
elif netstat -tln | grep -q "::1:4321"; then
    echo "  ⚠️ 4321端口 - 只监听本地 (::1) - 需要修复！"
else
    echo "  ❌ 4321端口 - 未监听"
fi

if netstat -tln | grep -q ":4001"; then
    echo "  ✅ 4001端口 - 正在监听"
else
    echo "  ❌ 4001端口 - 未监听"
fi

if netstat -tln | grep -q ":80"; then
    echo "  ✅ 80端口 - 正在监听"
else
    echo "  ❌ 80端口 - 未监听"
fi

echo ""

# 4. 数据库检查
echo "🗄️ 4. 数据库检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
DB_FILE="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"
if [ -f "$DB_FILE" ]; then
    MOTO_COUNT=$(sqlite3 "$DB_FILE" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
    DB_SIZE=$(du -h "$DB_FILE" | awk '{print $1}')
    echo "  ✅ 数据库文件存在 ($DB_SIZE)"
    echo "  ✅ 摩托车数量: $MOTO_COUNT 款"
else
    echo "  ❌ 数据库文件不存在"
fi

echo ""

# 5. 访问测试
echo "🌐 5. 访问测试"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 测试4321端口
if curl -sf http://localhost:4321/ > /dev/null 2>&1; then
    echo "  ✅ 前端主站 (4321) - 可访问"
else
    echo "  ❌ 前端主站 (4321) - 无法访问"
fi

# 测试后端健康检查
if curl -sf http://localhost:4001/health > /dev/null 2>&1; then
    echo "  ✅ 后端健康检查 (4001) - 正常"
else
    echo "  ❌ 后端健康检查 (4001) - 失败"
fi

# 测试Nginx
if curl -sf http://localhost/ > /dev/null 2>&1; then
    echo "  ✅ Nginx静态站 (80) - 可访问"
else
    echo "  ⚠️ Nginx静态站 (80) - 可能有问题"
fi

echo ""

# 6. 部署脚本检查
echo "🔧 6. 部署脚本检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
FRONTEND_COUNT=$(grep -c "vietnam-moto-frontend" /root/越南摩托汽车网站/deploy.sh)
if [ $FRONTEND_COUNT -ge 3 ]; then
    echo "  ✅ deploy.sh包含前端服务配置 ($FRONTEND_COUNT 处)"
else
    echo "  ⚠️ deploy.sh可能缺少前端服务配置"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    检查完成！                            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📌 访问地址:"
echo "   主要入口: http://47.237.79.9:4321"
echo "   备用入口: http://47.237.79.9"
echo "   后端API:  http://47.237.79.9:4001/api"
echo ""
