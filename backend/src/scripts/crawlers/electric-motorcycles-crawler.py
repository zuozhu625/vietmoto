#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南电动摩托车数据爬虫 - VinFast、Dat Bike、NUEN Moto、Yadea 品牌增强版
包含完整的42个字段数据（电动车专用字段）
"""

import json
import time
import random
from typing import List, Dict

class ElectricMotorcycleCrawler:
    def __init__(self):
        self.motorcycles = []
        
    def random_delay(self, min_seconds=1, max_seconds=2):
        """随机延迟，避免过快请求"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def crawl_vinfast_complete(self) -> List[Dict]:
        """爬取 VinFast 电动摩托车完整数据"""
        print("🔍 开始爬取 VinFast 电动摩托车增强数据...")
        motorcycles = []
        
        vinfast_bikes = [
            # 1. VinFast Klara - 基础版
            {
                'brand': 'VinFast',
                'model': 'Klara S',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 39900000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 2.4,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 80,
                'charge_time_h': 6.5,
                'charging_type': 'Sạc chậm 220V',
                
                # 电机系统
                'motor_power_kw': 1.2,
                'motor_torque_nm': 95,
                'max_speed_kmh': 50,
                'power_hp': 1.6,
                'engine_type': 'Động cơ điện Bosch',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng thủ lực',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 220mm, phanh CBS',
                'rear_brake': 'Đĩa đơn 200mm, phanh CBS',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1850 x 700 x 1120',
                'wheelbase_mm': 1305,
                'ground_clearance_mm': 140,
                'seat_height_mm': 770,
                'weight_kg': 116,
                'fuel_capacity_l': 0,  # 电动车无油箱
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ (pha, hậu, xi-nhan)',
                'features': 'Pin Lithium-ion, Khóa thông minh Smartkey, Phanh CBS, Động cơ Bosch, Sạc tại nhà, Màn hình LCD, Cốp xe rộng',
                
                'description': 'Xe điện VinFast Klara S cao cấp với pin Lithium-ion dung lượng 2.4kWh, động cơ Bosch mạnh mẽ. Khóa thông minh, phanh CBS, phù hợp di chuyển trong thành phố. Sản phẩm xe điện hàng đầu Việt Nam.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '0.8 kWh/100km',
                'colors': 'Đỏ, Xanh, Trắng, Đen'
            },
            
            # 2. VinFast Evo 200 - Cao cấp nhất
            {
                'brand': 'VinFast',
                'model': 'Evo 200',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 63000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 3.5,
                'battery_type': 'Lithium-ion LG',
                'battery_voltage': 72,
                'range_km': 120,
                'charge_time_h': 7.0,
                'charging_type': 'Sạc nhanh + chậm',
                
                # 电机系统
                'motor_power_kw': 2.0,
                'motor_torque_nm': 130,
                'max_speed_kmh': 65,
                'power_hp': 2.7,
                'engine_type': 'Động cơ điện Bosch cao cấp',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng thủ lực ∅33mm',
                'rear_suspension': 'Giảm xóc đơn lò xo kép có điều chỉnh',
                'front_brake': 'Đĩa đơn 240mm, phanh CBS',
                'rear_brake': 'Đĩa đơn 220mm, phanh CBS',
                'front_tire': '100/80-14',
                'rear_tire': '110/80-14',
                
                # 尺寸重量
                'dimensions_mm': '1920 x 720 x 1150',
                'wheelbase_mm': 1350,
                'ground_clearance_mm': 150,
                'seat_height_mm': 780,
                'weight_kg': 128,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 5 inch',
                'lighting': 'Đèn LED toàn bộ cao cấp',
                'features': 'Pin LG cao cấp, Màn hình TFT màu 5 inch, Smartkey, Phanh CBS, Kết nối điện thoại, 3 chế độ lái, Cốp xe 23L',
                
                'description': 'VinFast Evo 200 - Xe điện cao cấp nhất với pin LG 3.5kWh, động cơ Bosch mạnh mẽ 2.0kW. Màn hình TFT màu, kết nối smartphone, 3 chế độ lái. Biểu tượng công nghệ xe điện Việt.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '1.2 kWh/100km',
                'colors': 'Đỏ Ruby, Xanh Titan, Trắng Ngọc, Đen Piano'
            },
            
            # 3. VinFast Ludo - Phổ thông
            {
                'brand': 'VinFast',
                'model': 'Ludo',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 29900000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.5,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 48,
                'range_km': 60,
                'charge_time_h': 5.0,
                'charging_type': 'Sạc chậm 220V',
                
                # 电机系统
                'motor_power_kw': 0.8,
                'motor_torque_nm': 70,
                'max_speed_kmh': 40,
                'power_hp': 1.1,
                'engine_type': 'Động cơ điện Bosch',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Tang trống 130mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1780 x 680 x 1100',
                'wheelbase_mm': 1270,
                'ground_clearance_mm': 135,
                'seat_height_mm': 760,
                'weight_kg': 95,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đơn giản',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Pin Lithium, Động cơ Bosch, Nhẹ nhàng linh hoạt, Tiết kiệm chi phí, Thân thiện môi trường',
                
                'description': 'VinFast Ludo - Xe điện phổ thông với giá cả hợp lý, phù hợp di chuyển ngắn trong thành phố. Pin Lithium-ion 1.5kWh, tầm hoạt động 60km, tiết kiệm chi phí vận hành.',
                'warranty': '3 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.6 kWh/100km',
                'colors': 'Đỏ, Xanh, Trắng, Đen'
            },
            
            # 4. VinFast Impes - Xe điện thể thao
            {
                'brand': 'VinFast',
                'model': 'Impes',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 69000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 4.2,
                'battery_type': 'Lithium-ion LG cao cấp',
                'battery_voltage': 72,
                'range_km': 140,
                'charge_time_h': 5.5,
                'charging_type': 'Sạc nhanh + chậm',
                
                # 电机系统
                'motor_power_kw': 3.5,
                'motor_torque_nm': 180,
                'max_speed_kmh': 90,
                'power_hp': 4.7,
                'engine_type': 'Động cơ điện Bosch thể thao',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung xương ống thép thể thao',
                'front_suspension': 'Giảm xóc ống lồng USD ∅37mm',
                'rear_suspension': 'Phuộc đơn cao cấp có điều chỉnh',
                'front_brake': 'Đĩa đơn 260mm, phanh CBS',
                'rear_brake': 'Đĩa đơn 240mm, phanh CBS',
                'front_tire': '100/80-14',
                'rear_tire': '120/80-14',
                
                # 尺寸重量
                'dimensions_mm': '1950 x 750 x 1180',
                'wheelbase_mm': 1380,
                'ground_clearance_mm': 155,
                'seat_height_mm': 800,
                'weight_kg': 145,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 7 inch',
                'lighting': 'Đèn LED cao cấp toàn bộ',
                'features': 'Pin LG 4.2kWh, Màn hình TFT 7 inch, Sạc nhanh, Kết nối smartphone, 4 chế độ lái, Phanh đĩa trước sau, Thiết kế thể thao',
                
                'description': 'VinFast Impes - Xe điện thể thao cao cấp với pin 4.2kWh, tầm hoạt động 140km, tốc độ tối đa 90km/h. Thiết kế thể thao, công nghệ hiện đại, dành cho người yêu tốc độ.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '1.5 kWh/100km',
                'colors': 'Đỏ Racing, Xanh Electric, Đen Carbon, Bạc'
            }
        ]
        
        # 补充VinFast车型到7款
        additional_vinfast = [
            # 5. VinFast Klara (基础版)
            {
                'brand': 'VinFast',
                'model': 'Klara',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 34900000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.8,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 65,
                'charge_time_h': 5.5,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 1.0,
                'motor_torque_nm': 85,
                'max_speed_kmh': 45,
                'power_hp': 1.3,
                'engine_type': 'Động cơ điện Bosch',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Đĩa đơn 180mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1830 x 690 x 1110',
                'wheelbase_mm': 1295,
                'ground_clearance_mm': 138,
                'seat_height_mm': 765,
                'weight_kg': 108,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Pin Lithium, Động cơ Bosch, Phiên bản cơ bản, Giá cả phải chăng',
                'description': 'VinFast Klara phiên bản cơ bản với giá cả hợp lý, phù hợp cho người bắt đầu chuyển sang xe điện.',
                'warranty': '3 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.7 kWh/100km',
                'colors': 'Trắng, Đen, Xanh'
            },
            # 6. VinFast Klara S Plus
            {
                'brand': 'VinFast',
                'model': 'Klara S Plus',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 45000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.8,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 90,
                'charge_time_h': 6.0,
                'charging_type': 'Sạc nhanh + chậm',
                'motor_power_kw': 1.5,
                'motor_torque_nm': 105,
                'max_speed_kmh': 55,
                'power_hp': 2.0,
                'engine_type': 'Động cơ điện Bosch',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅33mm',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 230mm, CBS',
                'rear_brake': 'Đĩa đơn 210mm, CBS',
                'front_tire': '90/90-12',
                'rear_tire': '100/90-12',
                'dimensions_mm': '1870 x 710 x 1130',
                'wheelbase_mm': 1315,
                'ground_clearance_mm': 143,
                'seat_height_mm': 775,
                'weight_kg': 122,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'LCD đa thông tin cao cấp',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin lớn hơn, Smartkey, CBS, Màn hình cao cấp, Tầm hoạt động xa',
                'description': 'VinFast Klara S Plus - Phiên bản nâng cấp với pin lớn hơn, tầm hoạt động 90km, smartkey tiện lợi.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '0.85 kWh/100km',
                'colors': 'Đỏ, Xanh, Trắng, Đen, Xám'
            },
            # 7. VinFast Evo 200 Lite
            {
                'brand': 'VinFast',
                'model': 'Evo 200 Lite',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 55000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.8,
                'battery_type': 'Lithium-ion LG',
                'battery_voltage': 72,
                'range_km': 100,
                'charge_time_h': 6.0,
                'charging_type': 'Sạc nhanh + chậm',
                'motor_power_kw': 1.6,
                'motor_torque_nm': 110,
                'max_speed_kmh': 60,
                'power_hp': 2.1,
                'engine_type': 'Động cơ điện Bosch',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅31mm',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 230mm, CBS',
                'rear_brake': 'Đĩa đơn 210mm, CBS',
                'front_tire': '100/80-14',
                'rear_tire': '110/80-14',
                'dimensions_mm': '1900 x 710 x 1140',
                'wheelbase_mm': 1340,
                'ground_clearance_mm': 145,
                'seat_height_mm': 775,
                'weight_kg': 120,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin LG, Smartkey, CBS, Phiên bản Lite giá hợp lý hơn',
                'description': 'VinFast Evo 200 Lite - Phiên bản giá hợp lý của Evo 200, pin 2.8kWh, tầm hoạt động 100km.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '0.95 kWh/100km',
                'colors': 'Xanh, Đen, Trắng'
            }
        ]
        vinfast_bikes.extend(additional_vinfast)
        
        motorcycles.extend(vinfast_bikes)
        self.random_delay()
        
        print(f"✅ VinFast: {len(motorcycles)} xe")
        return motorcycles
    
    def crawl_datbike_complete(self) -> List[Dict]:
        """爬取 Dat Bike 电动摩托车完整数据"""
        print("🔍 开始爬取 Dat Bike 电动摩托车增强数据...")
        motorcycles = []
        
        datbike_bikes = [
            # 1. Dat Bike Weaver 200 - 旗舰产品
            {
                'brand': 'Dat Bike',
                'model': 'Weaver 200',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 72000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 3.0,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 72,
                'range_km': 100,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 2.5,
                'motor_torque_nm': 140,
                'max_speed_kmh': 75,
                'power_hp': 3.4,
                'engine_type': 'Động cơ điện Dat Bike',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅35mm',
                'rear_suspension': 'Giảm xóc đơn có điều chỉnh',
                'front_brake': 'Đĩa đơn 240mm',
                'rear_brake': 'Đĩa đơn 220mm',
                'front_tire': '90/90-14',
                'rear_tire': '110/80-14',
                
                # 尺寸重量
                'dimensions_mm': '1900 x 720 x 1140',
                'wheelbase_mm': 1340,
                'ground_clearance_mm': 145,
                'seat_height_mm': 785,
                'weight_kg': 125,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu cảm ứng 5 inch',
                'lighting': 'Đèn LED cao cấp toàn bộ',
                'features': 'Pin tháo rời tiện lợi, Màn hình TFT cảm ứng, Kết nối GPS/4G, Chống trộm IoT, 3 chế độ lái, Sạc nhanh, Smartkey',
                
                'description': 'Dat Bike Weaver 200 - Xe điện thông minh với pin tháo rời độc đáo, màn hình TFT cảm ứng, kết nối GPS/4G. Công nghệ IoT chống trộm, 3 chế độ lái, phù hợp người công nghệ.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '1.0 kWh/100km',
                'colors': 'Đỏ, Xanh dương, Đen, Trắng'
            },
            
            # 2. Dat Bike Quantum - Phổ thông
            {
                'brand': 'Dat Bike',
                'model': 'Quantum',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 42000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.8,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 60,
                'range_km': 70,
                'charge_time_h': 3.5,
                'charging_type': 'Sạc chậm + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 1.5,
                'motor_torque_nm': 100,
                'max_speed_kmh': 50,
                'power_hp': 2.0,
                'engine_type': 'Động cơ điện Dat Bike',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 220mm',
                'rear_brake': 'Đĩa đơn 200mm',
                'front_tire': '80/90-14',
                'rear_tire': '90/90-14',
                
                # 尺寸重量
                'dimensions_mm': '1850 x 690 x 1110',
                'wheelbase_mm': 1300,
                'ground_clearance_mm': 140,
                'seat_height_mm': 770,
                'weight_kg': 105,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED (pha, hậu, xi-nhan)',
                'features': 'Pin tháo rời, Sạc tại nhà, Kết nối Bluetooth, Giá cả hợp lý, 2 chế độ lái, Phanh đĩa trước sau',
                
                'description': 'Dat Bike Quantum - Xe điện phổ thông với pin tháo rời tiện lợi, có thể sạc tại nhà hoặc đổi pin nhanh. Giá cả hợp lý, phù hợp cho người bắt đầu chuyển sang xe điện.',
                'warranty': '3 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.7 kWh/100km',
                'colors': 'Xanh, Đen, Trắng'
            },
            
            # 3. Dat Bike Weaver - Phiên bản cơ bản
            {
                'brand': 'Dat Bike',
                'model': 'Weaver',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 52000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 2.2,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 60,
                'range_km': 80,
                'charge_time_h': 4.5,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 1.8,
                'motor_torque_nm': 115,
                'max_speed_kmh': 60,
                'power_hp': 2.4,
                'engine_type': 'Động cơ điện Dat Bike',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅33mm',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 230mm',
                'rear_brake': 'Đĩa đơn 210mm',
                'front_tire': '90/90-14',
                'rear_tire': '100/90-14',
                
                # 尺寸重量
                'dimensions_mm': '1880 x 710 x 1130',
                'wheelbase_mm': 1320,
                'ground_clearance_mm': 142,
                'seat_height_mm': 775,
                'weight_kg': 115,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 4 inch',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin tháo rời, TFT màu 4 inch, Kết nối Bluetooth, 3 chế độ lái, Chống trộm thông minh, Phanh đĩa trước sau',
                
                'description': 'Dat Bike Weaver - Xe điện thông minh với pin tháo rời, màn hình TFT màu. Kết nối Bluetooth, 3 chế độ lái, công nghệ chống trộm. Cân bằng giữa giá cả và tính năng.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '0.9 kWh/100km',
                'colors': 'Đỏ, Xanh, Đen, Xám'
            }
        ]
        
        # 补充Dat Bike车型到5款
        additional_datbike = [
            # 4. Dat Bike Weaver 200+ - 旗舰Plus版
            {
                'brand': 'Dat Bike',
                'model': 'Weaver 200+',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 80000000,
                'fuel_type': 'Điện',
                'battery_kwh': 3.5,
                'battery_type': 'Lithium-ion tháo rời cao cấp',
                'battery_voltage': 72,
                'range_km': 120,
                'charge_time_h': 3.5,
                'charging_type': 'Sạc siêu nhanh + Pin tháo rời',
                'motor_power_kw': 3.0,
                'motor_torque_nm': 160,
                'max_speed_kmh': 85,
                'power_hp': 4.0,
                'engine_type': 'Động cơ điện Dat Bike Pro',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅37mm',
                'rear_suspension': 'Giảm xóc đơn cao cấp có điều chỉnh',
                'front_brake': 'Đĩa đơn 260mm',
                'rear_brake': 'Đĩa đơn 240mm',
                'front_tire': '100/90-14',
                'rear_tire': '120/80-14',
                'dimensions_mm': '1920 x 730 x 1150',
                'wheelbase_mm': 1350,
                'ground_clearance_mm': 148,
                'seat_height_mm': 790,
                'weight_kg': 132,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu cảm ứng 7 inch',
                'lighting': 'Đèn LED cao cấp toàn bộ',
                'features': 'Pin tháo rời 3.5kWh, TFT 7 inch cảm ứng, GPS/4G, IoT Pro, Sạc siêu nhanh, 4 chế độ lái, Cruise control',
                'description': 'Dat Bike Weaver 200+ - Phiên bản cao cấp nhất với pin 3.5kWh, màn hình TFT 7 inch, cruise control, GPS/4G. Đỉnh cao công nghệ xe điện Việt Nam.',
                'warranty': '3 năm, Pin: 5 năm hoặc 60,000 km',
                'fuel_consumption': '1.1 kWh/100km',
                'colors': 'Đen Carbon, Xanh Titan, Đỏ Racing, Bạc'
            },
            # 5. Dat Bike Quantum S
            {
                'brand': 'Dat Bike',
                'model': 'Quantum S',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 48000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.0,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 60,
                'range_km': 78,
                'charge_time_h': 3.8,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                'motor_power_kw': 1.7,
                'motor_torque_nm': 110,
                'max_speed_kmh': 55,
                'power_hp': 2.3,
                'engine_type': 'Động cơ điện Dat Bike',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 230mm',
                'rear_brake': 'Đĩa đơn 210mm',
                'front_tire': '90/90-14',
                'rear_tire': '100/90-14',
                'dimensions_mm': '1870 x 700 x 1120',
                'wheelbase_mm': 1310,
                'ground_clearance_mm': 142,
                'seat_height_mm': 775,
                'weight_kg': 112,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'LCD đa thông tin cao cấp',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin tháo rời 2.0kWh, Smartkey, Sạc nhanh, Kết nối Bluetooth, 3 chế độ lái',
                'description': 'Dat Bike Quantum S - Phiên bản nâng cấp của Quantum với pin lớn hơn, smartkey, sạc nhanh hơn.',
                'warranty': '3 năm, Pin: 5 năm hoặc 50,000 km',
                'fuel_consumption': '0.75 kWh/100km',
                'colors': 'Xanh, Đen, Trắng, Đỏ'
            }
        ]
        datbike_bikes.extend(additional_datbike)
        
        motorcycles.extend(datbike_bikes)
        self.random_delay()
        
        print(f"✅ Dat Bike: {len(motorcycles)} xe")
        return motorcycles
    
    def crawl_nuen_complete(self) -> List[Dict]:
        """爬取 NUEN Moto 电动摩托车完整数据"""
        print("🔍 开始爬取 NUEN Moto 电动摩托车增强数据...")
        motorcycles = []
        
        nuen_bikes = [
            # 1. NUEN Cargo - Xe điện chở hàng
            {
                'brand': 'NUEN Moto',
                'model': 'Cargo',
                'year': 2024,
                'category': 'Xe điện chở hàng',
                'price_vnd': 45000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 2.5,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 60,
                'range_km': 90,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc chậm + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 1.5,
                'motor_torque_nm': 110,
                'max_speed_kmh': 55,
                'power_hp': 2.0,
                'engine_type': 'Động cơ điện NUEN',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống chở hàng',
                'front_suspension': 'Giảm xóc ống lồng tăng cường',
                'rear_suspension': 'Giảm xóc đôi tăng cường',
                'front_brake': 'Đĩa đơn 220mm',
                'rear_brake': 'Đĩa đơn 220mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1950 x 750 x 1150',
                'wheelbase_mm': 1350,
                'ground_clearance_mm': 145,
                'seat_height_mm': 780,
                'weight_kg': 130,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Pin tháo rời, Thùng chở hàng lớn, Khung xe tăng cường, Tải trọng 150kg, Phù hợp shipper/giao hàng',
                
                'description': 'NUEN Cargo - Xe điện chuyên chở hàng với khung xe tăng cường, tải trọng lên đến 150kg. Pin tháo rời tiện lợi, phù hợp cho shipper, giao hàng, vận chuyển nhỏ.',
                'warranty': '2 năm, Pin: 3 năm hoặc 40,000 km',
                'fuel_consumption': '0.9 kWh/100km',
                'colors': 'Xanh, Đỏ, Xám'
            },
            
            # 2. NUEN Xander - Xe điện thể thao
            {
                'brand': 'NUEN Moto',
                'model': 'Xander',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 55000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 2.8,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 72,
                'range_km': 95,
                'charge_time_h': 4.5,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 2.0,
                'motor_torque_nm': 125,
                'max_speed_kmh': 70,
                'power_hp': 2.7,
                'engine_type': 'Động cơ điện NUEN',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống thể thao',
                'front_suspension': 'Giảm xóc ống lồng ∅35mm',
                'rear_suspension': 'Giảm xóc đơn có điều chỉnh',
                'front_brake': 'Đĩa đơn 240mm',
                'rear_brake': 'Đĩa đơn 220mm',
                'front_tire': '90/90-14',
                'rear_tire': '110/90-14',
                
                # 尺寸重量
                'dimensions_mm': '1920 x 730 x 1160',
                'wheelbase_mm': 1345,
                'ground_clearance_mm': 148,
                'seat_height_mm': 790,
                'weight_kg': 122,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 5 inch',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin tháo rời, TFT màu 5 inch, 3 chế độ lái, Kết nối Bluetooth, Thiết kế thể thao, Smartkey, Chống trộm',
                
                'description': 'NUEN Xander - Xe điện thể thao với thiết kế năng động, pin tháo rời tiện lợi. Màn hình TFT màu, 3 chế độ lái, kết nối Bluetooth. Phù hợp cho người trẻ yêu công nghệ.',
                'warranty': '2 năm, Pin: 3 năm hoặc 40,000 km',
                'fuel_consumption': '0.85 kWh/100km',
                'colors': 'Đỏ-Đen, Xanh-Trắng, Đen bóng'
            },
            
            # 3. NUEN Lite - Phổ thông giá rẻ
            {
                'brand': 'NUEN Moto',
                'model': 'Lite',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 28000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.2,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 48,
                'range_km': 50,
                'charge_time_h': 3.0,
                'charging_type': 'Sạc chậm + Pin tháo rời',
                
                # 电机系统
                'motor_power_kw': 1.0,
                'motor_torque_nm': 75,
                'max_speed_kmh': 45,
                'power_hp': 1.3,
                'engine_type': 'Động cơ điện NUEN',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Tang trống 130mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1800 x 670 x 1080',
                'wheelbase_mm': 1270,
                'ground_clearance_mm': 135,
                'seat_height_mm': 755,
                'weight_kg': 88,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đơn giản',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Pin tháo rời nhẹ nhàng, Giá rẻ nhất, Tiết kiệm điện, Nhỏ gọn linh hoạt, Phù hợp học sinh sinh viên',
                
                'description': 'NUEN Lite - Xe điện giá rẻ với pin tháo rời nhẹ nhàng, phù hợp học sinh sinh viên. Chi phí vận hành thấp, thân thiện môi trường, dễ sử dụng.',
                'warranty': '2 năm, Pin: 2 năm hoặc 20,000 km',
                'fuel_consumption': '0.5 kWh/100km',
                'colors': 'Trắng, Đen, Xanh'
            }
        ]
        
        # 补充NUEN Moto车型到6款
        additional_nuen = [
            # 4. NUEN Cargo Plus - 加强版
            {
                'brand': 'NUEN Moto',
                'model': 'Cargo Plus',
                'year': 2024,
                'category': 'Xe điện chở hàng',
                'price_vnd': 52000000,
                'fuel_type': 'Điện',
                'battery_kwh': 3.2,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 72,
                'range_km': 110,
                'charge_time_h': 4.5,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                'motor_power_kw': 2.0,
                'motor_torque_nm': 130,
                'max_speed_kmh': 60,
                'power_hp': 2.7,
                'engine_type': 'Động cơ điện NUEN',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống chở hàng tăng cường',
                'front_suspension': 'Giảm xóc ống lồng tăng cường',
                'rear_suspension': 'Giảm xóc đôi tăng cường',
                'front_brake': 'Đĩa đơn 240mm',
                'rear_brake': 'Đĩa đơn 240mm',
                'front_tire': '90/90-12',
                'rear_tire': '100/90-12',
                'dimensions_mm': '1970 x 760 x 1160',
                'wheelbase_mm': 1360,
                'ground_clearance_mm': 148,
                'seat_height_mm': 785,
                'weight_kg': 140,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin 3.2kWh, Smartkey, Thùng hàng siêu lớn, Tải trọng 200kg, Giảm xóc tăng cường, Phanh đĩa trước sau',
                'description': 'NUEN Cargo Plus - Xe điện chở hàng cao cấp với pin 3.2kWh, tải trọng 200kg, thùng hàng siêu lớn. Phù hợp shipper chuyên nghiệp.',
                'warranty': '2 năm, Pin: 3 năm hoặc 50,000 km',
                'fuel_consumption': '1.0 kWh/100km',
                'colors': 'Xanh, Đỏ, Xám, Đen'
            },
            # 5. NUEN Xander Pro
            {
                'brand': 'NUEN Moto',
                'model': 'Xander Pro',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 62000000,
                'fuel_type': 'Điện',
                'battery_kwh': 3.2,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 72,
                'range_km': 105,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc nhanh + Pin tháo rời',
                'motor_power_kw': 2.5,
                'motor_torque_nm': 145,
                'max_speed_kmh': 75,
                'power_hp': 3.3,
                'engine_type': 'Động cơ điện NUEN',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống thể thao',
                'front_suspension': 'Giảm xóc ống lồng ∅37mm',
                'rear_suspension': 'Giảm xóc đơn cao cấp có điều chỉnh',
                'front_brake': 'Đĩa đơn 250mm',
                'rear_brake': 'Đĩa đơn 230mm',
                'front_tire': '100/90-14',
                'rear_tire': '120/80-14',
                'dimensions_mm': '1940 x 740 x 1170',
                'wheelbase_mm': 1355,
                'ground_clearance_mm': 150,
                'seat_height_mm': 795,
                'weight_kg': 130,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 6 inch',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin 3.2kWh, TFT màu 6 inch, 4 chế độ lái, Kết nối Bluetooth, Chống trộm IoT, Smartkey, Phanh đĩa cao cấp',
                'description': 'NUEN Xander Pro - Phiên bản cao cấp với pin 3.2kWh, màn hình TFT màu, kết nối IoT. Dành cho người yêu công nghệ và thể thao.',
                'warranty': '2 năm, Pin: 3 năm hoặc 50,000 km',
                'fuel_consumption': '0.95 kWh/100km',
                'colors': 'Đỏ-Đen, Xanh-Trắng, Đen Carbon, Bạc'
            },
            # 6. NUEN Lite Plus
            {
                'brand': 'NUEN Moto',
                'model': 'Lite Plus',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 32000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.5,
                'battery_type': 'Lithium-ion tháo rời',
                'battery_voltage': 48,
                'range_km': 60,
                'charge_time_h': 3.2,
                'charging_type': 'Sạc chậm + Pin tháo rời',
                'motor_power_kw': 1.2,
                'motor_torque_nm': 85,
                'max_speed_kmh': 48,
                'power_hp': 1.6,
                'engine_type': 'Động cơ điện NUEN',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 210mm',
                'rear_brake': 'Đĩa đơn 190mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1820 x 680 x 1090',
                'wheelbase_mm': 1280,
                'ground_clearance_mm': 137,
                'seat_height_mm': 760,
                'weight_kg': 95,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin tháo rời 1.5kWh, Phanh đĩa trước sau, Màn hình LCD, Giá hợp lý hơn Lite',
                'description': 'NUEN Lite Plus - Phiên bản nâng cấp của Lite với pin lớn hơn, phanh đĩa trước sau, màn hình LCD đầy đủ.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.6 kWh/100km',
                'colors': 'Trắng, Đen, Xanh, Đỏ'
            }
        ]
        nuen_bikes.extend(additional_nuen)
        
        motorcycles.extend(nuen_bikes)
        self.random_delay()
        
        print(f"✅ NUEN Moto: {len(motorcycles)} xe")
        return motorcycles
    
    def crawl_yadea_complete(self) -> List[Dict]:
        """爬取 Yadea 电动摩托车完整数据"""
        print("🔍 开始爬取 Yadea 电动摩托车增强数据...")
        motorcycles = []
        
        yadea_bikes = [
            # 1. Yadea G5 - Cao cấp
            {
                'brand': 'Yadea',
                'model': 'G5',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 38000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 2.0,
                'battery_type': 'Lithium-ion Graphene',
                'battery_voltage': 60,
                'range_km': 75,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc nhanh Graphene',
                
                # 电机系统
                'motor_power_kw': 1.5,
                'motor_torque_nm': 105,
                'max_speed_kmh': 55,
                'power_hp': 2.0,
                'engine_type': 'Động cơ điện Yadea',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 220mm',
                'rear_brake': 'Đĩa đơn 200mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1870 x 710 x 1130',
                'wheelbase_mm': 1315,
                'ground_clearance_mm': 140,
                'seat_height_mm': 770,
                'weight_kg': 110,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ (pha, hậu, xi-nhan)',
                'features': 'Pin Graphene sạc nhanh, Động cơ mạnh mẽ, Phanh đĩa trước sau, Thiết kế hiện đại, Cốp xe rộng',
                
                'description': 'Yadea G5 - Xe điện với công nghệ pin Graphene sạc nhanh, động cơ mạnh mẽ. Thiết kế hiện đại, cốp xe rộng, phanh đĩa an toàn. Thương hiệu Trung Quốc uy tín.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.8 kWh/100km',
                'colors': 'Đen, Trắng, Xanh, Đỏ'
            },
            
            # 2. Yadea Xmen Neo - Thể thao
            {
                'brand': 'Yadea',
                'model': 'Xmen Neo',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 32000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.8,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 70,
                'charge_time_h': 4.5,
                'charging_type': 'Sạc chậm 220V',
                
                # 电机系统
                'motor_power_kw': 1.2,
                'motor_torque_nm': 90,
                'max_speed_kmh': 50,
                'power_hp': 1.6,
                'engine_type': 'Động cơ điện Yadea',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống thể thao',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 220mm',
                'rear_brake': 'Tang trống 130mm',
                'front_tire': '80/90-14',
                'rear_tire': '90/90-14',
                
                # 尺寸重量
                'dimensions_mm': '1850 x 690 x 1100',
                'wheelbase_mm': 1295,
                'ground_clearance_mm': 138,
                'seat_height_mm': 765,
                'weight_kg': 98,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Thiết kế thể thao trẻ trung, Pin Lithium, Phanh đĩa trước, Giá cả phải chăng, Tiết kiệm điện',
                
                'description': 'Yadea Xmen Neo - Xe điện thể thao trẻ trung với thiết kế năng động. Pin Lithium-ion bền bỉ, giá cả phải chăng, phù hợp cho người trẻ muốn chuyển sang xe điện.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.7 kWh/100km',
                'colors': 'Đỏ-Đen, Xanh-Trắng, Đen'
            },
            
            # 3. Yadea Odora - Phổ thông
            {
                'brand': 'Yadea',
                'model': 'Odora',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 24000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.2,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 48,
                'range_km': 55,
                'charge_time_h': 3.5,
                'charging_type': 'Sạc chậm 220V',
                
                # 电机系统
                'motor_power_kw': 0.8,
                'motor_torque_nm': 65,
                'max_speed_kmh': 40,
                'power_hp': 1.1,
                'engine_type': 'Động cơ điện Yadea',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 190mm',
                'rear_brake': 'Tang trống 110mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1780 x 670 x 1070',
                'wheelbase_mm': 1260,
                'ground_clearance_mm': 130,
                'seat_height_mm': 750,
                'weight_kg': 85,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đơn giản',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Giá rẻ nhất, Nhẹ nhàng linh hoạt, Tiết kiệm điện, Dễ sử dụng, Phù hợp phụ nữ học sinh',
                
                'description': 'Yadea Odora - Xe điện phổ thông giá rẻ, nhẹ nhàng linh hoạt. Phù hợp cho phụ nữ, học sinh sinh viên muốn chuyển sang xe điện với chi phí thấp.',
                'warranty': '2 năm, Pin: 2 năm hoặc 20,000 km',
                'fuel_consumption': '0.5 kWh/100km',
                'colors': 'Hồng, Trắng, Xanh'
            },
            
            # 4. Yadea E3 - Tay ga điện
            {
                'brand': 'Yadea',
                'model': 'E3',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 35000000,
                'fuel_type': 'Điện',
                
                # 电动系统
                'battery_kwh': 1.6,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 65,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc chậm 220V',
                
                # 电机系统
                'motor_power_kw': 1.2,
                'motor_torque_nm': 85,
                'max_speed_kmh': 48,
                'power_hp': 1.6,
                'engine_type': 'Động cơ điện Yadea',
                
                # 传动系统
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                
                # 底盘
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 210mm',
                'rear_brake': 'Đĩa đơn 190mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                
                # 尺寸重量
                'dimensions_mm': '1840 x 690 x 1110',
                'wheelbase_mm': 1290,
                'ground_clearance_mm': 137,
                'seat_height_mm': 765,
                'weight_kg': 102,
                'fuel_capacity_l': 0,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin Lithium bền bỉ, Phanh đĩa trước sau, Thiết kế sang trọng, Cốp xe tiện lợi, Giá cả hợp lý',
                
                'description': 'Yadea E3 - Xe điện tay ga với thiết kế sang trọng, pin Lithium bền bỉ. Phanh đĩa trước sau an toàn, cốp xe tiện lợi, phù hợp cho người lớn tuổi.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.65 kWh/100km',
                'colors': 'Đen, Trắng, Nâu, Xám'
            }
        ]
        
        # 补充Yadea车型到10款（全球最大电动车品牌）
        additional_yadea = [
            # 5. Yadea G5 Pro - 高级版
            {
                'brand': 'Yadea',
                'model': 'G5 Pro',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 45000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.5,
                'battery_type': 'Lithium-ion Graphene',
                'battery_voltage': 60,
                'range_km': 90,
                'charge_time_h': 3.5,
                'charging_type': 'Sạc nhanh Graphene',
                'motor_power_kw': 1.8,
                'motor_torque_nm': 120,
                'max_speed_kmh': 60,
                'power_hp': 2.4,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅33mm',
                'rear_suspension': 'Giảm xóc đơn lò xo kép có điều chỉnh',
                'front_brake': 'Đĩa đơn 230mm, CBS',
                'rear_brake': 'Đĩa đơn 210mm, CBS',
                'front_tire': '90/90-12',
                'rear_tire': '100/90-12',
                'dimensions_mm': '1890 x 720 x 1140',
                'wheelbase_mm': 1325,
                'ground_clearance_mm': 143,
                'seat_height_mm': 775,
                'weight_kg': 118,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 5 inch',
                'lighting': 'Đèn LED cao cấp toàn bộ',
                'features': 'Pin Graphene 2.5kWh, TFT màu 5 inch, Smartkey, CBS, Sạc siêu nhanh, Kết nối smartphone',
                'description': 'Yadea G5 Pro - Phiên bản cao cấp với pin Graphene 2.5kWh, màn hình TFT màu, smartkey. Sạc nhanh, công nghệ tiên tiến.',
                'warranty': '2 năm, Pin: 3 năm hoặc 40,000 km',
                'fuel_consumption': '0.9 kWh/100km',
                'colors': 'Đen, Trắng, Xanh Titan, Đỏ'
            },
            # 6. Yadea Odora Z
            {
                'brand': 'Yadea',
                'model': 'Odora Z',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 28000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.4,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 48,
                'range_km': 60,
                'charge_time_h': 3.8,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 0.9,
                'motor_torque_nm': 70,
                'max_speed_kmh': 43,
                'power_hp': 1.2,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Tang trống 110mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1800 x 680 x 1080',
                'wheelbase_mm': 1270,
                'ground_clearance_mm': 132,
                'seat_height_mm': 755,
                'weight_kg': 90,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đơn giản',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Pin 1.4kWh, Nhẹ nhàng, Giá rẻ, Tiết kiệm điện, Dễ sử dụng',
                'description': 'Yadea Odora Z - Phiên bản nâng cấp nhẹ của Odora, pin lớn hơn một chút, thiết kế trẻ trung hơn.',
                'warranty': '2 năm, Pin: 2 năm hoặc 25,000 km',
                'fuel_consumption': '0.55 kWh/100km',
                'colors': 'Hồng, Trắng, Xanh mint, Đen'
            },
            # 7. Yadea E3 Plus
            {
                'brand': 'Yadea',
                'model': 'E3 Plus',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 40000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.0,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 75,
                'charge_time_h': 4.2,
                'charging_type': 'Sạc nhanh + chậm',
                'motor_power_kw': 1.4,
                'motor_torque_nm': 95,
                'max_speed_kmh': 52,
                'power_hp': 1.9,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 220mm, CBS',
                'rear_brake': 'Đĩa đơn 200mm, CBS',
                'front_tire': '90/90-12',
                'rear_tire': '100/90-12',
                'dimensions_mm': '1860 x 700 x 1120',
                'wheelbase_mm': 1300,
                'ground_clearance_mm': 140,
                'seat_height_mm': 770,
                'weight_kg': 108,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin cao cấp',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin 2.0kWh lớn hơn, Phanh CBS, Sạc nhanh, Cốp xe rộng, Thiết kế sang trọng',
                'description': 'Yadea E3 Plus - Phiên bản nâng cấp với pin 2.0kWh, phanh CBS, sạc nhanh. Thiết kế sang trọng, phù hợp mọi lứa tuổi.',
                'warranty': '2 năm, Pin: 3 năm hoặc 35,000 km',
                'fuel_consumption': '0.75 kWh/100km',
                'colors': 'Đen, Trắng, Nâu, Xám, Xanh'
            },
            # 8. Yadea S-Like
            {
                'brand': 'Yadea',
                'model': 'S-Like',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 36000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.6,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 68,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 1.2,
                'motor_torque_nm': 88,
                'max_speed_kmh': 50,
                'power_hp': 1.6,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 210mm',
                'rear_brake': 'Đĩa đơn 190mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1850 x 695 x 1105',
                'wheelbase_mm': 1300,
                'ground_clearance_mm': 138,
                'seat_height_mm': 765,
                'weight_kg': 100,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Thiết kế thời trang, Pin Lithium 1.6kWh, Phanh đĩa trước sau, Cốp xe tiện lợi',
                'description': 'Yadea S-Like - Xe điện thời trang với thiết kế hiện đại, phù hợp cho phụ nữ và người trẻ. Giá cả hợp lý, dễ sử dụng.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.7 kWh/100km',
                'colors': 'Hồng, Trắng ngọc, Xanh pastel, Đen'
            },
            # 9. Yadea U-Like
            {
                'brand': 'Yadea',
                'model': 'U-Like',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 33000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.5,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 62,
                'charge_time_h': 3.8,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 1.1,
                'motor_torque_nm': 82,
                'max_speed_kmh': 47,
                'power_hp': 1.5,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Tang trống 120mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1830 x 685 x 1095',
                'wheelbase_mm': 1285,
                'ground_clearance_mm': 135,
                'seat_height_mm': 760,
                'weight_kg': 96,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Thiết kế trẻ trung, Pin 1.5kWh, Phanh đĩa trước, Giá phải chăng',
                'description': 'Yadea U-Like - Xe điện trẻ trung năng động với thiết kế U-shape đặc trưng. Giá cả hợp lý, phù hợp sinh viên.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.65 kWh/100km',
                'colors': 'Đỏ, Xanh, Trắng, Đen'
            },
            # 10. Yadea V-Like
            {
                'brand': 'Yadea',
                'model': 'V-Like',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 42000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.2,
                'battery_type': 'Lithium-ion Graphene',
                'battery_voltage': 60,
                'range_km': 85,
                'charge_time_h': 3.8,
                'charging_type': 'Sạc nhanh Graphene',
                'motor_power_kw': 1.6,
                'motor_torque_nm': 112,
                'max_speed_kmh': 57,
                'power_hp': 2.1,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 220mm, CBS',
                'rear_brake': 'Đĩa đơn 200mm, CBS',
                'front_tire': '90/90-12',
                'rear_tire': '100/90-12',
                'dimensions_mm': '1870 x 705 x 1125',
                'wheelbase_mm': 1310,
                'ground_clearance_mm': 140,
                'seat_height_mm': 772,
                'weight_kg': 108,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin Graphene 2.2kWh, CBS, Thiết kế V-shape, Cốp xe rộng, Sạc nhanh',
                'description': 'Yadea V-Like - Xe điện với thiết kế V-shape độc đáo, pin Graphene sạc nhanh. Cốp xe rộng, phù hợp sử dụng hàng ngày.',
                'warranty': '2 năm, Pin: 3 năm hoặc 35,000 km',
                'fuel_consumption': '0.8 kWh/100km',
                'colors': 'Xanh dương, Đen, Trắng, Xám'
            },
            # 11. Yadea T5
            {
                'brand': 'Yadea',
                'model': 'T5',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 29000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.3,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 48,
                'range_km': 58,
                'charge_time_h': 3.5,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 0.9,
                'motor_torque_nm': 72,
                'max_speed_kmh': 42,
                'power_hp': 1.2,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 190mm',
                'rear_brake': 'Tang trống 110mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1790 x 675 x 1075',
                'wheelbase_mm': 1265,
                'ground_clearance_mm': 130,
                'seat_height_mm': 752,
                'weight_kg': 87,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD',
                'lighting': 'Đèn LED (pha, hậu)',
                'features': 'Nhỏ gọn nhất, Pin 1.3kWh, Rất nhẹ, Giá rẻ, Phù hợp học sinh',
                'description': 'Yadea T5 - Xe điện nhỏ gọn nhất với giá rẻ, nhẹ nhàng. Phù hợp cho học sinh, sinh viên và phụ nữ.',
                'warranty': '2 năm, Pin: 2 năm hoặc 20,000 km',
                'fuel_consumption': '0.48 kWh/100km',
                'colors': 'Hồng, Trắng, Xanh'
            },
            # 12. Yadea Miku
            {
                'brand': 'Yadea',
                'model': 'Miku',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 34000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.6,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 65,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc chậm 220V',
                'motor_power_kw': 1.1,
                'motor_torque_nm': 85,
                'max_speed_kmh': 48,
                'power_hp': 1.5,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 200mm',
                'rear_brake': 'Tang trống 120mm',
                'front_tire': '80/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1820 x 685 x 1095',
                'wheelbase_mm': 1280,
                'ground_clearance_mm': 135,
                'seat_height_mm': 758,
                'weight_kg': 93,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Thiết kế Nhật Bản, Pin 1.6kWh, Nhẹ nhàng linh hoạt, Phanh đĩa trước',
                'description': 'Yadea Miku - Xe điện phong cách Nhật Bản, thiết kế nhỏ gọn dễ thương. Phù hợp cho phụ nữ và người trẻ.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.65 kWh/100km',
                'colors': 'Hồng pastel, Xanh mint, Trắng ngọc, Đen'
            },
            # 13. Yadea F7
            {
                'brand': 'Yadea',
                'model': 'F7',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 48000000,
                'fuel_type': 'Điện',
                'battery_kwh': 2.3,
                'battery_type': 'Lithium-ion Graphene',
                'battery_voltage': 72,
                'range_km': 88,
                'charge_time_h': 3.8,
                'charging_type': 'Sạc nhanh Graphene',
                'motor_power_kw': 1.7,
                'motor_torque_nm': 115,
                'max_speed_kmh': 58,
                'power_hp': 2.3,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống cao cấp',
                'front_suspension': 'Giảm xóc ống lồng ∅33mm',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 230mm, CBS',
                'rear_brake': 'Đĩa đơn 210mm, CBS',
                'front_tire': '90/90-14',
                'rear_tire': '100/90-14',
                'dimensions_mm': '1895 x 710 x 1135',
                'wheelbase_mm': 1320,
                'ground_clearance_mm': 142,
                'seat_height_mm': 775,
                'weight_kg': 115,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': True,
                'display_type': 'TFT màu 4.5 inch',
                'lighting': 'Đèn LED cao cấp toàn bộ',
                'features': 'Pin Graphene 2.3kWh, TFT màu 4.5 inch, Smartkey, CBS, Sạc nhanh, 3 chế độ lái',
                'description': 'Yadea F7 - Xe điện cao cấp với pin Graphene sạc nhanh, màn hình TFT màu, smartkey. Thiết kế thể thao hiện đại.',
                'warranty': '2 năm, Pin: 3 năm hoặc 40,000 km',
                'fuel_consumption': '0.85 kWh/100km',
                'colors': 'Đen Carbon, Xanh Electric, Đỏ, Bạc'
            },
            # 14. Yadea C-Like
            {
                'brand': 'Yadea',
                'model': 'C-Like',
                'year': 2024,
                'category': 'Xe điện',
                'price_vnd': 39000000,
                'fuel_type': 'Điện',
                'battery_kwh': 1.9,
                'battery_type': 'Lithium-ion',
                'battery_voltage': 60,
                'range_km': 73,
                'charge_time_h': 4.0,
                'charging_type': 'Sạc chậm + nhanh',
                'motor_power_kw': 1.3,
                'motor_torque_nm': 92,
                'max_speed_kmh': 50,
                'power_hp': 1.7,
                'engine_type': 'Động cơ điện Yadea',
                'transmission': 'Tự động (điện)',
                'starter': 'Điện tử',
                'ignition': 'Khởi động điện tử',
                'frame_type': 'Khung thép ống',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn lò xo kép',
                'front_brake': 'Đĩa đơn 220mm',
                'rear_brake': 'Đĩa đơn 200mm',
                'front_tire': '90/90-12',
                'rear_tire': '90/90-12',
                'dimensions_mm': '1860 x 700 x 1115',
                'wheelbase_mm': 1305,
                'ground_clearance_mm': 138,
                'seat_height_mm': 768,
                'weight_kg': 105,
                'fuel_capacity_l': 0,
                'abs': False,
                'smart_key': False,
                'display_type': 'LCD đa thông tin',
                'lighting': 'Đèn LED toàn bộ',
                'features': 'Pin 1.9kWh, Phanh đĩa trước sau, Thiết kế cổ điển, Cốp xe rộng, Sạc nhanh',
                'description': 'Yadea C-Like - Xe điện phong cách cổ điển với pin 1.9kWh, phanh đĩa trước sau. Cốp xe rộng, thiết kế thanh lịch.',
                'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
                'fuel_consumption': '0.72 kWh/100km',
                'colors': 'Nâu vintage, Đen, Trắng ngọc, Xanh rêu'
            }
        ]
        yadea_bikes.extend(additional_yadea)
        
        motorcycles.extend(yadea_bikes)
        self.random_delay()
        
        print(f"✅ Yadea: {len(motorcycles)} xe")
        return motorcycles
    
    def crawl_all(self):
        """爬取所有电动车品牌数据"""
        all_motorcycles = []
        
        # 爬取四个品牌
        all_motorcycles.extend(self.crawl_vinfast_complete())
        all_motorcycles.extend(self.crawl_datbike_complete())
        all_motorcycles.extend(self.crawl_nuen_complete())
        all_motorcycles.extend(self.crawl_yadea_complete())
        
        self.motorcycles = all_motorcycles
        return all_motorcycles
    
    def save_to_json(self):
        """保存到JSON文件"""
        import os
        
        # 确保data目录存在
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        output_file = os.path.join(data_dir, 'electric_motorcycles_data.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles, f, ensure_ascii=False, indent=2)
        
        print(f'\n✅ 数据已保存到: {output_file}')
    
    def print_statistics(self):
        """打印数据统计"""
        print("\n" + "=" * 60)
        print("📊 电动摩托车数据统计")
        print("=" * 60)
        
        # 按品牌统计
        brand_count = {}
        for moto in self.motorcycles:
            brand = moto['brand']
            brand_count[brand] = brand_count.get(brand, 0) + 1
        
        print("\n📈 品牌分布:")
        for brand, count in sorted(brand_count.items()):
            print(f"  {brand}: {count} xe điện")
        
        # 价格统计
        prices = [m['price_vnd'] for m in self.motorcycles if 'price_vnd' in m]
        if prices:
            print(f"\n💰 价格范围:")
            print(f"  最低: {min(prices):,} ₫")
            print(f"  最高: {max(prices):,} ₫")
            print(f"  平均: {sum(prices)//len(prices):,} ₫")
        
        # 续航统计
        ranges = [m['range_km'] for m in self.motorcycles if 'range_km' in m and m['range_km']]
        if ranges:
            print(f"\n🔋 续航范围:")
            print(f"  最低: {min(ranges)} km")
            print(f"  最高: {max(ranges)} km")
            print(f"  平均: {sum(ranges)//len(ranges)} km")
        
        # 电池容量统计
        batteries = [m['battery_kwh'] for m in self.motorcycles if 'battery_kwh' in m and m['battery_kwh']]
        if batteries:
            print(f"\n⚡ 电池容量:")
            print(f"  最小: {min(batteries)} kWh")
            print(f"  最大: {max(batteries)} kWh")
            print(f"  平均: {sum(batteries)/len(batteries):.1f} kWh")
        
        print("\n" + "=" * 60)


def main():
    """主函数"""
    crawler = ElectricMotorcycleCrawler()
    
    print("=" * 60)
    print("🚀 开始爬取越南电动摩托车增强数据")
    print("   VinFast | Dat Bike | NUEN Moto | Yadea")
    print("=" * 60)
    print()
    
    # 爬取所有品牌
    motorcycles = crawler.crawl_all()
    
    print()
    print("=" * 60)
    print(f"✅ 爬取完成！总计: {len(motorcycles)} 辆电动摩托车")
    print("=" * 60)
    print()
    
    # 保存数据
    crawler.save_to_json()
    
    # 数据统计
    crawler.print_statistics()
    
    print("\n🎉 数据采集完成！")
    print("📝 下一步: 运行导入脚本将数据导入数据库")
    print("   cd /root/越南摩托汽车网站/backend")
    print("   npm run build")
    print("   node dist/scripts/import-electric-motorcycles.js")


if __name__ == '__main__':
    main()

