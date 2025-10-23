/**
 * 二手市场数据定时调度器
 * 每天自动从Chợ Tốt获取最新数据
 */

import ChoTotService from './ChoTotService';

class MarketplaceScheduler {
  private intervalId: NodeJS.Timeout | null = null;
  private isRunning: boolean = false;
  
  // 更新间隔：每12小时更新一次 (12 * 60 * 60 * 1000)
  private readonly UPDATE_INTERVAL = 12 * 60 * 60 * 1000;
  
  /**
   * 启动调度器
   */
  start(): void {
    if (this.isRunning) {
      console.log('⚠️  Marketplace调度器已经在运行中');
      return;
    }
    
    console.log('🚀 启动Marketplace数据调度器...');
    console.log(`📅 更新频率: 每12小时`);
    console.log(`🔗 数据源: Chợ Tốt API`);
    
    // 立即执行一次
    this.fetchData();
    
    // 设置定时任务
    this.intervalId = setInterval(() => {
      this.fetchData();
    }, this.UPDATE_INTERVAL);
    
    this.isRunning = true;
    console.log('✅ Marketplace调度器启动成功\n');
  }
  
  /**
   * 停止调度器
   */
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
      this.isRunning = false;
      console.log('🛑 Marketplace调度器已停止');
    }
  }
  
  /**
   * 获取调度器状态
   */
  getStatus(): { running: boolean; interval: number } {
    return {
      running: this.isRunning,
      interval: this.UPDATE_INTERVAL,
    };
  }
  
  /**
   * 执行数据获取
   */
  private async fetchData(): Promise<void> {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    console.log(`\n⏰ [${timestamp}] 开始Marketplace数据更新...`);
    
    try {
      // 每次获取50条最新数据
      const result = await ChoTotService.fetchAndSaveAll(50);
      
      console.log(`📊 数据更新统计:`);
      console.log(`   - 获取: ${result.fetched} 条`);
      console.log(`   - 保存: ${result.saved} 条`);
      console.log(`   - 下次更新: 12小时后\n`);
      
    } catch (error: any) {
      console.error(`❌ Marketplace数据更新失败:`, error.message);
    }
  }
  
  /**
   * 手动触发更新（用于测试或强制更新）
   */
  async triggerUpdate(): Promise<Record<string, { fetched: number; saved: number }>> {
    console.log('🔄 手动触发Marketplace数据更新...');
    return await ChoTotService.fetchAndSaveAll(50);
  }
}

export default new MarketplaceScheduler();

