import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

// 定义新闻属性接口（匹配旧数据库实际结构）
export interface NewsAttributes {
  id: number;
  title: string;
  slug: string;
  content: string;
  summary?: string;
  excerpt?: string;
  featured_image?: string;
  category?: string;
  author_name?: string;
  status: string;
  is_featured: boolean;
  view_count: number;
  published_at?: Date;
  created_at: Date;
  updated_at: Date;
}

// 定义创建新闻时的可选属性
interface NewsCreationAttributes extends Optional<NewsAttributes, 'id' | 'slug' | 'summary' | 'excerpt' | 'featured_image' | 'category' | 'author_name' | 'status' | 'is_featured' | 'view_count' | 'published_at' | 'created_at' | 'updated_at'> {}

// 定义News模型类
class News extends Model<NewsAttributes, NewsCreationAttributes> implements NewsAttributes {
  public id!: number;
  public title!: string;
  public slug!: string;
  public content!: string;
  public summary?: string;
  public excerpt?: string;
  public featured_image?: string;
  public category?: string;
  public author_name?: string;
  public status!: string;
  public is_featured!: boolean;
  public view_count!: number;
  public published_at?: Date;
  public created_at!: Date;
  public updated_at!: Date;
}

// 初始化模型
News.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    title: {
      type: DataTypes.TEXT,
      allowNull: false,
      validate: {
        notEmpty: true,
      },
    },
    slug: {
      type: DataTypes.TEXT,
      allowNull: false,
      unique: true,
      validate: {
        notEmpty: true,
      },
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    summary: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    excerpt: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    featured_image: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    category: {
      type: DataTypes.TEXT,
      allowNull: true,
      defaultValue: 'Tin tức',
    },
    author_name: {
      type: DataTypes.TEXT,
      allowNull: true,
      defaultValue: 'Ban biên tập',
    },
    status: {
      type: DataTypes.TEXT,
      allowNull: false,
      defaultValue: 'published',
    },
    is_featured: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false,
    },
    view_count: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    published_at: {
      type: DataTypes.DATE,
      allowNull: true,
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
    tableName: 'news',
    timestamps: true,
    underscored: false,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
    indexes: [
      {
        fields: ['status'],
      },
      {
        fields: ['category'],
      },
      {
        fields: ['is_featured'],
      },
      {
        fields: ['published_at'],
      },
      {
        fields: ['slug'],
        unique: true,
      },
    ],
  }
);

export default News;
