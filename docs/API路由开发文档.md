# 越南摩托汽车网站 - API 路由开发文档

## 📋 文档概述

本文档详细记录越南摩托汽车网站后端 API 的所有路由接口，包括请求参数、响应格式、状态码和使用示例。

### API 信息
- **基础URL（开发）**: `http://localhost:4001/api`
- **基础URL（生产 - 域名+SSL）**: `https://vietmoto.top/api` ⭐ 推荐
- **基础URL（生产 - IP访问）**: `http://47.237.79.9:4001/api` ⚠️ 已弃用
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`
- **字符编码**: UTF-8

### ⚠️ 重要说明：域名+SSL部署

**当前生产环境配置**：
- ✅ 使用域名：`vietmoto.top`
- ✅ HTTPS加密：Let's Encrypt SSL证书
- ✅ Nginx反向代理：所有API请求通过HTTPS代理到后端
- ✅ 前端API调用：使用相对路径 `/api`（自动HTTPS）

**前端API调用规范**：
```typescript
// ✅ 正确：使用相对路径（域名+SSL环境）
const API_BASE_URL = '/api';
fetch('/api/vehicles/motorcycles');

// ❌ 错误：硬编码HTTP地址（导致Mixed Content错误）
const API_BASE_URL = 'http://47.237.79.9:4001/api';
fetch('http://47.237.79.9:4001/api/vehicles/motorcycles');

// ❌ 错误：使用环境变量配置HTTP地址
const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://...';
```

**重要提醒**：
- 🚫 不要使用 `.env.production` 配置 `PUBLIC_API_URL`
- ✅ 所有前端API调用使用相对路径 `/api`
- ✅ Nginx自动代理到后端：`/api/* → http://127.0.0.1:4001/api/*`
- ✅ 浏览器看到的都是HTTPS请求

---

---

## 🔧 API连接修复与配置（2025-10-14）

### 问题背景
在域名+SSL部署后，前端无法获取后端数据，出现"Mixed Content"错误。

### 根本原因
1. **硬编码HTTP地址**：前端代码使用 `http://47.237.79.9:4001/api`
2. **环境变量配置错误**：`.env.production` 设置了HTTP地址
3. **未使用Nginx代理**：直接访问后端导致HTTPS页面加载HTTP资源被阻止

### 修复方案

#### 1. 删除所有环境变量文件
```bash
rm -f /root/越南摩托汽车网站/frontend/.env*
```

#### 2. 更新所有API服务文件
修复的文件清单：
- ✅ `frontend/src/services/marketplaceApi.ts`
- ✅ `frontend/src/services/reviewsApi.ts`
- ✅ `frontend/src/services/qaApi.ts`
- ✅ `frontend/src/components/MarketplaceSection.tsx`
- ✅ `frontend/src/config/api.ts`
- ✅ `frontend/src/pages/sitemap.xml.ts`
- ✅ `frontend/src/pages/marketplace/[id].astro`
- ✅ `frontend/src/pages/cars/[slug].astro`
- ✅ `frontend/src/pages/qa/[id].astro`
- ✅ `frontend/src/pages/reviews/[slug].astro`
- ✅ `frontend/src/lib/api/carsApi.ts`
- ✅ `frontend/src/lib/api/motorcyclesApi.ts`

#### 3. API调用规范

**修复前（❌ 错误）**：
```typescript
const API_URL = 'http://47.237.79.9:4001/api';
const API_BASE_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:4001/api';
```

**修复后（✅ 正确）**：
```typescript
const API_BASE_URL = '/api';  // 相对路径，通过Nginx代理
```

#### 4. Nginx代理配置

```nginx
# API代理配置（/etc/nginx/conf.d/vietmoto.conf）
location /api/ {
    proxy_pass http://127.0.0.1:4001;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cache_bypass $http_upgrade;
}
```

#### 5. API请求流程

```
浏览器 (HTTPS)
  ↓ GET https://vietmoto.top/api/vehicles/motorcycles
Nginx (443端口)
  ↓ proxy_pass
后端 (http://127.0.0.1:4001/api/vehicles/motorcycles)
  ↓ 返回JSON数据
浏览器 ✅ 成功（全程HTTPS）
```

### 验证测试

```bash
# 1. API直接测试
curl https://vietmoto.top/api/vehicles/cars?limit=2
# ✅ HTTP 200
# ✅ 返回正确的JSON数据

# 2. 健康检查
curl https://vietmoto.top/health
# ✅ {"status":"OK"}

# 3. 测评API
curl https://vietmoto.top/api/reviews?limit=5
# ✅ 返回测评列表

# 4. 二手市场API
curl https://vietmoto.top/api/marketplace?limit=5
# ✅ 返回二手车辆列表
```

### 修复结果

| 测试项 | 结果 | 说明 |
|--------|------|------|
| 后端服务 | ✅ 运行中 | 端口4001 |
| API健康检查 | ✅ 正常 | /health返回200 |
| 汽车API | ✅ 正常 | 返回124条数据 |
| 摩托车API | ✅ 正常 | 返回126条数据 |
| 问答API | ✅ 正常 | 返回11条数据 |
| 二手市场API | ✅ 正常 | 返回648条数据 |
| Nginx代理 | ✅ 正常 | 正确转发请求 |
| HTTPS访问 | ✅ 正常 | 无Mixed Content错误 |

### 最佳实践总结

1. **域名+SSL环境**：
   - ✅ 前端使用相对路径 `/api`
   - ✅ 通过Nginx HTTPS代理访问后端
   - ✅ 不使用 `.env.production` 配置API地址

2. **开发环境**：
   - ✅ 可以使用 `http://localhost:4001/api`
   - ✅ 或使用相对路径 `/api`（需要Nginx）

3. **SSR环境**（⚠️ 重要 - 2025-10-14更新）：
   ```typescript
   // Astro SSR页面（服务器端渲染）
   // ✅ 正确：使用完整的内网地址
   const API_URL = 'http://localhost:4001/api';
   const response = await fetch(`${API_URL}/vehicles/cars/slug/${slug}`);
   
   // 客户端JavaScript（浏览器环境）
   // ✅ 正确：使用相对路径，通过Nginx代理
   const API_BASE_URL = '/api';
   fetch(`${API_BASE_URL}/reviews/slug/${slug}`);
   ```
   
   **重要说明**：
   - Astro在服务器端执行时，无法解析相对路径 `/api`
   - 必须使用完整URL `http://localhost:4001/api`
   - 客户端JavaScript可以使用相对路径（通过Nginx代理）

---

## 🌐 全局规范

### 1. 请求头

#### 通用请求头
```http
Content-Type: application/json
Accept: application/json
Origin: https://vietmoto.top
```

#### 认证请求头
```http
Authorization: Bearer <jwt_token>
```

---

### 2. 响应格式

#### 成功响应
```json
{
  "success": true,
  "message": "操作成功描述",
  "data": { },
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100,
    "totalPages": 10
  }
}
```

#### 错误响应
```json
{
  "success": false,
  "message": "错误描述",
  "error": "详细错误信息",
  "code": "ERROR_CODE"
}
```

---

### 3. HTTP 状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 权限不足 |
| 404 | Not Found | 资源不存在 |
| 422 | Unprocessable Entity | 验证失败 |
| 429 | Too Many Requests | 请求过于频繁 |
| 500 | Internal Server Error | 服务器错误 |

---

### 4. 分页参数

所有列表接口支持分页：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | number | 1 | 页码 |
| limit | number | 10 | 每页数量 |

---

## 📰 测评模块 API（Reviews）

### 路由前缀
`/api/reviews`

### 实现状态
✅ **完整实现** - 包含控制器和服务层

### 说明
测评模块用于管理车辆测评文章（原News模块），包括摩托车、汽车的专业测评和用户评价。系统支持定时自动生成测评内容（每40分钟一条）。

---

### 1. 创建测评

#### 端点
```
POST /api/reviews
POST /api/reviews/webhook  (n8n Webhook专用)
```

#### 请求体
```json
{
  "title": "Honda Winner X 2024 ra mắt tại Việt Nam",
  "content": "<p>Nội dung chi tiết của bài viết...</p>",
  "summary": "Tóm tắt ngắn gọn về nội dung",
  "category": "Xe máy",
  "author_name": "Nguyễn Văn A",
  "featured_image": "https://example.com/image.jpg",
  "status": "published"
}
```

#### 字段说明
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | ✅ | 新闻标题 |
| content | string | ✅ | 新闻内容（HTML格式） |
| summary | string | ❌ | 摘要（自动提取如未提供） |
| category | string | ❌ | 分类（Xe máy/Ô tô/Tin tức） |
| author_name | string | ❌ | 作者名称 |
| featured_image | string | ❌ | 特色图片URL |
| status | string | ❌ | 状态（draft/published，默认draft） |

#### 响应示例
```json
{
  "success": true,
  "message": "News created successfully",
  "data": {
    "id": "uuid-123",
    "title": "Honda Winner X 2024 ra mắt tại Việt Nam",
    "slug": "honda-winner-x-2024-ra-mat-tai-viet-nam",
    "created_at": "2025-10-12T00:00:00.000Z"
  }
}
```

---

### 2. 获取测评列表

#### 端点
```
GET /api/reviews
```

#### 查询参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | number | 1 | 页码 |
| limit | number | 10 | 每页数量 |
| category | string | - | 分类筛选 |
| status | string | published | 状态筛选 |
| is_featured | boolean | - | 是否精选 |
| search | string | - | 搜索关键词 |

#### 请求示例
```bash
# 生产环境（域名+SSL）
curl "https://vietmoto.top/api/reviews"

# 开发环境
curl "https://vietmoto.top/api/reviews"

# 筛选摩托车测评
curl "https://vietmoto.top/api/reviews?category=Xe+máy&limit=20"

# 搜索关键词
curl "https://vietmoto.top/api/reviews?search=Honda"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "title": "Honda Winner X 2024 ra mắt",
      "slug": "honda-winner-x-2024-ra-mat",
      "summary": "Tóm tắt...",
      "featured_image": "https://...",
      "category": "Xe máy",
      "author_name": "Nguyễn Văn A",
      "view_count": 1250,
      "published_at": "2025-10-11T00:00:00.000Z",
      "created_at": "2025-10-11T00:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "totalPages": 5
  }
}
```

---

### 3. 获取最新测评

#### 端点
```
GET /api/reviews/latest
```

#### 查询参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | number | 6 | 返回数量 |

#### 请求示例
```bash
# 生产环境
curl "https://vietmoto.top/api/reviews/latest?limit=6"

# 开发环境
curl "https://vietmoto.top/api/reviews/latest?limit=6"
```

---

### 4. 获取测评详情（通过 Slug）

#### 端点
```
GET /api/reviews/slug/:slug
```

#### 路径参数
- `slug`: 测评文章的URL友好标识

#### 请求示例
```bash
# 生产环境
curl "https://vietmoto.top/api/reviews/slug/honda-winner-x-2024-ra-mat"

# 开发环境
curl "https://vietmoto.top/api/reviews/slug/honda-winner-x-2024-ra-mat"
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "id": "1",
    "title": "Honda Winner X 2024 ra mắt tại Việt Nam",
    "slug": "honda-winner-x-2024-ra-mat",
    "content": "<p>Nội dung đầy đủ...</p>",
    "summary": "Tóm tắt...",
    "featured_image": "https://...",
    "category": "Xe máy",
    "author_name": "Nguyễn Văn A",
    "view_count": 1251,
    "is_featured": false,
    "status": "published",
    "published_at": "2025-10-11T00:00:00.000Z",
    "created_at": "2025-10-11T00:00:00.000Z",
    "updated_at": "2025-10-12T00:00:00.000Z"
  }
}
```

**特性**：
- ✅ 自动增加浏览次数（view_count + 1）

---

### 5. 获取相关测评

#### 端点
```
GET /api/reviews/slug/:slug/related
```

#### 查询参数
- `limit`: 返回数量（默认4）

#### 请求示例
```bash
# 生产环境
curl "https://vietmoto.top/api/reviews/slug/honda-winner-x-2024-ra-mat/related?limit=4"

# 开发环境
curl "https://vietmoto.top/api/reviews/slug/honda-winner-x-2024-ra-mat/related?limit=4"
```

---

### 6. 获取测评详情（通过 ID）

#### 端点
```
GET /api/reviews/:id
```

---

### 7. 获取所有分类

#### 端点
```
GET /api/reviews/categories
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    { "category": "Xe máy", "count": 25 },
    { "category": "Ô tô", "count": 30 },
    { "category": "Tin tức", "count": 15 }
  ]
}
```

---

### 8. 更新测评

#### 端点
```
PUT /api/reviews/:id
```

#### 权限
🔒 需要管理员权限

#### 请求体
同创建测评（字段可选）

---

### 9. 删除测评

#### 端点
```
DELETE /api/reviews/:id
```

#### 权限
🔒 需要管理员权限

---

## 🏍️ 摩托车模块 API

### 路由前缀
`/api/vehicles/motorcycles`

### 实现状态
✅ **完整实现** - 包含控制器和服务层

---

### 1. 创建摩托车

#### 端点
```
POST /api/vehicles/motorcycles
POST /api/vehicles/motorcycles/webhook  (n8n Webhook)
```

#### 请求体
```json
{
  "brand": "Honda",
  "model": "Winner X",
  "year": 2024,
  "category": "Sport",
  "price_vnd": 48000000,
  "engine_cc": 149,
  "engine_type": "Xi-lanh đơn, 4 kỳ",
  "power_hp": 17.1,
  "torque_nm": 14.4,
  "transmission": "Số sàn 6 cấp",
  "fuel_capacity_l": 4.7,
  "weight_kg": 127,
  "seat_height_mm": 795,
  "wheelbase_mm": 1328,
  "ground_clearance_mm": 165,
  "abs": true,
  "smart_key": false,
  "features": "...",
  "description": "..."
}
```

**注意**：字段名必须与数据库匹配（category、price_vnd、view_count等）

---

### 2. 获取摩托车列表

#### 端点
```
GET /api/vehicles/motorcycles
```

#### 查询参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | number | 1 | 页码 |
| limit | number | 12 | 每页数量 |
| brand | string | - | 品牌筛选（Honda/Yamaha/Suzuki等） |
| category | string | - | 类型筛选（Sport/Touring/Cruiser等）⚠️ 使用category |
| fuel_type | string | - | 燃料类型（Gasoline/Electric等） |
| min_price | number | - | 最低价格 |
| max_price | number | - | 最高价格 |
| year | number | - | 年份 |
| status | string | active | 状态筛选 |
| search | string | - | 搜索关键词 |

#### 请求示例
```bash
# 获取所有Honda摩托车
curl "https://vietmoto.top/api/vehicles/motorcycles?brand=Honda"

# 筛选运动型摩托车
curl "https://vietmoto.top/api/vehicles/motorcycles?category=Sport"

# 价格筛选
curl "https://vietmoto.top/api/vehicles/motorcycles?min_price=40000000&max_price=60000000&limit=20"

# ✨ 按浏览量排序获取热门车型（首页精选使用）
curl "https://vietmoto.top/api/vehicles/motorcycles?fuel_type=Xăng&limit=6&sort=view_count&order=DESC"

# 按价格从低到高排序
curl "https://vietmoto.top/api/vehicles/motorcycles?sort=price_vnd&order=ASC"

# 获取最新车型
curl "https://vietmoto.top/api/vehicles/motorcycles?sort=created_at&order=DESC&limit=10"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "brand": "Honda",
      "model": "Winner X",
      "year": 2024,
      "category": "Sport",
      "price_vnd": 48000000,
      "engine_cc": 149,
      "power_hp": 17.1,
      "abs": true,
      "smart_key": false,
      "view_count": 520,
      "rating": 4.5,
      "status": "active",
      "created_at": "2025-10-11T00:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 12,
    "total": 31,
    "totalPages": 3
  }
}
```

---

### 3. 获取摩托车详情

#### 端点
```
GET /api/vehicles/motorcycles/:id
```

#### 路径参数
- `id`: 摩托车ID

#### 请求示例
```bash
curl "https://vietmoto.top/api/vehicles/motorcycles/1"
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "id": 1,
    "brand": "Honda",
    "model": "Winner X",
    "year": 2024,
    "category": "Sport",
    "price_vnd": 48000000,
    "engine_cc": 149,
    "engine_type": "Xi-lanh đơn, 4 kỳ, làm mát bằng dung dịch",
    "power_hp": 17.1,
    "power_rpm": 9000,
    "torque_nm": 14.4,
    "torque_rpm": 7000,
    "transmission": "Số sàn 6 cấp",
    "fuel_type": "Gasoline",
    "fuel_capacity_l": 4.7,
    "weight_kg": 127,
    "seat_height_mm": 795,
    "wheelbase_mm": 1328,
    "ground_clearance_mm": 165,
    "abs": true,
    "smart_key": false,
    "display_type": "Kỹ thuật số toàn phần",
    "features": "...",
    "description": "...",
    "image_url": "...",
    "rating": 4.5,
    "view_count": 521,
    "status": "active",
    "created_at": "2025-10-11T00:00:00.000Z",
    "updated_at": "2025-10-12T00:00:00.000Z"
  }
}
```

**特性**：
- ✅ 自动增加浏览次数（view_count + 1）

**字段说明**：
- `category`: 类型分类（不是 type）
- `price_vnd`: 价格（越南盾）
- `view_count`: 浏览次数（不是 views）
- `abs`: 是否有ABS系统
- `smart_key`: 是否有智能钥匙

---

### 4. 获取精选摩托车

#### 端点
```
GET /api/vehicles/motorcycles/featured
```

#### 查询参数
- `limit`: 返回数量（默认6）

---

### 5. 获取摩托车品牌列表

#### 端点
```
GET /api/vehicles/motorcycles/brands
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    { "brand": "Honda", "count": 6 },
    { "brand": "Yamaha", "count": 5 },
    { "brand": "Suzuki", "count": 2 },
    { "brand": "VinFast", "count": 3 }
  ]
}
```

---

### 6. 获取摩托车分类列表

#### 端点
```
GET /api/vehicles/motorcycles/categories
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    { "category": "Sport", "count": 8 },
    { "category": "Scooter", "count": 10 },
    { "category": "Underbone", "count": 4 }
  ]
}
```

**注意**：返回的字段是 `category`（不是 `type`）

---

### 7. 更新摩托车

#### 端点
```
PUT /api/vehicles/motorcycles/:id
```

#### 权限
🔒 需要管理员权限

---

### 8. 删除摩托车

#### 端点
```
DELETE /api/vehicles/motorcycles/:id
```

#### 权限
🔒 需要管理员权限

---

## 🚗 汽车模块 API

### 路由前缀
`/api/vehicles/cars`

### 实现状态
✅ **完整实现** - 包含控制器和服务层

---

### 1. 创建汽车

#### 端点
```
POST /api/vehicles/cars
POST /api/vehicles/cars/webhook  (n8n Webhook)
```

#### 请求体
```json
{
  "brand": "Toyota",
  "model": "Vios",
  "year": 2024,
  "category": "Sedan hạng B",
  "slug": "toyota-vios-2024",
  "price_vnd": 458000000,
  "seating_capacity": 5,
  "engine_capacity_l": 1.5,
  "engine_type": "4 xi-lanh thẳng hàng, DOHC, Dual VVT-i",
  "power_hp": 107,
  "torque_nm": 140,
  "fuel_type": "Xăng",
  "transmission": "CVT",
  "drive_type": "FWD",
  "description": "...",
  "features": "..."
}
```

---

### 2. 获取汽车列表

#### 端点
```
GET /api/vehicles/cars
```

#### 查询参数
|| 参数 | 类型 | 默认值 | 说明 |
||------|------|--------|------|
|| page | number | 1 | 页码 |
|| limit | number | 12 | 每页数量 |
|| brand | string | - | 品牌筛选（Toyota/Honda/VinFast等） |
|| category | string | - | 类型筛选（Sedan/SUV/MPV等） |
|| fuel_type | string | - | 燃料类型（Xăng/Điện/Hybrid等） |
|| min_price | number | - | 最低价格 |
|| max_price | number | - | 最高价格 |
|| year | number | - | 年份 |
|| seating_capacity | number | - | 座位数 |
|| status | string | active | 状态筛选 |
|| search | string | - | 搜索关键词 |
|| **sort** | **string** | **year** | **排序字段（view_count/price_vnd/year）** ✨新增 |
|| **order** | **string** | **DESC** | **排序方向（ASC/DESC）** ✨新增 |

#### 请求示例
```bash
# 获取所有Toyota汽车
curl "https://vietmoto.top/api/vehicles/cars?brand=Toyota"

# 筛选SUV车型
curl "https://vietmoto.top/api/vehicles/cars?category=SUV"

# ✨ 按浏览量排序获取热门汽车（首页精选使用）
curl "https://vietmoto.top/api/vehicles/cars?fuel_type=Điện&limit=6&sort=view_count&order=DESC"

# 按价格从低到高排序
curl "https://vietmoto.top/api/vehicles/cars?sort=price_vnd&order=ASC&limit=20"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "brand": "Toyota",
      "model": "Vios",
      "year": 2024,
      "category": "Sedan hạng B",
      "slug": "toyota-vios-2024",
      "price_vnd": 458000000,
      "seating_capacity": 5,
      "power_hp": 107,
      "fuel_type": "Xăng",
      "view_count": 9000,
      "rating": 4.6,
      "status": "active",
      "created_at": "2025-10-11T00:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 12,
    "total": 124,
    "pages": 11
  }
}
```

---

### 3. 获取汽车详情

#### 端点
```
GET /api/vehicles/cars/:id          通过ID获取
GET /api/vehicles/cars/slug/:slug   通过slug获取（推荐）
```

#### 路径参数
- `id`: 汽车ID
- `slug`: URL友好标识（如：toyota-vios-2024）

#### 请求示例
```bash
# 通过slug获取（推荐）
curl "https://vietmoto.top/api/vehicles/cars/slug/toyota-vios-2024"

# 通过ID获取
curl "https://vietmoto.top/api/vehicles/cars/1"
```

**特性**：
- ✅ 自动增加浏览次数（view_count + 1）

---

### 4. 获取汽车品牌列表

#### 端点
```
GET /api/vehicles/cars/brands
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    { "brand": "Toyota", "count": 15 },
    { "brand": "Honda", "count": 12 },
    { "brand": "VinFast", "count": 8 },
    { "brand": "Hyundai", "count": 10 }
  ]
}
```

---

### 5. 获取汽车分类列表

#### 端点
```
GET /api/vehicles/cars/categories
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    { "category": "Sedan", "count": 35 },
    { "category": "SUV", "count": 45 },
    { "category": "MPV", "count": 20 }
  ]
}
```

---

### 6. 更新汽车

#### 端点
```
PUT /api/vehicles/cars/:id
```

#### 权限
🔒 需要管理员权限

---

### 7. 删除汽车

#### 端点
```
DELETE /api/vehicles/cars/:id
```

#### 权限
🔒 需要管理员权限

---

## 💬 问答模块 API

### 路由前缀
`/api/qa`

### 实现状态
✅ **完整实现** - 包含AI自动生成功能

### 说明
问答模块基于AI（LangChain + GPT-4）自动生成车辆相关问答内容，每小时自动生成1条Q&A。支持按分类、车型筛选，以及多种排序方式（最新、最热、最受欢迎）。

---

### 1. 获取问题列表

#### 端点
```
GET /api/qa
```

#### 查询参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | number | 1 | 页码 |
| limit | number | 20 | 每页数量 |
| category | string | - | 分类筛选（购买建议/维修保养/技术对比等） |
| vehicle_type | string | - | 车型筛选（motorcycle/car） |
| sort | string | latest | 排序方式（latest=最新/popular=浏览最多/hot=最热门） |

#### 排序说明
- `latest`: 按创建时间倒序（最新发布）
- `popular`: 按浏览量倒序（view_count DESC）
- `hot`: 按回答数和投票数倒序（answers_count + votes_count DESC）

#### 请求示例
```bash
# 获取所有问题
curl "https://vietmoto.top/api/qa"

# 筛选摩托车相关问题
curl "https://vietmoto.top/api/qa?vehicle_type=motorcycle&limit=20"

# 获取最热门问题
curl "https://vietmoto.top/api/qa?sort=hot&limit=10"

# 筛选购买建议类问题
curl "https://vietmoto.top/api/qa?category=购买建议"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Honda Winner X và Yamaha Exciter 155 nên chọn xe nào?",
      "content": "Chi tiết câu hỏi...",
      "category": "购买建议",
      "vehicle_type": "motorcycle",
      "status": "open",
      "view_count": 520,
      "answers_count": 3,
      "votes_count": 15,
      "created_at": "2025-10-13T00:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "totalPages": 3
  }
}
```

---

### 2. 获取问题详情

#### 端点
```
GET /api/qa/:id
```

#### 路径参数
- `id`: 问题ID

#### 请求示例
```bash
curl "https://vietmoto.top/api/qa/1"
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "question": {
      "id": 1,
      "title": "Honda Winner X và Yamaha Exciter 155 nên chọn xe nào?",
      "content": "Chi tiết câu hỏi...",
      "category": "购买建议",
      "vehicle_type": "motorcycle",
      "view_count": 521,
      "answers_count": 3,
      "votes_count": 15,
      "status": "open",
      "created_at": "2025-10-13T00:00:00.000Z"
    },
    "answers": [
      {
        "id": 1,
        "question_id": 1,
        "content": "Chi tiết trả lời...",
        "votes_count": 8,
        "is_accepted": false,
        "created_at": "2025-10-13T01:00:00.000Z"
      }
    ]
  }
}
```

**特性**：
- ✅ 自动增加浏览次数（view_count + 1）
- ✅ 返回问题及其所有回答

---

### 3. 手动生成问答（调试用）

#### 端点
```
POST /api/qa/generate
```

#### 说明
手动触发AI生成一条问答内容（正常由定时任务每小时自动执行）。

#### 权限
🔓 无需认证（生产环境建议加权限控制）

#### 请求示例
```bash
curl -X POST "http://localhost:4001/api/qa/generate"
```

#### 响应示例
```json
{
  "success": true,
  "message": "生成成功"
}
```

---

### 定时任务
系统自动运行 **QAScheduler**：
- 频率：每小时生成1条问答
- AI模型：GPT-4（通过LangChain）
- 自动分类、打标签、生成回答

---

## 🛒 二手交易模块 API

### 路由前缀
`/api/marketplace`

### 实现状态
✅ **完整实现** - 包含自动数据同步功能

### 说明
二手交易模块集成Chợ Tốt平台数据，自动抓取和同步二手车辆信息。系统每12小时自动更新数据，支持丰富的筛选和排序功能。

---

### 1. 获取二手车辆列表

#### 端点
```
GET /api/marketplace
```

#### 查询参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | number | 1 | 页码 |
| limit | number | 12 | 每页数量 |
| type | string | motorcycle | 车辆类型（motorcycle/car） |
| vehicle_type | string | - | 详细分类（moto-gas/moto-electric/car-gas/car-electric） |
| brand | string | - | 品牌筛选 |
| minPrice | number | - | 最低价格（VND） |
| maxPrice | number | - | 最高价格（VND） |
| minYear | number | - | 最早年份 |
| maxYear | number | - | 最晚年份 |
| city | string | - | 城市筛选 |
| sort | string | latest | 排序方式（latest/price_asc/price_desc/popular/year_desc/year_asc） |

#### 排序说明
- `latest`: 按发布时间倒序（最新发布）
- `price_asc`: 按价格升序（便宜优先）
- `price_desc`: 按价格降序（贵的优先）
- `popular`: 按浏览量倒序（最受欢迎）
- `year_desc`: 按年份倒序（最新年份）
- `year_asc`: 按年份升序（最旧年份）

#### 请求示例
```bash
# 获取所有二手摩托车
curl "https://vietmoto.top/api/marketplace?type=motorcycle"

# 筛选燃油摩托车
curl "https://vietmoto.top/api/marketplace?vehicle_type=moto-gas&limit=20"

# 筛选Honda品牌，价格2000-4000万
curl "https://vietmoto.top/api/marketplace?brand=Honda&minPrice=20000000&maxPrice=40000000"

# 按价格从低到高排序
curl "https://vietmoto.top/api/marketplace?sort=price_asc"

# 筛选河内市的车辆
curl "https://vietmoto.top/api/marketplace?city=Hà Nội"

# 获取最热门的二手车
curl "https://vietmoto.top/api/marketplace?type=car&sort=popular&limit=10"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "external_id": "123456",
      "external_url": "https://xe.chotot.com/...",
      "source": "chotot",
      "type": "motorcycle",
      "vehicle_type": "moto-gas",
      "brand": "Honda",
      "model": "Winner X",
      "year": 2022,
      "price": 35000000,
      "title": "Honda Winner X 2022 - Màu đỏ đen",
      "description": "Xe chính chủ, zin 100%...",
      "mileage": 8500,
      "condition_text": "Còn mới, đẹp long lanh",
      "condition_rating": 4.5,
      "image_url": "https://...",
      "images": ["https://...", "https://..."],
      "city": "Hà Nội",
      "district": "Cầu Giấy",
      "ward": null,
      "seller_name": "Nguyễn Văn A",
      "seller_avatar": null,
      "seller_rating": 4.8,
      "seller_sold_count": 12,
      "view_count": 520,
      "favorites_count": 35,
      "status": "active",
      "published_at": "2025-10-12T00:00:00.000Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 12,
    "total": 245,
    "totalPages": 21
  }
}
```

---

### 2. 获取车辆详情

#### 端点
```
GET /api/marketplace/:id
```

#### 路径参数
- `id`: 车辆ID

#### 请求示例
```bash
curl "https://vietmoto.top/api/marketplace/1"
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "id": 1,
    "external_id": "123456",
    "external_url": "https://xe.chotot.com/tp-ho-chi-minh/mua-ban-xe-may/honda/winner-x/123456.htm",
    "source": "chotot",
    "type": "motorcycle",
    "vehicle_type": "moto-gas",
    "brand": "Honda",
    "model": "Winner X",
    "year": 2022,
    "price": 35000000,
    "title": "Honda Winner X 2022 - Màu đỏ đen",
    "description": "Xe chính chủ, zin 100%, bảo dưỡng định kỳ...",
    "mileage": 8500,
    "condition_text": "Còn mới, đẹp long lanh",
    "condition_rating": 4.5,
    "image_url": "https://...",
    "images": ["https://img1.jpg", "https://img2.jpg"],
    "city": "Hà Nội",
    "district": "Cầu Giấy",
    "seller_name": "Nguyễn Văn A",
    "seller_rating": 4.8,
    "seller_sold_count": 12,
    "view_count": 521,
    "favorites_count": 35,
    "status": "active",
    "published_at": "2025-10-12T00:00:00.000Z",
    "created_at": "2025-10-12T00:00:00.000Z",
    "updated_at": "2025-10-13T00:00:00.000Z"
  }
}
```

**特性**：
- ✅ 自动增加浏览次数（view_count + 1）
- ✅ 解析JSON字段（images数组）

---

### 3. 手动同步数据

#### 端点
```
POST /api/marketplace/sync
```

#### 说明
手动触发从Chợ Tốt同步最新数据（正常由定时任务每12小时自动执行）。

#### 权限
🔓 无需认证（生产环境建议加权限控制）

#### 请求示例
```bash
curl -X POST "http://localhost:4001/api/marketplace/sync"
```

#### 响应示例
```json
{
  "success": true,
  "message": "Data sync completed",
  "data": {
    "motorcycles": 156,
    "cars": 89,
    "total": 245
  }
}
```

---

### 4. 重新分类数据

#### 端点
```
POST /api/marketplace/reclassify
```

#### 说明
重新分类现有数据，修复分类错误（将数据重新分类为moto-gas/moto-electric/car-gas/car-electric）。

#### 请求示例
```bash
curl -X POST "http://localhost:4001/api/marketplace/reclassify"
```

#### 响应示例
```json
{
  "success": true,
  "message": "Data reclassification completed",
  "data": {
    "updated": 245,
    "errors": 0
  }
}
```

---

### 5. 获取统计信息

#### 端点
```
GET /api/marketplace/stats/summary
```

#### 说明
获取二手市场的统计摘要信息。

#### 请求示例
```bash
curl "https://vietmoto.top/api/marketplace/stats/summary"
```

#### 响应示例
```json
{
  "success": true,
  "data": {
    "total": 245,
    "brands": 15,
    "cities": 8,
    "avgPrice": 32500000,
    "minPrice": 8000000,
    "maxPrice": 150000000
  }
}
```

---

### 数据来源
- **平台**: Chợ Tốt (xe.chotot.com)
- **更新频率**: 每12小时自动同步（MarketplaceScheduler）
- **数据分类**: 自动识别燃油/电动，摩托车/汽车

---

## 🗺️ Sitemap模块 API

### 路由前缀
`/api/sitemap`

### 实现状态
✅ **完整实现** - 专用于SEO sitemap生成

### 说明
Sitemap模块提供专用API端点用于生成SEO sitemap。与其他API不同，这些端点：
- **只返回数据库中的真实数据**（不包含外部API数据）
- **只返回active/published状态的内容**
- **限制返回数量**（每个端点最多1000条）
- **优化查询性能**（只查询必要字段：id, slug, lastmod）

**使用场景**：
- 前端动态sitemap生成（`/sitemap.xml`、`/sitemap-*.xml`）
- Google Search Console提交
- SEO优化和索引管理

---

### 1. 获取摩托车Sitemap数据

#### 端点
```
GET /api/sitemap/motorcycles
```

#### 说明
获取所有active状态的摩托车记录，用于sitemap生成。

#### 请求示例
```bash
curl "http://localhost:4001/api/sitemap/motorcycles"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "lastmod": "2025-10-14T10:30:00.000Z"
    },
    {
      "id": 2,
      "lastmod": "2025-10-13T15:20:00.000Z"
    }
  ]
}
```

#### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 摩托车ID |
| lastmod | string | 最后修改时间（ISO 8601格式） |

#### 数据来源
- **表**: `motorcycles`
- **条件**: `status = 'active'`
- **排序**: 默认按ID
- **限制**: 最多1000条

---

### 2. 获取汽车Sitemap数据

#### 端点
```
GET /api/sitemap/cars
```

#### 说明
获取所有active状态的汽车记录，用于sitemap生成。

#### 请求示例
```bash
curl "http://localhost:4001/api/sitemap/cars"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "slug": "toyota-vios-2024",
      "lastmod": "2025-10-14T10:30:00.000Z"
    },
    {
      "id": 2,
      "slug": "honda-city-2024",
      "lastmod": "2025-10-13T15:20:00.000Z"
    }
  ]
}
```

#### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 汽车ID |
| slug | string | URL友好标识（用于构建URL） |
| lastmod | string | 最后修改时间（ISO 8601格式） |

#### 数据来源
- **表**: `cars`
- **条件**: `status = 'active'`
- **排序**: 默认按ID
- **限制**: 最多1000条

---

### 3. 获取测评Sitemap数据

#### 端点
```
GET /api/sitemap/reviews
```

#### 说明
获取所有published状态的测评文章，用于sitemap生成。

#### 请求示例
```bash
curl "http://localhost:4001/api/sitemap/reviews"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "slug": "honda-winner-x-2024-review",
      "lastmod": "2025-10-14T10:30:00.000Z"
    },
    {
      "id": 2,
      "slug": "yamaha-exciter-155-review",
      "lastmod": "2025-10-13T15:20:00.000Z"
    }
  ]
}
```

#### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 测评文章ID |
| slug | string | URL友好标识（用于构建URL） |
| lastmod | string | 发布/更新时间（优先published_at） |

#### 数据来源
- **表**: `news`
- **条件**: `status = 'published'` AND `slug IS NOT NULL`
- **排序**: 默认按ID
- **限制**: 最多1000条

---

### 4. 获取二手市场Sitemap数据

#### 端点
```
GET /api/sitemap/marketplace
```

#### 说明
获取所有active状态的二手车辆，用于sitemap生成。

#### 请求示例
```bash
curl "http://localhost:4001/api/sitemap/marketplace"
```

#### 响应示例
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "lastmod": "2025-10-14T10:30:00.000Z"
    },
    {
      "id": 2,
      "lastmod": "2025-10-13T15:20:00.000Z"
    }
  ]
}
```

#### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| id | number | 二手车辆ID |
| lastmod | string | 最后修改时间（优先updated_at） |

#### 数据来源
- **表**: `marketplace_vehicles`
- **条件**: `status = 'active'`
- **排序**: 默认按ID
- **限制**: 最多1000条

---

### Sitemap API使用最佳实践

#### 1. 性能优化
```typescript
// ✅ 推荐：只查询必要字段
const motorcycles = await Motorcycle.findAll({
  where: { status: 'active' },
  attributes: ['id', 'updated_at', 'created_at'], // 只查询需要的字段
  limit: 1000,
});

// ❌ 不推荐：查询所有字段
const motorcycles = await Motorcycle.findAll({
  where: { status: 'active' },
  limit: 1000,
});
```

#### 2. 数据过滤
```typescript
// ✅ 确保只返回有效数据
where: { 
  status: 'published',
  slug: { [Op.ne]: null } // 必须有slug才能生成URL
}
```

#### 3. 前端调用（SSR环境）
```typescript
// Astro SSR页面中调用
const API_URL = 'http://localhost:4001/api';
const response = await fetch(`${API_URL}/sitemap/motorcycles`);
const result = await response.json();

const motorcycleUrls = result.data.map(moto => ({
  loc: `https://vietmoto.top/motorcycles/${moto.id}`,
  lastmod: moto.lastmod,
  changefreq: 'weekly',
  priority: '0.7',
}));
```

#### 4. 分割Sitemap策略
```typescript
// 推荐：为每种内容类型创建独立sitemap
// sitemap-index.xml -> 指向以下文件
// - sitemap-static.xml (6个静态页面)
// - sitemap-motorcycles.xml (126个摩托车)
// - sitemap-cars.xml (124个汽车)
// - sitemap-reviews.xml (89个测评)
// - sitemap-marketplace.xml (1000个二手车辆，限制)
```

---

### 与普通API的区别

| 特性 | 普通API | Sitemap API |
|------|---------|-------------|
| **数据来源** | 数据库 + 外部API | 仅数据库 |
| **数据状态** | 所有状态 | 仅active/published |
| **返回字段** | 完整信息 | 仅id, slug, lastmod |
| **分页支持** | 是（page/limit） | 否（固定limit 1000） |
| **排序参数** | 支持多种 | 固定排序 |
| **缓存策略** | 按需 | 建议缓存1-2小时 |
| **使用场景** | 前端展示 | SEO sitemap生成 |

---

### 常见问题

**Q: 为什么要单独创建Sitemap API？**

A: 因为普通的marketplace API会包含从Chợ Tốt抓取的外部数据，这些数据对应的页面在我们网站上不存在，不应该出现在sitemap中。

**Q: 为什么限制1000条？**

A: 遵循Google sitemap最佳实践，单个sitemap文件不应超过50MB或50,000个URL。1000条是合理的分割大小。

**Q: lastmod时间从哪里来？**

A: 优先使用`updated_at`，如果没有则使用`published_at`或`created_at`。

**Q: 可以增加分页支持吗？**

A: 不建议。Sitemap应该返回所有有效数据。如果数据量超过1000，应该在前端分批调用或考虑分割成多个sitemap。

---

## 🔐 认证模块 API

### 路由前缀
`/api/auth`

### 实现状态
⏳ **占位实现** - 返回"Coming soon"响应

### 说明
认证模块端点已创建但功能未实现，当前所有端点返回占位响应。计划实现JWT认证、用户注册登录、权限管理等功能。

---

### 规划的端点

#### 1. 用户注册
```
POST /api/auth/register
```

**请求体**：
```json
{
  "username": "nguyenvana",
  "email": "nguyenvana@example.com",
  "password": "SecurePassword123!",
  "full_name": "Nguyễn Văn A",
  "phone": "0912345678"
}
```

**响应**：
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": "uuid-123",
    "username": "nguyenvana",
    "email": "nguyenvana@example.com"
  }
}
```

---

#### 2. 用户登录
```
POST /api/auth/login
```

**请求体**：
```json
{
  "email": "nguyenvana@example.com",
  "password": "SecurePassword123!"
}
```

**响应**：
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "uuid-123",
      "username": "nguyenvana",
      "email": "nguyenvana@example.com",
      "full_name": "Nguyễn Văn A",
      "avatar": null,
      "role": "user",
      "reputation_points": 0
    }
  }
}
```

---

#### 3. 用户登出
```
POST /api/auth/logout
Authorization: Bearer <token>
```

---

#### 4. 刷新 Token
```
POST /api/auth/refresh
```

**请求体**：
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

#### 5. 获取当前用户信息
```
GET /api/auth/profile
Authorization: Bearer <token>
```

---

## 👤 用户模块 API

### 路由前缀
`/api/users`

### 实现状态
⏳ **占位实现** - 返回"Coming soon"响应

### 说明
用户模块端点已创建但功能未实现，当前返回占位响应。计划实现用户资料管理、活动记录、收藏夹等功能。

---

### 规划的端点

```
# 个人资料
GET    /api/users/profile              获取当前用户资料
PUT    /api/users/profile              更新当前用户资料
POST   /api/users/avatar               上传头像

# 用户活动
GET    /api/users/me/questions         我的问题
GET    /api/users/me/answers           我的回答
GET    /api/users/me/listings          我的商品
GET    /api/users/me/favorites         我的收藏

# 用户公开信息
GET    /api/users/:id                  获取用户公开信息
GET    /api/users/:id/questions        用户的问题列表
GET    /api/users/:id/answers          用户的回答列表
```

---

## 📤 文件上传 API

### 路由前缀
`/api/upload`

### 实现状态
⏳ **占位实现** - 返回"Coming soon"响应

### 说明
文件上传模块端点已创建但功能未实现，当前返回占位响应。计划实现图片上传、文件管理、缩略图生成等功能。

---

### 规划的端点

#### 1. 上传图片
```
POST /api/upload/image
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**表单数据**：
```
file: <binary file>
type: news | motorcycle | car | listing | avatar
```

**响应**：
```json
{
  "success": true,
  "data": {
    "url": "/uploads/images/2025/10/12/abc123.jpg",
    "thumbnail_url": "/uploads/thumbnails/2025/10/12/abc123_thumb.jpg",
    "filename": "abc123.jpg",
    "size": 245678,
    "mimetype": "image/jpeg",
    "width": 1920,
    "height": 1080
  }
}
```

---

#### 2. 上传文件
```
POST /api/upload/file
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

---

#### 3. 批量上传图片
```
POST /api/upload/images
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**表单数据**：
```
files[]: <binary file 1>
files[]: <binary file 2>
files[]: <binary file 3>
```

**响应**：
```json
{
  "success": true,
  "data": [
    { "url": "/uploads/images/...", "filename": "..." },
    { "url": "/uploads/images/...", "filename": "..." }
  ]
}
```

---

## 🏥 健康检查 API

### 端点
```
GET /health
```

### 说明
无需认证，用于服务健康检查。

### 响应示例
```json
{
  "status": "OK",
  "timestamp": "2025-10-12T00:00:00.000Z",
  "uptime": 12345,
  "environment": "production"
}
```

### 使用场景
- 负载均衡器健康检查
- 监控系统探测
- 部署后验证

---

## 🔒 认证与授权

### 1. JWT Token 结构

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "id": "uuid-123",
    "username": "nguyenvana",
    "email": "nguyenvana@example.com",
    "role": "user",
    "iat": 1697040000,
    "exp": 1697644800
  }
}
```

---

### 2. 使用 Token

在请求头中携带 Token：

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  http://localhost:4001/api/users/profile
```

---

### 3. 权限级别

| 角色 | 权限 |
|------|------|
| **user** | 基础用户，可发布问题、回答、商品 |
| **moderator** | 版主，可管理评论、举报内容 |
| **admin** | 管理员，完全权限 |

---

## 🚦 速率限制

### 配置
```typescript
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15分钟
  max: 100,                  // 最多100个请求
});
```

### 应用范围
- 所有 `/api/*` 路由

### 响应
```json
{
  "error": "Too many requests from this IP, please try again later."
}
```

---

## 🌍 CORS 配置

### 允许的源
```typescript
const allowedOrigins = [
  'http://localhost:4321',
  'http://47.237.79.9:4321',
  'http://127.0.0.1:4321'
];
```

### 允许的方法
```
GET, POST, PUT, DELETE, PATCH, OPTIONS
```

### 允许的头
```
Content-Type, Authorization
```

---

## 📝 API 使用示例

### 1. JavaScript/TypeScript (Fetch)

```typescript
// 获取测评列表
async function getReviews() {
  const response = await fetch('http://localhost:4001/api/reviews?limit=10');
  const data = await response.json();
  return data;
}

// 创建测评（需要认证）
async function createReview(reviewData: any, token: string) {
  const response = await fetch('http://localhost:4001/api/reviews', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify(reviewData),
  });
  return response.json();
}
```

---

### 2. Axios

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:4001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 设置认证 Token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 获取测评
const getReviews = () => api.get('/reviews');

// 获取摩托车
const getMotorcycles = (params) => api.get('/vehicles/motorcycles', { params });
```

---

### 3. cURL 命令

```bash
# GET 请求
curl "https://vietmoto.top/api/reviews"

# POST 请求
curl -X POST "http://localhost:4001/api/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Honda Winner X 2024 Test",
    "content": "<p>Chi tiết đánh giá...</p>"
  }'

# 带认证的请求
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:4001/api/users/profile"

# 文件上传
curl -X POST "http://localhost:4001/api/upload/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@image.jpg" \
  -F "type=news"
```

---

## 🧪 API 测试

### 1. 使用 Postman

#### 环境变量设置
```
BASE_URL: http://localhost:4001
API_BASE_URL: {{BASE_URL}}/api
TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### 请求示例
```
GET {{API_BASE_URL}}/news
Authorization: Bearer {{TOKEN}}
```

---

### 2. 使用 VS Code REST Client

创建 `api-test.http` 文件：

```http
### 变量定义
@baseUrl = http://localhost:4001/api
@token = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

### 健康检查
GET http://localhost:4001/health

### 获取测评列表
GET {{baseUrl}}/reviews?limit=10

### 获取测评详情
GET {{baseUrl}}/reviews/slug/honda-winner-x-2024-ra-mat

### 创建测评
POST {{baseUrl}}/reviews
Content-Type: application/json

{
  "title": "Honda Winner X 2024 - Đánh giá chi tiết",
  "content": "<p>Nội dung đánh giá...</p>",
  "category": "Xe máy"
}

### 获取摩托车列表
GET {{baseUrl}}/vehicles/motorcycles?brand=Honda
```

---

## 📊 API 路由总览

### 已实现的路由（完整功能）✅

| 模块 | 路由前缀 | 端点数量 | 状态 | 特殊功能 |
|------|---------|---------|------|---------|
| **测评模块** | `/api/reviews` | 10个 | ✅ 完整 | 定时自动生成（40分钟/条） |
| **摩托车** | `/api/vehicles/motorcycles` | 9个 | ✅ 完整 | 支持排序、筛选 |
| **汽车** | `/api/vehicles/cars` | 9个 | ✅ 完整 | 支持排序、筛选 |
| **问答** | `/api/qa` | 3个 | ✅ 完整 | AI自动生成（每小时1条） |
| **二手市场** | `/api/marketplace` | 5个 | ✅ 完整 | 自动同步Chợ Tốt数据（12小时） |
| **Sitemap** | `/api/sitemap` | 4个 | ✅ 完整 | 专用于SEO sitemap生成 |
| **健康检查** | `/health` | 1个 | ✅ 完整 | - |

**总计**：41个完整实现的端点

**重要提示**：
- Reviews API (原News) 使用字段：`is_featured`, `view_count`, `featured_image`, `author_name`
- Motorcycles/Cars API 使用字段：`category`, `price_vnd`, `view_count`, `abs`, `smart_key`
- 所有列表API支持分页：`page`, `limit`
- 所有详情API自动增加浏览量（view_count + 1）

---

### 占位实现的路由（待开发）⏳

| 模块 | 路由前缀 | 端点数量 | 状态 | 优先级 |
|------|---------|---------|------|--------|
| **认证** | `/api/auth` | 5个 | ⏳ 占位 | 中 |
| **用户** | `/api/users` | 2个 | ⏳ 占位 | 中 |
| **上传** | `/api/upload` | 2个 | ⏳ 占位 | 中 |

**说明**：这些端点已创建但返回"Coming soon"占位响应，功能待实现。

---

## 🔍 错误处理

### 常见错误码

| 状态码 | 错误信息 | 原因 |
|--------|----------|------|
| 400 | Title and content are required | 缺少必填字段 |
| 401 | Unauthorized | 未提供Token或Token无效 |
| 403 | Forbidden | 权限不足 |
| 404 | Review not found | 资源不存在 |
| 422 | Validation failed | 数据验证失败 |
| 429 | Too many requests | 请求频率超限 |
| 500 | Internal server error | 服务器内部错误 |

---

### 错误响应示例

#### 验证错误
```json
{
  "success": false,
  "message": "Validation errors",
  "errors": [
    {
      "field": "title",
      "message": "Title is required"
    },
    {
      "field": "email",
      "message": "Email format is invalid"
    }
  ]
}
```

#### 认证错误
```json
{
  "success": false,
  "message": "Invalid token",
  "code": "INVALID_TOKEN"
}
```

#### 资源不存在
```json
{
  "success": false,
  "message": "Review not found",
  "code": "NOT_FOUND"
}
```

---

## 🛠️ 开发指南

### 1. 添加新路由

**步骤**：

1. 创建路由文件：`src/routes/example.ts`
```typescript
import { Router } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import ExampleController from '../controllers/ExampleController';

const router = Router();

router.get('/', asyncHandler(ExampleController.getList));
router.post('/', asyncHandler(ExampleController.create));
router.get('/:id', asyncHandler(ExampleController.getById));
router.put('/:id', asyncHandler(ExampleController.update));
router.delete('/:id', asyncHandler(ExampleController.delete));

export default router;
```

2. 在 `src/index.ts` 中注册：
```typescript
import exampleRoutes from './routes/example';
app.use('/api/example', exampleRoutes);
```

---

### 2. 添加中间件

```typescript
import { authenticate } from '../middleware/auth';
import { validate } from '../middleware/validator';

// 需要认证的路由
router.post('/', authenticate, asyncHandler(Controller.create));

// 需要验证的路由
router.post('/', validate, asyncHandler(Controller.create));

// 需要特定角色
router.delete('/:id', authenticate, authorize('admin'), asyncHandler(Controller.delete));
```

---

### 3. 路由测试

```typescript
// tests/routes/reviews.test.ts
import request from 'supertest';
import app from '../../src/index';

describe('Reviews Routes', () => {
  it('GET /api/reviews - 应该返回测评列表', async () => {
    const response = await request(app)
      .get('/api/reviews')
      .expect(200);

    expect(response.body.success).toBe(true);
    expect(response.body.data).toBeInstanceOf(Array);
  });

  it('POST /api/reviews - 应该创建测评', async () => {
    const reviewData = {
      title: 'Honda Winner X 2024 Test',
      content: '<p>Chi tiết đánh giá...</p>',
    };

    const response = await request(app)
      .post('/api/reviews')
      .send(reviewData)
      .expect(201);

    expect(response.body.success).toBe(true);
    expect(response.body.data).toHaveProperty('id');
  });
});
```

---

## 📚 最佳实践

### 1. RESTful 设计
- ✅ 使用正确的 HTTP 方法（GET/POST/PUT/DELETE）
- ✅ 资源名称使用复数（/reviews、/motorcycles）
- ✅ 使用嵌套路由表示关系（/questions/:id/answers）
- ✅ 使用查询参数进行筛选和分页

### 2. 版本控制
```typescript
// 方式1：URL版本
app.use('/api/v1/reviews', reviewsRoutes);
app.use('/api/v2/reviews', reviewsRoutesV2);

// 方式2：请求头版本
app.use((req, res, next) => {
  const version = req.headers['api-version'] || 'v1';
  // 根据版本路由
});
```

### 3. 错误处理
- ✅ 使用 asyncHandler 包装异步路由
- ✅ 统一的错误响应格式
- ✅ 详细的错误日志

### 4. 性能优化
- ✅ 使用 Redis 缓存常用数据
- ✅ 数据库查询优化
- ✅ 响应压缩（gzip）
- ✅ 分页限制（避免大数据量）

---

## 🔗 Webhook 集成

### n8n Webhook 端点

#### 测评 Webhook
```
POST /api/reviews/webhook
```

**用途**：从 n8n workflow 自动创建测评文章

**请求示例**（n8n）：
```json
{
  "title": "{{ $json.title }}",
  "content": "{{ $json.content }}",
  "summary": "{{ $json.summary }}",
  "category": "{{ $json.category }}",
  "featured_image": "{{ $json.image }}"
}
```

---

#### 摩托车 Webhook
```
POST /api/vehicles/motorcycles/webhook
```

**用途**：从爬虫或外部系统同步车型数据

---

#### 汽车 Webhook
```
POST /api/vehicles/cars/webhook
```

**用途**：从爬虫或外部系统同步汽车数据

---

## 🌐 完整 API 路由表

### 测评模块（10个端点）✅
```
POST   /api/reviews                      创建测评
POST   /api/reviews/webhook              创建测评（Webhook）
GET    /api/reviews                      获取测评列表
GET    /api/reviews/latest               获取最新测评
GET    /api/reviews/categories           获取所有分类
GET    /api/reviews/slug/:slug           获取测评详情（slug）
GET    /api/reviews/slug/:slug/related   获取相关测评
GET    /api/reviews/:id                  获取测评详情（ID）
PUT    /api/reviews/:id                  更新测评
DELETE /api/reviews/:id                  删除测评
```

---

### 摩托车模块（9个端点）✅
```
POST   /api/vehicles/motorcycles              创建摩托车
POST   /api/vehicles/motorcycles/webhook      创建摩托车（Webhook）
GET    /api/vehicles/motorcycles              获取摩托车列表 ✨支持sort/order参数
GET    /api/vehicles/motorcycles/featured     获取精选摩托车
GET    /api/vehicles/motorcycles/brands       获取品牌列表
GET    /api/vehicles/motorcycles/categories   获取分类列表
GET    /api/vehicles/motorcycles/:id          获取摩托车详情
PUT    /api/vehicles/motorcycles/:id          更新摩托车
DELETE /api/vehicles/motorcycles/:id          删除摩托车
```

---

### 汽车模块（9个端点）✅
```
POST   /api/vehicles/cars              创建汽车
POST   /api/vehicles/cars/webhook      创建汽车（Webhook）
GET    /api/vehicles/cars              获取汽车列表 ✨支持sort/order参数
GET    /api/vehicles/cars/featured     获取精选汽车
GET    /api/vehicles/cars/brands       获取品牌列表
GET    /api/vehicles/cars/categories   获取分类列表
GET    /api/vehicles/cars/:id          获取汽车详情（通过ID）
GET    /api/vehicles/cars/slug/:slug   获取汽车详情（通过slug，推荐）
PUT    /api/vehicles/cars/:id          更新汽车
DELETE /api/vehicles/cars/:id          删除汽车
```

---

### 问答模块（3个端点）✅
```
GET    /api/qa                        获取问题列表（支持筛选、排序）
GET    /api/qa/:id                    获取问题详情（含回答）
POST   /api/qa/generate               手动生成问答（调试用）
```

---

### 二手交易模块（5个端点）✅
```
GET    /api/marketplace                       获取车辆列表（支持筛选、排序）
GET    /api/marketplace/:id                   获取车辆详情
POST   /api/marketplace/sync                  手动同步数据
POST   /api/marketplace/reclassify            重新分类数据
GET    /api/marketplace/stats/summary         获取统计信息
```

---

### Sitemap模块（4个端点）✅
```
GET    /api/sitemap/motorcycles               获取摩托车sitemap数据（仅数据库）
GET    /api/sitemap/cars                      获取汽车sitemap数据（仅数据库）
GET    /api/sitemap/reviews                   获取测评sitemap数据（仅数据库）
GET    /api/sitemap/marketplace               获取二手市场sitemap数据（仅数据库）
```

**说明**：
- 专用于SEO sitemap生成
- 只返回数据库中真实存在的active状态数据
- 不包含外部API数据
- 限制每个端点最多返回1000条记录
- 返回格式：`{ success: true, data: [{ id, slug?, lastmod }] }`

---

### 认证模块（5个端点）⏳
```
POST   /api/auth/register             用户注册（占位）
POST   /api/auth/login                用户登录（占位）
POST   /api/auth/logout               用户登出（占位）
POST   /api/auth/refresh              刷新Token（占位）
GET    /api/auth/profile              获取当前用户（占位）
```

---

### 用户模块（2个端点）⏳
```
GET    /api/users/profile             获取用户资料（占位）
PUT    /api/users/profile             更新用户资料（占位）
```

---

### 上传模块（2个端点）⏳
```
POST   /api/upload/image              上传图片（占位）
POST   /api/upload/file               上传文件（占位）
```

---

### 系统端点（1个）✅
```
GET    /health                        健康检查
```

---

## 🔧 最近更新（2025-10-12）

### API排序功能增强 ✨

#### 问题描述
首页精选车型无法正确展示，主要原因：
1. **缺少排序参数**：API不支持按浏览量（view_count）排序
2. **硬编码API地址**：前端使用相对路径`/api`但API无法访问
3. **品牌单一化**：没有混合品牌展示机制

#### 解决方案

**1. 摩托车API新增排序参数**
```typescript
// MotorcycleService.ts
static async getMotorcyclesList(params: {
  // ... 其他参数
  sort?: string;      // ✨新增：排序字段
  order?: string;     // ✨新增：排序方向
}) {
  const sortField = params.sort || 'created_at';
  const sortOrder = (params.order || 'DESC').toUpperCase() as 'ASC' | 'DESC';
  const orderBy: any[] = [[sortField, sortOrder]];
  // ...
}
```

**2. 汽车API新增排序参数**
```typescript
// CarService.ts
static async getCarsList(params: CarListParams) {
  const sortField = sort || 'year';
  const sortOrder = (order || 'DESC').toUpperCase() as 'ASC' | 'DESC';
  const orderBy: any[] = [[sortField, sortOrder]];
  // 如果不是按浏览量排序，添加view_count作为次要排序
  if (sortField !== 'view_count') {
    orderBy.push(['view_count', 'DESC']);
  }
  // ...
}
```

**3. API使用示例**
```bash
# 获取热门燃油摩托车（首页使用）
curl "http://47.237.79.9:4001/api/vehicles/motorcycles?fuel_type=Xăng&limit=6&sort=view_count&order=DESC"

# 获取热门电动汽车（首页使用）
curl "http://47.237.79.9:4001/api/vehicles/cars?fuel_type=Điện&limit=6&sort=view_count&order=DESC"

# 按价格从低到高
curl "http://47.237.79.9:4001/api/vehicles/motorcycles?sort=price_vnd&order=ASC"
```

**4. 前端组件修复**
```typescript
// VehiclesSection.tsx - 使用统一ContentCard组件
import ContentCard from './ContentCard';  // 统一组件
import { getMotorcycles, formatPrice, formatPower } from '../lib/api/motorcyclesApi';
import { getCars } from '../lib/api/carsApi';

// 获取数据并在客户端排序（自动混合品牌）
const gasMotosRes = await getMotorcycles({ fuel_type: 'Xăng', limit: 100 });
const sortedGasMotos = gasMotosRes.data
  .sort((a, b) => b.view_count - a.view_count)
  .slice(0, 6);
```

**5. Nginx缓存优化**
```nginx
# 从1年缓存改为1小时，方便前端更新
location ~* \.(js|css)$ {
    expires 1h;  # 之前是1y
    add_header Cache-Control "public, max-age=3600";
}
```

#### 影响的端点
- ✅ `GET /api/vehicles/motorcycles` - 支持sort和order参数
- ✅ `GET /api/vehicles/cars` - 支持sort和order参数

#### 测试验证
```bash
# 验证排序功能
curl "http://47.237.79.9:4001/api/vehicles/motorcycles?sort=view_count&order=DESC&limit=3"

# 验证结果（按浏览量降序）
# Honda Winner X - 5000 浏览
# Honda Air Blade - 4600 浏览
# Yamaha Sirius - 4400 浏览
```

---

## 📈 开发路线图

### Phase 1 - 已完成 ✅
- [x] 测评模块完整实现（原News模块）
- [x] 摩托车模块完整实现（含排序功能）
- [x] 汽车模块完整实现（含排序功能）
- [x] 问答模块完整实现（AI自动生成）
- [x] 二手交易模块完整实现（自动同步Chợ Tốt数据）
- [x] 基础框架搭建
- [x] 健康检查端点
- [x] 定时任务系统（ReviewScheduler、QAScheduler、MarketplaceScheduler）

### Phase 2 - 计划中 📋
- [ ] 用户认证系统（JWT + 权限管理）
- [ ] 文件上传功能（图片处理、缩略图）
- [ ] 用户资料管理
- [ ] 评论系统
- [ ] 收藏和点赞功能

### Phase 3 - 未来规划 🔮
- [ ] WebSocket 实时通知
- [ ] 图片处理服务（压缩、水印）
- [ ] 全文搜索优化（Elasticsearch）
- [ ] 数据统计和分析仪表板
- [ ] 推荐系统（基于用户行为）
- [ ] 邮件通知服务

---

## 🔗 相关文档

- [README.md](./README.md) - 项目总览
- [后端服务开发文档.md](./后端服务开发文档.md) - 后端服务详细设计
- [数据库设计文档.md](./数据库设计文档.md) - 数据库表结构
- [爬虫系统设计开发文档.md](./爬虫系统设计开发文档.md) - 数据采集
- [生产环境部署文档.md](./生产环境部署文档.md) - 部署说明

---

## 📞 技术支持

### API 调试工具
- **Postman**: https://www.postman.com
- **Insomnia**: https://insomnia.rest
- **VS Code REST Client**: https://marketplace.visualstudio.com/items?itemName=humao.rest-client

### 问题反馈
- 查看后端日志: `sudo journalctl -u vietnam-moto-backend -f`
- 查看应用日志: `tail -f /var/www/vietnam-moto-auto/backend/logs/backend.log`

---

**文档版本**: v3.2.0  
**最后更新**: 2025年10月14日  
**API 版本**: v1  
**已完整实现端点**: 41个 ✅  
**占位端点**: 9个 ⏳  
**总端点数**: 50个  
**生产环境**: https://vietmoto.top (HTTPS+SSL)

## 📝 更新日志

### v3.2.0 (2025-10-14 下午)
- ✅ 新增Sitemap专用API模块（4个端点）
- ✅ 修复sitemap数据来源问题（移除外部API数据）
- ✅ 实现分割sitemap索引结构
- ✅ 添加sitemap-index.xml和5个子sitemap文件
- ✅ 优化sitemap查询性能（只查询必要字段）
- ✅ 确保sitemap只包含数据库中的真实页面
- ✅ 完善Sitemap API使用最佳实践文档
- ✅ 总API端点数：37 → 41个

### v3.1.0 (2025-10-14 下午)
- ✅ 修复所有详情页SSR渲染问题
- ✅ 更新SSR环境API调用规范
- ✅ 区分服务器端和客户端API调用方式
- ✅ 修复5个详情页面（cars/motorcycles/marketplace/qa/reviews）
- ✅ 添加SSR模式下的API调用最佳实践
- ✅ 更新后端CORS配置（支持HTTPS域名）

### v3.0.0 (2025-10-14 上午)
- ✅ 合并API修复总结文档
- ✅ 新增API连接修复与配置章节
- ✅ 更新所有API示例为生产域名（https://vietmoto.top）
- ✅ 添加域名+SSL部署说明
- ✅ 添加HTTPS混合内容错误解决方案
- ✅ 更新前端API调用规范（使用相对路径 `/api`）
- ✅ 添加Nginx代理配置说明
- ✅ 更新最佳实践总结

### v2.0.0 (2025-10-14)
- ✅ 更新所有API路径：`/api/news` → `/api/reviews`（测评模块）
- ✅ 问答模块完整实现（3个端点）
- ✅ 二手交易模块完整实现（5个端点）
- ✅ 添加AI自动生成功能说明
- ✅ 添加自动数据同步功能说明
- ✅ 更新定时任务说明（ReviewScheduler、QAScheduler、MarketplaceScheduler）
- ✅ 更新API总览和路由表
- ✅ 更新开发路线图

### v1.0.0 (2025-10-12)
- 初始版本发布
- 测评、摩托车、汽车模块完整实现
- 基础框架搭建

