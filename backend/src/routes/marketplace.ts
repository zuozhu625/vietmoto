/**
 * 二手市场 API路由
 */

import express, { Request, Response } from 'express';
import { Op } from 'sequelize';
import MarketplaceVehicle from '../models/MarketplaceVehicle';
import MarketplaceScheduler from '../services/MarketplaceScheduler';

const router = express.Router();

/**
 * GET /api/marketplace
 * 获取二手车辆列表
 */
router.get('/', async (req: Request, res: Response) => {
  try {
    const {
      page = '1',
      limit = '12',
      type = 'motorcycle', // motorcycle | car
      vehicle_type, // moto-gas | moto-electric | car-gas | car-electric
      brand,
      minPrice,
      maxPrice,
      minYear,
      maxYear,
      city,
      sort = 'latest', // latest | price_asc | price_desc | popular
    } = req.query;
    
    const pageNum = parseInt(page as string);
    const limitNum = parseInt(limit as string);
    const offset = (pageNum - 1) * limitNum;
    
    // 构建WHERE条件
    const where: any = { status: 'active' };
    
    // 优先使用vehicle_type筛选，如果没有则使用type
    if (vehicle_type) {
      where.vehicle_type = vehicle_type;
    } else if (type) {
      where.type = type;
    }
    
    if (brand) {
      where.brand = brand;
    }
    
    if (minPrice || maxPrice) {
      where.price = {};
      if (minPrice) where.price[Op.gte] = parseFloat(minPrice as string);
      if (maxPrice) where.price[Op.lte] = parseFloat(maxPrice as string);
    }
    
    if (minYear || maxYear) {
      where.year = {};
      if (minYear) where.year[Op.gte] = parseInt(minYear as string);
      if (maxYear) where.year[Op.lte] = parseInt(maxYear as string);
    }
    
    if (city) {
      where.city = city;
    }
    
    // 排序 - 默认按年份最新排序，年份为空时按发布时间排序
    let order: any[] = [
      ['year', 'DESC NULLS LAST'], // 年份最新，空值排在最后
      ['published_at', 'DESC']      // 发布时间最新
    ];
    if (sort === 'price_asc') order = [['price', 'ASC']];
    if (sort === 'price_desc') order = [['price', 'DESC']];
    if (sort === 'popular') order = [['view_count', 'DESC']];
    if (sort === 'year_desc') order = [['year', 'DESC NULLS LAST'], ['published_at', 'DESC']]; // 年份最新
    if (sort === 'year_asc') order = [['year', 'ASC NULLS LAST'], ['published_at', 'DESC']]; // 年份最旧
    if (sort === 'latest') order = [['published_at', 'DESC']]; // 最新发布
    
    // 查询数据
    const { rows: vehicles, count: total } = await MarketplaceVehicle.findAndCountAll({
      where,
      order,
      limit: limitNum,
      offset,
      attributes: [
        'id', 'external_id', 'external_url', 'source',
        'type', 'vehicle_type', 'brand', 'model', 'year', 'price',
        'title', 'description', 'mileage', 'condition_text', 'condition_rating',
        'image_url', 'images', 'city', 'district', 'ward',
        'seller_name', 'seller_avatar', 'seller_rating', 'seller_sold_count',
        'view_count', 'favorites_count', 'status', 'published_at'
      ],
    });
    
    // 解析JSON字段
    const formattedVehicles = vehicles.map(vehicle => {
      const data = vehicle.toJSON();
      return {
        ...data,
        images: data.images ? JSON.parse(data.images) : [],
      };
    });
    
    res.json({
      success: true,
      data: formattedVehicles,
      pagination: {
        page: pageNum,
        limit: limitNum,
        total,
        totalPages: Math.ceil(total / limitNum),
      },
    });
    
  } catch (error: any) {
    console.error('获取二手车辆列表失败:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch marketplace vehicles',
      message: error.message,
    });
  }
});

/**
 * GET /api/marketplace/:id
 * 获取单个车辆详情
 */
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    
    const vehicle = await MarketplaceVehicle.findOne({
      where: { id, status: 'active' },
    });
    
    if (!vehicle) {
      res.status(404).json({
        success: false,
        error: 'Vehicle not found',
      });
      return;
    }
    
    // 增加浏览次数
    await vehicle.increment('view_count');
    
    // 解析JSON字段
    const vehicleData = vehicle.toJSON();
    vehicleData.images = vehicleData.images ? JSON.parse(vehicleData.images) : [];
    
    res.json({
      success: true,
      data: vehicleData,
    });
    
  } catch (error: any) {
    console.error('获取车辆详情失败:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch vehicle details',
      message: error.message,
    });
  }
});

/**
 * POST /api/marketplace/sync
 * 手动触发数据同步（管理员功能）
 */
router.post('/sync', async (req: Request, res: Response) => {
  try {
    console.log('📥 收到手动同步请求...');
    
    const result = await MarketplaceScheduler.triggerUpdate();
    
    res.json({
      success: true,
      message: 'Data sync completed',
      data: result,
    });
    
  } catch (error: any) {
    console.error('数据同步失败:', error);
    res.status(500).json({
      success: false,
      error: 'Sync failed',
      message: error.message,
    });
  }
});

/**
 * POST /api/marketplace/reclassify
 * 重新分类现有数据（修复分类错误）
 */
router.post('/reclassify', async (req: Request, res: Response) => {
  try {
    console.log('📥 收到重新分类请求...');
    
    const ChoTotService = require('../services/ChoTotService').default;
    const result = await ChoTotService.reclassifyExistingData();
    
    res.json({
      success: true,
      message: 'Data reclassification completed',
      data: result,
    });
    
  } catch (error: any) {
    console.error('数据重新分类失败:', error);
    res.status(500).json({
      success: false,
      error: 'Reclassification failed',
      message: error.message,
    });
  }
});

/**
 * GET /api/marketplace/stats/summary
 * 获取统计信息
 */
router.get('/stats/summary', async (req: Request, res: Response) => {
  try {
    const total = await MarketplaceVehicle.count({ where: { status: 'active' } });
    
    // 获取所有数据来计算统计信息
    const vehicles = await MarketplaceVehicle.findAll({
      where: { status: 'active' },
      attributes: ['brand', 'city', 'price'],
    });
    
    const brands = new Set(vehicles.map(v => v.brand).filter(Boolean)).size;
    const cities = new Set(vehicles.map(v => v.city).filter(Boolean)).size;
    const prices = vehicles.map(v => v.price);
    const avgPrice = prices.reduce((a, b) => a + b, 0) / prices.length || 0;
    const minPrice = Math.min(...prices) || 0;
    const maxPrice = Math.max(...prices) || 0;
    
    res.json({
      success: true,
      data: {
        total,
        brands,
        cities,
        avgPrice,
        minPrice,
        maxPrice,
      },
    });
    
  } catch (error: any) {
    console.error('获取统计信息失败:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch stats',
      message: error.message,
    });
  }
});

export default router;
