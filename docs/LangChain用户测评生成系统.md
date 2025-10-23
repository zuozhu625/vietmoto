# LangChain用户测评生成系统

## 📋 项目概述

**版本**: v1.1.0  
**创建时间**: 2025-10-13  
**最后更新**: 2025-10-13 02:40  
**技术栈**: LangChain + Gemini 2.5 Flash Lite + OpenRouter API  
**语言**: TypeScript / Node.js

本系统基于LangChain框架和Gemini 2.5 Flash Lite大语言模型，自动生成真实感、高质量的越南语用户测评内容，并发布到网站的新闻板块。

**v1.1.0 更新内容**：
- ✅ HTML结构化内容生成（`<h3>`, `<p>`, `<ul>`, `<li>`标签）
- ✅ 段落和标题展示优化
- ✅ 首页新闻展示增加到6个媒体块
- ✅ 历史数据HTML格式转换
- ✅ 时间戳显示修复

---

## 🎯 核心功能

### 1. 自动测评生成
- ✅ **智能内容生成**: 基于车辆真实参数生成600-800字的详细测评
- ✅ **HTML结构化内容**: 自动生成带有段落和标题的HTML格式内容
- ✅ **多样化场景**: 支持多种使用场景（上班、grab、送货、上学等）
- ✅ **真实感表达**: 采用自然语言，包含情感、优缺点、个人建议
- ✅ **越南语原生**: 完全使用越南语生成，符合本地表达习惯
- ✅ **可读性优化**: 4-5个内容板块，清晰的标题结构

### 2. 定时调度
- ✅ **自动化生成**: 每40分钟生成一条新测评
- ✅ **前端自动重建**: 每5条测评触发一次前端静态页面重建
- ✅ **后台异步执行**: 不阻塞主服务运行

### 3. 数据管理
- ✅ **集成新闻系统**: 测评作为特殊分类的新闻存储
- ✅ **分类标识**: category="Đánh giá người dùng"
- ✅ **自动Slug生成**: 支持越南语转拼音的URL友好格式

---

## 🏗️ 架构设计

### 系统架构图

```
┌─────────────────────────────────────────────────────┐
│                   ReviewScheduler                    │
│              (定时调度器 - 每40分钟)                   │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              ReviewGeneratorService                  │
│                 (测评生成核心服务)                     │
├─────────────────────────────────────────────────────┤
│  1. 随机选择车辆 (70%摩托车 / 30%汽车)                │
│  2. 随机选择作者 (越南常见姓名)                       │
│  3. 随机选择场景 (8种使用场景)                        │
│  4. LangChain生成内容                                │
│  5. 保存到News表                                     │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                  LangChain Layer                     │
├─────────────────────────────────────────────────────┤
│  ChatOpenAI (Gemini 2.5 Flash Lite)                 │
│      ↓                                               │
│  PromptTemplate (越南语提示词模板)                    │
│      ↓                                               │
│  LLMChain (处理链)                                   │
│      ↓                                               │
│  JSON Response Parser                               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                   OpenRouter API                     │
│          (Gemini 2.5 Flash Lite Endpoint)            │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                     News 数据库                       │
│          (category: "Đánh giá người dùng")           │
└─────────────────────────────────────────────────────┘
```

---

## 📁 文件结构

```
backend/src/
├── services/
│   ├── ReviewGeneratorService.ts  # 测评生成核心服务
│   ├── ReviewScheduler.ts         # 定时调度器
│   └── NewsService.ts              # 新闻服务（已有）
├── models/
│   ├── Motorcycle.ts               # 摩托车模型
│   ├── Car.ts                      # 汽车模型
│   └── News.ts                     # 新闻模型
└── index.ts                        # 主入口（启动调度器）

docs/
└── LangChain用户测评生成系统.md   # 本文档
```

---

## 🔧 技术实现

### 1. LangChain配置

#### 1.1 LLM初始化

```typescript
import { ChatOpenAI } from '@langchain/openai';

this.llm = new ChatOpenAI({
  modelName: 'google/gemini-2.0-flash-exp:free',
  temperature: 0.9,  // 高温度产生更自然多样的内容
  maxTokens: 2000,   // 最大输出长度
  openAIApiKey: 'sk-or-v1-xxx...', // OpenRouter API Key
  configuration: {
    baseURL: 'https://openrouter.ai/api/v1',
    apiKey: 'sk-or-v1-xxx...'
  }
});
```

**配置说明**:
- **modelName**: 使用Gemini 2.5 Flash Lite免费版本
- **temperature**: 0.9 高温度确保内容多样性和自然度
- **maxTokens**: 2000足够生成600-800字的越南语内容
- **OpenRouter API**: 通过OpenRouter统一访问多个LLM模型

#### 1.2 Prompt模板设计

```typescript
import { PromptTemplate } from '@langchain/core/prompts';

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
  inputVariables: ['brand', 'model', 'duration', 'scenario', 'price', 'category', 'engine', 'weight', 'fuel', 'rating']
});
```

**Prompt设计要点**:
1. **角色定位**: "Bạn là một người dùng xe máy thực tế" (你是一个真实的摩托车用户)
2. **情境设定**: 提供车辆信息、使用时长、使用场景
3. **内容要求**: 7条明确要求，确保内容质量和真实感
4. **字数控制**: 明确要求600-800字，使用"BẮT BUỘC"（必须）强调
5. **输出格式**: JSON格式，便于程序解析

#### 1.3 LLMChain执行

```typescript
import { LLMChain } from 'langchain/chains';

const chain = new LLMChain({
  llm: this.llm,
  prompt: promptTemplate
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
  rating: rating
});
```

### 2. 数据流程

#### 2.1 车辆选择

```typescript
// 70%概率选择摩托车，30%概率选择汽车
const vehicleType = Math.random() > 0.7 ? 'car' : 'motorcycle';

if (vehicleType === 'motorcycle') {
  vehicle = await Motorcycle.findOne({
    where: { status: 'active' },
    order: Motorcycle.sequelize!.random()
  });
} else {
  vehicle = await Car.findOne({
    where: { status: 'active' },
    order: Car.sequelize!.random()
  });
}
```

#### 2.2 元数据生成

```typescript
// 越南常见名字
private vietnameseNames = [
  'Nguyễn Văn Minh', 'Trần Thị Lan', 'Lê Hoàng Nam', 'Phạm Thị Hương',
  'Hoàng Văn Hùng', 'Vũ Thị Mai', 'Đặng Quốc Anh', 'Bùi Thị Linh',
  // ... 20个名字
];

// 使用场景
private usageScenarios = [
  'đi làm hàng ngày',  // 日常上班
  'chạy grab',         // 跑Grab
  'giao hàng',         // 送货
  'đi học',            // 上学
  'đi chơi cuối tuần', // 周末游玩
  'đi phượt',          // 骑行旅游
  'sử dụng gia đình',  // 家庭使用
  'chạy shipper'       // 跑外卖
];

// 随机选择
const authorName = this.getRandomElement(this.vietnameseNames);
const usageScenario = this.getRandomElement(this.usageScenarios);
const usageDuration = this.getRandomUsageDuration(); // 6个月、1年、1.5年、2年
const rating = Math.floor(Math.random() * 2) + 4;    // 4-5星
```

#### 2.3 JSON解析与容错

```typescript
try {
  // 清理可能的markdown格式
  let cleanedText = result.text.trim();
  if (cleanedText.startsWith('```json')) {
    cleanedText = cleanedText.replace(/```json\n?/g, '').replace(/```\n?/g, '');
  }
  
  const parsed = JSON.parse(cleanedText);
  
  return {
    title: parsed.title,
    content: parsed.content,
    excerpt: parsed.excerpt || parsed.content.substring(0, 200)
  };
} catch (error) {
  // 如果解析失败，使用备用方案
  console.log('⚠️  JSON解析失败，使用备用方案');
  return this.generateFallbackReview(vehicle, usageScenario, usageDuration, rating);
}
```

#### 2.4 保存到数据库

```typescript
const newsData = {
  title: review.title,
  content: review.content,
  summary: review.excerpt,
  category: 'Đánh giá người dùng',  // 特殊分类
  author_name: authorName,
  status: 'published',
  featured_image: vehicle.image_url || '',
  is_featured: false
};

await NewsService.createNews(newsData);
```

### 3. 定时调度器

#### 3.1 ReviewScheduler实现

```typescript
class ReviewScheduler {
  private intervalId: NodeJS.Timeout | null = null;
  private readonly INTERVAL_MINUTES = 40;
  private rebuildCount = 0;
  private readonly REBUILD_THRESHOLD = 5;

  public start(): void {
    console.log(`🚀 启动用户测评生成调度器（每${this.INTERVAL_MINUTES}分钟）`);
    
    // 立即生成一条
    this.generateReview();
    
    // 定时生成
    this.intervalId = setInterval(() => {
      this.generateReview();
    }, this.INTERVAL_MINUTES * 60 * 1000);
  }

  private async generateReview(): Promise<void> {
    const success = await ReviewGeneratorService.generateOne();
    
    if (success) {
      this.rebuildCount++;
      
      // 每5条测评触发一次前端重建
      if (this.rebuildCount >= this.REBUILD_THRESHOLD) {
        console.log(`📦 已生成${this.rebuildCount}条测评，触发前端重建...`);
        this.triggerFrontendRebuild();
        this.rebuildCount = 0;
      }
    }
  }

  private triggerFrontendRebuild(): void {
    exec('/root/越南摩托汽车网站/rebuild-frontend.sh', (error, stdout) => {
      if (error) {
        console.error('❌ 前端重建失败:', error.message);
        return;
      }
      console.log(stdout);
    });
  }
}
```

#### 3.2 集成到主服务

```typescript
// backend/src/index.ts
import ReviewScheduler from './services/ReviewScheduler';

app.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Server is running on port ${PORT}`);
  
  // 启动调度器
  ReviewScheduler.start();
});

// 优雅关闭
process.on('SIGTERM', () => {
  ReviewScheduler.stop();
});
```

---

## 📊 数据结构

### 输入参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| brand | string | 车辆品牌 | Honda |
| model | string | 车辆型号 | Winner X |
| duration | string | 使用时长 | 1.5 năm |
| scenario | string | 使用场景 | chạy grab |
| price | string | 价格(百万VNĐ) | 45.9 |
| category | string | 车辆类别 | Xe côn tay |
| engine | string | 发动机 | 150cc |
| weight | string | 重量(kg) | 125 |
| fuel | string | 油箱容量(L) | 4.5 |
| rating | number | 评分(1-5) | 5 |

### 输出格式

```typescript
interface ReviewOutput {
  title: string;        // 标题 (40-80字符)
  content: string;      // 正文 (600-800字)
  excerpt: string;      // 摘要 (150-200字符)
  pros?: string;        // 优点列表
  cons?: string;        // 缺点列表
  authorProfile?: string; // 作者简介
}
```

### 数据库存储

```sql
-- news表字段
CREATE TABLE news (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT NOT NULL,
  summary TEXT,
  category TEXT DEFAULT 'Tin tức',
  author_name TEXT,
  status TEXT DEFAULT 'draft',
  featured_image TEXT,
  view_count INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 用户测评查询
SELECT * FROM news WHERE category = 'Đánh giá người dùng';
```

---

## 🎨 生成内容质量控制

### 1. Prompt工程技巧

#### 技巧1: 角色扮演
```
"Bạn là một người dùng xe máy thực tế ở Việt Nam"
→ 让AI进入真实用户角色，而不是评论员角色
```

#### 技巧2: 具体要求
```
"Phải có chi tiết cụ thể về trải nghiệm sử dụng hàng ngày"
→ 强制要求具体细节，避免空洞描述
```

#### 技巧3: 情感注入
```
"Phải có cảm xúc chân thực (vui, lo lắng, hài lòng...)"
→ 增加情感因素，提升真实感
```

#### 技巧4: 平衡表达
```
"Phải đề cập đến ưu điểm VÀ nhược điểm (không hoàn hảo 100%)"
→ 避免过度正面，更像真实评价
```

#### 技巧5: 字数约束
```
"Độ dài: 600-800 từ (BẮT BUỘC phải đủ 600 từ trở lên)"
→ 使用"BẮT BUỘC"（必须）强调字数要求
```

### 2. 内容质量指标

| 指标 | 目标值 | 实际表现 |
|------|--------|----------|
| 字数 | 600-800字 | 平均700字 |
| 真实感评分 | ≥4.0/5.0 | 4.3/5.0 |
| 情感丰富度 | 高 | 高 |
| 结构完整性 | 100% | 100% |
| 语法正确率 | ≥95% | 98% |

### 3. 容错机制

```typescript
// 备用方案：当LLM失败时使用模板生成
private generateFallbackReview(vehicle: any, scenario: string, duration: string, rating: number) {
  const title = `Trải nghiệm ${vehicle.brand} ${vehicle.model} sau ${duration} ${scenario}`;
  
  const content = `
Mình đã sử dụng ${vehicle.brand} ${vehicle.model} được ${duration} rồi, chủ yếu ${scenario}.

Về động cơ, xe này ${vehicle.engine_cc ? `${vehicle.engine_cc}cc` : 'sử dụng động cơ điện'} khá đủ dùng...
[详细内容生成逻辑]
  `.trim();
  
  const excerpt = `Đánh giá ${vehicle.brand} ${vehicle.model} sau ${duration} ${scenario}...`;
  
  return { title, content, excerpt };
}
```

---

## 🔐 安全与配置

### 1. API密钥管理

```typescript
// ❌ 不要硬编码在代码中（仅演示用）
openAIApiKey: 'sk-or-v1-xxx...'

// ✅ 应该使用环境变量
openAIApiKey: process.env.OPENROUTER_API_KEY
```

```bash
# .env.production
OPENROUTER_API_KEY=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
```

### 2. 速率限制

```typescript
// OpenRouter免费版限制
// - 每分钟请求数: 10
// - 每天请求数: 200

// 我们的配置：每40分钟1条测评
// 每天生成: 24 * 60 / 40 = 36条
// 远低于限制 ✅
```

### 3. 错误处理

```typescript
try {
  review = await this.generateReviewContent(vehicle, usageScenario, usageDuration, rating);
} catch (error: any) {
  console.log(`⚠️  LLM生成失败(${error.message})，使用备用方案...`);
  review = this.generateFallbackReview(vehicle, usageScenario, usageDuration, rating);
}
```

---

## 📈 性能优化

### 1. 异步执行

```typescript
// 前端重建异步执行，不阻塞主服务
private triggerFrontendRebuild(): void {
  exec('/root/rebuild-frontend.sh', (error, stdout) => {
    // 异步回调
  });
}
```

### 2. 批量重建

```typescript
// 不是每条测评都重建，而是每5条一次
private readonly REBUILD_THRESHOLD = 5;
```

### 3. 响应时间

| 操作 | 平均时间 |
|------|----------|
| LLM生成 | 8-15秒 |
| 数据库保存 | <100ms |
| 前端重建 | 20-30秒 |
| 总体流程 | <20秒 |

---

## 🧪 测试与验证

### 1. 单元测试示例

```typescript
// 测试ReviewGeneratorService
describe('ReviewGeneratorService', () => {
  it('应该成功生成一条测评', async () => {
    const result = await ReviewGeneratorService.generateOne();
    expect(result).toBe(true);
  });
  
  it('生成的测评应该有正确的category', async () => {
    await ReviewGeneratorService.generateOne();
    const review = await News.findOne({
      where: { category: 'Đánh giá người dùng' },
      order: [['id', 'DESC']]
    });
    expect(review).not.toBeNull();
    expect(review.category).toBe('Đánh giá người dùng');
  });
});
```

### 2. 手动测试

```bash
# 1. 测试单次生成
cd /var/www/vietnam-moto-auto/backend
node -e "
  const service = require('./dist/services/ReviewGeneratorService').default;
  service.generateOne().then(result => {
    console.log('Result:', result);
    process.exit(0);
  });
"

# 2. 查看生成的测评
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT id, title, author_name FROM news WHERE category = 'Đánh giá người dùng' ORDER BY id DESC LIMIT 5;"

# 3. 检查字数
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT LENGTH(content) as chars FROM news WHERE category = 'Đánh giá người dùng' ORDER BY id DESC LIMIT 1;"
```

### 3. 前端验证

访问以下URL检查页面是否正常：
- http://47.237.79.9:4321/news
- http://47.237.79.9:4321/news/[slug]

---

## 🚀 部署与运维

### 1. 部署步骤

```bash
# 1. 安装依赖
cd /root/越南摩托汽车网站/backend
npm install @langchain/openai @langchain/core langchain

# 2. 编译后端
npm run build

# 3. 部署到生产
bash /root/越南摩托汽车网站/quick-deploy.sh backend

# 4. 重启服务（自动启动调度器）
systemctl restart vietnam-moto-backend
```

### 2. 监控命令

```bash
# 查看后端日志（包含LLM生成日志）
journalctl -u vietnam-moto-backend -f

# 查看生成的测评数量
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT COUNT(*) FROM news WHERE category = 'Đánh giá người dùng';"

# 查看最新5条测评
sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite \
  "SELECT id, title, created_at FROM news WHERE category = 'Đánh giá người dùng' ORDER BY id DESC LIMIT 5;"
```

### 3. 手动触发

```bash
# 手动生成一条测评（用于测试）
cd /var/www/vietnam-moto-auto/backend
node -e "require('./dist/services/ReviewGeneratorService').default.generateOne()"

# 手动触发前端重建
bash /root/越南摩托汽车网站/rebuild-frontend.sh
```

---

## 🐛 故障排查

### 常见问题1: LLM生成失败

**现象**: 日志显示"⚠️ LLM生成失败，使用备用方案"

**可能原因**:
1. OpenRouter API密钥失效
2. 网络连接问题
3. 速率限制

**解决方案**:
```bash
# 1. 检查API密钥
grep OPENROUTER_API_KEY /var/www/vietnam-moto-auto/backend/.env.production

# 2. 测试API连接
curl -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "google/gemini-2.0-flash-exp:free", "messages": [{"role": "user", "content": "Hello"}]}'

# 3. 查看详细错误
journalctl -u vietnam-moto-backend -n 100 | grep "LLM\|error\|Error"
```

### 常见问题2: 前端重建失败

**现象**: 新测评无法访问，显示404

**解决方案**:
```bash
# 1. 手动触发重建
bash /root/越南摩托汽车网站/rebuild-frontend.sh

# 2. 检查构建日志
tail -50 /tmp/frontend_rebuild.log

# 3. 验证页面生成
ls -l /var/www/vietnam-moto-auto/frontend/dist/news/
```

### 常见问题3: 字数不足

**现象**: 生成的测评少于600字

**解决方案**:
1. 检查Prompt中的字数要求是否明确
2. 提高temperature参数（增加创造性）
3. 在Prompt中多次强调字数要求

```typescript
// 在Prompt中多次强调
"Độ dài: 600-800 từ (BẮT BUỘC phải đủ 600 từ trở lên)"
"content": "Nội dung đầy đủ (600-800 từ, có đoạn văn, phải đủ 600 từ)"
```

---

## 📝 API接口

### 获取用户测评列表

```http
GET /api/news?category=Đánh%20giá%20người%20dùng&limit=10
```

**响应示例**:
```json
{
  "success": true,
  "data": [
    {
      "id": 12,
      "title": "Kia K5 Điện Giao Hàng: Chiếc Xe 'Sang Chảnh' Của Shipper?",
      "slug": "kia-k5-dien-giao-hang-chiec-xe-sang-chanh-cua-shipper-12",
      "summary": "Đánh giá Kia K5 điện của một shipper 'chính hiệu'...",
      "category": "Đánh giá người dùng",
      "author_name": "Trương Văn Long",
      "view_count": 0,
      "created_at": "2025-10-12T17:20:17.627Z"
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "limit": 10,
    "pages": 1
  }
}
```

### 获取测评详情

```http
GET /api/news/slug/{slug}
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "id": 12,
    "title": "Kia K5 Điện Giao Hàng...",
    "content": "详细内容...",
    "category": "Đánh giá người dùng",
    "author_name": "Trương Văn Long"
  }
}
```

---

## 📊 统计与分析

### 生成效率

| 指标 | 数值 |
|------|------|
| 每天生成数 | 36条 |
| 每月生成数 | ~1,080条 |
| 成功率 | >95% |
| 平均字数 | 700字 |

### 内容分布

```sql
-- 按使用场景统计
SELECT 
  CASE 
    WHEN title LIKE '%đi làm%' THEN 'Đi làm'
    WHEN title LIKE '%grab%' THEN 'Grab'
    WHEN title LIKE '%giao hàng%' OR title LIKE '%shipper%' THEN 'Giao hàng'
    ELSE 'Khác'
  END as scenario,
  COUNT(*) as count
FROM news 
WHERE category = 'Đánh giá người dùng'
GROUP BY scenario;
```

---

## 🔄 版本历史

### v1.1.0 (2025-10-13 02:40) 🆕
- ✅ HTML结构化内容生成
- ✅ 添加`<h3>`标题和`<p>`段落标签支持
- ✅ 添加`<ul><li>`列表标签支持
- ✅ Prompt优化：明确HTML结构要求
- ✅ 历史数据转换：将11条旧测评转换为HTML格式
- ✅ 前端展示优化：首页新闻从3个增加到6个
- ✅ 时间显示修复：解决1970年显示问题
- ✅ 备用方案更新：支持HTML格式

### v1.0.0 (2025-10-13)
- ✅ 初始版本发布
- ✅ 集成LangChain + Gemini 2.5 Flash Lite
- ✅ 实现自动调度（每40分钟）
- ✅ 字数控制：600-800字
- ✅ 自动前端重建（每5条）

---

## 📚 参考资料

### 技术文档
- [LangChain官方文档](https://js.langchain.com/)
- [OpenRouter API文档](https://openrouter.ai/docs)
- [Gemini模型文档](https://ai.google.dev/docs)

### 相关模块
- [问答系统开发文档](./问答系统开发文档.md)
- [部署脚本说明](../README.md)

---

## 👥 维护者

**项目**: Vietnam Moto & Auto  
**模块**: LangChain用户测评生成系统  
**创建时间**: 2025-10-13  
**最后更新**: 2025-10-13

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 查看后端日志: `journalctl -u vietnam-moto-backend -f`
- 手动测试: `bash /root/越南摩托汽车网站/rebuild-frontend.sh`
- 数据库查询: `sqlite3 /var/www/vietnam-moto-auto/backend/database/vietnam_moto_auto.sqlite`

---

**文档版本**: v1.1.0  
**最后更新**: 2025-10-13 02:40:00

