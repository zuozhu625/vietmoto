import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

// 定义摩托车属性接口（匹配旧数据库实际结构）
export interface MotorcycleAttributes {
  id: number;
  brand: string;
  model: string;
  year: number;
  category: string;
  price_vnd: number;
  
  // 发动机系统
  engine_cc?: number;
  engine_type?: string;
  power_hp?: number;
  power_rpm?: number;
  torque_nm?: number;
  torque_rpm?: number;
  compression_ratio?: string;
  bore_stroke?: string;
  valve_system?: string;
  
  // 传动系统
  transmission?: string;
  clutch_type?: string;
  fuel_type?: string;
  fuel_supply?: string;
  starter?: string;
  ignition?: string;
  
  // 电动车参数
  battery_kwh?: number;
  range_km?: number;
  charge_time_h?: number;
  
  // 底盘系统
  frame_type?: string;
  front_suspension?: string;
  rear_suspension?: string;
  front_brake?: string;
  rear_brake?: string;
  front_tire?: string;
  rear_tire?: string;
  
  // 尺寸重量
  dimensions_mm?: string;
  wheelbase_mm?: number;
  ground_clearance_mm?: number;
  seat_height_mm?: number;
  weight_kg?: number;
  fuel_capacity_l?: number;
  
  // 配置信息
  abs: boolean;
  smart_key: boolean;
  display_type?: string;
  lighting?: string;
  features?: string;
  
  // 其他信息
  description?: string;
  warranty?: string;
  fuel_consumption?: string;
  colors?: string;
  image_url?: string;
  rating?: number;
  view_count: number;
  status: string;
  created_at: Date;
  updated_at: Date;
}

// 定义创建摩托车时的可选属性
interface MotorcycleCreationAttributes extends Optional<MotorcycleAttributes, 
  'id' | 'engine_cc' | 'engine_type' | 'power_hp' | 'power_rpm' | 'torque_nm' | 'torque_rpm' | 
  'compression_ratio' | 'bore_stroke' | 'valve_system' | 'transmission' | 'clutch_type' | 
  'fuel_type' | 'fuel_supply' | 'starter' | 'ignition' | 'battery_kwh' | 'range_km' | 
  'charge_time_h' | 'frame_type' | 'front_suspension' | 'rear_suspension' | 'front_brake' | 
  'rear_brake' | 'front_tire' | 'rear_tire' | 'dimensions_mm' | 'wheelbase_mm' | 
  'ground_clearance_mm' | 'seat_height_mm' | 'weight_kg' | 'fuel_capacity_l' | 
  'display_type' | 'lighting' | 'features' | 'description' | 'warranty' | 
  'fuel_consumption' | 'colors' | 'image_url' | 'rating' | 'view_count' | 'status' | 
  'created_at' | 'updated_at'> {}

// 定义Motorcycle模型类
class Motorcycle extends Model<MotorcycleAttributes, MotorcycleCreationAttributes> implements MotorcycleAttributes {
  public id!: number;
  public brand!: string;
  public model!: string;
  public year!: number;
  public category!: string;
  public price_vnd!: number;
  
  // 发动机系统
  public engine_cc?: number;
  public engine_type?: string;
  public power_hp?: number;
  public power_rpm?: number;
  public torque_nm?: number;
  public torque_rpm?: number;
  public compression_ratio?: string;
  public bore_stroke?: string;
  public valve_system?: string;
  
  // 传动系统
  public transmission?: string;
  public clutch_type?: string;
  public fuel_type?: string;
  public fuel_supply?: string;
  public starter?: string;
  public ignition?: string;
  
  // 电动车参数
  public battery_kwh?: number;
  public range_km?: number;
  public charge_time_h?: number;
  
  // 底盘系统
  public frame_type?: string;
  public front_suspension?: string;
  public rear_suspension?: string;
  public front_brake?: string;
  public rear_brake?: string;
  public front_tire?: string;
  public rear_tire?: string;
  
  // 尺寸重量
  public dimensions_mm?: string;
  public wheelbase_mm?: number;
  public ground_clearance_mm?: number;
  public seat_height_mm?: number;
  public weight_kg?: number;
  public fuel_capacity_l?: number;
  
  // 配置信息
  public abs!: boolean;
  public smart_key!: boolean;
  public display_type?: string;
  public lighting?: string;
  public features?: string;
  
  // 其他信息
  public description?: string;
  public warranty?: string;
  public fuel_consumption?: string;
  public colors?: string;
  public image_url?: string;
  public rating?: number;
  public view_count!: number;
  public status!: string;
  public created_at!: Date;
  public updated_at!: Date;
}

// 初始化模型
Motorcycle.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    brand: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    model: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    year: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    category: {
      type: DataTypes.STRING(255),
      allowNull: false,
    },
    price_vnd: {
      type: DataTypes.DECIMAL(12, 2),
      allowNull: false,
    },
    engine_cc: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    engine_type: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    power_hp: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    power_rpm: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    torque_nm: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    torque_rpm: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    compression_ratio: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    bore_stroke: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    valve_system: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    transmission: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    clutch_type: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    fuel_type: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    fuel_supply: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    starter: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    ignition: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    battery_kwh: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    range_km: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    charge_time_h: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    frame_type: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    front_suspension: {
      type: DataTypes.STRING(200),
      allowNull: true,
    },
    rear_suspension: {
      type: DataTypes.STRING(200),
      allowNull: true,
    },
    front_brake: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    rear_brake: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    front_tire: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    rear_tire: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    dimensions_mm: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    wheelbase_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    ground_clearance_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    seat_height_mm: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    weight_kg: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    fuel_capacity_l: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    abs: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    smart_key: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    display_type: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    lighting: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    features: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    warranty: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    fuel_consumption: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    colors: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    image_url: {
      type: DataTypes.STRING(255),
      allowNull: true,
    },
    rating: {
      type: DataTypes.FLOAT,
      allowNull: true,
    },
    view_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    status: {
      type: DataTypes.STRING(255),
      allowNull: false,
      defaultValue: 'active',
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
    tableName: 'motorcycles',
    timestamps: true,
    underscored: false,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
  }
);

export default Motorcycle;
