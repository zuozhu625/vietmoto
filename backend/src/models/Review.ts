import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

interface ReviewAttributes {
  id: number;
  title: string;
  content: string;
  excerpt: string;
  vehicle_id: number;
  vehicle_type: 'motorcycle' | 'car';
  author_name: string;
  author_profile?: string;
  rating?: number;
  usage_duration?: string;
  usage_scenario?: string;
  pros?: string;
  cons?: string;
  view_count: number;
  like_count: number;
  status: string;
  created_at: Date;
  updated_at: Date;
}

interface ReviewCreationAttributes extends Optional<ReviewAttributes, 
  'id' | 'created_at' | 'updated_at' | 'author_profile' | 'rating' | 
  'usage_duration' | 'usage_scenario' | 'pros' | 'cons' | 'view_count' | 'like_count' | 'status'> {}

export class Review extends Model<ReviewAttributes, ReviewCreationAttributes> implements ReviewAttributes {
  public id!: number;
  public title!: string;
  public content!: string;
  public excerpt!: string;
  public vehicle_id!: number;
  public vehicle_type!: 'motorcycle' | 'car';
  public author_name!: string;
  public author_profile?: string;
  public rating?: number;
  public usage_duration?: string;
  public usage_scenario?: string;
  public pros?: string;
  public cons?: string;
  public view_count!: number;
  public like_count!: number;
  public status!: string;
  public created_at!: Date;
  public updated_at!: Date;
}

Review.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    title: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    excerpt: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    vehicle_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    vehicle_type: {
      type: DataTypes.TEXT,
      allowNull: false,
      validate: {
        isIn: [['motorcycle', 'car']],
      },
    },
    author_name: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    author_profile: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    rating: {
      type: DataTypes.INTEGER,
      allowNull: true,
      validate: {
        min: 1,
        max: 5,
      },
    },
    usage_duration: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    usage_scenario: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    pros: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    cons: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    view_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    like_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    status: {
      type: DataTypes.TEXT,
      allowNull: false,
      defaultValue: 'published',
      validate: {
        isIn: [['published', 'draft', 'deleted']],
      },
    },
    created_at: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW,
    },
    updated_at: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW,
    },
  },
  {
    sequelize: dbConfig,
    tableName: 'reviews',
    timestamps: true,
    underscored: true,
    hooks: {
      beforeUpdate: (review: Review) => {
        review.updated_at = new Date();
      },
    },
  }
);

export default Review;

