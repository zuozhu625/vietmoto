import Motorcycle, { MotorcycleAttributes } from '../models/Motorcycle';
import { Op } from 'sequelize';

// 生成slug的辅助函数
function generateSlug(brand: string, model: string, year: number, id?: number): string {
  const baseSlug = `${brand}-${model}-${year}`
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .trim();
  
  return id ? `${baseSlug}-${id}` : baseSlug;
}

export class MotorcycleService {
  // 创建摩托车（n8n webhook调用）
  static async createMotorcycle(data: Partial<MotorcycleAttributes>) {
    try {
      const motorcycle = await Motorcycle.create({
        ...data,
        status: data.status || 'active',
        abs: data.abs || false,
        smart_key: data.smart_key || false,
        view_count: 0,
      } as any);

      return motorcycle;
    } catch (error) {
      console.error('创建摩托车失败:', error);
      throw error;
    }
  }

  // 获取摩托车列表（支持分页、筛选、排序）
  static async getMotorcyclesList(params: {
    page?: number;
    limit?: number;
    brand?: string;
    category?: string;
    fuel_type?: string;
    min_price?: number;
    max_price?: number;
    status?: string;
    search?: string;
    sort?: string;
    order?: string;
  }) {
    const page = params.page || 1;
    const limit = params.limit || 12;
    const offset = (page - 1) * limit;

    const where: any = {};

    if (params.brand) {
      where.brand = params.brand;
    }

    if (params.category) {
      where.category = params.category;
    }

    if (params.fuel_type) {
      where.fuel_type = params.fuel_type;
    }

    if (params.min_price || params.max_price) {
      where.price_vnd = {};
      if (params.min_price) {
        where.price_vnd[Op.gte] = params.min_price;
      }
      if (params.max_price) {
        where.price_vnd[Op.lte] = params.max_price;
      }
    }

    if (params.status) {
      where.status = params.status;
    } else {
      where.status = 'active';
    }

    if (params.search) {
      where[Op.or] = [
        { brand: { [Op.like]: `%${params.search}%` } },
        { model: { [Op.like]: `%${params.search}%` } },
        { description: { [Op.like]: `%${params.search}%` } },
      ];
    }

    // 排序参数 - 默认按年份降序，确保2025年车型优先显示
    const sortField = params.sort || 'year';
    const sortOrder = (params.order || 'DESC').toUpperCase() as 'ASC' | 'DESC';
    const orderBy: any[] = [[sortField, sortOrder]];
    // 添加view_count作为第二排序条件
    if (sortField !== 'view_count') {
      orderBy.push(['view_count', 'DESC']);
    }

    const { count, rows } = await Motorcycle.findAndCountAll({
      where,
      limit,
      offset,
      order: orderBy,
    });

    return {
      data: rows,
      pagination: {
        total: count,
        page,
        limit,
        pages: Math.ceil(count / limit),
      },
    };
  }

  // 根据ID获取摩托车详情
  static async getMotorcycleById(id: number) {
    const motorcycle = await Motorcycle.findByPk(id);

    if (!motorcycle) {
      return null;
    }

    // 增加浏览次数
    await motorcycle.increment('view_count');

    return motorcycle;
  }

  // 更新摩托车
  static async updateMotorcycle(id: number, data: Partial<MotorcycleAttributes>) {
    const motorcycle = await Motorcycle.findByPk(id);

    if (!motorcycle) {
      return null;
    }

    await motorcycle.update(data);
    return motorcycle;
  }

  // 删除摩托车
  static async deleteMotorcycle(id: number) {
    const motorcycle = await Motorcycle.findByPk(id);

    if (!motorcycle) {
      return null;
    }

    await motorcycle.destroy();
    return true;
  }

  // 获取所有品牌列表（带数量统计）
  static async getBrands(): Promise<Array<{ brand: string; count: number }>> {
    const { fn, col } = require('sequelize');
    const motorcycles: any = await Motorcycle.findAll({
      attributes: [
        'brand',
        [fn('COUNT', col('id')), 'count']
      ],
      where: { status: 'active' },
      group: ['brand'],
      order: [[fn('COUNT', col('id')), 'DESC']],
      raw: true,
    });

    return motorcycles.map((m: any) => ({
      brand: m.brand,
      count: parseInt(m.count, 10)
    }));
  }

  // 获取所有分类列表
  static async getCategories() {
    const motorcycles = await Motorcycle.findAll({
      attributes: ['category'],
      where: { status: 'active' },
      group: ['category'],
    });

    return motorcycles.map(m => m.category).filter(Boolean);
  }

  // 获取推荐摩托车
  static async getFeaturedMotorcycles(limit: number = 6) {
    const motorcycles = await Motorcycle.findAll({
      where: { 
        status: 'active',
        rating: { [Op.gte]: 4.5 }
      },
      limit,
      order: [['rating', 'DESC'], ['view_count', 'DESC']],
    });

    return motorcycles;
  }
}

export default MotorcycleService;

