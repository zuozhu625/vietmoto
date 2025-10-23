#!/bin/bash
# ========================================
# Sitemap验证脚本 - 越南摩托汽车网站
# ========================================

echo "=========================================="
echo "🔍 Sitemap部署验证"
echo "=========================================="
echo ""

# 清除代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# 1. 检查sitemap.xml
echo "1️⃣ 检查 sitemap.xml:"
echo "   URL: https://vietmoto.top/sitemap.xml"
RESPONSE=$(curl -s -I http://localhost:4321/sitemap.xml)
STATUS=$(echo "$RESPONSE" | grep "HTTP" | awk '{print $2}')
COUNT=$(echo "$RESPONSE" | grep -i "x-sitemap-count" | cut -d: -f2 | tr -d ' \r')
GENERATED=$(echo "$RESPONSE" | grep -i "x-sitemap-generated" | cut -d: -f2- | tr -d ' \r')

if [ "$STATUS" == "200" ]; then
  echo "   ✅ 状态: HTTP $STATUS (正常)"
  echo "   📊 URL总数: $COUNT"
  echo "   🕒 生成时间: $GENERATED"
else
  echo "   ❌ 状态: HTTP $STATUS (异常)"
fi
echo ""

# 2. 检查sitemap-index.xml (应该404)
echo "2️⃣ 检查 sitemap-index.xml (应该已删除):"
INDEX_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:4321/sitemap-index.xml)
if [ "$INDEX_STATUS" == "404" ]; then
  echo "   ✅ 状态: HTTP 404 (已成功删除) ✓"
else
  echo "   ⚠️ 状态: HTTP $INDEX_STATUS (仍可访问，可能有缓存)"
fi
echo ""

# 3. 检查robots.txt
echo "3️⃣ 检查 robots.txt:"
SITEMAP_LINE=$(curl -s http://localhost:4321/robots.txt | grep "Sitemap:")
echo "   $SITEMAP_LINE"
if echo "$SITEMAP_LINE" | grep -q "sitemap.xml"; then
  echo "   ✅ 指向正确的sitemap.xml ✓"
else
  echo "   ⚠️ 未指向sitemap.xml"
fi
echo ""

# 4. 统计URL类型分布
echo "4️⃣ URL类型分布统计:"
SITEMAP_CONTENT=$(curl -s http://localhost:4321/sitemap.xml)
STATIC=$(echo "$SITEMAP_CONTENT" | grep -c "<loc>https://vietmoto.top/[^/]*</loc>" || echo "0")
MOTORCYCLES=$(echo "$SITEMAP_CONTENT" | grep -c "motorcycles/" || echo "0")
CARS=$(echo "$SITEMAP_CONTENT" | grep -c "/cars/" || echo "0")
REVIEWS=$(echo "$SITEMAP_CONTENT" | grep -c "/reviews/" || echo "0")
QA=$(echo "$SITEMAP_CONTENT" | grep -c "/qa/" || echo "0")
MARKETPLACE=$(echo "$SITEMAP_CONTENT" | grep -c "/marketplace/" || echo "0")

echo "   - 静态页面:    $STATIC 个"
echo "   - 摩托车:      $MOTORCYCLES 个"
echo "   - 汽车:        $CARS 个"
echo "   - 测评:        $REVIEWS 个"
echo "   - 问答:        $QA 个"
echo "   - 二手车:      $MARKETPLACE 个"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL=$((STATIC + MOTORCYCLES + CARS + REVIEWS + QA + MARKETPLACE))
echo "   - 总计:        $TOTAL 个"
echo ""

# 5. 检查服务日志
echo "5️⃣ 最近的Sitemap生成日志:"
journalctl -u vietnam-moto-frontend -n 500 --no-pager 2>/dev/null | grep "\[Sitemap\]" | tail -15 | sed 's/^/   /'
echo ""

# 6. 抽样检查URL可访问性
echo "6️⃣ 抽样检查URL可访问性:"
SAMPLE_URLS=$(echo "$SITEMAP_CONTENT" | grep -oP '(?<=<loc>)[^<]+' | head -10)
SUCCESS_COUNT=0
FAIL_COUNT=0

while IFS= read -r url; do
  if [ -n "$url" ]; then
    # 转换为本地URL
    LOCAL_URL=$(echo "$url" | sed 's|https://vietmoto.top|http://localhost:4321|')
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$LOCAL_URL")
    
    if [ "$HTTP_CODE" == "200" ]; then
      SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
      FAIL_COUNT=$((FAIL_COUNT + 1))
      echo "   ⚠️ $url → HTTP $HTTP_CODE"
    fi
  fi
done <<< "$SAMPLE_URLS"

echo "   ✅ 成功: $SUCCESS_COUNT/10"
if [ $FAIL_COUNT -gt 0 ]; then
  echo "   ❌ 失败: $FAIL_COUNT/10"
fi
echo ""

# 7. 最终总结
echo "=========================================="
echo "📋 验证总结"
echo "=========================================="
if [ "$STATUS" == "200" ] && [ "$INDEX_STATUS" == "404" ] && [ $FAIL_COUNT -eq 0 ]; then
  echo "✅ 所有检查通过！Sitemap已成功优化"
  echo ""
  echo "🎯 下一步操作："
  echo "   1. 在Google Search Console重新提交sitemap.xml"
  echo "   2. 删除旧的sitemap-index.xml引用"
  echo "   3. 监控索引状态和404错误率"
else
  echo "⚠️ 部分检查未通过，请查看上述详情"
fi
echo "=========================================="

