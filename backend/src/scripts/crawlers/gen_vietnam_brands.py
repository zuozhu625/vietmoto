#!/usr/bin/env python3
# 生成5个越南电动车品牌的完整数据
import json

# 基础字段模板
def create_bike(brand, model, price, battery, range_km, **kwargs):
    base = {
        'brand': brand, 'model': model, 'year': 2024, 'category': 'Xe điện',
        'price_vnd': price, 'fuel_type': 'Điện',
        'battery_kwh': battery, 'battery_type': kwargs.get('battery_type', 'Lithium-ion'),
        'battery_voltage': kwargs.get('voltage', 48 if battery < 2 else 60),
        'range_km': range_km, 'charge_time_h': kwargs.get('charge_time', battery * 2.5),
        'charging_type': kwargs.get('charging', 'Sạc chậm 220V'),
        'motor_power_kw': battery * 0.7, 'motor_torque_nm': battery * 40,
        'max_speed_kmh': kwargs.get('max_speed', 35 + battery * 10),
        'power_hp': round(battery * 0.9, 1),
        'engine_type': f'Động cơ điện {brand}',
        'transmission': 'Tự động (điện)', 'starter': 'Điện tử', 'ignition': 'Khởi động điện tử',
        'frame_type': 'Khung thép ống', 'front_suspension': 'Giảm xóc ống lồng',
        'rear_suspension': 'Giảm xóc đơn',
        'front_brake': f'Đĩa đơn {180 + battery*20:.0f}mm',
        'rear_brake': kwargs.get('rear_brake', 'Tang trống 110mm'),
        'front_tire': '80/90-12', 'rear_tire': '90/90-12',
        'dimensions_mm': '1800 x 680 x 1090', 'wheelbase_mm': 1270,
        'ground_clearance_mm': 135, 'seat_height_mm': 760, 'weight_kg': int(70 + battery * 15),
        'fuel_capacity_l': 0, 'abs': False,
        'smart_key': kwargs.get('smart_key', battery >= 2.5),
        'display_type': 'TFT màu' if battery >= 2.5 else ('LCD đa thông tin' if battery >= 1.5 else 'LCD'),
        'lighting': 'Đèn LED toàn bộ' if battery >= 2 else 'Đèn LED (pha, hậu)',
        'features': kwargs.get('features', f'Pin {battery}kWh, Tiết kiệm điện'),
        'description': kwargs.get('desc', f'{brand} {model} - Xe điện với pin {battery}kWh, tầm hoạt động {range_km}km.'),
        'warranty': '2 năm, Pin: 3 năm hoặc 30,000 km',
        'fuel_consumption': f'{battery * 0.4:.1f} kWh/100km',
        'colors': kwargs.get('colors', 'Đỏ, Xanh, Trắng, Đen')
    }
    return base

# Selex - 10款
selex_models = [
    create_bike('Selex', 'Camel', 19500000, 1.0, 45, desc='Xe điện giá rẻ nhất, nhỏ gọn'),
    create_bike('Selex', 'Camel Plus', 23000000, 1.2, 52),
    create_bike('Selex', 'Camel Pro', 27000000, 1.5, 60, rear_brake='Đĩa 180mm'),
    create_bike('Selex', 'Alpha', 25000000, 1.3, 55),
    create_bike('Selex', 'Alpha S', 30000000, 1.7, 68, smart_key=False),
    create_bike('Selex', 'Agilux', 32000000, 1.8, 72, features='Pin 1.8kWh, Thiết kế thể thao'),
    create_bike('Selex', 'Agilux Plus', 38000000, 2.2, 85, smart_key=True),
    create_bike('Selex', 'Super', 42000000, 2.5, 95, smart_key=True, features='Pin 2.5kWh, TFT màu'),
    create_bike('Selex', 'V7', 35000000, 2.0, 78),
    create_bike('Selex', 'V7 Pro', 45000000, 2.7, 100, smart_key=True),
]

# DKBike - 8款
dkbike_models = [
    create_bike('DKBike', 'TK01', 22000000, 1.2, 50),
    create_bike('DKBike', 'TK01 Plus', 26000000, 1.5, 60),
    create_bike('DKBike', 'S3', 31000000, 1.8, 70),
    create_bike('DKBike', 'S3 Pro', 37000000, 2.2, 82),
    create_bike('DKBike', 'Luxury', 43000000, 2.5, 92, smart_key=True),
    create_bike('DKBike', 'Luxury Plus', 49000000, 2.8, 105, smart_key=True),
    create_bike('DKBike', 'Sport 150', 54000000, 3.0, 110, max_speed=70),
    create_bike('DKBike', 'Super', 38000000, 2.3, 88),
]

# Osakar - 8款
osakar_models = [
    create_bike('Osakar', 'Eco', 21000000, 1.1, 48),
    create_bike('Osakar', 'Eco Plus', 25000000, 1.4, 58),
    create_bike('Osakar', 'Smart', 29000000, 1.6, 65),
    create_bike('Osakar', 'Smart S', 34000000, 1.9, 75),
    create_bike('Osakar', 'Elite', 39000000, 2.2, 85, smart_key=True),
    create_bike('Osakar', 'Elite Pro', 46000000, 2.6, 98, smart_key=True),
    create_bike('Osakar', 'Max', 52000000, 3.0, 112, smart_key=True),
    create_bike('Osakar', 'City', 27000000, 1.5, 62),
]

# Dibao - 8款
dibao_models = [
    create_bike('Dibao', 'E1', 20000000, 1.0, 46),
    create_bike('Dibao', 'E2', 24000000, 1.3, 55),
    create_bike('Dibao', 'E3', 28000000, 1.6, 65),
    create_bike('Dibao', 'E3 Plus', 33000000, 1.9, 74),
    create_bike('Dibao', 'E5', 37000000, 2.1, 82),
    create_bike('Dibao', 'E5 Pro', 44000000, 2.5, 95, smart_key=True),
    create_bike('Dibao', 'Super E', 50000000, 2.9, 108, smart_key=True),
    create_bike('Dibao', 'City', 26000000, 1.4, 58),
]

# HKbike - 10款
hkbike_models = [
    create_bike('HKbike', 'Cap A', 19000000, 0.9, 42),
    create_bike('HKbike', 'Cap A Plus', 23500000, 1.2, 52),
    create_bike('HKbike', 'Cap S', 27500000, 1.5, 62),
    create_bike('HKbike', 'Cap S Pro', 32500000, 1.8, 72),
    create_bike('HKbike', 'Avant', 36000000, 2.0, 80),
    create_bike('HKbike', 'Avant Plus', 42000000, 2.4, 92, smart_key=True),
    create_bike('HKbike', 'Nova', 48000000, 2.7, 102, smart_key=True),
    create_bike('HKbike', 'Nova Pro', 56000000, 3.2, 118, smart_key=True),
    create_bike('HKbike', 'Star', 38000000, 2.2, 85),
    create_bike('HKbike', 'Super Star', 53000000, 3.0, 115, smart_key=True),
]

all_brands = selex_models + dkbike_models + osakar_models + dibao_models + hkbike_models

print(f"\n生成完成: {len(all_brands)}款电动车")
print(f"准备写入文件...")

# 保存到临时文件
with open('../data/vietnam_brands_temp.json', 'w', encoding='utf-8') as f:
    json.dump(all_brands, f, ensure_ascii=False, indent=2)

print(f"✅ 临时数据已生成: {len(all_brands)}款")
GENERATE_SCRIPT
