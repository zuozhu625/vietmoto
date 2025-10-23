#!/bin/bash

# ============================================
# 越南摩托汽车网站 - SEO验证脚本
# ============================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 网站配置
SITE_URL="https://vietmoto.top"

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}    越南摩托汽车网站 - SEO验证检查${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# 清除代理环境变量（避免curl失败）
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# ============================================
# 1. 检查关键页面可访问性
# ============================================
echo -e "${CYAN}🌐 检查关键页面可访问性...${NC}"

check_page() {
    local url=$1
    local name=$2
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    local time=$(curl -s -o /dev/null -w "%{time_total}" "$url" 2>/dev/null)
    
    if [ "$status" = "200" ]; then
        echo -e "   ${GREEN}✅ ${name}: HTTP ${status} (${time}s)${NC}"
        return 0
    else
        echo -e "   ${RED}❌ ${name}: HTTP ${status}${NC}"
        return 1
    fi
}

check_page "${SITE_URL}/" "首页"
check_page "${SITE_URL}/motorcycles" "摩托车页面"
check_page "${SITE_URL}/cars" "汽车页面"
check_page "${SITE_URL}/qa" "问答页面"
check_page "${SITE_URL}/marketplace" "二手市场页面"
check_page "${SITE_URL}/reviews" "测评页面"

echo ""

# ============================================
# 2. 检查 robots.txt
# ============================================
echo -e "${CYAN}🤖 检查 robots.txt...${NC}"

robots_status=$(curl -s -o /dev/null -w "%{http_code}" "${SITE_URL}/robots.txt" 2>/dev/null)
if [ "$robots_status" = "200" ]; then
    echo -e "   ${GREEN}✅ robots.txt 可访问 (HTTP ${robots_status})${NC}"
    
    # 检查内容
    robots_content=$(curl -s "${SITE_URL}/robots.txt" 2>/dev/null)
    
    if echo "$robots_content" | grep -q "User-agent"; then
        echo -e "   ${GREEN}✅ 包含 User-agent 规则${NC}"
    else
        echo -e "   ${YELLOW}⚠️  缺少 User-agent 规则${NC}"
    fi
    
    if echo "$robots_content" | grep -q "Sitemap"; then
        echo -e "   ${GREEN}✅ 包含 Sitemap 链接${NC}"
    else
        echo -e "   ${YELLOW}⚠️  缺少 Sitemap 链接${NC}"
    fi
else
    echo -e "   ${RED}❌ robots.txt 不可访问 (HTTP ${robots_status})${NC}"
fi

echo ""

# ============================================
# 3. 检查 sitemap.xml
# ============================================
echo -e "${CYAN}🗺️  检查 sitemap.xml...${NC}"

sitemap_status=$(curl -s -o /dev/null -w "%{http_code}" "${SITE_URL}/sitemap.xml" 2>/dev/null)
sitemap_time=$(curl -s -o /dev/null -w "%{time_total}" "${SITE_URL}/sitemap.xml" 2>/dev/null)

if [ "$sitemap_status" = "200" ]; then
    echo -e "   ${GREEN}✅ sitemap.xml 可访问 (HTTP ${sitemap_status}, ${sitemap_time}s)${NC}"
    
    # 统计URL数量
    sitemap_content=$(curl -s "${SITE_URL}/sitemap.xml" 2>/dev/null)
    url_count=$(echo "$sitemap_content" | grep -c "<loc>")
    
    if [ "$url_count" -gt 0 ]; then
        echo -e "   ${GREEN}✅ 包含 ${url_count} 个URL${NC}"
        
        # 检查是否是有效的XML
        if echo "$sitemap_content" | grep -q "<?xml version"; then
            echo -e "   ${GREEN}✅ XML格式正确${NC}"
        else
            echo -e "   ${YELLOW}⚠️  XML格式可能有问题${NC}"
        fi
    else
        echo -e "   ${RED}❌ 没有找到URL${NC}"
    fi
else
    echo -e "   ${RED}❌ sitemap.xml 不可访问 (HTTP ${sitemap_status})${NC}"
fi

echo ""

# ============================================
# 4. 检查响应时间
# ============================================
echo -e "${CYAN}⚡ 检查网站性能...${NC}"

check_performance() {
    local url=$1
    local name=$2
    local time=$(curl -s -o /dev/null -w "%{time_total}" "$url" 2>/dev/null)
    local time_ms=$(echo "$time * 1000" | bc)
    local time_int=${time_ms%.*}
    
    if [ "$time_int" -lt 200 ]; then
        echo -e "   ${GREEN}✅ ${name}: ${time_int}ms (优秀🚀)${NC}"
    elif [ "$time_int" -lt 500 ]; then
        echo -e "   ${GREEN}✅ ${name}: ${time_int}ms (良好👍)${NC}"
    elif [ "$time_int" -lt 1000 ]; then
        echo -e "   ${YELLOW}⚠️  ${name}: ${time_int}ms (需要优化)${NC}"
    else
        echo -e "   ${RED}❌ ${name}: ${time_int}ms (太慢)${NC}"
    fi
}

check_performance "${SITE_URL}/" "首页响应时间"
check_performance "${SITE_URL}/robots.txt" "robots.txt响应时间"
check_performance "${SITE_URL}/sitemap.xml" "sitemap.xml响应时间"

echo ""

# ============================================
# 5. 检查HTTP响应头
# ============================================
echo -e "${CYAN}📡 检查HTTP响应头...${NC}"

headers=$(curl -s -I "${SITE_URL}/" 2>/dev/null)

# 检查服务器类型
if echo "$headers" | grep -i "server" > /dev/null; then
    server=$(echo "$headers" | grep -i "server:" | cut -d' ' -f2- | tr -d '\r')
    echo -e "   ${GREEN}✅ 服务器: ${server}${NC}"
fi

# 检查是否有noindex
if echo "$headers" | grep -i "x-robots-tag.*noindex" > /dev/null; then
    echo -e "   ${RED}❌ 发现 noindex 标记（页面不会被索引）${NC}"
else
    echo -e "   ${GREEN}✅ 无 noindex 标记（页面可被索引）${NC}"
fi

# 检查Content-Type
if echo "$headers" | grep -i "content-type.*text/html" > /dev/null; then
    echo -e "   ${GREEN}✅ Content-Type 正确${NC}"
fi

echo ""

# ============================================
# 6. 检查meta标签
# ============================================
echo -e "${CYAN}🏷️  检查meta标签...${NC}"

page_content=$(curl -s "${SITE_URL}/" 2>/dev/null)

# 检查title
if echo "$page_content" | grep -q "<title>"; then
    title=$(echo "$page_content" | grep -o "<title>[^<]*</title>" | sed 's/<[^>]*>//g' | head -1)
    echo -e "   ${GREEN}✅ Title: ${title}${NC}"
else
    echo -e "   ${RED}❌ 缺少 title 标签${NC}"
fi

# 检查description
if echo "$page_content" | grep -q 'name="description"'; then
    echo -e "   ${GREEN}✅ 包含 description meta标签${NC}"
else
    echo -e "   ${RED}❌ 缺少 description meta标签${NC}"
fi

# 检查canonical
if echo "$page_content" | grep -q 'rel="canonical"'; then
    echo -e "   ${GREEN}✅ 包含 canonical 链接${NC}"
else
    echo -e "   ${YELLOW}⚠️  缺少 canonical 链接${NC}"
fi

# 检查Open Graph
og_count=$(echo "$page_content" | grep -c 'property="og:')
if [ "$og_count" -gt 0 ]; then
    echo -e "   ${GREEN}✅ 包含 ${og_count} 个 Open Graph 标签${NC}"
else
    echo -e "   ${YELLOW}⚠️  缺少 Open Graph 标签${NC}"
fi

# 检查结构化数据
schema_count=$(echo "$page_content" | grep -c 'application/ld+json')
if [ "$schema_count" -gt 0 ]; then
    echo -e "   ${GREEN}✅ 包含 ${schema_count} 个结构化数据块${NC}"
else
    echo -e "   ${YELLOW}⚠️  缺少结构化数据${NC}"
fi

echo ""

# ============================================
# 7. 检查服务状态
# ============================================
echo -e "${CYAN}🔧 检查服务状态...${NC}"

# 检查前端服务
if systemctl is-active --quiet vietnam-moto-frontend 2>/dev/null; then
    echo -e "   ${GREEN}✅ 前端服务运行中${NC}"
else
    echo -e "   ${RED}❌ 前端服务未运行${NC}"
fi

# 检查后端服务
if systemctl is-active --quiet vietnam-moto-backend 2>/dev/null; then
    echo -e "   ${GREEN}✅ 后端服务运行中${NC}"
else
    echo -e "   ${RED}❌ 后端服务未运行${NC}"
fi

echo ""

# ============================================
# 8. 数据库统计
# ============================================
echo -e "${CYAN}📊 数据库内容统计...${NC}"

DB_PATH="/root/越南摩托汽车网站/vietnam_moto_auto.sqlite"

if [ -f "$DB_PATH" ]; then
    motorcycles_count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM motorcycles;" 2>/dev/null)
    cars_count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cars;" 2>/dev/null)
    qa_count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM questions;" 2>/dev/null)
    marketplace_count=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM marketplace_vehicles;" 2>/dev/null)
    
    echo -e "   ${GREEN}✅ 摩托车: ${motorcycles_count} 条${NC}"
    echo -e "   ${GREEN}✅ 汽车: ${cars_count} 条${NC}"
    echo -e "   ${GREEN}✅ 问答: ${qa_count} 条${NC}"
    echo -e "   ${GREEN}✅ 二手交易: ${marketplace_count} 条${NC}"
else
    echo -e "   ${YELLOW}⚠️  数据库文件未找到${NC}"
fi

echo ""

# ============================================
# 总结
# ============================================
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}    SEO检查完成！${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo -e "   1. 确保所有页面响应时间 < 500ms"
echo -e "   2. 定期检查sitemap URL数量是否增长"
echo -e "   3. 使用 Google Search Console 提交sitemap"
echo -e "   4. 使用 Google Rich Results Test 验证结构化数据"
echo -e "   5. 建议每2-4周在GSC重新提交sitemap"
echo ""

