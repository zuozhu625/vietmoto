import { Router } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import NewsController from '../controllers/NewsController';

const router = Router();

// n8n Webhook - 创建测评
router.post('/webhook', asyncHandler(NewsController.create));

// 创建测评（也可以通过常规API调用）
router.post('/', asyncHandler(NewsController.create));

// 获取测评列表
router.get('/', asyncHandler(NewsController.getList));

// 获取最新测评
router.get('/latest', asyncHandler(NewsController.getLatest));

// 获取所有分类
router.get('/categories', asyncHandler(NewsController.getCategories));

// 获取测评详情（通过slug）
router.get('/slug/:slug', asyncHandler(NewsController.getBySlug));

// 获取相关测评
router.get('/slug/:slug/related', asyncHandler(NewsController.getRelated));

// 获取测评详情（通过ID）
router.get('/:id', asyncHandler(NewsController.getById));

// 更新测评
router.put('/:id', asyncHandler(NewsController.update));

// 删除测评
router.delete('/:id', asyncHandler(NewsController.delete));

export default router;