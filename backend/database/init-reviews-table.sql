-- 用户测评表
CREATE TABLE IF NOT EXISTS reviews (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,                              -- 测评标题
  content TEXT NOT NULL,                            -- 测评详细内容
  excerpt TEXT NOT NULL,                            -- 内容摘要（用于列表展示）
  vehicle_id INTEGER NOT NULL,                      -- 关联的车辆ID
  vehicle_type TEXT NOT NULL                        -- 车辆类型
    CHECK (vehicle_type IN ('motorcycle', 'car')),
  author_name TEXT NOT NULL,                        -- 作者昵称
  author_profile TEXT,                              -- 作者简介
  rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- 评分 1-5星
  usage_duration TEXT,                              -- 使用时长
  usage_scenario TEXT,                              -- 使用场景
  pros TEXT,                                        -- 优点
  cons TEXT,                                        -- 缺点
  view_count INTEGER NOT NULL DEFAULT 0,            -- 浏览次数
  like_count INTEGER NOT NULL DEFAULT 0,            -- 点赞数
  status TEXT NOT NULL DEFAULT 'published'          -- 状态
    CHECK (status IN ('published', 'draft', 'deleted')),
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_reviews_vehicle_id ON reviews(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_reviews_vehicle_type ON reviews(vehicle_type);
CREATE INDEX IF NOT EXISTS idx_reviews_status ON reviews(status);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

