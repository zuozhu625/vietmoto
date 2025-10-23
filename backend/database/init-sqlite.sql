-- ============================================
-- 越南摩托汽车资讯网站 - SQLite数据库结构
-- ============================================
-- 版本: 1.0.0
-- 创建日期: 2025-10-11
-- 数据库: vietnam_moto_auto.sqlite
-- ============================================

-- 启用外键约束
PRAGMA foreign_keys = ON;

-- ============================================
-- 1. 用户表 (users)
-- ============================================
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY, -- 用户唯一标识
  username TEXT UNIQUE NOT NULL, -- 用户名
  email TEXT UNIQUE NOT NULL, -- 邮箱
  password_hash TEXT NOT NULL, -- 密码哈希
  full_name TEXT, -- 真实姓名
  avatar TEXT, -- 头像URL
  phone TEXT, -- 手机号
  bio TEXT, -- 个人简介
  reputation_points INTEGER DEFAULT 0, -- 声望积分
  verified BOOLEAN DEFAULT FALSE, -- 是否认证
  role TEXT DEFAULT 'user' CHECK (role IN ('user', 'moderator', 'admin')), -- 用户角色
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 创建时间
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 更新时间
  last_login DATETIME, -- 最后登录时间
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'suspended', 'deleted')) -- 账号状态
);

-- 用户表索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- ============================================
-- 2. 新闻表 (news)
-- ============================================
CREATE TABLE IF NOT EXISTS news (
  id TEXT PRIMARY KEY, -- 新闻ID
  title TEXT NOT NULL, -- 新闻标题
  slug TEXT UNIQUE NOT NULL, -- URL友好标识
  excerpt TEXT, -- 摘要
  content TEXT NOT NULL, -- 正文内容
  cover_image TEXT, -- 封面图片
  category TEXT NOT NULL CHECK (category IN ('motorcycle', 'car', 'industry')), -- 分类
  author_id TEXT NOT NULL, -- 作者ID
  published_at DATETIME, -- 发布时间
  views INTEGER DEFAULT 0, -- 浏览次数
  likes INTEGER DEFAULT 0, -- 点赞数
  featured BOOLEAN DEFAULT FALSE, -- 是否精选
  status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')), -- 状态
  meta_title TEXT, -- SEO标题
  meta_description TEXT, -- SEO描述
  meta_keywords TEXT, -- SEO关键词
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- 新闻表索引
CREATE INDEX IF NOT EXISTS idx_news_slug ON news(slug);
CREATE INDEX IF NOT EXISTS idx_news_category ON news(category);
CREATE INDEX IF NOT EXISTS idx_news_author ON news(author_id);
CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_at);
CREATE INDEX IF NOT EXISTS idx_news_status ON news(status);
CREATE INDEX IF NOT EXISTS idx_news_featured ON news(featured);
CREATE INDEX IF NOT EXISTS idx_news_category_status ON news(category, status, published_at);

-- ============================================
-- 3. 摩托车型表 (motorcycles)
-- ============================================
CREATE TABLE IF NOT EXISTS motorcycles (
  id TEXT PRIMARY KEY,
  brand TEXT NOT NULL, -- 品牌
  model TEXT NOT NULL, -- 型号
  year INTEGER NOT NULL, -- 年份
  type TEXT, -- 类型
  displacement INTEGER, -- 排量(cc)
  engine_type TEXT, -- 引擎类型
  power TEXT, -- 最大功率
  torque TEXT, -- 最大扭矩
  transmission TEXT, -- 变速箱
  fuel_capacity REAL, -- 油箱容量(L)
  weight REAL, -- 整车重量(kg)
  seat_height INTEGER, -- 座高(mm)
  wheelbase INTEGER, -- 轴距(mm)
  ground_clearance INTEGER, -- 离地间隙(mm)
  official_price REAL, -- 官方价格
  dealer_price REAL, -- 经销商价格
  specifications TEXT, -- 详细参数JSON
  features TEXT, -- 特色功能JSON
  rating REAL DEFAULT 0, -- 评分(0-5)
  reviews_count INTEGER DEFAULT 0, -- 评价数量
  views INTEGER DEFAULT 0, -- 浏览次数
  featured BOOLEAN DEFAULT FALSE, -- 是否精选
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'discontinued', 'upcoming')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 摩托车表索引
CREATE INDEX IF NOT EXISTS idx_motorcycles_brand ON motorcycles(brand);
CREATE INDEX IF NOT EXISTS idx_motorcycles_type ON motorcycles(type);
CREATE INDEX IF NOT EXISTS idx_motorcycles_year ON motorcycles(year);
CREATE INDEX IF NOT EXISTS idx_motorcycles_displacement ON motorcycles(displacement);
CREATE INDEX IF NOT EXISTS idx_motorcycles_price ON motorcycles(official_price);
CREATE INDEX IF NOT EXISTS idx_motorcycles_rating ON motorcycles(rating);

-- ============================================
-- 4. 汽车表 (cars)
-- ============================================
CREATE TABLE IF NOT EXISTS cars (
  id TEXT PRIMARY KEY,
  brand TEXT NOT NULL, -- 品牌
  model TEXT NOT NULL, -- 型号
  year INTEGER NOT NULL, -- 年份
  type TEXT NOT NULL CHECK (type IN ('sedan', 'suv', 'mpv', 'pickup', 'ev', 'hatchback', 'coupe')), -- 车型类型
  engine_type TEXT, -- 发动机类型
  displacement INTEGER, -- 排量(cc)
  power TEXT, -- 最大功率(hp)
  torque TEXT, -- 最大扭矩(Nm)
  fuel_type TEXT NOT NULL CHECK (fuel_type IN ('gasoline', 'diesel', 'hybrid', 'electric', 'phev')), -- 燃油类型
  transmission TEXT, -- 变速箱
  drive_type TEXT CHECK (drive_type IN ('fwd', 'rwd', 'awd', '4wd')), -- 驱动方式
  seats INTEGER, -- 座位数
  doors INTEGER, -- 车门数
  fuel_consumption REAL, -- 油耗(L/100km)
  acceleration REAL, -- 0-100加速(秒)
  top_speed INTEGER, -- 最高时速(km/h)
  price_min REAL, -- 起始价格
  price_max REAL, -- 最高价格
  dimensions TEXT, -- 尺寸参数JSON
  features TEXT, -- 配置特性JSON
  safety_features TEXT, -- 安全配置JSON
  specifications TEXT, -- 详细规格JSON
  rating REAL DEFAULT 0, -- 评分
  reviews_count INTEGER DEFAULT 0, -- 评价数
  views INTEGER DEFAULT 0, -- 浏览次数
  featured BOOLEAN DEFAULT FALSE, -- 是否精选
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'discontinued', 'upcoming')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 汽车表索引
CREATE INDEX IF NOT EXISTS idx_cars_brand ON cars(brand);
CREATE INDEX IF NOT EXISTS idx_cars_type ON cars(type);
CREATE INDEX IF NOT EXISTS idx_cars_year ON cars(year);
CREATE INDEX IF NOT EXISTS idx_cars_fuel_type ON cars(fuel_type);
CREATE INDEX IF NOT EXISTS idx_cars_price ON cars(price_min, price_max);
CREATE INDEX IF NOT EXISTS idx_cars_rating ON cars(rating);

-- ============================================
-- 5. 问题表 (questions)
-- ============================================
CREATE TABLE IF NOT EXISTS questions (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL, -- 问题标题
  content TEXT NOT NULL, -- 问题内容
  category TEXT NOT NULL CHECK (category IN ('motorcycle', 'car')), -- 分类
  subcategory TEXT, -- 子分类
  author_id TEXT NOT NULL, -- 提问者ID
  views INTEGER DEFAULT 0, -- 浏览次数
  votes_count INTEGER DEFAULT 0, -- 投票数
  answers_count INTEGER DEFAULT 0, -- 回答数
  has_accepted_answer BOOLEAN DEFAULT FALSE, -- 是否有采纳答案
  last_activity_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 最后活动时间
  status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed', 'deleted')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- 问题表索引
CREATE INDEX IF NOT EXISTS idx_questions_category ON questions(category);
CREATE INDEX IF NOT EXISTS idx_questions_author ON questions(author_id);
CREATE INDEX IF NOT EXISTS idx_questions_votes ON questions(votes_count);
CREATE INDEX IF NOT EXISTS idx_questions_activity ON questions(last_activity_at);
CREATE INDEX IF NOT EXISTS idx_questions_status ON questions(status);

-- ============================================
-- 6. 答案表 (answers)
-- ============================================
CREATE TABLE IF NOT EXISTS answers (
  id TEXT PRIMARY KEY,
  question_id TEXT NOT NULL, -- 问题ID
  content TEXT NOT NULL, -- 答案内容
  author_id TEXT NOT NULL, -- 回答者ID
  votes_count INTEGER DEFAULT 0, -- 投票数
  is_accepted BOOLEAN DEFAULT FALSE, -- 是否被采纳
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- 答案表索引
CREATE INDEX IF NOT EXISTS idx_answers_question ON answers(question_id);
CREATE INDEX IF NOT EXISTS idx_answers_author ON answers(author_id);
CREATE INDEX IF NOT EXISTS idx_answers_votes ON answers(votes_count);
CREATE INDEX IF NOT EXISTS idx_answers_accepted ON answers(is_accepted);

-- ============================================
-- 7. 二手车市场表 (marketplace_vehicles)
-- ============================================
CREATE TABLE IF NOT EXISTS marketplace_vehicles (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL, -- 卖家ID
  vehicle_type TEXT NOT NULL CHECK (vehicle_type IN ('motorcycle', 'car')), -- 车辆类型
  brand TEXT NOT NULL, -- 品牌
  model TEXT NOT NULL, -- 型号
  year INTEGER NOT NULL, -- 年份
  mileage INTEGER, -- 里程数
  condition_rating INTEGER CHECK (condition_rating BETWEEN 1 AND 5), -- 车况评分
  price REAL NOT NULL, -- 售价
  negotiable BOOLEAN DEFAULT TRUE, -- 是否可议价
  description TEXT, -- 描述
  location TEXT, -- 所在地
  contact_phone TEXT, -- 联系电话
  images TEXT, -- 图片URLs JSON
  features TEXT, -- 配置特性JSON
  maintenance_records TEXT, -- 保养记录JSON
  views INTEGER DEFAULT 0, -- 浏览次数
  favorites_count INTEGER DEFAULT 0, -- 收藏数
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'sold', 'inactive', 'deleted')),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE RESTRICT
);

-- 二手车市场表索引
CREATE INDEX IF NOT EXISTS idx_marketplace_seller ON marketplace_vehicles(seller_id);
CREATE INDEX IF NOT EXISTS idx_marketplace_type ON marketplace_vehicles(vehicle_type);
CREATE INDEX IF NOT EXISTS idx_marketplace_brand ON marketplace_vehicles(brand);
CREATE INDEX IF NOT EXISTS idx_marketplace_year ON marketplace_vehicles(year);
CREATE INDEX IF NOT EXISTS idx_marketplace_price ON marketplace_vehicles(price);
CREATE INDEX IF NOT EXISTS idx_marketplace_status ON marketplace_vehicles(status);
CREATE INDEX IF NOT EXISTS idx_marketplace_location ON marketplace_vehicles(location);

-- ============================================
-- 8. 评论表 (comments)
-- ============================================
CREATE TABLE IF NOT EXISTS comments (
  id TEXT PRIMARY KEY,
  content TEXT NOT NULL, -- 评论内容
  author_id TEXT NOT NULL, -- 评论者ID
  target_type TEXT NOT NULL CHECK (target_type IN ('news', 'question', 'answer', 'vehicle')), -- 目标类型
  target_id TEXT NOT NULL, -- 目标ID
  parent_id TEXT, -- 父评论ID (用于回复)
  likes INTEGER DEFAULT 0, -- 点赞数
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
  FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE
);

-- 评论表索引
CREATE INDEX IF NOT EXISTS idx_comments_author ON comments(author_id);
CREATE INDEX IF NOT EXISTS idx_comments_target ON comments(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent ON comments(parent_id);
CREATE INDEX IF NOT EXISTS idx_comments_created ON comments(created_at);

-- ============================================
-- 9. 标签表 (tags)
-- ============================================
CREATE TABLE IF NOT EXISTS tags (
  id TEXT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL, -- 标签名
  description TEXT, -- 标签描述
  color TEXT, -- 标签颜色
  usage_count INTEGER DEFAULT 0, -- 使用次数
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 标签表索引
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
CREATE INDEX IF NOT EXISTS idx_tags_usage ON tags(usage_count);

-- ============================================
-- 10. 内容标签关联表 (content_tags)
-- ============================================
CREATE TABLE IF NOT EXISTS content_tags (
  id TEXT PRIMARY KEY,
  content_type TEXT NOT NULL CHECK (content_type IN ('news', 'question', 'vehicle')), -- 内容类型
  content_id TEXT NOT NULL, -- 内容ID
  tag_id TEXT NOT NULL, -- 标签ID
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
  UNIQUE(content_type, content_id, tag_id)
);

-- 内容标签关联表索引
CREATE INDEX IF NOT EXISTS idx_content_tags_content ON content_tags(content_type, content_id);
CREATE INDEX IF NOT EXISTS idx_content_tags_tag ON content_tags(tag_id);

-- ============================================
-- 触发器：自动更新 updated_at 字段
-- ============================================

-- 用户表更新触发器
CREATE TRIGGER IF NOT EXISTS update_users_updated_at 
  AFTER UPDATE ON users
  FOR EACH ROW
  BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 新闻表更新触发器
CREATE TRIGGER IF NOT EXISTS update_news_updated_at 
  AFTER UPDATE ON news
  FOR EACH ROW
  BEGIN
    UPDATE news SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 摩托车表更新触发器
CREATE TRIGGER IF NOT EXISTS update_motorcycles_updated_at 
  AFTER UPDATE ON motorcycles
  FOR EACH ROW
  BEGIN
    UPDATE motorcycles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 汽车表更新触发器
CREATE TRIGGER IF NOT EXISTS update_cars_updated_at 
  AFTER UPDATE ON cars
  FOR EACH ROW
  BEGIN
    UPDATE cars SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 问题表更新触发器
CREATE TRIGGER IF NOT EXISTS update_questions_updated_at 
  AFTER UPDATE ON questions
  FOR EACH ROW
  BEGIN
    UPDATE questions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 答案表更新触发器
CREATE TRIGGER IF NOT EXISTS update_answers_updated_at 
  AFTER UPDATE ON answers
  FOR EACH ROW
  BEGIN
    UPDATE answers SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 二手车市场表更新触发器
CREATE TRIGGER IF NOT EXISTS update_marketplace_vehicles_updated_at 
  AFTER UPDATE ON marketplace_vehicles
  FOR EACH ROW
  BEGIN
    UPDATE marketplace_vehicles SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- 评论表更新触发器
CREATE TRIGGER IF NOT EXISTS update_comments_updated_at 
  AFTER UPDATE ON comments
  FOR EACH ROW
  BEGIN
    UPDATE comments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
  END;

-- ============================================
-- 初始数据插入
-- ============================================

-- 插入管理员用户
INSERT OR IGNORE INTO users (
  id, username, email, password_hash, full_name, role, verified
) VALUES (
  'admin-001', 
  'admin', 
  'admin@vietnammoto.com', 
  '$2b$10$example.hash.for.admin.password', 
  'System Administrator', 
  'admin', 
  TRUE
);

-- 插入示例标签
INSERT OR IGNORE INTO tags (id, name, description, color) VALUES
('tag-001', 'Honda', 'Honda品牌相关', '#FF0000'),
('tag-002', 'Yamaha', 'Yamaha品牌相关', '#0066CC'),
('tag-003', 'Suzuki', 'Suzuki品牌相关', '#FFD700'),
('tag-004', '踏板车', '踏板车相关', '#00AA00'),
('tag-005', '跑车', '跑车相关', '#FF6600'),
('tag-006', 'SUV', 'SUV车型相关', '#8B4513'),
('tag-007', '电动车', '电动车相关', '#00FFFF'),
('tag-008', '维修保养', '维修保养相关', '#800080');

-- 完成初始化
SELECT 'SQLite数据库初始化完成!' as message;