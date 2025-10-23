import { dbConfig } from '../config/database';
import Car from '../models/Car';
import * as fs from 'fs';
import * as path from 'path';

async function importAdditionalCars() {
  try {
    console.log('🔄 开始导入补充品牌汽车数据...\n');

    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表结构已更新\n');

    const jsonPath = path.join(__dirname, 'data', 'vietnam_cars_additional_brands.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 vietnam-cars-additional-brands.py');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const carsData = JSON.parse(jsonData);

    console.log(`📊 找到 ${carsData.length} 条汽车数据\n`);

    let successCount = 0;
    let errorCount = 0;
    let updateCount = 0;
    let createCount = 0;

    for (const data of carsData) {
      try {
        const existing = await Car.findOne({
          where: { slug: data.slug }
        });

        if (existing) {
          await existing.update({
            ...data,
            view_count: existing.view_count,
            review_count: existing.review_count,
          });
          console.log(`🔄 更新: ${data.brand} ${data.model} ${data.year}`);
          updateCount++;
        } else {
          await Car.create({
            ...data,
            review_count: 0,
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
    console.log(`   成功: ${successCount} 条`);
    console.log(`   失败: ${errorCount} 条`);
    console.log('='.repeat(60));

    const brands = await Car.findAll({
      attributes: ['brand', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['brand'],
      order: [[dbConfig.fn('COUNT', dbConfig.col('id')), 'DESC']],
      raw: true
    });

    console.log('\n📈 品牌统计:');
    for (const brand of brands as any[]) {
      console.log(`   ${brand.brand}: ${brand.count} xe`);
    }

    const fuelTypes = await Car.findAll({
      attributes: ['fuel_type', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      group: ['fuel_type'],
      order: [[dbConfig.fn('COUNT', dbConfig.col('id')), 'DESC']],
      raw: true
    });
    
    console.log('\n🔋 燃料类型统计:');
    for (const type of fuelTypes as any[]) {
      console.log(`   ${type.fuel_type}: ${type.count} xe`);
    }

    const total = await Car.count({ where: { status: 'active' } });
    console.log(`\n📊 总计: ${total} xe ô tô đang hoạt động`);

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

importAdditionalCars();

