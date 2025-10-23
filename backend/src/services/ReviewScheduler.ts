import ReviewGeneratorService from './ReviewGeneratorService';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * 用户测评调度器
 * 定时自动生成用户测评内容并发布到News板块
 */
class ReviewScheduler {
  private intervalId: NodeJS.Timeout | null = null;
  private readonly INTERVAL_MINUTES = 40; // 每40分钟生成一条测评
  private rebuildCount = 0; // 重建计数器
  private readonly REBUILD_THRESHOLD = 5; // 每5条测评触发一次前端重建

  /**
   * 启动调度器
   */
  public start(): void {
    console.log(`🚀 启动用户测评生成调度器（每${this.INTERVAL_MINUTES}分钟生成一条，发布到News板块）`);

    // 立即生成一条
    this.generateReview();

    // 定时生成（每40分钟）
    this.intervalId = setInterval(() => {
      this.generateReview();
    }, this.INTERVAL_MINUTES * 60 * 1000);
  }

  /**
   * 停止调度器
   */
  public stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      console.log('🛑 用户测评生成调度器已停止');
    }
  }

  /**
   * 生成一条测评
   */
  private async generateReview(): Promise<void> {
    console.log('🤖 正在生成用户测评...');
    
    try {
      const success = await ReviewGeneratorService.generateOne();
      
      if (success) {
        console.log('✅ 用户测评生成成功');
        
        // 计数器递增
        this.rebuildCount++;
        
        // 每5条测评触发一次前端重建
        if (this.rebuildCount >= this.REBUILD_THRESHOLD) {
          console.log(`📦 已生成${this.rebuildCount}条测评，触发前端重建...`);
          this.triggerFrontendRebuild();
          this.rebuildCount = 0; // 重置计数器
        }
      } else {
        console.log('❌ 用户测评生成失败');
      }
    } catch (error) {
      console.error('❌ 生成测评时出错:', error);
    }
  }

  /**
   * 触发前端重建（后台执行）
   */
  private triggerFrontendRebuild(): void {
    exec('/root/越南摩托汽车网站/rebuild-frontend.sh', (error, stdout, stderr) => {
      if (error) {
        console.error('❌ 前端重建失败:', error.message);
        return;
      }
      if (stdout) console.log(stdout);
      if (stderr) console.error(stderr);
    });
  }
}

export default new ReviewScheduler();

