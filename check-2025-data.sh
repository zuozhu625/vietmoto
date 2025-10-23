#!/bin/bash

# ============================================
# 2025年车型数据检查脚本
# ============================================

echo "🔍 检查2025年车型数据..."
echo ""

DB_PATH="/var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite"

if [ ! -f "$DB_PATH" ]; then
    echo "❌ 数据库文件不存在: $DB_PATH"
    exit 1
fi

echo "📊 数据统计："
CARS_2025=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM cars WHERE year = 2025;" 2>/dev/null || echo "0")
MOTORCYCLES_2025=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM motorcycles WHERE year = 2025;" 2>/dev/null || echo "0")

echo "   🚗 2025年汽车: $CARS_2025 辆"
echo "   🏍️  2025年摩托车: $MOTORCYCLES_2025 辆"
echo ""

if [ "$CARS_2025" -gt 0 ]; then
    echo "🚗 2025年汽车样本："
    sqlite3 "$DB_PATH" "SELECT '   ' || brand || ' ' || model || ' (' || CAST(price_vnd/1000000 AS INTEGER) || ' triệu VND)' FROM cars WHERE year = 2025 ORDER BY brand, price_vnd LIMIT 5;"
    echo ""
fi

if [ "$MOTORCYCLES_2025" -gt 0 ]; then
    echo "🏍️  2025年摩托车样本："
    sqlite3 "$DB_PATH" "SELECT '   ' || brand || ' ' || model || ' (' || CAST(price_vnd/1000000 AS INTEGER) || ' triệu VND)' FROM motorcycles WHERE year = 2025 ORDER BY brand, price_vnd LIMIT 5;"
    echo ""
fi

TOTAL_2025=$((CARS_2025 + MOTORCYCLES_2025))
if [ "$TOTAL_2025" -gt 0 ]; then
    echo "✅ 2025年数据完整！总计 $TOTAL_2025 辆车型"
else
    echo "❌ 未找到2025年数据，可能需要重新导入"
fi
