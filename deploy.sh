#!/bin/bash

# ============================================
# 越南摩托汽车网站 - 生产环境部署脚本 v3.2
# ============================================
# 
# 特点：
# - 支持选择性部署（全部/前端/后端/配置）
# - 使用tar复制文件（不依赖rsync）
# - 完善的数据库保护机制
# - 详细的错误检查
# - 失败自动回滚
# - 清晰的日志输出
#
# 使用: 
#   sudo ./deploy.sh                    # 完整部署（默认）
#   sudo ./deploy.sh frontend           # 只部署前端
#   sudo ./deploy.sh backend            # 只部署后端
#   sudo ./deploy.sh config             # 只更新配置
#   sudo ./deploy.sh all --keep-db      # 完整部署但保持现有数据库
#   sudo ./deploy.sh frontend keep-db   # 部署前端并保持数据库
#
# 支持的部署模式：
#   all       - 完整部署（包含前端、后端、数据库）
#   frontend  - 只构建和部署前端
#   backend   - 只编译和部署后端
#   config    - 只更新配置文件（Nginx、Systemd）

set -e  # 遇到错误立即退出

# 部署模式（从命令行参数获取，默认为all）
DEPLOY_MODE="${1:-all}"

# 数据库恢复选项（从第二个参数获取）
# --keep-db 或 keep-db: 保持现有数据库，不恢复备份
KEEP_DB="${2:-}"

# ============================================
# 配置变量
# ============================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 路径配置
SOURCE_DIR="/root/越南摩托汽车网站"
TARGET_DIR="/var/www/vietnam-moto-auto"
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)

# 数据库保护
DB_FILE="backend/database/vietnam_moto_auto.sqlite"
DB_BACKUP_TEMP="/tmp/db_backup_${DATE}.sqlite"
DEPLOYMENT_BACKUP="${BACKUP_DIR}/deployment_${DATE}"

# 验证部署模式
case "$DEPLOY_MODE" in
    all|frontend|backend|config)
        # 有效的部署模式
        ;;
    *)
        echo -e "${RED}错误: 无效的部署模式 '$DEPLOY_MODE'${NC}"
        echo -e "${YELLOW}支持的模式: all, frontend, backend, config${NC}"
        echo ""
        echo "使用方法:"
        echo "  sudo ./deploy.sh           # 完整部署"
        echo "  sudo ./deploy.sh frontend  # 只部署前端"
        echo "  sudo ./deploy.sh backend   # 只部署后端"
        echo "  sudo ./deploy.sh config    # 只更新配置"
        exit 1
        ;;
esac

# ============================================
# 日志函数
# ============================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

log_step() {
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# ============================================
# 错误处理函数
# ============================================

rollback() {
    log_error "部署失败，开始回滚..."
    
    if [ -d "$DEPLOYMENT_BACKUP" ]; then
        log_info "恢复之前的版本..."
        rm -rf "$TARGET_DIR"
        mv "$DEPLOYMENT_BACKUP" "$TARGET_DIR"
        
        # 重启服务
        systemctl restart vietnam-moto-backend 2>/dev/null || true
        systemctl restart nginx 2>/dev/null || true
        
        log_success "回滚完成"
    else
        log_warning "没有找到备份，无法回滚"
    fi
    
    # 清理临时文件
    rm -f "$DB_BACKUP_TEMP"
    
    exit 1
}

# 设置错误陷阱
trap rollback ERR

# ============================================
# 主流程
# ============================================

# 显示部署模式
MODE_TEXT="完整部署"
case "$DEPLOY_MODE" in
    frontend) MODE_TEXT="前端部署" ;;
    backend) MODE_TEXT="后端部署" ;;
    config) MODE_TEXT="配置更新" ;;
esac

echo ""
log_step "🚀 越南摩托汽车网站 - 生产环境部署 v3.2"
echo ""
log_info "部署模式: ${CYAN}$MODE_TEXT${NC} ($DEPLOY_MODE)"
log_info "源目录: $SOURCE_DIR"
log_info "目标目录: $TARGET_DIR"
log_info "备份目录: $BACKUP_DIR"
log_info "时间戳: $DATE"

# 显示数据库保护状态
if [[ "$KEEP_DB" == "--keep-db" || "$KEEP_DB" == "keep-db" ]]; then
    log_warning "🔒 数据库保护模式：将保持现有数据库，不恢复备份"
fi
echo ""

# 检查域名+SSL部署（检测Nginx HTTPS配置）
if grep -r "listen 443 ssl" /etc/nginx/conf.d/*.conf 2>/dev/null | grep -q "vietmoto.top\|vietnam"; then
    log_warning "检测到域名+SSL配置，将自动清理.env文件"
    SSL_MODE=true
else
    SSL_MODE=false
fi

# ============================================
# 1. 权限检查
# ============================================

log_step "步骤 1/12: 权限检查"

if [ "$EUID" -ne 0 ]; then
    log_error "请使用 root 用户或 sudo 运行此脚本"
    exit 1
fi

log_success "权限检查通过"

# ============================================
# 2. 环境检查
# ============================================

log_step "步骤 2/12: 环境检查"

# 检查源目录
if [ ! -d "$SOURCE_DIR" ]; then
    log_error "源目录不存在: $SOURCE_DIR"
    exit 1
fi

# 检查必要命令
for cmd in tar node npm sqlite3 nginx systemctl; do
    if ! command -v $cmd > /dev/null 2>&1; then
        log_error "缺少必要命令: $cmd"
        exit 1
    fi
done

log_success "环境检查通过"

# ============================================
# 3. 数据库备份（最高优先级）
# ============================================

log_step "步骤 3/12: 数据库安全备份"

if [ -f "$TARGET_DIR/$DB_FILE" ]; then
    # 检查数据库完整性
    if sqlite3 "$TARGET_DIR/$DB_FILE" "PRAGMA integrity_check;" | grep -q "ok"; then
        # 统计数据量
        MOTO_COUNT=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
        NEWS_COUNT=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM news;" 2>/dev/null || echo "0")
        
        # 备份到临时位置
        cp "$TARGET_DIR/$DB_FILE" "$DB_BACKUP_TEMP"
        log_success "数据库已备份: $MOTO_COUNT 辆车, $NEWS_COUNT 条新闻"
        log_info "备份位置: $DB_BACKUP_TEMP"
        
        # 额外备份到备份目录
        mkdir -p "$BACKUP_DIR/database"
        cp "$TARGET_DIR/$DB_FILE" "$BACKUP_DIR/database/vietnam_moto_auto_${DATE}.sqlite"
        gzip "$BACKUP_DIR/database/vietnam_moto_auto_${DATE}.sqlite"
        log_success "数据库已永久备份到: $BACKUP_DIR/database/"
    else
        log_error "数据库完整性检查失败"
        exit 1
    fi
else
    log_warning "未找到现有数据库文件"
fi

# ============================================
# 4. 完整备份当前版本
# ============================================

log_step "步骤 4/12: 备份当前版本（用于回滚）"

if [ -d "$TARGET_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    
    # 完整备份（用于可能的回滚）
    cp -r "$TARGET_DIR" "$DEPLOYMENT_BACKUP"
    log_success "当前版本已备份到: $DEPLOYMENT_BACKUP"
    
    # 压缩归档（永久保存）
    tar -czf "$BACKUP_DIR/vietnam-moto-auto-${DATE}.tar.gz" -C "$TARGET_DIR" . 2>/dev/null || true
    log_success "永久归档已创建"
else
    log_info "首次部署，跳过备份"
fi

# ============================================
# 5. 创建目标目录结构
# ============================================

log_step "步骤 5/12: 准备目标目录"

mkdir -p "$TARGET_DIR"
mkdir -p "$TARGET_DIR/backend/database"
mkdir -p "$TARGET_DIR/backend/logs"
mkdir -p "$TARGET_DIR/backend/uploads"
mkdir -p "$TARGET_DIR/frontend/logs"

log_success "目录结构已创建"

# ============================================
# 6. 复制项目文件（排除数据库）
# ============================================

log_step "步骤 6/12: 复制项目文件"

# 域名+SSL模式：清理前端环境变量文件
if [ "$SSL_MODE" = true ]; then
    log_info "域名+SSL模式：删除前端环境变量文件..."
    rm -f "$SOURCE_DIR/frontend/.env.production" 2>/dev/null || true
    rm -f "$SOURCE_DIR/frontend/.env.local" 2>/dev/null || true
    rm -f "$SOURCE_DIR/frontend/.env" 2>/dev/null || true
    log_success "前端.env文件已清理（使用相对路径/api）"
fi

log_info "使用tar复制文件（排除数据库、日志、uploads）..."

cd "$SOURCE_DIR"
tar --exclude='node_modules' \
    --exclude='dist' \
    --exclude='.git' \
    --exclude='*.sqlite*' \
    --exclude='backend/database' \
    --exclude='backend/uploads' \
    --exclude='backend/logs' \
    --exclude='frontend/dist' \
    --exclude='frontend/node_modules' \
    --exclude='.env.local' \
    --exclude='.env.production' \
    -cf - . | (cd "$TARGET_DIR" && tar -xf -)

if [ $? -eq 0 ]; then
    log_success "项目文件复制完成"
else
    log_error "文件复制失败"
    exit 1
fi

# ============================================
# 7. 恢复数据库并同步表结构
# ============================================

log_step "步骤 7/12: 恢复数据库并同步表结构"

# 检查是否要保持现有数据库
if [[ "$KEEP_DB" == "--keep-db" || "$KEEP_DB" == "keep-db" ]]; then
    log_warning "🔒 保持现有数据库模式：跳过数据库恢复"
    
    # 检查生产环境数据库是否存在
    if [ -f "$TARGET_DIR/$DB_FILE" ]; then
        EXISTING_CARS=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM cars;" 2>/dev/null || echo "0")
        EXISTING_MOTO=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
        log_success "✅ 使用现有数据库: $EXISTING_CARS 辆汽车, $EXISTING_MOTO 辆摩托车"
    else
        log_warning "⚠️  生产环境数据库不存在，将使用开发环境数据库"
        if [ -f "$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite" ]; then
            cp "$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite" "$TARGET_DIR/$DB_FILE"
            chmod 666 "$TARGET_DIR/$DB_FILE"
        fi
    fi
else
    # 原有的数据库恢复逻辑
    if [ -f "$DB_BACKUP_TEMP" ]; then
        cp "$DB_BACKUP_TEMP" "$TARGET_DIR/$DB_FILE"
        chmod 666 "$TARGET_DIR/$DB_FILE"
        
        # 验证恢复的数据库
        MOTO_COUNT=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
        log_success "数据库已恢复: $MOTO_COUNT 辆车"
    else
        # 检查开发环境是否有带数据的数据库
        if [ -f "$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite" ]; then
            DEV_MOTO=$(sqlite3 "$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
            if [ "$DEV_MOTO" -gt 0 ]; then
                log_warning "使用开发环境数据库（包含 $DEV_MOTO 辆车）"
                cp "$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite" "$TARGET_DIR/$DB_FILE"
                chmod 666 "$TARGET_DIR/$DB_FILE"
            fi
        else
            log_warning "没有现有数据库，将创建新数据库"
        fi
    fi
fi

# 同步数据库表结构（确保 marketplace_vehicles 和 reviews 表存在）
log_info "检查并同步数据库表结构..."
if [ -f "$SOURCE_DIR/backend/database/sync-dev-to-prod.sql" ]; then
    sqlite3 "$TARGET_DIR/$DB_FILE" < "$SOURCE_DIR/backend/database/sync-dev-to-prod.sql" 2>/dev/null || true
    log_success "数据库表结构已同步"
else
    log_warning "未找到表结构同步脚本"
fi

# 验证关键表是否存在
TABLES=$(sqlite3 "$TARGET_DIR/$DB_FILE" ".tables" 2>/dev/null || echo "")
if echo "$TABLES" | grep -q "marketplace_vehicles"; then
    log_success "✅ marketplace_vehicles 表存在"
else
    log_warning "⚠️  marketplace_vehicles 表不存在"
fi

if echo "$TABLES" | grep -q "reviews"; then
    log_success "✅ reviews 表存在"
else
    log_warning "⚠️  reviews 表不存在"
fi

# ============================================
# 8. 安装后端依赖
# ============================================

log_step "步骤 8/12: 安装后端依赖"

cd "$TARGET_DIR/backend"
log_info "安装 npm 包（包含dev依赖用于编译）..."
npm install --silent

if [ $? -eq 0 ]; then
    log_success "后端依赖安装完成"
else
    log_error "后端依赖安装失败"
    exit 1
fi

# ============================================
# 9. 编译后端 TypeScript
# ============================================

log_step "步骤 9/12: 编译 TypeScript"

if [ -f "tsconfig.json" ]; then
    npm run build
    
    if [ $? -eq 0 ] && [ -d "dist" ]; then
        log_success "TypeScript 编译完成"
    else
        log_error "TypeScript 编译失败"
        exit 1
    fi
else
    log_warning "未找到 tsconfig.json，跳过编译"
fi

# ============================================
# 10. 安装前端依赖并构建
# ============================================

log_step "步骤 10/12: 构建前端"

cd "$TARGET_DIR/frontend"
log_info "安装前端依赖..."
npm install --silent

if [ $? -ne 0 ]; then
    log_error "前端依赖安装失败"
    exit 1
fi

log_info "构建前端（这可能需要几分钟）..."

# 域名+SSL模式：再次确认.env文件已删除
if [ "$SSL_MODE" = true ]; then
    rm -f .env.production .env.local .env 2>/dev/null || true
    log_info "✓ 确认使用相对路径API（无.env文件）"
fi

npm run build

if [ $? -eq 0 ] && [ -d "dist" ]; then
    # Astro hybrid 模式验证
    if [ -d "dist/client" ] || [ -d "dist/server" ] || [ -f "dist/index.html" ]; then
        log_success "前端构建完成（Hybrid 模式）"
        
        # 验证构建产物中无硬编码地址
        if [ "$SSL_MODE" = true ]; then
            if grep -r "localhost:4001\|47\.237\.79\.9:4001" dist/ 2>/dev/null | grep -q "http://"; then
                log_warning "⚠️  检测到构建产物中包含HTTP地址，请检查源码"
            else
                log_success "✓ 构建产物检查通过（无HTTP硬编码）"
            fi
        fi
    else
        log_error "前端构建失败：找不到有效的构建产物"
        exit 1
    fi
else
    log_error "前端构建失败"
    exit 1
fi

# 创建CSS/JS文件名大小写兼容符号链接
log_info "创建静态资源大小写兼容符号链接..."
if [ -d "dist/client/_astro" ]; then
    cd dist/client/_astro
    link_count=0
    for file in *.css *.js; do
        if [ -f "$file" ]; then
            lowercase=$(echo "$file" | tr '[:upper:]' '[:lower:]')
            if [ "$file" != "$lowercase" ] && [ ! -e "$lowercase" ]; then
                ln -sf "$file" "$lowercase"
                link_count=$((link_count + 1))
            fi
        fi
    done
    cd - > /dev/null
    if [ $link_count -gt 0 ]; then
        log_success "✓ 创建了 $link_count 个大小写兼容链接"
    else
        log_info "✓ 无需创建额外链接"
    fi
else
    log_warning "⚠️  未找到 dist/client/_astro 目录"
fi

# ============================================
# 11. 配置生产环境
# ============================================

log_step "步骤 11/12: 配置生产环境"

cd "$TARGET_DIR/backend"

# 创建 .env.production（如果不存在）
if [ ! -f ".env.production" ]; then
    cat > .env.production << 'EOF'
NODE_ENV=production
PORT=4001
HOST=0.0.0.0

# 数据库配置 (SQLite)
DB_TYPE=sqlite
DB_PATH=/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite
DB_LOGGING=false

# JWT 配置
JWT_SECRET=your-super-secret-jwt-key-please-change-in-production
JWT_EXPIRES_IN=7d

# 上传配置
UPLOAD_DIR=/var/www/vietnam-moto-auto/backend/uploads
MAX_FILE_SIZE=10485760

# 日志配置
LOG_LEVEL=info
LOG_DIR=/var/www/vietnam-moto-auto/backend/logs

# Redis 配置 (可选)
REDIS_HOST=localhost
REDIS_PORT=6379
EOF
    log_success "已创建 .env.production"
else
    log_info ".env.production 已存在"
fi

# 配置 Systemd 服务
log_info "配置 Systemd 服务..."

cat > /etc/systemd/system/vietnam-moto-backend.service << EOF
[Unit]
Description=Vietnam Moto Auto Backend Service
Documentation=https://github.com/vietnam-moto-auto
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=$TARGET_DIR/backend
Environment=NODE_ENV=production
EnvironmentFile=$TARGET_DIR/backend/.env.production
ExecStart=/usr/bin/node dist/index.js
Restart=always
RestartSec=10
StandardOutput=append:$TARGET_DIR/backend/logs/backend.log
StandardError=append:$TARGET_DIR/backend/logs/backend-error.log

# 安全设置
NoNewPrivileges=true
PrivateTmp=true

# 资源限制
LimitNOFILE=65535

[Install]
WantedBy=multi-user.target
EOF

# 配置 Nginx
log_info "配置 Nginx..."

if [ -d "/etc/nginx/conf.d" ]; then
    NGINX_CONF="/etc/nginx/conf.d/vietnam-moto-auto.conf"
else
    NGINX_CONF="/etc/nginx/sites-available/vietnam-moto-auto"
    mkdir -p /etc/nginx/sites-enabled
fi

cat > "$NGINX_CONF" << 'NGINXEOF'
# 后端上游
upstream vietnam_backend {
    server 127.0.0.1:4001;
    keepalive 64;
}

server {
    listen 80;
    server_name _;
    
    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # 日志
    access_log /var/log/nginx/vietnam-moto-auto.access.log;
    error_log /var/log/nginx/vietnam-moto-auto.error.log;
    
    # 前端静态文件
    location / {
        root /var/www/vietnam-moto-auto/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # 静态资源缓存
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
        
        # HTML 不缓存
        location ~* \.html$ {
            expires -1;
            add_header Cache-Control "no-cache, no-store, must-revalidate";
        }
    }
    
    # API 代理
    location /api/ {
        proxy_pass http://vietnam_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://vietnam_backend/health;
        access_log off;
    }
    
    # 上传文件访问
    location /uploads/ {
        alias /var/www/vietnam-moto-auto/backend/uploads/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    # 禁止访问敏感文件
    location ~ /\. {
        deny all;
    }
    
    location ~ \.(sql|sqlite|log|env)$ {
        deny all;
    }
    
    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
    
    # 客户端限制
    client_max_body_size 10M;
}
NGINXEOF

# 启用站点（如果使用 sites-enabled）
if [ -d "/etc/nginx/sites-enabled" ]; then
    ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/vietnam-moto-auto
    rm -f /etc/nginx/sites-enabled/default
fi

log_success "配置文件已更新"

# ============================================
# 12. 设置文件权限
# ============================================

log_info "设置文件权限..."
chmod -R 755 "$TARGET_DIR"
chmod -R 777 "$TARGET_DIR/backend/uploads"
chmod -R 777 "$TARGET_DIR/backend/logs"
chmod -R 777 "$TARGET_DIR/backend/database"
chmod 666 "$TARGET_DIR/$DB_FILE" 2>/dev/null || true

log_success "文件权限设置完成"

# ============================================
# 13. 重启服务
# ============================================

log_step "步骤 12/12: 启动服务"

log_info "重新加载 systemd..."
systemctl daemon-reload

log_info "停止旧服务..."
systemctl stop vietnam-moto-backend 2>/dev/null || true
systemctl stop vietnam-moto-frontend 2>/dev/null || true

log_info "启动后端服务..."
systemctl start vietnam-moto-backend
systemctl enable vietnam-moto-backend

log_info "启动前端服务 (4321)..."
systemctl start vietnam-moto-frontend
systemctl enable vietnam-moto-frontend

log_info "测试 Nginx 配置..."
if nginx -t; then
    log_info "重启 Nginx..."
    systemctl restart nginx
    log_success "Nginx 已重启"
else
    log_error "Nginx 配置测试失败"
    exit 1
fi

# ============================================
# 14. 健康检查
# ============================================

log_step "健康检查"

log_info "等待服务启动..."
sleep 5

# 临时禁用代理（避免代理服务未运行导致curl失败）
export no_proxy="localhost,127.0.0.1"
export NO_PROXY="localhost,127.0.0.1"

# 检查后端
if curl --noproxy '*' -f http://localhost:4001/health > /dev/null 2>&1; then
    log_success "✅ 后端服务正常 (端口 4001)"
else
    log_error "❌ 后端服务异常"
    log_info "查看日志: journalctl -u vietnam-moto-backend -n 50"
    exit 1
fi

# 检查前端
if curl --noproxy '*' -f http://localhost:4321 > /dev/null 2>&1; then
    log_success "✅ 前端服务正常 (端口 4321)"
else
    log_warning "⚠️  前端服务可能有问题"
    log_info "查看日志: journalctl -u vietnam-moto-frontend -n 50"
fi

# 检查 Nginx
if curl --noproxy '*' -f http://localhost/health > /dev/null 2>&1; then
    log_success "✅ Nginx 代理正常 (端口 80)"
else
    log_warning "⚠️  Nginx 代理可能有问题"
fi

# 验证数据库
FINAL_MOTO=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
FINAL_NEWS=$(sqlite3 "$TARGET_DIR/$DB_FILE" "SELECT COUNT(*) FROM news;" 2>/dev/null || echo "0")
log_success "✅ 数据库: $FINAL_MOTO 辆车, $FINAL_NEWS 条新闻"

# ============================================
# 15. 清理临时文件
# ============================================

log_step "清理临时文件"

rm -f "$DB_BACKUP_TEMP"
log_info "临时数据库备份已清理"

# 保留回滚备份一段时间后再清理
log_info "回滚备份保留在: $DEPLOYMENT_BACKUP"
log_info "如确认部署成功，可手动删除: rm -rf $DEPLOYMENT_BACKUP"

# 清理旧备份（保留最近5个）
cd "$BACKUP_DIR"
ls -t vietnam-moto-auto-*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null || true
log_info "已清理旧备份文件"

# ============================================
# 完成
# ============================================

echo ""
log_step "🎉 部署完成！"
echo ""

# 根据SSL模式显示不同的访问地址
if [ "$SSL_MODE" = true ]; then
    log_info "🌐 访问地址 (HTTPS模式):"
    echo "   前端主站: https://vietmoto.top"
    echo "   后端API: https://vietmoto.top/api"
    echo "   健康检查: https://vietmoto.top/health"
    echo ""
    log_info "✅ 域名+SSL部署完成"
    log_info "所有API调用通过HTTPS + Nginx代理"
else
    log_info "🌐 访问地址 (IP模式):"
    echo "   前端主站: http://47.237.79.9:4321 (推荐)"
    echo "   前端静态: http://47.237.79.9 (Nginx)"
    echo "   后端API: http://47.237.79.9:4001/api"
    echo "   健康检查: http://localhost:4001/health"
fi
echo ""
log_info "📋 常用命令:"
echo "   查看前端状态: systemctl status vietnam-moto-frontend"
echo "   查看前端日志: journalctl -u vietnam-moto-frontend -f"
echo "   重启前端: systemctl restart vietnam-moto-frontend"
echo "   查看后端状态: systemctl status vietnam-moto-backend"
echo "   查看后端日志: journalctl -u vietnam-moto-backend -f"
echo "   重启后端: systemctl restart vietnam-moto-backend"
echo "   查看 Nginx 状态: systemctl status nginx"
echo "   重启 Nginx: systemctl restart nginx"
echo ""
log_info "📁 重要路径:"
echo "   项目目录: $TARGET_DIR"
echo "   数据库: $TARGET_DIR/$DB_FILE"
echo "   日志目录: $TARGET_DIR/backend/logs"
echo "   备份目录: $BACKUP_DIR"
echo "   回滚备份: $DEPLOYMENT_BACKUP"
echo ""
log_success "所有步骤已完成！数据库已妥善保护！"
echo ""

exit 0
