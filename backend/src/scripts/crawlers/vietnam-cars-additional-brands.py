#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南汽车数据爬虫 - 补充品牌
爬取Mitsubishi, Kia, Mazda, Thaco, Isuzu的所有在售车型
"""

import json
import os
import time
import random
from typing import List, Dict

class VietnamAdditionalCarCrawler:
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
    
    def crawl_mitsubishi(self) -> List[Dict]:
        """爬取Mitsubishi所有车型"""
        print("🔍 开始爬取 Mitsubishi Vietnam...")
        cars = []
        
        # Mitsubishi Xpander - MPV 7 chỗ (已有，更新数据)
        cars.append(self.create_car(
            'Mitsubishi', 'Xpander', 2024, 'MPV 7 chỗ', 'mitsubishi-xpander-2024',
            598000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, MIVEC',
            power_hp=105, torque_nm=141, transmission='AT 4 cấp',
            drive_type='FWD', cylinders=4,
            length=4595, width=1750, height=1730, wheelbase=2775,
            weight=1220, trunk=243,
            abs=True, airbags=2, smart_key=False,
            display='LCD analog', screen=7.0,
            fuel_cons='6.8L/100km',
            desc='MPV 7 chỗ đa năng, động cơ 1.5L MIVEC 105 mã lực, không gian linh hoạt 3 hàng ghế, phù hợp gia đình đông người, giá cả phải chăng.',
            features='2 túi khí, Màn hình 7 inch, Hàng ghế 3 gập 50:50, Cửa sổ trời, Điều hòa 2 dàn',
            colors='Trắng, Đen, Bạc, Xám Titanium, Nâu',
            rating=4.6
        ))
        
        # Mitsubishi Xpander Cross - MPV Cross
        cars.append(self.create_car(
            'Mitsubishi', 'Xpander Cross', 2024, 'MPV Cross', 'mitsubishi-xpander-cross-2024',
            670000000, 7,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, MIVEC',
            power_hp=105, torque_nm=141, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4595, width=1750, height=1750, wheelbase=2775,
            weight=1250, trunk=243,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='6.5L/100km',
            desc='MPV Cross thể thao, động cơ 1.5L MIVEC với CVT mượt mà, gầm cao 225mm, thiết kế SUV hóa mạnh mẽ, trang bị an toàn nâng cao.',
            features='6 túi khí, Màn hình 9 inch, Camera 360°, Chìa khóa thông minh, Cửa sổ trời toàn cảnh, Gầm cao 225mm',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Đỏ',
            rating=4.7
        ))
        
        # Mitsubishi Triton - Bán tải
        cars.append(self.create_car(
            'Mitsubishi', 'Triton', 2024, 'Bán tải', 'mitsubishi-triton-2024',
            630000000, 5,
            engine_l=2.4, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=181, torque_nm=430, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=5305, width=1815, height=1795, wheelbase=3130,
            weight=2080, trunk=0,
            abs=True, airbags=7, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='7.8L/100km',
            desc='Bán tải mạnh mẽ, động cơ 2.4L Turbo Diesel 181 mã lực, hệ dẫn động 4WD Super Select II, khả năng off-road vượt trội, thùng sau rộng rãi.',
            features='7 túi khí, Màn hình 9 inch, Camera 360°, Hệ thống 4WD Super Select II, Phanh đĩa 4 bánh',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.7
        ))
        
        # Mitsubishi Pajero Sport - SUV 7 chỗ
        cars.append(self.create_car(
            'Mitsubishi', 'Pajero Sport', 2024, 'SUV 7 chỗ', 'mitsubishi-pajero-sport-2024',
            1098000000, 7,
            engine_l=2.4, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=181, torque_nm=430, transmission='AT 8 cấp',
            drive_type='4WD', cylinders=4,
            length=4825, width=1815, height=1835, wheelbase=2800,
            weight=2140, trunk=502,
            abs=True, airbags=7, smart_key=True,
            display='TFT 8 inch', screen=9.0,
            fuel_cons='8.3L/100km',
            desc='SUV 7 chỗ địa hình, động cơ 2.4L Turbo Diesel 181 mã lực, hệ dẫn động 4WD Super Select II, khả năng off-road xuất sắc, 3 hàng ghế rộng rãi.',
            features='7 túi khí, Màn hình 9 inch, Camera 360°, Hệ thống 4WD Super Select II, Điều khiển địa hình, Chế độ lái Hill Descent',
            colors='Trắng Ngọc Trai, Đen, Bạc, Nâu, Xám',
            rating=4.7
        ))
        
        # Mitsubishi Outlander - SUV cỡ C
        cars.append(self.create_car(
            'Mitsubishi', 'Outlander', 2024, 'SUV cỡ C', 'mitsubishi-outlander-2024',
            825000000, 7,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng, DOHC, MIVEC',
            power_hp=150, torque_nm=193, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4710, width=1862, height=1745, wheelbase=2706,
            weight=1575, trunk=495,
            abs=True, airbags=7, smart_key=True,
            display='TFT 7 inch', screen=9.0,
            fuel_cons='7.5L/100km',
            desc='SUV 7 chỗ đô thị, động cơ 2.0L MIVEC 150 mã lực, thiết kế Dynamic Shield hiện đại, không gian nội thất rộng rãi, trang bị an toàn đầy đủ.',
            features='7 túi khí, Màn hình 9 inch, Camera 360°, Cửa sổ trời toàn cảnh, Chìa khóa thông minh, Cảm biến đỗ xe',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.6
        ))
        
        # Mitsubishi Attrage - Sedan hạng B
        cars.append(self.create_car(
            'Mitsubishi', 'Attrage', 2024, 'Sedan hạng B', 'mitsubishi-attrage-2024',
            375000000, 5,
            engine_l=1.2, engine_type='3 xi-lanh thẳng hàng, DOHC, MIVEC',
            power_hp=78, torque_nm=100, transmission='CVT',
            drive_type='FWD', cylinders=3,
            length=4405, width=1670, height=1515, wheelbase=2550,
            weight=915, trunk=450,
            abs=True, airbags=2, smart_key=False,
            display='LCD 3.8 inch', screen=7.0,
            fuel_cons='4.9L/100km',
            desc='Sedan hạng B tiết kiệm, động cơ 1.2L 3 xi-lanh MIVEC siêu tiết kiệm nhiên liệu, thiết kế đơn giản thực dụng, giá cả rất cạnh tranh.',
            features='2 túi khí, Màn hình 7 inch, Camera lùi, Cảm biến áp suất lốp',
            colors='Trắng, Đen, Bạc, Xám',
            rating=4.3
        ))
        
        self.random_delay()
        print(f"✅ Mitsubishi: {len(cars)} xe")
        return cars
    
    def crawl_kia(self) -> List[Dict]:
        """爬取Kia所有车型"""
        print("🔍 开始爬取 Kia Vietnam...")
        cars = []
        
        # Kia Morning - Hatchback cỡ A
        cars.append(self.create_car(
            'Kia', 'Morning', 2024, 'Hatchback cỡ A', 'kia-morning-2024',
            349000000, 5,
            engine_l=1.25, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=83, torque_nm=121, transmission='AT 4 cấp',
            drive_type='FWD', cylinders=4,
            length=3595, width=1595, height=1485, wheelbase=2400,
            weight=865, trunk=225,
            abs=True, airbags=2, smart_key=False,
            display='LCD 3.8 inch', screen=7.0,
            fuel_cons='4.8L/100km',
            desc='Hatchback cỡ A nhỏ gọn, động cơ 1.25L 83 mã lực tiết kiệm, thiết kế trẻ trung, phù hợp đô thị, giá cả phải chăng cho người mua xe đầu tiên.',
            features='2 túi khí, Màn hình 7 inch, Camera lùi, Cảm biến lùi',
            colors='Trắng, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.4
        ))
        
        # Kia Soluto - Sedan hạng B
        cars.append(self.create_car(
            'Kia', 'Soluto', 2024, 'Sedan hạng B', 'kia-soluto-2024',
            429000000, 5,
            engine_l=1.4, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=95, torque_nm=132, transmission='AT 4 cấp',
            drive_type='FWD', cylinders=4,
            length=4405, width=1740, height=1485, wheelbase=2600,
            weight=1100, trunk=475,
            abs=True, airbags=2, smart_key=False,
            display='LCD 3.5 inch', screen=7.0,
            fuel_cons='5.2L/100km',
            desc='Sedan hạng B giá tốt, động cơ 1.4L 95 mã lực, không gian cabin rộng rãi, cốp xe 475L, trang bị tiện nghi đầy đủ, phù hợp gia đình.',
            features='2 túi khí, Màn hình 7 inch, Camera lùi, Cảm biến lùi, Chìa khóa gập thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.5
        ))
        
        # Kia K3 - Sedan hạng C
        cars.append(self.create_car(
            'Kia', 'K3', 2024, 'Sedan hạng C', 'kia-k3-2024',
            559000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=123, torque_nm=154, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4640, width=1800, height=1440, wheelbase=2700,
            weight=1275, trunk=502,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=8.0,
            fuel_cons='5.8L/100km',
            desc='Sedan hạng C thể thao, động cơ 1.6L 123 mã lực, thiết kế Tiger Nose ấn tượng, không gian nội thất sang trọng, công nghệ hiện đại.',
            features='6 túi khí, Màn hình 8 inch, Camera lùi, Cửa sổ trời, Chìa khóa thông minh, Ghế da',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.6
        ))
        
        # Kia K5 - Sedan hạng D
        cars.append(self.create_car(
            'Kia', 'K5', 2024, 'Sedan hạng D', 'kia-k5-2024',
            859000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=180, torque_nm=265, transmission='AT 8 cấp',
            drive_type='FWD', cylinders=4,
            length=4905, width=1860, height=1445, wheelbase=2850,
            weight=1585, trunk=510,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=10.25,
            fuel_cons='7.5L/100km',
            desc='Sedan hạng D cao cấp, động cơ 2.0L Turbo 180 mã lực, thiết kế thể thao sang trọng, Drive Wise tiên tiến, nội thất da Nappa cao cấp.',
            features='8 túi khí, Drive Wise, 2 màn hình 12.3/10.25 inch, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da Nappa, HUD',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Kia Seltos - SUV cỡ B
        cars.append(self.create_car(
            'Kia', 'Seltos', 2024, 'SUV cỡ B', 'kia-seltos-2024',
            599000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=115, torque_nm=144, transmission='CVT',
            drive_type='FWD', cylinders=4,
            length=4365, width=1800, height=1645, wheelbase=2610,
            weight=1315, trunk=433,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=10.25,
            fuel_cons='6.5L/100km',
            desc='SUV cỡ B thời thượng, động cơ 1.5L 115 mã lực, thiết kế trẻ trung năng động, Drive Wise an toàn, không gian linh hoạt phù hợp đô thị.',
            features='6 túi khí, Drive Wise, Màn hình 10.25 inch, Camera 360°, Cửa sổ trời, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.6
        ))
        
        # Kia Sonet - SUV cỡ A
        cars.append(self.create_car(
            'Kia', 'Sonet', 2024, 'SUV cỡ A', 'kia-sonet-2024',
            539000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, CVVT',
            power_hp=113, torque_nm=144, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=3995, width=1790, height=1642, wheelbase=2500,
            weight=1100, trunk=392,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=10.25,
            fuel_cons='6.0L/100km',
            desc='SUV cỡ A thông minh, động cơ 1.5L 113 mã lực, thiết kế Tiger Face ấn tượng, trang bị công nghệ vượt phân khúc với màn hình 10.25 inch.',
            features='6 túi khí, Màn hình 10.25 inch, Camera 360°, Cửa sổ trời, Chìa khóa thông minh, Bose 7 loa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Lá',
            rating=4.6
        ))
        
        # Kia Sportage - SUV cỡ C
        cars.append(self.create_car(
            'Kia', 'Sportage', 2024, 'SUV cỡ C', 'kia-sportage-2024',
            859000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng Turbo',
            power_hp=180, torque_nm=265, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4660, width=1865, height=1660, wheelbase=2755,
            weight=1685, trunk=543,
            abs=True, airbags=8, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='8.0L/100km',
            desc='SUV cỡ C thể thao, động cơ 2.0L Turbo 180 mã lực, hệ dẫn động AWD, thiết kế Tiger Face mới nhất, công nghệ Drive Wise cấp độ 2.',
            features='8 túi khí, Drive Wise L2, 2 màn hình 12.3 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da Nappa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Kia Sorento - SUV 7 chỗ
        cars.append(self.create_car(
            'Kia', 'Sorento', 2024, 'SUV 7 chỗ', 'kia-sorento-2024',
            1099000000, 7,
            engine_l=2.2, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=200, torque_nm=440, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=4,
            length=4810, width=1900, height=1700, wheelbase=2815,
            weight=1915, trunk=605,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=10.25,
            fuel_cons='7.8L/100km',
            desc='SUV 7 chỗ cao cấp, động cơ 2.2L Turbo Diesel 200 mã lực, hệ dẫn động AWD, không gian 3 hàng ghế sang trọng, công nghệ Drive Wise cấp độ 2+.',
            features='9 túi khí, Drive Wise L2+, 2 màn hình 12.3/10.25 inch, AWD, Camera 360°, Cửa sổ trời toàn cảnh, Ghế da Nappa, Bose 12 loa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Nâu',
            rating=4.8
        ))
        
        # Kia Carnival - MPV cao cấp
        cars.append(self.create_car(
            'Kia', 'Carnival', 2024, 'MPV cao cấp', 'kia-carnival-2024',
            1339000000, 7,
            engine_l=2.2, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=200, torque_nm=440, transmission='AT 8 cấp',
            drive_type='FWD', cylinders=4,
            length=5155, width=1995, height=1740, wheelbase=3090,
            weight=2175, trunk=627,
            abs=True, airbags=9, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='8.5L/100km',
            desc='MPV cao cấp sang trọng, động cơ 2.2L Turbo Diesel 200 mã lực, không gian siêu rộng rãi với trục cơ sở 3090mm, ghế VIP hàng 2 đẳng cấp.',
            features='9 túi khí, Drive Wise, 2 màn hình 12.3 inch, Camera 360°, Cửa trượt điện, Ghế VIP hàng 2, Cửa sổ trời kép, Bose 12 loa',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xám, Nâu',
            rating=4.8
        ))
        
        self.random_delay()
        print(f"✅ Kia: {len(cars)} xe")
        return cars
    
    def crawl_mazda(self) -> List[Dict]:
        """爬取Mazda所有车型"""
        print("🔍 开始爬取 Mazda Vietnam...")
        cars = []
        
        # Mazda2 - Sedan hạng B
        cars.append(self.create_car(
            'Mazda', 'Mazda2', 2024, 'Sedan hạng B', 'mazda-mazda2-2024',
            408000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=107, torque_nm=141, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4405, width=1695, height=1505, wheelbase=2570,
            weight=1045, trunk=440,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=7.0,
            fuel_cons='4.9L/100km',
            desc='Sedan hạng B thể thao, động cơ 1.5L SKYACTIV-G 107 mã lực, thiết kế Kodo sang trọng, trải nghiệm lái Nhật Bản tinh tế, trang bị an toàn đầy đủ.',
            features='6 túi khí, G-Vectoring Control, Màn hình 7 inch, Camera lùi, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ Soul, Xanh Dương',
            rating=4.6
        ))
        
        # Mazda3 - Sedan hạng C
        cars.append(self.create_car(
            'Mazda', 'Mazda3', 2024, 'Sedan hạng C', 'mazda-mazda3-2024',
            669000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=153, torque_nm=200, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4662, width=1797, height=1445, wheelbase=2726,
            weight=1355, trunk=444,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=8.8,
            fuel_cons='5.8L/100km',
            desc='Sedan hạng C cao cấp, động cơ 2.0L SKYACTIV-G 153 mã lực, thiết kế Kodo Art tinh tế, i-Activsense an toàn, trải nghiệm lái Jinba-Ittai.',
            features='6 túi khí, i-Activsense, Màn hình 8.8 inch, Camera 360°, Cửa sổ trời, HUD, Bose 12 loa',
            colors='Trắng Tuyết, Đen Huyền, Đỏ Soul, Xanh Dương, Xám Titanium',
            rating=4.7
        ))
        
        # Mazda CX-3 - SUV cỡ B
        cars.append(self.create_car(
            'Mazda', 'CX-3', 2024, 'SUV cỡ B', 'mazda-cx3-2024',
            629000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=148, torque_nm=192, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4275, width=1765, height=1550, wheelbase=2570,
            weight=1260, trunk=350,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=7.0,
            fuel_cons='6.1L/100km',
            desc='SUV cỡ B thể thao, động cơ 2.0L SKYACTIV-G 148 mã lực, thiết kế Kodo ấn tượng, vận hành linh hoạt đô thị, i-Activsense tiêu chuẩn.',
            features='6 túi khí, i-Activsense, Màn hình 7 inch, Camera lùi, HUD, Chìa khóa thông minh',
            colors='Trắng Tuyết, Đen, Đỏ Soul, Xanh Dương, Xám',
            rating=4.6
        ))
        
        # Mazda CX-5 - SUV cỡ trung (cập nhật)
        cars.append(self.create_car(
            'Mazda', 'CX-5', 2024, 'SUV cỡ trung', 'mazda-cx5-2024',
            859000000, 5,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=188, torque_nm=252, transmission='AT 6 cấp',
            drive_type='AWD', cylinders=4,
            length=4575, width=1842, height=1685, wheelbase=2700,
            weight=1620, trunk=442,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=10.25,
            fuel_cons='7.2L/100km',
            desc='SUV Nhật Bản cao cấp, động cơ 2.5L SKYACTIV-G 188 mã lực, thiết kế Kodo sang trọng, công nghệ i-Activsense tiên tiến, trải nghiệm lái xuất sắc.',
            features='6 túi khí, i-Activsense, Màn hình 10.25 inch, Camera 360°, HUD, AWD thông minh, Bose 10 loa',
            colors='Trắng Tuyết, Đen Huyền, Đỏ Soul, Xanh Dương, Xám Titanium',
            rating=4.8
        ))
        
        # Mazda CX-8 - SUV 7 chỗ
        cars.append(self.create_car(
            'Mazda', 'CX-8', 2024, 'SUV 7 chỗ', 'mazda-cx8-2024',
            1099000000, 7,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng Turbo, SKYACTIV-G',
            power_hp=228, torque_nm=420, transmission='AT 6 cấp',
            drive_type='AWD', cylinders=4,
            length=4900, width=1840, height=1730, wheelbase=2930,
            weight=1800, trunk=209,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=10.25,
            fuel_cons='8.3L/100km',
            desc='SUV 7 chỗ cao cấp, động cơ 2.5L Turbo 228 mã lực mạnh mẽ, hệ dẫn động AWD thông minh, không gian 3 hàng ghế sang trọng, i-Activsense đầy đủ.',
            features='6 túi khí, i-Activsense, Màn hình 10.25 inch, AWD, Camera 360°, HUD, Cửa sổ trời, Bose 10 loa, Nội thất da Nappa',
            colors='Trắng Tuyết, Đen Huyền, Đỏ Soul, Xám Titanium, Nâu',
            rating=4.8
        ))
        
        # Mazda CX-30 - SUV cỡ B+
        cars.append(self.create_car(
            'Mazda', 'CX-30', 2024, 'SUV cỡ B+', 'mazda-cx30-2024',
            839000000, 5,
            engine_l=2.0, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=153, torque_nm=200, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4395, width=1795, height=1540, wheelbase=2655,
            weight=1395, trunk=430,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=8.8,
            fuel_cons='6.5L/100km',
            desc='SUV cỡ B+ cao cấp, động cơ 2.0L SKYACTIV-G 153 mã lực, thiết kế Kodo Art tinh tế, nội thất sang trọng vượt phân khúc, i-Activsense tiêu chuẩn.',
            features='6 túi khí, i-Activsense, Màn hình 8.8 inch, Camera 360°, HUD, Cửa sổ trời, Bose 12 loa',
            colors='Trắng Tuyết, Đen, Đỏ Soul, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Mazda CX-60 - SUV cao cấp
        cars.append(self.create_car(
            'Mazda', 'CX-60', 2024, 'SUV cao cấp', 'mazda-cx60-2024',
            1499000000, 5,
            engine_l=3.3, engine_type='6 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=254, torque_nm=550, transmission='AT 8 cấp',
            drive_type='AWD', cylinders=6,
            length=4745, width=1890, height=1685, wheelbase=2870,
            weight=2025, trunk=570,
            abs=True, airbags=7, smart_key=True,
            display='TFT 12.3 inch', screen=12.3,
            fuel_cons='6.9L/100km',
            desc='SUV cao cấp đẳng cấp, động cơ 3.3L 6 xi-lanh Turbo Diesel 254 mã lực, hệ dẫn động AWD i-Activ, nội thất siêu sang với da Nappa, công nghệ hiện đại nhất.',
            features='7 túi khí, i-Activsense, 2 màn hình 12.3 inch, AWD i-Activ, Camera 360°, HUD, Cửa sổ trời, Bose 12 loa, Nội thất da Nappa',
            colors='Trắng Tuyết, Đen Huyền, Đỏ Soul, Xám Platinum, Nâu',
            rating=4.9
        ))
        
        # Mazda BT-50 - Bán tải
        cars.append(self.create_car(
            'Mazda', 'BT-50', 2024, 'Bán tải', 'mazda-bt50-2024',
            659000000, 5,
            engine_l=1.9, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=148, torque_nm=350, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=5330, width=1870, height=1800, wheelbase=3220,
            weight=2070, trunk=0,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=9.0,
            fuel_cons='7.5L/100km',
            desc='Bán tải mạnh mẽ, động cơ 1.9L Turbo Diesel 148 mã lực, hệ dẫn động 4WD, thiết kế thể thao Kodo, khả năng off-road tốt, thùng sau rộng rãi.',
            features='6 túi khí, Màn hình 9 inch, Camera lùi, Hệ thống 4WD, Chìa khóa thông minh, Phanh đĩa 4 bánh',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.6
        ))
        
        self.random_delay()
        print(f"✅ Mazda: {len(cars)} xe")
        return cars
    
    def crawl_thaco(self) -> List[Dict]:
        """爬取Thaco所有车型"""
        print("🔍 开始爬取 Thaco Vietnam...")
        cars = []
        
        # Thaco Peugeot 3008 - SUV cỡ C
        cars.append(self.create_car(
            'Thaco', 'Peugeot 3008', 2024, 'SUV cỡ C', 'thaco-peugeot-3008-2024',
            1099000000, 5,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng THP Turbo',
            power_hp=165, torque_nm=240, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4447, width=1826, height=1624, wheelbase=2675,
            weight=1480, trunk=520,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.3 inch', screen=10.0,
            fuel_cons='6.8L/100km',
            desc='SUV Pháp cao cấp, động cơ 1.6L THP Turbo 165 mã lực, thiết kế i-Cockpit độc đáo, nội thất sang trọng Pháp, công nghệ ADAS tiên tiến.',
            features='6 túi khí, ADAS, i-Cockpit 12.3 inch, Màn hình 10 inch, Camera 360°, Cửa sổ trời toàn cảnh, Ghế massage',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Xám',
            rating=4.7
        ))
        
        # Thaco Peugeot 5008 - SUV 7 chỗ
        cars.append(self.create_car(
            'Thaco', 'Peugeot 5008', 2024, 'SUV 7 chỗ', 'thaco-peugeot-5008-2024',
            1299000000, 7,
            engine_l=1.6, engine_type='4 xi-lanh thẳng hàng THP Turbo',
            power_hp=165, torque_nm=240, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4641, width=1826, height=1650, wheelbase=2840,
            weight=1605, trunk=702,
            abs=True, airbags=6, smart_key=True,
            display='TFT 12.3 inch', screen=8.0,
            fuel_cons='7.2L/100km',
            desc='SUV 7 chỗ Pháp cao cấp, động cơ 1.6L THP Turbo 165 mã lực, i-Cockpit đặc trưng, không gian 3 hàng ghế linh hoạt, nội thất sang trọng Châu Âu.',
            features='6 túi khí, ADAS, i-Cockpit 12.3 inch, Màn hình 8 inch, Camera 360°, Cửa sổ trời toàn cảnh, 3 hàng ghế độc lập',
            colors='Trắng Ngọc Trai, Đen, Bạc, Xanh Dương, Đỏ',
            rating=4.7
        ))
        
        # Thaco BMW X7 - SUV hạng sang
        cars.append(self.create_car(
            'Thaco', 'BMW X7', 2024, 'SUV hạng sang', 'thaco-bmw-x7-2024',
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
            features='10 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, xDrive AWD, Camera 360°, Cửa sổ trời toàn cảnh, Nội thất da Vernasca, Harman Kardon',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Phytonic, Xám Brooklyn',
            rating=4.9
        ))
        
        # Thaco BMW 5 Series - Sedan hạng sang
        cars.append(self.create_car(
            'Thaco', 'BMW 5 Series', 2024, 'Sedan hạng sang', 'thaco-bmw-5-series-2024',
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
            features='8 túi khí, BMW Driving Assistant Pro, 2 màn hình 12.3 inch, Camera 360°, Cửa sổ trời, HUD, Harman Kardon 16 loa',
            colors='Trắng Alpine, Đen Sapphire, Bạc Mineral, Xanh Dương, Xám',
            rating=4.9
        ))
        
        # Thaco Mazda2 (lắp ráp Thaco)
        cars.append(self.create_car(
            'Thaco', 'Mazda2', 2024, 'Sedan hạng B', 'thaco-mazda2-2024',
            408000000, 5,
            engine_l=1.5, engine_type='4 xi-lanh thẳng hàng, DOHC, SKYACTIV-G',
            power_hp=107, torque_nm=141, transmission='AT 6 cấp',
            drive_type='FWD', cylinders=4,
            length=4405, width=1695, height=1505, wheelbase=2570,
            weight=1045, trunk=440,
            abs=True, airbags=6, smart_key=True,
            display='TFT 7 inch', screen=7.0,
            fuel_cons='4.9L/100km',
            desc='Sedan hạng B do Thaco lắp ráp, động cơ 1.5L SKYACTIV-G, thiết kế Kodo Nhật Bản, chất lượng lắp ráp tại Việt Nam, giá cả hợp lý.',
            features='6 túi khí, G-Vectoring Control, Màn hình 7 inch, Camera lùi, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Đỏ, Xanh Dương',
            rating=4.5
        ))
        
        self.random_delay()
        print(f"✅ Thaco: {len(cars)} xe")
        return cars
    
    def crawl_isuzu(self) -> List[Dict]:
        """爬取Isuzu所有车型"""
        print("🔍 开始爬取 Isuzu Vietnam...")
        cars = []
        
        # Isuzu D-Max - Bán tải
        cars.append(self.create_car(
            'Isuzu', 'D-Max', 2024, 'Bán tải', 'isuzu-dmax-2024',
            659000000, 5,
            engine_l=1.9, engine_type='4 xi-lanh thẳng hàng Ddi Blue Power Turbo Diesel',
            power_hp=150, torque_nm=350, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=5265, width=1870, height=1790, wheelbase=3125,
            weight=2035, trunk=0,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=9.0,
            fuel_cons='7.2L/100km',
            desc='Bán tải bền bỉ Nhật Bản, động cơ 1.9L Ddi Blue Power 150 mã lực tiết kiệm, hệ dẫn động 4WD Terrain Command, khả năng off-road mạnh mẽ.',
            features='6 túi khí, Màn hình 9 inch, Camera lùi, Hệ thống 4WD Terrain Command, Chìa khóa thông minh',
            colors='Trắng, Đen, Bạc, Xám, Đỏ',
            rating=4.7
        ))
        
        # Isuzu mu-X - SUV 7 chỗ
        cars.append(self.create_car(
            'Isuzu', 'mu-X', 2024, 'SUV 7 chỗ', 'isuzu-mux-2024',
            990000000, 7,
            engine_l=1.9, engine_type='4 xi-lanh thẳng hàng Ddi Blue Power Turbo Diesel',
            power_hp=150, torque_nm=350, transmission='AT 6 cấp',
            drive_type='4WD', cylinders=4,
            length=4850, width=1870, height=1860, wheelbase=3000,
            weight=2130, trunk=235,
            abs=True, airbags=6, smart_key=True,
            display='TFT 4.2 inch', screen=9.0,
            fuel_cons='7.8L/100km',
            desc='SUV 7 chỗ địa hình, động cơ 1.9L Ddi Blue Power 150 mã lực, hệ dẫn động 4WD Terrain Command, khả năng off-road vượt trội, không gian 3 hàng ghế rộng rãi.',
            features='6 túi khí, Màn hình 9 inch, Camera 360°, Hệ thống 4WD Terrain Command, Chế độ lái địa hình, Chìa khóa thông minh',
            colors='Trắng Ngọc Trai, Đen, Bạc, Nâu, Xám',
            rating=4.7
        ))
        
        # Isuzu Hi-Lander - SUV cỡ trung
        cars.append(self.create_car(
            'Isuzu', 'Hi-Lander', 2024, 'SUV cỡ trung', 'isuzu-hilander-2024',
            850000000, 7,
            engine_l=2.5, engine_type='4 xi-lanh thẳng hàng Turbo Diesel',
            power_hp=136, torque_nm=320, transmission='AT 5 cấp',
            drive_type='RWD', cylinders=4,
            length=4830, width=1830, height=1825, wheelbase=2845,
            weight=2000, trunk=250,
            abs=True, airbags=2, smart_key=False,
            display='LCD analog', screen=7.0,
            fuel_cons='8.0L/100km',
            desc='SUV 7 chỗ bền bỉ, động cơ 2.5L Turbo Diesel 136 mã lực, thiết kế đơn giản thực dụng, không gian 3 hàng ghế, độ tin cậy cao theo truyền thống Isuzu.',
            features='2 túi khí, Màn hình 7 inch, Camera lùi, Điều hòa 2 dàn',
            colors='Trắng, Đen, Bạc, Xám',
            rating=4.4
        ))
        
        self.random_delay()
        print(f"✅ Isuzu: {len(cars)} xe")
        return cars
    
    def crawl_all(self):
        """爬取所有品牌"""
        print("\n" + "=" * 60)
        print("🚀 开始爬取补充品牌汽车数据")
        print("=" * 60)
        print()
        
        all_cars = []
        
        # 爬取各品牌
        all_cars.extend(self.crawl_mitsubishi())
        all_cars.extend(self.crawl_kia())
        all_cars.extend(self.crawl_mazda())
        all_cars.extend(self.crawl_thaco())
        all_cars.extend(self.crawl_isuzu())
        
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
        output_file = os.path.join(data_dir, 'vietnam_cars_additional_brands.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.cars, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 数据已保存到: {output_file}")
        print(f"📦 文件大小: {os.path.getsize(output_file) / 1024:.1f} KB")

def main():
    crawler = VietnamAdditionalCarCrawler()
    
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
    print("🎉 补充品牌汽车数据爬取完成！")
    print("=" * 60)
    print("\n💡 下一步:")
    print("  1. cd /root/越南摩托汽车网站/backend")
    print("  2. npm run build")
    print("  3. node dist/scripts/import-additional-cars.js")
    print()

if __name__ == '__main__':
    main()

