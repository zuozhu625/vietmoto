/**
 * 二手车辆模型
 */

import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

export interface MarketplaceVehicleAttributes {
  id: number;
  external_id: string;
  external_url?: string;
  source: string;
  type: string;
  vehicle_type: string; // moto-gas, moto-electric, car-gas, car-electric
  brand?: string;
  model?: string;
  year?: number;
  price: number;
  title: string;
  description?: string;
  mileage?: number;
  condition_text?: string;
  condition_rating?: number;
  image_url?: string;
  images?: string;
  city?: string;
  district?: string;
  ward?: string;
  location?: string;
  seller_name?: string;
  seller_id?: string;
  seller_avatar?: string;
  seller_phone?: string;
  seller_rating?: number;
  seller_sold_count?: number;
  view_count: number;
  favorites_count: number;
  status: string;
  is_featured: boolean;
  published_at?: Date;
  created_at: Date;
  updated_at: Date;
}

interface MarketplaceVehicleCreationAttributes
  extends Optional<MarketplaceVehicleAttributes, 'id' | 'created_at' | 'updated_at'> {}

class MarketplaceVehicle
  extends Model<MarketplaceVehicleAttributes, MarketplaceVehicleCreationAttributes>
  implements MarketplaceVehicleAttributes
{
  public id!: number;
  public external_id!: string;
  public external_url?: string;
  public source!: string;
  public type!: string;
  public vehicle_type!: string;
  public brand?: string;
  public model?: string;
  public year?: number;
  public price!: number;
  public title!: string;
  public description?: string;
  public mileage?: number;
  public condition_text?: string;
  public condition_rating?: number;
  public image_url?: string;
  public images?: string;
  public city?: string;
  public district?: string;
  public ward?: string;
  public location?: string;
  public seller_name?: string;
  public seller_id?: string;
  public seller_avatar?: string;
  public seller_phone?: string;
  public seller_rating?: number;
  public seller_sold_count?: number;
  public view_count!: number;
  public favorites_count!: number;
  public status!: string;
  public is_featured!: boolean;
  public published_at?: Date;
  public readonly created_at!: Date;
  public readonly updated_at!: Date;
}

MarketplaceVehicle.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    external_id: {
      type: DataTypes.TEXT,
      unique: true,
      allowNull: false,
    },
    external_url: {
      type: DataTypes.TEXT,
    },
    source: {
      type: DataTypes.TEXT,
      defaultValue: 'chotot',
    },
    type: {
      type: DataTypes.TEXT,
      defaultValue: 'motorcycle',
    },
    vehicle_type: {
      type: DataTypes.TEXT,
      defaultValue: 'moto-gas',
    },
    brand: DataTypes.TEXT,
    model: DataTypes.TEXT,
    year: DataTypes.INTEGER,
    price: {
      type: DataTypes.REAL,
      allowNull: false,
    },
    title: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    description: DataTypes.TEXT,
    mileage: DataTypes.INTEGER,
    condition_text: DataTypes.TEXT,
    condition_rating: DataTypes.INTEGER,
    image_url: DataTypes.TEXT,
    images: DataTypes.TEXT, // JSON string
    city: DataTypes.TEXT,
    district: DataTypes.TEXT,
    ward: DataTypes.TEXT,
    location: DataTypes.TEXT,
    seller_name: DataTypes.TEXT,
    seller_id: DataTypes.TEXT,
    seller_avatar: DataTypes.TEXT,
    seller_phone: DataTypes.TEXT,
    seller_rating: DataTypes.REAL,
    seller_sold_count: DataTypes.INTEGER,
    view_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    favorites_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    status: {
      type: DataTypes.TEXT,
      defaultValue: 'active',
    },
    is_featured: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    published_at: DataTypes.DATE,
    created_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
    updated_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
    },
  },
  {
    sequelize: dbConfig,
    tableName: 'marketplace_vehicles',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
  }
);

export default MarketplaceVehicle;

