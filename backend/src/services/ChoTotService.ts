/**
 * Chợ Tốt API 数据获取服务
 * 从 Chợ Tốt 公开API获取二手摩托车数据
 */

import axios from 'axios';
import MarketplaceVehicle from '../models/MarketplaceVehicle';

interface ChoTotAd {
  ad_id: number;
  subject: string;
  body: string;
  price: number;
  image: string;
  images: string[];
  motorbikebrand?: number;
  motorbikemodel?: number;
  motorbiketype?: number;
  regdate?: number;
  mileage_v2?: number;
  condition_ad?: number;
  condition_ad_name?: string;
  region_name?: string;
  area_name?: string;
  ward_name?: string;
  location?: string;
  full_name?: string;
  account_id?: number;
  avatar?: string;
  average_rating?: number;
  sold_ads?: number;
  list_time?: number;
  status?: string;
  phone?: string;
  phone_hidden?: string;
}

interface ChoTotResponse {
  total: number;
  ads: ChoTotAd[];
}

class ChoTotService {
  private baseUrl = 'https://gateway.chotot.com/v1/public/ad-listing';
  private detailUrl = 'https://gateway.chotot.com/v1/public/ad-listing';
  
  // 分类ID映射
  private categories = {
    'moto-gas': '2020',      // 燃油摩托车
    'moto-electric': '2020', // 电动摩托车 (同样是2020分类，通过其他字段区分)
    'car-gas': '2010',       // 燃油汽车
    'car-electric': '2010',  // 电动汽车 (同样是2010分类，通过其他字段区分)
  };
  
  // 电动车辆关键词
  private electricKeywords = [
    'điện', 'electric', 'e-', 'ev', 'xe điện', 'xe máy điện', 'ô tô điện',
    'pin', 'battery', 'sạc', 'charging', 'hybrid', 'híbrido'
  ];
  
  // 燃油车辆关键词
  private gasKeywords = [
    'xăng', 'gas', 'petrol', 'diesel', 'dầu', 'nhiên liệu', 'động cơ',
    'máy', 'engine', 'cc', 'cm3', 'phân khối'
  ];
  
  /**
   * 获取广告详情（包含电话信息）
   */
  async fetchAdDetail(adId: number): Promise<any> {
    try {
      const response = await axios.get(`${this.detailUrl}/${adId}`, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': 'application/json',
        },
        timeout: 10000,
      });
      
      return response.data?.ad || null;
    } catch (error: any) {
      console.error(`❌ 获取广告 ${adId} 详情失败:`, error.message);
      return null;
    }
  }
  
  /**
   * 获取车辆列表（只获取最近3周的数据）
   * @param vehicleType - 车辆类型: moto-gas, moto-electric, car-gas, car-electric
   * @param limit - 需要的数量
   */
  async fetchVehicles(vehicleType: string, limit: number = 50): Promise<ChoTotAd[]> {
    try {
      const category = this.categories[vehicleType as keyof typeof this.categories] || '2020';
      
      const response = await axios.get<ChoTotResponse>(this.baseUrl, {
        params: {
          cg: category,
          st: 's,k', // 出售类型
          limit: limit * 3, // 多获取一些以确保过滤后有足够数据
          o: 0,
        },
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Accept': 'application/json',
        },
        timeout: 15000,
      });
      
      // 过滤最近3周的数据
      const threeWeeksAgo = Date.now() - (21 * 24 * 60 * 60 * 1000);
      const recentAds = (response.data.ads || []).filter(ad => {
        if (!ad.list_time) return false;
        const adTime = ad.list_time * 1000;
        return adTime >= threeWeeksAgo;
      }).slice(0, limit);
      
      console.log(`✅ [${vehicleType}] 成功获取 ${response.data.ads?.length || 0} 条数据，过滤后剩余 ${recentAds.length} 条（最近3周）`);
      return recentAds;
      
    } catch (error: any) {
      console.error(`❌ [${vehicleType}] 获取Chợ Tốt数据失败:`, error.message);
      throw error;
    }
  }
  
  /**
   * 保存或更新数据到数据库
   */
  async saveToDatabase(ads: ChoTotAd[], vehicleType: string): Promise<number> {
    let savedCount = 0;
    
    for (const ad of ads) {
      try {
        // 获取详情页信息（包含电话）
        const detail = await this.fetchAdDetail(ad.ad_id);
        const phone = detail?.phone || detail?.phone_hidden || ad.phone || ad.phone_hidden || '';
        
        // 智能判断实际车辆类型
        const actualVehicleType = this.determineVehicleType(ad, vehicleType);
        const isMotorcycle = actualVehicleType.startsWith('moto');
        
        // 从标题中提取年份
        const extractedYear = this.extractYearFromTitle(ad.subject);
        const finalYear = ad.regdate || extractedYear || undefined;
        
        console.log(`🔍 车辆分类: ${ad.subject} -> ${vehicleType} -> ${actualVehicleType}, 年份: ${finalYear}`);
        
        const data = {
          external_id: ad.ad_id.toString(),
          external_url: `https://xe.chotot.com/${ad.ad_id}`,
          source: 'chotot',
          type: isMotorcycle ? 'motorcycle' : 'car',
          vehicle_type: actualVehicleType, // 使用智能判断的结果
          brand: this.getBrandName(ad.motorbikebrand),
          model: ad.subject?.split(' ')[0] || '',
          year: finalYear,
          price: ad.price,
          title: ad.subject,
          description: ad.body,
          mileage: ad.mileage_v2 || undefined,
          condition_text: ad.condition_ad_name || '',
          condition_rating: ad.condition_ad === 1 ? 3 : 5,
          image_url: ad.image,
          images: JSON.stringify(ad.images || []),
          city: ad.region_name || '',
          district: ad.area_name || '',
          ward: ad.ward_name || '',
          location: ad.location || '',
          seller_name: ad.full_name || '',
          seller_id: ad.account_id?.toString() || '',
          seller_avatar: ad.avatar || '',
          seller_phone: phone,
          seller_rating: ad.average_rating || undefined,
          seller_sold_count: ad.sold_ads || 0,
          view_count: 0,
          favorites_count: 0,
          status: ad.status === 'active' ? 'active' : 'inactive',
          is_featured: false,
          published_at: ad.list_time ? new Date(ad.list_time) : new Date(),
        };
        
        // 使用upsert自动处理插入或更新
        await MarketplaceVehicle.upsert(data);
        savedCount++;
        
        // 添加延迟避免请求过快
        await new Promise(resolve => setTimeout(resolve, 500));
        
      } catch (error: any) {
        console.error(`❌ 保存广告 ${ad.ad_id} 失败:`, error.message);
      }
    }
    
    return savedCount;
  }
  
  /**
   * 从标题中提取年份
   * @param title - 车辆标题
   * @returns 提取到的年份，如果没有则返回null
   */
  private extractYearFromTitle(title: string): number | null {
    if (!title) return null;
    
    // 匹配4位数字年份 (1990-2030)
    const yearMatch = title.match(/\b(19[9]\d|20[0-2]\d|2030)\b/);
    if (yearMatch) {
      const year = parseInt(yearMatch[1]);
      if (year >= 1990 && year <= 2030) {
        return year;
      }
    }
    
    return null;
  }
  
  /**
   * 智能判断车辆类型（燃油 vs 电动）
   * @param ad - 广告数据
   * @param requestedType - 请求的类型
   * @returns 实际应该分类的类型
   */
  private determineVehicleType(ad: ChoTotAd, requestedType: string): string {
    const title = (ad.subject || '').toLowerCase();
    const description = (ad.body || '').toLowerCase();
    const text = `${title} ${description}`;
    
    // 检查电动关键词
    const hasElectricKeywords = this.electricKeywords.some(keyword => 
      text.includes(keyword.toLowerCase())
    );
    
    // 检查燃油关键词
    const hasGasKeywords = this.gasKeywords.some(keyword => 
      text.includes(keyword.toLowerCase())
    );
    
    // 根据请求类型和关键词判断
    if (requestedType.startsWith('moto')) {
      if (hasElectricKeywords && !hasGasKeywords) {
        return 'moto-electric';
      } else if (hasGasKeywords && !hasElectricKeywords) {
        return 'moto-gas';
      } else {
        // 如果都有或都没有，根据请求类型决定
        return requestedType;
      }
    } else if (requestedType.startsWith('car')) {
      if (hasElectricKeywords && !hasGasKeywords) {
        return 'car-electric';
      } else if (hasGasKeywords && !hasElectricKeywords) {
        return 'car-gas';
      } else {
        // 如果都有或都没有，根据请求类型决定
        return requestedType;
      }
    }
    
    return requestedType;
  }
  
  /**
   * 获取品牌名称（简化版，可以后续扩展）
   */
  private getBrandName(brandId?: number): string {
    const brands: Record<number, string> = {
      1: 'Honda',
      2: 'Yamaha',
      3: 'Piaggio',
      4: 'Suzuki',
      5: 'SYM',
      6: 'Aprilia',
      9: 'BMW',
      12: 'Ducati',
      17: 'Kawasaki',
      20: 'KTM',
      21: 'Kymco',
      // 可以添加更多品牌映射
    };
    
    return brandId ? (brands[brandId] || 'Other') : 'Other';
  }
  
  /**
   * 执行完整的数据采集流程（按类型）
   */
  async fetchAndSaveByType(vehicleType: string, limit: number = 50): Promise<{ fetched: number; saved: number }> {
    console.log(`\n🚀 开始从Chợ Tốt获取 [${vehicleType}] 数据...`);
    console.log(`📊 计划获取: ${limit} 条`);
    
    try {
      // 获取数据
      const ads = await this.fetchVehicles(vehicleType, limit);
      
      if (ads.length === 0) {
        console.log(`⚠️  [${vehicleType}] 未获取到任何数据`);
        return { fetched: 0, saved: 0 };
      }
      
      // 保存到数据库
      const savedCount = await this.saveToDatabase(ads, vehicleType);
      
      console.log(`✅ [${vehicleType}] 完成! 获取: ${ads.length} 条, 保存: ${savedCount} 条\n`);
      
      return {
        fetched: ads.length,
        saved: savedCount,
      };
      
    } catch (error: any) {
      console.error(`❌ [${vehicleType}] 数据采集失败:`, error.message);
      throw error;
    }
  }
  
  /**
   * 清理和重新分类现有数据
   */
  async reclassifyExistingData(): Promise<{ processed: number; updated: number }> {
    console.log('\n🔄 开始重新分类现有数据...');
    
    const vehicles = await MarketplaceVehicle.findAll({
      where: { status: 'active' },
      attributes: ['id', 'title', 'description', 'vehicle_type', 'external_id']
    });
    
    let processed = 0;
    let updated = 0;
    
    for (const vehicle of vehicles) {
      try {
        const ad: ChoTotAd = {
          ad_id: parseInt(vehicle.external_id),
          subject: vehicle.title,
          body: vehicle.description || '',
          price: 0,
          image: '',
          images: [],
        };
        
        // 智能判断正确的类型
        const correctType = this.determineVehicleType(ad, vehicle.vehicle_type);
        
        // 从标题中提取年份
        const extractedYear = this.extractYearFromTitle(vehicle.title);
        const finalYear = vehicle.year || extractedYear || undefined;
        
        // 检查是否需要更新
        const needsUpdate = correctType !== vehicle.vehicle_type || finalYear !== vehicle.year;
        
        if (needsUpdate) {
          const updateData: any = {};
          if (correctType !== vehicle.vehicle_type) {
            updateData.vehicle_type = correctType;
          }
          if (finalYear !== vehicle.year) {
            updateData.year = finalYear;
          }
          
          await vehicle.update(updateData);
          console.log(`✅ 重新分类: ${vehicle.title} -> ${vehicle.vehicle_type} -> ${correctType}, 年份: ${vehicle.year} -> ${finalYear}`);
          updated++;
        }
        
        processed++;
      } catch (error: any) {
        console.error(`❌ 重新分类失败 ${vehicle.id}:`, error.message);
      }
    }
    
    console.log(`\n📊 重新分类完成: 处理 ${processed} 条, 更新 ${updated} 条\n`);
    return { processed, updated };
  }
  
  /**
   * 同步所有分类的数据
   */
  async fetchAndSaveAll(limitPerType: number = 50): Promise<Record<string, { fetched: number; saved: number }>> {
    const types = ['moto-gas', 'moto-electric', 'car-gas', 'car-electric'];
    const results: Record<string, { fetched: number; saved: number }> = {};
    
    console.log(`\n🚀 开始同步所有分类数据，每个分类 ${limitPerType} 条...`);
    
    for (const type of types) {
      try {
        results[type] = await this.fetchAndSaveByType(type, limitPerType);
        // 分类之间延迟，避免请求过快
        await new Promise(resolve => setTimeout(resolve, 2000));
      } catch (error: any) {
        console.error(`❌ [${type}] 同步失败:`, error.message);
        results[type] = { fetched: 0, saved: 0 };
      }
    }
    
    console.log('\n📊 同步汇总:');
    let totalFetched = 0;
    let totalSaved = 0;
    for (const [type, result] of Object.entries(results)) {
      console.log(`  ${type}: 获取 ${result.fetched} 条, 保存 ${result.saved} 条`);
      totalFetched += result.fetched;
      totalSaved += result.saved;
    }
    console.log(`  总计: 获取 ${totalFetched} 条, 保存 ${totalSaved} 条\n`);
    
    return results;
  }
}

export default new ChoTotService();

