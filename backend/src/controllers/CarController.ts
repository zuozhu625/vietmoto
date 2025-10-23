import { Request, Response } from 'express';
import CarService from '../services/CarService';

export class CarController {
  // 创建汽车
  static async create(req: Request, res: Response): Promise<void> {
    try {
      const car = await CarService.createCar(req.body);

      res.status(201).json({
        success: true,
        message: 'Car created successfully',
        data: car,
      });
    } catch (error: any) {
      console.error('创建汽车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to create car',
        error: error.message,
      });
    }
  }

  // 获取汽车列表
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

      const result = await CarService.getCarsList({
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
      console.error('获取汽车列表失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch cars list',
        error: error.message,
      });
    }
  }

  // 获取汽车详情（通过ID）
  static async getById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const car = await CarService.getCarById(Number(id));

      if (!car) {
        res.status(404).json({
          success: false,
          message: 'Car not found',
        });
        return;
      }

      res.json({
        success: true,
        data: car,
      });
    } catch (error: any) {
      console.error('获取汽车详情失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch car details',
        error: error.message,
      });
    }
  }

  // 获取汽车详情（通过slug）
  static async getBySlug(req: Request, res: Response): Promise<void> {
    try {
      const { slug } = req.params;
      const car = await CarService.getCarBySlug(slug);

      if (!car) {
        res.status(404).json({
          success: false,
          message: 'Car not found',
        });
        return;
      }

      res.json({
        success: true,
        data: car,
      });
    } catch (error: any) {
      console.error('获取汽车详情失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch car details',
        error: error.message,
      });
    }
  }

  // 更新汽车
  static async update(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const car = await CarService.updateCar(Number(id), req.body);

      if (!car) {
        res.status(404).json({
          success: false,
          message: 'Car not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Car updated successfully',
        data: car,
      });
    } catch (error: any) {
      console.error('更新汽车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to update car',
        error: error.message,
      });
    }
  }

  // 删除汽车
  static async delete(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const result = await CarService.deleteCar(Number(id));

      if (!result) {
        res.status(404).json({
          success: false,
          message: 'Car not found',
        });
        return;
      }

      res.json({
        success: true,
        message: 'Car deleted successfully',
      });
    } catch (error: any) {
      console.error('删除汽车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to delete car',
        error: error.message,
      });
    }
  }

  // 获取所有品牌
  static async getBrands(req: Request, res: Response): Promise<void> {
    try {
      const brands = await CarService.getBrands();

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
      const categories = await CarService.getCategories();

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

  // 获取推荐汽车
  static async getFeatured(req: Request, res: Response): Promise<void> {
    try {
      const { limit = 6 } = req.query;
      const cars = await CarService.getFeaturedCars(Number(limit));

      res.json({
        success: true,
        data: cars,
      });
    } catch (error: any) {
      console.error('获取推荐汽车失败:', error);
      res.status(500).json({
        success: false,
        message: 'Failed to fetch featured cars',
        error: error.message,
      });
    }
  }
}

export default CarController;

