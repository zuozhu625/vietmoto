#!/bin/bash

# SEO优化验证脚本
# 验证页面Title、Description、Keywords等SEO元素

set -e

echo "🔍 SEO优化验证脚本"
echo "=================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 测试URL列表
declare -a urls=(
    "http://localhost:4321/"
    "http://localhost:4321/motorcycles"
    "http://localhost:4321/qa"
    "http://localhost:4321/marketplace"
)

# 检查服务状态
echo -e "${BLUE}📊 检查服务状态...${NC}"
if systemctl is-active --quiet vietnam-moto-frontend; then
    echo -e "${GREEN}✅ 前端服务运行正常${NC}"
else
    echo -e "${RED}❌ 前端服务未运行${NC}"
    echo "启动服务: sudo systemctl start vietnam-moto-frontend"
    exit 1
fi

# 等待服务完全启动
echo -e "${BLUE}⏳ 等待服务启动...${NC}"
sleep 5

# 验证每个页面
for url in "${urls[@]}"; do
    echo ""
    echo -e "${BLUE}🔍 验证: $url${NC}"
    echo "----------------------------------------"
    
    # 获取页面内容
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null || echo -e "\n000")
    http_code=$(echo "$response" | tail -n1)
    content=$(echo "$response" | head -n -1)
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ HTTP状态: $http_code${NC}"
        
        # 提取Title
        title=$(echo "$content" | grep -o '<title>.*</title>' | sed 's/<[^>]*>//g' || echo "")
        if [ -n "$title" ]; then
            echo -e "${GREEN}✅ Title: $title${NC}"
            
            # 检查Title长度
            title_length=${#title}
            if [ $title_length -ge 50 ] && [ $title_length -le 60 ]; then
                echo -e "${GREEN}✅ Title长度: $title_length (理想)${NC}"
            elif [ $title_length -ge 40 ] && [ $title_length -le 70 ]; then
                echo -e "${YELLOW}⚠️  Title长度: $title_length (可接受)${NC}"
            else
                echo -e "${RED}❌ Title长度: $title_length (需要优化)${NC}"
            fi
            
            # 检查是否包含emoji
            if echo "$title" | grep -q "[🏍️🚗⚡⭐💰❓🛒]"; then
                echo -e "${GREEN}✅ 包含emoji${NC}"
            else
                echo -e "${YELLOW}⚠️  未包含emoji${NC}"
            fi
        else
            echo -e "${RED}❌ 未找到Title标签${NC}"
        fi
        
        # 提取Description
        description=$(echo "$content" | grep -o '<meta name="description" content="[^"]*"' | sed 's/<meta name="description" content="//g' | sed 's/"//g' || echo "")
        if [ -n "$description" ]; then
            echo -e "${GREEN}✅ Description: ${description:0:80}...${NC}"
            
            # 检查Description长度
            desc_length=${#description}
            if [ $desc_length -ge 150 ] && [ $desc_length -le 160 ]; then
                echo -e "${GREEN}✅ Description长度: $desc_length (理想)${NC}"
            elif [ $desc_length -ge 120 ] && [ $desc_length -le 180 ]; then
                echo -e "${YELLOW}⚠️  Description长度: $desc_length (可接受)${NC}"
            else
                echo -e "${RED}❌ Description长度: $desc_length (需要优化)${NC}"
            fi
        else
            echo -e "${RED}❌ 未找到Description标签${NC}"
        fi
        
        # 提取Keywords
        keywords=$(echo "$content" | grep -o '<meta name="keywords" content="[^"]*"' | sed 's/<meta name="keywords" content="//g' | sed 's/"//g' || echo "")
        if [ -n "$keywords" ]; then
            echo -e "${GREEN}✅ Keywords: 已设置${NC}"
            keyword_count=$(echo "$keywords" | tr ',' '\n' | wc -l)
            echo -e "${GREEN}✅ 关键词数量: $keyword_count${NC}"
        else
            echo -e "${RED}❌ 未找到Keywords标签${NC}"
        fi
        
        # 提取H1
        h1=$(echo "$content" | grep -o '<h1[^>]*>.*</h1>' | sed 's/<[^>]*>//g' || echo "")
        if [ -n "$h1" ]; then
            echo -e "${GREEN}✅ H1: $h1${NC}"
        else
            echo -e "${RED}❌ 未找到H1标签${NC}"
        fi
        
        # 检查页面大小
        page_size=$(echo "$content" | wc -c)
        echo -e "${GREEN}✅ 页面大小: $page_size 字节${NC}"
        
    else
        echo -e "${RED}❌ HTTP状态: $http_code${NC}"
        echo -e "${RED}❌ 页面无法访问${NC}"
    fi
done

echo ""
echo -e "${BLUE}📋 SEO验证总结${NC}"
echo "=================="

# 检查sitemap
echo -e "${BLUE}🗺️  检查Sitemap...${NC}"
sitemap_response=$(curl -s -w "%{http_code}" http://localhost:4321/sitemap.xml -o /dev/null 2>/dev/null || echo "000")
if [ "$sitemap_response" = "200" ]; then
    echo -e "${GREEN}✅ Sitemap可访问${NC}"
    sitemap_count=$(curl -s http://localhost:4321/sitemap.xml | grep -c '<loc>' 2>/dev/null || echo "0")
    echo -e "${GREEN}✅ Sitemap包含 $sitemap_count 个URL${NC}"
else
    echo -e "${RED}❌ Sitemap不可访问${NC}"
fi

# 检查robots.txt
echo -e "${BLUE}🤖 检查robots.txt...${NC}"
robots_response=$(curl -s -w "%{http_code}" http://localhost:4321/robots.txt -o /dev/null 2>/dev/null || echo "000")
if [ "$robots_response" = "200" ]; then
    echo -e "${GREEN}✅ robots.txt可访问${NC}"
else
    echo -e "${RED}❌ robots.txt不可访问${NC}"
fi

echo ""
echo -e "${GREEN}🎉 SEO验证完成！${NC}"
echo ""
echo -e "${BLUE}📝 下一步建议:${NC}"
echo "1. 在Google Search Console提交sitemap"
echo "2. 请求索引主要页面"
echo "3. 监控关键词排名"
echo "4. 定期检查SEO效果"

exit 0
