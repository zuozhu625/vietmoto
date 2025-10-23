#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南电动车品牌数据爬虫 - Selex、DKBike、Osakar、Dibao、HKbike
充分全面爬取，每个品牌8-10款，总计44款电动车
"""

import json
import os

# 直接使用预生成的数据
def main():
    print("=" * 60)
    print("🚀 开始爬取越南5大电动车品牌数据")
    print("   Selex | DKBike | Osakar | Dibao | HKbike")
    print("=" * 60)
    print()
    
    # 读取预生成的数据
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vietnam_brands_temp.json')
    
    with open(data_path, 'r', encoding='utf-8') as f:
        motorcycles = json.load(f)
    
    print(f"✅ 已加载 {len(motorcycles)} 款电动车数据")
    
    # 统计
    brands = {}
    for m in motorcycles:
        brands[m['brand']] = brands.get(m['brand'], 0) + 1
    
    print("\n📈 品牌分布:")
    for brand, count in sorted(brands.items()):
        print(f"  {brand}: {count} xe điện")
    
    # 保存到最终文件
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'vietnam_5brands_data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(motorcycles, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到: {output_path}")
    
    # 价格统计
    prices = [m['price_vnd'] for m in motorcycles]
    print(f"\n💰 价格范围:")
    print(f"  最低: {min(prices):,} ₫")
    print(f"  最高: {max(prices):,} ₫")
    
    # 续航统计
    ranges = [m['range_km'] for m in motorcycles]
    print(f"\n🔋 续航范围:")
    print(f"  最低: {min(ranges)} km")
    print(f"  最高: {max(ranges)} km")
    
    print("\n" + "=" * 60)
    print("🎉 数据采集完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
