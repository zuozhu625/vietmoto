import { Router, Request, Response } from 'express';
import { asyncHandler } from '../middleware/errorHandler';

const router = Router();

// 上传图片
router.post('/image', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'Image upload endpoint - Coming soon',
    data: null,
  });
}));

// 上传文件
router.post('/file', asyncHandler(async (req: Request, res: Response) => {
  res.json({
    success: true,
    message: 'File upload endpoint - Coming soon',
    data: null,
  });
}));

export default router;