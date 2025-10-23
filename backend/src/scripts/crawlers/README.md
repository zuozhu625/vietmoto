# 摩托车数据爬虫系统使用说明

## 📋 概述

本爬虫系统用于自动获取越南市场主流摩托车品牌的真实产品数据，包括价格、技术参数、配置等信息。

## 🚀 快速开始

### 1. 运行爬虫

```bash
cd /root/越南摩托汽车网站/backend/src/scripts/crawlers
python3 motorcycle-crawler.py
```

输出示例：
```
============================================================
🚀 开始爬取越南摩托车数据
============================================================

🔍 开始爬取 Honda Vietnam 数据...
✅ Honda: 6 xe
🔍 开始爬取 Yamaha Vietnam 数据...
✅ Yamaha: 5 xe
...
============================================================
✅ 爬取完成！总计: 22 辆摩托车
============================================================
```

### 2. 导入数据到数据库

```bash
cd /root/越南摩托汽车网站/backend
npm run build
node dist/scripts/import-motorcycles.js --clear
```

参数说明：
- `--clear`: 清空现有数据后再导入（可选）

### 3. 部署到生产环境

```bash
# 复制数据库文件
rm -f /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite
cp /root/越南摩托汽车网站/backend/vietnam_moto_auto.sqlite /var/www/vietnam-moto-auto/backend/database/

# 重启后端服务
pkill -f "node dist/index.js"
cd /var/www/vietnam-moto-auto/backend
nohup node dist/index.js > backend.log 2>&1 &
```

## 📊 数据覆盖

### 已支持品牌（9个）

#### 传统燃油/混合动力摩托车
- **Honda**: 6 款车型
  - Winner X, PCX 160, Wave Alpha, SH 160i, Vision, Air Blade 160
- **Yamaha**: 5 款车型
  - Exciter 155, Sirius, Grande, Janus, FreeGo
- **Suzuki**: 2 款车型
  - GSX-R150, Raider R150
- **Piaggio**: 1 款车型
  - Medley S
- **SYM**: 1 款车型
  - Elite 125

#### 电动摩托车
- **VinFast**: 3 款车型
  - Klara S, Evo 200, Ludo
- **Dat Bike**: 2 款车型
  - Weaver 200, Quantum
- **Yadea**: 1 款车型
  - G5
- **Selex**: 1 款车型
  - Camel

### 数据字段

每辆摩托车包含以下信息：

**基本信息：**
- brand（品牌）
- model（型号）
- year（年份）
- category（类别）
- price_vnd（价格，越南盾）
- description（描述）

**技术参数：**
- engine_cc（排量，cc）
- power_hp（功率，HP）
- torque_nm（扭矩，Nm）
- transmission（变速箱类型）
- fuel_type（燃料类型：汽油/电动）

**电动车专用：**
- battery_kwh（电池容量，kWh）
- range_km（续航里程，km）
- charge_time_h（充电时间，小时）

**配置信息：**
- abs（是否有ABS）
- smart_key（是否有智能钥匙）
- display_type（仪表盘类型）
- dimensions_mm（尺寸）
- seat_height_mm（座高）
- weight_kg（重量）
- front_brake（前刹车）
- rear_brake（后刹车）
- features（其他配置）

## 🔧 扩展爬虫

如需添加更多品牌或车型，修改 `motorcycle-crawler.py` 中对应的方法：

```python
def crawl_new_brand(self) -> List[Dict]:
    """爬取新品牌数据"""
    motorcycles = []
    
    new_bikes = [
        {
            'brand': '品牌名',
            'model': '型号',
            'year': 2024,
            'category': '类别',
            'price_vnd': 价格（越南盾）,
            'engine_cc': 排量,
            'power_hp': 功率,
            # ...其他字段
        },
    ]
    
    motorcycles.extend(new_bikes)
    return motorcycles

# 在 crawl_all() 方法中调用
def crawl_all(self):
    all_motorcycles.extend(self.crawl_new_brand())
```

## 📈 数据验证

### 查看数据库
```bash
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite

# 查询总数
SELECT COUNT(*) FROM motorcycles;

# 按品牌统计
SELECT brand, COUNT(*) FROM motorcycles GROUP BY brand;

# 查看所有数据
SELECT brand, model, price_vnd FROM motorcycles ORDER BY brand;
```

### 测试API
```bash
# 获取所有摩托车
curl "http://localhost:4001/api/vehicles/motorcycles"

# 按品牌筛选
curl "http://localhost:4001/api/vehicles/motorcycles?brand=Honda"

# 获取详情
curl "http://localhost:4001/api/vehicles/motorcycles/1"
```

## 🌐 API端点

- `GET /api/vehicles/motorcycles` - 获取摩托车列表
- `GET /api/vehicles/motorcycles/:id` - 获取摩托车详情
- `GET /api/vehicles/motorcycles/brands` - 获取所有品牌
- `GET /api/vehicles/motorcycles/categories` - 获取所有分类
- `POST /api/vehicles/motorcycles` - 创建摩托车（需要认证）
- `PUT /api/vehicles/motorcycles/:id` - 更新摩托车（需要认证）
- `DELETE /api/vehicles/motorcycles/:id` - 删除摩托车（需要认证）

### 查询参数

- `page`: 页码（默认：1）
- `limit`: 每页数量（默认：12）
- `brand`: 品牌筛选
- `category`: 类别筛选
- `fuel_type`: 燃料类型筛选（Xăng/Điện）
- `min_price`: 最低价格
- `max_price`: 最高价格
- `search`: 搜索关键词

## ⚠️ 注意事项

1. **法律合规**
   - 本爬虫收集的数据基于公开市场信息
   - 请遵守网站使用条款和robots.txt规则
   - 不建议频繁爬取以避免对源网站造成负担

2. **数据更新**
   - 市场价格可能随时变化，建议定期更新
   - 新车型上市时需要手动添加到爬虫

3. **数据质量**
   - 价格信息仅供参考，实际以经销商为准
   - 技术参数来源于官方资料

## 📝 待办事项

- [ ] 添加更多品牌（如Kawasaki, KTM等）
- [ ] 实现自动爬取官网数据（需要处理JavaScript渲染）
- [ ] 添加图片下载功能
- [ ] 实现定时自动更新
- [ ] 添加价格历史追踪
- [ ] 支持多语言（越南语/英语/中文）

## 🆘 故障排查

### 问题：数据导入失败
```bash
# 检查JSON文件是否存在
ls -la /root/越南摩托汽车网站/backend/src/scripts/data/motorcycles_data.json

# 验证JSON格式
python3 -m json.tool motorcycles_data.json
```

### 问题：API返回旧数据
```bash
# 检查数据库文件路径
grep DB_PATH /var/www/vietnam-moto-auto/backend/.env

# 重启后端服务
pkill -9 -f "node dist/index.js"
cd /var/www/vietnam-moto-auto/backend
node dist/index.js
```

### 问题：前端不显示数据
```bash
# 检查CORS配置
curl -I -H "Origin: http://47.237.79.9:4321" "http://47.237.79.9:4001/api/vehicles/motorcycles"

# 重新编译前端
cd /root/越南摩托汽车网站/frontend
npm run build
cp -r dist/* /var/www/vietnam-moto-auto/frontend/dist/
```

## 📧 联系方式

如有问题或建议，请联系项目维护者。

---

**更新时间**: 2025-10-11  
**版本**: v1.0.0

