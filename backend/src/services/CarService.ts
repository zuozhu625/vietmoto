import Car, { CarAttributes } from '../models/Car';
import { Op } from 'sequelize';

interface CarListParams {
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
}

class CarService {
  // 获取汽车列表（带筛选和分页）
  static async getCarsList(params: CarListParams) {
    const {
      page = 1,
      limit = 12,
      brand,
      category,
      fuel_type,
      min_price,
      max_price,
      status = 'active',
      search,
      sort,
      order,
    } = params;

    const offset = (page - 1) * limit;

    // 构建查询条件
    const where: any = { status };

    if (brand) where.brand = brand;
    if (category) where.category = category;
    if (fuel_type) where.fuel_type = fuel_type;
    
    if (min_price || max_price) {
      where.price_vnd = {};
      if (min_price) where.price_vnd[Op.gte] = min_price;
      if (max_price) where.price_vnd[Op.lte] = max_price;
    }

    if (search) {
      where[Op.or] = [
        { brand: { [Op.like]: `%${search}%` } },
        { model: { [Op.like]: `%${search}%` } },
        { description: { [Op.like]: `%${search}%` } },
      ];
    }

    // 排序参数
    const sortField = sort || 'year';
    const sortOrder = (order || 'DESC').toUpperCase() as 'ASC' | 'DESC';
    const orderBy: any[] = [[sortField, sortOrder]];
    // 添加view_count作为第二排序条件
    if (sortField !== 'view_count') {
      orderBy.push(['view_count', 'DESC']);
    }

    const { count, rows } = await Car.findAndCountAll({
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

  // 获取汽车详情
  static async getCarById(id: number) {
    const car = await Car.findByPk(id);
    
    if (car) {
      // 增加浏览次数
      await car.increment('view_count');
    }
    
    return car;
  }

  // 通过slug获取汽车
  static async getCarBySlug(slug: string) {
    const car = await Car.findOne({ where: { slug } });
    
    if (car) {
      await car.increment('view_count');
    }
    
    return car;
  }

  // 创建汽车
  static async createCar(data: Partial<CarAttributes>) {
    return await Car.create(data as any);
  }

  // 更新汽车
  static async updateCar(id: number, data: Partial<CarAttributes>) {
    const car = await Car.findByPk(id);
    
    if (!car) {
      return null;
    }
    
    await car.update(data);
    return car;
  }

  // 删除汽车
  static async deleteCar(id: number) {
    const car = await Car.findByPk(id);
    
    if (!car) {
      return null;
    }
    
    await car.destroy();
    return true;
  }

  // 获取所有品牌列表（带数量统计）
  static async getBrands(): Promise<Array<{ brand: string; count: number }>> {
    const { fn, col } = require('sequelize');
    const cars: any = await Car.findAll({
      attributes: [
        'brand',
        [fn('COUNT', col('id')), 'count']
      ],
      where: { status: 'active' },
      group: ['brand'],
      order: [[fn('COUNT', col('id')), 'DESC']],
      raw: true,
    });

    return cars.map((c: any) => ({
      brand: c.brand,
      count: parseInt(c.count, 10)
    }));
  }

  // 获取所有分类列表
  static async getCategories() {
    const cars = await Car.findAll({
      attributes: ['category'],
      where: { status: 'active' },
      group: ['category'],
    });

    return cars.map(c => c.category).filter(Boolean);
  }

  // 获取推荐汽车
  static async getFeaturedCars(limit: number = 6) {
    const cars = await Car.findAll({
      where: { 
        status: 'active',
        rating: { [Op.gte]: 4.5 }
      },
      limit,
      order: [['rating', 'DESC'], ['view_count', 'DESC']],
    });

    return cars;
  }
}

export default CarService;

