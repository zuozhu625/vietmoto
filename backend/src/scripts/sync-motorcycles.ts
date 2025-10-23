import { dbConfig } from '../config/database';
import Motorcycle from '../models/Motorcycle';

async function syncMotorcycles() {
  try {
    console.log('🔄 开始同步摩托车数据库...');

    // 测试数据库连接
    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步motorcycles表
    await dbConfig.sync({ alter: true });
    console.log('✅ 摩托车表同步完成');

    // 检查是否需要插入示例数据
    const count = await Motorcycle.count();
    console.log(`📊 当前摩托车数量: ${count}`);

    if (count === 0) {
      console.log('📝 插入示例摩托车数据...');
      
      await Motorcycle.bulkCreate([
        {
          brand: 'Honda',
          model: 'Winner X',
          year: 2024,
          category: 'Xe thể thao',
          price_vnd: 48000000,
          engine_cc: 149,
          power_hp: 17.1,
          torque_nm: 14.4,
          transmission: 'Số sàn 6 cấp',
          fuel_type: 'Xăng',
          dimensions_mm: '2020x740x1100',
          seat_height_mm: 795,
          weight_kg: 127,
          front_brake: 'Đĩa đơn 276mm',
          rear_brake: 'Đĩa đơn 220mm',
          abs: true,
          display_type: 'LCD toàn màu',
          smart_key: false,
          features: 'Đèn LED toàn bộ, Phanh ABS 2 kênh, Bảng đồng hồ LCD màu',
          description: 'Động cơ 149.2cc mạnh mẽ, công suất 17.1 mã lực, thiết kế thể thao, phù hợp di chuyển trong thành phố và đi chơi cuối tuần.',
          rating: 4.8,
          status: 'active',
        },
        {
          brand: 'Yamaha',
          model: 'Exciter 155',
          year: 2024,
          category: 'Xe thể thao',
          price_vnd: 50000000,
          engine_cc: 155,
          power_hp: 15.4,
          torque_nm: 14.3,
          transmission: 'Số sàn 6 cấp',
          fuel_type: 'Xăng',
          dimensions_mm: '2015x725x1100',
          seat_height_mm: 795,
          weight_kg: 118,
          front_brake: 'Đĩa đơn 267mm',
          rear_brake: 'Đĩa đơn 230mm',
          abs: true,
          display_type: 'LCD',
          smart_key: false,
          features: 'Công nghệ VVA, Đèn LED, Phanh ABS',
          description: 'Động cơ 155cc với công nghệ van biến thiên VVA, công suất mượt mà, khung gầm thể thao, mang đến trải nghiệm lái đầy cảm xúc.',
          rating: 4.7,
          status: 'active',
        },
        {
          brand: 'Honda',
          model: 'PCX 160',
          year: 2024,
          category: 'Xe tay ga',
          price_vnd: 59000000,
          engine_cc: 157,
          power_hp: 15.8,
          torque_nm: 14.7,
          transmission: 'Tự động vô cấp',
          fuel_type: 'Xăng',
          dimensions_mm: '1935x745x1105',
          seat_height_mm: 764,
          weight_kg: 131,
          front_brake: 'Đĩa đơn 220mm',
          rear_brake: 'Đĩa đơn 140mm',
          abs: true,
          display_type: 'LCD',
          smart_key: true,
          features: 'Khóa thông minh, Hệ thống Idle Stop, Đèn LED, ABS',
          description: 'Xe tay ga thời trang, động cơ eSP+ 156.9cc, hệ thống khởi động dừng thông minh, tiết kiệm nhiên liệu tuyệt vời.',
          rating: 4.9,
          status: 'active',
        },
        {
          brand: 'VinFast',
          model: 'Klara S',
          year: 2024,
          category: 'Xe điện',
          price_vnd: 35000000,
          battery_kwh: 2.4,
          range_km: 90,
          charge_time_h: 6,
          fuel_type: 'Điện',
          dimensions_mm: '1775x680x1125',
          seat_height_mm: 770,
          weight_kg: 116,
          front_brake: 'Đĩa đơn',
          rear_brake: 'Đĩa đơn',
          abs: false,
          display_type: 'LCD',
          smart_key: true,
          features: 'Pin Lithium-ion, Khóa thông minh, Sạc nhanh',
          description: 'Xe điện VinFast Klara S với pin lithium-ion, phạm vi hoạt động 90km, thiết kế thời trang.',
          rating: 4.5,
          status: 'active',
        },
        {
          brand: 'Yamaha',
          model: 'Sirius',
          year: 2024,
          category: 'Xe số',
          price_vnd: 20500000,
          engine_cc: 110,
          power_hp: 7.8,
          torque_nm: 8.5,
          transmission: 'Số sàn 4 cấp',
          fuel_type: 'Xăng',
          seat_height_mm: 765,
          weight_kg: 97,
          front_brake: 'Đĩa đơn',
          rear_brake: 'Tang trống',
          abs: false,
          display_type: 'Analog',
          smart_key: false,
          features: 'Tiết kiệm nhiên liệu, Bền bỉ',
          description: 'Xe số kinh điển, động cơ 110cc tiết kiệm, hiệu suất nhiên liệu xuất sắc, chi phí bảo dưỡng thấp.',
          rating: 4.5,
          status: 'active',
        },
        {
          brand: 'Honda',
          model: 'Wave Alpha',
          year: 2024,
          category: 'Xe số',
          price_vnd: 19500000,
          engine_cc: 110,
          power_hp: 7.7,
          torque_nm: 8.8,
          transmission: 'Số sàn 4 cấp',
          fuel_type: 'Xăng',
          seat_height_mm: 765,
          weight_kg: 96,
          front_brake: 'Đĩa đơn',
          rear_brake: 'Tang trống',
          abs: false,
          display_type: 'Analog',
          smart_key: false,
          features: 'Tiết kiệm nhiên liệu, Độ tin cậy cao',
          description: 'Xe số bán chạy nhất Việt Nam, động cơ 110cc, bền bỉ đáng tin cậy, tiết kiệm nhiên liệu tuyệt vời.',
          rating: 4.6,
          status: 'active',
        },
      ]);

      console.log('✅ 示例摩托车数据插入完成');
    }

    console.log('🎉 摩托车数据库同步完成！');
    process.exit(0);
  } catch (error) {
    console.error('❌ 摩托车数据库同步失败:', error);
    process.exit(1);
  }
}

syncMotorcycles();

