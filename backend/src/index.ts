import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import compression from 'compression';
import rateLimit from 'express-rate-limit';
import dotenv from 'dotenv';
import path from 'path';

// 导入配置
import { dbConfig } from './config/database';
import { redisConfig } from './config/redis';

// 导入路由
import authRoutes from './routes/auth';
import newsRoutes from './routes/news';
import vehicleRoutes from './routes/vehicles';
import qaRoutes from './routes/qa';
import marketplaceRoutes from './routes/marketplace';
import userRoutes from './routes/users';
import uploadRoutes from './routes/upload';
import sitemapRoutes from './routes/sitemap';

// 导入中间件
import { errorHandler } from './middleware/errorHandler';
import { notFound } from './middleware/notFound';

// 导入服务
import QAScheduler from './services/QAScheduler';
import ReviewScheduler from './services/ReviewScheduler';
import MarketplaceScheduler from './services/MarketplaceScheduler';

// 加载环境变量
dotenv.config();

const app = express();
const PORT = parseInt(process.env.PORT || '3000', 10);

// 安全中间件
app.use(helmet({
  crossOriginEmbedderPolicy: false,
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// CORS配置 - 允许多个来源
const allowedOrigins = [
  'http://localhost:4321',
  'https://vietmoto.top',        // 生产环境域名+SSL
  'http://47.237.79.9:4321',     // 备用IP（已弃用）
  'http://127.0.0.1:4321'        // 本地测试
];

app.use(cors({
  origin: (origin, callback) => {
    // 允许没有origin的请求（比如移动应用或curl）
    if (!origin) return callback(null, true);
    
    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}));

// 速率限制（放宽限制）
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 500, // 每个IP最多500个请求（从100增加到500）
  message: {
    error: 'Too many requests from this IP, please try again later.',
  },
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    // 跳过内部请求（localhost）
    return req.ip === '127.0.0.1' || req.ip === '::1' || req.ip === '::ffff:127.0.0.1';
  }
});
app.use('/api/', limiter);

// 基础中间件
app.use(compression());
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// 静态文件服务
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// 健康检查
app.get('/health', (req, res) => {
  res.json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development',
  });
});

// API路由
app.use('/api/auth', authRoutes);
app.use('/api/reviews', newsRoutes); // 测评模块（原news）
app.use('/api/vehicles', vehicleRoutes);
app.use('/api/qa', qaRoutes);
app.use('/api/marketplace', marketplaceRoutes);
app.use('/api/users', userRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/sitemap', sitemapRoutes); // Sitemap专用API

// 404处理
app.use(notFound);

// 错误处理
app.use(errorHandler);

// 启动服务器
async function startServer() {
  try {
    // 测试数据库连接
    await dbConfig.authenticate();
    console.log('✅ Database connection established successfully.');

    // 测试Redis连接（可选）
    try {
      await redisConfig.ping();
      console.log('✅ Redis connection established successfully.');
    } catch (redisError) {
      console.warn('⚠️  Redis connection failed, continuing without cache:', redisError);
    }

    app.listen(PORT, '0.0.0.0', () => {
      console.log(`🚀 Server is running on port ${PORT}`);
      console.log(`📱 Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log(`🔗 Health check: http://localhost:${PORT}/health`);
      console.log(`📰 News API: http://localhost:${PORT}/api/news`);
      
      // 启动自动生成调度器
      QAScheduler.start();
      ReviewScheduler.start(); // 每40分钟生成一条用户测评到News板块
      MarketplaceScheduler.start(); // 每12小时更新二手市场数据
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

// 优雅关闭
process.on('SIGTERM', async () => {
  console.log('🔄 SIGTERM received, shutting down gracefully...');
  QAScheduler.stop();
  ReviewScheduler.stop();
  MarketplaceScheduler.stop();
  await dbConfig.close();
  await redisConfig.disconnect();
  process.exit(0);
});

process.on('SIGINT', async () => {
  console.log('🔄 SIGINT received, shutting down gracefully...');
  QAScheduler.stop();
  ReviewScheduler.stop();
  MarketplaceScheduler.stop();
  await dbConfig.close();
  await redisConfig.disconnect();
  process.exit(0);
});

startServer();