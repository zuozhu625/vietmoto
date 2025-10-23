/**
 * Sitemap专用API路由
 * 只返回数据库中真实存在的数据，不包含外部API数据
 */

import { Router } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import MarketplaceVehicle from '../models/MarketplaceVehicle';
import Car from '../models/Car';
import Motorcycle from '../models/Motorcycle';
import News from '../models/News';

const router = Router();

/**
 * GET /api/sitemap/motorcycles
 * 获取摩托车列表（仅数据库数据，无limit限制）
 */
router.get('/motorcycles', asyncHandler(async (req: any, res: any) => {
  const motorcycles = await Motorcycle.findAll({
    where: { status: 'active' },
    attributes: ['id', 'updated_at', 'created_at'],
    // 移除limit限制，返回所有active摩托车
  });

  res.json({
    success: true,
    data: motorcycles.map(m => ({
      id: m.id,
      lastmod: m.updated_at || m.created_at,
    })),
  });
}));

/**
 * GET /api/sitemap/cars
 * 获取汽车列表（仅数据库数据，无limit限制）
 */
router.get('/cars', asyncHandler(async (req: any, res: any) => {
  const cars = await Car.findAll({
    where: { status: 'active' },
    attributes: ['id', 'slug', 'updated_at', 'created_at'],
    // 移除limit限制，返回所有active汽车
  });

  res.json({
    success: true,
    data: cars.map(c => ({
      id: c.id,
      slug: c.slug,
      lastmod: c.updated_at || c.created_at,
    })),
  });
}));

/**
 * GET /api/sitemap/reviews
 * 获取测评列表（仅数据库数据，无limit限制）
 */
router.get('/reviews', asyncHandler(async (req: any, res: any) => {
  const reviews = await News.findAll({
    where: { 
      status: 'published',
      slug: { [require('sequelize').Op.ne]: null }
    },
    attributes: ['id', 'slug', 'published_at', 'updated_at', 'created_at'],
    // 移除limit限制，返回所有published测评
  });

  res.json({
    success: true,
    data: reviews.map(r => ({
      id: r.id,
      slug: r.slug,
      lastmod: r.published_at || r.updated_at || r.created_at,
    })),
  });
}));

/**
 * GET /api/sitemap/marketplace
 * 获取二手市场列表（仅数据库数据，无limit限制）
 */
router.get('/marketplace', asyncHandler(async (req: any, res: any) => {
  const marketplace = await MarketplaceVehicle.findAll({
    where: { status: 'active' },
    attributes: ['id', 'updated_at', 'published_at'],
    // 移除limit限制，返回所有active二手车
  });

  res.json({
    success: true,
    data: marketplace.map(m => ({
      id: m.id,
      lastmod: m.updated_at || m.published_at,
    })),
  });
}));

export default router;
