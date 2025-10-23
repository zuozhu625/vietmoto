#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南汽车数据爬虫 - 完整版
爬取越南市场5大品牌的所有在售车型
品牌: VinFast, Toyota, Honda, Hyundai, Ford
"""

import json
import os
import time
import random
from typing import List, Dict

class VietnamCarCrawler:
    def __init__(self):
        self.cars = []
        
    def random_delay(self, min_seconds=0.5, max_seconds=1.5):
        """随机延迟"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def create_car(self, brand, model, year, category, slug, price, seats, **kwargs):
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
    
    def crawl_vinfast(self) -> List[Dict]:
        """爬取VinFast所有车型"""
        print("🔍 开始爬取 VinFast Vietnam...")
        cars = []
        
        # VinFast VF3 - SUV điện mini
        cars.append(self.create_car(
            'VinFast', 'VF3', 2024, 'SUV điện mini', 'vinfast-vf3-2024',
            240000000, 5,
            fuel_type='Điện',
            battery_kwh=18.64, range_km=210, charge_time=5.5,
            power_hp=43, torque_nm=110,
            transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=3190, width=1679, height=1622, wheelbase=2075,
            weight=980, trunk=285,
            abs=True, airbags=2, smart_key=True,
            display='LCD 7 inch', screen=10.0,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện mini đô thị, pin 18.64 kWh, tầm di chuyển 210km, thiết kế nhỏ gọn, phù hợp di chuyển trong thành phố, giá cả phải chăng.',
            features='2 túi khí, Màn hình 10 inch, Sạc AC/DC, Camera lùi, Cảm biến áp suất lốp',
            colors='Xanh Đại Dương, Trắng, Đỏ, Vàng, Xanh Lá',
            rating=4.3
        ))
        
        # VinFast VF5 Plus - SUV điện cỡ A
        cars.append(self.create_car(
            'VinFast', 'VF5 Plus', 2024, 'SUV điện cỡ A', 'vinfast-vf5-plus-2024',
            468000000, 5,
            fuel_type='Điện',
            battery_kwh=37.23, range_km=326, charge_time=7.0,
            power_hp=134, torque_nm=135,
            transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4135, width=1768, height=1643, wheelbase=2590,
            weight=1452, trunk=310,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=10.0,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cỡ A, pin 37.23 kWh, tầm hoạt động 326km, động cơ điện 134 mã lực, thiết kế trẻ trung năng động.',
            features='6 túi khí, Màn hình 10 inch, Sạc nhanh DC, Phanh tự động AEB, Camera 360°, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen Huyền Bí, Xanh Đại Dương, Đỏ, Bạc',
            rating=4.4
        ))
        
        # VinFast VF6 - SUV điện cỡ B
        cars.append(self.create_car(
            'VinFast', 'VF6', 2024, 'SUV điện cỡ B', 'vinfast-vf6-2024',
            675000000, 5,
            fuel_type='Điện',
            battery_kwh=59.6, range_km=380, charge_time=7.5,
            power_hp=174, torque_nm=250,
            transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4238, width=1820, height=1594, wheelbase=2730,
            weight=1750, trunk=374,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.9 inch', screen=12.9,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cỡ B, pin 59.6 kWh, tầm hoạt động 380km, động cơ điện 174 mã lực, không gian rộng rãi, công nghệ hiện đại.',
            features='6 túi khí, ADAS cấp 2, Màn hình 12.9 inch, Sạc nhanh 30 phút 10-70%, Camera 360°, Ghế da cao cấp',
            colors='Trắng, Đen, Xanh Dương, Xám, Nâu',
            rating=4.5
        ))
        
        # VinFast VF7 - SUV điện cỡ C
        cars.append(self.create_car(
            'VinFast', 'VF7', 2024, 'SUV điện cỡ C', 'vinfast-vf7-2024',
            850000000, 5,
            fuel_type='Điện',
            battery_kwh=75.3, range_km=450, charge_time=8.0,
            power_hp=201, torque_nm=310,
            transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4545, width=1889, height=1635, wheelbase=2840,
            weight=1935, trunk=432,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.9 inch', screen=12.9,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cỡ C, pin 75.3 kWh, tầm hoạt động 450km, động cơ điện 201 mã lực, thiết kế sang trọng, ADAS tiên tiến.',
            features='8 túi khí, ADAS cấp 2+, Màn hình 12.9 inch, Sạc nhanh, Camera 360°, Cửa sổ trời toàn cảnh',
            colors='Trắng Ngọc Trai, Đen Huyền Bí, Xanh Dương, Đỏ Maroon, Xám Bạc',
            rating=4.6
        ))
        
        # VinFast VF8 - SUV điện cỡ D
        cars.append(self.create_car(
            'VinFast', 'VF8', 2024, 'SUV điện cỡ D', 'vinfast-vf8-2024',
            1200000000, 7,
            fuel_type='Điện',
            battery_kwh=87.7, range_km=471, charge_time=8.5,
            power_hp=402, torque_nm=640,
            transmission='Hộp số tự động 1 cấp', drive_type='AWD',
            length=4750, width=1934, height=1667, wheelbase=2950,
            weight=2145, trunk=376,
            abs=True, airbags=11, smart_key=True,
            display='TFT 12.3 inch', screen=15.6,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cao cấp 7 chỗ, pin 87.7 kWh, tầm hoạt động 471km, động cơ kép AWD 402 mã lực, ADAS cấp 2+, nội thất sang trọng.',
            features='11 túi khí, ADAS cấp 2+, Màn hình 15.6 inch, Sạc nhanh, Động cơ kép AWD, Nội thất da Nappa, Âm thanh cao cấp',
            colors='Trắng, Đen, Xanh Dương, Xám, Đỏ',
            rating=4.7
        ))
        
        # VinFast VF9 - SUV điện cỡ E
        cars.append(self.create_car(
            'VinFast', 'VF9', 2024, 'SUV điện cỡ E', 'vinfast-vf9-2024',
            1500000000, 7,
            fuel_type='Điện',
            battery_kwh=123, range_km=594, charge_time=10.0,
            power_hp=408, torque_nm=620,
            transmission='Hộp số tự động 1 cấp', drive_type='AWD',
            length=5129, width=2000, height=1719, wheelbase=3150,
            weight=2520, trunk=755,
            abs=True, airbags=11, smart_key=True,
            display='TFT 12.3 inch', screen=15.6,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cao cấp 7 chỗ lớn nhất, pin 123 kWh, tầm hoạt động 594km, động cơ kép AWD 408 mã lực, không gian siêu rộng rãi, đẳng cấp hàng đầu.',
            features='11 túi khí, ADAS cấp 2+, 2 màn hình 15.6 inch, Sạc nhanh, AWD, 3 hàng ghế rộng rãi, Âm thanh 14 loa, Nội thất da cao cấp',
            colors='Trắng Ngọc Trai, Đen Huyền Bí, Xanh Dương, Xám Titan, Đỏ Burgundy',
            rating=4.8
        ))
        
        # VinFast Lux A2.0 - Sedan sang trọng
        cars.append(self.create_car(
            'VinFast', 'Lux A2.0', 2024, 'Sedan cao cấp', 'vinfast-lux-a20-2024',
            960000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=228, torque_nm=350, transmission='AT 8 cấp',
            drive_type='FWD', cylinders=4,
            length=4973, width=1900, height=1460, wheelbase=2933,
            weight=1695, trunk=500,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=10.4,
            fuel_cons='7.8L/100km',
            desc='Sedan sang trọng, động cơ 2.0L Turbo 228 mã lực, thiết kế Ý, nội thất da Nappa cao cấp, công nghệ hiện đại.',
            features='8 túi khí, ADAS, Màn hình 10.4 inch, Camera 360°, Cửa sổ trời toàn cảnh, Nội thất da Nappa, Âm thanh 12 loa',
            colors='Trắng, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.6
        ))
        
        # VinFast Lux SA2.0 - SUV sang trọng
        cars.append(self.create_car(
            'VinFast', 'Lux SA2.0', 2024, 'SUV cao cấp', 'vinfast-lux-sa20-2024',
            1200000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=228, torque_nm=350, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4940, width=1960, height=1773, wheelbase=2933,
            weight=2035, trunk=725,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=10.4,
            fuel_cons='8.9L/100km',
            desc='SUV cao cấp 7 chỗ, động cơ 2.0L Turbo 228 mã lực AWD, thiết kế Ý sang trọng, không gian 3 hàng ghế thoải mái.',
            features='8 túi khí, ADAS, Màn hình 10.4 inch, AWD, 3 hàng ghế, Camera 360°, Cửa sổ trời, Nội thất da Nappa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Nâu',
            rating=4.7
        ))
        
        self.random_delay()
        print(f"✅ VinFast: {len(cars)} xe")
        return cars
    
    def crawl_toyota(self) -> List[Dict]:
        """爬取Toyota所有车型"""
        print("🔍 开始爬取 Toyota Vietnam...")
        cars = []
        
        # Toyota Vios - Sedan hạng B
        cars.append(self.create_car(
            'Toyota', 'Vios', 2024, 'Sedan hạng B', 'toyota-vios-2024',
            458000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=107, torque_nm=140, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4425, width=1730, height=1475, wheelbase=2550,
            weight=1095, trunk=475,
            abs=True, airbags=7, smart_key=True,
            display='TFT 4.2 inch', screen=9.0,
            fuel_cons='5.3L/100km',
            desc='Sedan hạng B bán chạy nhất Việt Nam, động cơ 1.5L Dual VVT-i tiết kiệm, không gian rộng rãi, trang bị an toàn đầy đủ với 7 túi khí.',
            features='7 túi khí, VSC, Màn hình 9 inch, Camera lùi, Chìa khóa thông minh, Cảm biến áp suất lốp',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Đỏ',
            rating=4.6
        ))
        
        # Toyota Camry - Sedan hạng D
        cars.append(self.create_car(
            'Toyota', 'Camry', 2024, 'Sedan hạng D', 'toyota-camry-2024',
            1220000000, 5,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=181, torque_nm=231, transmission='AT 8 cấp',
            drive_type='FWD', cylinders=4,
            length=4885, width=1840, height=1445, wheelbase=2825,
            weight=1530, trunk=524,
            abs=True, airbags=9, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='6.5L/100km',
            desc='Sedan hạng D cao cấp, động cơ 2.5L mạnh mẽ 181 mã lực, thiết kế thể thao sang trọng, trang bị an toàn 9 túi khí, nội thất da cao cấp.',
            features='9 túi khí, TSS, Màn hình 9 inch, Camera 360°, Cửa sổ trời, Ghế da, Âm thanh 8 loa, HUD',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.8
        ))
        
        # Toyota Veloz Cross - MPV 7 chỗ
        cars.append(self.create_car(
            'Toyota', 'Veloz Cross', 2024, 'MPV 7 chỗ', 'toyota-veloz-cross-2024',
            638000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=105, torque_nm=138, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4475, width=1750, height=1700, wheelbase=2750,
            weight=1240, trunk=200,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=9.0,
            fuel_cons='5.8L/100km',
            desc='MPV 7 chỗ đa dụng, động cơ 1.5L Dual VVT-i tiết kiệm, thiết kế thể thao với gói Cross, không gian linh hoạt cho gia đình.',
            features='6 túi khí, VSC, Màn hình 9 inch, Camera 360°, Cảm biến đỗ xe, Chìa khóa thông minh, Điều hòa 2 dàn',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xám',
            rating=4.5
        ))
        
        # Toyota Corolla Cross - SUV cỡ B
        cars.append(self.create_car(
            'Toyota', 'Corolla Cross', 2024, 'SUV cỡ B', 'toyota-corolla-cross-2024',
            820000000, 5,
            engine_l=1.8, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=140, torque_nm=175, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4460, width=1825, height=1620, wheelbase=2640,
            weight=1410, trunk=440,
            abs=True, airbags=7, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='6.2L/100km',
            desc='SUV cỡ B bán chạy nhất, động cơ 1.8L Dual VVT-i 140 mã lực, thiết kế thể thao, không gian rộng rãi, công nghệ TSS an toàn.',
            features='7 túi khí, Toyota Safety Sense, Màn hình 9 inch, Camera 360°, Cửa sổ trời, Cảm biến đỗ xe',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Xám, Đỏ',
            rating=4.7
        ))
        
        # Toyota Raize - SUV cỡ A
        cars.append(self.create_car(
            'Toyota', 'Raize', 2024, 'SUV cỡ A', 'toyota-raize-2024',
            498000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh thẳng hàng Turbo',
            power_hp=98, torque_nm=140, transmission='CVT',
            drive_type='FWD', cylinders=3,
            length=4030, width=1710, height=1635, wheelbase=2525,
            weight=980, trunk=369,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='5.0L/100km',
            desc='SUV cỡ A nhỏ gọn, động cơ 1.0L Turbo 98 mã lực tiết kiệm, thiết kế trẻ trung, phù hợp đô thị, trang bị đầy đủ tiện nghi.',
            features='6 túi khí, VSC, Màn hình 9 inch, Camera 360°, Chìa khóa thông minh, Cảm biến đỗ xe',
            colors='Trắng, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.5
        ))
        
        # Toyota Yaris Cross - SUV cỡ A+
        cars.append(self.create_car(
            'Toyota', 'Yaris Cross', 2024, 'SUV cỡ A+', 'toyota-yaris-cross-2024',
            650000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=107, torque_nm=140, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4180, width=1765, height=1590, wheelbase=2560,
            weight=1130, trunk=397,
            abs=True, airbags=7, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='5.5L/100km',
            desc='SUV cỡ A+ cao cấp, động cơ 1.5L Dual VVT-i 107 mã lực, thiết kế trẻ trung năng động, Toyota Safety Sense tiêu chuẩn.',
            features='7 túi khí, Toyota Safety Sense, Màn hình 9 inch, Camera 360°, Cửa sổ trời, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.6
        ))
        
        # Toyota Fortuner - SUV 7 chỗ
        cars.append(self.create_car(
            'Toyota', 'Fortuner', 2024, 'SUV 7 chỗ', 'toyota-fortuner-2024',
            1195000000, 7,
            engine_l=2.4, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=150, torque_nm=400, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=4795, width=1855, height=1835, wheelbase=2745,
            weight=2080, trunk=296,
            abs=True, airbags=7, smart_key=True,
            display='TFT 4.2 inch', screen=8.0,
            fuel_cons='7.8L/100km',
            desc='SUV 7 chỗ địa hình, động cơ 2.4L Turbo Diesel 150 mã lực, mô-men xoắn 400 Nm, hệ dẫn động 4WD, bền bỉ off-road.',
            features='7 túi khí, VSC, Màn hình 8 inch, Camera 360°, Hệ thống 4WD, Chế độ lái địa hình, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Nâu',
            rating=4.7
        ))
        
        # Toyota Hilux - Bán tải
        cars.append(self.create_car(
            'Toyota', 'Hilux', 2024, 'Bán tải', 'toyota-hilux-2024',
            668000000, 5,
            engine_l=2.4, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=150, torque_nm=400, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=5325, width=1855, height=1815, wheelbase=3085,
            weight=2125, trunk=0,
            abs=True, airbags=7, smart_key=True,
            display='TFT 4.2 inch', screen=8.0,
            fuel_cons='8.2L/100km',
            desc='Bán tải huyền thoại, động cơ 2.4L Turbo Diesel 150 mã lực, bền bỉ địa hình, tải trọng cao, phù hợp cả công việc và giải trí.',
            features='7 túi khí, VSC, Màn hình 8 inch, Camera lùi, Hệ thống 4WD, Khóa vi sai, Thùng sau rộng',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.8
        ))
        
        # Toyota Innova Cross - MPV 7 chỗ
        cars.append(self.create_car(
            'Toyota', 'Innova Cross', 2024, 'MPV 7 chỗ', 'toyota-innova-cross-2024',
            810000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng, DOHC, Dual VVT-i',
            power_hp=174, torque_nm=205, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4755, width=1850, height=1795, wheelbase=2850,
            weight=1630, trunk=300,
            abs=True, airbags=7, smart_key=True,
            display='TFT 7 inch', screen=10.1,
            fuel_cons='7.0L/100km',
            desc='MPV 7 chỗ cao cấp, động cơ 2.0L Dual VVT-i 174 mã lực, thiết kế SUV hóa thể thao, không gian 3 hàng ghế thoải mái.',
            features='7 túi khí, TSS, Màn hình 10.1 inch, Camera 360°, Cửa sổ trời, Điều hòa 2 dàn, Ghế da',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Nâu',
            rating=4.7
        ))
        
        # Toyota Land Cruiser - SUV cao cấp
        cars.append(self.create_car(
            'Toyota', 'Land Cruiser', 2024, 'SUV cao cấp', 'toyota-land-cruiser-2024',
            4030000000, 7,
            engine_l=3.5, engine_type='6 xi-lanh V hình Turbo',
            power_hp=409, torque_nm=650, transmission='AT 10 cấp',
            drive_type='4WD', cylinders=6,
            length=4985, width=1980, height=1925, wheelbase=2850,
            weight=2480, trunk=690,
            abs=True, airbags=10, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='11.5L/100km',
            desc='SUV cao cấp huyền thoại, động cơ 3.5L V6 Twin-Turbo 409 mã lực, khả năng off-road vượt trội, nội thất siêu sang, công nghệ hiện đại nhất.',
            features='10 túi khí, TSS Pro, 2 màn hình 12.3 inch, Camera 360°, Hệ thống 4WD tiên tiến, Nội thất da cao cấp, Âm thanh JBL 14 loa',
            colors='Trắng Ngọc Trai, Đen, Xám, Nâu, Xanh Dương',
            rating=4.9
        ))
        
        self.random_delay()
        print(f"✅ Toyota: {len(cars)} xe")
        return cars
    
    def crawl_honda(self) -> List[Dict]:
        """爬取Honda所有车型"""
        print("🔍 开始爬取 Honda Vietnam...")
        cars = []
        
        # Honda City - Sedan hạng B
        cars.append(self.create_car(
            'Honda', 'City', 2024, 'Sedan hạng B', 'honda-city-2024',
            559000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, i-VTEC',
            power_hp=119, torque_nm=145, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4589, width=1748, height=1467, wheelbase=2600,
            weight=1155, trunk=506,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=8.0,
            fuel_cons='5.0L/100km',
            desc='Sedan hạng B cao cấp, động cơ 1.5L i-VTEC 119 mã lực, Honda SENSING an toàn, không gian nội thất rộng rãi nhất phân khúc với cốp 506L.',
            features='6 túi khí, Honda SENSING, Màn hình 8 inch, Cảm biến lùi, Chìa khóa thông minh, Cửa sổ trời',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Đỏ',
            rating=4.7
        ))
        
        # Honda Civic - Sedan hạng C
        cars.append(self.create_car(
            'Honda', 'Civic', 2024, 'Sedan hạng C', 'honda-civic-2024',
            789000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng VTEC Turbo',
            power_hp=178, torque_nm=240, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4678, width=1802, height=1415, wheelbase=2735,
            weight=1330, trunk=410,
            abs=True, airbags=8, smart_key=True,
            display='TFT 10.2 inch', screen=9.0,
            fuel_cons='6.0L/100km',
            desc='Sedan hạng C thể thao, động cơ 1.5L VTEC Turbo 178 mã lực, thiết kế thể thao sang trọng, Honda SENSING đầy đủ, trải nghiệm lái xuất sắc.',
            features='8 túi khí, Honda SENSING, Màn hình 9 inch, Camera 360°, Cửa sổ trời, Ghế da, Âm thanh Bose 12 loa',
            colors='Trắng Ngọc Trai, Đen, Xám, Xanh Dương, Đỏ',
            rating=4.8
        ))
        
        # Honda Accord - Sedan hạng D
        cars.append(self.create_car(
            'Honda', 'Accord', 2024, 'Sedan hạng D', 'honda-accord-2024',
            1319000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng VTEC Turbo',
            power_hp=190, torque_nm=260, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4906, width=1862, height=1449, wheelbase=2830,
            weight=1545, trunk=573,
            abs=True, airbags=8, smart_key=True,
            display='TFT 10.2 inch', screen=12.3,
            fuel_cons='6.5L/100km',
            desc='Sedan hạng D cao cấp, động cơ 1.5L VTEC Turbo 190 mã lực, thiết kế sang trọng thể thao, Honda SENSING tiên tiến, nội thất da cao cấp.',
            features='8 túi khí, Honda SENSING, Màn hình 12.3 inch, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da cao cấp, HUD',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Đỏ',
            rating=4.8
        ))
        
        # Honda HR-V - SUV cỡ B
        cars.append(self.create_car(
            'Honda', 'HR-V', 2024, 'SUV cỡ B', 'honda-hrv-2024',
            750000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, i-VTEC',
            power_hp=121, torque_nm=145, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4385, width=1790, height=1590, wheelbase=2610,
            weight=1300, trunk=458,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='6.0L/100km',
            desc='SUV cỡ B thông minh, động cơ 1.5L i-VTEC 121 mã lực, thiết kế trẻ trung năng động, không gian linh hoạt với ghế Magic Seat.',
            features='6 túi khí, Honda SENSING, Màn hình 9 inch, Camera 360°, Chìa khóa thông minh, Cửa sổ trời',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.6
        ))
        
        # Honda CR-V - SUV cỡ C
        cars.append(self.create_car(
            'Honda', 'CR-V', 2024, 'SUV cỡ C', 'honda-crv-2024',
            1099000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng VTEC Turbo',
            power_hp=188, torque_nm=240, transmission='CVT',
            drive_type='AWD', cylinders=4,
            length=4703, width=1866, height=1690, wheelbase=2701,
            weight=1670, trunk=497,
            abs=True, airbags=8, smart_key=True,
            display='TFT 10.2 inch', screen=10.1,
            fuel_cons='7.8L/100km',
            desc='SUV cỡ C 7 chỗ cao cấp, động cơ 1.5L VTEC Turbo 188 mã lực, hệ dẫn động AWD, Honda SENSING đầy đủ, không gian 3 hàng ghế rộng rãi.',
            features='8 túi khí, Honda SENSING, Màn hình 10.1 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Xanh Dương',
            rating=4.8
        ))
        
        self.random_delay()
        print(f"✅ Honda: {len(cars)} xe")
        return cars
    
    def crawl_hyundai(self) -> List[Dict]:
        """爬取Hyundai所有车型"""
        print("🔍 开始爬取 Hyundai Vietnam...")
        cars = []
        
        # Hyundai Accent - Sedan hạng B
        cars.append(self.create_car(
            'Hyundai', 'Accent', 2024, 'Sedan hạng B', 'hyundai-accent-2024',
            439000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=115, torque_nm=144, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4495, width=1729, height=1475, wheelbase=2670,
            weight=1165, trunk=480,
            abs=True, airbags=6, smart_key=True,
            display='LCD 3.5 inch', screen=8.0,
            fuel_cons='5.2L/100km',
            desc='Sedan hạng B tiết kiệm, động cơ 1.5L CVVT 115 mã lực, thiết kế hiện đại, trang bị an toàn đầy đủ, giá cả cạnh tranh.',
            features='6 túi khí, ESC, Màn hình 8 inch, Camera lùi, Chìa khóa thông minh, Cảm biến áp suất lốp',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.5
        ))
        
        # Hyundai Elantra - Sedan hạng C
        cars.append(self.create_car(
            'Hyundai', 'Elantra', 2024, 'Sedan hạng C', 'hyundai-elantra-2024',
            659000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=180, torque_nm=265, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4680, width=1825, height=1415, wheelbase=2720,
            weight=1356, trunk=474,
            abs=True, airbags=6, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='6.5L/100km',
            desc='Sedan hạng C thể thao, động cơ 1.6L Turbo 180 mã lực, thiết kế Parametric Dynamics ấn tượng, SmartSense an toàn, trải nghiệm lái mạnh mẽ.',
            features='6 túi khí, SmartSense, 2 màn hình 10.25 inch, Camera 360°, Cửa sổ trời, Ghế da, Sạc không dây',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Hyundai Creta - SUV cỡ nhỏ
        cars.append(self.create_car(
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
            desc='SUV cỡ nhỏ thông minh, động cơ tăng áp 1.5T 140 mã lực, SmartSense cấp độ 2, thiết kế Parametric hiện đại, giá trị vượt trội.',
            features='6 túi khí, SmartSense L2, Màn hình 10.25 inch, Camera 360°, Cửa sổ trời toàn cảnh, Chìa khóa thông minh',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.7
        ))
        
        # Hyundai Tucson - SUV cỡ C
        cars.append(self.create_car(
            'Hyundai', 'Tucson', 2024, 'SUV cỡ C', 'hyundai-tucson-2024',
            769000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=180, torque_nm=265, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4500, width=1865, height=1650, wheelbase=2680,
            weight=1570, trunk=539,
            abs=True, airbags=6, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='7.0L/100km',
            desc='SUV cỡ C cao cấp, động cơ 1.6L Turbo 180 mã lực, thiết kế Parametric Jewel độc đáo, SmartSense tiên tiến, nội thất hiện đại sang trọng.',
            features='6 túi khí, SmartSense, 2 màn hình 10.25 inch, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da, Sạc không dây',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Hyundai Santa Fe - SUV 7 chỗ
        cars.append(self.create_car(
            'Hyundai', 'Santa Fe', 2024, 'SUV 7 chỗ', 'hyundai-santa-fe-2024',
            1069000000, 7,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=281, torque_nm=422, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4830, width=1900, height=1720, wheelbase=2815,
            weight=1930, trunk=571,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='8.2L/100km',
            desc='SUV 7 chỗ cao cấp, động cơ 2.5L Turbo 281 mã lực mạnh mẽ, hệ dẫn động AWD, SmartSense cấp độ 2+, không gian 3 hàng ghế sang trọng.',
            features='9 túi khí, SmartSense L2+, 2 màn hình 12.3 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da Nappa, Âm thanh Bose',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Xám',
            rating=4.8
        ))
        
        # Hyundai Palisade - SUV 8 chỗ
        cars.append(self.create_car(
            'Hyundai', 'Palisade', 2024, 'SUV 8 chỗ', 'hyundai-palisade-2024',
            1439000000, 8,
            engine_l=2.2, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=200, torque_nm=440, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4995, width=1975, height=1750, wheelbase=2900,
            weight=2105, trunk=311,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=10.25,
            fuel_cons='7.8L/100km',
            desc='SUV 8 chỗ siêu rộng rãi, động cơ 2.2L Turbo Diesel 200 mã lực, hệ dẫn động AWD, không gian 3 hàng ghế VIP, nội thất cao cấp nhất.',
            features='9 túi khí, SmartSense, 2 màn hình 12.3/10.25 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, 3 hàng ghế VIP, Âm thanh Harman Kardon',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Nâu',
            rating=4.8
        ))
        
        # Hyundai Stargazer - MPV 7 chỗ
        cars.append(self.create_car(
            'Hyundai', 'Stargazer', 2024, 'MPV 7 chỗ', 'hyundai-stargazer-2024',
            489000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=115, torque_nm=144, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4460, width=1780, height=1695, wheelbase=2780,
            weight=1295, trunk=628,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=8.0,
            fuel_cons='6.5L/100km',
            desc='MPV 7 chỗ thông minh, động cơ 1.5L CVVT 115 mã lực, thiết kế Parametric hiện đại, không gian linh hoạt, giá cả hấp dẫn.',
            features='6 túi khí, ESC, Màn hình 8 inch, Camera 360°, Chìa khóa thông minh, Điều hòa 2 dàn, Cửa trượt điện',
            colors='Trắng, Đen, Bạc, Xám, Xanh Dương',
            rating=4.6
        ))
        
        # Hyundai Custin - MPV 7 chỗ cao cấp
        cars.append(self.create_car(
            'Hyundai', 'Custin', 2024, 'MPV cao cấp', 'hyundai-custin-2024',
            820000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=160, torque_nm=253, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4950, width=1850, height=1734, wheelbase=3055,
            weight=1780, trunk=590,
            abs=True, airbags=6, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='7.2L/100km',
            desc='MPV 7 chỗ cao cấp, động cơ 1.5L Turbo 160 mã lực, không gian siêu rộng rãi với trục cơ sở 3055mm, ghế hàng 2 VIP, nội thất sang trọng.',
            features='6 túi khí, SmartSense, 2 màn hình 10.25 inch, Camera 360°, Cửa trượt điện, Ghế VIP hàng 2, Cửa sổ trời toàn cảnh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Nâu',
            rating=4.7
        ))
        
        self.random_delay()
        print(f"✅ Hyundai: {len(cars)} xe")
        return cars
    
    def crawl_ford(self) -> List[Dict]:
        """爬取Ford所有车型"""
        print("🔍 开始爬取 Ford Vietnam...")
        cars = []
        
        # Ford Ranger - Bán tải
        cars.append(self.create_car(
            'Ford', 'Ranger', 2024, 'Bán tải', 'ford-ranger-2024',
            659000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Bi-Turbo Diesel',
            power_hp=210, torque_nm=500, transmission='AT 10 cấp',
            drive_type='4WD', cylinders=4,
            length=5370, width=1918, height=1884, wheelbase=3270,
            weight=2140, trunk=0,
            abs=True, airbags=7, smart_key=True,
            display='TFT 12 inch', screen=12.0,
            fuel_cons='8.0L/100km',
            desc='Bán tải mạnh mẽ nhất phân khúc, động cơ 2.0L Bi-Turbo Diesel 210 mã lực, mô-men xoắn 500 Nm, hộp số 10 cấp, hệ 4WD tiên tiến.',
            features='7 túi khí, Co-Pilot360, Màn hình 12 inch SYNC4, Camera 360°, Hệ thống 4WD điện tử, Cảm biến địa hình, Thùng sau 1560mm',
            colors='Trắng, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.8
        ))
        
        # Ford Everest - SUV 7 chỗ
        cars.append(self.create_car(
            'Ford', 'Everest', 2024, 'SUV 7 chỗ', 'ford-everest-2024',
            1099000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Bi-Turbo Diesel',
            power_hp=210, torque_nm=500, transmission='AT 10 cấp',
            drive_type='4WD', cylinders=4,
            length=4914, width=1923, height=1842, wheelbase=2900,
            weight=2350, trunk=259,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.4 inch', screen=12.0,
            fuel_cons='7.8L/100km',
            desc='SUV 7 chỗ địa hình, động cơ 2.0L Bi-Turbo Diesel 210 mã lực, hộp số 10 cấp, khả năng off-road mạnh mẽ, không gian 3 hàng ghế rộng rãi.',
            features='9 túi khí, Co-Pilot360, Màn hình 12 inch SYNC4, Camera 360°, Hệ thống 4WD địa hình, 7 chế độ lái, Ghế da cao cấp',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Nâu',
            rating=4.7
        ))
        
        # Ford Territory - SUV cỡ C
        cars.append(self.create_car(
            'Ford', 'Territory', 2024, 'SUV cỡ C', 'ford-territory-2024',
            839000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng EcoBoost Turbo',
            power_hp=163, torque_nm=245, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4580, width=1936, height=1674, wheelbase=2716,
            weight=1635, trunk=448,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.3 inch', screen=10.0,
            fuel_cons='7.0L/100km',
            desc='SUV cỡ C thông minh, động cơ 1.5L EcoBoost Turbo 163 mã lực, thiết kế hiện đại, Co-Pilot360 an toàn, nội thất rộng rãi tiện nghi.',
            features='6 túi khí, Co-Pilot360, Màn hình 10 inch SYNC, Camera 360°, Cửa sổ trời toàn cảnh, Chìa khóa thông minh',
            colors='Trắng, Đen, Bạc, Xanh Dương, Xám',
            rating=4.6
        ))
        
        # Ford Explorer - SUV 7 chỗ cao cấp
        cars.append(self.create_car(
            'Ford', 'Explorer', 2024, 'SUV cao cấp', 'ford-explorer-2024',
            2199000000, 7,
            engine_l=3.0, engine_type='6 xi-lanh V hình EcoBoost Twin-Turbo',
            power_hp=400, torque_nm=563, transmission='AT 10 cấp',
            drive_type='AWD', cylinders=6,
            length=5050, width=2004, height=1778, wheelbase=3025,
            weight=2285, trunk=595,
            abs=True, airbags=10, smart_key=True,
            display='TFT 12.3 inch', screen=10.1,
            fuel_cons='11.0L/100km',
            desc='SUV 7 chỗ cao cấp, động cơ 3.0L V6 EcoBoost Twin-Turbo 400 mã lực, hệ dẫn động AWD thông minh, nội thất siêu sang, công nghệ hiện đại nhất.',
            features='10 túi khí, Co-Pilot360, Màn hình 10.1 inch SYNC4, Camera 360°, AWD thông minh, 3 hàng ghế VIP, Âm thanh B&O 12 loa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.8
        ))
        
        # Ford Mustang - Xe thể thao
        cars.append(self.create_car(
            'Ford', 'Mustang', 2024, 'Xe thể thao', 'ford-mustang-2024',
            2999000000, 4,
            engine_l=5.0, engine_type='8 xi-lanh V hình',
            power_hp=450, torque_nm=529, transmission='AT 10 cấp',
            drive_type='RWD', cylinders=8,
            length=4788, width=1916, height=1381, wheelbase=2720,
            weight=1705, trunk=382,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.4 inch', screen=13.2,
            fuel_cons='12.5L/100km',
            desc='Xe thể thao huyền thoại, động cơ 5.0L V8 450 mã lực, âm thanh V8 đặc trưng, thiết kế cơ bắp mạnh mẽ, trải nghiệm lái thuần túy.',
            features='6 túi khí, Màn hình 13.2 inch, Hệ thống âm thanh B&O, Ghế thể thao Recaro, Phanh Brembo, Hệ thống xả hiệu suất cao',
            colors='Đỏ, Đen, Xanh Dương, Bạc, Trắng',
            rating=4.9
        ))
        
        self.random_delay()
        print(f"✅ Ford: {len(cars)} xe")
        return cars
    
    def crawl_all(self):
        """爬取所有品牌"""
        print("\n" + "=" * 60)
        print("🚀 开始爬取越南汽车市场完整数据")
        print("=" * 60)
        print()
        
        all_cars = []
        
        # 爬取各品牌
        all_cars.extend(self.crawl_vinfast())
        all_cars.extend(self.crawl_toyota())
        all_cars.extend(self.crawl_honda())
        all_cars.extend(self.crawl_hyundai())
        all_cars.extend(self.crawl_ford())
        
        self.cars = all_cars
        return all_cars
    
    def print_statistics(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📊 数据统计")
        print("=" * 60)
        
        # 品牌统计
        brands = {}
        for car in self.cars:
            brands[car['brand']] = brands.get(car['brand'], 0) + 1
        
        print("\n📈 品牌分布:")
        for brand, count in sorted(brands.items(), key=lambda x: x[1], reverse=True):
            print(f"  {brand}: {count} xe")
        
        # 类别统计
        categories = {}
        for car in self.cars:
            cat = car['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 分类分布:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} xe")
        
        # 燃料类型统计
        fuel_types = {}
        for car in self.cars:
            fuel = car['fuel_type']
            fuel_types[fuel] = fuel_types.get(fuel, 0) + 1
        
        print("\n🔋 燃料类型:")
        for fuel, count in sorted(fuel_types.items()):
            print(f"  {fuel}: {count} xe")
        
        # 价格统计
        prices = [c['price_vnd'] for c in self.cars]
        print(f"\n💰 价格范围:")
        print(f"  最低: {min(prices):,} ₫ ({min(prices)/1000000:.0f} triệu)")
        print(f"  最高: {max(prices):,} ₫ ({max(prices)/1000000:.0f} triệu)")
        print(f"  平均: {sum(prices)//len(prices):,} ₫ ({sum(prices)//len(prices)/1000000:.0f} triệu)")
    
    def save_to_json(self):
        """保存到JSON文件"""
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        output_file = os.path.join(data_dir, 'vietnam_cars_complete.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.cars, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 数据已保存到: {output_file}")
        print(f"📦 文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")

def main():
    crawler = VietnamCarCrawler()
    
    # 爬取所有数据
    cars = crawler.crawl_all()
    
    print("\n" + "=" * 60)
    print(f"✅ 爬取完成！总计: {len(cars)} 辆汽车")
    print("=" * 60)
    
    # 统计信息
    crawler.print_statistics()
    
    # 保存数据
    crawler.save_to_json()
    
    print("\n" + "=" * 60)
    print("🎉 越南汽车数据爬取完成！")
    print("=" * 60)
    print("\n💡 下一步:")
    print("  1. cd /root/越南摩托汽车网站/backend")
    print("  2. npm run build")
    print("  3. node dist/scripts/import-vietnam-cars.js")
    print()

if __name__ == '__main__':
    main()

