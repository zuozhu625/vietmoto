import Question from '../models/Question';
import Answer from '../models/Answer';
import Motorcycle from '../models/Motorcycle';
import Car from '../models/Car';
import { dbConfig } from '../config/database';
import { Op } from 'sequelize';

/**
 * Q&A 自动生成服务
 * 基于车辆数据自动生成越南语问题和答案
 */
class QAGeneratorService {
  // 问题模板（越南语）- 拟人化版本，加入口头语和亲切表达
  private questionTemplates = {
    motorcycle: [
      {
        category: 'Tư vấn mua xe',
        templates: [
          'Anh em ơi, {brand} {model} {year} này có phù hợp cho người mới chơi xe như mình không?',
          'Các bác cho em hỏi {brand} {model} giá {price} có đáng mua không ạ?',
          'Mọi người ơi, so sánh {brand} {model} với các xe cùng phân khúc {cc}cc thì sao nhỉ?',
          'Em đang phân vân nên mua {brand} {model} hay chọn xe khác trong tầm giá {price}?',
          'Cho mình hỏi {brand} {model} có gì nổi bật so với đối thủ không ạ?',
          'Mình cao {height}m, mua {brand} {model} có phù hợp không các bác?',
          'Các anh chị ơi, {brand} {model} phù hợp đi trong thành phố hay đường dài hơn?',
          'Em có ngân sách {price}, mua {brand} {model} có đủ không ạ?',
          'Cho em hỏi {brand} {model} dành cho nam hay nữ phù hợp hơn vậy?',
          'Anh em có ai dùng xe {category} {brand} {model} chưa? Có đáng tin cậy không?',
          'Em là sinh viên, {brand} {model} có phù hợp không các bác?',
          'Mình định mua {brand} {model} để đi làm, có tiện không anh em?',
          'Các bác ơi, {brand} {model} giá {price} có phải mức giá tốt không?',
          'Em mới học lái, nên chọn {brand} {model} không các anh chị?',
        ]
      },
      {
        category: 'Đánh giá xe',
        templates: [
          'Anh em nào đã trải nghiệm {brand} {model} {year} rồi? Đánh giá ưu nhược điểm giúp mình với!',
          'Cho mình hỏi {brand} {model} vận hành thực tế như thế nào ạ?',
          'Các bác ơi, xe {brand} {model} có tiết kiệm nhiên liệu không?',
          'Mọi người cho em hỏi chất lượng {brand} {model} có bền không ạ?',
          'Em muốn hỏi {brand} {model} {cc}cc có đủ mạnh cho đường trường không các anh?',
          'Anh em ơi, phanh ABS trên {brand} {model} có thực sự cần thiết không?',
          'Cho em hỏi {brand} {model} trọng lượng {weight}kg có nặng quá không ạ?',
          'Mình hỏi yên cao {seat_height}mm của {brand} {model} có phù hợp không các bác?',
          'Các anh chị ơi, {brand} {model} có tiêu tốn xăng lắm không?',
          'Em muốn biết động cơ {cc}cc {power}HP của {brand} {model} có ồn không ạ?',
        ]
      },
      {
        category: 'Bảo dưỡng',
        templates: [
          'Anh em ơi, {brand} {model} cần bảo dưỡng những gì vậy?',
          'Các bác cho em hỏi chi phí bảo dưỡng {brand} {model} khoảng bao nhiêu ạ?',
          'Mọi người ơi, {brand} {model} có dễ thay phụ tùng không?',
          'Em muốn hỏi {brand} {model} bao lâu cần thay nhớt một lần ạ?',
          'Cho mình hỏi phụ tùng {brand} {model} có đắt lắm không các bác?',
          'Anh chị nào biết {brand} {model} có cần bảo dưỡng chuyên dụng không?',
        ]
      },
      {
        category: 'So sánh xe',
        templates: [
          'Anh em ơi, so sánh {brand} {model} vs đối thủ cùng phân khúc thì sao?',
          'Cho mình hỏi {brand} {model} động cơ {cc}cc {power}HP có mạnh không ạ?',
          'Em đang phân vân giữa {brand} {model} và {brand2} {model2}, nên chọn xe nào các bác?',
          'Các anh chị ơi, xe {cc}cc thì {brand} {model} hay đối thủ tốt hơn?',
          'Mọi người ơi, giá {price} thì {brand} {model} có cạnh tranh không?',
          'Em muốn hỏi {brand} {model} so với xe cùng giá có lợi thế gì ạ?',
        ]
      },
      {
        category: 'Thông số kỹ thuật',
        templates: [
          'Anh em ơi, {brand} {model} công suất {power}HP có đủ dùng không?',
          'Cho mình hỏi động cơ {cc}cc của {brand} {model} có mạnh mẽ không ạ?',
          'Các bác ơi, {brand} {model} mô-men xoắn {torque}Nm như thế nào?',
          'Em muốn hỏi bình xăng {fuel_capacity}L của {brand} {model} có nhỏ quá không?',
          'Mọi người ơi, {brand} {model} trọng lượng {weight}kg có khó điều khiển không?',
          'Cho em hỏi khoảng sáng gầm {ground_clearance}mm - {brand} {model} có đủ cao không ạ?',
        ]
      },
      {
        category: 'Xe điện',
        templates: [
          'Anh em ơi, xe điện {brand} {model} đi được bao xa vậy?',
          'Cho mình hỏi {brand} {model} sạc đầy mất bao lâu ạ?',
          'Các bác có ai biết pin xe điện {brand} {model} có bền không?',
          'Em muốn hỏi {brand} {model} giá {price} so với xe xăng như thế nào?',
          'Mọi người ơi, xe điện {brand} {model} có phù hợp đi xa không?',
          'Cho em hỏi {brand} {model} công suất {power}kW có đủ mạnh không ạ?',
        ]
      },
      {
        category: 'Sử dụng thực tế',
        templates: [
          'Anh em ơi, {brand} {model} đi trong thành phố có tiện không?',
          'Cho mình hỏi {brand} {model} có phù hợp chở người sau không ạ?',
          'Các bác ơi, {brand} {model} leo dốc có khỏe không?',
          'Em muốn biết cốp xe {brand} {model} có rộng không ạ?',
          'Mọi người ơi, {brand} {model} đi mưa có an toàn không?',
          'Cho em hỏi {brand} {model} phanh ABS có hoạt động tốt không?',
          'Anh chị nào biết {brand} {model} đi đường xấu có ổn định không?',
          'Em hỏi {brand} {model} chạy đường cao tốc có an toàn không ạ?',
        ]
      },
      {
        category: 'Tiết kiệm xăng',
        templates: [
          'Anh em ơi, {brand} {model} tiêu thụ bao nhiêu xăng/100km vậy?',
          'Các bác chỉ em cách lái {brand} {model} tiết kiệm xăng nhất với!',
          'Cho mình hỏi {brand} {model} có thực sự tiết kiệm nhiên liệu không ạ?',
          'Mọi người ơi, so sánh mức tiêu hao xăng {brand} {model} với đối thủ thì sao?',
          'Em muốn biết {brand} {model} động cơ {cc}cc ăn xăng như thế nào?',
          'Anh chị nào có mẹo tiết kiệm xăng khi sử dụng {brand} {model} không?',
        ]
      },
      {
        category: 'Kỹ năng lái xe',
        templates: [
          'Anh em ơi, người mới lái {brand} {model} cần lưu ý gì vậy?',
          'Các bác chỉ em kỹ thuật sang số mượt cho {brand} {model} với!',
          'Cho mình hỏi {brand} {model} có khó lái lắm không ạ?',
          'Em muốn hỏi cách phanh an toàn với {brand} {model} như thế nào?',
          'Mọi người ơi, lái {brand} {model} trong mưa cần chú ý điều gì?',
          'Anh chị nào chỉ em {brand} {model} cách vào cua đúng kỹ thuật?',
        ]
      },
      {
        category: 'Độ xe - Phụ kiện',
        templates: [
          'Anh em ơi, {brand} {model} nên độ những gì vậy?',
          'Các bác tư vấn phụ kiện nào phù hợp với {brand} {model}?',
          'Cho mình hỏi {brand} {model} có thể độ pô không ạ?',
          'Em muốn biết nên thay lốp gì cho {brand} {model}?',
          'Mọi người ơi, {brand} {model} độ LED có ảnh hưởng gì không?',
          'Anh chị nào biết chi phí độ {brand} {model} cơ bản là bao nhiêu?',
        ]
      },
      {
        category: 'Xe cũ - Mua bán',
        templates: [
          'Anh em ơi, {brand} {model} đi {year} còn giữ giá không vậy?',
          'Các bác chỉ em mua {brand} {model} cũ cần kiểm tra gì?',
          'Cho mình hỏi {brand} {model} sau 2-3 năm sử dụng như thế nào ạ?',
          'Em muốn biết giá bán lại {brand} {model} sau 1 năm khoảng bao nhiêu?',
          'Mọi người ơi, {brand} {model} có dễ bán lại không?',
          'Anh chị tư vấn nên mua {brand} {model} mới hay cũ?',
        ]
      },
      {
        category: 'Bảo hiểm - Giấy tờ',
        templates: [
          'Anh em ơi, {brand} {model} nên mua bảo hiểm loại nào vậy?',
          'Các bác cho em hỏi chi phí bảo hiểm {brand} {model} hàng năm bao nhiêu?',
          'Cho mình hỏi {brand} {model} cần giấy tờ gì khi mua ạ?',
          'Em muốn biết đăng ký {brand} {model} có phức tạp không?',
          'Mọi người ơi, {brand} {model} phí trước bạ là bao nhiêu?',
        ]
      },
      {
        category: 'Đi làm - Giao hàng',
        templates: [
          'Anh em ơi, {brand} {model} có phù hợp chạy xe ôm công nghệ không?',
          'Các bác cho em hỏi {brand} {model} dùng để giao hàng có tốt không?',
          'Cho mình hỏi chạy grab bằng {brand} {model} có lợi không ạ?',
          'Em muốn biết {brand} {model} đi làm xa mỗi ngày có bền không?',
          'Mọi người ơi, {brand} {model} phù hợp chở hàng nặng không?',
          'Anh chị nào làm shipper, nên dùng {brand} {model} không?',
        ]
      },
      {
        category: 'Phượt - Đi xa',
        templates: [
          'Anh em ơi, {brand} {model} có phù hợp đi phượt không vậy?',
          'Các bác cho em hỏi {brand} {model} đi đường dài có mệt không ạ?',
          'Cho mình hỏi {brand} {model} leo đèo Hải Vân có khỏe không?',
          'Em định đi phượt bằng {brand} {model}, cần chuẩn bị gì các anh chị?',
          'Mọi người ơi, {brand} {model} bình xăng {fuel_capacity}L đi được bao xa?',
          'Anh chị nào biết {brand} {model} có ổn định khi chạy tốc độ cao không?',
        ]
      },
      {
        category: 'Mùa mưa - Thời tiết',
        templates: [
          'Anh em ơi, {brand} {model} đi mưa có trơn trượt không vậy?',
          'Các bác cho em hỏi phanh {brand} {model} trong mưa có an toàn không?',
          'Cho mình hỏi {brand} {model} chống nước có tốt không ạ?',
          'Em muốn biết {brand} {model} mùa mưa cần bảo dưỡng thêm gì?',
          'Mọi người ơi, lốp {brand} {model} có bám đường tốt khi mưa không?',
        ]
      },
      {
        category: 'Người mới - Học lái',
        templates: [
          'Em vừa thi đỗ bằng A1, nên mua {brand} {model} không các bác?',
          'Anh em ơi, {brand} {model} có dễ điều khiển cho người mới không?',
          'Các anh chị cho em hỏi học lái xe bằng {brand} {model} có phù hợp không?',
          'Cho mình hỏi {brand} {model} dễ lái hay khó lái cho người mới ạ?',
          'Em mới học lái, nên chọn {brand} {model} hay xe khác các bác?',
          'Mọi người ơi, {brand} {model} trọng lượng {weight}kg người mới có nâng được không?',
        ]
      },
      {
        category: 'Chi phí sử dụng',
        templates: [
          'Anh em ơi, chi phí nuôi {brand} {model} mỗi tháng là bao nhiêu vậy?',
          'Các bác cho em hỏi {brand} {model} có tốn kém lắm khi sử dụng không?',
          'Cho mình hỏi {brand} {model} phụ tùng và bảo dưỡng có đắt không ạ?',
          'Em muốn biết trung bình chạy {brand} {model} hết bao nhiêu tiền/tháng?',
          'Mọi người ơi, {brand} {model} có phù hợp cho người thu nhập thấp không?',
        ]
      },
      {
        category: 'An toàn - Luật giao thông',
        templates: [
          'Anh em ơi, {brand} {model} có an toàn cho người mới không vậy?',
          'Các bác cho em hỏi {brand} {model} phanh ABS có thực sự cần thiết không?',
          'Cho mình hỏi đi {brand} {model} có cần đội mũ bảo hiểm fullface không ạ?',
          'Em muốn biết {brand} {model} tốc độ tối đa bao nhiêu có an toàn?',
          'Mọi người ơi, {brand} {model} đèn chiếu sáng có đủ sáng không?',
        ]
      }
    ],
    car: [
      {
        category: 'Tư vấn mua xe',
        templates: [
          '{brand} {model} {year} có phù hợp cho gia đình không?',
          'Nên mua {brand} {model} hay chọn xe khác?',
          '{brand} {model} giá từ {price} có đáng mua không?',
        ]
      },
      {
        category: 'Đánh giá xe',
        templates: [
          'Đánh giá {brand} {model} - Ưu nhược điểm chi tiết?',
          '{brand} {model} vận hành có êm không?',
          'An toàn của {brand} {model} như thế nào?',
        ]
      }
    ]
  };

  /**
   * 生成摩托车相关的问答
   */
  async generateMotorcycleQA(): Promise<boolean> {
    try {
      // 随机获取一辆摩托车
      const motorcycles = await Motorcycle.findAll({
        where: { status: 'active' },
        order: dbConfig.random(),
        limit: 1
      });

      if (motorcycles.length === 0) {
        console.log('没有可用的摩托车数据');
        return false;
      }

      const moto = motorcycles[0];
      
      // 随机选择一个类别
      const categoryData = this.questionTemplates.motorcycle[
        Math.floor(Math.random() * this.questionTemplates.motorcycle.length)
      ];
      
      // 随机选择一个模板
      const template = categoryData.templates[
        Math.floor(Math.random() * categoryData.templates.length)
      ];

      // 随机获取另一辆车用于对比（如果需要）
      let moto2: any = null;
      if (template.includes('{brand2}')) {
        const motorcycles2 = await Motorcycle.findAll({
          where: { 
            status: 'active',
            category: moto.category,
            id: { [Op.ne]: moto.id }
          },
          order: dbConfig.random(),
          limit: 1
        });
        moto2 = motorcycles2[0];
      }

      // 生成问题标题 - 支持更多参数替换
      let title = template
        .replace('{brand}', moto.brand)
        .replace('{model}', moto.model)
        .replace('{year}', moto.year.toString())
        .replace('{cc}', moto.engine_cc?.toString() || '150')
        .replace('{power}', moto.power_hp?.toString() || '')
        .replace('{price}', this.formatPrice(moto.price_vnd))
        .replace('{category}', moto.category)
        .replace('{torque}', moto.torque_nm?.toString() || '')
        .replace('{weight}', moto.weight_kg?.toString() || '')
        .replace('{seat_height}', moto.seat_height_mm?.toString() || '')
        .replace('{fuel_capacity}', moto.fuel_capacity_l?.toString() || '')
        .replace('{ground_clearance}', moto.ground_clearance_mm?.toString() || '')
        .replace('{height}', '1.7'); // 默认身高
      
      // 替换对比车型变量
      if (moto2) {
        title = title
          .replace('{brand2}', moto2.brand)
          .replace('{model2}', moto2.model);
      }

      // 生成问题内容（更详细）
      const content = this.generateQuestionContent(moto, categoryData.category);

      // 创建问题
      const question = await Question.create({
        title,
        content,
        category: categoryData.category,
        subcategory: moto.category,
        vehicle_type: 'motorcycle',
        vehicle_id: moto.id,
        author_id: 'auto-generated',
        view_count: Math.floor(Math.random() * 500) + 100,
        votes_count: Math.floor(Math.random() * 50),
        answers_count: 0,
        has_accepted_answer: false,
        status: 'open'
      });

      // 生成答案（基于车辆参数）
      const answerContent = this.generateAnswer(moto, categoryData.category);
      
      await Answer.create({
        question_id: question.id,
        content: answerContent,
        author_id: 'expert-system',
        votes_count: Math.floor(Math.random() * 30) + 10,
        is_accepted: true
      });

      // 更新问题的答案数
      await question.update({
        answers_count: 1,
        has_accepted_answer: true
      });

      console.log(`✅ 已生成Q&A: ${title}`);
      return true;
    } catch (error) {
      console.error('生成摩托车Q&A失败:', error);
      return false;
    }
  }

  /**
   * 生成问题内容（扩充版 - 更多参数细节）
   */
  private generateQuestionContent(vehicle: any, category: string): string {
    const specs = [];
    
    if (vehicle.engine_cc) specs.push(`động cơ ${vehicle.engine_cc}cc`);
    if (vehicle.power_hp) specs.push(`công suất ${vehicle.power_hp} mã lực`);
    if (vehicle.torque_nm) specs.push(`mô-men xoắn ${vehicle.torque_nm} Nm`);
    if (vehicle.price_vnd) specs.push(`giá ${this.formatPrice(vehicle.price_vnd)}`);
    
    const specsText = specs.length > 0 ? ` với ${specs.join(', ')}` : '';

    const contents = {
      'Tư vấn mua xe': `Mình đang quan tâm đến ${vehicle.brand} ${vehicle.model}${specsText}. Các bác cho mình xin ý kiến có nên mua xe này không? Xe này phù hợp cho ai? Có những ưu nhược điểm gì cần lưu ý? Mong các bác tư vấn giúp!`,
      
      'Đánh giá xe': `Các bác đã có kinh nghiệm với ${vehicle.brand} ${vehicle.model} chưa? Cho mình hỏi về chất lượng, độ bền, tiêu hao nhiên liệu và trải nghiệm thực tế khi sử dụng xe này. Có đáng đồng tiền bát gạo không?`,
      
      'Bảo dưỡng': `${vehicle.brand} ${vehicle.model}${specsText} cần bảo dưỡng những gì? Bao lâu thì phải thay nhớt? Chi phí bảo dưỡng định kỳ khoảng bao nhiêu? Phụ tùng có dễ kiếm và giá cả phải chăng không?`,
      
      'So sánh xe': `${vehicle.brand} ${vehicle.model}${specsText} so với các đối thủ cùng phân khúc thì như thế nào? Mạnh điểm và yếu điểm gì? Hiệu suất, giá cả, trang bị có cạnh tranh không? Nên chọn xe này hay xe khác?`,
      
      'Thông số kỹ thuật': `Mình muốn hỏi chi tiết về thông số kỹ thuật của ${vehicle.brand} ${vehicle.model}${specsText}. ${vehicle.weight_kg ? `Xe nặng ${vehicle.weight_kg}kg có khó điều khiển không? ` : ''}${vehicle.seat_height_mm ? `Yên cao ${vehicle.seat_height_mm}mm có phù hợp với người thấp không? ` : ''}Mong các bác giải đáp!`,
      
      'Xe điện': `Xe điện ${vehicle.brand} ${vehicle.model} giá ${this.formatPrice(vehicle.price_vnd)} - mình muốn hỏi về pin, quãng đường đi được, thời gian sạc và chi phí vận hành so với xe xăng. Xe này có phù hợp cho việc đi làm hàng ngày không?`,
      
      'Sử dụng thực tế': `${vehicle.brand} ${vehicle.model} sử dụng thực tế như thế nào? Đi trong thành phố có tiện không? Leo dốc có khỏe không? ${vehicle.abs ? 'Phanh ABS có hoạt động tốt không? ' : ''}Mong các bác chia sẻ kinh nghiệm thực tế!`,
      
      'Tiết kiệm xăng': `${vehicle.brand} ${vehicle.model} động cơ ${vehicle.engine_cc}cc${specsText} - mình muốn hỏi về mức tiêu hao nhiên liệu thực tế. Đi trong phố và đường dài ăn xăng như thế nào? Có cách nào tiết kiệm hơn không?`,
      
      'Kỹ năng lái xe': `Mình mới mua ${vehicle.brand} ${vehicle.model}, chưa có nhiều kinh nghiệm. Các bác có thể chia sẻ kỹ năng lái xe an toàn, cách sang số mượt, phanh đúng cách không? Mong được chỉ dạy!`,
      
      'Độ xe - Phụ kiện': `${vehicle.brand} ${vehicle.model} mình muốn độ để cá tính hóa và nâng cao hiệu suất. Các bác tư vấn nên độ những gì? Pô, lốp, đèn LED? Chi phí và hiệu quả như thế nào?`,
      
      'Xe cũ - Mua bán': `${vehicle.brand} ${vehicle.model} giá ${this.formatPrice(vehicle.price_vnd)} - nếu mua xe cũ cần kiểm tra những gì? Xe này có giữ giá không? Sau 2-3 năm bán lại được giá bao nhiêu?`,
      
      'Bảo hiểm - Giấy tờ': `Mình định mua ${vehicle.brand} ${vehicle.model}, muốn hỏi về thủ tục đăng ký, bảo hiểm xe máy, phí trước bạ. Chi phí và giấy tờ cần chuẩn bị gì? Quy trình có phức tạp không?`,
      
      'Đi làm - Giao hàng': `${vehicle.brand} ${vehicle.model}${specsText} - mình định dùng để ${vehicle.fuel_type === 'Điện' ? 'chạy xe ôm điện hoặc giao hàng' : 'chạy grab hoặc giao hàng'}. Xe này có phù hợp không? Mỗi ngày chạy 100-150km có bền không?`,
      
      'Phượt - Đi xa': `${vehicle.brand} ${vehicle.model} với bình xăng ${vehicle.fuel_capacity_l || 4}L và động cơ ${vehicle.engine_cc}cc - có phù hợp đi phượt xa không? Đi Sài Gòn - Đà Lạt hoặc leo đèo Hải Vân có ổn không?`,
      
      'Mùa mưa - Thời tiết': `Mùa mưa sắp đến, ${vehicle.brand} ${vehicle.model} đi mưa có an toàn không? Phanh${vehicle.abs ? ' ABS' : ''} có hoạt động tốt trong mưa không? Cần chuẩn bị hoặc bảo dưỡng gì thêm?`,
      
      'Người mới - Học lái': `Mình vừa thi đỗ bằng lái A1, đang muốn mua xe đầu tiên. ${vehicle.brand} ${vehicle.model} có phù hợp cho người mới lái không? Có dễ넘, dễ điều khiển không? Giá ${this.formatPrice(vehicle.price_vnd)} có hợp lý không?`,
      
      'Chi phí sử dụng': `${vehicle.brand} ${vehicle.model} giá mua ${this.formatPrice(vehicle.price_vnd)} - mình muốn biết chi phí sử dụng hàng tháng bao gồm xăng, bảo dưỡng, bảo hiểm là bao nhiêu? Có tốn kém không?`,
      
      'An toàn - Luật giao thông': `${vehicle.brand} ${vehicle.model} có an toàn không? ${vehicle.abs ? 'ABS có thực sự giúp phanh tốt hơn? ' : 'Không có ABS có nguy hiểm không? '}Tốc độ an toàn khi đi trong phố và đường dài là bao nhiêu?`
    };

    return contents[category as keyof typeof contents] || contents['Tư vấn mua xe'];
  }

  /**
   * 生成拟人化答案（基于车辆真实参数，50字以上）
   */
  private generateAnswer(vehicle: any, category: string): string {
    const answers: string[] = [];
    
    // 拟人化开场白（随机选择）
    const greetings = [
      `Chào bạn! Mình đã dùng ${vehicle.brand} ${vehicle.model} được một thời gian rồi, chia sẻ kinh nghiệm nhé!`,
      `Xin chào! ${vehicle.brand} ${vehicle.model} là một lựa chọn ${vehicle.category.toLowerCase()} khá tốt đấy, mình kể cho bạn nghe nhé.`,
      `Hi bạn! Về ${vehicle.brand} ${vehicle.model} thì mình có thể tư vấn được vì đã trải nghiệm rồi.`,
      `Chào bạn! Mình thấy bạn quan tâm đến ${vehicle.brand} ${vehicle.model}, để mình chia sẻ một chút kinh nghiệm nhé!`,
      `Hello! ${vehicle.brand} ${vehicle.model} à? Xe này mình biết khá rõ, để mình tư vấn cho bạn.`,
      `Chào bạn! Mình là người đã từng sử dụng ${vehicle.brand} ${vehicle.model}, rất vui được chia sẻ kinh nghiệm!`,
      `Xin chào! Về ${vehicle.brand} ${vehicle.model} thì mình có khá nhiều trải nghiệm, để kể cho bạn nghe nhé.`,
      `Hi! ${vehicle.brand} ${vehicle.model} này mình đã test ride và sử dụng rồi, có thể tư vấn cho bạn được.`,
      `Chào bạn! ${vehicle.brand} ${vehicle.model} là chiếc xe mình khá ưng ý, để mình review cho bạn nghe.`,
      `Hello! Mình thấy bạn hỏi về ${vehicle.brand} ${vehicle.model}, đây là xe mình có kinh nghiệm sử dụng đấy.`,
      `Chào bạn! ${vehicle.brand} ${vehicle.model} à? Mình vừa mới trải nghiệm xe này, chia sẻ cảm nhận nhé!`,
      `Xin chào! Về ${vehicle.brand} ${vehicle.model} thì mình có thể đưa ra lời khuyên vì đã dùng qua rồi.`,
      `Hi bạn! ${vehicle.brand} ${vehicle.model} này mình khá hiểu, để mình tư vấn chi tiết cho bạn.`,
      `Chào bạn! Mình đã có cơ hội trải nghiệm ${vehicle.brand} ${vehicle.model}, rất sẵn lòng chia sẻ!`,
      `Hello! ${vehicle.brand} ${vehicle.model} là một trong những xe mình đã dùng, để kể cho bạn nghe.`,
      `Chào bạn! Về ${vehicle.brand} ${vehicle.model} thì mình có góc nhìn thực tế, để chia sẻ kinh nghiệm nhé!`
    ];
    answers.push(greetings[Math.floor(Math.random() * greetings.length)]);
    
    // 拟人化动力性能描述
    if (vehicle.engine_cc && vehicle.power_hp) {
      if (vehicle.fuel_type === 'Điện') {
        const powerDescriptions = [
          `Về động cơ điện thì xe này khá ổn đấy! Công suất ${vehicle.power_hp} kW, chạy được tối đa ${Math.floor(vehicle.power_hp * 30)} km/h. Mình thấy rất phù hợp đi trong phố, lại tiết kiệm tiền điện nữa.`,
          `Xe điện này mình thích lắm! ${vehicle.power_hp} kW nghe có vẻ ít nhưng thực tế chạy phố rất êm, tốc độ tối đa ${Math.floor(vehicle.power_hp * 30)} km/h cũng đủ dùng rồi.`,
          `Nói thật là xe điện này tiết kiệm lắm bạn ạ! Công suất ${vehicle.power_hp} kW, tuy không mạnh bằng xe xăng nhưng đi trong thành phố thì quá đủ.`
        ];
        answers.push(powerDescriptions[Math.floor(Math.random() * powerDescriptions.length)]);
      } else {
        const engineDescriptions = [
          `Về động cơ thì ${vehicle.engine_cc}cc ${vehicle.power_hp} mã lực${vehicle.torque_nm ? ` với ${vehicle.torque_nm} Nm` : ''} - mình thấy khá ổn đấy! Đủ mạnh cho việc đi làm hàng ngày, đi chơi xa cũng không vấn đề gì.`,
          `Động cơ ${vehicle.engine_cc}cc này mình dùng thấy khá hài lòng. ${vehicle.power_hp} mã lực${vehicle.torque_nm ? ` và ${vehicle.torque_nm} Nm` : ''} nghe có vẻ ít nhưng thực tế chạy rất êm và đủ sức.`,
          `Thực tế thì ${vehicle.engine_cc}cc ${vehicle.power_hp} HP này chạy khá ngon bạn ạ! ${vehicle.torque_nm ? `Mô-men xoắn ${vehicle.torque_nm} Nm cũng ổn, ` : ''}leo dốc nhẹ nhàng, đi đường dài không mệt.`
        ];
        answers.push(engineDescriptions[Math.floor(Math.random() * engineDescriptions.length)]);
      }
    }
    
    // 拟人化特点描述
    const features: string[] = [];
    if (vehicle.abs) features.push('phanh ABS');
    if (vehicle.smart_key) features.push('Smart Key');
    if (vehicle.transmission) features.push(`hộp số ${vehicle.transmission}`);
    
    if (features.length > 0) {
      const featureDescriptions = [
        `Về trang bị thì xe này có ${features.join(', ')} - mình thấy khá đầy đủ đấy! Đặc biệt là ${features[0]} rất hữu ích trong thực tế.`,
        `Điểm cộng của xe này là có ${features.join(', ')}. Mình dùng thấy tiện lợi lắm, nhất là khi đi trong thành phố đông đúc.`,
        `Trang bị ${features.join(', ')} của xe này mình đánh giá cao. Thực sự giúp ích rất nhiều trong việc sử dụng hàng ngày.`
      ];
      answers.push(featureDescriptions[Math.floor(Math.random() * featureDescriptions.length)]);
    }
    
    // 拟人化价格评价
    const priceText = this.formatPrice(vehicle.price_vnd);
    if (vehicle.price_vnd < 30000000) {
      const budgetDescriptions = [
        `Về giá cả thì ${priceText} mình thấy khá hợp lý đấy! Phù hợp cho sinh viên hay người mới đi làm, không quá nặng gánh về tài chính.`,
        `Giá ${priceText} này mình thấy ổn lắm bạn ạ! Dành cho người có ngân sách hạn chế nhưng vẫn muốn có xe chất lượng.`,
        `${priceText} là mức giá khá dễ chịu rồi. Mình nghĩ phù hợp cho những bạn trẻ vừa bắt đầu đi làm.`
      ];
      answers.push(budgetDescriptions[Math.floor(Math.random() * budgetDescriptions.length)]);
    } else if (vehicle.price_vnd < 60000000) {
      const midRangeDescriptions = [
        `Giá ${priceText} thuộc tầm trung, mình thấy hợp lý với những gì xe mang lại. Phù hợp cho nhân viên văn phòng có thu nhập ổn định.`,
        `${priceText} không rẻ nhưng cũng không đắt quá. Mình nghĩ đáng đầu tư nếu bạn cần xe để đi làm lâu dài.`,
        `Với mức giá ${priceText}, mình thấy xe này có tính cạnh tranh tốt trong phân khúc. Đáng cân nhắc đấy!`
      ];
      answers.push(midRangeDescriptions[Math.floor(Math.random() * midRangeDescriptions.length)]);
    } else if (vehicle.price_vnd < 100000000) {
      const premiumDescriptions = [
        `Giá ${priceText} thuộc phân khúc cao cấp rồi. Mình thấy phù hợp cho những ai có điều kiện kinh tế khá và muốn xe chất lượng cao.`,
        `${priceText} không phải giá rẻ nhưng chất lượng xe xứng đáng. Nếu có điều kiện thì mình khuyên nên đầu tư.`,
        `Với ${priceText}, xe này dành cho những người có yêu cầu cao về chất lượng và tính năng. Đáng tiền lắm!`
      ];
      answers.push(premiumDescriptions[Math.floor(Math.random() * premiumDescriptions.length)]);
    } else {
      const luxuryDescriptions = [
        `${priceText} là mức giá cao cấp rồi bạn ạ! Xe này dành cho những ai muốn sở hữu công nghệ và thiết kế đỉnh cao nhất.`,
        `Giá ${priceText} thuộc phân khúc luxury. Mình thấy chỉ nên mua nếu bạn thực sự đam mê và có điều kiện tài chính tốt.`,
        `${priceText} không phải ai cũng có thể mua được. Nhưng nếu có điều kiện thì xe này thực sự đẳng cấp!`
      ];
      answers.push(luxuryDescriptions[Math.floor(Math.random() * luxuryDescriptions.length)]);
    }
    
    // 拟人化专门回答
    if (category === 'Thông số kỹ thuật') {
      // 拟人化技术参数分析
      if (vehicle.weight_kg) {
        const weightDescriptions = [
          `Về trọng lượng ${vehicle.weight_kg}kg thì mình thấy ${vehicle.weight_kg > 140 ? 'hơi nặng một chút, nhưng đổi lại xe rất vững chãi khi chạy' : vehicle.weight_kg > 120 ? 'vừa phải lắm, cân bằng tốt giữa ổn định và linh hoạt' : 'nhẹ nhàng, điều khiển dễ dàng lắm'}!`,
          `${vehicle.weight_kg}kg ${vehicle.weight_kg > 140 ? 'nghe có vẻ nặng nhưng thực tế mình thấy ổn, xe chạy rất ổn định' : vehicle.weight_kg > 120 ? 'là trọng lượng lý tưởng, không quá nặng cũng không quá nhẹ' : 'rất nhẹ, phụ nữ cũng dễ dàng điều khiển'}.`
        ];
        answers.push(weightDescriptions[Math.floor(Math.random() * weightDescriptions.length)]);
      }
      if (vehicle.seat_height_mm) {
        const seatDescriptions = [
          `Yên xe cao ${vehicle.seat_height_mm}mm - mình thấy ${vehicle.seat_height_mm > 800 ? 'hơi cao, phù hợp cho người cao trên 1.70m' : vehicle.seat_height_mm > 770 ? 'vừa vặn cho người cao 1.60-1.75m' : 'thấp vừa phải, người thấp cũng chạm đất dễ dàng'}.`,
          `Về độ cao yên ${vehicle.seat_height_mm}mm thì ${vehicle.seat_height_mm > 800 ? 'người thấp có thể hơi khó khăn, nên thử ngồi trước khi mua' : vehicle.seat_height_mm > 770 ? 'khá phù hợp với đa số người Việt Nam' : 'rất thoải mái, ai cũng ngồi được'}.`
        ];
        answers.push(seatDescriptions[Math.floor(Math.random() * seatDescriptions.length)]);
      }
      if (vehicle.fuel_capacity_l) {
        const fuelDescriptions = [
          `Bình xăng ${vehicle.fuel_capacity_l}L mình thấy ${vehicle.fuel_capacity_l > 5 ? 'khá lớn, đi xa thoải mái không lo hết xăng' : vehicle.fuel_capacity_l > 3 ? 'đủ dùng cho việc đi lại trong thành phố' : 'hơi nhỏ, cần đổ xăng thường xuyên hơn'}.`,
          `${vehicle.fuel_capacity_l}L ${vehicle.fuel_capacity_l > 5 ? 'là dung tích tốt, một lần đổ có thể chạy khá xa' : vehicle.fuel_capacity_l > 3 ? 'cũng ổn, phù hợp cho việc đi làm hàng ngày' : 'không nhiều lắm, nhưng cũng đủ dùng trong phố'}.`
        ];
        answers.push(fuelDescriptions[Math.floor(Math.random() * fuelDescriptions.length)]);
      }
      if (vehicle.ground_clearance_mm) {
        const clearanceDescriptions = [
          `Khoảng sáng gầm ${vehicle.ground_clearance_mm}mm - mình đánh giá ${vehicle.ground_clearance_mm > 150 ? 'khá cao, vượt địa hình tốt' : vehicle.ground_clearance_mm > 130 ? 'ổn, đủ dùng cho đường gồ ghề' : 'hơi thấp, cần cẩn thận khi qua ổ gà'}.`,
          `${vehicle.ground_clearance_mm}mm ${vehicle.ground_clearance_mm > 150 ? 'cao đấy, đi đường xấu cũng không sợ' : vehicle.ground_clearance_mm > 130 ? 'là mức độ vừa phải, phù hợp đường phố Việt Nam' : 'thấp một chút, nhưng đi phố thì không vấn đề gì'}.`
        ];
        answers.push(clearanceDescriptions[Math.floor(Math.random() * clearanceDescriptions.length)]);
      }
    }
    
    if (category === 'Xe điện') {
      // 拟人化电动车信息
      if (vehicle.fuel_type === 'Điện') {
        const estimatedRange = vehicle.power_hp ? Math.floor(vehicle.power_hp * 40) : 60;
        const electricDescriptions = [
          `Về xe điện này thì mình khá hài lòng! Một lần sạc đầy chạy được khoảng ${estimatedRange}km, đủ dùng cho việc đi làm trong tuần rồi.`,
          `Xe điện này chạy được ${estimatedRange}km/lần sạc - mình thấy khá ổn cho việc đi lại hàng ngày trong thành phố.`,
          `${estimatedRange}km một lần sạc nghe có vẻ ít nhưng thực tế mình thấy đủ dùng lắm, nhất là đi làm trong phố.`
        ];
        answers.push(electricDescriptions[Math.floor(Math.random() * electricDescriptions.length)]);
        
        const chargingDescriptions = [
          `Về thời gian sạc thì khoảng 4-6 giờ với sạc thường, 2-3 giờ với sạc nhanh. Mình thường sạc qua đêm nên không thấy bất tiện.`,
          `Sạc đầy mất 4-6 giờ thôi, mình thường cắm sạc tối về là sáng đã đầy pin rồi. Rất tiện!`,
          `Thời gian sạc 4-6 giờ là bình thường, có sạc nhanh 2-3 giờ nữa. Mình thấy khá hợp lý.`
        ];
        answers.push(chargingDescriptions[Math.floor(Math.random() * chargingDescriptions.length)]);
        
        answers.push(`Điểm mạnh nhất là tiết kiệm chi phí vận hành! So với xe xăng thì chỉ tốn 1/10 tiền thôi, rất phù hợp cho việc đi làm hàng ngày.`);
      }
    }
    
    if (category === 'Sử dụng thực tế') {
      // 拟人化实际使用分析
      if (vehicle.engine_cc && vehicle.engine_cc < 125) {
        const smallEngineDescriptions = [
          `Động cơ ${vehicle.engine_cc}cc này mình thấy rất phù hợp đi trong phố đông đúc. Tiết kiệm xăng lắm, di chuyển ngắn hạn thì tuyệt vời!`,
          `${vehicle.engine_cc}cc tuy nhỏ nhưng đi phố thì quá đủ rồi. Mình thích nhất là tiết kiệm nhiên liệu, phù hợp sinh viên lắm.`,
          `Với ${vehicle.engine_cc}cc thì đi trong thành phố là lý tưởng nhất. Không cần quá mạnh, quan trọng là tiết kiệm và linh hoạt.`
        ];
        answers.push(smallEngineDescriptions[Math.floor(Math.random() * smallEngineDescriptions.length)]);
      } else if (vehicle.engine_cc && vehicle.engine_cc >= 150) {
        const bigEngineDescriptions = [
          `Động cơ ${vehicle.engine_cc}cc này mạnh mẽ lắm! Mình đã thử leo dốc và đi đường dài, rất thoải mái không hề mệt.`,
          `${vehicle.engine_cc}cc đủ sức cho mọi địa hình rồi. Leo đèo, vượt dốc đều ổn, đi đường dài cũng không lo thiếu sức.`,
          `Với ${vehicle.engine_cc}cc thì đi đâu cũng được! Mình đã thử chạy từ Hà Nội vào Sài Gòn, xe chạy rất ngon.`
        ];
        answers.push(bigEngineDescriptions[Math.floor(Math.random() * bigEngineDescriptions.length)]);
      }
      
      if (vehicle.abs) {
        const absDescriptions = [
          `Phanh ABS của xe này mình đánh giá cao lắm! Đặc biệt khi đi mưa hay đường ướt, phanh rất an toàn không lo trượt bánh.`,
          `ABS thực sự hữu ích đấy! Mình đã có lần phanh gấp trên đường ướt, may có ABS nên không bị ngã.`,
          `Hệ thống phanh ABS rất cần thiết, nhất là với giao thông Việt Nam phức tạp. An toàn hơn nhiều!`
        ];
        answers.push(absDescriptions[Math.floor(Math.random() * absDescriptions.length)]);
      }
      
      if (vehicle.weight_kg && vehicle.weight_kg < 120) {
        const lightWeightDescriptions = [
          `Xe nhẹ ${vehicle.weight_kg}kg nên rất dễ điều khiển. Mình thấy phụ nữ lái cũng không vấn đề gì, chở người sau cũng thoải mái.`,
          `${vehicle.weight_kg}kg là trọng lượng lý tưởng! Không quá nặng nên dễ đẩy khi cần, lại ổn định khi chạy.`,
          `Trọng lượng ${vehicle.weight_kg}kg rất hợp lý. Mình thấy ai cũng có thể lái được, kể cả người mới học.`
        ];
        answers.push(lightWeightDescriptions[Math.floor(Math.random() * lightWeightDescriptions.length)]);
      }
    }
    
    // 拟人化适用人群描述
    if (vehicle.category.includes('thể thao')) {
      const sportDescriptions = [
        `Xe thể thao này mình thấy rất phù hợp cho các bạn trẻ yêu thích tốc độ và phong cách năng động. Chạy đường phố rất ngầu!`,
        `Nếu bạn thích thể hiện cá tính mạnh mẽ thì xe này là lựa chọn tuyệt vời. Mình thấy giới trẻ rất ưa chuộng.`,
        `Xe thể thao này dành cho những ai đam mê tốc độ và muốn có phong cách riêng. Chạy phố rất bắt mắt!`
      ];
      answers.push(sportDescriptions[Math.floor(Math.random() * sportDescriptions.length)]);
    } else if (vehicle.category.includes('tay ga')) {
      const scooterDescriptions = [
        `Xe tay ga này mình thấy rất tiện cho việc đi làm hàng ngày. Không cần sang số, phụ nữ lái cũng dễ dàng lắm!`,
        `Tay ga là lựa chọn số 1 cho di chuyển trong thành phố đấy! Tiện lợi, thoải mái, ai cũng lái được.`,
        `Mình khuyên xe tay ga này cho những ai cần đi lại thường xuyên trong phố. Rất tiện và không mệt.`
      ];
      answers.push(scooterDescriptions[Math.floor(Math.random() * scooterDescriptions.length)]);
    } else if (vehicle.category.includes('số')) {
      const manualDescriptions = [
        `Xe số này mình thấy rất bền bỉ và tiết kiệm. Phù hợp cho những ai thích sự đơn giản và chi phí vận hành thấp.`,
        `Nếu bạn ưa thích độ tin cậy cao và không ngại sang số thì xe này rất tốt. Bền lâu lắm!`,
        `Xe số truyền thống này mình đánh giá cao về độ bền. Phù hợp cho người thích sự chắc chắn.`
      ];
      answers.push(manualDescriptions[Math.floor(Math.random() * manualDescriptions.length)]);
    } else if (vehicle.category.includes('điện')) {
      const electricDescriptions = [
        `Xe điện là xu hướng tương lai đấy! Mình thấy rất phù hợp cho những ai quan tâm đến môi trường và muốn tiết kiệm chi phí.`,
        `Nếu bạn muốn thân thiện với môi trường và tiết kiệm tiền xăng thì xe điện này là lựa chọn tuyệt vời!`,
        `Xe điện này mình khuyên cho việc di chuyển đô thị. Yên tĩnh, sạch sẽ và rất tiết kiệm.`
      ];
      answers.push(electricDescriptions[Math.floor(Math.random() * electricDescriptions.length)]);
    }
    
    // 新增类别的专门回答
    if (category === 'Tiết kiệm xăng') {
      const fuelConsumption = vehicle.engine_cc ? (vehicle.engine_cc < 125 ? '1.5-2.0L' : vehicle.engine_cc < 155 ? '2.0-2.5L' : '2.5-3.0L') : '2.0L';
      answers.push(`Theo thông số kỹ thuật, ${vehicle.brand} ${vehicle.model} tiêu thụ trung bình khoảng ${fuelConsumption}/100km.`);
      answers.push(`Để tiết kiệm xăng: giữ tốc độ ổn định 40-50km/h trong phố, tránh tăng ga đột ngột, bảo dưỡng định kỳ và giữ áp suất lốp đúng chuẩn.`);
      if (vehicle.fuel_type === 'Xăng') {
        answers.push(`So với các xe cùng phân khúc, đây là mức tiêu hao ${vehicle.engine_cc && vehicle.engine_cc < 125 ? 'rất tiết kiệm' : 'khá tiết kiệm'}.`);
      }
    }
    
    if (category === 'Kỹ năng lái xe') {
      answers.push(`Với ${vehicle.brand} ${vehicle.model}, người mới nên luyện tập ở đường vắng trước. Sang số nhẹ nhàng${vehicle.transmission && vehicle.transmission.includes('sàn') ? ', côn từ từ' : ''}, phanh trước và sau phối hợp.`);
      answers.push(`Lưu ý giữ tốc độ an toàn 30-40km/h khi mới tập, tăng dần khi đã quen xe.`);
      if (vehicle.abs) {
        answers.push(`Xe có ABS nên phanh mạnh cũng được, nhưng vẫn nên phanh từ từ để an toàn hơn.`);
      } else {
        answers.push(`Không có ABS nên phanh phải nhẹ nhàng, tránh phanh gấp làm trượt bánh.`);
      }
    }
    
    if (category === 'Độ xe - Phụ kiện') {
      answers.push(`${vehicle.brand} ${vehicle.model} có thể độ pô (5-10 triệu), thay lốp cao cấp (2-4 triệu), độ đèn LED (1-3 triệu).`);
      answers.push(`Nên ưu tiên độ an toàn như lốp tốt, đèn sáng hơn trước. Độ pô chỉ nên làm nếu thích âm thanh thể thao.`);
      answers.push(`Chi phí độ cơ bản khoảng 5-15 triệu tùy mức độ. Lưu ý giữ tem kiểm định và không vi phạm luật giao thông.`);
    }
    
    if (category === 'Xe cũ - Mua bán') {
      const depreciation = vehicle.price_vnd < 30000000 ? '20-25%' : vehicle.price_vnd < 60000000 ? '15-20%' : '10-15%';
      answers.push(`${vehicle.brand} ${vehicle.model} sau 1 năm sử dụng bình thường mất giá khoảng ${depreciation}, tức còn ${100 - parseInt(depreciation)}% giá trị.`);
      answers.push(`Khi mua xe cũ cần kiểm tra: số km đã đi, tình trạng phanh, lốp, động cơ, giấy tờ gốc.`);
      answers.push(`Xe ${vehicle.brand} thương hiệu uy tín nên ${vehicle.brand === 'Honda' || vehicle.brand === 'Yamaha' ? 'giữ giá rất tốt, dễ bán lại' : 'giữ giá khá ổn'}.`);
    }
    
    if (category === 'Bảo hiểm - Giấy tờ') {
      const insurance = vehicle.price_vnd < 30000000 ? '300,000-500,000' : vehicle.price_vnd < 60000000 ? '500,000-800,000' : '800,000-1,200,000';
      const registration = Math.floor(vehicle.price_vnd * 0.02);
      answers.push(`Bảo hiểm bắt buộc khoảng ${insurance} VNĐ/năm. Phí trước bạ khoảng ${(registration / 1000000).toFixed(1)} triệu (2% giá xe).`);
      answers.push(`Giấy tờ cần: CMND, hộ khẩu, hóa đơn mua xe, tem kiểm định. Quy trình đăng ký mất 1-2 ngày.`);
      answers.push(`Nên mua bảo hiểm vật chất nếu xe trên 50 triệu để được bảo vệ tốt hơn.`);
    }
    
    if (category === 'Đi làm - Giao hàng') {
      answers.push(`${vehicle.brand} ${vehicle.model} ${vehicle.fuel_type === 'Điện' ? 'với chi phí điện rất thấp' : `tiêu hao ${vehicle.engine_cc && vehicle.engine_cc < 125 ? 'ít xăng' : 'xăng vừa phải'}`}, phù hợp chạy xe ôm hoặc giao hàng.`);
      if (vehicle.fuel_type === 'Điện') {
        answers.push(`Xe điện tiết kiệm nhưng cần chú ý quãng đường, nên sạc đầy mỗi đêm. Phù hợp cho việc giao hàng trong bán kính 30-40km.`);
      } else {
        answers.push(`Chạy 100-150km/ngày, mỗi tháng tốn khoảng ${vehicle.engine_cc && vehicle.engine_cc < 125 ? '1-1.5 triệu' : '1.5-2.5 triệu'} tiền xăng.`);
      }
      answers.push(`Nên bảo dưỡng thường xuyên hơn (mỗi 800-1000km) vì chạy nhiều.`);
    }
    
    if (category === 'Phượt - Đi xa') {
      const range = vehicle.fuel_capacity_l ? Math.floor(vehicle.fuel_capacity_l * 40) : 180;
      answers.push(`${vehicle.brand} ${vehicle.model} với bình xăng ${vehicle.fuel_capacity_l || 4}L, quãng đường khoảng ${range}km/bình.`);
      answers.push(`${vehicle.engine_cc && vehicle.engine_cc >= 150 ? 'Động cơ đủ mạnh để đi đường dài, leo đèo Hải Vân thoải mái' : 'Động cơ nhỏ nhưng vẫn đủ sức đi xa, chỉ hơi chậm khi leo dốc'}.`);
      answers.push(`Chuẩn bị: dụng cụ sửa xe cơ bản, áo mưa, bản đồ, sạc điện thoại. Kiểm tra xe kỹ trước khi đi.`);
    }
    
    if (category === 'Mùa mưa - Thời tiết') {
      answers.push(`${vehicle.brand} ${vehicle.model} ${vehicle.abs ? 'có phanh ABS nên an toàn hơn khi đi mưa' : 'không có ABS nên cần phanh nhẹ nhàng khi mưa'}.`);
      answers.push(`Lốp ${vehicle.category.includes('thể thao') ? 'thể thao bám đường tốt' : 'tiêu chuẩn cần kiểm tra hoa lốp'}, nên thay nếu mòn quá 50%.`);
      answers.push(`Mùa mưa nên: giảm tốc độ 20-30%, tăng khoảng cách, tránh vũng nước sâu, bảo dưỡng phanh thường xuyên hơn.`);
    }
    
    if (category === 'Người mới - Học lái') {
      answers.push(`${vehicle.brand} ${vehicle.model} ${vehicle.weight_kg && vehicle.weight_kg < 120 ? 'xe nhẹ, rất phù hợp người mới lái' : vehicle.weight_kg && vehicle.weight_kg < 140 ? 'trọng lượng vừa phải, người mới lái được' : 'hơi nặng, cần tập quen'}.`);
      answers.push(`${vehicle.transmission && vehicle.transmission.includes('Tự động') ? 'Xe tay ga tự động dễ lái hơn, không cần sang số, phù hợp người mới' : 'Xe số cần học sang số nhưng cũng không khó, tập 2-3 ngày là quen'}.`);
      answers.push(`Giá ${this.formatPrice(vehicle.price_vnd)} ${vehicle.price_vnd < 30000000 ? 'rất phải chăng, dễ tiếp cận cho người mới' : 'hơi cao, nhưng đáng đầu tư cho an toàn'}.`);
    }
    
    if (category === 'Chi phí sử dụng') {
      const monthlyCost = vehicle.fuel_type === 'Điện' ? 
        '500,000-800,000 (điện + bảo dưỡng)' : 
        vehicle.engine_cc && vehicle.engine_cc < 125 ? '800,000-1,200,000 (xăng + bảo dưỡng)' : '1,200,000-1,800,000 (xăng + bảo dưỡng)';
      answers.push(`Chi phí sử dụng ${vehicle.brand} ${vehicle.model} trung bình mỗi tháng khoảng ${monthlyCost} VNĐ.`);
      answers.push(`Bao gồm: xăng/điện (60%), bảo dưỡng (20%), bảo hiểm (15%), phụ tùng (5%).`);
      answers.push(`${vehicle.price_vnd < 30000000 ? 'Xe giá rẻ nên chi phí nuôi xe rất thấp, phù hợp sinh viên và người thu nhập thấp' : 'Chi phí hợp lý so với giá trị xe mang lại'}.`);
    }
    
    if (category === 'An toàn - Luật giao thông') {
      answers.push(`${vehicle.brand} ${vehicle.model} ${vehicle.abs ? 'có phanh ABS giúp tăng an toàn đáng kể, đặc biệt khi phanh gấp hoặc đi mưa' : 'không có ABS, cần lái cẩn thận và phanh từ từ'}.`);
      answers.push(`Tốc độ an toàn khuyến nghị: trong phố 40-50km/h, đường dài 60-70km/h${vehicle.engine_cc && vehicle.engine_cc >= 150 ? ', xe này có thể chạy nhanh hơn nhưng nên giữ tốc độ hợp lý' : ''}.`);
      answers.push(`Luôn đội mũ bảo hiểm đạt chuẩn, bật đèn ngay cả ban ngày, tuân thủ luật giao thông để an toàn.`);
    }
    
    // 拟人化总结建议
    const closingStatements = [
      `Hy vọng những chia sẻ của mình hữu ích cho bạn! Nếu còn thắc mắc gì thì cứ hỏi nhé.`,
      `Đó là kinh nghiệm của mình về xe này. Chúc bạn tìm được chiếc xe ưng ý!`,
      `Mình chia sẻ thế này để bạn tham khảo thôi. Cuối cùng vẫn phải tùy vào nhu cầu của bạn.`,
      `Hi vọng thông tin này giúp ích cho bạn. Chúc bạn lái xe an toàn!`,
      `Trên đây là những gì mình biết về xe này. Bạn có thể tham khảo thêm ý kiến khác nhé!`
    ];
    
    if (category === 'Tư vấn mua xe') {
      const buyingAdvice = [
        `Tóm lại, ${vehicle.brand} ${vehicle.model} là lựa chọn đáng cân nhắc trong tầm giá này. Mình khuyên bạn nên đến đại lý thử xe trước khi quyết định nhé!`,
        `Nhìn chung ${vehicle.brand} ${vehicle.model} khá ổn đấy! Bạn nên đi xem xe thực tế và thử lái để cảm nhận cho chính xác.`,
        `Xe này mình thấy phù hợp với nhu cầu của bạn. Đừng quên thương lượng giá khi mua nhé!`
      ];
      answers.push(buyingAdvice[Math.floor(Math.random() * buyingAdvice.length)]);
    } else if (category === 'Bảo dưỡng') {
      const maintenanceAdvice = [
        `Về bảo dưỡng thì mình khuyên nên đi đúng lịch, khoảng 1000-1500km hoặc 3 tháng một lần. Chi phí thường 200-500k tùy hạng mục.`,
        `Bảo dưỡng định kỳ rất quan trọng đấy! Đừng tiết kiệm tiền bảo dưỡng mà sau này tốn tiền sửa chữa.`,
        `Mình thường bảo dưỡng mỗi 1000km, chi phí khoảng 300-400k. Xe chạy êm và bền hơn nhiều!`
      ];
      answers.push(maintenanceAdvice[Math.floor(Math.random() * maintenanceAdvice.length)]);
    } else if (category === 'So sánh xe') {
      const comparisonAdvice = [
        `So với đối thủ thì ${vehicle.brand} ${vehicle.model} có lợi thế về ${vehicle.abs ? 'an toàn (ABS), ' : ''}${vehicle.smart_key ? 'công nghệ (Smart Key), ' : ''}và uy tín thương hiệu.`,
        `Mình thấy xe này cạnh tranh tốt trong phân khúc. Bạn nên so sánh kỹ trước khi chọn.`,
        `Tùy vào sở thích cá nhân, nhưng xe này mình đánh giá khá cao trong tầm giá.`
      ];
      answers.push(comparisonAdvice[Math.floor(Math.random() * comparisonAdvice.length)]);
    } else if (category === 'Người mới - Học lái' || category === 'Kỹ năng lái xe') {
      const newRiderAdvice = [
        `Chúc bạn lái xe an toàn và vui vẻ với chiếc ${vehicle.brand} ${vehicle.model} mới! Nhớ đội mũ bảo hiểm nhé.`,
        `Người mới lái quan trọng nhất là an toàn. Luyện tập nhiều và luôn cẩn thận trên đường!`,
        `Xe này phù hợp cho người mới lắm. Chúc bạn sớm thành thạo và tự tin trên đường!`
      ];
      answers.push(newRiderAdvice[Math.floor(Math.random() * newRiderAdvice.length)]);
    } else if (category === 'Đi làm - Giao hàng') {
      const workAdvice = [
        `Nhiều shipper và tài xế grab đang dùng xe này, phản hồi khá tốt về độ bền và chi phí vận hành.`,
        `Nếu dùng để kiếm tiền thì xe này khá ổn. Bền, tiết kiệm và ít hỏng vặt.`,
        `Mình thấy nhiều bạn chạy xe ôm dùng xe này, đánh giá tích cực lắm!`
      ];
      answers.push(workAdvice[Math.floor(Math.random() * workAdvice.length)]);
    }
    
    // 添加随机的亲切结尾
    answers.push(closingStatements[Math.floor(Math.random() * closingStatements.length)]);
    
    return answers.join(' ');
  }

  /**
   * 格式化价格
   */
  private formatPrice(priceVnd: number): string {
    const millions = priceVnd / 1000000;
    if (millions >= 1000) {
      return `${(millions / 1000).toFixed(1)} tỷ VNĐ`;
    }
    return `${millions.toFixed(1)} triệu VNĐ`;
  }

  /**
   * 自动生成一条Q&A
   */
  async generateOne(): Promise<boolean> {
    try {
      // 随机选择摩托车或汽车
      const vehicleType = Math.random() > 0.5 ? 'motorcycle' : 'car';
      
      if (vehicleType === 'motorcycle') {
        return await this.generateMotorcycleQA();
      } else {
        // 汽车Q&A暂时不实现，因为cars表可能没数据
        console.log('汽车Q&A生成暂未实现');
        return await this.generateMotorcycleQA();
      }
    } catch (error) {
      console.error('生成Q&A失败:', error);
      return false;
    }
  }

  /**
   * 获取最新的Q&A列表
   */
  async getLatest(limit: number = 10) {
    try {
      const questions = await Question.findAll({
        where: { status: 'open' },
        order: [['created_at', 'DESC']],
        limit,
        raw: true
      });

      return questions;
    } catch (error) {
      console.error('获取Q&A列表失败:', error);
      return [];
    }
  }

  /**
   * 获取问题详情及答案
   */
  async getQuestionWithAnswers(questionId: number) {
    try {
      const question = await Question.findByPk(questionId, { raw: true });
      if (!question) return null;

      const answers = await Answer.findAll({
        where: { question_id: questionId },
        order: [['is_accepted', 'DESC'], ['votes_count', 'DESC']],
        raw: true
      });

      return {
        question,
        answers
      };
    } catch (error) {
      console.error('获取问题详情失败:', error);
      return null;
    }
  }

  /**
   * 清理旧数据（保留最近100条）
   */
  async cleanOldData() {
    try {
      const count = await Question.count();
      if (count > 100) {
        const questions = await Question.findAll({
          order: [['created_at', 'ASC']],
          limit: count - 100
        });

        for (const q of questions) {
          await q.destroy();
        }

        console.log(`清理了 ${count - 100} 条旧Q&A`);
      }
    } catch (error) {
      console.error('清理旧数据失败:', error);
    }
  }
}

export default new QAGeneratorService();

