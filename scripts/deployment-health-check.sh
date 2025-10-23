#!/bin/bash

# ============================================
# 越南摩托汽车网站 - 部署健康检查脚本
# ============================================
# 
# 功能：
# - 全面检查部署环境配置
# - 发现潜在问题并提供修复建议
# - 验证前后端API连接
# - 检查常见配置错误
#
# 使用: 
#   sudo ./deployment-health-check.sh
#

set +e  # 允许命令失败以便收集所有问题

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 问题计数器
ISSUES_FOUND=0
WARNINGS_FOUND=0

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
    ((WARNINGS_FOUND++))
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
    ((ISSUES_FOUND++))
}

log_section() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

echo ""
log_section "🔍 越南摩托汽车网站 - 部署健康检查"
echo ""
log_info "检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# ============================================
# 1. 检查前端API配置
# ============================================

log_section "1️⃣  检查前端API配置"

# 检查环境变量文件
if [ -f "/root/越南摩托汽车网站/frontend/.env.production" ]; then
    log_warning "发现.env.production文件（域名+SSL部署时应删除）"
    log_info "  → 域名+SSL模式应使用相对路径/api，不需要环境变量"
    log_info "  → 建议: rm /root/越南摩托汽车网站/frontend/.env.production"
elif [ -f "/root/越南摩托汽车网站/frontend/.env" ]; then
    log_warning "发现.env文件"
else
    log_success "无环境变量文件（推荐配置）"
fi

# 检查硬编码的HTTP地址
log_info "检查前端代码中的硬编码地址..."
HARDCODED=$(grep -r "localhost:4001\|47\.237\.79\.9" /root/越南摩托汽车网站/frontend/src/ 2>/dev/null | grep -v "sitemap" | grep -v "\.astro" | grep -v "//")

if [ ! -z "$HARDCODED" ]; then
    log_error "发现硬编码HTTP地址（客户端代码不应包含）"
    echo "$HARDCODED" | head -3
    log_info "  → SSR页面（.astro）使用localhost:4001是正确的"
    log_info "  → 客户端代码（.ts/.tsx）应使用相对路径/api"
else
    log_success "未发现硬编码HTTP地址（客户端代码）"
fi

# 检查API调用配置
API_CONFIG_FILES=(
    "/root/越南摩托汽车网站/frontend/src/services/marketplaceApi.ts"
    "/root/越南摩托汽车网站/frontend/src/services/reviewsApi.ts"
    "/root/越南摩托汽车网站/frontend/src/services/qaApi.ts"
    "/root/越南摩托汽车网站/frontend/src/lib/api/carsApi.ts"
    "/root/越南摩托汽车网站/frontend/src/lib/api/motorcyclesApi.ts"
)

log_info "检查API服务文件配置..."
for file in "${API_CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        if grep -q "const API_BASE_URL = '/api'" "$file" || grep -q "const API_URL = '/api'" "$file"; then
            log_success "$(basename $file) 使用相对路径 ✓"
        else
            log_error "$(basename $file) 未使用相对路径"
            log_info "  → 应包含: const API_BASE_URL = '/api'"
        fi
    fi
done

# ============================================
# 2. 检查后端配置
# ============================================

log_section "2️⃣  检查后端配置"

# 检查后端路由注册
log_info "检查后端路由注册..."
BACKEND_INDEX="/root/越南摩托汽车网站/backend/src/index.ts"

if [ -f "$BACKEND_INDEX" ]; then
    if grep -q "app.use('/api/sitemap', sitemapRoutes)" "$BACKEND_INDEX"; then
        log_success "Sitemap路由已注册"
    else
        log_error "Sitemap路由未注册"
        log_info "  → 需要添加: app.use('/api/sitemap', sitemapRoutes)"
    fi
    
    if grep -q "import sitemapRoutes from './routes/sitemap'" "$BACKEND_INDEX"; then
        log_success "Sitemap路由已导入"
    else
        log_error "Sitemap路由未导入"
    fi
else
    log_error "未找到backend/src/index.ts"
fi

# 检查sitemap路由文件
if [ -f "/root/越南摩托汽车网站/backend/src/routes/sitemap.ts" ]; then
    log_success "sitemap.ts路由文件存在"
else
    log_error "sitemap.ts路由文件不存在"
    log_info "  → 需要创建: backend/src/routes/sitemap.ts"
fi

# 检查CORS配置
if grep -q "https://vietmoto.top" "$BACKEND_INDEX" 2>/dev/null; then
    log_success "CORS配置包含生产域名"
else
    log_warning "CORS配置可能缺少生产域名"
    log_info "  → 建议添加: 'https://vietmoto.top' 到allowedOrigins"
fi

# ============================================
# 3. 检查Nginx配置
# ============================================

log_section "3️⃣  检查Nginx配置"

NGINX_CONF="/root/越南摩托汽车网站/nginx/vietnam-moto-auto.conf"

if [ -f "$NGINX_CONF" ]; then
    log_success "Nginx配置文件存在"
    
    # 检查API代理配置
    if grep -q "location /api/" "$NGINX_CONF"; then
        log_success "API代理配置存在"
        
        if grep -q "proxy_pass http://127.0.0.1:4001" "$NGINX_CONF"; then
            log_success "API代理指向正确端口"
        else
            log_error "API代理端口配置错误"
        fi
    else
        log_error "缺少API代理配置"
    fi
    
    # 检查server_name
    if grep -q "server_name _" "$NGINX_CONF"; then
        log_warning "使用通配符server_name（可能被其他配置覆盖）"
        log_info "  → 建议使用具体IP或域名: server_name 47.237.79.9 localhost"
    elif grep -q "server_name 47.237.79.9" "$NGINX_CONF" || grep -q "server_name vietmoto.top" "$NGINX_CONF"; then
        log_success "server_name配置正确"
    fi
else
    log_error "Nginx配置文件不存在"
fi

# 检查生产环境Nginx配置
if [ -f "/etc/nginx/conf.d/vietnam-moto-auto.conf" ] || [ -f "/etc/nginx/sites-enabled/vietnam-moto-auto" ]; then
    log_success "生产环境Nginx配置存在"
else
    log_warning "生产环境Nginx配置未找到"
fi

# ============================================
# 4. 检查Systemd服务
# ============================================

log_section "4️⃣  检查Systemd服务配置"

# 检查后端服务文件
BACKEND_SERVICE="/root/越南摩托汽车网站/systemd/vietnam-moto-backend.service"

if [ -f "$BACKEND_SERVICE" ]; then
    log_success "后端服务配置文件存在"
    
    # 检查ExecStart路径
    if grep -q "ExecStart=/usr/bin/node src/index.js" "$BACKEND_SERVICE"; then
        log_error "后端服务启动路径错误（应该是dist/index.js）"
        log_info "  → 应该是: ExecStart=/usr/bin/node dist/index.js"
    elif grep -q "ExecStart=/usr/bin/node dist/index.js" "$BACKEND_SERVICE"; then
        log_success "后端服务启动路径正确"
    fi
    
    # 检查数据库路径
    if grep -q "DB_PATH=.*database.sqlite" "$BACKEND_SERVICE"; then
        log_warning "数据库路径可能不正确"
        log_info "  → 应该是: /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"
    fi
else
    log_error "后端服务配置文件不存在"
fi

# 检查前端服务配置
if [ -f "/etc/systemd/system/vietnam-moto-frontend.service" ]; then
    log_success "前端服务配置存在"
    
    # 检查监听地址
    if grep -q "HOST=0.0.0.0" "/etc/systemd/system/vietnam-moto-frontend.service" 2>/dev/null; then
        log_success "前端服务监听所有接口"
    else
        log_warning "前端服务可能只监听localhost"
        log_info "  → 确保astro.config.mjs中: server: { host: '0.0.0.0' }"
    fi
else
    log_warning "前端服务配置文件不存在"
fi

# ============================================
# 5. 检查运行时状态
# ============================================

log_section "5️⃣  检查运行时状态"

# 检查服务状态
if systemctl is-active vietnam-moto-backend >/dev/null 2>&1; then
    log_success "后端服务正在运行"
else
    log_error "后端服务未运行"
    log_info "  → 启动: sudo systemctl start vietnam-moto-backend"
fi

if systemctl is-active vietnam-moto-frontend >/dev/null 2>&1; then
    log_success "前端服务正在运行"
else
    log_warning "前端服务未运行"
    log_info "  → 启动: sudo systemctl start vietnam-moto-frontend"
fi

if systemctl is-active nginx >/dev/null 2>&1; then
    log_success "Nginx服务正在运行"
else
    log_error "Nginx服务未运行"
fi

# 检查端口监听
log_info "检查端口监听状态..."

if netstat -tlnp 2>/dev/null | grep -q ":4001 "; then
    log_success "后端API端口4001正在监听"
else
    log_error "后端API端口4001未监听"
fi

if netstat -tlnp 2>/dev/null | grep -q ":4321 "; then
    LISTEN_ADDR=$(netstat -tlnp 2>/dev/null | grep ":4321 " | awk '{print $4}')
    if echo "$LISTEN_ADDR" | grep -q "0.0.0.0:4321"; then
        log_success "前端端口4321监听所有接口"
    else
        log_warning "前端端口4321只监听本地: $LISTEN_ADDR"
        log_info "  → 检查astro.config.mjs: server: { host: '0.0.0.0' }"
    fi
else
    log_warning "前端端口4321未监听"
fi

if netstat -tlnp 2>/dev/null | grep -q ":80 "; then
    log_success "Nginx端口80正在监听"
else
    log_error "Nginx端口80未监听"
fi

# ============================================
# 6. API连通性测试
# ============================================

log_section "6️⃣  API连通性测试"

# 测试后端健康检查
if curl --noproxy '*' -f -s http://localhost:4001/health >/dev/null 2>&1; then
    log_success "后端健康检查通过"
else
    log_error "后端健康检查失败"
    log_info "  → 检查后端服务日志: journalctl -u vietnam-moto-backend -n 50"
fi

# 测试Sitemap API
if curl --noproxy '*' -f -s http://localhost:4001/api/sitemap/motorcycles >/dev/null 2>&1; then
    log_success "Sitemap API可访问"
else
    log_error "Sitemap API不可访问"
    log_info "  → 确认sitemap路由已注册"
fi

# 测试前端
if curl --noproxy '*' -f -s http://localhost:4321 >/dev/null 2>&1; then
    log_success "前端页面可访问"
else
    log_warning "前端页面不可访问"
fi

# 测试Nginx代理
if curl --noproxy '*' -f -s http://localhost/health >/dev/null 2>&1; then
    log_success "Nginx代理正常"
else
    log_warning "Nginx代理可能有问题"
fi

# ============================================
# 7. 检查数据库
# ============================================

log_section "7️⃣  检查数据库状态"

DB_DEV="/root/越南摩托汽车网站/backend/database/vietnam_moto_auto.sqlite"
DB_PROD="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"

if [ -f "$DB_DEV" ]; then
    log_success "开发环境数据库存在"
    MOTO_COUNT=$(sqlite3 "$DB_DEV" "SELECT COUNT(*) FROM motorcycles WHERE status='active';" 2>/dev/null || echo "0")
    CAR_COUNT=$(sqlite3 "$DB_DEV" "SELECT COUNT(*) FROM cars WHERE status='active';" 2>/dev/null || echo "0")
    log_info "  → 摩托车: $MOTO_COUNT 辆, 汽车: $CAR_COUNT 辆"
else
    log_warning "开发环境数据库不存在"
fi

if [ -f "$DB_PROD" ]; then
    log_success "生产环境数据库存在"
    MOTO_COUNT=$(sqlite3 "$DB_PROD" "SELECT COUNT(*) FROM motorcycles WHERE status='active';" 2>/dev/null || echo "0")
    CAR_COUNT=$(sqlite3 "$DB_PROD" "SELECT COUNT(*) FROM cars WHERE status='active';" 2>/dev/null || echo "0")
    MARKET_COUNT=$(sqlite3 "$DB_PROD" "SELECT COUNT(*) FROM marketplace_vehicles WHERE status='active';" 2>/dev/null || echo "0")
    log_info "  → 摩托车: $MOTO_COUNT 辆, 汽车: $CAR_COUNT 辆, 二手市场: $MARKET_COUNT 条"
    
    # 检查关键表是否存在
    TABLES=$(sqlite3 "$DB_PROD" ".tables" 2>/dev/null || echo "")
    if echo "$TABLES" | grep -q "marketplace_vehicles"; then
        log_success "marketplace_vehicles表存在"
    else
        log_error "marketplace_vehicles表不存在"
        log_info "  → 运行数据库同步脚本"
    fi
else
    log_warning "生产环境数据库不存在"
fi

# ============================================
# 8. 检查关键文件
# ============================================

log_section "8️⃣  检查关键文件"

CRITICAL_FILES=(
    "/root/越南摩托汽车网站/backend/src/routes/sitemap.ts"
    "/root/越南摩托汽车网站/frontend/src/pages/sitemap-index.xml.ts"
    "/root/越南摩托汽车网站/frontend/src/pages/sitemap-motorcycles.xml.ts"
    "/root/越南摩托汽车网站/frontend/src/pages/sitemap-cars.xml.ts"
    "/root/越南摩托汽车网站/frontend/src/pages/sitemap-reviews.xml.ts"
    "/root/越南摩托汽车网站/frontend/src/pages/sitemap-marketplace.xml.ts"
    "/root/越南摩托汽车网站/frontend/public/robots.txt"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        log_success "$(basename $file) 存在"
    else
        log_error "$(basename $file) 不存在"
    fi
done

# ============================================
# 总结
# ============================================

log_section "📊 检查总结"

echo ""
if [ $ISSUES_FOUND -eq 0 ] && [ $WARNINGS_FOUND -eq 0 ]; then
    log_success "🎉 恭喜！未发现任何问题，部署环境健康！"
elif [ $ISSUES_FOUND -eq 0 ]; then
    log_success "✅ 未发现严重问题"
    log_warning "⚠️  发现 $WARNINGS_FOUND 个警告（建议修复）"
else
    log_error "❌ 发现 $ISSUES_FOUND 个问题需要修复"
    log_warning "⚠️  发现 $WARNINGS_FOUND 个警告"
    echo ""
    log_info "建议按以下顺序修复："
    log_info "1. 修复代码配置问题（API路径、环境变量）"
    log_info "2. 更新服务配置文件"
    log_info "3. 重新部署: sudo ./deploy.sh"
    log_info "4. 验证服务状态"
fi

echo ""
log_info "💡 常用修复命令："
echo "   1. 查看后端日志: journalctl -u vietnam-moto-backend -n 100"
echo "   2. 查看前端日志: journalctl -u vietnam-moto-frontend -n 100"
echo "   3. 重启后端: sudo systemctl restart vietnam-moto-backend"
echo "   4. 重启前端: sudo systemctl restart vietnam-moto-frontend"
echo "   5. 重新部署: cd /root/越南摩托汽车网站 && sudo ./deploy.sh"
echo ""

exit $ISSUES_FOUND

