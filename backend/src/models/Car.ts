import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

// 汽车属性接口（方案A：30个核心字段）
export interface CarAttributes {
  id: number;
  
  // 基础信息（7个）
  brand: string;
  model: string;
  year: number;
  category: string;
  slug: string;
  price_vnd: number;
  seating_capacity: number;
  
  // 发动机系统（8个）
  engine_capacity_l?: number;
  engine_type?: string;
  power_hp?: number;
  torque_nm?: number;
  fuel_type: string;
  transmission?: string;
  drive_type?: string;
  cylinder_count?: number;
  
  // 电动车参数（3个）
  battery_kwh?: number;
  range_km?: number;
  charge_time_h?: number;
  
  // 尺寸重量（6个）
  length_mm?: number;
  width_mm?: number;
  height_mm?: number;
  wheelbase_mm?: number;
  curb_weight_kg?: number;
  trunk_capacity_l?: number;
  
  // 配置信息（6个）
  abs: boolean;
  airbag_count?: number;
  smart_key: boolean;
  display_type?: string;
  infotainment_size?: number;
  fuel_consumption?: string;
  
  // 系统字段
  description?: string;
  features?: string;
  colors?: string;
  image_url?: string;
  image_gallery?: string;
  rating?: number;
  review_count: number;
  view_count: number;
  status: string;
  created_at: Date;
  updated_at: Date;
}

// 创建汽车时的可选属性
interface CarCreationAttributes extends Optional<CarAttributes, 
  'id' | 'engine_capacity_l' | 'engine_type' | 'power_hp' | 'torque_nm' | 
  'transmission' | 'drive_type' | 'cylinder_count' | 'battery_kwh' | 
  'range_km' | 'charge_time_h' | 'length_mm' | 'width_mm' | 'height_mm' | 
  'wheelbase_mm' | 'curb_weight_kg' | 'trunk_capacity_l' | 'airbag_count' | 
  'display_type' | 'infotainment_size' | 'fuel_consumption' | 'description' | 
  'features' | 'colors' | 'image_url' | 'image_gallery' | 'rating' | 
  'review_count' | 'view_count' | 'status' | 'created_at' | 'updated_at'> {}

// 定义Car模型类
class Car extends Model<CarAttributes, CarCreationAttributes> implements CarAttributes {
  public id!: number;
  
  // 基础信息
  public brand!: string;
  public model!: string;
  public year!: number;
  public category!: string;
  public slug!: string;
  public price_vnd!: number;
  public seating_capacity!: number;
  
  // 发动机系统
  public engine_capacity_l?: number;
  public engine_type?: string;
  public power_hp?: number;
  public torque_nm?: number;
  public fuel_type!: string;
  public transmission?: string;
  public drive_type?: string;
  public cylinder_count?: number;
  
  // 电动车参数
  public battery_kwh?: number;
  public range_km?: number;
  public charge_time_h?: number;
  
  // 尺寸重量
  public length_mm?: number;
  public width_mm?: number;
  public height_mm?: number;
  public wheelbase_mm?: number;
  public curb_weight_kg?: number;
  public trunk_capacity_l?: number;
  
  // 配置信息
  public abs!: boolean;
  public airbag_count?: number;
  public smart_key!: boolean;
  public display_type?: string;
  public infotainment_size?: number;
  public fuel_consumption?: string;
  
  // 系统字段
  public description?: string;
  public features?: string;
  public colors?: string;
  public image_url?: string;
  public image_gallery?: string;
  public rating?: number;
  public review_count!: number;
  public view_count!: number;
  public status!: string;
  public created_at!: Date;
  public updated_at!: Date;
}

// 初始化模型
Car.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    // 基础信息
    brand: {
      type: DataTypes.STRING(100),
      allowNull: false,
      comment: '品牌',
    },
    model: {
      type: DataTypes.STRING(100),
      allowNull: false,
      comment: '型号',
    },
    year: {
      type: DataTypes.INTEGER,
      allowNull: false,
      comment: '年份',
    },
    category: {
      type: DataTypes.STRING(100),
      allowNull: false,
      comment: '车型分类',
    },
    slug: {
      type: DataTypes.STRING(200),
      allowNull: false,
      unique: true,
      comment: 'URL友好标识',
    },
    price_vnd: {
      type: DataTypes.DECIMAL(15, 2),
      allowNull: false,
      comment: '价格（越南盾）',
    },
    seating_capacity: {
      type: DataTypes.INTEGER,
      allowNull: false,
      comment: '座位数',
    },
    // 发动机系统
    engine_capacity_l: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '发动机排量（升）',
    },
    engine_type: {
      type: DataTypes.STRING(200),
      allowNull: true,
      comment: '发动机类型',
    },
    power_hp: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '最大功率（马力）',
    },
    torque_nm: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '最大扭矩（牛米）',
    },
    fuel_type: {
      type: DataTypes.STRING(50),
      allowNull: false,
      defaultValue: 'Xăng',
      comment: '燃料类型',
    },
    transmission: {
      type: DataTypes.STRING(200),
      allowNull: true,
      comment: '变速箱类型',
    },
    drive_type: {
      type: DataTypes.STRING(50),
      allowNull: true,
      comment: '驱动方式',
    },
    cylinder_count: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '气缸数',
    },
    // 电动车参数
    battery_kwh: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '电池容量（千瓦时）',
    },
    range_km: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '续航里程（公里）',
    },
    charge_time_h: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '充电时间（小时）',
    },
    // 尺寸重量
    length_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '车长（毫米）',
    },
    width_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '车宽（毫米）',
    },
    height_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '车高（毫米）',
    },
    wheelbase_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '轴距（毫米）',
    },
    curb_weight_kg: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '整备质量（公斤）',
    },
    trunk_capacity_l: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '后备箱容积（升）',
    },
    // 配置信息
    abs: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
      comment: 'ABS防抱死',
    },
    airbag_count: {
      type: DataTypes.INTEGER,
      allowNull: true,
      comment: '安全气囊数量',
    },
    smart_key: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
      comment: '智能钥匙',
    },
    display_type: {
      type: DataTypes.STRING(100),
      allowNull: true,
      comment: '仪表类型',
    },
    infotainment_size: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '中控屏尺寸（英寸）',
    },
    fuel_consumption: {
      type: DataTypes.STRING(100),
      allowNull: true,
      comment: '油耗',
    },
    // 系统字段
    description: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '车型描述',
    },
    features: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '主要特点',
    },
    colors: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '可选颜色',
    },
    image_url: {
      type: DataTypes.STRING(500),
      allowNull: true,
      comment: '主图片URL',
    },
    image_gallery: {
      type: DataTypes.TEXT,
      allowNull: true,
      comment: '图片集（JSON）',
    },
    rating: {
      type: DataTypes.FLOAT,
      allowNull: true,
      comment: '评分',
    },
    review_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
      comment: '评论数',
    },
    view_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
      comment: '浏览次数',
    },
    status: {
      type: DataTypes.STRING(50),
      allowNull: false,
      defaultValue: 'active',
      comment: '状态',
    },
    created_at: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    updated_at: {
      type: DataTypes.DATE,
      allowNull: false,
    },
  },
  {
    sequelize: dbConfig,
    tableName: 'cars',
    timestamps: true,
    underscored: false,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    indexes: [
      {
        name: 'idx_slug',
        unique: true,
        fields: ['slug'],
      },
      {
        name: 'idx_brand',
        fields: ['brand'],
      },
      {
        name: 'idx_category',
        fields: ['category'],
      },
      {
        name: 'idx_fuel_type',
        fields: ['fuel_type'],
      },
      {
        name: 'idx_year',
        fields: ['year'],
      },
      {
        name: 'idx_status',
        fields: ['status'],
      },
      {
        name: 'idx_brand_year',
        fields: ['brand', 'year'],
      },
    ],
  }
);

export default Car;

