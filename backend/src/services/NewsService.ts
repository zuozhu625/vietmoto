import News, { NewsAttributes } from '../models/News';
import { Op } from 'sequelize';

// 生成slug的辅助函数
function generateSlug(title: string, id?: number): string {
  const baseSlug = title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // 去除越南语声调
    .replace(/đ/g, 'd')
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
  
  return id ? `${baseSlug}-${id}` : baseSlug;
}

export class NewsService {
  // 创建新闻（n8n webhook调用）
  static async createNews(data: {
    title: string;
    content: string;
    summary?: string;
    category?: string;
    author_name?: string;
    featured_image?: string;
    status?: string;
  }) {
    try {
      // 创建新闻记录
      const news = await News.create({
        title: data.title,
        slug: generateSlug(data.title), // 临时slug
        content: data.content,
        summary: data.summary,
        excerpt: data.summary?.substring(0, 200),
        category: data.category || 'Tin tức',
        author_name: data.author_name || 'Ban biên tập',
        featured_image: data.featured_image,
        status: data.status || 'published',
        published_at: data.status === 'published' ? new Date() : undefined,
      });

      // 更新slug包含ID
      const finalSlug = generateSlug(data.title, news.id);
      await news.update({ slug: finalSlug });

      return news;
    } catch (error) {
      console.error('创建新闻失败:', error);
      throw error;
    }
  }

  // 获取新闻列表（支持分页、筛选、排序）
  static async getNewsList(params: {
    page?: number;
    limit?: number;
    category?: string;
    status?: string;
    is_featured?: boolean;
    search?: string;
  }) {
    const page = params.page || 1;
    const limit = params.limit || 10;
    const offset = (page - 1) * limit;

    const where: any = {};

    if (params.category) {
      where.category = params.category;
    }

    if (params.status) {
      where.status = params.status;
    } else {
      where.status = 'published'; // 默认只返回已发布的
    }

    if (params.is_featured !== undefined) {
      where.is_featured = params.is_featured;
    }

    if (params.search) {
      where[Op.or] = [
        { title: { [Op.like]: `%${params.search}%` } },
        { content: { [Op.like]: `%${params.search}%` } },
      ];
    }

    const { count, rows } = await News.findAndCountAll({
      where,
      limit,
      offset,
      order: [['published_at', 'DESC'], ['created_at', 'DESC']],
    });

    return {
      data: rows,
      pagination: {
        total: count,
        totalPages: Math.ceil(count / limit),
        page,
        limit,
      },
    };
  }

  // 根据slug获取新闻详情
  static async getNewsBySlug(slug: string) {
    const news = await News.findOne({
      where: { slug },
    });

    if (!news) {
      return null;
    }

    // 增加浏览次数
    await news.increment('view_count');

    return news;
  }

  // 根据ID获取新闻详情
  static async getNewsById(id: number) {
    const news = await News.findByPk(id);

    if (!news) {
      return null;
    }

    // 增加浏览次数
    await news.increment('view_count');

    return news;
  }

  // 更新新闻
  static async updateNews(id: number, data: Partial<NewsAttributes>) {
    const news = await News.findByPk(id);

    if (!news) {
      return null;
    }

    // 如果更新了标题，也更新slug
    if (data.title && data.title !== news.title) {
      data.slug = generateSlug(data.title, id);
    }

    await news.update(data);
    return news;
  }

  // 删除新闻
  static async deleteNews(id: number) {
    const news = await News.findByPk(id);

    if (!news) {
      return null;
    }

    await news.destroy();
    return true;
  }

  // 获取最新的N条新闻
  static async getLatestNews(limit: number = 6) {
    const news = await News.findAll({
      where: { status: 'published' },
      limit,
      order: [['published_at', 'DESC'], ['created_at', 'DESC']],
    });

    return news;
  }

  // 获取相关新闻
  static async getRelatedNews(currentSlug: string, category?: string, limit: number = 6) {
    const where: any = {
      slug: { [Op.ne]: currentSlug },
      status: 'published',
    };

    if (category) {
      where.category = category;
    }

    const news = await News.findAll({
      where,
      limit,
      order: [['published_at', 'DESC'], ['created_at', 'DESC']],
    });

    return news;
  }

  // 获取所有分类
  static async getCategories() {
    const categories = await News.findAll({
      attributes: ['category'],
      where: { status: 'published' },
      group: ['category'],
    });

    return categories.map(c => c.category).filter(Boolean);
  }
}

export default NewsService;

