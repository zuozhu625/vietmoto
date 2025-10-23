-- ============================================
-- 越南摩托汽车资讯网站 - 数据库结构
-- ============================================
-- 版本: 1.0.0
-- 创建日期: 2025-10-11
-- 数据库: vietnam_moto_auto
-- ============================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS vietnam_moto_auto 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE vietnam_moto_auto;

-- 设置时区
SET time_zone = '+07:00';

-- ============================================
-- 1. 用户表 (users)
-- ============================================
CREATE TABLE users (
  id VARCHAR(36) PRIMARY KEY COMMENT '用户唯一标识',
  username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
  email VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
  password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
  full_name VARCHAR(100) COMMENT '真实姓名',
  avatar VARCHAR(255) COMMENT '头像URL',
  phone VARCHAR(20) COMMENT '手机号',
  bio TEXT COMMENT '个人简介',
  reputation_points INT DEFAULT 0 COMMENT '声望积分',
  verified BOOLEAN DEFAULT FALSE COMMENT '是否认证',
  role ENUM('user', 'moderator', 'admin') DEFAULT 'user' COMMENT '用户角色',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  last_login TIMESTAMP NULL COMMENT '最后登录时间',
  status ENUM('active', 'suspended', 'deleted') DEFAULT 'active' COMMENT '账号状态',
  
  INDEX idx_username (username),
  INDEX idx_email (email),
  INDEX idx_status (status),
  INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 2. 新闻表 (news)
-- ============================================
CREATE TABLE news (
  id VARCHAR(36) PRIMARY KEY COMMENT '新闻ID',
  title VARCHAR(255) NOT NULL COMMENT '新闻标题',
  slug VARCHAR(255) UNIQUE NOT NULL COMMENT 'URL友好标识',
  excerpt TEXT COMMENT '摘要',
  content LONGTEXT NOT NULL COMMENT '正文内容',
  cover_image VARCHAR(255) COMMENT '封面图片',
  category ENUM('motorcycle', 'car', 'industry') NOT NULL COMMENT '分类',
  author_id VARCHAR(36) NOT NULL COMMENT '作者ID',
  published_at TIMESTAMP NULL COMMENT '发布时间',
  views INT DEFAULT 0 COMMENT '浏览次数',
  likes INT DEFAULT 0 COMMENT '点赞数',
  featured BOOLEAN DEFAULT FALSE COMMENT '是否精选',
  status ENUM('draft', 'published', 'archived') DEFAULT 'draft' COMMENT '状态',
  meta_title VARCHAR(255) COMMENT 'SEO标题',
  meta_description TEXT COMMENT 'SEO描述',
  meta_keywords VARCHAR(255) COMMENT 'SEO关键词',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_slug (slug),
  INDEX idx_category (category),
  INDEX idx_author (author_id),
  INDEX idx_published (published_at),
  INDEX idx_status (status),
  INDEX idx_featured (featured),
  INDEX idx_category_status (category, status, published_at),
  FULLTEXT idx_search (title, content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='新闻表';

-- ============================================
-- 3. 摩托车型表 (motorcycles)
-- ============================================
CREATE TABLE motorcycles (
  id VARCHAR(36) PRIMARY KEY,
  brand VARCHAR(50) NOT NULL COMMENT '品牌',
  model VARCHAR(100) NOT NULL COMMENT '型号',
  year INT NOT NULL COMMENT '年份',
  type VARCHAR(50) COMMENT '类型',
  displacement INT COMMENT '排量(cc)',
  engine_type VARCHAR(50) COMMENT '引擎类型',
  power VARCHAR(50) COMMENT '最大功率',
  torque VARCHAR(50) COMMENT '最大扭矩',
  transmission VARCHAR(50) COMMENT '变速箱',
  fuel_capacity DECIMAL(5,2) COMMENT '油箱容量(L)',
  weight DECIMAL(6,2) COMMENT '整车重量(kg)',
  seat_height INT COMMENT '座高(mm)',
  wheelbase INT COMMENT '轴距(mm)',
  ground_clearance INT COMMENT '离地间隙(mm)',
  official_price DECIMAL(12,2) COMMENT '官方价格',
  dealer_price DECIMAL(12,2) COMMENT '经销商价格',
  specifications JSON COMMENT '详细参数JSON',
  features JSON COMMENT '特色功能',
  rating DECIMAL(3,2) DEFAULT 0 COMMENT '评分(0-5)',
  reviews_count INT DEFAULT 0 COMMENT '评价数量',
  views INT DEFAULT 0 COMMENT '浏览次数',
  featured BOOLEAN DEFAULT FALSE COMMENT '是否精选',
  status ENUM('active', 'discontinued', 'upcoming') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_brand (brand),
  INDEX idx_type (type),
  INDEX idx_year (year),
  INDEX idx_displacement (displacement),
  INDEX idx_price (official_price),
  INDEX idx_rating (rating),
  INDEX idx_filter (type, year, displacement),
  FULLTEXT idx_search (brand, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='摩托车型表';

-- ============================================
-- 4. 汽车表 (cars)
-- ============================================
CREATE TABLE cars (
  id VARCHAR(36) PRIMARY KEY,
  brand VARCHAR(50) NOT NULL COMMENT '品牌',
  model VARCHAR(100) NOT NULL COMMENT '型号',
  year INT NOT NULL COMMENT '年份',
  type ENUM('sedan', 'suv', 'mpv', 'pickup', 'ev', 'hatchback', 'coupe') NOT NULL COMMENT '车型类型',
  engine_type VARCHAR(50) COMMENT '发动机类型',
  displacement INT COMMENT '排量(cc)',
  power VARCHAR(50) COMMENT '最大功率(hp)',
  torque VARCHAR(50) COMMENT '最大扭矩(Nm)',
  fuel_type ENUM('gasoline', 'diesel', 'hybrid', 'electric', 'phev') NOT NULL COMMENT '燃油类型',
  transmission VARCHAR(50) COMMENT '变速箱',
  drive_type ENUM('fwd', 'rwd', 'awd', '4wd') COMMENT '驱动方式',
  seats INT COMMENT '座位数',
  doors INT COMMENT '车门数',
  fuel_consumption DECIMAL(4,2) COMMENT '油耗(L/100km)',
  acceleration DECIMAL(4,2) COMMENT '0-100加速(秒)',
  top_speed INT COMMENT '最高时速(km/h)',
  price_min DECIMAL(12,2) COMMENT '起始价格',
  price_max DECIMAL(12,2) COMMENT '最高价格',
  dimensions JSON COMMENT '尺寸参数',
  features JSON COMMENT '配置特性',
  safety_features JSON COMMENT '安全配置',
  specifications JSON COMMENT '详细规格',
  rating DECIMAL(3,2) DEFAULT 0 COMMENT '评分',
  reviews_count INT DEFAULT 0 COMMENT '评价数',
  views INT DEFAULT 0 COMMENT '浏览次数',
  featured BOOLEAN DEFAULT FALSE COMMENT '是否精选',
  status ENUM('active', 'discontinued', 'upcoming') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  INDEX idx_brand (brand),
  INDEX idx_type (type),
  INDEX idx_year (year),
  INDEX idx_fuel_type (fuel_type),
  INDEX idx_price (price_min, price_max),
  INDEX idx_rating (rating),
  INDEX idx_filter (type, fuel_type, price_min),
  FULLTEXT idx_search (brand, model)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='汽车表';

-- ============================================
-- 5. 问题表 (questions)
-- ============================================
CREATE TABLE questions (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(255) NOT NULL COMMENT '问题标题',
  content TEXT NOT NULL COMMENT '问题内容',
  category ENUM('motorcycle', 'car') NOT NULL COMMENT '分类',
  subcategory VARCHAR(50) COMMENT '子分类',
  author_id VARCHAR(36) NOT NULL COMMENT '提问者ID',
  views INT DEFAULT 0 COMMENT '浏览次数',
  votes_count INT DEFAULT 0 COMMENT '投票数',
  answers_count INT DEFAULT 0 COMMENT '回答数',
  has_accepted_answer BOOLEAN DEFAULT FALSE COMMENT '是否有采纳答案',
  last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '最后活动时间',
  status ENUM('open', 'closed', 'deleted') DEFAULT 'open',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_category (category),
  INDEX idx_author (author_id),
  INDEX idx_votes (votes_count),
  INDEX idx_activity (last_activity_at),
  INDEX idx_status (status),
  INDEX idx_hot (category, status, votes_count, created_at),
  FULLTEXT idx_search (title, content)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='问题表';

-- ============================================
-- 6. 答案表 (answers)
-- ============================================
CREATE TABLE answers (
  id VARCHAR(36) PRIMARY KEY,
  question_id VARCHAR(36) NOT NULL COMMENT '问题ID',
  content TEXT NOT NULL COMMENT '答案内容',
  author_id VARCHAR(36) NOT NULL COMMENT '回答者ID',
  votes_count INT DEFAULT 0 COMMENT '投票数',
  is_accepted BOOLEAN DEFAULT FALSE COMMENT '是否被采纳',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_question (question_id),
  INDEX idx_author (author_id),
  INDEX idx_votes (votes_count),
  INDEX idx_accepted (is_accepted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='答案表';

-- ============================================
-- 7. 二手交易表 (listings)
-- ============================================
CREATE TABLE listings (
  id VARCHAR(36) PRIMARY KEY,
  type ENUM('motorcycle', 'car') NOT NULL COMMENT '车辆类型',
  brand VARCHAR(50) NOT NULL COMMENT '品牌',
  model VARCHAR(100) NOT NULL COMMENT '型号',
  year INT NOT NULL COMMENT '年份',
  price DECIMAL(12,2) NOT NULL COMMENT '售价',
  mileage INT COMMENT '里程(公里)',
  condition_rating INT COMMENT '车况评分(1-10)',
  description TEXT COMMENT '描述',
  color VARCHAR(50) COMMENT '颜色',
  license_plate VARCHAR(20) COMMENT '车牌号',
  city VARCHAR(100) COMMENT '城市',
  district VARCHAR(100) COMMENT '区域',
  address TEXT COMMENT '详细地址',
  seller_id VARCHAR(36) NOT NULL COMMENT '卖家ID',
  contact_name VARCHAR(100) COMMENT '联系人',
  contact_phone VARCHAR(20) NOT NULL COMMENT '联系电话',
  contact_email VARCHAR(100) COMMENT '联系邮箱',
  views INT DEFAULT 0 COMMENT '浏览次数',
  favorites_count INT DEFAULT 0 COMMENT '收藏次数',
  status ENUM('active', 'sold', 'removed', 'expired') DEFAULT 'active',
  featured BOOLEAN DEFAULT FALSE COMMENT '是否推荐',
  verified BOOLEAN DEFAULT FALSE COMMENT '是否认证',
  expires_at TIMESTAMP NULL COMMENT '过期时间',
  sold_at TIMESTAMP NULL COMMENT '成交时间',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_type (type),
  INDEX idx_brand (brand),
  INDEX idx_price (price),
  INDEX idx_year (year),
  INDEX idx_city (city),
  INDEX idx_status (status),
  INDEX idx_seller (seller_id),
  INDEX idx_created (created_at),
  INDEX idx_search (type, status, city, price),
  FULLTEXT idx_fulltext (brand, model, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='二手交易表';

-- ============================================
-- 8. 图片表 (images)
-- ============================================
CREATE TABLE images (
  id VARCHAR(36) PRIMARY KEY,
  entity_type ENUM('news', 'motorcycle', 'car', 'listing', 'user', 'question', 'answer') NOT NULL COMMENT '关联实体类型',
  entity_id VARCHAR(36) NOT NULL COMMENT '关联实体ID',
  url VARCHAR(255) NOT NULL COMMENT '图片URL',
  thumbnail_url VARCHAR(255) COMMENT '缩略图URL',
  alt_text VARCHAR(255) COMMENT 'ALT文本',
  width INT COMMENT '宽度',
  height INT COMMENT '高度',
  file_size INT COMMENT '文件大小(字节)',
  mime_type VARCHAR(50) COMMENT 'MIME类型',
  display_order INT DEFAULT 0 COMMENT '显示顺序',
  is_primary BOOLEAN DEFAULT FALSE COMMENT '是否主图',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_order (entity_type, entity_id, display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='图片表';

-- ============================================
-- 9. 评论表 (comments)
-- ============================================
CREATE TABLE comments (
  id VARCHAR(36) PRIMARY KEY,
  entity_type ENUM('news', 'question', 'answer', 'listing') NOT NULL COMMENT '评论对象类型',
  entity_id VARCHAR(36) NOT NULL COMMENT '评论对象ID',
  content TEXT NOT NULL COMMENT '评论内容',
  author_id VARCHAR(36) NOT NULL COMMENT '评论者ID',
  parent_id VARCHAR(36) NULL COMMENT '父评论ID',
  likes_count INT DEFAULT 0 COMMENT '点赞数',
  status ENUM('active', 'hidden', 'deleted') DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE RESTRICT,
  FOREIGN KEY (parent_id) REFERENCES comments(id) ON DELETE CASCADE,
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_author (author_id),
  INDEX idx_parent (parent_id),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

-- ============================================
-- 10. 标签表 (tags)
-- ============================================
CREATE TABLE tags (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL COMMENT '标签名称',
  slug VARCHAR(50) UNIQUE NOT NULL COMMENT 'URL标识',
  description TEXT COMMENT '标签描述',
  usage_count INT DEFAULT 0 COMMENT '使用次数',
  category ENUM('motorcycle', 'car', 'general') DEFAULT 'general',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_name (name),
  INDEX idx_slug (slug),
  INDEX idx_usage (usage_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='标签表';

-- ============================================
-- 11. 实体标签关联表 (entity_tags)
-- ============================================
CREATE TABLE entity_tags (
  id VARCHAR(36) PRIMARY KEY,
  entity_type ENUM('news', 'question', 'motorcycle', 'car', 'listing') NOT NULL,
  entity_id VARCHAR(36) NOT NULL,
  tag_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
  UNIQUE KEY uk_entity_tag (entity_type, entity_id, tag_id),
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_tag (tag_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='实体标签关联表';

-- ============================================
-- 12. 投票表 (votes)
-- ============================================
CREATE TABLE votes (
  id VARCHAR(36) PRIMARY KEY,
  entity_type ENUM('question', 'answer', 'comment') NOT NULL,
  entity_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  vote_type ENUM('up', 'down') NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY uk_user_vote (entity_type, entity_id, user_id),
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='投票表';

-- ============================================
-- 13. 收藏表 (favorites)
-- ============================================
CREATE TABLE favorites (
  id VARCHAR(36) PRIMARY KEY,
  entity_type ENUM('news', 'motorcycle', 'car', 'listing', 'question') NOT NULL,
  entity_id VARCHAR(36) NOT NULL,
  user_id VARCHAR(36) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY uk_user_favorite (entity_type, entity_id, user_id),
  INDEX idx_entity (entity_type, entity_id),
  INDEX idx_user (user_id),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收藏表';

-- ============================================
-- 14. 通知表 (notifications)
-- ============================================
CREATE TABLE notifications (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL COMMENT '接收者ID',
  type VARCHAR(50) NOT NULL COMMENT '通知类型',
  title VARCHAR(255) NOT NULL COMMENT '通知标题',
  content TEXT COMMENT '通知内容',
  link VARCHAR(255) COMMENT '跳转链接',
  is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  read_at TIMESTAMP NULL COMMENT '阅读时间',
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user (user_id),
  INDEX idx_read (is_read),
  INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='通知表';

-- ============================================
-- 15. 会话表 (sessions)
-- ============================================
CREATE TABLE sessions (
  id VARCHAR(36) PRIMARY KEY,
  user_id VARCHAR(36) NOT NULL,
  token VARCHAR(255) UNIQUE NOT NULL,
  refresh_token VARCHAR(255) UNIQUE NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user (user_id),
  INDEX idx_token (token),
  INDEX idx_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会话表';

-- ============================================
-- 数据库初始化完成
-- ============================================

