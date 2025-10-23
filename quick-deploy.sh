#!/bin/bash

# ============================================
# 越南摩托汽车网站 - 快速部署脚本 v1.0
# ============================================
#
# 用途：快速部署单个模块，不进行完整备份
#
# 使用:
#   sudo ./quick-deploy.sh frontend  # 只部署前端
#   sudo ./quick-deploy.sh backend   # 只部署后端
#
# 注意：此脚本不创建完整备份，仅适用于快速更新

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
TARGET_DIR="/var/www/vietnam-moto-auto"

# 日志函数
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }
log_error() { echo -e "${RED}[✗]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[!]${NC} $1"; }

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}错误: 请指定部署模块${NC}"
    echo ""
    echo "使用方法:"
    echo "  sudo ./quick-deploy.sh frontend  # 只部署前端"
    echo "  sudo ./quick-deploy.sh backend   # 只部署后端"
    echo ""
    exit 1
fi

DEPLOY_MODULE="$1"

# 验证部署模块
case "$DEPLOY_MODULE" in
    frontend|backend)
        # 有效
        ;;
    *)
        echo -e "${RED}错误: 无效的部署模块 '$DEPLOY_MODULE'${NC}"
        echo -e "${YELLOW}支持的模块: frontend, backend${NC}"
        exit 1
        ;;
esac

# 权限检查
if [ "$EUID" -ne 0 ]; then
    log_error "请使用 root 用户或 sudo 运行此脚本"
    exit 1
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🚀 快速部署 - $DEPLOY_MODULE${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ============================================
# 部署前端
# ============================================
if [ "$DEPLOY_MODULE" = "frontend" ]; then
    log_info "1/4: 构建前端..."
    cd "$SOURCE_DIR/frontend"
    
    # 清理旧构建
    rm -rf dist
    
    # 安装依赖（如果需要）
    if [ ! -d "node_modules" ]; then
        log_info "安装前端依赖..."
        npm install
    fi
    
    # 构建
    npm run build
    
    # Astro hybrid 模式检查（生成 dist/client 和 dist/server）
    if [ ! -d "dist" ]; then
        log_error "前端构建失败，找不到 dist 目录"
        exit 1
    fi
    
    if [ ! -d "dist/client" ] && [ ! -d "dist/server" ] && [ ! -f "dist/index.html" ]; then
        log_error "前端构建失败，找不到有效的构建产物"
        exit 1
    fi
    
    log_success "前端构建完成"
    
    log_info "2/4: 复制前端文件到生产环境..."
    rm -rf "$TARGET_DIR/frontend/dist"
    mkdir -p "$TARGET_DIR/frontend"
    cp -r dist "$TARGET_DIR/frontend/"
    cp package.json "$TARGET_DIR/frontend/"
    
    # 复制配置文件
    if [ -f "$SOURCE_DIR/frontend/astro.config.mjs" ]; then
        cp "$SOURCE_DIR/frontend/astro.config.mjs" "$TARGET_DIR/frontend/"
    fi
    if [ -f "$SOURCE_DIR/frontend/.env.production" ]; then
        cp "$SOURCE_DIR/frontend/.env.production" "$TARGET_DIR/frontend/"
    fi
    
    log_success "前端文件复制完成"
    
    # 创建CSS/JS文件名大小写兼容符号链接
    log_info "创建静态资源大小写兼容符号链接..."
    if [ -d "$TARGET_DIR/frontend/dist/client/_astro" ]; then
        cd "$TARGET_DIR/frontend/dist/client/_astro"
        link_count=0
        for file in *.css *.js; do
            if [ -f "$file" ]; then
                lowercase=$(echo "$file" | tr '[:upper:]' '[:lower:]')
                if [ "$file" != "$lowercase" ] && [ ! -e "$lowercase" ]; then
                    ln -sf "$file" "$lowercase"
                    ((link_count++))
                fi
            fi
        done
        cd - > /dev/null
        if [ $link_count -gt 0 ]; then
            log_success "✓ 创建了 $link_count 个大小写兼容链接"
        fi
    fi
    
    log_info "3/4: 重启前端服务..."
    systemctl restart vietnam-moto-frontend
    
    log_success "前端服务已重启"
    
    log_info "4/4: 健康检查..."
    sleep 3
    
    # 禁用代理进行健康检查
    unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
    
    if curl --noproxy '*' -f http://localhost:4321/ > /dev/null 2>&1; then
        log_success "✅ 前端服务正常 (http://localhost:4321)"
    else
        log_warning "⚠️  前端服务可能有问题，请检查日志"
        log_info "查看日志: journalctl -u vietnam-moto-frontend -n 50"
    fi
fi

# ============================================
# 部署后端
# ============================================
if [ "$DEPLOY_MODULE" = "backend" ]; then
    log_info "1/5: 编译后端..."
    cd "$SOURCE_DIR/backend"
    
    # 安装依赖（如果需要）
    if [ ! -d "node_modules" ]; then
        log_info "安装后端依赖..."
        npm install
    fi
    
    # 编译 TypeScript
    npm run build
    
    if [ ! -d "dist" ] || [ ! -f "dist/index.js" ]; then
        log_error "后端编译失败，找不到 dist/index.js"
        exit 1
    fi
    
    log_success "后端编译完成"
    
    log_info "2/5: 复制后端文件到生产环境..."
    rm -rf "$TARGET_DIR/backend/dist"
    mkdir -p "$TARGET_DIR/backend"
    cp -r dist "$TARGET_DIR/backend/"
    cp package.json "$TARGET_DIR/backend/"
    
    # 复制配置文件
    if [ -f "$SOURCE_DIR/backend/.env.production" ]; then
        cp "$SOURCE_DIR/backend/.env.production" "$TARGET_DIR/backend/"
    fi
    
    log_success "后端文件复制完成"
    
    log_info "3/5: 安装生产依赖..."
    cd "$TARGET_DIR/backend"
    npm install --omit=dev
    
    log_success "生产依赖安装完成"
    
    log_info "4/5: 重启后端服务..."
    systemctl restart vietnam-moto-backend
    
    log_success "后端服务已重启"
    
    log_info "5/5: 健康检查..."
    sleep 3
    
    # 禁用代理进行健康检查
    unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
    
    if curl --noproxy '*' -f http://localhost:4001/health > /dev/null 2>&1; then
        log_success "✅ 后端服务正常 (http://localhost:4001)"
    else
        log_warning "⚠️  后端服务可能有问题，请检查日志"
        log_info "查看日志: journalctl -u vietnam-moto-backend -n 50"
    fi
fi

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ ${DEPLOY_MODULE} 部署完成！${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "  - 查看服务状态: systemctl status vietnam-moto-$DEPLOY_MODULE"
echo "  - 查看服务日志: journalctl -u vietnam-moto-$DEPLOY_MODULE -f"
echo "  - 测试API: /root/越南摩托汽车网站/test-api.sh"
echo ""

