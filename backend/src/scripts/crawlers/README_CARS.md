# 越南汽车爬虫系统 - 完整文档

## 📋 系统概述

本系统成功爬取并导入了越南市场**15个汽车品牌、98款车型**的完整数据。

---

## 🎯 爬虫文件列表

### 第一批爬虫（主流品牌）
**文件**: `vietnam-cars-complete-crawler.py`
```bash
# 运行命令
python3 vietnam-cars-complete-crawler.py

# 输出文件
../data/vietnam_cars_complete.json (36款)

# 导入命令
node dist/scripts/import-vietnam-cars.js
```

**覆盖品牌**：
- VinFast (8款) - 含6款电动车
- Toyota (10款)
- Honda (5款)
- Hyundai (8款)
- Ford (5款)

**总计**: 36款

---

### 第二批爬虫（补充品牌）
**文件**: `vietnam-cars-additional-brands.py`
```bash
# 运行命令
python3 vietnam-cars-additional-brands.py

# 输出文件
../data/vietnam_cars_additional_brands.json (31款)

# 导入命令
node dist/scripts/import-additional-cars.js
```

**覆盖品牌**：
- Mitsubishi (6款)
- Kia (9款)
- Mazda (8款)
- Thaco (5款)
- Isuzu (3款)

**总计**: 31款

---

### 第三批爬虫（豪华欧系品牌）
**文件**: `vietnam-cars-luxury-brands.py`
```bash
# 运行命令
python3 vietnam-cars-luxury-brands.py

# 输出文件
../data/vietnam_cars_luxury_brands.json (31款)

# 导入命令
node dist/scripts/import-luxury-cars.js
```

**覆盖品牌**：
- Nissan (5款)
- Peugeot (4款)
- BMW (7款)
- Mercedes-Benz (9款)
- Skoda (6款)

**总计**: 31款

---

## 📊 数据统计（总计98款）

### 品牌分布（15个品牌）

| 排名 | 品牌 | 车型数 | 类型 |
|------|------|--------|------|
| 1 | Toyota | 10 | 日系主流 |
| 2 | Kia | 9 | 韩系性价比 |
| 3 | Mercedes-Benz | 9 | 德系豪华 |
| 4 | VinFast | 8 | 越南电动 |
| 5 | Mazda | 8 | 日系精品 |
| 6 | Hyundai | 8 | 韩系主流 |
| 7 | BMW | 7 | 德系豪华 |
| 8 | Mitsubishi | 6 | 日系实用 |
| 9 | Skoda | 6 | 捷克实用 |
| 10 | Thaco | 5 | 本土代理 |
| 11 | Nissan | 5 | 日系实用 |
| 12 | Honda | 5 | 日系经典 |
| 13 | Ford | 5 | 美系强者 |
| 14 | Peugeot | 4 | 法系浪漫 |
| 15 | Isuzu | 3 | 日系工具车 |

---

### 燃料类型分布

- 🔋 **电动车**: 6款（全部VinFast）
- ⛽ **燃油车**: 92款

---

### 价格区间分布

- 💰 **入门级（< 5亿）**: 约15款
- 💰 **主流级（5-10亿）**: 约40款
- 💰 **中高端（10-20亿）**: 约25款
- 💰 **豪华级（20-55亿）**: 约18款

---

## 🚀 完整更新流程

### 方法1: 分批更新（推荐）

```bash
# 1. 更新第一批（主流品牌）
cd /root/越南摩托汽车网站/backend/src/scripts/crawlers
python3 vietnam-cars-complete-crawler.py

# 2. 更新第二批（补充品牌）
python3 vietnam-cars-additional-brands.py

# 3. 更新第三批（豪华品牌）
python3 vietnam-cars-luxury-brands.py

# 4. 编译并导入
cd /root/越南摩托汽车网站/backend
npm run build

# 复制数据文件
mkdir -p dist/scripts/data
cp src/scripts/data/*.json dist/scripts/data/

# 5. 依次导入
node dist/scripts/import-vietnam-cars.js
node dist/scripts/import-additional-cars.js
node dist/scripts/import-luxury-cars.js

# 6. 部署到生产
cd /root/越南摩托汽车网站
sudo cp backend/database/vietnam_moto_auto.sqlite /var/www/vietnam-moto-auto/backend/database/
sudo systemctl restart vietnam-moto-backend
```

---

### 方法2: 一键更新（快速）

创建一键更新脚本：

```bash
#!/bin/bash
# update-all-cars.sh

echo "🚀 开始更新所有汽车数据..."

cd /root/越南摩托汽车网站/backend/src/scripts/crawlers

# 运行所有爬虫
python3 vietnam-cars-complete-crawler.py
python3 vietnam-cars-additional-brands.py
python3 vietnam-cars-luxury-brands.py

# 编译并导入
cd /root/越南摩托汽车网站/backend
npm run build
mkdir -p dist/scripts/data
cp src/scripts/data/*.json dist/scripts/data/

# 导入所有数据
node dist/scripts/import-vietnam-cars.js
node dist/scripts/import-additional-cars.js
node dist/scripts/import-luxury-cars.js

# 部署
sudo cp backend/database/vietnam_moto_auto.sqlite /var/www/vietnam-moto-auto/backend/database/
sudo systemctl restart vietnam-moto-backend

echo "✅ 所有汽车数据更新完成！"
```

---

## 📈 各品牌完整车型列表

### 🚗 Toyota (10款)
1. Vios - Sedan hạng B - 458 triệu
2. Camry - Sedan hạng D - 1,220 triệu
3. Raize - SUV cỡ A - 498 triệu
4. Yaris Cross - SUV cỡ A+ - 650 triệu
5. Corolla Cross - SUV cỡ B - 820 triệu
6. Veloz Cross - MPV 7 chỗ - 638 triệu
7. Innova Cross - MPV 7 chỗ - 810 triệu
8. Fortuner - SUV 7 chỗ - 1,195 triệu
9. Hilux - Bán tải - 668 triệu
10. Land Cruiser - SUV cao cấp - 4,030 triệu

### 🚗 Kia (9款)
1. Morning - Hatchback cỡ A - 349 triệu
2. Soluto - Sedan hạng B - 429 triệu
3. K3 - Sedan hạng C - 559 triệu
4. K5 - Sedan hạng D - 859 triệu
5. Sonet - SUV cỡ A - 539 triệu
6. Seltos - SUV cỡ B - 599 triệu
7. Sportage - SUV cỡ C - 859 triệu
8. Sorento - SUV 7 chỗ - 1,099 triệu
9. Carnival - MPV cao cấp - 1,339 triệu

### ⚡ VinFast (8款电动)
1. VF3 - SUV điện mini - 240 triệu (210km)
2. VF5 Plus - SUV điện cỡ A - 468 triệu (326km)
3. VF6 - SUV điện cỡ B - 675 triệu (380km)
4. VF7 - SUV điện cỡ C - 850 triệu (450km)
5. VF8 - SUV điện cỡ D - 1,200 triệu (471km)
6. VF9 - SUV điện cỡ E - 1,500 triệu (594km)
7. Lux A2.0 - Sedan cao cấp - 960 triệu
8. Lux SA2.0 - SUV cao cấp - 1,200 triệu

### 🚗 Mazda (8款)
1. Mazda2 - Sedan hạng B - 408 triệu
2. Mazda3 - Sedan hạng C - 669 triệu
3. CX-3 - SUV cỡ B - 629 triệu
4. CX-30 - SUV cỡ B+ - 839 triệu
5. CX-5 - SUV cỡ trung - 859 triệu
6. CX-8 - SUV 7 chỗ - 1,099 triệu
7. CX-60 - SUV cao cấp - 1,499 triệu
8. BT-50 - Bán tải - 659 triệu

### 🚗 Hyundai (8款)
1. Accent - Sedan hạng B - 439 triệu
2. Elantra - Sedan hạng C - 659 triệu
3. Creta - SUV cỡ nhỏ - 640 triệu
4. Tucson - SUV cỡ C - 769 triệu
5. Santa Fe - SUV 7 chỗ - 1,069 triệu
6. Palisade - SUV 8 chỗ - 1,439 triệu
7. Stargazer - MPV 7 chỗ - 489 triệu
8. Custin - MPV cao cấp - 820 triệu

### 💎 Mercedes-Benz (9款)
1. A-Class - Sedan hạng sang - 1,599 triệu
2. C-Class - Sedan hạng sang - 1,899 triệu
3. E-Class - Sedan hạng sang - 2,899 triệu
4. S-Class - Sedan siêu sang - 5,499 triệu
5. GLA - SUV cỡ nhỏ - 1,799 triệu
6. GLB - SUV 7 chỗ - 2,099 triệu
7. GLC - SUV cỡ trung - 2,599 triệu
8. GLE - SUV cỡ lớn - 3,999 triệu
9. GLS - SUV hạng sang - 5,499 triệu

### 💎 BMW (7款)
1. 3 Series - Sedan hạng sang - 1,899 triệu
2. 5 Series - Sedan hạng sang - 2,499 triệu
3. 7 Series - Sedan siêu sang - 5,499 triệu
4. X1 - SUV cỡ nhỏ - 1,799 triệu
5. X3 - SUV cỡ trung - 2,499 triệu
6. X5 - SUV cỡ lớn - 3,699 triệu
7. X7 - SUV hạng sang - 4,999 triệu

### 🚗 Mitsubishi (6款)
1. Attrage - Sedan hạng B - 375 triệu
2. Xpander - MPV 7 chỗ - 598 triệu
3. Xpander Cross - MPV Cross - 670 triệu
4. Triton - Bán tải - 630 triệu
5. Pajero Sport - SUV 7 chỗ - 1,098 triệu
6. Outlander - SUV cỡ C - 825 triệu

### 🚗 Skoda (6款)
1. Fabia - Hatchback hạng B - 469 triệu
2. Scala - Sedan hạng B - 629 triệu
3. Kamiq - SUV cỡ B - 799 triệu
4. Karoq - SUV cỡ C - 999 triệu
5. Kodiaq - SUV 7 chỗ - 1,399 triệu
6. Superb - Sedan hạng D - 1,399 triệu

### 🚗 Thaco (5款)
1. Mazda2 - Sedan hạng B - 408 triệu
2. Peugeot 3008 - SUV cỡ C - 1,099 triệu
3. Peugeot 5008 - SUV 7 chỗ - 1,299 triệu
4. BMW 5 Series - Sedan hạng sang - 2,499 triệu
5. BMW X7 - SUV hạng sang - 4,999 triệu

### 🚗 Nissan (5款)
1. Almera - Sedan hạng B - 469 triệu
2. Kicks - SUV cỡ B - 749 triệu
3. X-Trail - SUV cỡ C - 1,099 triệu
4. Terra - SUV 7 chỗ - 999 triệu
5. Navara - Bán tải - 748 triệu

### 🚗 Honda (5款)
1. City - Sedan hạng B - 559 triệu
2. Civic - Sedan hạng C - 789 triệu
3. Accord - Sedan hạng D - 1,319 triệu
4. HR-V - SUV cỡ B - 750 triệu
5. CR-V - SUV cỡ C - 1,099 triệu

### 🚗 Ford (5款)
1. Ranger - Bán tải - 659 triệu
2. Everest - SUV 7 chỗ - 1,099 triệu
3. Territory - SUV cỡ C - 839 triệu
4. Explorer - SUV cao cấp - 2,199 triệu
5. Mustang - Xe thể thao - 2,999 triệu

### 🚗 Peugeot (4款)
1. 2008 - SUV cỡ B - 789 triệu
2. 3008 - SUV cỡ C - 1,099 triệu
3. 5008 - SUV 7 chỗ - 1,299 triệu
4. Traveller - MPV cao cấp - 1,699 triệu

### 🚗 Isuzu (3款)
1. D-Max - Bán tải - 659 triệu
2. mu-X - SUV 7 chỗ - 990 triệu
3. Hi-Lander - SUV cỡ trung - 850 triệu

---

## 🔄 完整更新命令

### 爬取所有品牌数据
```bash
cd /root/越南摩托汽车网站/backend/src/scripts/crawlers

# 第一批
python3 vietnam-cars-complete-crawler.py

# 第二批
python3 vietnam-cars-additional-brands.py

# 第三批
python3 vietnam-cars-luxury-brands.py
```

### 导入所有数据
```bash
cd /root/越南摩托汽车网站/backend

# 编译
npm run build

# 复制数据文件
mkdir -p dist/scripts/data
cp src/scripts/data/*.json dist/scripts/data/

# 导入（按顺序）
node dist/scripts/import-vietnam-cars.js
node dist/scripts/import-additional-cars.js
node dist/scripts/import-luxury-cars.js
```

### 部署到生产
```bash
# 方法1: 仅更新数据库
sudo cp /root/越南摩托汽车网站/backend/database/vietnam_moto_auto.sqlite \
        /var/www/vietnam-moto-auto/backend/database/
sudo systemctl restart vietnam-moto-backend

# 方法2: 完整部署（推荐）
cd /root/越南摩托汽车网站
sudo bash deploy.sh
```

---

## 📊 数据验证

### 查看数据库统计
```bash
# 品牌统计
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT brand, COUNT(*) FROM cars GROUP BY brand ORDER BY COUNT(*) DESC;"

# 燃料类型
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT fuel_type, COUNT(*) FROM cars GROUP BY fuel_type;"

# 总数
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT COUNT(*) FROM cars WHERE status='active';"
```

### API测试
```bash
# 取消代理
unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY

# 获取品牌列表
curl "http://localhost:4001/api/vehicles/cars/brands" | python3 -m json.tool

# 按品牌查询
curl "http://localhost:4001/api/vehicles/cars?brand=Mercedes-Benz" | python3 -m json.tool

# 电动车查询
curl "http://localhost:4001/api/vehicles/cars?fuel_type=Điện" | python3 -m json.tool

# 价格区间查询
curl "http://localhost:4001/api/vehicles/cars?min_price=2000000000&max_price=3000000000" | python3 -m json.tool
```

---

## 🎯 亮点车型

### 🏆 各价位段代表车型

**入门级（< 5亿）**:
- 最便宜: Kia Morning - 349 triệu
- 性价比: Mitsubishi Attrage - 375 triệu

**主流级（5-10亿）**:
- 畅销王: Toyota Vios - 458 triệu
- 电动入门: VinFast VF3 - 240 triệu

**中高端（10-20亿）**:
- 日系代表: Toyota Camry - 1,220 triệu
- 韩系代表: Hyundai Palisade - 1,439 triệu
- 电动代表: VinFast VF9 - 1,500 triệu

**豪华级（20-55亿）**:
- 德系双雄: BMW 7 Series / Mercedes S-Class - 5,499 triệu
- 越野之王: Toyota Land Cruiser - 4,030 triệu
- 超跑传奇: Ford Mustang - 2,999 triệu

---

## 🔍 数据字段说明

### 必填字段（10个）
- brand, model, year, category, slug
- price_vnd, seating_capacity, fuel_type
- abs, smart_key, status

### 核心字段（30个）
包括发动机、尺寸、配置等关键参数

### 电动车专用字段
- battery_kwh (电池容量)
- range_km (续航里程)
- charge_time_h (充电时间)

---

## 📞 API端点

### 获取汽车列表
```
GET /api/vehicles/cars
参数: brand, category, fuel_type, min_price, max_price, limit, page
```

### 获取品牌列表
```
GET /api/vehicles/cars/brands
```

### 获取分类列表
```
GET /api/vehicles/cars/categories
```

### 获取单个汽车
```
GET /api/vehicles/cars/:id
GET /api/vehicles/cars/slug/:slug
```

---

## ✅ 完成情况

- ✅ 15个品牌全覆盖
- ✅ 98款车型完整数据
- ✅ 从入门到豪华全价位段
- ✅ 电动车完整系列（VinFast）
- ✅ 所有数据已部署上线

---

**创建日期**: 2024年10月12日  
**最后更新**: 2024年10月12日  
**维护者**: 爬虫开发团队

