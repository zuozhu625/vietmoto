const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

// 数据库文件路径
const dbPath = path.join(__dirname, 'vietnam_moto_auto.sqlite');
const sqlPath = path.join(__dirname, 'init-sqlite.sql');

// 初始化数据库
async function initDatabase() {
  try {
    console.log('🚀 开始初始化SQLite数据库...');
    
    // 如果数据库文件已存在，先删除
    if (fs.existsSync(dbPath)) {
      fs.unlinkSync(dbPath);
      console.log('📝 删除旧的数据库文件');
    }
    
    // 创建新的数据库连接
    const db = new sqlite3.Database(dbPath, (err) => {
      if (err) {
        console.error('❌ 创建数据库失败:', err.message);
        return;
      }
      console.log('✅ 成功创建SQLite数据库文件');
    });
    
    // 读取SQL初始化脚本
    const sqlScript = fs.readFileSync(sqlPath, 'utf8');
    
    console.log('📋 准备执行SQL初始化脚本...');
    
    // 使用exec方法执行整个SQL脚本
    return new Promise((resolve, reject) => {
      db.exec(sqlScript, function(err) {
        if (err) {
          console.error('❌ 执行SQL脚本失败:', err.message);
          reject(err);
          return;
        }
        
        console.log('✅ SQL脚本执行完成');
        
        // 关闭数据库连接
        db.close((err) => {
          if (err) {
            console.error('❌ 关闭数据库连接失败:', err.message);
            reject(err);
          } else {
            console.log('🎉 数据库初始化完成!');
            console.log(`📍 数据库文件位置: ${dbPath}`);
            resolve();
          }
        });
      });
    });
    
  } catch (error) {
    console.error('❌ 数据库初始化失败:', error.message);
    throw error;
  }
}

// 验证数据库
async function verifyDatabase() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(dbPath, sqlite3.OPEN_READONLY, (err) => {
      if (err) {
        reject(err);
        return;
      }
      
      // 查询所有表
      db.all("SELECT name FROM sqlite_master WHERE type='table'", [], (err, rows) => {
        if (err) {
          reject(err);
          return;
        }
        
        console.log('📊 数据库表列表:');
        rows.forEach(row => {
          console.log(`  - ${row.name}`);
        });
        
        db.close();
        resolve(rows);
      });
    });
  });
}

// 主函数
async function main() {
  try {
    await initDatabase();
    await verifyDatabase();
    console.log('🎊 SQLite数据库设置完成!');
  } catch (error) {
    console.error('💥 初始化过程中出现错误:', error.message);
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main();
}

module.exports = { initDatabase, verifyDatabase };