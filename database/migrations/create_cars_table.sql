-- ============================================
-- 创建汽车表 (cars) - SQLite版本
-- ============================================
-- 版本: 1.0.0
-- 创建日期: 2025-10-12
-- ============================================

CREATE TABLE IF NOT EXISTS cars (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  
  -- 基础信息（7个字段）
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  year INTEGER NOT NULL,
  category TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  price_vnd REAL NOT NULL,
  seating_capacity INTEGER NOT NULL,
  
  -- 发动机系统（8个字段）
  engine_capacity_l REAL,
  engine_type TEXT,
  power_hp REAL,
  torque_nm REAL,
  fuel_type TEXT NOT NULL DEFAULT 'Xăng',
  transmission TEXT,
  drive_type TEXT,
  cylinder_count INTEGER,
  
  -- 电动车参数（3个字段）
  battery_kwh REAL,
  range_km INTEGER,
  charge_time_h REAL,
  
  -- 尺寸重量（6个字段）
  length_mm INTEGER,
  width_mm INTEGER,
  height_mm INTEGER,
  wheelbase_mm INTEGER,
  curb_weight_kg INTEGER,
  trunk_capacity_l INTEGER,
  
  -- 配置信息（6个字段）
  abs INTEGER NOT NULL DEFAULT 0,
  airbag_count INTEGER,
  smart_key INTEGER NOT NULL DEFAULT 0,
  display_type TEXT,
  infotainment_size REAL,
  fuel_consumption TEXT,
  
  -- 系统字段
  description TEXT,
  features TEXT,
  colors TEXT,
  image_url TEXT,
  image_gallery TEXT,
  rating REAL DEFAULT 0,
  review_count INTEGER NOT NULL DEFAULT 0,
  view_count INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'active',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE UNIQUE INDEX IF NOT EXISTS idx_cars_slug ON cars(slug);
CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand);
CREATE INDEX IF NOT EXISTS idx_cars_category ON cars(category);
CREATE INDEX IF NOT EXISTS idx_cars_fuel_type ON cars(fuel_type);
CREATE INDEX IF NOT EXISTS idx_cars_year ON cars(year);
CREATE INDEX IF NOT EXISTS idx_cars_status ON cars(status);
CREATE INDEX IF NOT EXISTS idx_cars_brand_year ON cars(brand, year);
CREATE INDEX IF NOT EXISTS idx_cars_price ON cars(price_vnd);

-- 创建全文搜索表（可选）
-- CREATE VIRTUAL TABLE IF NOT EXISTS cars_fts USING fts5(brand, model, description, content='cars', content_rowid='id');

