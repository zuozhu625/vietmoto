#!/bin/bash
# 快速验证三个品牌数据

echo "======================================================"
echo "    快速验证 Suzuki、Piaggio、SYM 数据"
echo "======================================================"
echo ""

# 数据库查询
echo "📊 数据库车型统计:"
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite << SQL
SELECT '  ' || brand || ': ' || COUNT(*) || '款 (价格: ' || 
       MIN(price_vnd)/1000000 || '-' || MAX(price_vnd)/1000000 || '百万₫)'
FROM motorcycles 
WHERE brand IN ('Suzuki', 'Piaggio', 'SYM')
GROUP BY brand
ORDER BY brand;
SQL

echo ""
echo "======================================================"
echo "✅ 验证完成！"
echo "======================================================"
