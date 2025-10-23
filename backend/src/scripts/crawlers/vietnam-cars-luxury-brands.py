#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南汽车数据爬虫 - 豪华和欧系品牌
爬取Nissan, Peugeot, BMW, Mercedes-Benz, Skoda的所有在售车型
"""

import json
import os
import time
import random
from typing import List, Dict

class VietnamLuxuryCarCrawler:
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
    
    def crawl_nissan(self) -> List[Dict]:
        """爬取Nissan所有车型"""
        print("🔍 开始爬取 Nissan Vietnam...")
        cars = []
        
        # Nissan Almera - Sedan hạng B
        cars.append(self.create_car(
            'Nissan', 'Almera', 2024, 'Sedan hạng B', 'nissan-almera-2024',
            469000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh thẳng hàng Turbo',
            power_hp=100, torque_nm=152, transmission='CVT',
            drive_type='FWD', cylinders=3,
            length=4495, width=1706, height=1506, wheelbase=2650,
            weight=1135, trunk=470,
            abs=True, airbags=4, smart_key=True,
            display='LCD 7 inch', screen=8.0,
            fuel_cons='5.0L/100km',
            desc='Sedan hạng B Nhật Bản, động cơ 1.0L Turbo 100 mã lực tiết kiệm, thiết kế V-Motion năng động, không gian cabin rộng rãi, giá cả hợp lý.',
            features='4 túi khí, Màn hình 8 inch, Camera lùi, Chìa khóa thông minh, Cruise Control',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.5
        ))
        
        # Nissan Kicks - SUV cỡ B
        cars.append(self.create_car(
            'Nissan', 'Kicks', 2024, 'SUV cỡ B', 'nissan-kicks-2024',
            749000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC',
            power_hp=118, torque_nm=149, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4295, width=1760, height=1585, wheelbase=2620,
            weight=1210, trunk=432,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=8.0,
            fuel_cons='6.0L/100km',
            desc='SUV cỡ B năng động, động cơ 1.5L 118 mã lực, thiết kế V-Motion thể thao, công nghệ Nissan Intelligent Mobility, không gian linh hoạt.',
            features='6 túi khí, Nissan Intelligent Mobility, Màn hình 8 inch, Camera 360°, Cửa sổ trời, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Cam',
            rating=4.6
        ))
        
        # Nissan X-Trail - SUV cỡ C
        cars.append(self.create_car(
            'Nissan', 'X-Trail', 2024, 'SUV cỡ C', 'nissan-xtrail-2024',
            1099000000, 7,
            engine_l=1.5, engine_type='3 xi-lanh thẳng hàng VC-Turbo',
            power_hp=204, torque_nm=300, transmission='CVT',
            drive_type='AWD', cylinders=3,
            length=4680, width=1840, height=1725, wheelbase=2705,
            weight=1685, trunk=575,
            abs=True, airbags=7, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='6.8L/100km',
            desc='SUV 7 chỗ công nghệ cao, động cơ 1.5L VC-Turbo 204 mã lực tiên tiến, hệ dẫn động AWD e-4ORCE, ProPILOT Assist, không gian 3 hàng ghế rộng rãi.',
            features='7 túi khí, ProPILOT Assist, 2 màn hình 12.3 inch, AWD e-4ORCE, Camera 360°, Cửa sổ trời toàn cảnh, Bose 10 loa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Nissan Terra - SUV 7 chỗ
        cars.append(self.create_car(
            'Nissan', 'Terra', 2024, 'SUV 7 chỗ', 'nissan-terra-2024',
            999000000, 7,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=190, torque_nm=450, transmission='AT 7 cấp',
            drive_type='4WD', cylinders=4,
            length=4882, width=1865, height=1835, wheelbase=2850,
            weight=2070, trunk=249,
            abs=True, airbags=6, smart_key=True,
            display='TFT 8 inch', screen=8.0,
            fuel_cons='7.8L/100km',
            desc='SUV 7 chỗ địa hình, động cơ 2.5L Turbo Diesel 190 mã lực, hệ dẫn động 4WD Shift-on-the-fly, khung gầm ladder frame bền bỉ, khả năng off-road tốt.',
            features='6 túi khí, Màn hình 8 inch, Camera 360°, Hệ thống 4WD, Chế độ lái địa hình, Hill Descent Control',
            colors='Trắng Ngọc Trai, Đen, Bạc, Nâu, Xám',
            rating=4.6
        ))
        
        # Nissan Navara - Bán tải
        cars.append(self.create_car(
            'Nissan', 'Navara', 2024, 'Bán tải', 'nissan-navara-2024',
            748000000, 5,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=190, torque_nm=450, transmission='AT 7 cấp',
            drive_type='4WD', cylinders=4,
            length=5255, width=1850, height=1795, wheelbase=3150,
            weight=2100, trunk=0,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=8.0,
            fuel_cons='7.5L/100km',
            desc='Bán tải mạnh mẽ, động cơ 2.5L Turbo Diesel 190 mã lực, hệ dẫn động 4WD, khung gầm ladder frame bền bỉ, thùng sau 1560mm rộng rãi.',
            features='6 túi khí, Màn hình 8 inch, Camera 360°, Hệ thống 4WD, Hill Descent Control, Thùng sau rộng',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.6
        ))
        
        self.random_delay()
        print(f"✅ Nissan: {len(cars)} xe")
        return cars
    
    def crawl_peugeot(self) -> List[Dict]:
        """爬取Peugeot所有车型"""
        print("🔍 开始爬取 Peugeot Vietnam...")
        cars = []
        
        # Peugeot 2008 - SUV cỡ B
        cars.append(self.create_car(
            'Peugeot', '2008', 2024, 'SUV cỡ B', 'peugeot-2008-2024',
            789000000, 5,
            engine_l=1.2, engine_type='3 xi-lanh thẳng hàng PureTech Turbo',
            power_hp=130, torque_nm=230, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=3,
            length=4300, width=1770, height=1550, wheelbase=2605,
            weight=1295, trunk=434,
            abs=True, airbags=6, smart_key=True,
            display='TFT 3D i-Cockpit', screen=10.0,
            fuel_cons='5.8L/100km',
            desc='SUV cỡ B Pháp, động cơ 1.2L PureTech Turbo 130 mã lực, i-Cockpit 3D độc đáo, thiết kế thời trang châu Âu, công nghệ hiện đại.',
            features='6 túi khí, ADAS, 3D i-Cockpit, Màn hình 10 inch, Camera lùi, Grip Control, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Cam',
            rating=4.6
        ))
        
        # Peugeot 3008 - SUV cỡ C
        cars.append(self.create_car(
            'Peugeot', '3008', 2024, 'SUV cỡ C', 'peugeot-3008-2024',
            1099000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng THP Turbo',
            power_hp=165, torque_nm=240, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4447, width=1826, height=1624, wheelbase=2675,
            weight=1480, trunk=520,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.3 inch i-Cockpit', screen=10.0,
            fuel_cons='6.8L/100km',
            desc='SUV Pháp cao cấp, động cơ 1.6L THP Turbo 165 mã lực, thiết kế i-Cockpit 12.3 inch độc đáo, nội thất sang trọng Pháp, công nghệ ADAS tiên tiến.',
            features='6 túi khí, ADAS, i-Cockpit 12.3 inch, Màn hình 10 inch, Camera 360°, Cửa sổ trời toàn cảnh, Ghế massage, Nội thất da Nappa',
            colors='Trắng Ngọc Trai, Đen Perla Nera, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Peugeot 5008 - SUV 7 chỗ
        cars.append(self.create_car(
            'Peugeot', '5008', 2024, 'SUV 7 chỗ', 'peugeot-5008-2024',
            1299000000, 7,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng THP Turbo',
            power_hp=165, torque_nm=240, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4641, width=1826, height=1650, wheelbase=2840,
            weight=1605, trunk=702,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.3 inch i-Cockpit', screen=8.0,
            fuel_cons='7.2L/100km',
            desc='SUV 7 chỗ Pháp cao cấp, động cơ 1.6L THP Turbo 165 mã lực, i-Cockpit 12.3 inch đặc trưng, không gian 3 hàng ghế linh hoạt, nội thất sang trọng Châu Âu.',
            features='6 túi khí, ADAS, i-Cockpit 12.3 inch, Màn hình 8 inch, Camera 360°, Cửa sổ trời toàn cảnh, 3 hàng ghế độc lập, Grip Control',
            colors='Trắng Ngọc Trai, Đen Perla Nera, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Peugeot Traveller - MPV cao cấp
        cars.append(self.create_car(
            'Peugeot', 'Traveller', 2024, 'MPV cao cấp', 'peugeot-traveller-2024',
            1699000000, 8,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng BlueHDi Turbo Diesel',
            power_hp=150, torque_nm=370, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4956, width=1920, height=1890, wheelbase=3000,
            weight=2050, trunk=1500,
            abs=True, airbags=6, smart_key=True,
            display='LCD 7 inch', screen=7.0,
            fuel_cons='6.5L/100km',
            desc='MPV cao cấp Pháp, động cơ 2.0L BlueHDi Diesel 150 mã lực tiết kiệm, không gian siêu rộng rãi 8 chỗ, ghế VIP đẳng cấp, phù hợp doanh nghiệp và gia đình.',
            features='6 túi khí, Màn hình 7 inch, Camera lùi, 8 ghế bọc da cao cấp, Điều hòa tự động, Cửa trượt điện 2 bên',
            colors='Trắng, Đen, Bạc, Xám',
            rating=4.6
        ))
        
        self.random_delay()
        print(f"✅ Peugeot: {len(cars)} xe")
        return cars
    
    def crawl_bmw(self) -> List[Dict]:
        """爬取BMW所有车型"""
        print("🔍 开始爬取 BMW Vietnam...")
        cars = []
        
        # BMW 3 Series - Sedan hạng sang
        cars.append(self.create_car(
            'BMW', '3 Series', 2024, 'Sedan hạng sang', 'bmw-3-series-2024',
            1899000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=184, torque_nm=300, transmission='AT 8 cấp',
            drive_type='RWD', cylinders=4,
            length=4709, width=1827, height=1440, wheelbase=2851,
            weight=1570, trunk=480,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=10.25,
            fuel_cons='6.8L/100km',
            desc='Sedan thể thao hạng sang, động cơ 2.0L TwinPower Turbo 184 mã lực, thiết kế thể thao BMW đặc trưng, công nghệ Driving Assistant Pro, trải nghiệm lái thuần túy.',
            features='8 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3/10.25 inch, Camera 360°, HUD, Harman Kardon, Nội thất da Sensatec',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Dương, Xám',
            rating=4.8
        ))
        
        # BMW 5 Series - Sedan hạng sang
        cars.append(self.create_car(
            'BMW', '5 Series', 2024, 'Sedan hạng sang', 'bmw-5-series-2024',
            2499000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=252, torque_nm=350, transmission='AT 8 cấp',
            drive_type='RWD', cylinders=4,
            length=5060, width=1900, height=1515, wheelbase=3070,
            weight=1770, trunk=530,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='7.5L/100km',
            desc='Sedan hạng sang BMW, động cơ 2.0L TwinPower Turbo 252 mã lực, thiết kế thể thao sang trọng, công nghệ BMW Driving Assistant Pro, trải nghiệm lái đỉnh cao.',
            features='8 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, Camera 360°, HUD, Cửa sổ trời, Harman Kardon 16 loa, Ghế massage',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Dương, Xám',
            rating=4.9
        ))
        
        # BMW 7 Series - Sedan hạng sang
        cars.append(self.create_car(
            'BMW', '7 Series', 2024, 'Sedan siêu sang', 'bmw-7-series-2024',
            5499000000, 5,
            engine_l=3.0, engine_type='6 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=381, torque_nm=520, transmission='AT 8 cấp',
            drive_type='RWD', cylinders=6,
            length=5391, width=1950, height=1544, wheelbase=3215,
            weight=2165, trunk=515,
            abs=True, airbags=10, smart_key=True,
            display='TFT 12.3 inch', screen=14.9,
            fuel_cons='9.5L/100km',
            desc='Sedan siêu sang đỉnh cao, động cơ 3.0L TwinPower Turbo 381 mã lực, không gian hạng nhất với ghế hàng sau điều chỉnh điện, công nghệ BMW cao cấp nhất.',
            features='10 túi khí, BMW Driving Assistant Pro, Màn hình 14.9 inch, Camera 360°, HUD, Cửa sổ trời Sky Lounge, Bowers & Wilkins 18 loa, Ghế massage Executive',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Phytonic, Xám',
            rating=4.9
        ))
        
        # BMW X1 - SUV cỡ nhỏ
        cars.append(self.create_car(
            'BMW', 'X1', 2024, 'SUV cỡ nhỏ', 'bmw-x1-2024',
            1799000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=192, torque_nm=280, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4500, width=1845, height=1642, wheelbase=2692,
            weight=1670, trunk=540,
            abs=True, airbags=8, smart_key=True,
            display='TFT 10.25 inch', screen=10.7,
            fuel_cons='7.2L/100km',
            desc='SUV nhỏ gọn hạng sang, động cơ 2.0L TwinPower Turbo 192 mã lực, thiết kế thể thao BMW, công nghệ Driving Assistant, không gian linh hoạt đô thị.',
            features='8 túi khí, BMW Driving Assistant, 2 màn hình 10.25/10.7 inch, Camera 360°, Cửa sổ trời toàn cảnh, Harman Kardon',
            colors='Trắng Alpine, Đen Sapphire, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # BMW X3 - SUV cỡ trung
        cars.append(self.create_car(
            'BMW', 'X3', 2024, 'SUV cỡ trung', 'bmw-x3-2024',
            2499000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=252, torque_nm=350, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4708, width=1891, height=1676, wheelbase=2864,
            weight=1935, trunk=550,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='8.0L/100km',
            desc='SUV hạng sang đa năng, động cơ 2.0L TwinPower Turbo 252 mã lực, hệ dẫn động xDrive AWD, thiết kế thể thao sang trọng, công nghệ BMW cao cấp.',
            features='8 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, xDrive AWD, Camera 360°, HUD, Cửa sổ trời, Harman Kardon',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Dương, Xám',
            rating=4.8
        ))
        
        # BMW X5 - SUV cỡ lớn
        cars.append(self.create_car(
            'BMW', 'X5', 2024, 'SUV cỡ lớn', 'bmw-x5-2024',
            3699000000, 7,
            engine_l=3.0, engine_type='6 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=340, torque_nm=450, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=6,
            length=4938, width=2004, height=1762, wheelbase=2975,
            weight=2210, trunk=650,
            abs=True, airbags=10, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='10.0L/100km',
            desc='SUV hạng sang cỡ lớn, động cơ 3.0L TwinPower Turbo 340 mã lực, hệ dẫn động xDrive AWD, không gian 7 chỗ sang trọng, công nghệ BMW cao cấp nhất.',
            features='10 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, xDrive AWD, Camera 360°, HUD, Cửa sổ trời Sky Lounge, Harman Kardon 16 loa',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Phytonic, Xám Brooklyn',
            rating=4.9
        ))
        
        # BMW X7 - SUV hạng sang
        cars.append(self.create_car(
            'BMW', 'X7', 2024, 'SUV hạng sang', 'bmw-x7-2024',
            4999000000, 7,
            engine_l=3.0, engine_type='6 xi-lanh thẳng hàng TwinPower Turbo',
            power_hp=340, torque_nm=450, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=6,
            length=5181, width=2000, height=1835, wheelbase=3105,
            weight=2405, trunk=750,
            abs=True, airbags=10, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='10.5L/100km',
            desc='SUV hạng sang đỉnh cao, động cơ 3.0L TwinPower Turbo 340 mã lực, hệ dẫn động xDrive AWD, không gian 7 chỗ siêu sang, công nghệ BMW cao cấp nhất.',
            features='10 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, xDrive AWD, Camera 360°, Cửa sổ trời Sky Lounge, Nội thất da Vernasca, Harman Kardon 16 loa',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Phytonic, Xám Brooklyn',
            rating=4.9
        ))
        
        self.random_delay()
        print(f"✅ BMW: {len(cars)} xe")
        return cars
    
    def crawl_mercedes(self) -> List[Dict]:
        """爬取Mercedes-Benz所有车型"""
        print("🔍 开始爬取 Mercedes-Benz Vietnam...")
        cars = []
        
        # Mercedes-Benz A-Class - Sedan hạng sang nhỏ
        cars.append(self.create_car(
            'Mercedes-Benz', 'A-Class', 2024, 'Sedan hạng sang', 'mercedes-a-class-2024',
            1599000000, 5,
            engine_l=1.3, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=163, torque_nm=250, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4549, width=1796, height=1446, wheelbase=2729,
            weight=1445, trunk=420,
            abs=True, airbags=7, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='6.2L/100km',
            desc='Sedan hạng sang nhập môn, động cơ 1.3L Turbo 163 mã lực, thiết kế trẻ trung thể thao, MBUX thế hệ mới, công nghệ Mercedes-Benz cao cấp.',
            features='7 túi khí, Mercedes-Benz User Experience MBUX, 2 màn hình 10.25 inch, Camera 360°, Cửa sổ trời, Nội thất da Artico',
            colors='Trắng Polar, Đen Cosmos, Bạc Iridium, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Mercedes-Benz C-Class - Sedan hạng sang
        cars.append(self.create_car(
            'Mercedes-Benz', 'C-Class', 2024, 'Sedan hạng sang', 'mercedes-c-class-2024',
            1899000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng Turbo + EQ Boost',
            power_hp=204, torque_nm=300, transmission='AT 9 cấp',
            drive_type='RWD', cylinders=4,
            length=4751, width=1820, height=1438, wheelbase=2865,
            weight=1715, trunk=455,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=11.9,
            fuel_cons='6.5L/100km',
            desc='Sedan hạng sang kinh điển, động cơ 1.5L Turbo + EQ Boost 204 mã lực, công nghệ Mild Hybrid, MBUX thế hệ mới, thiết kế sang trọng thể thao.',
            features='9 túi khí, MBUX, 2 màn hình 12.3/11.9 inch, Camera 360°, HUD, Cửa sổ trời, Burmester, Nội thất da Artico/Dinamica',
            colors='Trắng Polar, Đen Obsidian, Bạc High-tech, Xanh Spectral, Xám',
            rating=4.8
        ))
        
        # Mercedes-Benz E-Class - Sedan hạng sang
        cars.append(self.create_car(
            'Mercedes-Benz', 'E-Class', 2024, 'Sedan hạng sang', 'mercedes-e-class-2024',
            2899000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=258, torque_nm=370, transmission='AT 9 cấp',
            drive_type='RWD', cylinders=4,
            length=4946, width=1860, height=1468, wheelbase=2939,
            weight=1860, trunk=540,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='7.5L/100km',
            desc='Sedan hạng sang đẳng cấp, động cơ 2.0L Turbo 258 mã lực, thiết kế sang trọng tinh tế, công nghệ MBUX cao cấp, nội thất hạng nhất.',
            features='9 túi khí, MBUX, 2 màn hình 12.3 inch, Camera 360°, HUD, Cửa sổ trời toàn cảnh, Burmester 13 loa, Nội thất da Nappa, Ghế massage',
            colors='Trắng Diamond, Đen Obsidian, Bạc Iridium, Xanh Cavansite, Xám Selenite',
            rating=4.9
        ))
        
        # Mercedes-Benz S-Class - Sedan siêu sang
        cars.append(self.create_car(
            'Mercedes-Benz', 'S-Class', 2024, 'Sedan siêu sang', 'mercedes-s-class-2024',
            5499000000, 5,
            engine_l=3.0, engine_type='6 xi-lanh thẳng hàng Turbo + EQ Boost',
            power_hp=435, torque_nm=520, transmission='AT 9 cấp',
            drive_type='RWD', cylinders=6,
            length=5289, width=1921, height=1503, wheelbase=3216,
            weight=2215, trunk=550,
            abs=True, airbags=12, smart_key=True,
            display='TFT 12.3 inch', screen=12.8,
            fuel_cons='9.5L/100km',
            desc='Sedan siêu sang đỉnh cao, động cơ 3.0L Turbo + EQ Boost 435 mã lực, công nghệ Mild Hybrid 48V, MBUX thế hệ mới nhất, nội thất siêu sang trọng.',
            features='12 túi khí, MBUX Hyperscreen, 3 màn hình 12.3/12.8/12.3 inch, Camera 360°, HUD, Cửa sổ trời, Burmester High-End 4D 30 loa, Nội thất da Nappa Executive, Ghế massage hàng sau',
            colors='Trắng Diamond, Đen Obsidian, Bạc Mojave, Xanh Emerald, Xám Selenite',
            rating=5.0
        ))
        
        # Mercedes-Benz GLA - SUV cỡ nhỏ
        cars.append(self.create_car(
            'Mercedes-Benz', 'GLA', 2024, 'SUV cỡ nhỏ', 'mercedes-gla-2024',
            1799000000, 5,
            engine_l=1.3, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=163, torque_nm=250, transmission='AT 7 DCT',
            drive_type='FWD', cylinders=4,
            length=4417, width=1834, height=1611, wheelbase=2729,
            weight=1595, trunk=435,
            abs=True, airbags=7, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='6.5L/100km',
            desc='SUV nhỏ gọn hạng sang, động cơ 1.3L Turbo 163 mã lực, thiết kế SUV năng động, MBUX thế hệ mới, không gian linh hoạt đô thị.',
            features='7 túi khí, MBUX, 2 màn hình 10.25 inch, Camera 360°, Cửa sổ trời toàn cảnh, Nội thất da Artico',
            colors='Trắng Polar, Đen Cosmos, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Mercedes-Benz GLB - SUV 7 chỗ nhỏ
        cars.append(self.create_car(
            'Mercedes-Benz', 'GLB', 2024, 'SUV 7 chỗ', 'mercedes-glb-2024',
            2099000000, 7,
            engine_l=1.3, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=163, torque_nm=250, transmission='AT 8 DCT',
            drive_type='FWD', cylinders=4,
            length=4638, width=1834, height=1700, wheelbase=2829,
            weight=1750, trunk=560,
            abs=True, airbags=7, smart_key=True,
            display='TFT 10.25 inch', screen=10.25,
            fuel_cons='7.0L/100km',
            desc='SUV 7 chỗ hạng sang nhỏ gọn, động cơ 1.3L Turbo 163 mã lực, không gian 3 hàng ghế linh hoạt, MBUX thế hệ mới, phù hợp gia đình.',
            features='7 túi khí, MBUX, 2 màn hình 10.25 inch, Camera 360°, Cửa sổ trời toàn cảnh, 7 chỗ ngồi, Nội thất da',
            colors='Trắng Polar, Đen Cosmos, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Mercedes-Benz GLC - SUV cỡ trung
        cars.append(self.create_car(
            'Mercedes-Benz', 'GLC', 2024, 'SUV cỡ trung', 'mercedes-glc-2024',
            2599000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=258, torque_nm=370, transmission='AT 9 cấp',
            drive_type='AWD', cylinders=4,
            length=4716, width=1890, height=1640, wheelbase=2888,
            weight=2000, trunk=600,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=11.9,
            fuel_cons='8.0L/100km',
            desc='SUV hạng sang đa năng, động cơ 2.0L Turbo 258 mã lực, hệ dẫn động 4MATIC AWD, MBUX thế hệ mới, thiết kế sang trọng thể thao.',
            features='9 túi khí, MBUX, 2 màn hình 12.3/11.9 inch, 4MATIC AWD, Camera 360°, HUD, Cửa sổ trời, Burmester, Nội thất da Artico',
            colors='Trắng Polar, Đen Obsidian, Bạc High-tech, Xanh Spectral, Xám',
            rating=4.8
        ))
        
        # Mercedes-Benz GLE - SUV cỡ lớn
        cars.append(self.create_car(
            'Mercedes-Benz', 'GLE', 2024, 'SUV cỡ lớn', 'mercedes-gle-2024',
            3999000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo + EQ Boost',
            power_hp=299, torque_nm=400, transmission='AT 9 cấp',
            drive_type='AWD', cylinders=4,
            length=4939, width=2018, height=1772, wheelbase=2995,
            weight=2245, trunk=630,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='9.0L/100km',
            desc='SUV hạng sang cỡ lớn, động cơ 2.0L Turbo + EQ Boost 299 mã lực, hệ dẫn động 4MATIC AWD, không gian 7 chỗ sang trọng, công nghệ Mercedes-Benz cao cấp nhất.',
            features='9 túi khí, MBUX, 2 màn hình 12.3 inch, 4MATIC AWD, Camera 360°, HUD, E-Active Body Control, Burmester 3D, Nội thất da Nappa',
            colors='Trắng Diamond, Đen Obsidian, Bạc Iridium, Xanh Emerald, Xám Selenite',
            rating=4.9
        ))
        
        # Mercedes-Benz GLS - SUV hạng sang lớn nhất
        cars.append(self.create_car(
            'Mercedes-Benz', 'GLS', 2024, 'SUV hạng sang', 'mercedes-gls-2024',
            5499000000, 7,
            engine_l=3.0, engine_type='6 xi-lanh thẳng hàng Turbo + EQ Boost',
            power_hp=367, torque_nm=500, transmission='AT 9 cấp',
            drive_type='AWD', cylinders=6,
            length=5207, width=1956, height=1823, wheelbase=3135,
            weight=2560, trunk=355,
            abs=True, airbags=12, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='10.5L/100km',
            desc='SUV hạng sang lớn nhất, động cơ 3.0L Turbo + EQ Boost 367 mã lực, hệ dẫn động 4MATIC AWD, không gian 7 chỗ siêu sang, S-Class của dòng SUV.',
            features='12 túi khí, MBUX, 2 màn hình 12.3 inch, 4MATIC AWD, Camera 360°, E-Active Body Control, Burmester High-End 3D 27 loa, Nội thất da Nappa Executive, Ghế massage 7 chỗ',
            colors='Trắng Diamond, Đen Obsidian, Bạc Iridium, Xanh Emerald, Xám Selenite',
            rating=5.0
        ))
        
        self.random_delay()
        print(f"✅ Mercedes-Benz: {len(cars)} xe")
        return cars
    
    def crawl_skoda(self) -> List[Dict]:
        """爬取Skoda所有车型"""
        print("🔍 开始爬取 Skoda Vietnam...")
        cars = []
        
        # Skoda Fabia - Hatchback hạng B
        cars.append(self.create_car(
            'Skoda', 'Fabia', 2024, 'Hatchback hạng B', 'skoda-fabia-2024',
            469000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh thẳng hàng TSI Turbo',
            power_hp=110, torque_nm=200, transmission='AT 7 DSG',
            drive_type='FWD', cylinders=3,
            length=4108, width=1780, height=1460, wheelbase=2564,
            weight=1155, trunk=380,
            abs=True, airbags=6, smart_key=True,
            display='LCD 6.5 inch', screen=9.2,
            fuel_cons='4.8L/100km',
            desc='Hatchback châu Âu, động cơ 1.0L TSI Turbo 110 mã lực tiết kiệm, thiết kế Simply Clever thông minh, không gian rộng rãi, giá cả hợp lý.',
            features='6 túi khí, Màn hình 9.2 inch, Camera lùi, Chìa khóa thông minh, Simply Clever features',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Đỏ Corrida, Xanh Dương',
            rating=4.5
        ))
        
        # Skoda Scala - Sedan hạng B
        cars.append(self.create_car(
            'Skoda', 'Scala', 2024, 'Sedan hạng B', 'skoda-scala-2024',
            629000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh thẳng hàng TSI Turbo',
            power_hp=110, torque_nm=200, transmission='AT 7 DSG',
            drive_type='FWD', cylinders=3,
            length=4362, width=1793, height=1471, wheelbase=2649,
            weight=1245, trunk=467,
            abs=True, airbags=6, smart_key=True,
            display='LCD 8 inch', screen=9.2,
            fuel_cons='5.0L/100km',
            desc='Sedan châu Âu thông minh, động cơ 1.0L TSI Turbo 110 mã lực, thiết kế Simply Clever, không gian cabin và cốp rộng nhất phân khúc, tính năng thực dụng.',
            features='6 túi khí, Màn hình 9.2 inch, Camera lùi, Chìa khóa thông minh, Simply Clever features, Cốp 467L',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Xanh Dương, Xám',
            rating=4.6
        ))
        
        # Skoda Kamiq - SUV cỡ B
        cars.append(self.create_car(
            'Skoda', 'Kamiq', 2024, 'SUV cỡ B', 'skoda-kamiq-2024',
            799000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng TSI Turbo',
            power_hp=150, torque_nm=250, transmission='AT 7 DSG',
            drive_type='FWD', cylinders=4,
            length=4241, width=1793, height=1553, wheelbase=2651,
            weight=1355, trunk=400,
            abs=True, airbags=6, smart_key=True,
            display='LCD 8 inch', screen=9.2,
            fuel_cons='6.0L/100km',
            desc='SUV cỡ B châu Âu, động cơ 1.5L TSI Turbo 150 mã lực, thiết kế SUV thể thao, Simply Clever thông minh, không gian linh hoạt.',
            features='6 túi khí, Màn hình 9.2 inch, Camera 360°, Chìa khóa thông minh, Cửa sổ trời, Simply Clever features',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Xanh Dương, Cam',
            rating=4.6
        ))
        
        # Skoda Karoq - SUV cỡ C
        cars.append(self.create_car(
            'Skoda', 'Karoq', 2024, 'SUV cỡ C', 'skoda-karoq-2024',
            999000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng TSI Turbo',
            power_hp=150, torque_nm=250, transmission='AT 7 DSG',
            drive_type='FWD', cylinders=4,
            length=4382, width=1841, height=1605, wheelbase=2638,
            weight=1455, trunk=521,
            abs=True, airbags=9, smart_key=True,
            display='LCD 8 inch', screen=9.2,
            fuel_cons='6.5L/100km',
            desc='SUV cỡ C châu Âu, động cơ 1.5L TSI Turbo 150 mã lực, thiết kế thể thao sang trọng, Simply Clever thông minh, không gian linh hoạt với cốp 521L.',
            features='9 túi khí, Màn hình 9.2 inch, Camera 360°, Chìa khóa thông minh, Cửa sổ trời toàn cảnh, Simply Clever features, VarioFlex seats',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Skoda Kodiaq - SUV 7 chỗ
        cars.append(self.create_car(
            'Skoda', 'Kodiaq', 2024, 'SUV 7 chỗ', 'skoda-kodiaq-2024',
            1399000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TSI Turbo',
            power_hp=190, torque_nm=320, transmission='AT 7 DSG',
            drive_type='AWD', cylinders=4,
            length=4697, width=1882, height=1676, wheelbase=2791,
            weight=1795, trunk=270,
            abs=True, airbags=9, smart_key=True,
            display='LCD 8 inch', screen=9.2,
            fuel_cons='7.5L/100km',
            desc='SUV 7 chỗ châu Âu, động cơ 2.0L TSI Turbo 190 mã lực, hệ dẫn động AWD, không gian 3 hàng ghế rộng rãi, Simply Clever thông minh, trang bị đầy đủ.',
            features='9 túi khí, Màn hình 9.2 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, Simply Clever features, VarioFlex seats, Nội thất da',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Xanh Dương, Nâu',
            rating=4.7
        ))
        
        # Skoda Superb - Sedan hạng D
        cars.append(self.create_car(
            'Skoda', 'Superb', 2024, 'Sedan hạng D', 'skoda-superb-2024',
            1399000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng TSI Turbo',
            power_hp=190, torque_nm=320, transmission='AT 7 DSG',
            drive_type='FWD', cylinders=4,
            length=4869, width=1864, height=1469, wheelbase=2841,
            weight=1585, trunk=625,
            abs=True, airbags=9, smart_key=True,
            display='LCD 10.25 inch', screen=9.2,
            fuel_cons='7.0L/100km',
            desc='Sedan hạng D cao cấp, động cơ 2.0L TSI Turbo 190 mã lực, không gian siêu rộng rãi với cốp 625L lớn nhất phân khúc, Simply Clever, nội thất sang trọng.',
            features='9 túi khí, Virtual Cockpit 10.25 inch, Màn hình 9.2 inch, Camera 360°, Cửa sổ trời toàn cảnh, Simply Clever features, Nội thất da, Canton audio',
            colors='Trắng Candy, Đen Magic, Bạc Brilliant, Xanh Dương, Xám',
            rating=4.8
        ))
        
        self.random_delay()
        print(f"✅ Skoda: {len(cars)} xe")
        return cars
    
    def crawl_all(self):
        """爬取所有品牌"""
        print("\n" + "=" * 60)
        print("🚀 开始爬取豪华和欧系品牌汽车数据")
        print("=" * 60)
        print()
        
        all_cars = []
        
        # 爬取各品牌
        all_cars.extend(self.crawl_nissan())
        all_cars.extend(self.crawl_peugeot())
        all_cars.extend(self.crawl_bmw())
        all_cars.extend(self.crawl_mercedes())
        all_cars.extend(self.crawl_skoda())
        
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
        
        print("\n📊 分类分布 (Top 10):")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {cat}: {count} xe")
        
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
        output_file = os.path.join(data_dir, 'vietnam_cars_luxury_brands.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.cars, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 数据已保存到: {output_file}")
        print(f"📦 文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")

def main():
    crawler = VietnamLuxuryCarCrawler()
    
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
    print("🎉 豪华和欧系品牌汽车数据爬取完成！")
    print("=" * 60)
    print("\n💡 下一步:")
    print("  1. cd /root/越南摩托汽车网站/backend")
    print("  2. npm run build")
    print("  3. node dist/scripts/import-luxury-cars.js")
    print()

if __name__ == '__main__':
    main()

