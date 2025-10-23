#!/bin/bash

# ============================================
# SSL证书申请脚本 - vietmoto.top
# ============================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 清除所有代理设置
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset no_proxy
unset NO_PROXY

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}  SSL证书申请 - vietmoto.top${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# 检查域名解析
echo -e "${CYAN}1. 检查域名解析...${NC}"
if ping -c 2 vietmoto.top > /dev/null 2>&1; then
    echo -e "   ${GREEN}✅ vietmoto.top 解析正常${NC}"
else
    echo -e "   ${RED}❌ vietmoto.top 解析失败${NC}"
    exit 1
fi

# 停止Nginx
echo -e "${CYAN}2. 停止Nginx服务...${NC}"
systemctl stop nginx
echo -e "   ${GREEN}✅ Nginx已停止${NC}"

# 申请证书（standalone模式）
echo -e "${CYAN}3. 申请SSL证书...${NC}"
certbot certonly --standalone \
    -d vietmoto.top \
    -d www.vietmoto.top \
    --email admin@vietmoto.top \
    --agree-tos \
    --non-interactive \
    --preferred-challenges http

if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ SSL证书申请成功！${NC}"
else
    echo -e "   ${RED}❌ SSL证书申请失败${NC}"
    systemctl start nginx
    exit 1
fi

# 启用HTTPS配置
echo -e "${CYAN}4. 启用HTTPS配置...${NC}"
sed -i 's/#     return 301 https:/    return 301 https:/g' /etc/nginx/conf.d/vietmoto.conf
sed -i '/^# server {$/,/^# }$/ {
    s/^# //
}' /etc/nginx/conf.d/vietmoto.conf

echo -e "   ${GREEN}✅ HTTPS配置已启用${NC}"

# 测试Nginx配置
echo -e "${CYAN}5. 测试Nginx配置...${NC}"
if nginx -t; then
    echo -e "   ${GREEN}✅ Nginx配置测试通过${NC}"
else
    echo -e "   ${RED}❌ Nginx配置测试失败${NC}"
    exit 1
fi

# 启动Nginx
echo -e "${CYAN}6. 启动Nginx服务...${NC}"
systemctl start nginx
echo -e "   ${GREEN}✅ Nginx已启动${NC}"

# 设置证书自动更新
echo -e "${CYAN}7. 设置证书自动更新...${NC}"
if ! crontab -l 2>/dev/null | grep -q "certbot renew"; then
    (crontab -l 2>/dev/null; echo "0 0 1 * * /usr/bin/certbot renew --quiet --post-hook 'systemctl reload nginx'") | crontab -
    echo -e "   ${GREEN}✅ 已添加自动更新任务（每月1号）${NC}"
else
    echo -e "   ${GREEN}✅ 自动更新任务已存在${NC}"
fi

echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  SSL证书配置完成！${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${YELLOW}💡 提示：${NC}"
echo -e "   - 证书已安装到: /etc/letsencrypt/live/vietmoto.top/"
echo -e "   - HTTPS访问: https://vietmoto.top"
echo -e "   - HTTP自动重定向到HTTPS"
echo -e "   - 证书每月自动更新"
echo ""

