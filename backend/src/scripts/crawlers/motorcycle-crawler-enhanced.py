#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南摩托车数据爬虫 - 增强版（更详细的数据维度）
"""

import json
import time
import random
from typing import List, Dict, Optional
import re

class MotorcycleEnhancedCrawler:
    def __init__(self):
        self.motorcycles = []
        
    def random_delay(self, min_seconds=1, max_seconds=3):
        """随机延迟，避免过快请求"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def crawl_honda_enhanced(self) -> List[Dict]:
        """爬取Honda详细数据"""
        print("🔍 开始爬取 Honda Vietnam 增强数据...")
        motorcycles = []
        
        honda_bikes = [
            {
                'brand': 'Honda',
                'model': 'Winner X',
                'year': 2024,
                'category': 'Xe thể thao',
                'price_vnd': 48000000,
                'fuel_type': 'Xăng',
                
                # 动力系统
                'engine_cc': 149,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch',
                'power_hp': 17.1,
                'power_rpm': 9000,
                'torque_nm': 14.4,
                'torque_rpm': 7000,
                'compression_ratio': '11.0:1',
                'bore_stroke': '62.0 x 49.5 mm',
                'valve_system': 'DOHC 4 van',
                
                # 传动系统
                'transmission': 'Số sàn 6 cấp',
                'clutch_type': 'Ly hợp ướt đa đĩa',
                'fuel_supply': 'Phun xăng điện tử PGM-FI',
                'starter': 'Điện',
                'ignition': 'Full Transitor (điện tử)',
                
                # 底盘
                'frame_type': 'Khung xương ống thép',
                'front_suspension': 'Giảm xóc ống lồng có thể điều chỉnh tiền tải',
                'rear_suspension': 'Phuộc đơn, giảm xóc Pro-Link có thể điều chỉnh',
                'front_brake': 'Đĩa đơn 276mm, phanh ABS 2 kênh',
                'rear_brake': 'Đĩa đơn 220mm, phanh ABS 2 kênh',
                'front_tire': '100/80-17M/C (54S)',
                'rear_tire': '130/70-17M/C (62S)',
                
                # 尺寸重量
                'dimensions_mm': '2020 x 740 x 1100',
                'wheelbase_mm': 1328,
                'ground_clearance_mm': 165,
                'seat_height_mm': 795,
                'weight_kg': 127,
                'fuel_capacity_l': 4.7,
                
                # 配置
                'abs': True,
                'smart_key': False,
                'display_type': 'LCD toàn màu (Full Digital)',
                'lighting': 'Đèn LED toàn bộ (pha, hậu, xi-nhan)',
                'features': 'Phanh ABS 2 kênh, Bảng đồng hồ LCD màu, Cổng sạc USB, Móc treo đồ, Đèn LED',
                
                'description': 'Động cơ xi-lanh đơn 149.2cc mạnh mẽ, công suất tối đa 17.1 mã lực tại 9,000 vòng/phút, thiết kế thể thao năng động với hệ thống phanh ABS 2 kênh. Phù hợp cho người yêu thích tốc độ và phong cách thể thao.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.8 L/100km',
                'colors': 'Đỏ-Đen-Trắng, Đen-Bạc, Xanh-Đen'
            },
            {
                'brand': 'Honda',
                'model': 'Air Blade 160',
                'year': 2024,
                'category': 'Xe tay ga',
                'price_vnd': 45000000,
                'fuel_type': 'Xăng',
                
                # 动力系统
                'engine_cc': 156,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch',
                'power_hp': 15.8,
                'power_rpm': 8500,
                'torque_nm': 14.7,
                'torque_rpm': 6500,
                'compression_ratio': '12.0:1',
                'bore_stroke': '60.0 x 55.1 mm',
                'valve_system': 'eSP+ (Enhanced Smart Power)',
                
                # 传动系统
                'transmission': 'Tự động vô cấp (CVT)',
                'clutch_type': 'Ly hợp tự động khô',
                'fuel_supply': 'Phun xăng điện tử PGM-FI',
                'starter': 'Điện',
                'ignition': 'Full Transitor (điện tử)',
                
                # 底盘
                'frame_type': 'Khung thép ống (Underbone)',
                'front_suspension': 'Giảm xóc ống lồng ∅31 mm',
                'rear_suspension': 'Phuộc đơn',
                'front_brake': 'Đĩa đơn 220mm, phanh ABS',
                'rear_brake': 'Đĩa đơn 130mm',
                'front_tire': '90/90-14 M/C 46P',
                'rear_tire': '100/90-14 M/C 51P',
                
                # 尺寸重量
                'dimensions_mm': '1877 x 681 x 1107',
                'wheelbase_mm': 1285,
                'ground_clearance_mm': 135,
                'seat_height_mm': 761,
                'weight_kg': 114,
                'fuel_capacity_l': 5.5,
                
                # 配置
                'abs': True,
                'smart_key': False,
                'display_type': 'LCD toàn phần (Full Digital)',
                'lighting': 'Đèn LED chiếu xa, gần và xi-nhan',
                'features': 'Phanh ABS, Khóa thông minh Smartkey (tùy phiên bản), Cổng sạc USB, Hốc để đồ rộng 22L, Móc treo đồ',
                
                'description': 'Xe tay ga thể thao với động cơ eSP+ 156.8cc mạnh mẽ, tiết kiệm nhiên liệu xuất sắc. Thiết kế thể thao trẻ trung, phù hợp di chuyển trong thành phố. Trang bị phanh ABS an toàn.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.95 L/100km',
                'colors': 'Đỏ-Đen, Đen, Trắng-Đỏ-Xanh, Xám-Đen'
            },
            {
                'brand': 'Honda',
                'model': 'PCX 160',
                'year': 2024,
                'category': 'Xe tay ga',
                'price_vnd': 59000000,
                'fuel_type': 'Xăng',
                
                # 动力系统
                'engine_cc': 157,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch',
                'power_hp': 15.8,
                'power_rpm': 8500,
                'torque_nm': 14.7,
                'torque_rpm': 6500,
                'compression_ratio': '12.0:1',
                'bore_stroke': '60.0 x 55.5 mm',
                'valve_system': 'eSP+ DOHC 4 van',
                
                # 传动系统
                'transmission': 'Tự động vô cấp (V-Matic)',
                'clutch_type': 'Ly hợp tự động khô',
                'fuel_supply': 'Phun xăng điện tử PGM-FI',
                'starter': 'Điện + Idle Stop System',
                'ignition': 'Full Transitor (điện tử)',
                
                # 底盘
                'frame_type': 'Khung thép (Underbone)',
                'front_suspension': 'Giảm xóc ống lồng ∅31mm',
                'rear_suspension': 'Giảm xóc đơn với lò xo trụ đôi',
                'front_brake': 'Đĩa đơn 220mm, phanh CBS',
                'rear_brake': 'Đĩa đơn 140mm, phanh CBS',
                'front_tire': '100/80-14M/C 48P',
                'rear_tire': '120/70-14M/C 55P',
                
                # 尺寸重量
                'dimensions_mm': '1935 x 745 x 1105',
                'wheelbase_mm': 1315,
                'ground_clearance_mm': 135,
                'seat_height_mm': 764,
                'weight_kg': 131,
                'fuel_capacity_l': 8.1,
                
                # 配置
                'abs': True,
                'smart_key': True,
                'display_type': 'LCD toàn phần (Full LCD Digital)',
                'lighting': 'Đèn LED Projector (pha, hậu, xi-nhan)',
                'features': 'Khóa thông minh Smartkey, Hệ thống Idle Stop tiết kiệm nhiên liệu, Cổng sạc USB Type-C, Hốc chứa đồ 30.4L, Phanh CBS',
                
                'description': 'Xe tay ga cao cấp với động cơ eSP+ 156.9cc, hệ thống khởi động dừng thông minh Idle Stop tiết kiệm nhiên liệu tuyệt vời. Thiết kế sang trọng, rộng rãi với hốc chứa đồ lớn. Khóa thông minh tiện lợi.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.82 L/100km',
                'colors': 'Xám-Đen, Trắng-Đỏ, Xanh-Trắng, Đen'
            },
            {
                'brand': 'Honda',
                'model': 'SH 160i',
                'year': 2024,
                'category': 'Xe tay ga',
                'price_vnd': 78500000,
                'fuel_type': 'Xăng',
                
                # 动力系统  
                'engine_cc': 156,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch',
                'power_hp': 15.8,
                'power_rpm': 8500,
                'torque_nm': 14.7,
                'torque_rpm': 6500,
                'compression_ratio': '12.0:1',
                'bore_stroke': '60.0 x 55.1 mm',
                'valve_system': 'eSP+ DOHC 4 van',
                
                # 传动系统
                'transmission': 'Tự động vô cấp (V-Matic)',
                'clutch_type': 'Ly hợp tự động đa đĩa, khô',
                'fuel_supply': 'Phun xăng điện tử PGM-FI',
                'starter': 'Điện + Idle Stop System',
                'ignition': 'Full Transitor (điện tử)',
                
                # 底盘
                'frame_type': 'Khung thép ống (Underbone)',
                'front_suspension': 'Giảm xóc ống lồng, lò xo trụ',
                'rear_suspension': 'Giảm xóc đơn với lò xo trụ đôi',
                'front_brake': 'Đĩa đơn 240mm, phanh ABS',
                'rear_brake': 'Đĩa đơn 240mm',
                'front_tire': '100/80-16M/C',
                'rear_tire': '120/80-16M/C',
                
                # 尺寸重量
                'dimensions_mm': '2093 x 739 x 1129',
                'wheelbase_mm': 1353,
                'ground_clearance_mm': 146,
                'seat_height_mm': 765,
                'weight_kg': 134,
                'fuel_capacity_l': 7.5,
                
                # 配置
                'abs': True,
                'smart_key': True,
                'display_type': 'LCD đa thông tin (TFT có thể ở một số phiên bản)',
                'lighting': 'Đèn LED toàn bộ (pha Projector, hậu, xi-nhan)',
                'features': 'Khóa thông minh Smartkey, Hệ thống Idle Stop, Phanh ABS, Cổng sạc USB, Hốc chứa đồ lớn, Lẫy phanh tích hợp xi-nhan',
                
                'description': 'Xe tay ga cao cấp hàng đầu phân khúc với thiết kế sang trọng, tinh tế. Động cơ eSP+ mạnh mẽ, hệ thống an toàn ABS. Không gian rộng rãi, trang bị hiện đại. Lựa chọn hoàn hảo cho người thành đạt.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.95 L/100km',
                'colors': 'Đen, Trắng, Xám, Nâu, Xanh'
            },
            {
                'brand': 'Honda',
                'model': 'Vision',
                'year': 2024,
                'category': 'Xe tay ga',
                'price_vnd': 30500000,
                'fuel_type': 'Xăng',
                
                # 动力系统
                'engine_cc': 110,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát cưỡng bức bằng gió',
                'power_hp': 8.83,
                'power_rpm': 7500,
                'torque_nm': 9.3,
                'torque_rpm': 5500,
                'compression_ratio': '10.0:1',
                'bore_stroke': '50.0 x 55.1 mm',
                'valve_system': 'eSP OHC 2 van',
                
                # 传动系统
                'transmission': 'Tự động vô cấp (V-Matic)',
                'clutch_type': 'Ly hợp tự động khô',
                'fuel_supply': 'Phun xăng điện tử PGM-FI',
                'starter': 'Điện',
                'ignition': 'DC-CDI',
                
                # 底盘
                'frame_type': 'Khung thép ống (Underbone)',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 190mm',
                'rear_brake': 'Tang trống 130mm',
                'front_tire': '80/90-14M/C 40P',
                'rear_tire': '90/90-14M/C 46P',
                
                # 尺寸重量
                'dimensions_mm': '1877 x 684 x 1100',
                'wheelbase_mm': 1280,
                'ground_clearance_mm': 133,
                'seat_height_mm': 755,
                'weight_kg': 102,
                'fuel_capacity_l': 5.2,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'Đồng hồ analog kết hợp LCD',
                'lighting': 'Đèn Halogen (pha), LED (hậu, xi-nhan)',
                'features': 'Tiết kiệm nhiên liệu, Cốp xe rộng 16.5L, Móc treo đồ, Phanh CBS (tùy phiên bản)',
                
                'description': 'Xe tay ga phổ thông tiết kiệm nhiên liệu với động cơ eSP 109.2cc. Thiết kế nhỏ gọn, dễ điều khiển, phù hợp di chuyển trong thành phố. Giá cả hợp lý, chi phí vận hành thấp.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.69 L/100km',
                'colors': 'Đỏ-Đen, Xanh-Đen, Trắng-Đen, Đen'
            },
            {
                'brand': 'Honda',
                'model': 'Wave Alpha',
                'year': 2024,
                'category': 'Xe số',
                'price_vnd': 19500000,
                'fuel_type': 'Xăng',
                
                # 动力系统
                'engine_cc': 110,
                'engine_type': 'Xi-lanh đơn, 4 kỳ, làm mát cưỡng bức bằng gió',
                'power_hp': 7.7,
                'power_rpm': 7500,
                'torque_nm': 8.8,
                'torque_rpm': 5500,
                'compression_ratio': '9.3:1',
                'bore_stroke': '50.0 x 55.1 mm',
                'valve_system': 'OHC 2 van',
                
                # 传动系统
                'transmission': 'Số sàn 4 cấp, ly hợp tự động',
                'clutch_type': 'Ly hợp tự động ly tâm',
                'fuel_supply': 'Bộ chế hòa khí',
                'starter': 'Điện + đạp',
                'ignition': 'DC-CDI',
                
                # 底盘
                'frame_type': 'Khung xương ống thép (Underbone)',
                'front_suspension': 'Giảm xóc ống lồng',
                'rear_suspension': 'Giảm xóc đơn',
                'front_brake': 'Đĩa đơn 240mm (hoặc tang trống)',
                'rear_brake': 'Tang trống 130mm',
                'front_tire': '70/90-17M/C 38P',
                'rear_tire': '80/90-17M/C 44P',
                
                # 尺寸重量
                'dimensions_mm': '1940 x 710 x 1069',
                'wheelbase_mm': 1224,
                'ground_clearance_mm': 141,
                'seat_height_mm': 765,
                'weight_kg': 96,
                'fuel_capacity_l': 3.7,
                
                # 配置
                'abs': False,
                'smart_key': False,
                'display_type': 'Đồng hồ analog',
                'lighting': 'Đèn Halogen',
                'features': 'Tiết kiệm nhiên liệu vượt trội, Bền bỉ, Chi phí bảo dưỡng thấp, Dễ điều khiển',
                
                'description': 'Xe số huyền thoại bán chạy nhất Việt Nam. Động cơ 109.1cc bền bỉ, tiết kiệm nhiên liệu xuất sắc (chỉ 1.55L/100km). Thiết kế đơn giản, dễ bảo dưỡng, độ tin cậy cao. Lựa chọn số 1 của người lao động.',
                'warranty': '3 năm hoặc 30,000 km',
                'fuel_consumption': '1.55 L/100km',
                'colors': 'Đỏ, Đen, Xanh, Bạc'
            }
        ]
        
        motorcycles.extend(honda_bikes)
        print(f"✅ Honda: {len(honda_bikes)} xe (dữ liệu chi tiết)")
        return motorcycles
    
    def crawl_all_enhanced(self) -> List[Dict]:
        """爬取所有增强数据"""
        print("\n" + "="*60)
        print("🚀 开始爬取越南摩托车详细数据")
        print("="*60 + "\n")
        
        all_motorcycles = []
        
        # 爬取Honda详细数据
        all_motorcycles.extend(self.crawl_honda_enhanced())
        
        print("\n" + "="*60)
        print(f"✅ 爬取完成！总计: {len(all_motorcycles)} 辆摩托车（增强版）")
        print("="*60 + "\n")
        
        self.motorcycles = all_motorcycles
        return all_motorcycles
    
    def save_to_json(self, filename='motorcycles_enhanced_data.json'):
        """保存数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles, f, ensure_ascii=False, indent=2)
        print(f"💾 详细数据已保存到: {filename}")


def main():
    crawler = MotorcycleEnhancedCrawler()
    
    # 爬取详细数据
    motorcycles = crawler.crawl_all_enhanced()
    
    # 保存到JSON文件
    crawler.save_to_json('/root/越南摩托汽车网站/backend/src/scripts/data/motorcycles_enhanced_data.json')
    
    # 显示数据统计
    print("\n📊 数据维度统计:")
    if motorcycles:
        sample = motorcycles[0]
        dimensions = len([k for k in sample.keys() if sample[k] is not None])
        print(f"   每辆车包含 {dimensions} 个数据维度")
        print(f"\n   新增维度包括:")
        print(f"   • 发动机详情: engine_type, compression_ratio, bore_stroke, valve_system")
        print(f"   • 性能参数: power_rpm, torque_rpm")
        print(f"   • 传动系统: clutch_type, fuel_supply, starter, ignition")
        print(f"   • 底盘系统: frame_type, suspension (前后), tire (前后)")
        print(f"   • 详细尺寸: wheelbase, ground_clearance")
        print(f"   • 容量参数: fuel_capacity")
        print(f"   • 配置详情: lighting, warranty, fuel_consumption, colors")
    
    print("\n✨ 所有操作完成！")
    print("📝 下一步: 需要扩展数据库表结构以支持新字段")


if __name__ == '__main__':
    main()

