import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';
import { LLMChain } from 'langchain/chains';
import Motorcycle from '../models/Motorcycle';
import Car from '../models/Car';
import NewsService from './NewsService';
import { Op } from 'sequelize';

/**
 * 用户测评生成服务
 * 基于LangChain + Gemini 2.5 Flash Lite生成真实感人的用户体验分享
 */
class ReviewGeneratorService {
  private llm: ChatOpenAI;
  
  // 越南常见名字
  private vietnameseNames = [
    'Nguyễn Văn Minh', 'Trần Thị Lan', 'Lê Hoàng Nam', 'Phạm Thị Hương',
    'Hoàng Văn Hùng', 'Vũ Thị Mai', 'Đặng Quốc Anh', 'Bùi Thị Linh',
    'Đỗ Văn Tuấn', 'Ngô Thị Thanh', 'Dương Minh Quân', 'Lý Thị Nga',
    'Phan Văn Đức', 'Võ Thị Tâm', 'Đinh Minh Hiếu', 'Tạ Thị Hoa',
    'Trương Văn Long', 'Lưu Thị Yến', 'Mai Quốc Bảo', 'Chu Thị Phượng'
  ];

  // 使用场景
  private usageScenarios = [
    'đi làm hàng ngày',
    'chạy grab',
    'giao hàng',
    'đi học',
    'đi chơi cuối tuần',
    'đi phượt',
    'sử dụng gia đình',
    'chạy shipper'
  ];

  constructor() {
    // 使用OpenRouter API连接Gemini 2.5 Flash Lite
    this.llm = new ChatOpenAI({
      modelName: 'google/gemini-2.0-flash-exp:free',
      temperature: 0.9, // 高温度产生更自然多样的内容
      maxTokens: 2000,
      openAIApiKey: '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',
      configuration: {
        baseURL: 'https://openrouter.ai/api/v1',
        apiKey: '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',
      },
    });
  }

  /**
   * 生成一条用户测评（发布到news板块）
   */
  public async generateOne(): Promise<boolean> {
    try {
      // 1. 随机选择车辆（摩托车或汽车）
      const vehicleType = Math.random() > 0.7 ? 'car' : 'motorcycle'; // 70%摩托车，30%汽车
      let vehicle: any;

      if (vehicleType === 'motorcycle') {
        vehicle = await Motorcycle.findOne({
          where: { status: 'active' },
          order: Motorcycle.sequelize!.random(),
        });
      } else {
        vehicle = await Car.findOne({
          where: { status: 'active' },
          order: Car.sequelize!.random(),
        });
      }

      if (!vehicle) {
        console.log('❌ 没有找到活跃的车辆');
        return false;
      }

      // 2. 随机选择作者和场景
      const authorName = this.getRandomElement(this.vietnameseNames);
      const usageScenario = this.getRandomElement(this.usageScenarios);
      const usageDuration = this.getRandomUsageDuration();
      const rating = Math.floor(Math.random() * 2) + 4; // 4-5星好评

      // 3. 使用LangChain生成测评内容（如果失败则使用备用方案）
      console.log(`🤖 正在为 ${vehicle.brand} ${vehicle.model} 生成用户测评...`);
      let review;
      try {
        review = await this.generateReviewContent(vehicle, usageScenario, usageDuration, rating);
      } catch (error: any) {
        console.log(`⚠️  LLM生成失败(${error.message})，使用备用方案...`);
        review = this.generateFallbackReview(vehicle, usageScenario, usageDuration, rating);
      }

      // 4. 保存到news表（作为特殊类型的新闻）
      const newsData = {
        title: review.title,
        content: review.content,
        summary: review.excerpt,
        category: 'Đánh giá người dùng', // 用户测评分类
        author_name: authorName,
        status: 'published',
        featured_image: vehicle.image_url || '',
        is_featured: false,
      };

      await NewsService.createNews(newsData);

      console.log(`✅ 成功生成用户测评: ${vehicle.brand} ${vehicle.model} - ${authorName}`);
      return true;
    } catch (error) {
      console.error('❌ 生成测评失败:', error);
      console.error('详细错误:', error);
      return false;
    }
  }

  /**
   * 使用LangChain生成测评内容
   */
  private async generateReviewContent(
    motorcycle: any,
    usageScenario: string,
    usageDuration: string,
    rating: number
  ): Promise<any> {
    // 创建提示词模板
    const promptTemplate = new PromptTemplate({
      template: `Bạn là một người dùng xe máy thực tế ở Việt Nam, đã sử dụng {brand} {model} trong {duration} cho mục đích {scenario}.

Thông tin xe:
- Thương hiệu: {brand} {model}
- Giá: {price} triệu VNĐ
- Phân loại: {category}
- Động cơ: {engine}
- Cân nặng: {weight}kg
- Bình xăng: {fuel}L

Hãy viết một bài đánh giá chân thực, cảm xúc và chi tiết từ góc nhìn người dùng thực tế. Đánh giá {rating} sao.

YÊU CẦU VỀ CẤU TRÚC (QUAN TRỌNG):
1. Nội dung PHẢI có cấu trúc rõ ràng với các tiêu đề phụ
2. Sử dụng HTML tags: <h2> cho tiêu đề chính, <h3> cho tiểu mục, <p> cho đoạn văn, <ul><li> cho danh sách
3. Cấu trúc bắt buộc:
   - Đoạn mở đầu (giới thiệu)
   - 4-5 phần nội dung với tiêu đề <h3>, mỗi phần 2-3 đoạn <p>
   - Phần kết luận với <h3>

YÊU CẦU VỀ NỘI DUNG:
1. Phải viết bằng giọng văn tự nhiên, như người thật chia sẻ kinh nghiệm
2. Phải có chi tiết cụ thể về trải nghiệm sử dụng hàng ngày
3. Phải có cảm xúc chân thực (vui, lo lắng, hài lòng...)
4. Phải đề cập đến ưu điểm VÀ nhược điểm (không hoàn hảo 100%)
5. Phải có lời khuyên cho người đang cân nhắc mua xe
6. Độ dài: 600-800 từ (BẮT BUỘC phải đủ 600 từ trở lên)
7. Phải để người đọc cảm thấy "đúng là kinh nghiệm thật"

Các tiêu đề phụ gợi ý (chọn 4-5 trong số này):
- "Ấn tượng ban đầu"
- "Trải nghiệm lái xe hàng ngày"
- "Hiệu suất và động cơ"
- "Tiết kiệm nhiên liệu"
- "Thiết kế và tiện nghi"
- "Chi phí sử dụng"
- "Ưu điểm nổi bật"
- "Nhược điểm cần lưu ý"
- "Lời khuyên cho người mua"

VÍ DỤ CẤU TRÚC:
<p>Đoạn mở đầu giới thiệu...</p>

<h3>Ấn tượng ban đầu</h3>
<p>Nội dung...</p>

<h3>Trải nghiệm lái xe</h3>
<p>Nội dung chi tiết...</p>
<p>Nội dung bổ sung...</p>

<h3>Ưu điểm nổi bật</h3>
<ul>
<li>Điểm mạnh 1</li>
<li>Điểm mạnh 2</li>
</ul>

<h3>Lời khuyên</h3>
<p>Kết luận và khuyến nghị...</p>

Trả về JSON format:
{{
  "title": "Tiêu đề hấp dẫn (40-80 ký tự)",
  "content": "Nội dung HTML có cấu trúc với <h3>, <p>, <ul>, <li> (600-800 từ)",
  "excerpt": "Tóm tắt thu hút (150-200 ký tự)"
}}`,
      inputVariables: ['brand', 'model', 'duration', 'scenario', 'price', 'category', 'engine', 'weight', 'fuel', 'rating'],
    });

    const chain = new LLMChain({
      llm: this.llm,
      prompt: promptTemplate,
    });

    const result = await chain.call({
      brand: motorcycle.brand,
      model: motorcycle.model,
      duration: usageDuration,
      scenario: usageScenario,
      price: (motorcycle.price_vnd / 1000000).toFixed(1),
      category: motorcycle.category,
      engine: motorcycle.engine_cc ? `${motorcycle.engine_cc}cc` : 'điện',
      weight: motorcycle.weight_kg || '120',
      fuel: motorcycle.fuel_capacity_l || '4',
      rating: rating,
    });

    // 解析JSON响应
    try {
      const text = result.text.trim();
      // 尝试提取JSON（可能被markdown包裹）
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('无法解析JSON响应');
    } catch (error) {
      console.error('JSON解析失败，使用备用方案:', error);
      // 备用方案：简单生成
      return this.generateFallbackReview(motorcycle, usageScenario, usageDuration, rating);
    }
  }

  /**
   * 备用生成方案（当LLM失败时）- HTML格式
   */
  private generateFallbackReview(motorcycle: any, usageScenario: string, usageDuration: string, rating: number): any {
    const brand = motorcycle.brand;
    const model = motorcycle.model;
    const price = (motorcycle.price_vnd/1000000).toFixed(1);
    const engine = motorcycle.engine_cc ? `${motorcycle.engine_cc}cc` : 'động cơ điện';
    
    return {
      title: `Trải nghiệm ${brand} ${model} sau ${usageDuration} ${usageScenario}`,
      content: `<p>Mình đã sử dụng ${brand} ${model} được ${usageDuration} rồi, chủ yếu ${usageScenario}. Sau thời gian trải nghiệm thực tế, mình muốn chia sẻ một số cảm nhận để anh em tham khảo.</p>

<h3>Ấn tượng ban đầu</h3>
<p>Lúc mới mua, điều đầu tiên mình chú ý là thiết kế khá đẹp mắt và hiện đại. Với mức giá ${price} triệu, xe ${brand} ${model} mang lại cảm giác khá chất lượng. Động cơ ${engine} khá đủ dùng cho nhu cầu di chuyển hàng ngày của mình.</p>

<h3>Trải nghiệm sử dụng hàng ngày</h3>
<p>Sau ${usageDuration} ${usageScenario}, mình thấy xe chạy khá ổn định. Điểm mạnh nhất của xe là độ bền và tiết kiệm nhiên liệu. Mình ${usageScenario} mỗi ngày nhưng xe vẫn rất tốt, ít hỏng vặt.</p>

<p>Xe khá linh hoạt trong phố, phanh êm, tăng tốc mượt mà. Đặc biệt là khả năng tiết kiệm nhiên liệu rất tốt, giúp mình tiết kiệm được kha khá chi phí hàng tháng.</p>

<h3>Ưu điểm nổi bật</h3>
<ul>
<li>Tiết kiệm nhiên liệu, chi phí sử dụng thấp</li>
<li>Độ bền cao, ít hỏng vặt</li>
<li>Thiết kế đẹp mắt, hiện đại</li>
<li>Giá cả hợp lý cho phân khúc</li>
<li>Linh kiện dễ tìm, bảo dưỡng thuận tiện</li>
</ul>

<h3>Nhược điểm cần lưu ý</h3>
<ul>
<li>Yên hơi cứng khi đi xa</li>
<li>Một số phụ kiện đi kèm chưa được tốt lắm</li>
<li>Cần thời gian làm quen với vận hành</li>
</ul>

<h3>Lời khuyên cho người mua</h3>
<p>Nhìn chung, với mức giá ${price} triệu, mình thấy ${brand} ${model} là lựa chọn khá hợp lý. Nếu bạn đang tìm xe ${usageScenario}, mình nghĩ đây là option đáng cân nhắc đấy!</p>

<p>Đặc biệt phù hợp với những bạn ưu tiên sự tiết kiệm và độ bền. Tuy có một số nhược điểm nhỏ, nhưng với mức giá này thì hoàn toàn chấp nhận được.</p>`,
      excerpt: `Chia sẻ trải nghiệm ${usageDuration} ${usageScenario} với ${brand} ${model} - Ưu nhược điểm thực tế và lời khuyên cho người đang cân nhắc mua xe.`
    };
  }

  /**
   * 随机获取使用时长
   */
  private getRandomUsageDuration(): string {
    const durations = [
      '3 tháng', '6 tháng', '1 năm', '1.5 năm', '2 năm',
      'gần 1 năm', 'hơn 6 tháng', 'được 4 tháng'
    ];
    return this.getRandomElement(durations);
  }

  /**
   * 随机获取数组元素
   */
  private getRandomElement<T>(array: T[]): T {
    return array[Math.floor(Math.random() * array.length)];
  }

  /**
   * 清理旧数据（用户测评类新闻保留最新30条）
   */
  public async cleanOldData(): Promise<void> {
    // 用户测评现在存储在news表中，category为"Đánh giá người dùng"
    // 可选：可以在这里添加清理逻辑，但News表已经有管理功能，暂时不需要
    console.log('📝 用户测评存储在News表中，通过后台管理');
  }
}

export default new ReviewGeneratorService();

