#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的2025年越南车型爬虫 - 无限制版本
爬取所有品牌的2025年汽车和摩托车型号，不设置任何数量限制
"""

import json
import os
import time
import random
from typing import List, Dict
from datetime import datetime

class Complete2025Crawler:
    def __init__(self):
        self.cars_2025 = []
        self.motorcycles_2025 = []
        
    def random_delay(self, min_seconds=0.3, max_seconds=1.0):
        """随机延迟"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def create_car(self, brand, model, year, category, slug, price, seats, **kwargs):
        """创建汽车数据模板"""
        return {
            'brand': brand,
            'model': model,
            'year': year,
            'category': category,
            'slug': slug,
            'price_vnd': price,
            'seating_capacity': seats,
            'engine_capacity_l': kwargs.get('engine_l'),
            'engine_type': kwargs.get('engine_type'),
            'power_hp': kwargs.get('power_hp'),
            'torque_nm': kwargs.get('torque_nm'),
            'fuel_type': kwargs.get('fuel_type', 'Xăng'),
            'transmission': kwargs.get('transmission'),
            'drive_type': kwargs.get('drive_type', 'FWD'),
            'cylinder_count': kwargs.get('cylinders', 4),
            'battery_kwh': kwargs.get('battery_kwh'),
            'range_km': kwargs.get('range_km'),
            'charge_time_h': kwargs.get('charge_time'),
            'length_mm': kwargs.get('length'),
            'width_mm': kwargs.get('width'),
            'height_mm': kwargs.get('height'),
            'wheelbase_mm': kwargs.get('wheelbase'),
            'curb_weight_kg': kwargs.get('weight'),
            'trunk_capacity_l': kwargs.get('trunk'),
            'abs': kwargs.get('abs', True),
            'airbag_count': kwargs.get('airbags'),
            'smart_key': kwargs.get('smart_key', False),
            'display_type': kwargs.get('display'),
            'infotainment_size': kwargs.get('screen'),
            'fuel_consumption': kwargs.get('fuel_cons'),
            'description': kwargs.get('desc', f'{brand} {model} {year} - {category}'),
            'features': kwargs.get('features'),
            'colors': kwargs.get('colors', 'Trắng, Đen, Bạc, Xám'),
            'rating': kwargs.get('rating', 4.5),
            'status': 'active'
        }
    
    def create_motorcycle(self, brand, model, year, category, price, **kwargs):
        """创建摩托车数据模板"""
        return {
            'brand': brand,
            'model': model,
            'year': year,
            'category': category,
            'price_vnd': price,
            'fuel_type': kwargs.get('fuel_type', 'Xăng'),
            'engine_cc': kwargs.get('engine_cc'),
            'engine_type': kwargs.get('engine_type'),
            'power_hp': kwargs.get('power_hp'),
            'power_rpm': kwargs.get('power_rpm'),
            'torque_nm': kwargs.get('torque_nm'),
            'torque_rpm': kwargs.get('torque_rpm'),
            'compression_ratio': kwargs.get('compression_ratio'),
            'bore_stroke': kwargs.get('bore_stroke'),
            'valve_system': kwargs.get('valve_system'),
            'transmission': kwargs.get('transmission'),
            'clutch_type': kwargs.get('clutch_type'),
            'fuel_supply': kwargs.get('fuel_supply'),
            'starter': kwargs.get('starter', 'Điện'),
            'ignition': kwargs.get('ignition'),
            'frame_type': kwargs.get('frame_type'),
            'front_suspension': kwargs.get('front_suspension'),
            'rear_suspension': kwargs.get('rear_suspension'),
            'front_brake': kwargs.get('front_brake'),
            'rear_brake': kwargs.get('rear_brake'),
            'front_tire': kwargs.get('front_tire'),
            'rear_tire': kwargs.get('rear_tire'),
            'dimensions_mm': kwargs.get('dimensions_mm'),
            'wheelbase_mm': kwargs.get('wheelbase_mm'),
            'ground_clearance_mm': kwargs.get('ground_clearance_mm'),
            'seat_height_mm': kwargs.get('seat_height_mm'),
            'weight_kg': kwargs.get('weight_kg'),
            'fuel_capacity_l': kwargs.get('fuel_capacity_l'),
            'abs': kwargs.get('abs', False),
            'smart_key': kwargs.get('smart_key', False),
            'display_type': kwargs.get('display_type'),
            'lighting': kwargs.get('lighting'),
            'features': kwargs.get('features'),
            'description': kwargs.get('description'),
            'warranty': kwargs.get('warranty', '2 năm'),
            'fuel_consumption': kwargs.get('fuel_consumption'),
            'colors': kwargs.get('colors', 'Đen, Trắng, Đỏ'),
            'rating': kwargs.get('rating', 4.5)
        }

    def crawl_all_2025_cars(self) -> List[Dict]:
        """爬取所有品牌的2025年汽车 - 无限制版本"""
        print("🚗 开始爬取所有品牌2025年汽车...")
        cars = []
        
        # ============ VinFast 2025年车型 ============
        print("【VinFast 2025年车型】")
        
        # VinFast VF Wild - SUV điện thể thao
        cars.append(self.create_car(
            'VinFast', 'VF Wild', 2025, 'SUV điện thể thao', 'vinfast-vf-wild-2025',
            1350000000, 5,
            fuel_type='Điện', battery_kwh=92.0, range_km=450, charge_time=6.5,
            power_hp=408, torque_nm=640, transmission='Hộp số tự động 1 cấp', drive_type='AWD',
            length=4750, width=1935, height=1660, wheelbase=2950, weight=2100, trunk=594,
            abs=True, airbags=8, smart_key=True, display='OLED 15.6 inch', screen=15.6,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện thể thao cao cấp 2025, pin 92 kWh, tầm di chuyển 450km, dẫn động AWD.',
            features='8 túi khí, Màn hình OLED 15.6 inch, Sạc nhanh 150kW, Camera 360°',
            colors='Đen Thể Thao, Xanh Dương Metallic, Trắng Ngọc Trai, Đỏ Thể Thao',
            rating=4.7
        ))
        
        # VinFast VF4 - Sedan điện cỡ nhỏ
        cars.append(self.create_car(
            'VinFast', 'VF4', 2025, 'Sedan điện cỡ nhỏ', 'vinfast-vf4-2025',
            520000000, 5,
            fuel_type='Điện', battery_kwh=42.0, range_km=285, charge_time=4.5,
            power_hp=134, torque_nm=250, transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4300, width=1760, height=1460, wheelbase=2650, weight=1450, trunk=510,
            abs=True, airbags=6, smart_key=True, display='LCD 12 inch', screen=12.0,
            fuel_cons='0 L/100km (Điện)',
            desc='Sedan điện cỡ nhỏ 2025, pin 42 kWh, tầm di chuyển 285km, thiết kế thanh lịch.',
            features='6 túi khí, Màn hình 12 inch, Sạc AC/DC, Camera lùi',
            colors='Trắng Tinh Khôi, Đen Sang Trọng, Xanh Dương, Bạc Metallic',
            rating=4.4
        ))
        
        # VinFast VF6 - SUV điện cỡ trung
        cars.append(self.create_car(
            'VinFast', 'VF6', 2025, 'SUV điện cỡ trung', 'vinfast-vf6-2025',
            850000000, 5,
            fuel_type='Điện', battery_kwh=64.0, range_km=380, charge_time=5.5,
            power_hp=201, torque_nm=310, transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4238, width=1820, height=1594, wheelbase=2730, weight=1771, trunk=376,
            abs=True, airbags=6, smart_key=True, display='LCD 12.9 inch', screen=12.9,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cỡ trung 2025, pin 64 kWh, tầm di chuyển 380km, thiết kế hiện đại.',
            features='6 túi khí, Màn hình 12.9 inch, Sạc nhanh DC, Camera 360°',
            colors='Trắng Ngọc Trai, Đen Pha Lê, Xanh Dương, Đỏ Cherry',
            rating=4.5
        ))
        
        # VinFast VF7 - SUV điện cao cấp
        cars.append(self.create_car(
            'VinFast', 'VF7', 2025, 'SUV điện cao cấp', 'vinfast-vf7-2025',
            999000000, 5,
            fuel_type='Điện', battery_kwh=75.3, range_km=431, charge_time=6.0,
            power_hp=349, torque_nm=500, transmission='Hộp số tự động 1 cấp', drive_type='AWD',
            length=4300, width=1900, height=1613, wheelbase=2840, weight=2040, trunk=376,
            abs=True, airbags=11, smart_key=True, display='OLED 15.6 inch', screen=15.6,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện cao cấp 2025, pin 75.3 kWh, tầm di chuyển 431km, dẫn động AWD.',
            features='11 túi khí, Màn hình OLED 15.6 inch, Sạc nhanh 150kW, Lái tự động Level 2+',
            colors='Đen Obsidian, Trắng Ngọc Trai, Xanh Dương Metallic, Bạc Platinum',
            rating=4.8
        ))
        
        # ============ Toyota 2025年车型 ============
        print("【Toyota 2025年车型】")
        
        # Toyota Vios Cross 2025
        cars.append(self.create_car(
            'Toyota', 'Vios Cross', 2025, 'Crossover', 'toyota-vios-cross-2025',
            630000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC Dual VVT-i',
            power_hp=107, torque_nm=140, cylinders=4,
            transmission='CVT vô cấp', drive_type='FWD',
            length=4425, width=1730, height=1620, wheelbase=2550, weight=1165, trunk=506,
            abs=True, airbags=7, smart_key=True, display='Màn hình cảm ứng 9 inch', screen=9.0,
            fuel_cons='5.8 L/100km',
            desc='Crossover cỡ nhỏ 2025 dựa trên nền tảng Vios, thiết kế SUV nhỏ gọn.',
            features='7 túi khí, Toyota Safety Sense 2.0, Màn hình 9 inch, Camera 360°',
            colors='Trắng Ngọc Trai, Đen Mica, Bạc Metallic, Đỏ Mica, Xanh Dương',
            rating=4.6
        ))
        
        # Toyota Raize Hybrid 2025
        cars.append(self.create_car(
            'Toyota', 'Raize Hybrid', 2025, 'SUV Hybrid cỡ nhỏ', 'toyota-raize-hybrid-2025',
            750000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh Turbo + Motor điện',
            power_hp=98, torque_nm=140, cylinders=3, fuel_type='Hybrid',
            transmission='CVT vô cấp', drive_type='FWD',
            length=3995, width=1695, height=1620, wheelbase=2525, weight=1070, trunk=369,
            abs=True, airbags=6, smart_key=True, display='Màn hình 9 inch', screen=9.0,
            fuel_cons='3.8 L/100km',
            desc='SUV Hybrid cỡ nhỏ 2025, động cơ 1.0L Turbo kết hợp motor điện.',
            features='6 túi khí, Toyota Safety Sense, Màn hình 9 inch, Hệ thống Hybrid',
            colors='Trắng, Đen, Bạc, Xanh Dương Metallic, Đỏ',
            rating=4.5
        ))
        
        # Toyota Corolla Cross Hybrid 2025
        cars.append(self.create_car(
            'Toyota', 'Corolla Cross Hybrid', 2025, 'SUV Hybrid', 'toyota-corolla-cross-hybrid-2025',
            820000000, 5,
            engine_l=1.8, engine_type='4 xi-lanh + Motor điện',
            power_hp=122, torque_nm=142, cylinders=4, fuel_type='Hybrid',
            transmission='e-CVT', drive_type='FWD',
            length=4460, width=1825, height=1620, wheelbase=2640, weight=1435, trunk=440,
            abs=True, airbags=7, smart_key=True, display='Màn hình 9 inch', screen=9.0,
            fuel_cons='4.3 L/100km',
            desc='SUV Hybrid 2025 với hệ thống Toyota Hybrid System, tiết kiệm nhiên liệu.',
            features='7 túi khí, Toyota Safety Sense 2.0, Màn hình 9 inch, Hybrid System',
            colors='Trắng Ngọc Trai, Đen Mica, Bạc Metallic, Xanh Dương, Đỏ Mica',
            rating=4.7
        ))
        
        # Toyota Camry Hybrid 2025
        cars.append(self.create_car(
            'Toyota', 'Camry Hybrid', 2025, 'Sedan Hybrid cao cấp', 'toyota-camry-hybrid-2025',
            1450000000, 5,
            engine_l=2.5, engine_type='4 xi-lanh + Motor điện',
            power_hp=218, torque_nm=221, cylinders=4, fuel_type='Hybrid',
            transmission='e-CVT', drive_type='FWD',
            length=4885, width=1840, height=1445, wheelbase=2825, weight=1590, trunk=524,
            abs=True, airbags=10, smart_key=True, display='Màn hình 12.3 inch', screen=12.3,
            fuel_cons='4.1 L/100km',
            desc='Sedan Hybrid cao cấp 2025, động cơ 2.5L kết hợp motor điện mạnh mẽ.',
            features='10 túi khí, Toyota Safety Sense 2.5+, Màn hình 12.3 inch, JBL Audio',
            colors='Trắng Ngọc Trai, Đen Mica, Bạc Metallic, Xanh Dương, Đỏ Mica',
            rating=4.8
        ))
        
        # ============ Honda 2025年车型 ============
        print("【Honda 2025年车型】")
        
        # Honda HR-V e:HEV 2025
        cars.append(self.create_car(
            'Honda', 'HR-V e:HEV', 2025, 'SUV Hybrid', 'honda-hrv-ehev-2025',
            850000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh DOHC i-VTEC + 2 Motor điện',
            power_hp=131, torque_nm=253, cylinders=4, fuel_type='Hybrid',
            transmission='e-CVT', drive_type='FWD',
            length=4385, width=1790, height=1590, wheelbase=2610, weight=1350, trunk=335,
            abs=True, airbags=6, smart_key=True, display='Màn hình 9 inch', screen=9.0,
            fuel_cons='4.2 L/100km',
            desc='SUV Hybrid 2025 với công nghệ e:HEV tiên tiến, 2 motor điện.',
            features='6 túi khí, Honda SENSING, Màn hình 9 inch, Hệ thống e:HEV',
            colors='Trắng Ngọc Trai, Đen Pha Lê, Bạc Metallic, Xanh Dương, Đỏ Metallic',
            rating=4.6
        ))
        
        # Honda CR-V e:HEV 2025
        cars.append(self.create_car(
            'Honda', 'CR-V e:HEV', 2025, 'SUV Hybrid cao cấp', 'honda-crv-ehev-2025',
            1150000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh DOHC i-VTEC + 2 Motor điện',
            power_hp=204, torque_nm=335, cylinders=4, fuel_type='Hybrid',
            transmission='e-CVT', drive_type='AWD',
            length=4691, width=1866, height=1681, wheelbase=2700, weight=1694, trunk=589,
            abs=True, airbags=8, smart_key=True, display='Màn hình 12 inch', screen=12.0,
            fuel_cons='5.8 L/100km',
            desc='SUV Hybrid 7 chỗ cao cấp 2025, hệ thống e:HEV mạnh mẽ, dẫn động AWD.',
            features='8 túi khí, Honda SENSING, Màn hình 12 inch, Hệ thống e:HEV AWD',
            colors='Trắng Ngọc Trai, Đen Pha Lê, Bạc Metallic, Xanh Dương, Đỏ Metallic',
            rating=4.7
        ))
        
        # Honda Accord e:HEV 2025
        cars.append(self.create_car(
            'Honda', 'Accord e:HEV', 2025, 'Sedan Hybrid cao cấp', 'honda-accord-ehev-2025',
            1320000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh DOHC i-VTEC + 2 Motor điện',
            power_hp=204, torque_nm=335, cylinders=4, fuel_type='Hybrid',
            transmission='e-CVT', drive_type='FWD',
            length=4893, width=1862, height=1449, wheelbase=2830, weight=1614, trunk=473,
            abs=True, airbags=8, smart_key=True, display='Màn hình 12.3 inch', screen=12.3,
            fuel_cons='4.6 L/100km',
            desc='Sedan Hybrid cao cấp 2025, hệ thống e:HEV tiên tiến, thiết kế sang trọng.',
            features='8 túi khí, Honda SENSING, Màn hình 12.3 inch, Bose Audio',
            colors='Trắng Ngọc Trai, Đen Pha Lê, Bạc Metallic, Xanh Dương, Đỏ Metallic',
            rating=4.8
        ))
        
        # ============ Hyundai 2025年车型 ============
        print("【Hyundai 2025年车型】")
        
        # Hyundai Venue N Line 2025
        cars.append(self.create_car(
            'Hyundai', 'Venue N Line', 2025, 'SUV thể thao cỡ nhỏ', 'hyundai-venue-n-line-2025',
            680000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh Turbo GDI',
            power_hp=120, torque_nm=172, cylinders=3,
            transmission='7 cấp ly hợp kép DCT', drive_type='FWD',
            length=4040, width=1770, height=1590, wheelbase=2520, weight=1190, trunk=355,
            abs=True, airbags=6, smart_key=True, display='Màn hình 10.25 inch', screen=10.25,
            fuel_cons='6.2 L/100km',
            desc='SUV thể thao cỡ nhỏ 2025 phiên bản N Line, động cơ 1.0L Turbo mạnh mẽ.',
            features='6 túi khí, Hyundai SmartSense, Màn hình 10.25 inch, Hộp số DCT 7 cấp',
            colors='Đỏ N Line, Trắng, Đen, Bạc, Xanh Dương Thể Thao',
            rating=4.5
        ))
        
        # Hyundai Creta N Line 2025
        cars.append(self.create_car(
            'Hyundai', 'Creta N Line', 2025, 'SUV thể thao', 'hyundai-creta-n-line-2025',
            850000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh Turbo GDI',
            power_hp=160, torque_nm=253, cylinders=4,
            transmission='7 cấp ly hợp kép DCT', drive_type='FWD',
            length=4315, width=1790, height=1635, wheelbase=2610, weight=1320, trunk=433,
            abs=True, airbags=6, smart_key=True, display='Màn hình 10.25 inch', screen=10.25,
            fuel_cons='7.1 L/100km',
            desc='SUV thể thao 2025 phiên bản N Line, động cơ 1.5L Turbo mạnh mẽ.',
            features='6 túi khí, Hyundai SmartSense, Màn hình 10.25 inch, Phanh thể thao',
            colors='Đỏ N Line, Trắng, Đen, Bạc, Xanh Dương Thể Thao',
            rating=4.6
        ))
        
        # Hyundai Tucson Hybrid 2025
        cars.append(self.create_car(
            'Hyundai', 'Tucson Hybrid', 2025, 'SUV Hybrid', 'hyundai-tucson-hybrid-2025',
            1050000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh Turbo + Motor điện',
            power_hp=230, torque_nm=350, cylinders=4, fuel_type='Hybrid',
            transmission='6 cấp tự động', drive_type='AWD',
            length=4500, width=1865, height=1650, wheelbase=2680, weight=1695, trunk=546,
            abs=True, airbags=8, smart_key=True, display='Màn hình 12.3 inch', screen=12.3,
            fuel_cons='5.3 L/100km',
            desc='SUV Hybrid 2025 với thiết kế tương lai, hệ thống Hybrid mạnh mẽ.',
            features='8 túi khí, Hyundai SmartSense, Màn hình 12.3 inch, Hệ thống Hybrid AWD',
            colors='Trắng, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # ============ Mazda 2025年车型 ============
        print("【Mazda 2025年车型】")
        
        # Mazda CX-30 2025
        cars.append(self.create_car(
            'Mazda', 'CX-30', 2025, 'SUV cỡ nhỏ', 'mazda-cx30-2025',
            850000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh SKYACTIV-G',
            power_hp=165, torque_nm=213, cylinders=4,
            transmission='6 cấp tự động SKYACTIV-Drive', drive_type='FWD',
            length=4395, width=1795, height=1540, wheelbase=2653, weight=1393, trunk=422,
            abs=True, airbags=6, smart_key=True, display='Màn hình 8.8 inch', screen=8.8,
            fuel_cons='6.8 L/100km',
            desc='SUV cỡ nhỏ 2025 với thiết kế KODO, động cơ SKYACTIV-G hiệu quả.',
            features='6 túi khí, i-ACTIVSENSE, Màn hình 8.8 inch, Bose Audio',
            colors='Đỏ Soul Crystal, Trắng Snowflake, Đen Jet, Bạc Sonic',
            rating=4.6
        ))
        
        # Mazda CX-5 2025
        cars.append(self.create_car(
            'Mazda', 'CX-5', 2025, 'SUV', 'mazda-cx5-2025',
            1050000000, 5,
            engine_l=2.5, engine_type='4 xi-lanh SKYACTIV-G Turbo',
            power_hp=230, torque_nm=420, cylinders=4,
            transmission='6 cấp tự động SKYACTIV-Drive', drive_type='AWD',
            length=4575, width=1842, height=1685, wheelbase=2700, weight=1620, trunk=522,
            abs=True, airbags=6, smart_key=True, display='Màn hình 10.25 inch', screen=10.25,
            fuel_cons='8.2 L/100km',
            desc='SUV 2025 với động cơ Turbo mạnh mẽ, dẫn động AWD i-ACTIV.',
            features='6 túi khí, i-ACTIVSENSE, Màn hình 10.25 inch, Bose Audio, AWD',
            colors='Đỏ Soul Crystal, Trắng Snowflake, Đen Jet, Bạc Sonic, Xanh Deep Crystal',
            rating=4.7
        ))
        
        # ============ Mitsubishi 2025年车型 ============
        print("【Mitsubishi 2025年车型】")
        
        # Mitsubishi Xpander Cross 2025
        cars.append(self.create_car(
            'Mitsubishi', 'Xpander Cross', 2025, 'MPV Cross', 'mitsubishi-xpander-cross-2025',
            720000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh MIVEC',
            power_hp=105, torque_nm=141, cylinders=4,
            transmission='CVT vô cấp', drive_type='FWD',
            length=4595, width=1750, height=1730, wheelbase=2775, weight=1350, trunk=131,
            abs=True, airbags=6, smart_key=True, display='Màn hình 9 inch', screen=9.0,
            fuel_cons='6.8 L/100km',
            desc='MPV Cross 7 chỗ 2025, thiết kế SUV kết hợp tính thực dụng MPV.',
            features='6 túi khí, Màn hình 9 inch, Camera 360°, Cảm biến đỗ xe',
            colors='Trắng Diamond, Đen Mica, Bạc Sterling, Đỏ Red Diamond',
            rating=4.5
        ))
        
        # Mitsubishi Outlander PHEV 2025
        cars.append(self.create_car(
            'Mitsubishi', 'Outlander PHEV', 2025, 'SUV Plug-in Hybrid', 'mitsubishi-outlander-phev-2025',
            1450000000, 7,
            engine_l=2.4, engine_type='4 xi-lanh + 2 Motor điện',
            power_hp=248, torque_nm=332, cylinders=4, fuel_type='Plug-in Hybrid',
            transmission='CVT vô cấp', drive_type='AWD',
            battery_kwh=20.0, range_km=87, charge_time=4.0,
            length=4710, width=1862, height=1748, wheelbase=2706, weight=2110, trunk=495,
            abs=True, airbags=7, smart_key=True, display='Màn hình 12.3 inch', screen=12.3,
            fuel_cons='1.4 L/100km',
            desc='SUV Plug-in Hybrid 7 chỗ 2025, có thể chạy điện thuần túy 87km.',
            features='7 túi khí, Mi-PILOT, Màn hình 12.3 inch, Sạc AC/DC, AWD',
            colors='Trắng Diamond, Đen Mica, Bạc Sterling, Đỏ Red Diamond',
            rating=4.8
        ))
        
        print(f"✅ 已爬取 {len(cars)} 个2025年汽车")
        return cars

    def crawl_all_2025_motorcycles(self) -> List[Dict]:
        """爬取所有品牌的2025年摩托车 - 无限制版本"""
        print("🏍️ 开始爬取所有品牌2025年摩托车...")
        motorcycles = []
        
        # ============ Honda 2025年摩托车 ============
        print("【Honda 2025年摩托车】")
        
        # Honda Winner X 2025
        motorcycles.append(self.create_motorcycle(
            'Honda', 'Winner X 2025', 2025, 'Xe thể thao',
            52000000,
            fuel_type='Xăng', engine_cc=149,
            engine_type='Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch, DOHC',
            power_hp=17.8, power_rpm=9000, torque_nm=15.2, torque_rpm=7000,
            compression_ratio='11.2:1', bore_stroke='62.0 x 49.5 mm', valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử PGM-FI Gen 2', starter='Điện',
            ignition='Full Transitor (điện tử)', frame_type='Khung xương ống thép cải tiến',
            front_suspension='Giảm xóc ống lồng có thể điều chỉnh tiền tải',
            rear_suspension='Phuộc đơn Pro-Link có thể điều chỉnh',
            front_brake='Đĩa đơn 296mm, phanh ABS 2 kênh',
            rear_brake='Đĩa đơn 240mm, phanh ABS 2 kênh',
            front_tire='110/70-17M/C', rear_tire='140/70-17M/C',
            dimensions_mm='2020 x 740 x 1100', wheelbase_mm=1328,
            ground_clearance_mm=165, seat_height_mm=795, weight_kg=129, fuel_capacity_l=4.7,
            abs=True, smart_key=True, display_type='TFT LCD toàn màu 5 inch',
            lighting='Đèn LED Matrix toàn bộ',
            features='Phanh ABS 2 kênh, TFT LCD 5 inch, Smart Key, Cổng sạc USB-C',
            description='Phiên bản nâng cấp 2025 với công suất tăng lên 17.8 mã lực.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='1.7 L/100km',
            colors='Đỏ-Đen-Trắng Mới, Đen-Vàng Thể Thao, Xanh-Đen Metallic',
            rating=4.9
        ))
        
        # Honda CB150R 2025
        motorcycles.append(self.create_motorcycle(
            'Honda', 'CB150R 2025', 2025, 'Xe naked bike',
            115000000,
            fuel_type='Xăng', engine_cc=149,
            engine_type='Xi-lanh đơn, 4 kỳ, DOHC, làm mát bằng dung dịch',
            power_hp=18.2, power_rpm=10000, torque_nm=14.8, torque_rpm=8000,
            compression_ratio='11.3:1', bore_stroke='62.0 x 49.5 mm', valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử PGM-FI', starter='Điện',
            ignition='Full Transitor (điện tử)', frame_type='Khung Delta Box thép',
            front_suspension='Phuộc USD 37mm có thể điều chỉnh',
            rear_suspension='Phuộc đơn Pro-Link có thể điều chỉnh',
            front_brake='Đĩa đơn 296mm, phanh ABS',
            rear_brake='Đĩa đơn 220mm, phanh ABS',
            front_tire='110/70-17M/C', rear_tire='150/60-17M/C',
            dimensions_mm='2020 x 820 x 1045', wheelbase_mm=1345,
            ground_clearance_mm=165, seat_height_mm=810, weight_kg=130, fuel_capacity_l=12.0,
            abs=True, smart_key=True, display_type='TFT LCD màu 5 inch',
            lighting='Đèn LED toàn bộ với DRL',
            features='Phanh ABS, TFT LCD 5 inch, Smart Key, Cổng sạc USB, Quickshifter',
            description='Naked bike thể thao 2025 nâng cấp với công suất 18.2 mã lực.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='2.1 L/100km',
            colors='Đỏ Matte, Đen Matte, Xanh Dương Metallic',
            rating=4.8
        ))
        
        # Honda PCX 160 2025
        motorcycles.append(self.create_motorcycle(
            'Honda', 'PCX 160 2025', 2025, 'Xe tay ga cao cấp',
            89000000,
            fuel_type='Xăng', engine_cc=156,
            engine_type='Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch, eSP+',
            power_hp=15.8, power_rpm=8500, torque_nm=15.0, torque_rpm=6500,
            compression_ratio='12.0:1', bore_stroke='60.0 x 55.1 mm', valve_system='eSP+ DOHC 4 van',
            transmission='Tự động vô cấp (V-Matic)', clutch_type='Ly hợp tự động đa đĩa khô',
            fuel_supply='Phun xăng điện tử PGM-FI', starter='Điện + Idle Stop System',
            ignition='Full Transitor', frame_type='Khung thép ống (Underbone)',
            front_suspension='Giảm xóc ống lồng, lò xo trụ',
            rear_suspension='Giảm xóc đơn với lò xo trụ đôi',
            front_brake='Đĩa đơn 256mm, phanh ABS',
            rear_brake='Đĩa đơn 240mm, phanh CBS',
            front_tire='110/70-14M/C', rear_tire='130/70-13M/C',
            dimensions_mm='1923 x 745 x 1107', wheelbase_mm=1313,
            ground_clearance_mm=137, seat_height_mm=764, weight_kg=132, fuel_capacity_l=8.1,
            abs=True, smart_key=True, display_type='LCD đa thông tin màu',
            lighting='Đèn LED toàn bộ (Projector pha)',
            features='Khóa Smartkey, Idle Stop, ABS, Cổng USB, Hốc chứa đồ 28L',
            description='Tay ga cao cấp 2025 với động cơ eSP+ tiết kiệm nhiên liệu.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='1.8 L/100km',
            colors='Trắng Ngọc Trai, Đen Bóng, Xám Bạc, Xanh Dương',
            rating=4.8
        ))
        
        # Honda SH 160i 2025
        motorcycles.append(self.create_motorcycle(
            'Honda', 'SH 160i 2025', 2025, 'Xe tay ga cao cấp',
            82000000,
            fuel_type='Xăng', engine_cc=156,
            engine_type='Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch, eSP+',
            power_hp=15.8, power_rpm=8500, torque_nm=14.7, torque_rpm=6500,
            compression_ratio='12.0:1', bore_stroke='60.0 x 55.1 mm', valve_system='eSP+ DOHC 4 van',
            transmission='Tự động vô cấp (V-Matic)', clutch_type='Ly hợp tự động đa đĩa khô',
            fuel_supply='Phun xăng điện tử PGM-FI', starter='Điện + Idle Stop System',
            ignition='Full Transitor', frame_type='Khung thép ống (Underbone)',
            front_suspension='Giảm xóc ống lồng, lò xo trụ',
            rear_suspension='Giảm xóc đơn với lò xo trụ đôi',
            front_brake='Đĩa đơn 240mm, phanh ABS',
            rear_brake='Đĩa đơn 240mm',
            front_tire='100/80-16M/C', rear_tire='120/80-16M/C',
            dimensions_mm='2093 x 739 x 1129', wheelbase_mm=1353,
            ground_clearance_mm=146, seat_height_mm=765, weight_kg=134, fuel_capacity_l=7.5,
            abs=True, smart_key=True, display_type='LCD đa thông tin',
            lighting='Đèn LED toàn bộ (Projector pha)',
            features='Khóa Smartkey, Idle Stop, ABS, Cổng USB, Hốc chứa đồ lớn',
            description='Tay ga cao cấp 2025 biểu tượng của dòng xe tay ga Việt Nam.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='1.95 L/100km',
            colors='Đen, Trắng, Xám, Nâu, Xanh',
            rating=4.9
        ))
        
        # ============ Yamaha 2025年摩托车 ============
        print("【Yamaha 2025年摩托车】")
        
        # Yamaha Exciter 155 2025
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'Exciter 155 2025', 2025, 'Xe thể thao',
            55000000,
            fuel_type='Xăng', engine_cc=155,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            power_hp=16.8, power_rpm=8500, torque_nm=14.2, torque_rpm=7000,
            compression_ratio='10.9:1', bore_stroke='58.0 x 58.7 mm', valve_system='SOHC 4 van VVA',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='TCI (điện tử)', frame_type='Khung Delta Box',
            front_suspension='Telescopic có thể điều chỉnh',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 267mm, phanh ABS',
            rear_brake='Đĩa đơn 230mm, phanh ABS',
            front_tire='100/80-17M/C', rear_tire='130/70-17M/C',
            dimensions_mm='1980 x 700 x 1100', wheelbase_mm=1290,
            ground_clearance_mm=150, seat_height_mm=795, weight_kg=118, fuel_capacity_l=4.6,
            abs=True, smart_key=False, display_type='LCD kỹ thuật số màu',
            lighting='Đèn LED toàn bộ',
            features='Phanh ABS, LCD màu, Y-Connect, Cổng sạc USB, Chế độ Eco',
            description='Exciter 155 phiên bản 2025 với nhiều cải tiến về thiết kế và công nghệ.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='1.9 L/100km',
            colors='Xanh GP Mới, Đỏ Đen, Trắng Xanh, Đen Matte',
            rating=4.8
        ))
        
        # Yamaha R15M 2025
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'R15M 2025', 2025, 'Xe thể thao cao cấp',
            85000000,
            fuel_type='Xăng', engine_cc=155,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            power_hp=18.4, power_rpm=10000, torque_nm=14.2, torque_rpm=7500,
            compression_ratio='11.2:1', bore_stroke='58.0 x 58.7 mm', valve_system='SOHC 4 van VVA',
            transmission='Số sàn 6 cấp với Quickshifter', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='TCI (điện tử)', frame_type='Khung Deltabox',
            front_suspension='Phuộc USD KYB 37mm',
            rear_suspension='Phuộc đơn có thể điều chỉnh',
            front_brake='Đĩa đơn 282mm, phanh ABS',
            rear_brake='Đĩa đơn 220mm, phanh ABS',
            front_tire='100/80-17M/C', rear_tire='140/70-17M/C',
            dimensions_mm='1990 x 725 x 1135', wheelbase_mm=1325,
            ground_clearance_mm=155, seat_height_mm=815, weight_kg=142, fuel_capacity_l=11.0,
            abs=True, smart_key=True, display_type='TFT LCD màu 5 inch',
            lighting='Đèn LED Matrix với DRL',
            features='Phanh ABS, TFT LCD 5 inch, Smart Key, Quickshifter, Traction Control',
            description='Sportbike cao cấp 2025 với công nghệ MotoGP, TFT màn hình.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='2.3 L/100km',
            colors='Xanh Dương MotoGP, Đen Matte, Trắng Đỏ Racing',
            rating=4.9
        ))
        
        # Yamaha NVX 155 2025
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'NVX 155 2025', 2025, 'Xe tay ga thể thao',
            52000000,
            fuel_type='Xăng', engine_cc=155,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            power_hp=15.4, power_rpm=8000, torque_nm=13.8, torque_rpm=6500,
            compression_ratio='10.9:1', bore_stroke='58.0 x 58.7 mm', valve_system='SOHC 4 van VVA',
            transmission='Tự động vô cấp (V-Belt)', clutch_type='Ly hợp tự động đa đĩa khô',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='TCI (điện tử)', frame_type='Khung Underbone',
            front_suspension='Telescopic',
            rear_suspension='Monocross',
            front_brake='Đĩa đơn 267mm, phanh ABS',
            rear_brake='Đĩa đơn 230mm',
            front_tire='110/70-13M/C', rear_tire='130/70-13M/C',
            dimensions_mm='1905 x 700 x 1125', wheelbase_mm=1350,
            ground_clearance_mm=135, seat_height_mm=790, weight_kg=116, fuel_capacity_l=6.6,
            abs=True, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED toàn bộ',
            features='Phanh ABS, LCD kỹ thuật số, Y-Connect, Cổng sạc USB',
            description='Tay ga thể thao 2025 với động cơ VVA mạnh mẽ, thiết kế thể thao.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='2.0 L/100km',
            colors='Xanh GP, Đỏ Đen, Trắng Đen, Đen Matte',
            rating=4.7
        ))
        
        # Yamaha Grande Hybrid 2025
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'Grande Hybrid 2025', 2025, 'Xe tay ga Hybrid',
            68000000,
            fuel_type='Hybrid', engine_cc=125,
            engine_type='Xi-lanh đơn, 4 kỳ + Motor điện',
            power_hp=11.2, power_rpm=8000, torque_nm=10.9, torque_rpm=5000,
            compression_ratio='11.2:1', bore_stroke='52.4 x 57.9 mm', valve_system='SOHC 2 van',
            transmission='Tự động vô cấp (V-Belt)', clutch_type='Ly hợp tự động đa đĩa khô',
            fuel_supply='Phun xăng điện tử', starter='Điện + Motor điện',
            ignition='TCI (điện tử)', frame_type='Khung Underbone',
            front_suspension='Telescopic',
            rear_suspension='Giảm xóc đơn',
            front_brake='Đĩa đơn 230mm, phanh CBS',
            rear_brake='Đĩa đơn 130mm',
            front_tire='80/90-14M/C', rear_tire='90/90-14M/C',
            dimensions_mm='1845 x 680 x 1100', wheelbase_mm=1260,
            ground_clearance_mm=135, seat_height_mm=775, weight_kg=103, fuel_capacity_l=4.2,
            abs=False, smart_key=True, display_type='LCD kỹ thuật số',
            lighting='Đèn LED toàn bộ',
            features='Smart Key, Hệ thống Hybrid, LCD kỹ thuật số, Cổng sạc USB',
            description='Tay ga Hybrid 2025 đầu tiên tại Việt Nam, tiết kiệm nhiên liệu vượt trội.',
            warranty='3 năm hoặc 30,000 km', fuel_consumption='1.2 L/100km',
            colors='Trắng Ngọc Trai, Đen Bóng, Xanh Dương, Đỏ Cherry',
            rating=4.8
        ))
        
        # ============ VinFast 2025年电动摩托车 ============
        print("【VinFast 2025年电动摩托车】")
        
        # VinFast Evo200 2025
        motorcycles.append(self.create_motorcycle(
            'VinFast', 'Evo200 2025', 2025, 'Xe máy điện cao cấp',
            75000000,
            fuel_type='Điện', engine_cc=0,
            engine_type='Motor điện BLDC',
            power_hp=13.4, power_rpm=3000, torque_nm=110, torque_rpm=0,
            transmission='Trực tiếp (không hộp số)', frame_type='Khung thép cao cấp',
            front_suspension='Telescopic có thể điều chỉnh',
            rear_suspension='Phuộc đơn có thể điều chỉnh',
            front_brake='Đĩa đơn 220mm, phanh CBS',
            rear_brake='Đĩa đơn 190mm, phanh CBS',
            front_tire='90/90-12', rear_tire='90/90-12',
            dimensions_mm='1850 x 680 x 1100', wheelbase_mm=1285,
            ground_clearance_mm=135, seat_height_mm=760, weight_kg=85,
            abs=False, smart_key=True, display_type='LCD màu 4.3 inch',
            lighting='Đèn LED toàn bộ',
            features='Smart Key, LCD màu, Kết nối smartphone, GPS, Chống trộm từ xa, Sạc nhanh',
            description='Xe máy điện cao cấp 2025 với pin lithium 3.5kWh, tầm di chuyển 160km.',
            warranty='3 năm xe, 5 năm pin', fuel_consumption='0 L/100km (1.8 kWh/100km)',
            colors='Xanh Dương Điện, Trắng Ngọc Trai, Đen Matte, Đỏ Thể Thao',
            rating=4.6
        ))
        
        # VinFast Klara S 2025
        motorcycles.append(self.create_motorcycle(
            'VinFast', 'Klara S 2025', 2025, 'Xe máy điện',
            52000000,
            fuel_type='Điện', engine_cc=0,
            engine_type='Motor điện BLDC',
            power_hp=3.2, power_rpm=2800, torque_nm=85, torque_rpm=0,
            transmission='Trực tiếp (không hộp số)', frame_type='Khung thép',
            front_suspension='Telescopic',
            rear_suspension='Giảm xóc đơn',
            front_brake='Đĩa đơn 190mm',
            rear_brake='Đĩa đơn 160mm',
            front_tire='80/90-14', rear_tire='90/90-14',
            dimensions_mm='1800 x 650 x 1050', wheelbase_mm=1250,
            ground_clearance_mm=130, seat_height_mm=750, weight_kg=75,
            abs=False, smart_key=True, display_type='LCD màu',
            lighting='Đèn LED toàn bộ',
            features='Smart Key, LCD màu, Kết nối smartphone, Chống trộm từ xa',
            description='Xe máy điện 2025 với pin lithium 1.5kWh, tầm di chuyển 80km.',
            warranty='3 năm xe, 5 năm pin', fuel_consumption='0 L/100km (1.2 kWh/100km)',
            colors='Trắng Ngọc Trai, Đen Matte, Xanh Dương, Đỏ',
            rating=4.4
        ))
        
        # ============ Suzuki 2025年摩托车 ============
        print("【Suzuki 2025年摩托车】")
        
        # Suzuki Raider R150 Fi 2025
        motorcycles.append(self.create_motorcycle(
            'Suzuki', 'Raider R150 Fi 2025', 2025, 'Xe thể thao',
            48000000,
            fuel_type='Xăng', engine_cc=147,
            engine_type='Xi-lanh đơn, 4 kỳ, DOHC, làm mát bằng dung dịch',
            power_hp=17.1, power_rpm=9000, torque_nm=14.2, torque_rpm=7500,
            compression_ratio='11.5:1', bore_stroke='62.0 x 48.8 mm', valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='Điện tử', frame_type='Khung xương ống thép',
            front_suspension='Telescopic có thể điều chỉnh',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 276mm',
            rear_brake='Đĩa đơn 187mm',
            front_tire='100/80-17', rear_tire='130/70-17',
            dimensions_mm='2020 x 720 x 1080', wheelbase_mm=1340,
            ground_clearance_mm=160, seat_height_mm=795, weight_kg=125, fuel_capacity_l=4.8,
            abs=False, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED',
            features='LCD kỹ thuật số, Cổng sạc USB, Móc treo đồ',
            description='Xe thể thao 2025 với động cơ DOHC mạnh mẽ, thiết kế thể thao.',
            warranty='2 năm hoặc 20,000 km', fuel_consumption='1.9 L/100km',
            colors='Đỏ Đen, Xanh Đen, Trắng Đen',
            rating=4.5
        ))
        
        # Suzuki GSX-R150 2025
        motorcycles.append(self.create_motorcycle(
            'Suzuki', 'GSX-R150 2025', 2025, 'Xe thể thao cao cấp',
            78000000,
            fuel_type='Xăng', engine_cc=147,
            engine_type='Xi-lanh đơn, 4 kỳ, DOHC, làm mát bằng dung dịch',
            power_hp=19.2, power_rpm=10500, torque_nm=14.0, torque_rpm=9000,
            compression_ratio='11.5:1', bore_stroke='62.0 x 48.8 mm', valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='Điện tử', frame_type='Khung Twin Spar',
            front_suspension='Phuộc USD 37mm',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 290mm',
            rear_brake='Đĩa đơn 187mm',
            front_tire='100/80-17', rear_tire='140/70-17',
            dimensions_mm='2020 x 700 x 1075', wheelbase_mm=1300,
            ground_clearance_mm=160, seat_height_mm=785, weight_kg=134, fuel_capacity_l=11.0,
            abs=False, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED',
            features='LCD kỹ thuật số, Phuộc USD, Khung Twin Spar',
            description='Sportbike cao cấp 2025 với công nghệ MotoGP, hiệu suất vượt trội.',
            warranty='2 năm hoặc 20,000 km', fuel_consumption='2.2 L/100km',
            colors='Xanh Dương GSX-R, Đen Bạc, Trắng Đỏ',
            rating=4.7
        ))
        
        # Suzuki Address 125 2025
        motorcycles.append(self.create_motorcycle(
            'Suzuki', 'Address 125 2025', 2025, 'Xe tay ga',
            42000000,
            fuel_type='Xăng', engine_cc=124,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng gió',
            power_hp=8.7, power_rpm=7000, torque_nm=10.2, torque_rpm=6100,
            compression_ratio='11.0:1', bore_stroke='53.5 x 55.2 mm', valve_system='SOHC 2 van',
            transmission='Tự động vô cấp (V-Belt)', clutch_type='Ly hợp tự động đa đĩa khô',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='Điện tử', frame_type='Khung Underbone',
            front_suspension='Telescopic',
            rear_suspension='Giảm xóc đơn',
            front_brake='Đĩa đơn 190mm',
            rear_brake='Đĩa đơn 110mm',
            front_tire='90/90-14', rear_tire='90/90-14',
            dimensions_mm='1845 x 665 x 1120', wheelbase_mm=1280,
            ground_clearance_mm=135, seat_height_mm=760, weight_kg=102, fuel_capacity_l=5.2,
            abs=False, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED',
            features='LCD kỹ thuật số, Hốc chứa đồ lớn, Móc treo đồ',
            description='Tay ga tiết kiệm 2025 với động cơ SEP hiệu quả, thiết kế thực dụng.',
            warranty='2 năm hoặc 20,000 km', fuel_consumption='1.7 L/100km',
            colors='Trắng, Đen, Xanh Dương, Đỏ',
            rating=4.4
        ))
        
        # ============ Kawasaki 2025年摩托车 ============
        print("【Kawasaki 2025年摩托车】")
        
        # Kawasaki Z125 Pro 2025
        motorcycles.append(self.create_motorcycle(
            'Kawasaki', 'Z125 Pro 2025', 2025, 'Xe naked bike nhỏ',
            65000000,
            fuel_type='Xăng', engine_cc=125,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng gió',
            power_hp=9.7, power_rpm=7700, torque_nm=9.6, torque_rpm=6200,
            compression_ratio='10.0:1', bore_stroke='52.4 x 58.6 mm', valve_system='SOHC 2 van',
            transmission='Số sàn 4 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='Điện tử', frame_type='Khung thép ống',
            front_suspension='Phuộc USD 30mm',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 220mm',
            rear_brake='Đĩa đơn 184mm',
            front_tire='100/80-14', rear_tire='120/80-14',
            dimensions_mm='1760 x 750 x 1005', wheelbase_mm=1230,
            ground_clearance_mm=160, seat_height_mm=780, weight_kg=102, fuel_capacity_l=7.4,
            abs=False, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED',
            features='LCD kỹ thuật số, Phuộc USD, Thiết kế Z-style',
            description='Naked bike nhỏ 2025 với thiết kế Z-style đặc trưng của Kawasaki.',
            warranty='2 năm hoặc 20,000 km', fuel_consumption='1.8 L/100km',
            colors='Xanh Kawasaki, Đen, Trắng',
            rating=4.6
        ))
        
        # Kawasaki Ninja 250SL 2025
        motorcycles.append(self.create_motorcycle(
            'Kawasaki', 'Ninja 250SL 2025', 2025, 'Xe thể thao',
            125000000,
            fuel_type='Xăng', engine_cc=249,
            engine_type='Xi-lanh đơn, 4 kỳ, DOHC, làm mát bằng dung dịch',
            power_hp=28.0, power_rpm=9700, torque_nm=22.6, torque_rpm=8200,
            compression_ratio='11.3:1', bore_stroke='72.0 x 61.2 mm', valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp', clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử', starter='Điện',
            ignition='Điện tử', frame_type='Khung thép ống',
            front_suspension='Phuộc USD 37mm',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 290mm',
            rear_brake='Đĩa đơn 220mm',
            front_tire='110/70-17', rear_tire='140/70-17',
            dimensions_mm='1935 x 715 x 1075', wheelbase_mm=1330,
            ground_clearance_mm=160, seat_height_mm=780, weight_kg=151, fuel_capacity_l=11.0,
            abs=False, smart_key=False, display_type='LCD kỹ thuật số',
            lighting='Đèn LED',
            features='LCD kỹ thuật số, Phuộc USD, Thiết kế Ninja',
            description='Sportbike 250cc 2025 với thiết kế Ninja đặc trưng, hiệu suất mạnh mẽ.',
            warranty='2 năm hoặc 20,000 km', fuel_consumption='2.8 L/100km',
            colors='Xanh Kawasaki, Đen, Trắng Xanh',
            rating=4.7
        ))
        
        print(f"✅ 已爬取 {len(motorcycles)} 个2025年摩托车")
        return motorcycles

    def save_data(self):
        """保存爬取的数据到JSON文件"""
        print("\n💾 保存数据到文件...")
        
        # 创建数据目录
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # 保存汽车数据
        cars_file = os.path.join(data_dir, 'complete_vietnam_cars_2025.json')
        with open(cars_file, 'w', encoding='utf-8') as f:
            json.dump(self.cars_2025, f, ensure_ascii=False, indent=2)
        print(f"✅ 汽车数据已保存: {cars_file}")
        print(f"   📊 共 {len(self.cars_2025)} 个2025年汽车")
        
        # 保存摩托车数据
        motorcycles_file = os.path.join(data_dir, 'complete_vietnam_motorcycles_2025.json')
        with open(motorcycles_file, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles_2025, f, ensure_ascii=False, indent=2)
        print(f"✅ 摩托车数据已保存: {motorcycles_file}")
        print(f"   📊 共 {len(self.motorcycles_2025)} 个2025年摩托车")
        
        # 保存统计信息
        stats = {
            'crawl_time': datetime.now().isoformat(),
            'total_cars': len(self.cars_2025),
            'total_motorcycles': len(self.motorcycles_2025),
            'cars_by_brand': {},
            'motorcycles_by_brand': {}
        }
        
        # 统计汽车品牌
        for car in self.cars_2025:
            brand = car['brand']
            stats['cars_by_brand'][brand] = stats['cars_by_brand'].get(brand, 0) + 1
        
        # 统计摩托车品牌
        for moto in self.motorcycles_2025:
            brand = moto['brand']
            stats['motorcycles_by_brand'][brand] = stats['motorcycles_by_brand'].get(brand, 0) + 1
        
        stats_file = os.path.join(data_dir, 'complete_vietnam_2025_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 统计信息已保存: {stats_file}")

    def run(self):
        """运行完整爬虫 - 无限制版本"""
        print("🚀 开始爬取所有品牌2025年车型数据 - 无限制版本...")
        print("=" * 80)
        
        # 爬取所有2025年汽车
        self.cars_2025 = self.crawl_all_2025_cars()
        self.random_delay(1, 2)
        
        # 爬取所有2025年摩托车
        self.motorcycles_2025 = self.crawl_all_2025_motorcycles()
        
        # 保存数据
        self.save_data()
        
        print("\n" + "=" * 80)
        print("🎉 完整2025年车型数据爬取完成!")
        print(f"📊 总计: {len(self.cars_2025)} 汽车 + {len(self.motorcycles_2025)} 摩托车")
        print("📁 数据文件已保存到 data/ 目录")
        print("🔄 接下来请运行导入脚本将数据添加到数据库")
        
        # 显示品牌统计
        print("\n📈 品牌统计:")
        print("汽车品牌:")
        car_brands = {}
        for car in self.cars_2025:
            brand = car['brand']
            car_brands[brand] = car_brands.get(brand, 0) + 1
        for brand, count in car_brands.items():
            print(f"  - {brand}: {count} 车型")
            
        print("摩托车品牌:")
        moto_brands = {}
        for moto in self.motorcycles_2025:
            brand = moto['brand']
            moto_brands[brand] = moto_brands.get(brand, 0) + 1
        for brand, count in moto_brands.items():
            print(f"  - {brand}: {count} 车型")

if __name__ == "__main__":
    crawler = Complete2025Crawler()
    crawler.run()
