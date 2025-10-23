import { Router, Request, Response } from 'express';
import { asyncHandler } from '../middleware/errorHandler';
import QAGeneratorService from '../services/QAGeneratorService';
import Question from '../models/Question';
import Answer from '../models/Answer';
import { Op } from 'sequelize';

const router = Router();

// 获取问题列表
router.get('/', asyncHandler(async (req: Request, res: Response) => {
  const { 
    page = 1, 
    limit = 20,
    category,
    vehicle_type,
    sort = 'latest',
    search
  } = req.query;

  const pageNum = parseInt(page as string);
  const limitNum = parseInt(limit as string);
  const offset = (pageNum - 1) * limitNum;

  // 构建查询条件
  const where: any = { status: 'open' };
  if (category) where.category = category;
  if (vehicle_type) where.vehicle_type = vehicle_type;
  
  // 添加搜索功能 - 只搜索问题标题
  if (search && typeof search === 'string') {
    where.title = {
      [Op.like]: `%${search}%`
    };
  }

  // 排序方式
  let order: any = [['created_at', 'DESC']];
  if (sort === 'popular') {
    order = [['view_count', 'DESC']];
  } else if (sort === 'hot') {
    order = [['answers_count', 'DESC'], ['votes_count', 'DESC']];
  }

  const { count, rows: questions } = await Question.findAndCountAll({
    where,
    order,
    limit: limitNum,
    offset,
    raw: true
  });

  res.json({
    success: true,
    data: questions,
    pagination: {
      page: pageNum,
      limit: limitNum,
      total: count,
      totalPages: Math.ceil(count / limitNum)
    }
  });
}));

// 获取问题详情
router.get('/:id', asyncHandler(async (req: Request, res: Response) => {
  const { id } = req.params;

  const result = await QAGeneratorService.getQuestionWithAnswers(parseInt(id));

  if (!result) {
    res.status(404).json({
      success: false,
      message: '问题不存在'
    });
    return;
  }

  // 增加浏览量
  await Question.increment('view_count', { 
    where: { id: parseInt(id) } 
  });

  res.json({
    success: true,
    data: result
  });
}));

// 手动触发生成Q&A（调试用）
router.post('/generate', asyncHandler(async (req: Request, res: Response) => {
  const success = await QAGeneratorService.generateOne();

  res.json({
    success,
    message: success ? '生成成功' : '生成失败'
  });
}));

export default router;