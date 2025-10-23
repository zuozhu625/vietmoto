import { Request, Response } from 'express';
import NewsService from '../services/NewsService';

export class NewsController {
  // 创建新闻（n8n webhook）
  static async create(req: Request, res: Response): Promise<void> {
    try {
      const { title, content, summary, category, author_name, featured_image, status } = req.body;

      // 验证必填字段
      if (!title || !content) {
        res.status(400).json({
          success: false,
          message: 'Title and content are required',
        });
        return;
      }

      const news = await NewsService.createNews({
        title,
        content,
        summary,
        category,
        author_name,
        featured_image,
        status,
      });

      res.status(201).json({
        success: true,
        message: 'News created successfully',
        data: news,
      });
    } catch (error: any) {
      console.error('创建新闻失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to create news',
        error: error.message,
      });
    }
  }

  // 获取新闻列表
  static async getList(req: Request, res: Response): Promise<void> {
    try {
      const {
        page = 1,
        limit = 10,
        category,
        status,
        is_featured,
        search,
      } = req.query;

      const result = await NewsService.getNewsList({
        page: Number(page),
        limit: Number(limit),
        category: category as string,
        status: status as string,
        is_featured: is_featured === 'true',
        search: search as string,
      });

      res.json({
        success: true,
        ...result,
      });
    } catch (error: any) {
      console.error('获取新闻列表失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch news list',
        error: error.message,
      });
    }
  }

  // 获取新闻详情（通过slug）
  static async getBySlug(req: Request, res: Response): Promise<void> {
    try {
      const { slug } = req.params;
      const news = await NewsService.getNewsBySlug(slug);

      if (!news) {
        res.status(404).json({
          success: false,
          message: 'News not found',
        });
        return;
      }

      res.json({
        success: true,
        data: news,
      });
    } catch (error: any) {
      console.error('获取新闻详情失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch news details',
        error: error.message,
      });
    }
  }

  // 获取新闻详情（通过ID）
  static async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const news = await NewsService.getNewsById(Number(id));

      if (!news) {
        res.status(404).json({
          success: false,
          message: 'News not found',
        });
        return;
      }

      res.json({
        success: true,
        data: news,
      });
    } catch (error: any) {
      console.error('获取新闻详情失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch news details',
        error: error.message,
      });
    }
  }

  // 更新新闻
  static async update(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const news = await NewsService.updateNews(Number(id), req.body);

      if (!news) {
        res.status(404).json({
          success: false,
          message: 'News not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'News updated successfully',
        data: news,
      });
    } catch (error: any) {
      console.error('更新新闻失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to update news',
        error: error.message,
      });
    }
  }

  // 删除新闻
  static async delete(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const result = await NewsService.deleteNews(Number(id));

      if (!result) {
        res.status(404).json({
          success: false,
          message: 'News not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'News deleted successfully',
      });
    } catch (error: any) {
      console.error('删除新闻失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to delete news',
        error: error.message,
      });
    }
  }

  // 获取最新新闻
  static async getLatest(req: Request, res: Response): Promise<void> {
    try {
      const { limit = 6 } = req.query;
      const news = await NewsService.getLatestNews(Number(limit));

      res.json({
        success: true,
        data: news,
      });
    } catch (error: any) {
      console.error('获取最新新闻失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch latest news',
        error: error.message,
      });
    }
  }

  // 获取相关新闻
  static async getRelated(req: Request, res: Response): Promise<void> {
    try {
      const { slug } = req.params;
      const { category, limit = 6 } = req.query;

      const news = await NewsService.getRelatedNews(
        slug,
        category as string,
        Number(limit)
      );

      res.json({
        success: true,
        data: news,
      });
    } catch (error: any) {
      console.error('获取相关新闻失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch related news',
        error: error.message,
      });
    }
  }

  // 获取所有分类
  static async getCategories(req: Request, res: Response): Promise<void> {
    try {
      const categories = await NewsService.getCategories();

      res.json({
        success: true,
        data: categories,
      });
    } catch (error: any) {
      console.error('获取分类失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch categories',
        error: error.message,
      });
    }
  }
}

export default NewsController;
