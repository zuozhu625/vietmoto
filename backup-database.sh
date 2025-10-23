#!/bin/bash

# ============================================
# SQLite 数据库备份脚本
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
DB_PATH="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"
BACKUP_DIR="/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vietnam_moto_auto_${DATE}.sqlite"
KEEP_DAYS=30  # 保留最近30天的备份

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_separator() {
    echo "============================================"
}

# 开始备份
echo ""
print_separator
log_info "💾 SQLite 数据库备份"
print_separator
echo ""

# 1. 检查数据库文件是否存在
log_info "检查数据库文件..."
if [ ! -f "$DB_PATH" ]; then
    log_error "数据库文件不存在: $DB_PATH"
    exit 1
fi
log_success "数据库文件: $DB_PATH"

# 2. 检查并创建备份目录
log_info "检查备份目录..."
if [ ! -d "$BACKUP_DIR" ]; then
    log_info "创建备份目录..."
    mkdir -p "$BACKUP_DIR"
fi
log_success "备份目录: $BACKUP_DIR"

# 3. 执行备份
log_info "开始备份数据库..."
if cp "$DB_PATH" "$BACKUP_FILE"; then
    log_success "备份完成"
else
    log_error "备份失败！"
    exit 1
fi

# 4. 压缩备份文件
log_info "压缩备份文件..."
if gzip "$BACKUP_FILE"; then
    BACKUP_FILE="${BACKUP_FILE}.gz"
    log_success "压缩完成"
else
    log_warning "压缩失败，保留原始文件"
fi

# 5. 检查备份文件
FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
log_success "备份文件: $BACKUP_FILE"
log_success "文件大小: $FILE_SIZE"

# 6. 验证备份完整性（可选）
if [ -f "$BACKUP_FILE" ]; then
    GUNZIP_TEST=$(gunzip -t "$BACKUP_FILE" 2>&1)
    if [ $? -eq 0 ]; then
        log_success "备份文件完整性验证通过"
    else
        log_warning "备份文件完整性验证失败"
    fi
fi

# 7. 清理旧备份
log_info "清理 $KEEP_DAYS 天前的旧备份..."
DELETED_COUNT=$(find "$BACKUP_DIR" -name "vietnam_moto_auto_*.sqlite.gz" -mtime +$KEEP_DAYS -type f 2>/dev/null | wc -l)

if [ $DELETED_COUNT -gt 0 ]; then
    find "$BACKUP_DIR" -name "vietnam_moto_auto_*.sqlite.gz" -mtime +$KEEP_DAYS -type f -delete
    log_success "清理了 $DELETED_COUNT 个旧备份文件"
else
    log_info "没有需要清理的旧备份"
fi

# 8. 显示备份列表
log_info "最近的备份文件:"
ls -lht "$BACKUP_DIR"/*.sqlite.gz 2>/dev/null | head -n 10 || log_warning "没有找到备份文件"

# 9. 备份统计
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/*.sqlite.gz 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)

# 完成
echo ""
print_separator
log_success "✅ 数据库备份完成！"
print_separator
echo ""
log_info "📊 备份统计:"
echo "  - 备份文件数: $BACKUP_COUNT"
echo "  - 总占用空间: $TOTAL_SIZE"
echo "  - 最新备份: $(basename "$BACKUP_FILE")"
echo "  - 备份目录: $BACKUP_DIR"
echo ""
log_info "📝 恢复命令:"
echo "  # 停止后端服务"
echo "  systemctl stop vietnam-moto-backend"
echo ""
echo "  # 恢复数据库"
echo "  gunzip -c $BACKUP_FILE > $DB_PATH"
echo ""
echo "  # 启动后端服务"
echo "  systemctl start vietnam-moto-backend"
echo ""
log_info "💡 提示:"
echo "  - 设置定时备份: crontab -e"
echo "  - 添加任务: 0 2 * * * /root/越南摩托汽车网站/backup-database.sh"
echo ""
print_separator

exit 0

