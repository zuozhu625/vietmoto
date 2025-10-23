#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南汽车数据爬虫 - 6个品牌初始数据
方案A：30个核心字段
"""

import json
import os

def create_car(brand, model, year, category, slug, price, seats, **kwargs):
    """创建汽车数据模板"""
    return {
        # 基础信息
        'brand': brand,
        'model': model,
        'year': year,
        'category': category,
        'slug': slug,
        'price_vnd': price,
        'seating_capacity': seats,
        
        # 发动机系统
        'engine_capacity_l': kwargs.get('engine_l'),
        'engine_type': kwargs.get('engine_type'),
        'power_hp': kwargs.get('power_hp'),
        'torque_nm': kwargs.get('torque_nm'),
        'fuel_type': kwargs.get('fuel_type', 'Xăng'),
        'transmission': kwargs.get('transmission'),
        'drive_type': kwargs.get('drive_type', 'FWD'),
        'cylinder_count': kwargs.get('cylinders', 4),
        
        # 电动车参数
        'battery_kwh': kwargs.get('battery_kwh'),
        'range_km': kwargs.get('range_km'),
        'charge_time_h': kwargs.get('charge_time'),
        
        # 尺寸重量
        'length_mm': kwargs.get('length'),
        'width_mm': kwargs.get('width'),
        'height_mm': kwargs.get('height'),
        'wheelbase_mm': kwargs.get('wheelbase'),
        'curb_weight_kg': kwargs.get('weight'),
        'trunk_capacity_l': kwargs.get('trunk'),
        
        # 配置信息
        'abs': kwargs.get('abs', True),
        'airbag_count': kwargs.get('airbags'),
        'smart_key': kwargs.get('smart_key', False),
        'display_type': kwargs.get('display'),
        'infotainment_size': kwargs.get('screen'),
        'fuel_consumption': kwargs.get('fuel_cons'),
        
        # 系统字段
        'description': kwargs.get('desc', f'{brand} {model} {year} - {category}'),
        'features': kwargs.get('features'),
        'colors': kwargs.get('colors', 'Trắng, Đen, Bạc, Xám'),
        'rating': kwargs.get('rating', 4.5),
        'status': 'active'
    }

def main():
    print("=" * 60)
    print("🚗 开始生成越南汽车数据（6个品牌）")
    print("=" * 60)
    print()
    
    cars = []
    
    # Toyota Vios 2024
    cars.append(create_car(
        'Toyota', 'Vios', 2024, 'Sedan hạng B', 'toyota-vios-2024',
        458000000, 5,
        engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, VVT-i',
        power_hp=107, torque_nm=140, transmission='CVT',
        drive_type='FWD', cylinders=4,
        length=4425, width=1730, height=1475, wheelbase=2550,
        weight=1095, trunk=475,
        abs=True, airbags=7, smart_key=True,
        display='TFT 4.2 inch', screen=9.0,
        fuel_cons='5.3L/100km',
        desc='Sedan hạng B bán chạy nhất, động cơ 1.5L tiết kiệm, không gian rộng rãi, trang bị an toàn đầy đủ, giá trị bền vững.',
        features='7 túi khí, Honda SENSING, Camera 360°, Màn hình 9 inch, Chìa khóa thông minh',
        rating=4.6
    ))
    
    # VinFast VF8 2024
    cars.append(create_car(
        'VinFast', 'VF8', 2024, 'SUV điện', 'vinfast-vf8-2024',
        1200000000, 7,
        fuel_type='Điện',
        battery_kwh=87.7, range_km=471, charge_time=7.5,
        power_hp=402, torque_nm=640,
        transmission='Hộp số tự động 1 cấp', drive_type='AWD',
        length=4750, width=1934, height=1667, wheelbase=2950,
        weight=2145, trunk=376,
        abs=True, airbags=11, smart_key=True,
        display='TFT 12.3 inch', screen=15.6,
        fuel_cons='0 L/100km (Điện)',
        desc='SUV điện cao cấp, động cơ kép AWD 402 mã lực, pin 87.7 kWh, tầm hoạt động 471km, tích hợp ADAS cấp độ 2+.',
        features='11 túi khí, ADAS cấp 2+, Màn hình 15.6 inch, Sạc nhanh, Động cơ kép AWD',
        rating=4.5
    ))
    
    # Hyundai Creta 2024
    cars.append(create_car(
        'Hyundai', 'Creta', 2024, 'SUV cỡ nhỏ', 'hyundai-creta-2024',
        640000000, 5,
        engine_l=1.5, engine_type='4 xi-lanh thẳng hàng Turbo',
        power_hp=140, torque_nm=242, transmission='CVT',
        drive_type='FWD', cylinders=4,
        length=4315, width=1790, height=1630, wheelbase=2610,
        weight=1210, trunk=433,
        abs=True, airbags=6, smart_key=True,
        display='TFT 4.2 inch', screen=10.25,
        fuel_cons='6.2L/100km',
        desc='SUV cỡ nhỏ thông minh, động cơ tăng áp 1.5T, SmartSense cấp độ 2, thiết kế hiện đại, giá trị vượt trội.',
        features='6 túi khí, SmartSense L2, Màn hình 10.25 inch, Chìa khóa thông minh, Camera 360°',
        rating=4.7
    ))
    
    # Mazda CX-5 2024
    cars.append(create_car(
        'Mazda', 'CX-5', 2024, 'SUV cỡ trung', 'mazda-cx5-2024',
        859000000, 5,
        engine_l=2.5, engine_type='4 xi-lanh thẳng hàng, SKYACTIV-G',
        power_hp=188, torque_nm=252, transmission='AT 6 cấp',
        drive_type='AWD', cylinders=4,
        length=4575, width=1842, height=1685, wheelbase=2700,
        weight=1620, trunk=442,
        abs=True, airbags=6, smart_key=True,
        display='TFT 7 inch', screen=10.25,
        fuel_cons='7.2L/100km',
        desc='SUV Nhật Bản cao cấp, động cơ 2.5L SKYACTIV-G, thiết kế Kodo sang trọng, công nghệ i-Activsense, trải nghiệm lái xuất sắc.',
        features='6 túi khí, i-Activsense, Màn hình 10.25 inch, HUD, AWD thông minh, Bose 10 loa',
        rating=4.8
    ))
    
    # Honda City 2024
    cars.append(create_car(
        'Honda', 'City', 2024, 'Sedan hạng B', 'honda-city-2024',
        559000000, 5,
        engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, i-VTEC',
        power_hp=119, torque_nm=145, transmission='CVT',
        drive_type='FWD', cylinders=4,
        length=4589, width=1748, height=1467, wheelbase=2600,
        weight=1155, trunk=506,
        abs=True, airbags=6, smart_key=True,
        display='TFT 7 inch', screen=8.0,
        fuel_cons='5.0L/100km',
        desc='Sedan hạng B cao cấp, động cơ 1.5L i-VTEC, Honda SENSING an toàn, không gian nội thất rộng rãi nhất phân khúc.',
        features='6 túi khí, Honda SENSING, Màn hình 8 inch, Cảm biến lùi, Chìa khóa thông minh',
        rating=4.7
    ))
    
    # Mitsubishi Xpander 2024
    cars.append(create_car(
        'Mitsubishi', 'Xpander', 2024, 'MPV 7 chỗ', 'mitsubishi-xpander-2024',
        598000000, 7,
        engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, MIVEC',
        power_hp=105, torque_nm=141, transmission='AT 4 cấp',
        drive_type='FWD', cylinders=4,
        length=4595, width=1750, height=1730, wheelbase=2775,
        weight=1220, trunk=243,
        abs=True, airbags=2, smart_key=False,
        display='LCD analog', screen=7.0,
        fuel_cons='6.8L/100km',
        desc='MPV 7 chỗ đa năng, động cơ 1.5L MIVEC, không gian linh hoạt, phù hợp gia đình đông người, giá cả phải chăng.',
        features='2 túi khí, Màn hình 7 inch, Hàng ghế 3 gập 50:50, Cửa sổ trời, Điều hòa 2 dàn',
        rating=4.6
    ))
    
    print(f"✅ 已生成 {len(cars)} 款汽车数据\n")
    
    # 统计
    brands = {}
    for car in cars:
        brands[car['brand']] = brands.get(car['brand'], 0) + 1
    
    print("📊 品牌统计:")
    for brand, count in sorted(brands.items()):
        print(f"  {brand}: {count} xe")
    
    print(f"\n💰 价格范围:")
    prices = [c['price_vnd'] for c in cars]
    print(f"  最低: {min(prices):,} ₫ ({min(prices)/1000000:.0f} triệu)")
    print(f"  最高: {max(prices):,} ₫ ({max(prices)/1000000:.0f} triệu)")
    
    # 保存数据
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, 'cars_data.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到: {output_file}")
    print("\n" + "=" * 60)
    print("🎉 汽车数据生成完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
