#!/bin/bash

# ============================================
# 部署前环境检查脚本
# ============================================
# 用途：在实际部署前检查所有依赖和配置
# 使用：./pre-deploy-check.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
SOURCE_DIR="/root/越南摩托汽车网站"
DEV_DB="$SOURCE_DIR/backend/database/vietnam_moto_auto.sqlite"
PROD_DB="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

ERRORS=0
WARNINGS=0

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔍 部署前环境检查${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================
# 1. 检查必要命令
# ============================================
echo "【1/8】检查系统命令..."
for cmd in node npm sqlite3 nginx systemctl tar gzip; do
    if command -v $cmd > /dev/null 2>&1; then
        VERSION=$(${cmd} --version 2>/dev/null | head -1 || echo "unknown")
        log_success "$cmd: $VERSION"
    else
        log_error "缺少命令: $cmd"
        ERRORS=$((ERRORS + 1))
    fi
done

# ============================================
# 2. 检查 Node.js 版本
# ============================================
echo ""
echo "【2/8】检查 Node.js 版本..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -ge 18 ]; then
    log_success "Node.js 版本: v$NODE_VERSION (满足要求 >= 18)"
else
    log_error "Node.js 版本过低: v$NODE_VERSION (需要 >= 18)"
    ERRORS=$((ERRORS + 1))
fi

# ============================================
# 3. 检查项目目录
# ============================================
echo ""
echo "【3/8】检查项目目录..."
if [ -d "$SOURCE_DIR/frontend" ]; then
    log_success "前端目录存在"
else
    log_error "前端目录不存在"
    ERRORS=$((ERRORS + 1))
fi

if [ -d "$SOURCE_DIR/backend" ]; then
    log_success "后端目录存在"
else
    log_error "后端目录不存在"
    ERRORS=$((ERRORS + 1))
fi

# ============================================
# 4. 检查配置文件
# ============================================
echo ""
echo "【4/8】检查配置文件..."
if [ -f "$SOURCE_DIR/frontend/package.json" ]; then
    log_success "frontend/package.json 存在"
else
    log_error "frontend/package.json 不存在"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$SOURCE_DIR/backend/package.json" ]; then
    log_success "backend/package.json 存在"
else
    log_error "backend/package.json 不存在"
    ERRORS=$((ERRORS + 1))
fi

if [ -f "$SOURCE_DIR/backend/tsconfig.json" ]; then
    log_success "backend/tsconfig.json 存在"
else
    log_warning "backend/tsconfig.json 不存在"
    WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# 5. 检查开发环境数据库
# ============================================
echo ""
echo "【5/8】检查开发环境数据库..."
if [ -f "$DEV_DB" ]; then
    # 检查完整性
    if sqlite3 "$DEV_DB" "PRAGMA integrity_check;" | grep -q "ok"; then
        log_success "开发数据库完整性验证通过"
        
        # 统计数据
        MOTO_COUNT=$(sqlite3 "$DEV_DB" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
        CARS_COUNT=$(sqlite3 "$DEV_DB" "SELECT COUNT(*) FROM cars;" 2>/dev/null || echo "0")
        MARKET_COUNT=$(sqlite3 "$DEV_DB" "SELECT COUNT(*) FROM marketplace_vehicles;" 2>/dev/null || echo "0")
        QA_COUNT=$(sqlite3 "$DEV_DB" "SELECT COUNT(*) FROM questions;" 2>/dev/null || echo "0")
        
        log_info "  - 摩托车: $MOTO_COUNT 条"
        log_info "  - 汽车: $CARS_COUNT 条"
        log_info "  - 二手交易: $MARKET_COUNT 条"
        log_info "  - 问答: $QA_COUNT 条"
        
        # 检查关键表
        TABLES=$(sqlite3 "$DEV_DB" ".tables")
        if echo "$TABLES" | grep -q "marketplace_vehicles"; then
            log_success "  ✅ marketplace_vehicles 表存在"
        else
            log_error "  ❌ marketplace_vehicles 表不存在"
            ERRORS=$((ERRORS + 1))
        fi
        
        if echo "$TABLES" | grep -q "reviews"; then
            log_success "  ✅ reviews 表存在"
        else
            log_warning "  ⚠️  reviews 表不存在"
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        log_error "开发数据库完整性验证失败"
        ERRORS=$((ERRORS + 1))
    fi
else
    log_warning "开发环境数据库不存在（首次部署正常）"
    WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# 6. 检查生产环境数据库（如果存在）
# ============================================
echo ""
echo "【6/8】检查生产环境数据库..."
if [ -f "$PROD_DB" ]; then
    if sqlite3 "$PROD_DB" "PRAGMA integrity_check;" | grep -q "ok"; then
        log_success "生产数据库完整性验证通过"
        
        PROD_MOTO=$(sqlite3 "$PROD_DB" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
        PROD_MARKET=$(sqlite3 "$PROD_DB" "SELECT COUNT(*) FROM marketplace_vehicles;" 2>/dev/null || echo "0")
        
        log_info "  - 摩托车: $PROD_MOTO 条"
        log_info "  - 二手交易: $PROD_MARKET 条"
    else
        log_error "生产数据库完整性验证失败"
        ERRORS=$((ERRORS + 1))
    fi
else
    log_info "生产环境数据库不存在（首次部署正常）"
fi

# ============================================
# 7. 检查同步脚本
# ============================================
echo ""
echo "【7/8】检查数据库同步脚本..."
if [ -f "$SOURCE_DIR/backend/database/sync-dev-to-prod.sql" ]; then
    log_success "sync-dev-to-prod.sql 存在"
    
    # 验证 SQL 语法
    if grep -q "CREATE TABLE IF NOT EXISTS marketplace_vehicles" "$SOURCE_DIR/backend/database/sync-dev-to-prod.sql"; then
        log_success "  ✅ 包含 marketplace_vehicles 创建语句"
    else
        log_error "  ❌ 缺少 marketplace_vehicles 创建语句"
        ERRORS=$((ERRORS + 1))
    fi
    
    if grep -q "CREATE TABLE IF NOT EXISTS reviews" "$SOURCE_DIR/backend/database/sync-dev-to-prod.sql"; then
        log_success "  ✅ 包含 reviews 创建语句"
    else
        log_warning "  ⚠️  缺少 reviews 创建语句"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    log_error "sync-dev-to-prod.sql 不存在"
    ERRORS=$((ERRORS + 1))
fi

# ============================================
# 8. 检查磁盘空间
# ============================================
echo ""
echo "【8/8】检查磁盘空间..."
AVAILABLE=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE" -gt 5 ]; then
    log_success "可用磁盘空间: ${AVAILABLE}GB"
else
    log_warning "可用磁盘空间较少: ${AVAILABLE}GB"
    WARNINGS=$((WARNINGS + 1))
fi

# ============================================
# 总结
# ============================================
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}检查完成！${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    log_success "✅ 所有检查通过！可以开始部署"
    if [ $WARNINGS -gt 0 ]; then
        log_warning "⚠️  有 $WARNINGS 个警告，请注意"
    fi
    echo ""
    echo "执行部署："
    echo "  sudo ./quick-deploy.sh frontend  # 快速部署前端"
    echo "  sudo ./quick-deploy.sh backend   # 快速部署后端"
    echo "  sudo ./deploy.sh                 # 完整部署"
    exit 0
else
    log_error "❌ 发现 $ERRORS 个错误，$WARNINGS 个警告"
    echo ""
    echo "请修复以上错误后再进行部署！"
    exit 1
fi

