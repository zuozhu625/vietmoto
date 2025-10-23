#!/bin/bash

# ============================================
# API 健康检查脚本
# 用途：快速验证后端API是否正常工作
# 使用：./test-api.sh
# ============================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔍 越南摩托汽车网站 - API 健康检查${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 禁用代理（避免代理未运行导致curl失败）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# 1. 检查服务状态
echo -e "${YELLOW}1. 检查服务状态${NC}"
echo -e "后端服务: $(systemctl is-active vietnam-moto-backend 2>/dev/null || echo 'unknown')"
echo -e "前端服务: $(systemctl is-active vietnam-moto-frontend 2>/dev/null || echo 'unknown')"
echo -e "Nginx服务: $(systemctl is-active nginx 2>/dev/null || echo 'unknown')"
echo ""

# 2. 检查端口监听
echo -e "${YELLOW}2. 检查端口监听${NC}"
netstat -tlnp 2>/dev/null | grep -E "4001|4321|:80 " || echo "端口检查失败"
echo ""

# 3. 测试后端健康检查
echo -e "${YELLOW}3. 测试后端健康检查 (http://localhost:4001/health)${NC}"
HEALTH_RESPONSE=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" http://localhost:4001/health 2>&1)
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | grep -v "HTTP_CODE")

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 健康检查成功 (HTTP $HTTP_CODE)${NC}"
    echo "$RESPONSE_BODY" | head -5
else
    echo -e "${RED}❌ 健康检查失败 (HTTP $HTTP_CODE)${NC}"
    echo "$RESPONSE_BODY" | head -10
fi
echo ""

# 4. 测试摩托车API
echo -e "${YELLOW}4. 测试摩托车列表 API (http://localhost:4001/api/vehicles/motorcycles?limit=1)${NC}"
MOTO_RESPONSE=$(curl --noproxy '*' -s -w "\nHTTP_CODE:%{http_code}" "http://localhost:4001/api/vehicles/motorcycles?limit=1" 2>&1)
HTTP_CODE=$(echo "$MOTO_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
RESPONSE_BODY=$(echo "$MOTO_RESPONSE" | grep -v "HTTP_CODE")

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 摩托车API正常 (HTTP $HTTP_CODE)${NC}"
    # 提取并显示第一辆车的信息
    echo "$RESPONSE_BODY" | grep -o '"id":[0-9]*,"brand":"[^"]*","model":"[^"]*"' | head -1
else
    echo -e "${RED}❌ 摩托车API失败 (HTTP $HTTP_CODE)${NC}"
    echo "$RESPONSE_BODY" | head -10
fi
echo ""

# 5. 测试前端
echo -e "${YELLOW}5. 测试前端页面 (http://localhost:4321)${NC}"
FRONTEND_CODE=$(curl --noproxy '*' -s -o /dev/null -w "%{http_code}" http://localhost:4321 2>&1)
if [ "$FRONTEND_CODE" = "200" ]; then
    echo -e "${GREEN}✅ 前端页面正常 (HTTP $FRONTEND_CODE)${NC}"
else
    echo -e "${RED}❌ 前端页面失败 (HTTP $FRONTEND_CODE)${NC}"
fi
echo ""

# 6. 检查数据库
echo -e "${YELLOW}6. 检查数据库${NC}"
DB_PATH="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"
if [ -f "$DB_PATH" ]; then
    MOTO_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null || echo "0")
    NEWS_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM news;" 2>/dev/null || echo "0")
    echo -e "${GREEN}✅ 数据库: $MOTO_COUNT 辆车, $NEWS_COUNT 条新闻${NC}"
else
    echo -e "${RED}❌ 数据库文件不存在${NC}"
fi
echo ""

# 7. 检查最近的错误日志
echo -e "${YELLOW}7. 最近的错误日志（如有）${NC}"
if [ -f "/var/www/vietnam-moto-auto/backend/logs/backend-error.log" ]; then
    ERRORS=$(tail -5 /var/www/vietnam-moto-auto/backend/logs/backend-error.log 2>/dev/null | grep -i error | wc -l)
    if [ "$ERRORS" -gt 0 ]; then
        echo -e "${RED}⚠️  发现 $ERRORS 条错误，查看：${NC}"
        echo "tail -20 /var/www/vietnam-moto-auto/backend/logs/backend-error.log"
    else
        echo -e "${GREEN}✅ 无最近错误${NC}"
    fi
else
    echo -e "${YELLOW}日志文件不存在${NC}"
fi
echo ""

# 总结
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}检查完成${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo "  - 如果API无法访问，检查代理设置：env | grep -i proxy"
echo "  - 查看后端日志：journalctl -u vietnam-moto-backend -n 50"
echo "  - 重启服务：systemctl restart vietnam-moto-backend"
echo ""

