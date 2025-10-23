import { Request, Response } from 'express';
import MotorcycleService from '../services/MotorcycleService';

export class MotorcycleController {
  // 创建摩托车（n8n webhook）
  static async create(req: Request, res: Response): Promise<void> {
    try {
      const motorcycle = await MotorcycleService.createMotorcycle(req.body);

      res.status(201).json({
        success: true,
        message: 'Motorcycle created successfully',
        data: motorcycle,
      });
    } catch (error: any) {
      console.error('创建摩托车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to create motorcycle',
        error: error.message,
      });
    }
  }

  // 获取摩托车列表
  static async getList(req: Request, res: Response): Promise<void> {
    try {
      const {
        page = 1,
        limit = 12,
        brand,
        category,
        fuel_type,
        min_price,
        max_price,
        status,
        search,
        sort,
        order,
      } = req.query;

      const result = await MotorcycleService.getMotorcyclesList({
        page: Number(page),
        limit: Number(limit),
        brand: brand as string,
        category: category as string,
        fuel_type: fuel_type as string,
        min_price: min_price ? Number(min_price) : undefined,
        max_price: max_price ? Number(max_price) : undefined,
        status: status as string,
        search: search as string,
        sort: sort as string,
        order: order as string,
      });

      res.json({
        success: true,
        ...result,
      });
    } catch (error: any) {
      console.error('获取摩托车列表失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch motorcycles list',
        error: error.message,
      });
    }
  }

  // 获取摩托车详情
  static async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const motorcycle = await MotorcycleService.getMotorcycleById(Number(id));

      if (!motorcycle) {
        res.status(404).json({
          success: false,
          message: 'Motorcycle not found',
        });
        return;
      }

      res.json({
        success: true,
        data: motorcycle,
      });
    } catch (error: any) {
      console.error('获取摩托车详情失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch motorcycle details',
        error: error.message,
      });
    }
  }

  // 更新摩托车
  static async update(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const motorcycle = await MotorcycleService.updateMotorcycle(Number(id), req.body);

      if (!motorcycle) {
        res.status(404).json({
          success: false,
          message: 'Motorcycle not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Motorcycle updated successfully',
        data: motorcycle,
      });
    } catch (error: any) {
      console.error('更新摩托车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to update motorcycle',
        error: error.message,
      });
    }
  }

  // 删除摩托车
  static async delete(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const result = await MotorcycleService.deleteMotorcycle(Number(id));

      if (!result) {
        res.status(404).json({
          success: false,
          message: 'Motorcycle not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Motorcycle deleted successfully',
      });
    } catch (error: any) {
      console.error('删除摩托车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to delete motorcycle',
        error: error.message,
      });
    }
  }

  // 获取所有品牌
  static async getBrands(req: Request, res: Response): Promise<void> {
    try {
      const brands = await MotorcycleService.getBrands();

      res.json({
        success: true,
        data: brands,
      });
    } catch (error: any) {
      console.error('获取品牌列表失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch brands',
        error: error.message,
      });
    }
  }

  // 获取所有分类
  static async getCategories(req: Request, res: Response): Promise<void> {
    try {
      const categories = await MotorcycleService.getCategories();

      res.json({
        success: true,
        data: categories,
      });
    } catch (error: any) {
      console.error('获取分类列表失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch categories',
        error: error.message,
      });
    }
  }

  // 获取推荐摩托车
  static async getFeatured(req: Request, res: Response): Promise<void> {
    try {
      const { limit = 6 } = req.query;
      const motorcycles = await MotorcycleService.getFeaturedMotorcycles(Number(limit));

      res.json({
        success: true,
        data: motorcycles,
      });
    } catch (error: any) {
      console.error('获取推荐摩托车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch featured motorcycles',
        error: error.message,
      });
    }
  }
}

export default MotorcycleController;

