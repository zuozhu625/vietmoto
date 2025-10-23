import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

interface QuestionAttributes {
  id: number;
  title: string;
  content: string;
  category: string;
  subcategory?: string;
  vehicle_type: 'motorcycle' | 'car';
  vehicle_id?: number;
  author_id: string;
  view_count: number;
  votes_count: number;
  answers_count: number;
  has_accepted_answer: boolean;
  status: string;
  created_at: Date;
  updated_at: Date;
}

interface QuestionCreationAttributes extends Optional<QuestionAttributes, 'id' | 'subcategory' | 'vehicle_id' | 'view_count' | 'votes_count' | 'answers_count' | 'has_accepted_answer' | 'status' | 'created_at' | 'updated_at'> {}

class Question extends Model<QuestionAttributes, QuestionCreationAttributes> implements QuestionAttributes {
  public id!: number;
  public title!: string;
  public content!: string;
  public category!: string;
  public subcategory?: string;
  public vehicle_type!: 'motorcycle' | 'car';
  public vehicle_id?: number;
  public author_id!: string;
  public view_count!: number;
  public votes_count!: number;
  public answers_count!: number;
  public has_accepted_answer!: boolean;
  public status!: string;
  public readonly created_at!: Date;
  public readonly updated_at!: Date;
}

Question.init(
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
    category: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    subcategory: {
      type: DataTypes.TEXT,
      allowNull: true,
    },
    vehicle_type: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    vehicle_id: {
      type: DataTypes.INTEGER,
      allowNull: true,
    },
    author_id: {
      type: DataTypes.TEXT,
      allowNull: false,
      defaultValue: 'system',
    },
    view_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    votes_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    answers_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    has_accepted_answer: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    status: {
      type: DataTypes.TEXT,
      defaultValue: 'open',
    },
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
    tableName: 'questions',
    timestamps: true,
    underscored: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
  }
);

export default Question;
export type { QuestionAttributes, QuestionCreationAttributes };

