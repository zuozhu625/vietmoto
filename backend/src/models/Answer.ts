import { DataTypes, Model, Optional } from 'sequelize';
import { dbConfig } from '../config/database';

interface AnswerAttributes {
  id: number;
  question_id: number;
  content: string;
  author_id: string;
  votes_count: number;
  is_accepted: boolean;
  created_at: Date;
  updated_at: Date;
}

interface AnswerCreationAttributes extends Optional<AnswerAttributes, 'id' | 'votes_count' | 'is_accepted' | 'created_at' | 'updated_at'> {}

class Answer extends Model<AnswerAttributes, AnswerCreationAttributes> implements AnswerAttributes {
  public id!: number;
  public question_id!: number;
  public content!: string;
  public author_id!: string;
  public votes_count!: number;
  public is_accepted!: boolean;
  public readonly created_at!: Date;
  public readonly updated_at!: Date;
}

Answer.init(
  {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true,
    },
    question_id: {
      type: DataTypes.INTEGER,
      allowNull: false,
    },
    content: {
      type: DataTypes.TEXT,
      allowNull: false,
    },
    author_id: {
      type: DataTypes.TEXT,
      allowNull: false,
      defaultValue: 'system',
    },
    votes_count: {
      type: DataTypes.INTEGER,
      defaultValue: 0,
    },
    is_accepted: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
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
    tableName: 'answers',
    timestamps: true,
    underscored: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at',
  }
);

export default Answer;
export type { AnswerAttributes, AnswerCreationAttributes };

