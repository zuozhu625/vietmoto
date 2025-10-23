import { Sequelize } from 'sequelize';
import dotenv from 'dotenv';
import path from 'path';

dotenv.config();

const {
  DB_PATH = path.join(__dirname, '../../database/vietnam_moto_auto.sqlite'),
  NODE_ENV = 'development'
} = process.env;

export const dbConfig = new Sequelize({
  dialect: 'sqlite',
  storage: DB_PATH,
  logging: NODE_ENV === 'development' ? console.log : false,
  pool: {
    max: 5,
    min: 0,
    acquire: 30000,
    idle: 10000,
  },
  define: {
    timestamps: true,
    underscored: true,
    freezeTableName: true,
  },
});

// 数据库连接测试
export const testConnection = async (): Promise<boolean> => {
  try {
    await dbConfig.authenticate();
    console.log('✅ Database connection has been established successfully.');
    return true;
  } catch (error) {
    console.error('❌ Unable to connect to the database:', error);
    return false;
  }
};

export default dbConfig;