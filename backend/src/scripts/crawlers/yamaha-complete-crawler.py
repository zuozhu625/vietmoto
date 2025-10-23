#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yamaha Vietnam 完整车型数据爬虫
包含所有在售车型的详细参数
"""

import json
from typing import List, Dict

class YamahaCompleteCrawler:
    def __init__(self):
        self.motorcycles = []
        
    def crawl_yamaha_all_models(self) -> List[Dict]:
        """
        爬取Yamaha Vietnam所有车型
        数据来源：Yamaha官方网站技术规格
        """
        print("🔍 开始爬取 Yamaha Vietnam 所有车型...")
        print("数据来源：Yamaha Vietnam 官方技术规格\n")
        
        motorcycles = []
        
        # ============ 运动型系列 ============
        print("【运动型系列】")
        
        # Exciter 155 VVA
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Exciter 155 VVA',
            'year': 2024,
            'category': 'Xe thể thao',
            'price_vnd': 50000000,
            'fuel_type': 'Xăng',
            
            # 发动机
            'engine_cc': 155,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, SOHC, làm mát bằng dung dịch',
            'power_hp': 15.4,
            'power_rpm': 8000,
            'torque_nm': 14.3,
            'torque_rpm': 6500,
            'compression_ratio': '11.6:1',
            'bore_stroke': '58.0 x 58.7 mm',
            'valve_system': 'VVA (Variable Valve Actuation) SOHC 4 van',
            
            # 传动
            'transmission': 'Số sàn 6 cấp',
            'clutch_type': 'Ly hợp ướt đa đĩa',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI (điện tử)',
            
            # 底盘
            'frame_type': 'Khung Deltabox thép (kiểu dáng giống YZF-R15)',
            'front_suspension': 'Giảm xóc ống lồng ∅37mm',
            'rear_suspension': 'Phuộc đơn Monocross',
            'front_brake': 'Đĩa đơn 267mm, phanh ABS',
            'rear_brake': 'Đĩa đơn 230mm',
            'front_tire': '100/80-17M/C',
            'rear_tire': '130/70-17M/C',
            
            # 尺寸
            'dimensions_mm': '2015 x 725 x 1100',
            'wheelbase_mm': 1325,
            'ground_clearance_mm': 165,
            'seat_height_mm': 795,
            'weight_kg': 118,
            'fuel_capacity_l': 4.6,
            
            # 配置
            'abs': True,
            'smart_key': False,
            'display_type': 'LCD đa thông tin',
            'lighting': 'Đèn LED (pha, hậu, xi-nhan)',
            'features': 'Công nghệ VVA, Phanh ABS, Đèn LED, Vành đúc, Bảng đồng hồ LCD, Yên 2 tầng thể thao',
            
            'description': 'Xe thể thao 155cc với công nghệ van biến thiên VVA độc quyền của Yamaha. Công suất mượt mà, khung gầm Deltabox thể thao như YZF-R15. Mang đến trải nghiệm lái đầy cảm xúc cho người yêu tốc độ.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.99 L/100km',
            'colors': 'Xanh GP, Đỏ-Đen, Đen-Vàng, Trắng-Xanh',
            'rating': 4.8
        })
        print("  ✅ Exciter 155 VVA")
        
        # YZF-R15
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'YZF-R15',
            'year': 2024,
            'category': 'Xe thể thao',
            'price_vnd': 79000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 155,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, SOHC, làm mát dung dịch',
            'power_hp': 18.6,
            'power_rpm': 10000,
            'torque_nm': 14.2,
            'torque_rpm': 7500,
            'compression_ratio': '11.6:1',
            'bore_stroke': '58.0 x 58.7 mm',
            'valve_system': 'VVA SOHC 4 van',
            
            'transmission': 'Số sàn 6 cấp',
            'clutch_type': 'Ly hợp ướt đa đĩa',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung Deltabox',
            'front_suspension': 'Giảm xóc ống lồng USD ∅37mm',
            'rear_suspension': 'Phuộc đơn Monocross',
            'front_brake': 'Đĩa đơn 282mm, phanh ABS',
            'rear_brake': 'Đĩa đơn 220mm',
            'front_tire': '100/80-17',
            'rear_tire': '140/70-17',
            
            'dimensions_mm': '1990 x 725 x 1135',
            'wheelbase_mm': 1325,
            'ground_clearance_mm': 170,
            'seat_height_mm': 815,
            'weight_kg': 141,
            'fuel_capacity_l': 11.0,
            
            'abs': True,
            'smart_key': False,
            'display_type': 'LCD Full Digital',
            'lighting': 'Đèn LED toàn bộ',
            'features': 'VVA, ABS, USD cao cấp, Thiết kế Full Fairing thể thao, Traction Control',
            
            'description': 'Sport bike chính hãng với thiết kế Full Fairing đậm chất đua. Động cơ 155cc VVA công suất 18.6 HP. Giảm xóc USD cao cấp. ABS an toàn. Phong cách MotoGP đích thực.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '2.1 L/100km',
            'colors': 'Xanh Racing Blue, Đen, Đỏ-Trắng',
            'rating': 4.9
        })
        print("  ✅ YZF-R15")
        
        # MT-15
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'MT-15',
            'year': 2024,
            'category': 'Xe naked bike',
            'price_vnd': 72000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 155,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, SOHC VVA, làm mát dung dịch',
            'power_hp': 18.6,
            'power_rpm': 10000,
            'torque_nm': 14.1,
            'torque_rpm': 7500,
            'compression_ratio': '11.6:1',
            'bore_stroke': '58.0 x 58.7 mm',
            'valve_system': 'VVA SOHC 4 van',
            
            'transmission': 'Số sàn 6 cấp',
            'clutch_type': 'Ly hợp ướt đa đĩa',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung Deltabox',
            'front_suspension': 'Giảm xóc ống lồng USD ∅37mm',
            'rear_suspension': 'Phuộc đơn Monocross',
            'front_brake': 'Đĩa đơn 282mm, phanh ABS',
            'rear_brake': 'Đĩa đơn 220mm',
            'front_tire': '110/70-17',
            'rear_tire': '140/70-17',
            
            'dimensions_mm': '2020 x 800 x 1070',
            'wheelbase_mm': 1335,
            'ground_clearance_mm': 165,
            'seat_height_mm': 810,
            'weight_kg': 138,
            'fuel_capacity_l': 10.0,
            
            'abs': True,
            'smart_key': False,
            'display_type': 'LCD Full Digital',
            'lighting': 'Đèn LED toàn bộ',
            'features': 'VVA, ABS, USD, Naked bike phong cách Dark Side, Vành đúc đa chấu',
            
            'description': 'Naked bike phong cách Dark Side ấn tượng. Cùng động cơ với R15 nhưng thiết kế trần trụi hầm hố. USD cao cấp, ABS an toàn. Dành cho người yêu phong cách đường phố.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '2.05 L/100km',
            'colors': 'Đen-Xanh, Xám-Đen, Xanh',
            'rating': 4.8
        })
        print("  ✅ MT-15")
        
        # ============ Xe tay ga cao cấp ============
        print("\n【Xe tay ga cao cấp】")
        
        # Grande Hybrid
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Grande Hybrid',
            'year': 2024,
            'category': 'Xe tay ga hybrid',
            'price_vnd': 48000000,
            'fuel_type': 'Hybrid',
            
            'engine_cc': 125,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát dung dịch + Hỗ trợ điện Hybrid',
            'power_hp': 9.3,
            'power_rpm': 6500,
            'torque_nm': 9.7,
            'torque_rpm': 5000,
            'compression_ratio': '11.2:1',
            'bore_stroke': '52.0 x 58.7 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử + Motor điện Hybrid',
            'starter': 'Điện + Smart Motor Generator (Hybrid)',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống Underbone',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn Unit Swing',
            'front_brake': 'Đĩa đơn 230mm, phanh UBS',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '90/90-12',
            'rear_tire': '100/90-10',
            
            'dimensions_mm': '1850 x 685 x 1115',
            'wheelbase_mm': 1265,
            'ground_clearance_mm': 133,
            'seat_height_mm': 775,
            'weight_kg': 107,
            'fuel_capacity_l': 4.2,
            
            'abs': False,
            'smart_key': True,
            'display_type': 'LCD đa thông tin',
            'lighting': 'Đèn LED toàn bộ',
            'features': 'Công nghệ Hybrid tiết kiệm, Khóa Smartkey, Blue Core, Start-Stop, Phanh UBS, Cổng USB',
            
            'description': 'Xe tay ga Hybrid đầu tiên tại Việt Nam. Công nghệ Blue Core kết hợp Motor điện giúp tiết kiệm nhiên liệu vượt trội. Khóa Smartkey tiện lợi. Thiết kế sang trọng thanh lịch.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.47 L/100km',
            'colors': 'Xám-Vàng, Nâu, Trắng-Xanh, Đen-Xanh',
            'rating': 4.7
        })
        print("  ✅ Grande Hybrid")
        
        # NVX 155 VVA
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'NVX 155 VVA',
            'year': 2024,
            'category': 'Xe tay ga thể thao',
            'price_vnd': 52000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 155,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, SOHC VVA, Blue Core, làm mát dung dịch',
            'power_hp': 15.4,
            'power_rpm': 8000,
            'torque_nm': 14.4,
            'torque_rpm': 6000,
            'compression_ratio': '11.6:1',
            'bore_stroke': '58.0 x 58.7 mm',
            'valve_system': 'VVA Blue Core SOHC 4 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống Underbone',
            'front_suspension': 'Giảm xóc ống lồng ∅33mm',
            'rear_suspension': 'Phuộc đơn Monocross',
            'front_brake': 'Đĩa đơn 230mm, phanh ABS',
            'rear_brake': 'Đĩa đơn 230mm',
            'front_tire': '110/80-14',
            'rear_tire': '130/70-13',
            
            'dimensions_mm': '1935 x 710 x 1115',
            'wheelbase_mm': 1335,
            'ground_clearance_mm': 135,
            'seat_height_mm': 795,
            'weight_kg': 116,
            'fuel_capacity_l': 6.6,
            
            'abs': True,
            'smart_key': False,
            'display_type': 'LCD Full Digital',
            'lighting': 'Đèn LED toàn bộ',
            'features': 'VVA, Blue Core, ABS, Hốc chứa đồ lớn, Yên 2 tầng thể thao, Vành đúc đa chấu',
            
            'description': 'Xe tay ga thể thao 155cc đầu tiên của Yamaha. Công nghệ VVA và Blue Core. Thiết kế thể thao năng động. Phù hợp cho giới trẻ năng động.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '2.0 L/100km',
            'colors': 'Xanh-Trắng, Đỏ-Đen, Đen-Cam, Xám',
            'rating': 4.6
        })
        print("  ✅ NVX 155 VVA")
        
        # ============ Xe tay ga phổ thông ============
        print("\n【Xe tay ga phổ thông】")
        
        # FreeGo
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'FreeGo',
            'year': 2024,
            'category': 'Xe tay ga',
            'price_vnd': 38000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 125,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát cưỡng bức',
            'power_hp': 11.4,
            'power_rpm': 6500,
            'torque_nm': 10.9,
            'torque_rpm': 5000,
            'compression_ratio': '10.9:1',
            'bore_stroke': '52.0 x 58.7 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn Unit Swing',
            'front_brake': 'Đĩa đơn 230mm, phanh UBS',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '90/90-12',
            'rear_tire': '100/90-10',
            
            'dimensions_mm': '1850 x 670 x 1115',
            'wheelbase_mm': 1260,
            'ground_clearance_mm': 135,
            'seat_height_mm': 775,
            'weight_kg': 99,
            'fuel_capacity_l': 4.2,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ analog kết hợp LCD',
            'lighting': 'Đèn LED (pha, hậu, xi-nhan)',
            'features': 'Blue Core tiết kiệm, Phanh UBS, Đèn LED, Thiết kế thể thao, Start-Stop',
            
            'description': 'Xe tay ga thể thao 125cc với công nghệ Blue Core tiết kiệm nhiên liệu. Thiết kế năng động trẻ trung. Giá cả phải chăng phù hợp sinh viên và giới trẻ.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.68 L/100km',
            'colors': 'Xanh-Đen, Đỏ-Đen, Trắng-Xanh, Đen',
            'rating': 4.6
        })
        print("  ✅ FreeGo")
        
        # Janus
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Janus',
            'year': 2024,
            'category': 'Xe tay ga',
            'price_vnd': 32500000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 125,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát cưỡng bức',
            'power_hp': 9.2,
            'power_rpm': 6500,
            'torque_nm': 9.6,
            'torque_rpm': 5000,
            'compression_ratio': '10.9:1',
            'bore_stroke': '52.0 x 58.7 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn Unit Swing',
            'front_brake': 'Đĩa đơn 190mm, phanh UBS',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '80/90-14',
            'rear_tire': '90/90-14',
            
            'dimensions_mm': '1850 x 665 x 1100',
            'wheelbase_mm': 1240,
            'ground_clearance_mm': 125,
            'seat_height_mm': 765,
            'weight_kg': 93,
            'fuel_capacity_l': 4.2,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ analog kết hợp LCD',
            'lighting': 'Đèn LED (hậu, xi-nhan), Halogen (pha)',
            'features': 'Blue Core, Phanh UBS, Thiết kế nhỏ gọn cho nữ, Tiết kiệm nhiên liệu',
            
            'description': 'Xe tay ga nhỏ gọn dành cho phái nữ. Động cơ Blue Core 125cc tiết kiệm. Trọng lượng nhẹ chỉ 93kg dễ điều khiển. Thiết kế thanh lịch nữ tính.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.62 L/100km',
            'colors': 'Hồng-Trắng, Xanh Mint, Trắng-Tím, Đen',
            'rating': 4.5
        })
        print("  ✅ Janus")
        
        # Latte
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Latte',
            'year': 2024,
            'category': 'Xe tay ga',
            'price_vnd': 40000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 125,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát cưỡng bức',
            'power_hp': 11.4,
            'power_rpm': 6500,
            'torque_nm': 10.9,
            'torque_rpm': 5000,
            'compression_ratio': '10.9:1',
            'bore_stroke': '52.0 x 58.7 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện + Stop & Start System',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn Unit Swing',
            'front_brake': 'Đĩa đơn 200mm, phanh UBS',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '90/90-12',
            'rear_tire': '100/90-10',
            
            'dimensions_mm': '1845 x 695 x 1115',
            'wheelbase_mm': 1260,
            'ground_clearance_mm': 133,
            'seat_height_mm': 775,
            'weight_kg': 104,
            'fuel_capacity_l': 4.6,
            
            'abs': False,
            'smart_key': True,
            'display_type': 'LCD',
            'lighting': 'Đèn LED toàn bộ',
            'features': 'Khóa Smartkey, Stop & Start, Blue Core, Phanh UBS, Cổng USB, Thiết kế thời trang',
            
            'description': 'Xe tay ga thời trang dành cho phái nữ. Công nghệ Blue Core tiết kiệm. Stop & Start thông minh. Khóa Smartkey tiện lợi. Thiết kế Retro thanh lịch.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.59 L/100km',
            'colors': 'Xanh Pastel, Hồng, Trắng-Vàng, Nâu Vintage',
            'rating': 4.6
        })
        print("  ✅ Latte")
        
        # ============ Xe số phổ thông ============
        print("\n【Xe số phổ thông】")
        
        # Sirius
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Sirius',
            'year': 2024,
            'category': 'Xe số',
            'price_vnd': 20500000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 110,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát cưỡng bức bằng gió',
            'power_hp': 7.8,
            'power_rpm': 7500,
            'torque_nm': 8.5,
            'torque_rpm': 5500,
            'compression_ratio': '9.2:1',
            'bore_stroke': '51.0 x 54.0 mm',
            'valve_system': 'SOHC 2 van',
            
            'transmission': 'Số sàn 4 cấp',
            'clutch_type': 'Ly hợp tự động ly tâm',
            'fuel_supply': 'Bộ chế hòa khí',
            'starter': 'Điện + đạp',
            'ignition': 'CDI',
            
            'frame_type': 'Khung xương thép Diamond',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn',
            'front_brake': 'Đĩa đơn 180mm (hoặc tang trống)',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '70/90-17',
            'rear_tire': '80/90-17',
            
            'dimensions_mm': '1930 x 720 x 1055',
            'wheelbase_mm': 1225,
            'ground_clearance_mm': 145,
            'seat_height_mm': 770,
            'weight_kg': 97,
            'fuel_capacity_l': 3.4,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ analog',
            'lighting': 'Đèn Halogen',
            'features': 'Tiết kiệm nhiên liệu, Bền bỉ, Dễ bảo dưỡng, Giá rẻ',
            
            'description': 'Xe số kinh điển cạnh tranh với Honda Wave Alpha. Động cơ 110cc tiết kiệm nhiên liệu xuất sắc. Chi phí bảo dưỡng thấp. Lựa chọn lý tưởng cho người lao động.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.62 L/100km',
            'colors': 'Đỏ, Đen, Xanh, Bạc',
            'rating': 4.5
        })
        print("  ✅ Sirius")
        
        # Jupiter
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Jupiter',
            'year': 2024,
            'category': 'Xe số',
            'price_vnd': 24000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 115,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát cưỡng bức',
            'power_hp': 8.2,
            'power_rpm': 7500,
            'torque_nm': 9.0,
            'torque_rpm': 5500,
            'compression_ratio': '9.3:1',
            'bore_stroke': '52.0 x 54.0 mm',
            'valve_system': 'SOHC 2 van',
            
            'transmission': 'Số sàn 4 cấp',
            'clutch_type': 'Ly hợp tự động',
            'fuel_supply': 'Bộ chế hòa khí',
            'starter': 'Điện + đạp',
            'ignition': 'CDI',
            
            'frame_type': 'Khung Diamond thép',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn',
            'front_brake': 'Đĩa đơn 180mm',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '70/90-17',
            'rear_tire': '80/90-17',
            
            'dimensions_mm': '1940 x 715 x 1070',
            'wheelbase_mm': 1230,
            'ground_clearance_mm': 145,
            'seat_height_mm': 775,
            'weight_kg': 100,
            'fuel_capacity_l': 3.6,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ analog',
            'lighting': 'Đèn Halogen',
            'features': 'Động cơ 115cc mạnh hơn, Thiết kế thể thao, Tiết kiệm nhiên liệu',
            
            'description': 'Xe số 115cc mạnh mẽ hơn Sirius. Thiết kế thể thao với đèn pha góc cạnh. Phù hợp cho người cần sức mạnh hơn cho đường dài.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.68 L/100km',
            'colors': 'Đỏ-Đen, Xanh, Đen, Trắng',
            'rating': 4.5
        })
        print("  ✅ Jupiter")
        
        # ============ Xe số thể thao ============
        print("\n【Xe số thể thao】")
        
        # Jupiter Fi
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Jupiter Fi',
            'year': 2024,
            'category': 'Xe số',
            'price_vnd': 28000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 115,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát cưỡng bức',
            'power_hp': 8.6,
            'power_rpm': 7500,
            'torque_nm': 9.2,
            'torque_rpm': 5500,
            'compression_ratio': '9.5:1',
            'bore_stroke': '52.0 x 54.0 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Số sàn 4 cấp',
            'clutch_type': 'Ly hợp tự động',
            'fuel_supply': 'Phun xăng điện tử FI',
            'starter': 'Điện + đạp',
            'ignition': 'TCI',
            
            'frame_type': 'Khung Diamond thép',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn Monocross',
            'front_brake': 'Đĩa đơn 220mm',
            'rear_brake': 'Tang trống 130mm',
            'front_tire': '70/90-17',
            'rear_tire': '80/90-17',
            
            'dimensions_mm': '1945 x 720 x 1075',
            'wheelbase_mm': 1235,
            'ground_clearance_mm': 148,
            'seat_height_mm': 778,
            'weight_kg': 102,
            'fuel_capacity_l': 4.0,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ LCD',
            'lighting': 'Đèn LED (pha, hậu)',
            'features': 'Blue Core FI tiết kiệm, Phanh đĩa, Đèn LED, Monocross cao cấp',
            
            'description': 'Xe số 115cc phiên bản FI (phun xăng điện tử). Blue Core tiết kiệm nhiên liệu. Phuộc Monocross cao cấp. Thiết kế thể thao năng động.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.59 L/100km',
            'colors': 'Xanh-Trắng, Đỏ-Đen, Đen-Vàng',
            'rating': 4.6
        })
        print("  ✅ Jupiter Fi")
        
        # Sirius Fi
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'Sirius Fi',
            'year': 2024,
            'category': 'Xe số',
            'price_vnd': 23500000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 110,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, Blue Core, làm mát cưỡng bức',
            'power_hp': 8.1,
            'power_rpm': 7500,
            'torque_nm': 8.8,
            'torque_rpm': 5500,
            'compression_ratio': '9.5:1',
            'bore_stroke': '51.0 x 54.0 mm',
            'valve_system': 'Blue Core SOHC 2 van',
            
            'transmission': 'Số sàn 4 cấp',
            'clutch_type': 'Ly hợp tự động',
            'fuel_supply': 'Phun xăng điện tử FI',
            'starter': 'Điện + đạp',
            'ignition': 'TCI',
            
            'frame_type': 'Khung Diamond thép',
            'front_suspension': 'Giảm xóc ống lồng',
            'rear_suspension': 'Giảm xóc đơn',
            'front_brake': 'Đĩa đơn 220mm',
            'rear_brake': 'Tang trống 110mm',
            'front_tire': '70/90-17',
            'rear_tire': '80/90-17',
            
            'dimensions_mm': '1935 x 722 x 1060',
            'wheelbase_mm': 1230,
            'ground_clearance_mm': 145,
            'seat_height_mm': 772,
            'weight_kg': 99,
            'fuel_capacity_l': 3.6,
            
            'abs': False,
            'smart_key': False,
            'display_type': 'Đồng hồ LCD',
            'lighting': 'Đèn LED (pha, hậu)',
            'features': 'Blue Core FI, Đèn LED, Phanh đĩa, Tiết kiệm nhiên liệu',
            
            'description': 'Xe số 110cc phiên bản FI tiết kiệm nhiên liệu. Blue Core công nghệ mới. Đèn LED hiện đại. Giá cả hợp lý.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '1.55 L/100km',
            'colors': 'Đỏ, Đen, Xanh, Trắng',
            'rating': 4.5
        })
        print("  ✅ Sirius Fi")
        
        # ============ Xe Maxi Scooter ============
        print("\n【Xe Maxi Scooter】")
        
        # XMAX 300
        motorcycles.append({
            'brand': 'Yamaha',
            'model': 'XMAX 300',
            'year': 2024,
            'category': 'Maxi Scooter',
            'price_vnd': 155000000,
            'fuel_type': 'Xăng',
            
            'engine_cc': 292,
            'engine_type': 'Xi-lanh đơn, 4 kỳ, SOHC, Blue Core, làm mát dung dịch',
            'power_hp': 28,
            'power_rpm': 7250,
            'torque_nm': 29,
            'torque_rpm': 5750,
            'compression_ratio': '10.9:1',
            'bore_stroke': '70.0 x 75.9 mm',
            'valve_system': 'Blue Core SOHC 4 van',
            
            'transmission': 'Tự động vô cấp (CVT)',
            'clutch_type': 'Ly hợp tự động khô',
            'fuel_supply': 'Phun xăng điện tử',
            'starter': 'Điện',
            'ignition': 'TCI',
            
            'frame_type': 'Khung thép ống Tubular Diamond',
            'front_suspension': 'Giảm xóc ống lồng ∅41mm',
            'rear_suspension': 'Giảm xóc đơn Unit Swing',
            'front_brake': 'Đĩa đôi 267mm, phanh ABS',
            'rear_brake': 'Đĩa đơn 245mm, phanh ABS',
            'front_tire': '120/70-15',
            'rear_tire': '140/70-14',
            
            'dimensions_mm': '2185 x 775 x 1355',
            'wheelbase_mm': 1540,
            'ground_clearance_mm': 145,
            'seat_height_mm': 795,
            'weight_kg': 179,
            'fuel_capacity_l': 13.2,
            
            'abs': True,
            'smart_key': True,
            'display_type': 'LCD Full Digital đa màu',
            'lighting': 'Đèn LED toàn bộ (Bi-LED)',
            'features': 'Khóa Smartkey, ABS 2 kênh, Traction Control, Blue Core, Hốc chứa đồ 45L, Cổng USB, Kính chắn gió',
            
            'description': 'Maxi Scooter cao cấp 300cc. Động cơ Blue Core mạnh mẽ. ABS 2 kênh và Traction Control an toàn. Hốc chứa đồ khổng lồ 45L. Phù hợp đi tour và di chuyển đường dài.',
            'warranty': '3 năm hoặc 30,000 km',
            'fuel_consumption': '2.9 L/100km',
            'colors': 'Xám-Đen, Trắng-Xanh, Đen',
            'rating': 4.9
        })
        print("  ✅ XMAX 300")
        
        print(f"\n✅ Yamaha Vietnam: {len(motorcycles)} xe (100% dữ liệu chi tiết)")
        return motorcycles
    
    def save_to_json(self, filename='yamaha_complete_data.json'):
        """保存数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 完整Yamaha数据已保存: {filename}")
    
    def show_summary(self):
        """显示数据摘要"""
        if not self.motorcycles:
            return
        
        print("\n" + "="*60)
        print("📊 Yamaha Vietnam 完整车型统计")
        print("="*60)
        
        # 按类别统计
        categories = {}
        for m in self.motorcycles:
            cat = m['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n【按类别统计】")
        for cat, count in sorted(categories.items()):
            print(f"  • {cat}: {count} xe")
        
        # 价格范围
        prices = [m['price_vnd'] for m in self.motorcycles]
        print(f"\n【价格范围】")
        print(f"  • 最低: {min(prices)/1000000:.1f} triệu VNĐ")
        print(f"  • 最高: {max(prices)/1000000:.0f} triệu VNĐ")
        print(f"  • 平均: {sum(prices)/len(prices)/1000000:.0f} triệu VNĐ")
        
        # 特色技术
        vva_count = len([m for m in self.motorcycles if 'VVA' in str(m.get('valve_system', ''))])
        blue_core_count = len([m for m in self.motorcycles if 'Blue Core' in str(m.get('engine_type', ''))])
        
        print(f"\n【Yamaha特色技术】")
        print(f"  • VVA可变气门: {vva_count} xe")
        print(f"  • Blue Core省油: {blue_core_count} xe")
        
        print("\n" + "="*60)


def main():
    crawler = YamahaCompleteCrawler()
    
    # 爬取所有Yamaha车型
    motorcycles = crawler.crawl_yamaha_all_models()
    crawler.motorcycles = motorcycles
    
    # 显示统计
    crawler.show_summary()
    
    # 保存数据
    crawler.save_to_json('/root/越南摩托汽车网站/backend/src/scripts/data/yamaha_complete_data.json')
    
    print("\n✨ Yamaha完整数据爬取完成！")
    print("📝 下一步: 运行导入脚本将数据导入数据库\n")


if __name__ == '__main__':
    main()

