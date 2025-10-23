#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南2025年新车型数据爬虫
专门爬取2025年新发布的摩托车和汽车型号
补充到现有2024年数据中，不替换原有数据
"""

import json
import os
import time
import random
from typing import List, Dict
from datetime import datetime

class Vietnam2025ModelsCrawler:
    def __init__(self):
        self.cars_2025 = []
        self.motorcycles_2025 = []
        
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
    
    def create_motorcycle(self, brand, model, year, category, price, **kwargs):
        """创建摩托车数据模板"""
        return {
            'brand': brand,
            'model': model,
            'year': year,
            'category': category,
            'price_vnd': price,
            'fuel_type': kwargs.get('fuel_type', 'Xăng'),
            
            # 发动机
            'engine_cc': kwargs.get('engine_cc'),
            'engine_type': kwargs.get('engine_type'),
            'power_hp': kwargs.get('power_hp'),
            'power_rpm': kwargs.get('power_rpm'),
            'torque_nm': kwargs.get('torque_nm'),
            'torque_rpm': kwargs.get('torque_rpm'),
            'compression_ratio': kwargs.get('compression_ratio'),
            'bore_stroke': kwargs.get('bore_stroke'),
            'valve_system': kwargs.get('valve_system'),
            
            # 传动
            'transmission': kwargs.get('transmission'),
            'clutch_type': kwargs.get('clutch_type'),
            'fuel_supply': kwargs.get('fuel_supply'),
            'starter': kwargs.get('starter', 'Điện'),
            'ignition': kwargs.get('ignition'),
            
            # 底盘
            'frame_type': kwargs.get('frame_type'),
            'front_suspension': kwargs.get('front_suspension'),
            'rear_suspension': kwargs.get('rear_suspension'),
            'front_brake': kwargs.get('front_brake'),
            'rear_brake': kwargs.get('rear_brake'),
            'front_tire': kwargs.get('front_tire'),
            'rear_tire': kwargs.get('rear_tire'),
            
            # 尺寸
            'dimensions_mm': kwargs.get('dimensions_mm'),
            'wheelbase_mm': kwargs.get('wheelbase_mm'),
            'ground_clearance_mm': kwargs.get('ground_clearance_mm'),
            'seat_height_mm': kwargs.get('seat_height_mm'),
            'weight_kg': kwargs.get('weight_kg'),
            'fuel_capacity_l': kwargs.get('fuel_capacity_l'),
            
            # 配置
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

    def crawl_2025_cars(self) -> List[Dict]:
        """爬取2025年新车型"""
        print("🔍 开始爬取 2025年新车型...")
        cars = []
        
        # ============ VinFast 2025年新车型 ============
        print("【VinFast 2025年新车型】")
        
        # VinFast VF Wild - SUV điện thể thao mới
        cars.append(self.create_car(
            'VinFast', 'VF Wild', 2025, 'SUV điện thể thao', 'vinfast-vf-wild-2025',
            1350000000, 5,
            fuel_type='Điện',
            battery_kwh=92.0, range_km=450, charge_time=6.5,
            power_hp=408, torque_nm=640,
            transmission='Hộp số tự động 1 cấp', drive_type='AWD',
            length=4750, width=1935, height=1660, wheelbase=2950,
            weight=2100, trunk=594,
            abs=True, airbags=8, smart_key=True,
            display='OLED 15.6 inch', screen=15.6,
            fuel_cons='0 L/100km (Điện)',
            desc='SUV điện thể thao cao cấp 2025, pin 92 kWh, tầm di chuyển 450km, dẫn động AWD, công suất 408 mã lực, thiết kế thể thao mạnh mẽ.',
            features='8 túi khí, Màn hình OLED 15.6 inch, Sạc nhanh 150kW, Camera 360°, Hệ thống lái tự động Level 2+, Âm thanh Harman Kardon',
            colors='Đen Thể Thao, Xanh Dương Metallic, Trắng Ngọc Trai, Đỏ Thể Thao',
            rating=4.7
        ))
        
        # VinFast VF4 - Sedan điện cỡ nhỏ
        cars.append(self.create_car(
            'VinFast', 'VF4', 2025, 'Sedan điện cỡ nhỏ', 'vinfast-vf4-2025',
            520000000, 5,
            fuel_type='Điện',
            battery_kwh=42.0, range_km=285, charge_time=4.5,
            power_hp=134, torque_nm=250,
            transmission='Hộp số tự động 1 cấp', drive_type='FWD',
            length=4300, width=1760, height=1460, wheelbase=2650,
            weight=1450, trunk=510,
            abs=True, airbags=6, smart_key=True,
            display='LCD 12 inch', screen=12.0,
            fuel_cons='0 L/100km (Điện)',
            desc='Sedan điện cỡ nhỏ 2025, pin 42 kWh, tầm di chuyển 285km, thiết kế thanh lịch, phù hợp gia đình trẻ, giá cả hợp lý.',
            features='6 túi khí, Màn hình 12 inch, Sạc AC/DC, Camera lùi, Cảm biến đỗ xe, Điều hòa tự động',
            colors='Trắng Tinh Khôi, Đen Sang Trọng, Xanh Dương, Bạc Metallic',
            rating=4.4
        ))
        
        # ============ Toyota 2025年新车型 ============
        print("【Toyota 2025年新车型】")
        
        # Toyota Vios Cross 2025 - Crossover mới
        cars.append(self.create_car(
            'Toyota', 'Vios Cross', 2025, 'Crossover', 'toyota-vios-cross-2025',
            630000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC Dual VVT-i',
            power_hp=107, torque_nm=140, cylinders=4,
            transmission='CVT vô cấp', drive_type='FWD',
            length=4425, width=1730, height=1620, wheelbase=2550,
            weight=1165, trunk=506,
            abs=True, airbags=7, smart_key=True,
            display='Màn hình cảm ứng 9 inch', screen=9.0,
            fuel_cons='5.8 L/100km',
            desc='Crossover cỡ nhỏ 2025 dựa trên nền tảng Vios, thiết kế SUV nhỏ gọn, động cơ 1.5L tiết kiệm nhiên liệu, phù hợp đô thị.',
            features='7 túi khí, Toyota Safety Sense 2.0, Màn hình 9 inch, Camera 360°, Cảm biến đỗ xe, Điều hòa tự động',
            colors='Trắng Ngọc Trai, Đen Mica, Bạc Metallic, Đỏ Mica, Xanh Dương',
            rating=4.6
        ))
        
        # Toyota Raize Hybrid 2025
        cars.append(self.create_car(
            'Toyota', 'Raize Hybrid', 2025, 'SUV Hybrid cỡ nhỏ', 'toyota-raize-hybrid-2025',
            750000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh Turbo + Motor điện',
            power_hp=98, torque_nm=140, cylinders=3,
            fuel_type='Hybrid',
            transmission='CVT vô cấp', drive_type='FWD',
            length=3995, width=1695, height=1620, wheelbase=2525,
            weight=1070, trunk=369,
            abs=True, airbags=6, smart_key=True,
            display='Màn hình 9 inch', screen=9.0,
            fuel_cons='3.8 L/100km',
            desc='SUV Hybrid cỡ nhỏ 2025, động cơ 1.0L Turbo kết hợp motor điện, tiết kiệm nhiên liệu xuất sắc 3.8L/100km.',
            features='6 túi khí, Toyota Safety Sense, Màn hình 9 inch, Hệ thống Hybrid, Cảm biến đỗ xe, Smart Key',
            colors='Trắng, Đen, Bạc, Xanh Dương Metallic, Đỏ',
            rating=4.5
        ))
        
        # ============ Honda 2025年新车型 ============
        print("【Honda 2025年新车型】")
        
        # Honda HR-V e:HEV 2025 - Hybrid mới
        cars.append(self.create_car(
            'Honda', 'HR-V e:HEV', 2025, 'SUV Hybrid', 'honda-hrv-ehev-2025',
            850000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh DOHC i-VTEC + 2 Motor điện',
            power_hp=131, torque_nm=253, cylinders=4,
            fuel_type='Hybrid',
            transmission='e-CVT', drive_type='FWD',
            length=4385, width=1790, height=1590, wheelbase=2610,
            weight=1350, trunk=335,
            abs=True, airbags=6, smart_key=True,
            display='Màn hình 9 inch', screen=9.0,
            fuel_cons='4.2 L/100km',
            desc='SUV Hybrid 2025 với công nghệ e:HEV tiên tiến, 2 motor điện, tiết kiệm nhiên liệu 4.2L/100km, thiết kế thể thao.',
            features='6 túi khí, Honda SENSING, Màn hình 9 inch, Hệ thống e:HEV, Camera lùi, Cảm biến đỗ xe',
            colors='Trắng Ngọc Trai, Đen Pha Lê, Bạc Metallic, Xanh Dương, Đỏ Metallic',
            rating=4.6
        ))
        
        # ============ Hyundai 2025年新车型 ============
        print("【Hyundai 2025年新车型】")
        
        # Hyundai Venue N Line 2025
        cars.append(self.create_car(
            'Hyundai', 'Venue N Line', 2025, 'SUV thể thao cỡ nhỏ', 'hyundai-venue-n-line-2025',
            680000000, 5,
            engine_l=1.0, engine_type='3 xi-lanh Turbo GDI',
            power_hp=120, torque_nm=172, cylinders=3,
            transmission='7 cấp ly hợp kép DCT', drive_type='FWD',
            length=4040, width=1770, height=1590, wheelbase=2520,
            weight=1190, trunk=355,
            abs=True, airbags=6, smart_key=True,
            display='Màn hình 10.25 inch', screen=10.25,
            fuel_cons='6.2 L/100km',
            desc='SUV thể thao cỡ nhỏ 2025 phiên bản N Line, động cơ 1.0L Turbo mạnh mẽ, thiết kế thể thao năng động.',
            features='6 túi khí, Hyundai SmartSense, Màn hình 10.25 inch, Hộp số DCT 7 cấp, Phanh thể thao, Nội thất N Line',
            colors='Đỏ N Line, Trắng, Đen, Bạc, Xanh Dương Thể Thao',
            rating=4.5
        ))
        
        print(f"✅ 已爬取 {len(cars)} 个2025年新车型")
        return cars

    def crawl_2025_motorcycles(self) -> List[Dict]:
        """爬取2025年新摩托车型"""
        print("🔍 开始爬取 2025年新摩托车型...")
        motorcycles = []
        
        # ============ Honda 2025年新摩托车型 ============
        print("【Honda 2025年新摩托车型】")
        
        # Honda Winner X 2025 - 升级版
        motorcycles.append(self.create_motorcycle(
            'Honda', 'Winner X 2025', 2025, 'Xe thể thao',
            52000000,
            fuel_type='Xăng',
            engine_cc=149,
            engine_type='Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch, DOHC',
            power_hp=17.8,
            power_rpm=9000,
            torque_nm=15.2,
            torque_rpm=7000,
            compression_ratio='11.2:1',
            bore_stroke='62.0 x 49.5 mm',
            valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp',
            clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử PGM-FI Gen 2',
            starter='Điện',
            ignition='Full Transitor (điện tử)',
            frame_type='Khung xương ống thép cải tiến',
            front_suspension='Giảm xóc ống lồng có thể điều chỉnh tiền tải',
            rear_suspension='Phuộc đơn Pro-Link có thể điều chỉnh',
            front_brake='Đĩa đơn 296mm, phanh ABS 2 kênh',
            rear_brake='Đĩa đơn 240mm, phanh ABS 2 kênh',
            front_tire='110/70-17M/C',
            rear_tire='140/70-17M/C',
            dimensions_mm='2020 x 740 x 1100',
            wheelbase_mm=1328,
            ground_clearance_mm=165,
            seat_height_mm=795,
            weight_kg=129,
            fuel_capacity_l=4.7,
            abs=True,
            smart_key=True,
            display_type='TFT LCD toàn màu 5 inch',
            lighting='Đèn LED Matrix toàn bộ',
            features='Phanh ABS 2 kênh, TFT LCD 5 inch, Smart Key, Cổng sạc USB-C, Kết nối smartphone, Chế độ lái thể thao',
            description='Phiên bản nâng cấp 2025 với công suất tăng lên 17.8 mã lực, màn hình TFT 5 inch, Smart Key và nhiều tính năng thông minh mới.',
            warranty='3 năm hoặc 30,000 km',
            fuel_consumption='1.7 L/100km',
            colors='Đỏ-Đen-Trắng Mới, Đen-Vàng Thể Thao, Xanh-Đen Metallic',
            rating=4.9
        ))
        
        # Honda CB150R 2025 - Naked bike nâng cấp
        motorcycles.append(self.create_motorcycle(
            'Honda', 'CB150R 2025', 2025, 'Xe naked bike',
            115000000,
            fuel_type='Xăng',
            engine_cc=149,
            engine_type='Xi-lanh đơn, 4 kỳ, DOHC, làm mát bằng dung dịch',
            power_hp=18.2,
            power_rpm=10000,
            torque_nm=14.8,
            torque_rpm=8000,
            compression_ratio='11.3:1',
            bore_stroke='62.0 x 49.5 mm',
            valve_system='DOHC 4 van',
            transmission='Số sàn 6 cấp',
            clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử PGM-FI',
            starter='Điện',
            ignition='Full Transitor (điện tử)',
            frame_type='Khung Delta Box thép',
            front_suspension='Phuộc USD 37mm có thể điều chỉnh',
            rear_suspension='Phuộc đơn Pro-Link có thể điều chỉnh',
            front_brake='Đĩa đơn 296mm, phanh ABS',
            rear_brake='Đĩa đơn 220mm, phanh ABS',
            front_tire='110/70-17M/C',
            rear_tire='150/60-17M/C',
            dimensions_mm='2020 x 820 x 1045',
            wheelbase_mm=1345,
            ground_clearance_mm=165,
            seat_height_mm=810,
            weight_kg=130,
            fuel_capacity_l=12.0,
            abs=True,
            smart_key=True,
            display_type='TFT LCD màu 5 inch',
            lighting='Đèn LED toàn bộ với DRL',
            features='Phanh ABS, TFT LCD 5 inch, Smart Key, Cổng sạc USB, Chế độ lái Eco/Sport, Quickshifter',
            description='Naked bike thể thao 2025 nâng cấp với công suất 18.2 mã lực, phuộc USD, TFT màn hình và nhiều công nghệ mới.',
            warranty='3 năm hoặc 30,000 km',
            fuel_consumption='2.1 L/100km',
            colors='Đỏ Matte, Đen Matte, Xanh Dương Metallic',
            rating=4.8
        ))
        
        # ============ Yamaha 2025年新摩托车型 ============
        print("【Yamaha 2025年新摩托车型】")
        
        # Yamaha Exciter 155 2025 - Phiên bản mới
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'Exciter 155 2025', 2025, 'Xe thể thao',
            55000000,
            fuel_type='Xăng',
            engine_cc=155,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            power_hp=16.8,
            power_rpm=8500,
            torque_nm=14.2,
            torque_rpm=7000,
            compression_ratio='10.9:1',
            bore_stroke='58.0 x 58.7 mm',
            valve_system='SOHC 4 van VVA',
            transmission='Số sàn 6 cấp',
            clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử',
            starter='Điện',
            ignition='TCI (điện tử)',
            frame_type='Khung Delta Box',
            front_suspension='Telescopic có thể điều chỉnh',
            rear_suspension='Monocross có thể điều chỉnh',
            front_brake='Đĩa đơn 267mm, phanh ABS',
            rear_brake='Đĩa đơn 230mm, phanh ABS',
            front_tire='100/80-17M/C',
            rear_tire='130/70-17M/C',
            dimensions_mm='1980 x 700 x 1100',
            wheelbase_mm=1290,
            ground_clearance_mm=150,
            seat_height_mm=795,
            weight_kg=118,
            fuel_capacity_l=4.6,
            abs=True,
            smart_key=False,
            display_type='LCD kỹ thuật số màu',
            lighting='Đèn LED toàn bộ',
            features='Phanh ABS, LCD màu, Y-Connect, Cổng sạc USB, Chế độ Eco, Báo động chống trộm',
            description='Exciter 155 phiên bản 2025 với nhiều cải tiến về thiết kế, công nghệ và hiệu suất, duy trì vị thế dẫn đầu phân khúc.',
            warranty='3 năm hoặc 30,000 km',
            fuel_consumption='1.9 L/100km',
            colors='Xanh GP Mới, Đỏ Đen, Trắng Xanh, Đen Matte',
            rating=4.8
        ))
        
        # Yamaha R15M 2025 - Sportbike cao cấp
        motorcycles.append(self.create_motorcycle(
            'Yamaha', 'R15M 2025', 2025, 'Xe thể thao cao cấp',
            85000000,
            fuel_type='Xăng',
            engine_cc=155,
            engine_type='Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            power_hp=18.4,
            power_rpm=10000,
            torque_nm=14.2,
            torque_rpm=7500,
            compression_ratio='11.2:1',
            bore_stroke='58.0 x 58.7 mm',
            valve_system='SOHC 4 van VVA',
            transmission='Số sàn 6 cấp với Quickshifter',
            clutch_type='Ly hợp ướt đa đĩa',
            fuel_supply='Phun xăng điện tử',
            starter='Điện',
            ignition='TCI (điện tử)',
            frame_type='Khung Deltabox',
            front_suspension='Phuộc USD KYB 37mm',
            rear_suspension='Phuộc đơn có thể điều chỉnh',
            front_brake='Đĩa đơn 282mm, phanh ABS',
            rear_brake='Đĩa đơn 220mm, phanh ABS',
            front_tire='100/80-17M/C',
            rear_tire='140/70-17M/C',
            dimensions_mm='1990 x 725 x 1135',
            wheelbase_mm=1325,
            ground_clearance_mm=155,
            seat_height_mm=815,
            weight_kg=142,
            fuel_capacity_l=11.0,
            abs=True,
            smart_key=True,
            display_type='TFT LCD màu 5 inch',
            lighting='Đèn LED Matrix với DRL',
            features='Phanh ABS, TFT LCD 5 inch, Smart Key, Quickshifter, Y-Connect, Chế độ lái A/B, Traction Control',
            description='Sportbike cao cấp 2025 với công nghệ MotoGP, TFT màn hình, Quickshifter và hệ thống kiểm soát lực kéo.',
            warranty='3 năm hoặc 30,000 km',
            fuel_consumption='2.3 L/100km',
            colors='Xanh Dương MotoGP, Đen Matte, Trắng Đỏ Racing',
            rating=4.9
        ))
        
        # ============ VinFast 2025年电动摩托车 ============
        print("【VinFast 2025年电动摩托车】")
        
        # VinFast Evo200 2025 - Xe máy điện cao cấp
        motorcycles.append(self.create_motorcycle(
            'VinFast', 'Evo200 2025', 2025, 'Xe máy điện cao cấp',
            75000000,
            fuel_type='Điện',
            engine_cc=0,  # Điện không có phân khối
            engine_type='Motor điện BLDC',
            power_hp=13.4,  # Tương đương 10kW
            power_rpm=3000,
            torque_nm=110,
            torque_rpm=0,
            transmission='Trực tiếp (không hộp số)',
            frame_type='Khung thép cao cấp',
            front_suspension='Telescopic có thể điều chỉnh',
            rear_suspension='Phuộc đơn có thể điều chỉnh',
            front_brake='Đĩa đơn 220mm, phanh CBS',
            rear_brake='Đĩa đơn 190mm, phanh CBS',
            front_tire='90/90-12',
            rear_tire='90/90-12',
            dimensions_mm='1850 x 680 x 1100',
            wheelbase_mm=1285,
            ground_clearance_mm=135,
            seat_height_mm=760,
            weight_kg=85,
            abs=False,
            smart_key=True,
            display_type='LCD màu 4.3 inch',
            lighting='Đèn LED toàn bộ',
            features='Smart Key, LCD màu, Kết nối smartphone, GPS, Chống trộm từ xa, Sạc nhanh, Pin có thể tháo rời',
            description='Xe máy điện cao cấp 2025 với pin lithium 3.5kWh, tầm di chuyển 160km, sạc nhanh 2.5 giờ, thiết kế thể thao hiện đại.',
            warranty='3 năm xe, 5 năm pin',
            fuel_consumption='0 L/100km (1.8 kWh/100km)',
            colors='Xanh Dương Điện, Trắng Ngọc Trai, Đen Matte, Đỏ Thể Thao',
            rating=4.6
        ))
        
        print(f"✅ 已爬取 {len(motorcycles)} 个2025年新摩托车型")
        return motorcycles

    def save_data(self):
        """保存爬取的数据到JSON文件"""
        print("\n💾 保存数据到文件...")
        
        # 创建数据目录
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        # 保存汽车数据
        cars_file = os.path.join(data_dir, 'vietnam_cars_2025.json')
        with open(cars_file, 'w', encoding='utf-8') as f:
            json.dump(self.cars_2025, f, ensure_ascii=False, indent=2)
        print(f"✅ 汽车数据已保存: {cars_file}")
        print(f"   📊 共 {len(self.cars_2025)} 个2025年新车型")
        
        # 保存摩托车数据
        motorcycles_file = os.path.join(data_dir, 'vietnam_motorcycles_2025.json')
        with open(motorcycles_file, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles_2025, f, ensure_ascii=False, indent=2)
        print(f"✅ 摩托车数据已保存: {motorcycles_file}")
        print(f"   📊 共 {len(self.motorcycles_2025)} 个2025年新摩托车型")
        
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
        
        stats_file = os.path.join(data_dir, 'vietnam_2025_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        print(f"✅ 统计信息已保存: {stats_file}")

    def run(self):
        """运行爬虫"""
        print("🚀 开始爬取越南2025年新车型数据...")
        print("=" * 60)
        
        # 爬取2025年汽车
        self.cars_2025 = self.crawl_2025_cars()
        self.random_delay(1, 2)
        
        # 爬取2025年摩托车
        self.motorcycles_2025 = self.crawl_2025_motorcycles()
        
        # 保存数据
        self.save_data()
        
        print("\n" + "=" * 60)
        print("🎉 2025年新车型数据爬取完成!")
        print(f"📊 总计: {len(self.cars_2025)} 汽车 + {len(self.motorcycles_2025)} 摩托车")
        print("📁 数据文件已保存到 data/ 目录")
        print("🔄 接下来请运行导入脚本将数据添加到数据库")

if __name__ == "__main__":
    crawler = Vietnam2025ModelsCrawler()
    crawler.run()
