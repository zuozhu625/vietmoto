import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';
import * as fs from 'fs';
import * as path from 'path';

interface MotorcycleData {
  brand: string;
  model: string;
  year: number;
  category: string;
  price_vnd: number;
  engine_cc?: number;
  power_hp?: number;
  torque_nm?: number;
  transmission?: string;
  fuel_type?: string;
  battery_kwh?: number;
  range_km?: number;
  charge_time_h?: number;
  abs: boolean;
  smart_key: boolean;
  description: string;
}

async function importMotorcycles() {
  try {
    console.log('🔄 开始导入摩托车数据...\n');

    // 连接数据库
    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步数据库表
    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表同步完成\n');

    // 读取JSON数据
    const jsonPath = path.join(__dirname, 'data', 'motorcycles_data.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 数据文件不存在:', jsonPath);
      console.log('📝 请先运行爬虫脚本: python3 motorcycle-crawler.py');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData: MotorcycleData[] = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 条摩托车数据\n`);

    // 清空现有数据（可选）
    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      await Motorcycle.destroy({ where: {} });
      console.log('🗑️  已清空现有数据\n');
    }

    // 批量导入数据
    let successCount = 0;
    let errorCount = 0;

    for (const data of motorcyclesData) {
      try {
        // 检查是否已存在
        const existing = await Motorcycle.findOne({
          where: {
            brand: data.brand,
            model: data.model,
            year: data.year
          }
        });

        if (existing) {
          // 更新现有记录
          await existing.update(data);
          console.log(`🔄 更新: ${data.brand} ${data.model} ${data.year}`);
        } else {
          // 创建新记录
          await Motorcycle.create({
            ...data,
            status: 'active',
            view_count: 0,
          } as any);
          console.log(`✅ 添加: ${data.brand} ${data.model} ${data.year}`);
        }
        
        successCount++;
      } catch (error: any) {
        errorCount++;
        console.error(`❌ 错误: ${data.brand} ${data.model} - ${error.message}`);
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log('📊 导入统计:');
    console.log(`   成功: ${successCount} 条`);
    console.log(`   失败: ${errorCount} 条`);
    console.log('='.repeat(60));

    // 显示品牌统计
    const brands = await Motorcycle.findAll({
      attributes: ['brand', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['brand'],
      raw: true
    });

    console.log('\n📈 品牌统计:');
    brands.forEach((brand: any) => {
      console.log(`   ${brand.brand}: ${brand.count} 辆`);
    });

    console.log('\n✨ 数据导入完成！');
    process.exit(0);
  } catch (error) {
    console.error('❌ 导入失败:', error);
    process.exit(1);
  }
}

importMotorcycles();

