#!/usr/bin/env node

/**
 * SQLite数据库初始化脚本
 * 越南摩托汽车网站项目
 * 
 * 功能：
 * - 创建所有数据表
 * - 设置索引和约束
 * - 配置全文搜索(FTS5)
 * - 创建触发器
 * - 插入初始数据
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// 数据库配置
const DB_PATH = path.join(__dirname, '..', 'vietnam_moto_auto.sqlite');
const BACKUP_DIR = path.join(__dirname, '..', 'database', 'backup');

// 确保备份目录存在
if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
}

console.log('🚀 开始初始化SQLite数据库...');
console.log(`📍 数据库路径: ${DB_PATH}`);

// 创建数据库连接
const db = new sqlite3.Database(DB_PATH, (err) => {
    if (err) {
        console.error('❌ 数据库连接失败:', err.message);
        process.exit(1);
    }
    console.log('✅ 数据库连接成功');
});

// 配置SQLite PRAGMA设置
const configurePragma = () => {
    return new Promise((resolve, reject) => {
        const pragmaSettings = [
            'PRAGMA foreign_keys = ON',
            'PRAGMA journal_mode = WAL',
            'PRAGMA synchronous = NORMAL',
            'PRAGMA cache_size = 10000',
            'PRAGMA temp_store = memory',
            'PRAGMA mmap_size = 268435456'
        ];

        let completed = 0;
        pragmaSettings.forEach(pragma => {
            db.run(pragma, (err) => {
                if (err) {
                    console.error(`❌ PRAGMA设置失败: ${pragma}`, err.message);
                    reject(err);
                    return;
                }
                completed++;
                if (completed === pragmaSettings.length) {
                    console.log('✅ SQLite PRAGMA配置完成');
                    resolve();
                }
            });
        });
    });
};

// 创建用户表
const createUsersTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                phone TEXT,
                avatar_url TEXT,
                role TEXT DEFAULT 'user' CHECK (role IN ('admin', 'editor', 'user')),
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'banned')),
                email_verified INTEGER DEFAULT 0,
                last_login_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 用户表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 用户表创建成功');
                resolve();
            }
        });
    });
};

// 创建新闻表
const createNewsTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                excerpt TEXT,
                featured_image TEXT,
                category_id INTEGER,
                author_id INTEGER NOT NULL,
                status TEXT DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
                is_featured INTEGER DEFAULT 0,
                view_count INTEGER DEFAULT 0,
                published_at DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 新闻表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 新闻表创建成功');
                resolve();
            }
        });
    });
};

// 创建摩托车表
const createMotorcyclesTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS motorcycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_id INTEGER NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                price DECIMAL(12,2),
                currency TEXT DEFAULT 'VND',
                engine_capacity INTEGER,
                fuel_type TEXT CHECK (fuel_type IN ('gasoline', 'electric', 'hybrid')),
                transmission TEXT CHECK (transmission IN ('manual', 'automatic', 'cvt')),
                description TEXT,
                specifications TEXT,
                features TEXT,
                status TEXT DEFAULT 'available' CHECK (status IN ('available', 'sold', 'reserved', 'maintenance')),
                condition_type TEXT DEFAULT 'new' CHECK (condition_type IN ('new', 'used')),
                mileage INTEGER DEFAULT 0,
                location TEXT,
                seller_id INTEGER,
                view_count INTEGER DEFAULT 0,
                is_featured INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE,
                FOREIGN KEY (seller_id) REFERENCES users(id) ON DELETE SET NULL
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 摩托车表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 摩托车表创建成功');
                resolve();
            }
        });
    });
};

// 创建品牌表
const createBrandsTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                logo_url TEXT,
                description TEXT,
                country TEXT,
                website TEXT,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 品牌表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 品牌表创建成功');
                resolve();
            }
        });
    });
};

// 创建分类表
const createCategoriesTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                description TEXT,
                parent_id INTEGER,
                sort_order INTEGER DEFAULT 0,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 分类表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 分类表创建成功');
                resolve();
            }
        });
    });
};

// 创建图片表
const createImagesTable = () => {
    return new Promise((resolve, reject) => {
        const sql = `
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_name TEXT,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                mime_type TEXT,
                width INTEGER,
                height INTEGER,
                alt_text TEXT,
                entity_type TEXT NOT NULL CHECK (entity_type IN ('motorcycle', 'news', 'user', 'brand')),
                entity_id INTEGER NOT NULL,
                is_primary INTEGER DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        `;

        db.run(sql, (err) => {
            if (err) {
                console.error('❌ 图片表创建失败:', err.message);
                reject(err);
            } else {
                console.log('✅ 图片表创建成功');
                resolve();
            }
        });
    });
};

// 创建索引
const createIndexes = () => {
    return new Promise((resolve, reject) => {
        const indexes = [
            'CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)',
            'CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)',
            'CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)',
            'CREATE INDEX IF NOT EXISTS idx_news_status ON news(status)',
            'CREATE INDEX IF NOT EXISTS idx_news_category ON news(category_id)',
            'CREATE INDEX IF NOT EXISTS idx_news_author ON news(author_id)',
            'CREATE INDEX IF NOT EXISTS idx_news_published ON news(published_at)',
            'CREATE INDEX IF NOT EXISTS idx_motorcycles_brand ON motorcycles(brand_id)',
            'CREATE INDEX IF NOT EXISTS idx_motorcycles_status ON motorcycles(status)',
            'CREATE INDEX IF NOT EXISTS idx_motorcycles_price ON motorcycles(price)',
            'CREATE INDEX IF NOT EXISTS idx_motorcycles_year ON motorcycles(year)',
            'CREATE INDEX IF NOT EXISTS idx_images_entity ON images(entity_type, entity_id)',
            'CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id)',
            'CREATE INDEX IF NOT EXISTS idx_categories_slug ON categories(slug)'
        ];

        let completed = 0;
        indexes.forEach(indexSql => {
            db.run(indexSql, (err) => {
                if (err) {
                    console.error(`❌ 索引创建失败: ${indexSql}`, err.message);
                    reject(err);
                    return;
                }
                completed++;
                if (completed === indexes.length) {
                    console.log('✅ 所有索引创建完成');
                    resolve();
                }
            });
        });
    });
};

// 创建FTS5全文搜索表
const createFTSTables = () => {
    return new Promise((resolve, reject) => {
        const ftsTables = [
            `CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5(
                title, content, excerpt,
                content='news',
                content_rowid='id'
            )`,
            `CREATE VIRTUAL TABLE IF NOT EXISTS motorcycles_fts USING fts5(
                model, description, features,
                content='motorcycles',
                content_rowid='id'
            )`
        ];

        let completed = 0;
        ftsTables.forEach(sql => {
            db.run(sql, (err) => {
                if (err) {
                    console.error('❌ FTS表创建失败:', err.message);
                    reject(err);
                    return;
                }
                completed++;
                if (completed === ftsTables.length) {
                    console.log('✅ FTS5全文搜索表创建完成');
                    resolve();
                }
            });
        });
    });
};

// 创建触发器
const createTriggers = () => {
    return new Promise((resolve, reject) => {
        const triggers = [
            // 用户表更新时间触发器
            `CREATE TRIGGER IF NOT EXISTS users_updated_at 
             AFTER UPDATE ON users 
             BEGIN 
                 UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
             END`,
            
            // 新闻表更新时间触发器
            `CREATE TRIGGER IF NOT EXISTS news_updated_at 
             AFTER UPDATE ON news 
             BEGIN 
                 UPDATE news SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
             END`,
            
            // 新闻FTS同步触发器
            `CREATE TRIGGER IF NOT EXISTS news_fts_insert 
             AFTER INSERT ON news 
             BEGIN 
                 INSERT INTO news_fts(rowid, title, content, excerpt) 
                 VALUES (NEW.id, NEW.title, NEW.content, NEW.excerpt);
             END`,
            
            `CREATE TRIGGER IF NOT EXISTS news_fts_delete 
             AFTER DELETE ON news 
             BEGIN 
                 DELETE FROM news_fts WHERE rowid = OLD.id;
             END`,
            
            `CREATE TRIGGER IF NOT EXISTS news_fts_update 
             AFTER UPDATE ON news 
             BEGIN 
                 UPDATE news_fts SET title = NEW.title, content = NEW.content, excerpt = NEW.excerpt 
                 WHERE rowid = NEW.id;
             END`,
            
            // 摩托车FTS同步触发器
            `CREATE TRIGGER IF NOT EXISTS motorcycles_fts_insert 
             AFTER INSERT ON motorcycles 
             BEGIN 
                 INSERT INTO motorcycles_fts(rowid, model, description, features) 
                 VALUES (NEW.id, NEW.model, NEW.description, NEW.features);
             END`,
            
            `CREATE TRIGGER IF NOT EXISTS motorcycles_fts_delete 
             AFTER DELETE ON motorcycles 
             BEGIN 
                 DELETE FROM motorcycles_fts WHERE rowid = OLD.id;
             END`,
            
            `CREATE TRIGGER IF NOT EXISTS motorcycles_fts_update 
             AFTER UPDATE ON motorcycles 
             BEGIN 
                 UPDATE motorcycles_fts SET model = NEW.model, description = NEW.description, features = NEW.features 
                 WHERE rowid = NEW.id;
             END`
        ];

        let completed = 0;
        triggers.forEach(triggerSql => {
            db.run(triggerSql, (err) => {
                if (err) {
                    console.error('❌ 触发器创建失败:', err.message);
                    reject(err);
                    return;
                }
                completed++;
                if (completed === triggers.length) {
                    console.log('✅ 所有触发器创建完成');
                    resolve();
                }
            });
        });
    });
};

// 插入初始数据
const insertInitialData = () => {
    return new Promise((resolve, reject) => {
        // 插入默认管理员用户
        const adminUser = `
            INSERT OR IGNORE INTO users (username, email, password_hash, full_name, role, status, email_verified)
            VALUES ('admin', 'admin@vietnammoto.com', '$2a$10$example.hash.here', '系统管理员', 'admin', 'active', 1)
        `;

        // 插入默认品牌
        const brands = `
            INSERT OR IGNORE INTO brands (name, country, is_active) VALUES
            ('Honda', 'Japan', 1),
            ('Yamaha', 'Japan', 1),
            ('Suzuki', 'Japan', 1),
            ('Kawasaki', 'Japan', 1),
            ('SYM', 'Taiwan', 1),
            ('Piaggio', 'Italy', 1),
            ('Vinfast', 'Vietnam', 1)
        `;

        // 插入默认分类
        const categories = `
            INSERT OR IGNORE INTO categories (name, slug, description, is_active) VALUES
            ('摩托车新闻', 'motorcycle-news', '摩托车行业最新资讯', 1),
            ('市场动态', 'market-trends', '摩托车市场趋势分析', 1),
            ('技术评测', 'tech-reviews', '摩托车技术评测文章', 1),
            ('安全驾驶', 'safety-tips', '摩托车安全驾驶指南', 1)
        `;

        db.run(adminUser, (err) => {
            if (err) {
                console.error('❌ 管理员用户插入失败:', err.message);
                reject(err);
                return;
            }

            db.run(brands, (err) => {
                if (err) {
                    console.error('❌ 品牌数据插入失败:', err.message);
                    reject(err);
                    return;
                }

                db.run(categories, (err) => {
                    if (err) {
                        console.error('❌ 分类数据插入失败:', err.message);
                        reject(err);
                        return;
                    }

                    console.log('✅ 初始数据插入完成');
                    resolve();
                });
            });
        });
    });
};

// 主初始化函数
const initializeDatabase = async () => {
    try {
        await configurePragma();
        await createUsersTable();
        await createBrandsTable();
        await createCategoriesTable();
        await createNewsTable();
        await createMotorcyclesTable();
        await createImagesTable();
        await createIndexes();
        await createFTSTables();
        await createTriggers();
        await insertInitialData();

        console.log('🎉 数据库初始化完成！');
        console.log(`📊 数据库文件: ${DB_PATH}`);
        console.log('📝 包含的表: users, brands, categories, news, motorcycles, images');
        console.log('🔍 全文搜索: news_fts, motorcycles_fts');
        console.log('⚡ 索引和触发器已配置');

    } catch (error) {
        console.error('❌ 数据库初始化失败:', error.message);
        process.exit(1);
    } finally {
        db.close((err) => {
            if (err) {
                console.error('❌ 数据库关闭失败:', err.message);
            } else {
                console.log('✅ 数据库连接已关闭');
            }
        });
    }
};

// 如果直接运行此脚本
if (require.main === module) {
    initializeDatabase();
}

module.exports = { initializeDatabase };