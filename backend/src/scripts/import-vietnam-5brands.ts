import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';
import * as fs from 'fs';
import * as path from 'path';

async function importVietnam5Brands() {
  try {
    console.log('🔄 开始导入越南5大电动车品牌数据...\n');
    console.log('   Selex | DKBike | Osakar | Dibao | HKbike\n');

    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表结构已更新\n');

    const jsonPath = path.join(__dirname, 'data', 'vietnam_5brands_data.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 vietnam-5brands-crawler.py');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 条电动车数据\n`);

    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      const deleted = await Motorcycle.destroy({
        where: {
          brand: ['Selex', 'DKBike', 'Osakar', 'Dibao', 'HKbike']
        }
      });
      console.log(`🗑️  已清空5个品牌现有数据 (${deleted} 条)\n`);
    }

    let successCount = 0;
    let errorCount = 0;
    let updateCount = 0;
    let createCount = 0;

    for (const data of motorcyclesData) {
      try {
        const existing = await Motorcycle.findOne({
          where: {
            brand: data.brand,
            model: data.model,
            year: data.year
          }
        });

        if (existing) {
          await existing.update({
            ...data,
            view_count: existing.view_count,
          });
          console.log(`🔄 更新: ${data.brand} ${data.model}`);
          updateCount++;
        } else {
          await Motorcycle.create({
            ...data,
            status: 'active',
            view_count: 0,
          } as any);
          console.log(`✅ 添加: ${data.brand} ${data.model}`);
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

    const brands = await Motorcycle.findAll({
      attributes: ['brand', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['brand'],
      raw: true
    });

    console.log('\n📈 品牌统计 (数据库中所有品牌):');
    for (const brand of brands as any[]) {
      console.log(`   ${brand.brand}: ${brand.count} xe`);
    }

    const electricBrands = ['Selex', 'DKBike', 'Osakar', 'Dibao', 'HKbike'];
    console.log('\n⚡ 新增电动车品牌统计:');
    for (const brandName of electricBrands) {
      const count = await Motorcycle.count({ where: { brand: brandName } });
      console.log(`   ${brandName}: ${count} xe điện`);
    }

    const fuelTypes = await Motorcycle.findAll({
      attributes: ['fuel_type', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['fuel_type'],
      raw: true
    });
    console.log('\n🔋 燃料类型统计:');
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

importVietnam5Brands();

