# SQLite 数据库配置说明

## 概述
本项目已从MySQL迁移到SQLite数据库，以实现更好的项目独立性和简化部署。

## 数据库文件位置
- **数据库文件**: `/backend/database/vietnam_moto_auto.sqlite`
- **初始化脚本**: `/backend/database/init-sqlite.sql`
- **初始化工具**: `/backend/database/init-database.js`

## 环境变量配置
在 `docker-compose.yml` 或环境变量中设置：
```
DB_PATH=/app/database/vietnam_moto_auto.sqlite
```

## 数据库初始化
运行以下命令初始化数据库：
```bash
npm run init-db
# 或
npm run db:init
```

## 数据库表结构
数据库包含以下表：
- `users` - 用户信息
- `news` - 新闻文章
- `motorcycles` - 摩托车信息
- `cars` - 汽车信息
- `questions` - 问题
- `answers` - 答案
- `marketplace_vehicles` - 市场车辆
- `comments` - 评论
- `tags` - 标签
- `content_tags` - 内容标签关联

## 特性
- ✅ 外键约束支持
- ✅ 自动更新时间戳
- ✅ 索引优化
- ✅ 初始数据预设
- ✅ 事务支持

## 备份和恢复
SQLite数据库文件可以直接复制进行备份：
```bash
cp database/vietnam_moto_auto.sqlite database/backup_$(date +%Y%m%d_%H%M%S).sqlite
```

## 注意事项
- SQLite数据库文件会在Docker容器中持久化
- 数据库文件权限需要确保应用可读写
- 生产环境建议定期备份数据库文件