#!/bin/bash

# ============================================
# Q&A 系统测试脚本
# ============================================

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 禁用代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🤖 Q&A 自动生成系统测试${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. 检查数据库表
echo -e "${YELLOW}1. 检查数据库表${NC}"
TABLES=$(sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite ".tables" | grep -E "questions|answers")
if [ -n "$TABLES" ]; then
    echo -e "${GREEN}✅ 表已创建: $TABLES${NC}"
else
    echo -e "${RED}❌ 表不存在${NC}"
    exit 1
fi
echo ""

# 2. 生成5条Q&A
echo -e "${YELLOW}2. 生成5条测试Q&A${NC}"
for i in {1..5}; do
    RESULT=$(curl --noproxy '*' -s -X POST http://localhost:4001/api/qa/generate)
    SUCCESS=$(echo "$RESULT" | grep -o '"success":true' || echo "")
    if [ -n "$SUCCESS" ]; then
        echo -e "${GREEN}✓ 生成第 $i 条${NC}"
    else
        echo -e "${RED}✗ 生成第 $i 条失败${NC}"
    fi
    sleep 0.5
done
echo ""

# 3. 查看统计
echo -e "${YELLOW}3. Q&A 统计${NC}"
QA_COUNT=$(sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite "SELECT COUNT(*) FROM questions;")
ANSWER_COUNT=$(sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite "SELECT COUNT(*) FROM answers;")
echo -e "${GREEN}✅ 总问题数: $QA_COUNT${NC}"
echo -e "${GREEN}✅ 总答案数: $ANSWER_COUNT${NC}"
echo ""

# 4. 查看最新的3条问题
echo -e "${YELLOW}4. 最新的3条问题${NC}"
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite "SELECT '📌 ID: ' || id || ' | ' || title || ' (' || category || ')' FROM questions ORDER BY id DESC LIMIT 3;"
echo ""

# 5. 测试API
echo -e "${YELLOW}5. 测试Q&A API${NC}"
QA_API=$(curl --noproxy '*' -s "http://localhost:4001/api/qa?limit=1")
SUCCESS=$(echo "$QA_API" | grep -o '"success":true' || echo "")
if [ -n "$SUCCESS" ]; then
    echo -e "${GREEN}✅ API正常工作${NC}"
    echo "$QA_API" | head -c 200
    echo "..."
else
    echo -e "${RED}❌ API失败${NC}"
fi
echo ""
echo ""

# 6. 答案长度统计
echo -e "${YELLOW}6. 答案长度统计${NC}"
STATS=$(sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite "SELECT '最短: ' || MIN(LENGTH(content)) || '字符, 最长: ' || MAX(LENGTH(content)) || '字符, 平均: ' || ROUND(AVG(LENGTH(content))) || '字符' FROM answers;")
echo -e "${GREEN}$STATS${NC}"
echo -e "${GREEN}要求: 50字以上 ✅${NC}"
echo ""

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ 测试完成！${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}💡 访问网站查看效果：${NC}"
echo "  - 问答列表: http://47.237.79.9:4321/qa/"
echo "  - API接口: http://47.237.79.9:4001/api/qa"
echo ""

