import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';
import * as fs from 'fs';
import * as path from 'path';

async function importElectricMotorcycles() {
  try {
    console.log('🔄 开始导入电动摩托车数据...\n');
    console.log('   VinFast | Dat Bike | NUEN Moto | Yadea\n');

    // 连接数据库
    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步数据库表（保留现有数据）
    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表结构已更新\n');

    // 读取JSON数据
    const jsonPath = path.join(__dirname, 'data', 'electric_motorcycles_data.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 electric-motorcycles-crawler.py');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 条电动摩托车数据\n`);

    // 显示数据字段统计
    if (motorcyclesData.length > 0) {
      const sampleFields = Object.keys(motorcyclesData[0]).filter(k => motorcyclesData[0][k] !== null && motorcyclesData[0][k] !== undefined);
      console.log(`📈 数据维度: ${sampleFields.length} 个字段\n`);
    }

    // 清空这四个品牌的现有数据（可选）
    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      const deleted = await Motorcycle.destroy({
        where: {
          brand: ['VinFast', 'Dat Bike', 'NUEN Moto', 'Yadea']
        }
      });
      console.log(`🗑️  已清空电动车品牌现有数据 (${deleted} 条)\n`);
    }

    // 批量导入数据
    let successCount = 0;
    let errorCount = 0;
    let updateCount = 0;
    let createCount = 0;

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
          await existing.update({
            ...data,
            view_count: existing.view_count, // 保留浏览次数
          });
          console.log(`🔄 更新: ${data.brand} ${data.model} ${data.year}`);
          updateCount++;
        } else {
          // 创建新记录
          await Motorcycle.create({
            ...data,
            status: 'active',
            view_count: 0,
          } as any);
          console.log(`✅ 添加: ${data.brand} ${data.model} ${data.year}`);
          createCount++;
        }
        
        successCount++;
      } catch (error: any) {
        errorCount++;
        console.error(`❌ 错误: ${data.brand} ${data.model} - ${error.message}`);
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log('📊 导入统计:');
    console.log(`   新增: ${createCount} 条`);
    console.log(`   更新: ${updateCount} 条`);
    console.log(`   失败: ${errorCount} 条`);
    console.log('='.repeat(60));

    // 显示品牌统计
    const brands = await Motorcycle.findAll({
      attributes: ['brand', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['brand'],
      raw: true
    });

    console.log('\n📈 品牌统计 (数据库中所有品牌):');
    for (const brand of brands as any[]) {
      console.log(`   ${brand.brand}: ${brand.count} xe`);
    }

    // 显示电动车品牌详细统计
    console.log('\n⚡ 电动车品牌详细统计:');
    const electricBrands = ['VinFast', 'Dat Bike', 'NUEN Moto', 'Yadea'];
    for (const brandName of electricBrands) {
      const count = await Motorcycle.count({ where: { brand: brandName } });
      console.log(`   ${brandName}: ${count} xe điện`);
    }

    // 统计燃油类型
    console.log('\n🔋 燃料类型统计:');
    const fuelTypes = await Motorcycle.findAll({
      attributes: ['fuel_type', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['fuel_type'],
      raw: true
    });
    for (const type of fuelTypes as any[]) {
      console.log(`   ${type.fuel_type}: ${type.count} xe`);
    }

    console.log('\n' + '='.repeat(60));
    console.log('✅ 导入完成！');
    console.log('='.repeat(60));

  } catch (error) {
    console.error('❌ 导入过程出错:', error);
    process.exit(1);
  } finally {
    await dbConfig.close();
  }
}

// 运行导入
importElectricMotorcycles();

