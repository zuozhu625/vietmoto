#!/bin/bash

# ============================================
# CSS加载监控脚本
# ============================================
# 用途：检测CSS文件404错误，及时发现加载问题
# 使用：./check-css-loading.sh
# 或作为cron任务：*/5 * * * * /root/越南摩托汽车网站/check-css-loading.sh

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置
LOG_FILE="/var/log/nginx/vietmoto.access.log"
ALERT_THRESHOLD=5
DOMAIN="https://vietmoto.top"

# 检查Nginx日志中的CSS 404错误
echo "========================================"
echo "CSS加载监控报告 - $(date)"
echo "========================================"
echo ""

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}错误：日志文件不存在: $LOG_FILE${NC}"
    exit 1
fi

# 统计最近100条日志中的CSS 404错误
css_404=$(tail -100 "$LOG_FILE" | grep "\.css" | grep " 404 " | wc -l)

echo "最近100条日志中的CSS 404错误数: $css_404"

if [ $css_404 -gt $ALERT_THRESHOLD ]; then
    echo -e "${RED}警告：CSS加载失败次数过多！${NC}"
    echo ""
    echo "最近的错误URL："
    tail -100 "$LOG_FILE" | grep "\.css" | grep " 404 " | awk '{print $7}' | sort | uniq -c | sort -rn
    echo ""
    echo "建议操作："
    echo "1. 检查CSS文件是否存在："
    echo "   ls -la /var/www/vietnam-moto-auto/frontend/dist/client/_astro/*.css"
    echo ""
    echo "2. 检查符号链接："
    echo "   ls -la /var/www/vietnam-moto-auto/frontend/dist/client/_astro/ | grep '\->'"
    echo ""
    echo "3. 重新部署前端："
    echo "   sudo /root/越南摩托汽车网站/quick-deploy.sh frontend"
    
    exit 1
elif [ $css_404 -gt 0 ]; then
    echo -e "${YELLOW}提示：检测到少量CSS 404错误${NC}"
    tail -100 "$LOG_FILE" | grep "\.css" | grep " 404 " | awk '{print $7}' | sort | uniq -c
else
    echo -e "${GREEN}✓ CSS加载正常，无404错误${NC}"
fi

echo ""

# 检查主要CSS文件是否可访问
echo "检查主要CSS文件访问性..."
css_files=$(curl -s --noproxy '*' http://localhost:4321/ 2>/dev/null | grep -o 'href="/_astro/[^"]*\.css"' | cut -d'"' -f2 | head -3)

if [ -z "$css_files" ]; then
    echo -e "${RED}警告：无法获取CSS文件列表${NC}"
    exit 1
fi

error_count=0
for css in $css_files; do
    status=$(curl -s -o /dev/null -w "%{http_code}" --noproxy '*' "$DOMAIN$css" 2>/dev/null)
    if [ "$status" = "200" ]; then
        echo -e "${GREEN}✓${NC} $css - OK"
    else
        echo -e "${RED}✗${NC} $css - HTTP $status"
        ((error_count++))
    fi
done

echo ""

if [ $error_count -gt 0 ]; then
    echo -e "${RED}发现 $error_count 个CSS文件无法访问！${NC}"
    exit 1
else
    echo -e "${GREEN}所有CSS文件都可以正常访问${NC}"
fi

echo ""
echo "========================================"
echo "监控完成"
echo "========================================"

exit 0

