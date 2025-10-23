import { dbConfig } from '../config/database';
import News from '../models/News';

async function syncDatabase() {
  try {
    console.log('🔄 开始同步数据库...');

    // 测试数据库连接
    await dbConfig.authenticate();
    console.log('✅ 数据库连接成功');

    // 同步所有模型（创建表）
    await dbConfig.sync({ alter: true });
    console.log('✅ 数据库表同步完成');

    // 检查是否需要插入示例数据
    const newsCount = await News.count();
    console.log(`📊 当前新闻数量: ${newsCount}`);

    if (newsCount === 0) {
      console.log('📝 插入示例新闻数据...');
      
      await News.bulkCreate([
        {
          title: 'Honda Winner X 2024 - Chuẩn mực mới của xe côn tay thể thao tại Việt Nam',
          slug: 'honda-winner-x-2024',
          content: `<p class="lead">Honda Winner X 2024 mới đã chính thức ra mắt với nhiều nâng cấp đáng giá về thiết kế, động cơ và công nghệ.</p>
<h2>Thiết kế thể thao mạnh mẽ</h2>
<p>Winner X 2024 sở hữu thiết kế góc cạnh, thể thao với đèn LED toàn phần, tạo điểm nhấn nổi bật trên đường phố.</p>
<h2>Động cơ mạnh mẽ</h2>
<p>Động cơ 149.2cc, làm mát bằng nước, công suất 17.1 mã lực tại 9.000 vòng/phút, mô-men xoắn 14.4 Nm tại 7.000 vòng/phút.</p>
<h2>Giá cả cạnh tranh</h2>
<p>Winner X 2024 có giá từ 46-50 triệu đồng, rất cạnh tranh trong phân khúc xe côn tay thể thao.</p>`,
          summary: 'Honda Winner X 2024 mới với động cơ 149.2cc mạnh mẽ, thiết kế thể thao và công nghệ tiên tiến đang trở thành lựa chọn hàng đầu của giới trẻ.',
          category: 'Xe máy',
          author_name: 'Ban biên tập',
          status: 'published',
          published_at: new Date(),
        },
        {
          title: 'VinFast VF8 chính thức ra mắt thị trường quốc tế',
          slug: 'vinfast-vf8-global',
          content: `<p class="lead">SUV điện VinFast VF8 đã chính thức có mặt tại thị trường Mỹ và châu Âu, đánh dấu bước tiến quan trọng của ngành công nghiệp ô tô Việt Nam.</p>
<h2>Công nghệ tiên tiến</h2>
<p>VF8 được trang bị hệ thống pin 87.7 kWh, phạm vi hoạt động lên đến 420km theo tiêu chuẩn WLTP.</p>
<h2>An toàn 5 sao</h2>
<p>Xe đạt chuẩn an toàn 5 sao Euro NCAP với đầy đủ công nghệ hỗ trợ lái hiện đại.</p>`,
          summary: 'SUV điện VinFast VF8 đã có mặt tại thị trường Mỹ và châu Âu, thể hiện sức mạnh của ngành công nghiệp ô tô Việt Nam.',
          category: 'Ô tô điện',
          author_name: 'Phóng viên quốc tế',
          status: 'published',
          published_at: new Date(),
        },
        {
          title: 'Toyota Vios 2024 - Bí quyết thành công của ông vua sedan hạng B',
          slug: 'toyota-vios-2024',
          content: `<p class="lead">Toyota Vios tiếp tục dẫn đầu phân khúc sedan hạng B tại Việt Nam với doanh số ấn tượng.</p>
<h2>Tiết kiệm nhiên liệu</h2>
<p>Động cơ 1.5L chỉ tiêu thụ 4.5L/100km trong điều kiện hỗn hợp.</p>
<h2>Độ tin cậy cao</h2>
<p>Chất lượng Toyota đảm bảo, chi phí bảo dưỡng thấp, giá trị bán lại cao.</p>`,
          summary: 'Với khả năng tiết kiệm nhiên liệu, chất lượng đáng tin cậy và giá cả hợp lý, Toyota Vios tiếp tục dẫn đầu thị trường sedan hạng B tại Việt Nam.',
          category: 'Ô tô',
          author_name: 'Đội ngũ đánh giá',
          status: 'published',
          published_at: new Date(),
        },
      ]);

      console.log('✅ 示例新闻数据插入完成');
    }

    console.log('🎉 数据库同步完成！');
    process.exit(0);
  } catch (error) {
    console.error('❌ 数据库同步失败:', error);
    process.exit(1);
  }
}

syncDatabase();

