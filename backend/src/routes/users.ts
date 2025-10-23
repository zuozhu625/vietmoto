import { Router, Request, Response } from 'express';
import { asyncHandler } from '../middleware/errorHandler';

const router = Router();

// 获取用户资料
router.get('/profile', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'User profile endpoint - Coming soon',
    data: null,
  });
}));

// 更新用户资料
router.put('/profile', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'Update user profile endpoint - Coming soon',
    data: null,
  });
}));

export default router;