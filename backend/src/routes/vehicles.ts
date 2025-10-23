import { Router } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import MotorcycleController from '../controllers/MotorcycleController';
import CarController from '../controllers/CarController';

const router = Router();

// n8n Webhook - 创建摩托车
router.post('/motorcycles/webhook', asyncHandler(MotorcycleController.create));

// 创建摩托车
router.post('/motorcycles', asyncHandler(MotorcycleController.create));

// 获取推荐摩托车
router.get('/motorcycles/featured', asyncHandler(MotorcycleController.getFeatured));

// 获取所有品牌
router.get('/motorcycles/brands', asyncHandler(MotorcycleController.getBrands));

// 获取所有分类
router.get('/motorcycles/categories', asyncHandler(MotorcycleController.getCategories));

// 获取摩托车列表（支持品牌筛选）- 必须放在:id路由之前
router.get('/motorcycles', asyncHandler(MotorcycleController.getList));

// 获取摩托车详情（通过ID）
router.get('/motorcycles/:id', asyncHandler(MotorcycleController.getById));

// 更新摩托车
router.put('/motorcycles/:id', asyncHandler(MotorcycleController.update));

// 删除摩托车
router.delete('/motorcycles/:id', asyncHandler(MotorcycleController.delete));

// ==================== 汽车路由 ====================

// 创建汽车
router.post('/cars', asyncHandler(CarController.create));

// 获取推荐汽车
router.get('/cars/featured', asyncHandler(CarController.getFeatured));

// 获取所有品牌
router.get('/cars/brands', asyncHandler(CarController.getBrands));

// 获取所有分类
router.get('/cars/categories', asyncHandler(CarController.getCategories));

// 获取汽车列表（支持品牌筛选）- 必须放在:id和:slug路由之前
router.get('/cars', asyncHandler(CarController.getList));

// 获取汽车详情（通过slug）
router.get('/cars/slug/:slug', asyncHandler(CarController.getBySlug));

// 获取汽车详情（通过ID）
router.get('/cars/:id', asyncHandler(CarController.getById));

// 更新汽车
router.put('/cars/:id', asyncHandler(CarController.update));

// 删除汽车
router.delete('/cars/:id', asyncHandler(CarController.delete));

export default router;
