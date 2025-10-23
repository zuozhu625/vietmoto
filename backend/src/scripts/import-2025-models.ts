import { dbConfig } from '../config/database';
import Car from '../models/Car';
import * as fs from 'fs';
import * as path from 'path';

// 摩托车数据接口
interface MotorcycleData {
  brand: string;
  model: string;
  year: number;
  category: string;
  price_vnd: number;
  fuel_type: string;
  engine_cc?: number;
  engine_type?: string;
  power_hp?: number;
  power_rpm?: number;
  torque_nm?: number;
  torque_rpm?: number;
  compression_ratio?: string;
  bore_stroke?: string;
  valve_system?: string;
  transmission?: string;
  clutch_type?: string;
  fuel_supply?: string;
  starter?: string;
  ignition?: string;
  frame_type?: string;
  front_suspension?: string;
  rear_suspension?: string;
  front_brake?: string;
  rear_brake?: string;
  front_tire?: string;
  rear_tire?: string;
  dimensions_mm?: string;
  wheelbase_mm?: number;
  ground_clearance_mm?: number;
  seat_height_mm?: number;
  weight_kg?: number;
  fuel_capacity_l?: number;
  abs?: boolean;
  smart_key?: boolean;
  display_type?: string;
  lighting?: string;
  features?: string;
  description?: string;
  warranty?: string;
  fuel_consumption?: string;
  colors?: string;
  rating?: number;
}

async function importCars2025() {
  try {
    console.log('🔄 开始导入2025年新汽车数据...\n');

    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步数据表
    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表结构已更新\n');

    const jsonPath = path.join(__dirname, '..', '..', 'src', 'scripts', 'crawlers', 'data', 'vietnam_cars_2025.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 2025年汽车数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 vietnam-2025-models-crawler.py');
      return false;
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const carsData = JSON.parse(jsonData);

    console.log(`📊 找到 ${carsData.length} 条2025年新汽车数据\n`);

    let successCount = 0;
    let errorCount = 0;
    let skipCount = 0;

    for (const data of carsData) {
      try {
        // 检查是否已存在相同的车型（brand + model + year）
        const existing = await Car.findOne({
          where: { 
            brand: data.brand,
            model: data.model,
            year: data.year
          }
        });

        if (existing) {
          console.log(`⏭️  跳过已存在: ${data.brand} ${data.model} ${data.year}`);
          skipCount++;
          continue;
        }

        // 创建新记录
        await Car.create({
          ...data,
          created_at: new Date(),
          updated_at: new Date()
        });

        console.log(`✅ 新增: ${data.brand} ${data.model} ${data.year} - ${data.price_vnd.toLocaleString()} VND`);
        successCount++;

      } catch (error) {
        console.error(`❌ 导入失败: ${data.brand} ${data.model}`, error);
        errorCount++;
      }
    }

    console.log('\n📈 2025年汽车数据导入完成:');
    console.log(`   ✅ 成功: ${successCount} 条`);
    console.log(`   ⏭️  跳过: ${skipCount} 条`);
    console.log(`   ❌ 失败: ${errorCount} 条`);
    
    return true;

  } catch (error) {
    console.error('❌ 导入2025年汽车数据时发生错误:', error);
    return false;
  }
}

async function importMotorcycles2025() {
  try {
    console.log('\n🔄 开始导入2025年新摩托车数据...\n');

    // 注意：摩托车使用不同的表结构，需要适配
    const jsonPath = path.join(__dirname, '..', '..', 'src', 'scripts', 'crawlers', 'data', 'vietnam_motorcycles_2025.json');
    
    if (!fs.existsSync(jsonPath)) {
      console.log('❌ 2025年摩托车数据文件不存在:', jsonPath);
      console.log('📝 请先运行: python3 vietnam-2025-models-crawler.py');
      return false;
    }

    const jsonData = fs.readFileSync(jsonPath, 'utf-8');
    const motorcyclesData: MotorcycleData[] = JSON.parse(jsonData);

    console.log(`📊 找到 ${motorcyclesData.length} 条2025年新摩托车数据\n`);

    // 由于摩托车表结构不同，我们需要先检查表是否存在数据
    const { QueryTypes } = require('sequelize');
    
    let successCount = 0;
    let errorCount = 0;
    let skipCount = 0;

    for (const data of motorcyclesData) {
      try {
        // 检查是否已存在相同的摩托车（brand + model + year）- 适配现有表结构
        const existing = await dbConfig.query(
          'SELECT id FROM motorcycles WHERE brand = ? AND model = ? AND year = ?',
          {
            replacements: [data.brand, data.model, data.year],
            type: QueryTypes.SELECT
          }
        );

        if (existing.length > 0) {
          console.log(`⏭️  跳过已存在: ${data.brand} ${data.model} ${data.year}`);
          skipCount++;
          continue;
        }

        // 插入摩托车数据 - 适配现有表结构
        await dbConfig.query(`
          INSERT INTO motorcycles (
            brand, model, year, category, price_vnd, engine_cc, power_hp, torque_nm,
            transmission, fuel_type, battery_kwh, range_km, charge_time_h,
            dimensions_mm, seat_height_mm, weight_kg, front_brake, rear_brake,
            abs, display_type, smart_key, features, description, rating,
            view_count, status, created_at, updated_at, engine_type, power_rpm,
            torque_rpm, compression_ratio, bore_stroke, valve_system, clutch_type,
            fuel_supply, starter, ignition, frame_type, front_suspension,
            rear_suspension, front_tire, rear_tire, wheelbase_mm, ground_clearance_mm,
            fuel_capacity_l, lighting, warranty, fuel_consumption, colors
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `, {
          replacements: [
            data.brand,
            data.model,
            data.year,
            data.category,
            data.price_vnd,
            data.engine_cc || null,
            data.power_hp || null,
            data.torque_nm || null,
            data.transmission || null,
            data.fuel_type || 'Xăng',
            data.fuel_type === 'Điện' ? 3.5 : null, // 电动车电池容量
            data.fuel_type === 'Điện' ? 160 : null, // 电动车续航
            data.fuel_type === 'Điện' ? 2.5 : null, // 电动车充电时间
            data.dimensions_mm || null,
            data.seat_height_mm || null,
            data.weight_kg || null,
            data.front_brake || null,
            data.rear_brake || null,
            data.abs ? 1 : 0,
            data.display_type || null,
            data.smart_key ? 1 : 0,
            data.features || null,
            data.description || `${data.brand} ${data.model} ${data.year}`,
            data.rating || 4.5,
            0, // view_count
            'active', // status
            new Date(),
            new Date(),
            data.engine_type || null,
            data.power_rpm || null,
            data.torque_rpm || null,
            data.compression_ratio || null,
            data.bore_stroke || null,
            data.valve_system || null,
            data.clutch_type || null,
            data.fuel_supply || null,
            data.starter || null,
            data.ignition || null,
            data.frame_type || null,
            data.front_suspension || null,
            data.rear_suspension || null,
            data.front_tire || null,
            data.rear_tire || null,
            data.wheelbase_mm || null,
            data.ground_clearance_mm || null,
            data.fuel_capacity_l || null,
            data.lighting || null,
            data.warranty || null,
            data.fuel_consumption || null,
            data.colors || null
          ],
          type: QueryTypes.INSERT
        });

        console.log(`✅ 新增: ${data.brand} ${data.model} ${data.year} - ${data.price_vnd.toLocaleString()} VND`);
        successCount++;

      } catch (error) {
        console.error(`❌ 导入失败: ${data.brand} ${data.model}`, error);
        errorCount++;
      }
    }

    console.log('\n📈 2025年摩托车数据导入完成:');
    console.log(`   ✅ 成功: ${successCount} 条`);
    console.log(`   ⏭️  跳过: ${skipCount} 条`);
    console.log(`   ❌ 失败: ${errorCount} 条`);
    
    return true;

  } catch (error) {
    console.error('❌ 导入2025年摩托车数据时发生错误:', error);
    return false;
  }
}

async function import2025Models() {
  console.log('🚀 开始导入2025年新车型数据...');
  console.log('=' + '='.repeat(59));

  try {
    // 导入汽车数据
    const carsSuccess = await importCars2025();
    
    // 导入摩托车数据
    const motorcyclesSuccess = await importMotorcycles2025();

    console.log('\n' + '='.repeat(60));
    if (carsSuccess && motorcyclesSuccess) {
      console.log('🎉 2025年新车型数据导入完成!');
      console.log('📊 数据已成功添加到数据库，不会替换现有2024年数据');
      console.log('🔄 建议运行前端重新构建以更新页面内容');
    } else {
      console.log('⚠️  部分数据导入失败，请检查错误信息');
    }

  } catch (error) {
    console.error('❌ 导入过程中发生错误:', error);
  } finally {
    await dbConfig.close();
    console.log('🔌 数据库连接已关闭');
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  import2025Models();
}

export { import2025Models, importCars2025, importMotorcycles2025 };
