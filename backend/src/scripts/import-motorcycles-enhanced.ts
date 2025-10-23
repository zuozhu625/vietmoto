import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';
import * as fs from 'fs';
import * as path from 'path';

async function importEnhancedMotorcycles() {
  try {
    console.log('🔄 开始导入增强版摩托车数据...\n');

    // 连接数据库
    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步数据库表（保留现有数据）
    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表结构已更新为增强版\n');

    // 读取增强版JSON数据
    const jsonPath = path.join(__dirname, 'data', 'motorcycles_enhanced_data.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 增强版数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 motorcycle-crawler-enhanced.py');
      process.exit(1);
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 条增强版摩托车数据\n`);

    // 显示数据字段统计
    if (motorcyclesData.length > 0) {
      const sampleFields = Object.keys(motorcyclesData[0]).filter(k => motorcyclesData[0][k] !== null && motorcyclesData[0][k] !== undefined);
      console.log(`📈 数据维度: ${sampleFields.length} 个字段\n`);
    }

    // 清空现有数据（可选）
    const clearExisting = process.argv.includes('--clear');
    if (clearExisting) {
      await Motorcycle.destroy({ where: {} });
      console.log('🗑️  已清空现有摩托车数据\n');
    }

    // 批量导入数据
    let successCount = 0;
    let errorCount = 0;
    let updateCount = 0;

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
        }
        
        successCount++;
      } catch (error: any) {
        errorCount++;
        console.error(`❌ 错误: ${data.brand} ${data.model} - ${error.message}`);
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log('📊 导入统计:');
    console.log(`   新增: ${successCount - updateCount} 条`);
    console.log(`   更新: ${updateCount} 条`);
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

    // 显示数据字段示例
    const sample = await Motorcycle.findOne();
    if (sample) {
      const filledFields = Object.keys(sample.toJSON()).filter(k => {
        const value = (sample as any)[k];
        return value !== null && value !== undefined && value !== '';
      });
      console.log(`\n📊 示例数据 (${sample.brand} ${sample.model}):`);
      console.log(`   已填充字段: ${filledFields.length} 个`);
    }

    console.log('\n✨ 增强版数据导入完成！');
    console.log('🎯 数据维度已从 ~15个 扩展到 ~42个\n');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ 导入失败:', error);
    process.exit(1);
  }
}

importEnhancedMotorcycles();

