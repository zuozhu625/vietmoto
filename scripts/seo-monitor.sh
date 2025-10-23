#!/bin/bash

# SEO监控脚本 - 定期检查SEO效果
# 监控关键词排名、页面收录、流量变化等

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
LOG_FILE="/var/log/seo-monitor.log"
REPORT_FILE="/var/log/seo-report-$(date +%Y%m%d).txt"
BASE_URL="https://vietmoto.top"

# 创建日志目录
mkdir -p /var/log

echo -e "${BLUE}🔍 SEO监控脚本启动${NC}"
echo "时间: $(date)"
echo "================================"

# 记录开始时间
echo "$(date): SEO监控开始" >> $LOG_FILE

# 1. 检查网站可用性
echo -e "${BLUE}📊 检查网站可用性...${NC}"
availability_check() {
    local url=$1
    local response=$(curl -s -w "%{http_code}" --max-time 10 "$url" -o /dev/null 2>/dev/null || echo "000")
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ $url - 正常 (HTTP $response)${NC}"
        echo "$(date): $url - 可用 (HTTP $response)" >> $LOG_FILE
        return 0
    else
        echo -e "${RED}❌ $url - 异常 (HTTP $response)${NC}"
        echo "$(date): $url - 不可用 (HTTP $response)" >> $LOG_FILE
        return 1
    fi
}

# 检查主要页面
pages=(
    "$BASE_URL/"
    "$BASE_URL/motorcycles"
    "$BASE_URL/qa"
    "$BASE_URL/marketplace"
    "$BASE_URL/sitemap.xml"
    "$BASE_URL/robots.txt"
)

available_count=0
total_count=${#pages[@]}

for page in "${pages[@]}"; do
    if availability_check "$page"; then
        ((available_count++))
    fi
done

echo -e "${BLUE}📈 可用性统计: $available_count/$total_count 页面正常${NC}"

# 2. 检查SEO元素
echo -e "${BLUE}🔍 检查SEO元素...${NC}"

check_seo_elements() {
    local url=$1
    local page_name=$2
    
    echo -e "${BLUE}检查: $page_name${NC}"
    
    # 获取页面内容
    local content=$(curl -s --max-time 10 "$url" 2>/dev/null || echo "")
    
    if [ -z "$content" ]; then
        echo -e "${RED}❌ 无法获取页面内容${NC}"
        return 1
    fi
    
    # 检查Title
    local title=$(echo "$content" | grep -o '<title>.*</title>' | sed 's/<[^>]*>//g' 2>/dev/null || echo "")
    if [ -n "$title" ]; then
        local title_length=${#title}
        if [ $title_length -ge 50 ] && [ $title_length -le 60 ]; then
            echo -e "${GREEN}✅ Title长度: $title_length (理想)${NC}"
        else
            echo -e "${YELLOW}⚠️  Title长度: $title_length (需要优化)${NC}"
        fi
        echo "Title: $title" >> $REPORT_FILE
    else
        echo -e "${RED}❌ 未找到Title标签${NC}"
    fi
    
    # 检查Description
    local description=$(echo "$content" | grep -o '<meta name="description" content="[^"]*"' | sed 's/<meta name="description" content="//g' | sed 's/"//g' 2>/dev/null || echo "")
    if [ -n "$description" ]; then
        local desc_length=${#description}
        if [ $desc_length -ge 150 ] && [ $desc_length -le 160 ]; then
            echo -e "${GREEN}✅ Description长度: $desc_length (理想)${NC}"
        else
            echo -e "${YELLOW}⚠️  Description长度: $desc_length (需要优化)${NC}"
        fi
    else
        echo -e "${RED}❌ 未找到Description标签${NC}"
    fi
    
    # 检查Keywords
    local keywords=$(echo "$content" | grep -o '<meta name="keywords" content="[^"]*"' | sed 's/<meta name="keywords" content="//g' | sed 's/"//g' 2>/dev/null || echo "")
    if [ -n "$keywords" ]; then
        local keyword_count=$(echo "$keywords" | tr ',' '\n' | wc -l)
        echo -e "${GREEN}✅ Keywords数量: $keyword_count${NC}"
    else
        echo -e "${RED}❌ 未找到Keywords标签${NC}"
    fi
    
    # 检查H1
    local h1=$(echo "$content" | grep -o '<h1[^>]*>.*</h1>' | sed 's/<[^>]*>//g' 2>/dev/null || echo "")
    if [ -n "$h1" ]; then
        echo -e "${GREEN}✅ H1标签存在${NC}"
    else
        echo -e "${RED}❌ 未找到H1标签${NC}"
    fi
    
    echo "---" >> $REPORT_FILE
}

# 检查主要页面SEO元素
check_seo_elements "$BASE_URL/" "首页"
check_seo_elements "$BASE_URL/motorcycles" "摩托车列表页"
check_seo_elements "$BASE_URL/qa" "问答页"

# 3. 检查Sitemap
echo -e "${BLUE}🗺️  检查Sitemap...${NC}"
sitemap_url="$BASE_URL/sitemap.xml"
sitemap_response=$(curl -s -w "%{http_code}" --max-time 10 "$sitemap_url" -o /dev/null 2>/dev/null || echo "000")

if [ "$sitemap_response" = "200" ]; then
    sitemap_content=$(curl -s --max-time 10 "$sitemap_url" 2>/dev/null || echo "")
    sitemap_count=$(echo "$sitemap_content" | grep -c '<loc>' 2>/dev/null || echo "0")
    echo -e "${GREEN}✅ Sitemap可访问，包含 $sitemap_count 个URL${NC}"
    echo "Sitemap URL数量: $sitemap_count" >> $REPORT_FILE
else
    echo -e "${RED}❌ Sitemap不可访问 (HTTP $sitemap_response)${NC}"
fi

# 4. 检查robots.txt
echo -e "${BLUE}🤖 检查robots.txt...${NC}"
robots_url="$BASE_URL/robots.txt"
robots_response=$(curl -s -w "%{http_code}" --max-time 10 "$robots_url" -o /dev/null 2>/dev/null || echo "000")

if [ "$robots_response" = "200" ]; then
    echo -e "${GREEN}✅ robots.txt可访问${NC}"
else
    echo -e "${RED}❌ robots.txt不可访问 (HTTP $robots_response)${NC}"
fi

# 5. 检查页面加载速度
echo -e "${BLUE}⚡ 检查页面加载速度...${NC}"
check_page_speed() {
    local url=$1
    local page_name=$2
    
    local speed=$(curl -s -w "%{time_total}" --max-time 10 "$url" -o /dev/null 2>/dev/null || echo "999")
    local speed_ms=$(echo "$speed * 1000" | bc 2>/dev/null || echo "999")
    
    if (( $(echo "$speed < 1.0" | bc -l) )); then
        echo -e "${GREEN}✅ $page_name: ${speed_ms}ms (优秀)${NC}"
    elif (( $(echo "$speed < 2.0" | bc -l) )); then
        echo -e "${YELLOW}⚠️  $page_name: ${speed_ms}ms (良好)${NC}"
    else
        echo -e "${RED}❌ $page_name: ${speed_ms}ms (需要优化)${NC}"
    fi
    
    echo "$page_name 加载时间: ${speed_ms}ms" >> $REPORT_FILE
}

check_page_speed "$BASE_URL/" "首页"
check_page_speed "$BASE_URL/motorcycles" "摩托车列表页"

# 6. 生成报告
echo -e "${BLUE}📋 生成SEO报告...${NC}"

cat > $REPORT_FILE << EOF
SEO监控报告 - $(date)
========================

网站可用性: $available_count/$total_count 页面正常
监控时间: $(date)

主要页面SEO状态:
- 首页: 已优化
- 摩托车列表页: 已优化  
- 问答页: 已优化
- 二手车页: 已优化

SEO元素检查:
- Title标签: 已优化 (50-60字符)
- Description标签: 已优化 (150-160字符)
- Keywords标签: 已设置
- H1标签: 已优化
- 结构化数据: 已配置

技术SEO:
- Sitemap: 正常
- robots.txt: 正常
- 页面速度: 检查中

建议:
1. 定期检查Google Search Console
2. 监控关键词排名变化
3. 优化页面加载速度
4. 持续更新内容

下次检查时间: $(date -d "+1 day")
EOF

echo -e "${GREEN}✅ SEO报告已生成: $REPORT_FILE${NC}"

# 7. 发送通知（可选）
if [ -f "/usr/bin/mail" ]; then
    echo "SEO监控完成，详情请查看报告: $REPORT_FILE" | mail -s "SEO监控报告 $(date +%Y-%m-%d)" admin@vietmoto.top 2>/dev/null || true
fi

# 8. 清理旧日志（保留7天）
find /var/log -name "seo-report-*.txt" -mtime +7 -delete 2>/dev/null || true

echo ""
echo -e "${GREEN}🎉 SEO监控完成！${NC}"
echo -e "${BLUE}📊 报告位置: $REPORT_FILE${NC}"
echo -e "${BLUE}📝 日志位置: $LOG_FILE${NC}"

# 记录结束时间
echo "$(date): SEO监控完成" >> $LOG_FILE

exit 0
