import QAGeneratorService from './QAGeneratorService';

/**
 * Q&A 定时生成调度器
 * 每10分钟自动生成一条问答
 */
class QAScheduler {
  private intervalId: NodeJS.Timeout | null = null;
  private isRunning = false;

  /**
   * 启动调度器
   */
  start() {
    if (this.isRunning) {
      console.log('⚠️  Q&A调度器已经在运行');
      return;
    }

    console.log('🚀 启动Q&A自动生成调度器（每10分钟生成一条）');

    // 立即生成一条（启动时）
    this.generateQA();

    // 设置定时任务：每10分钟（600000毫秒）生成一条
    this.intervalId = setInterval(() => {
      this.generateQA();
    }, 10 * 60 * 1000); // 10分钟

    this.isRunning = true;
  }

  /**
   * 停止调度器
   */
  stop() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.isRunning = false;
      console.log('⏹️  Q&A调度器已停止');
    }
  }

  /**
   * 生成一条Q&A
   */
  private async generateQA() {
    try {
      const timestamp = new Date().toLocaleString('vi-VN');
      console.log(`[${timestamp}] 🤖 开始生成新的Q&A...`);
      
      const success = await QAGeneratorService.generateOne();
      
      if (success) {
        console.log(`[${timestamp}] ✅ Q&A生成成功`);
        
        // 定期清理旧数据（已禁用 - 保留所有问答积累）
        // await QAGeneratorService.cleanOldData();
      } else {
        console.log(`[${timestamp}] ⚠️  Q&A生成失败`);
      }
    } catch (error) {
      console.error('Q&A生成过程出错:', error);
    }
  }

  /**
   * 获取调度器状态
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      message: this.isRunning ? '调度器运行中' : '调度器已停止'
    };
  }
}

export default new QAScheduler();

