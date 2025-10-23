-- ============================================
-- 二手车市场表 - 适配Chợ Tốt数据
-- ============================================

CREATE TABLE IF NOT EXISTS marketplace_vehicles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- Chợ Tốt原始数据
  external_id TEXT UNIQUE NOT NULL, -- Chợ Tốt的ad_id
  external_url TEXT, -- 原平台链接
  source TEXT DEFAULT 'chotot', -- 数据来源
  
  -- 基本信息
  type TEXT NOT NULL DEFAULT 'motorcycle', -- motorcycle/car
  brand TEXT, -- 品牌
  model TEXT, -- 型号
  year INTEGER, -- 年份
  price REAL NOT NULL, -- 价格
  
  -- 车辆详情
  title TEXT NOT NULL, -- 标题
  description TEXT, -- 描述
  mileage INTEGER, -- 里程数
  condition_text TEXT, -- 车况文字描述
  condition_rating INTEGER, -- 车况评分1-5
  
  -- 图片
  image_url TEXT, -- 主图
  images TEXT, -- JSON数组 - 所有图片
  
  -- 位置信息
  city TEXT, -- 城市
  district TEXT, -- 区域
  ward TEXT, -- 街道
  location TEXT, -- 坐标
  
  -- 卖家信息
  seller_name TEXT, -- 卖家名称
  seller_id TEXT, -- 卖家ID
  seller_avatar TEXT, -- 卖家头像
  seller_phone TEXT, -- 卖家电话
  seller_rating REAL, -- 卖家评分
  seller_sold_count INTEGER, -- 已售数量
  
  -- 统计数据
  view_count INTEGER DEFAULT 0, -- 浏览次数
  favorites_count INTEGER DEFAULT 0, -- 收藏数
  
  -- 状态
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'sold', 'inactive', 'deleted')),
  is_featured BOOLEAN DEFAULT FALSE, -- 是否精选
  
  -- 时间戳
  published_at DATETIME, -- 发布时间
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_marketplace_external_id ON marketplace_vehicles(external_id);
CREATE INDEX IF NOT EXISTS idx_marketplace_source ON marketplace_vehicles(source);
CREATE INDEX IF NOT EXISTS idx_marketplace_type ON marketplace_vehicles(type);
CREATE INDEX IF NOT EXISTS idx_marketplace_brand ON marketplace_vehicles(brand);
CREATE INDEX IF NOT EXISTS idx_marketplace_year ON marketplace_vehicles(year);
CREATE INDEX IF NOT EXISTS idx_marketplace_price ON marketplace_vehicles(price);
CREATE INDEX IF NOT EXISTS idx_marketplace_status ON marketplace_vehicles(status);
CREATE INDEX IF NOT EXISTS idx_marketplace_city ON marketplace_vehicles(city);
CREATE INDEX IF NOT EXISTS idx_marketplace_published ON marketplace_vehicles(published_at);

