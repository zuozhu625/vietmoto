import Redis from 'ioredis';
import dotenv from 'dotenv';

dotenv.config();

const {
  REDIS_HOST = 'localhost',
  REDIS_PORT = '6379',
  REDIS_PASSWORD = '',
  REDIS_DB = '0',
  NODE_ENV = 'development'
} = process.env;

export const redisConfig = new Redis({
  host: REDIS_HOST,
  port: parseInt(REDIS_PORT),
  password: REDIS_PASSWORD || undefined,
  db: parseInt(REDIS_DB),
  enableReadyCheck: false,
  maxRetriesPerRequest: null,
  lazyConnect: true,
});

// Redis事件监听
redisConfig.on('connect', () => {
  console.log('✅ Redis connected successfully');
});

redisConfig.on('error', (error) => {
  console.error('❌ Redis connection error:', error);
});

redisConfig.on('ready', () => {
  console.log('✅ Redis is ready to receive commands');
});

redisConfig.on('close', () => {
  console.log('🔄 Redis connection closed');
});

// 缓存工具类
export class CacheService {
  private redis: Redis;

  constructor() {
    this.redis = redisConfig;
  }

  /**
   * 设置缓存
   * @param key 键
   * @param value 值
   * @param ttl 过期时间（秒）
   */
  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    try {
      const serializedValue = JSON.stringify(value);
      await this.redis.setex(key, ttl, serializedValue);
    } catch (error) {
      console.error('Cache set error:', error);
    }
  }

  /**
   * 获取缓存
   * @param key 键
   */
  async get<T = any>(key: string): Promise<T | null> {
    try {
      const value = await this.redis.get(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Cache get error:', error);
      return null;
    }
  }

  /**
   * 删除缓存
   * @param key 键
   */
  async del(key: string): Promise<void> {
    try {
      await this.redis.del(key);
    } catch (error) {
      console.error('Cache delete error:', error);
    }
  }

  /**
   * 检查键是否存在
   * @param key 键
   */
  async exists(key: string): Promise<boolean> {
    try {
      const result = await this.redis.exists(key);
      return result === 1;
    } catch (error) {
      console.error('Cache exists error:', error);
      return false;
    }
  }

  /**
   * 设置过期时间
   * @param key 键
   * @param ttl 过期时间（秒）
   */
  async expire(key: string, ttl: number): Promise<void> {
    try {
      await this.redis.expire(key, ttl);
    } catch (error) {
      console.error('Cache expire error:', error);
    }
  }

  /**
   * 获取所有匹配的键
   * @param pattern 模式
   */
  async keys(pattern: string): Promise<string[]> {
    try {
      return await this.redis.keys(pattern);
    } catch (error) {
      console.error('Cache keys error:', error);
      return [];
    }
  }

  /**
   * 清空所有缓存
   */
  async flushAll(): Promise<void> {
    try {
      await this.redis.flushall();
    } catch (error) {
      console.error('Cache flush error:', error);
    }
  }
}

export const cacheService = new CacheService();
export default redisConfig;