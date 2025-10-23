import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';
import * as fs from 'fs';
import * as path from 'path';

async function importYamahaComplete() {
  try {
    console.log('🔄 开始导入Yamaha完整车型数据...\n');

    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表同步完成\n');

    const jsonPath = path.join(__dirname, 'data', 'yamaha_complete_data.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ Yamaha完整数据文件不存在');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 款Yamaha车型\n`);

    // 清空现有Yamaha数据
    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      await Motorcycle.destroy({ where: { brand: 'Yamaha' } });
      console.log('🗑️  已清空现有Yamaha数据\n');
    }

    let successCount = 0;
    let updateCount = 0;

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
          console.log(`🔄 更新: ${data.model}`);
          updateCount++;
        } else {
          await Motorcycle.create({
            ...data,
            status: 'active',
            view_count: 0,
          } as any);
          console.log(`✅ 添加: ${data.model} - ${data.price_vnd/1000000}M VNĐ`);
        }
        
        successCount++;
      } catch (error: any) {
        console.error(`❌ 错误: ${data.model} - ${error.message}`);
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log('📊 Yamaha导入统计:');
    console.log(`   新增: ${successCount - updateCount} 款`);
    console.log(`   更新: ${updateCount} 款`);
    console.log(`   总计: ${successCount} 款`);
    console.log('='.repeat(60));

    // 按类别统计
    const categories = await Motorcycle.findAll({
      attributes: ['category', [dbConfig.fn('COUNT', dbConfig.col('id')), 'count']],
      where: { brand: 'Yamaha' },
      group: ['category'],
      raw: true
    });

    console.log('\n📈 Yamaha按类别分布:');
    categories.forEach((cat: any) => {
      console.log(`   • ${cat.category}: ${cat.count} xe`);
    });

    // 特色技术统计
    const vvaCount = await Motorcycle.count({
      where: { 
        brand: 'Yamaha',
        valve_system: { [require('sequelize').Op.like]: '%VVA%' }
      }
    });

    const blueCoreCount = await Motorcycle.count({
      where: { 
        brand: 'Yamaha',
        engine_type: { [require('sequelize').Op.like]: '%Blue Core%' }
      }
    });

    console.log('\n🔧 Yamaha特色技术:');
    console.log(`   • VVA可变气门: ${vvaCount} xe`);
    console.log(`   • Blue Core: ${blueCoreCount} xe`);

    console.log('\n✨ Yamaha完整车型导入成功！');
    console.log('🎯 从入门到高端，覆盖所有细分市场\n');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ 导入失败:', error);
    process.exit(1);
  }
}

importYamahaComplete();

