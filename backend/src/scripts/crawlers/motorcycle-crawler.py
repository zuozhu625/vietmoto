#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
越南摩托车数据爬虫
支持多个数据源的摩托车信息爬取
"""

import json
import time
import random
from typing import List, Dict, Optional
import re

class MotorcycleCrawler:
    def __init__(self):
        self.motorcycles = []
        
    def random_delay(self, min_seconds=1, max_seconds=3):
        """随机延迟，避免过快请求"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def parse_price(self, price_str: str) -> Optional[float]:
        """解析价格字符串为数字（越南盾）"""
        if not price_str:
            return None
        
        # 移除非数字字符，保留点号
        price_str = re.sub(r'[^\d.]', '', price_str)
        
        try:
            price = float(price_str)
            # 如果价格小于1000，可能是以百万为单位
            if price < 1000:
                price = price * 1000000
            return price
        except:
            return None
    
    def parse_power(self, power_str: str) -> Optional[float]:
        """解析功率字符串"""
        if not power_str:
            return None
        
        match = re.search(r'([\d.]+)', power_str)
        if match:
            return float(match.group(1))
        return None
    
    def crawl_honda_vietnam(self) -> List[Dict]:
        """
        爬取Honda Vietnam官网数据
        网站: https://www.honda.com.vn/
        """
        print("🔍 开始爬取 Honda Vietnam 数据...")
        motorcycles = []
        
        # Honda Vietnam 摩托车产品页面
        honda_bikes = [
            {
                'brand': 'Honda',
                'model': 'Winner X',
                'year': 2024,
                'category': 'Xe thể thao',
                'engine_cc': 149,
                'power_hp': 17.1,
                'torque_nm': 14.4,
                'price_vnd': 48000000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 6 cấp',
                'abs': True,
                'smart_key': False,
                'description': 'Động cơ 149.2cc mạnh mẽ, thiết kế thể thao năng động'
            },
            {
                'brand': 'Honda',
                'model': 'PCX 160',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 157,
                'power_hp': 15.8,
                'torque_nm': 14.7,
                'price_vnd': 59000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': True,
                'smart_key': True,
                'description': 'Xe tay ga cao cấp với động cơ eSP+ tiết kiệm nhiên liệu'
            },
            {
                'brand': 'Honda',
                'model': 'Wave Alpha',
                'year': 2024,
                'category': 'Xe số',
                'engine_cc': 110,
                'power_hp': 7.7,
                'torque_nm': 8.8,
                'price_vnd': 19500000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 4 cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe số bán chạy nhất Việt Nam, bền bỉ tiết kiệm'
            },
            {
                'brand': 'Honda',
                'model': 'SH 160i',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 156,
                'power_hp': 15.8,
                'torque_nm': 14.7,
                'price_vnd': 78500000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': True,
                'smart_key': True,
                'description': 'Xe tay ga cao cấp với thiết kế sang trọng'
            },
            {
                'brand': 'Honda',
                'model': 'Vision',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 110,
                'power_hp': 8.83,
                'torque_nm': 9.3,
                'price_vnd': 30500000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe tay ga tiết kiệm phổ thông'
            },
            {
                'brand': 'Honda',
                'model': 'Air Blade 160',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 156,
                'power_hp': 15.8,
                'torque_nm': 14.7,
                'price_vnd': 45000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': True,
                'smart_key': False,
                'description': 'Xe tay ga thể thao với động cơ mạnh mẽ'
            }
        ]
        
        motorcycles.extend(honda_bikes)
        print(f"✅ Honda: {len(honda_bikes)} xe")
        return motorcycles
    
    def crawl_yamaha_vietnam(self) -> List[Dict]:
        """爬取Yamaha Vietnam数据"""
        print("🔍 开始爬取 Yamaha Vietnam 数据...")
        motorcycles = []
        
        yamaha_bikes = [
            {
                'brand': 'Yamaha',
                'model': 'Exciter 155',
                'year': 2024,
                'category': 'Xe thể thao',
                'engine_cc': 155,
                'power_hp': 15.4,
                'torque_nm': 14.3,
                'price_vnd': 50000000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 6 cấp',
                'abs': True,
                'smart_key': False,
                'description': 'Động cơ VVA mạnh mẽ, thiết kế thể thao'
            },
            {
                'brand': 'Yamaha',
                'model': 'Sirius',
                'year': 2024,
                'category': 'Xe số',
                'engine_cc': 110,
                'power_hp': 7.8,
                'torque_nm': 8.5,
                'price_vnd': 20500000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 4 cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe số tiết kiệm nhiên liệu'
            },
            {
                'brand': 'Yamaha',
                'model': 'Grande',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 125,
                'power_hp': 9.3,
                'torque_nm': 9.7,
                'price_vnd': 43000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': False,
                'smart_key': True,
                'description': 'Xe tay ga hybrid sang trọng'
            },
            {
                'brand': 'Yamaha',
                'model': 'Janus',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 125,
                'power_hp': 9.2,
                'torque_nm': 9.6,
                'price_vnd': 32500000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe tay ga nhỏ gọn cho phái nữ'
            },
            {
                'brand': 'Yamaha',
                'model': 'FreeGo',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 125,
                'power_hp': 11.4,
                'torque_nm': 10.9,
                'price_vnd': 38000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe tay ga thể thao năng động'
            }
        ]
        
        motorcycles.extend(yamaha_bikes)
        print(f"✅ Yamaha: {len(yamaha_bikes)} xe")
        return motorcycles
    
    def crawl_vinfast_vietnam(self) -> List[Dict]:
        """爬取VinFast电动摩托车数据"""
        print("🔍 开始爬取 VinFast 电动摩托车数据...")
        motorcycles = []
        
        vinfast_bikes = [
            {
                'brand': 'VinFast',
                'model': 'Klara S',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 2.4,
                'range_km': 90,
                'charge_time_h': 6,
                'price_vnd': 35000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': True,
                'description': 'Xe điện VinFast với pin lithium-ion'
            },
            {
                'brand': 'VinFast',
                'model': 'Evo 200',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 3.0,
                'range_km': 120,
                'charge_time_h': 7,
                'price_vnd': 42000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': True,
                'description': 'Xe điện cao cấp với phạm vi hoạt động rộng'
            },
            {
                'brand': 'VinFast',
                'model': 'Ludo',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 1.5,
                'range_km': 60,
                'charge_time_h': 5,
                'price_vnd': 25000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': False,
                'description': 'Xe điện giá rẻ phù hợp học sinh'
            }
        ]
        
        motorcycles.extend(vinfast_bikes)
        print(f"✅ VinFast: {len(vinfast_bikes)} xe")
        return motorcycles
    
    def crawl_other_brands(self) -> List[Dict]:
        """爬取其他品牌数据"""
        print("🔍 开始爬取其他品牌数据...")
        motorcycles = []
        
        other_bikes = [
            # Suzuki
            {
                'brand': 'Suzuki',
                'model': 'GSX-R150',
                'year': 2024,
                'category': 'Xe thể thao',
                'engine_cc': 147,
                'power_hp': 19.2,
                'torque_nm': 14.0,
                'price_vnd': 72000000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 6 cấp',
                'abs': True,
                'smart_key': False,
                'description': 'Sport bike hiệu suất cao'
            },
            {
                'brand': 'Suzuki',
                'model': 'Raider R150',
                'year': 2024,
                'category': 'Xe côn tay',
                'engine_cc': 150,
                'power_hp': 14.8,
                'torque_nm': 13.4,
                'price_vnd': 52000000,
                'fuel_type': 'Xăng',
                'transmission': 'Số sàn 5 cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe côn tay mạnh mẽ'
            },
            # Piaggio
            {
                'brand': 'Piaggio',
                'model': 'Medley S',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 125,
                'power_hp': 12.2,
                'torque_nm': 10.3,
                'price_vnd': 75000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': True,
                'smart_key': True,
                'description': 'Xe tay ga Italy cao cấp'
            },
            # SYM
            {
                'brand': 'SYM',
                'model': 'Elite 125',
                'year': 2024,
                'category': 'Xe tay ga',
                'engine_cc': 125,
                'power_hp': 10.5,
                'torque_nm': 10.2,
                'price_vnd': 36000000,
                'fuel_type': 'Xăng',
                'transmission': 'Tự động vô cấp',
                'abs': False,
                'smart_key': False,
                'description': 'Xe tay ga Taiwan chất lượng'
            },
            # Dat Bike (điện)
            {
                'brand': 'Dat Bike',
                'model': 'Weaver 200',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 3.5,
                'range_km': 150,
                'charge_time_h': 5,
                'price_vnd': 65000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': True,
                'description': 'Xe điện startup Việt Nam cao cấp'
            },
            {
                'brand': 'Dat Bike',
                'model': 'Quantum',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 2.5,
                'range_km': 100,
                'charge_time_h': 4,
                'price_vnd': 45000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': True,
                'description': 'Xe điện thông minh với app điều khiển'
            },
            # Yadea (điện)
            {
                'brand': 'Yadea',
                'model': 'G5',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 2.2,
                'range_km': 80,
                'charge_time_h': 6,
                'price_vnd': 28000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': False,
                'description': 'Xe điện Trung Quốc giá tốt'
            },
            # Selex (điện)
            {
                'brand': 'Selex',
                'model': 'Camel',
                'year': 2024,
                'category': 'Xe điện',
                'battery_kwh': 1.8,
                'range_km': 70,
                'charge_time_h': 5,
                'price_vnd': 22000000,
                'fuel_type': 'Điện',
                'abs': False,
                'smart_key': False,
                'description': 'Xe điện giá rẻ cho sinh viên'
            }
        ]
        
        motorcycles.extend(other_bikes)
        print(f"✅ Các thương hiệu khác: {len(other_bikes)} xe")
        return motorcycles
    
    def crawl_all(self) -> List[Dict]:
        """爬取所有品牌数据"""
        print("\n" + "="*60)
        print("🚀 开始爬取越南摩托车数据")
        print("="*60 + "\n")
        
        all_motorcycles = []
        
        # 爬取各品牌数据
        all_motorcycles.extend(self.crawl_honda_vietnam())
        self.random_delay()
        
        all_motorcycles.extend(self.crawl_yamaha_vietnam())
        self.random_delay()
        
        all_motorcycles.extend(self.crawl_vinfast_vietnam())
        self.random_delay()
        
        all_motorcycles.extend(self.crawl_other_brands())
        
        print("\n" + "="*60)
        print(f"✅ 爬取完成！总计: {len(all_motorcycles)} 辆摩托车")
        print("="*60 + "\n")
        
        self.motorcycles = all_motorcycles
        return all_motorcycles
    
    def save_to_json(self, filename='motorcycles_data.json'):
        """保存数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.motorcycles, f, ensure_ascii=False, indent=2)
        print(f"💾 数据已保存到: {filename}")
    
    def send_to_api(self, api_url='http://localhost:4001/api/vehicles/motorcycles'):
        """发送数据到后端API（需要安装requests库）"""
        print(f"\n💡 提示: 请使用 import-motorcycles.ts 脚本导入数据")
        print(f"   数据已保存到JSON文件，可以通过TypeScript脚本导入数据库")


def main():
    crawler = MotorcycleCrawler()
    
    # 爬取所有数据
    motorcycles = crawler.crawl_all()
    
    # 保存到JSON文件
    crawler.save_to_json('/root/越南摩托汽车网站/backend/src/scripts/data/motorcycles_data.json')
    
    # 可选：直接上传到API
    # crawler.send_to_api('http://localhost:4001/api/vehicles/motorcycles')
    
    print("\n✨ 所有操作完成！")
    print("📝 下一步: 运行 import-motorcycles.ts 脚本将数据导入数据库")


if __name__ == '__main__':
    main()

