import { Router, Request, Response } from 'express';
import { asyncHandler } from '../middleware/errorHandler';

const router = Router();

// 用户注册
router.post('/register', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'User registration endpoint - Coming soon',
    data: null,
  });
}));

// 用户登录
router.post('/login', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'User login endpoint - Coming soon',
    data: null,
  });
}));

// 用户登出
router.post('/logout', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'User logout endpoint - Coming soon',
    data: null,
  });
}));

// 刷新令牌
router.post('/refresh', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'Token refresh endpoint - Coming soon',
    data: null,
  });
}));

// 获取用户信息
router.get('/profile', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'User profile endpoint - Coming soon',
    data: null,
  });
}));

export default router;