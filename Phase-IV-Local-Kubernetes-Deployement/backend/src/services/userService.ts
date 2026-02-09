import pool from '../config/database';
import { User } from '../models/user';
import bcrypt from 'bcrypt';
import { v4 as uuidv4 } from 'uuid';

export class UserService {
  private static readonly TABLE_NAME = 'users';

  public static async createUser(userData: Omit<User, 'id' | 'created_at' | 'updated_at'>): Promise<User> {
    const { username, email, password_hash } = userData;

    // Hash the password
    const hashedPassword = await bcrypt.hash(password_hash, 10);
    const id = uuidv4();
    const now = new Date();

    const query = `
      INSERT INTO ${UserService.TABLE_NAME} (id, username, email, password_hash, created_at, updated_at)
      VALUES ($1, $2, $3, $4, $5, $6)
      RETURNING id, username, email, created_at, updated_at;
    `;
    const values = [id, username, email, hashedPassword, now, now];

    try {
      const result = await pool.query(query, values);
      return result.rows[0];
    } catch (error) {
      if (error.code === '23505') { // Unique violation
        if (error.detail.includes('username')) {
          throw new Error('Username already exists');
        }
        if (error.detail.includes('email')) {
          throw new Error('Email already exists');
        }
      }
      throw error;
    }
  }

  public static async findUserByEmail(email: string): Promise<User | undefined> {
    const query = `
      SELECT id, username, email, password_hash, created_at, updated_at FROM ${UserService.TABLE_NAME}
      WHERE email = $1;
    `;
    const result = await pool.query(query, [email]);
    return result.rows[0];
  }

  public static async findUserById(id: string): Promise<User | undefined> {
    const query = `
      SELECT id, username, email, password_hash, created_at, updated_at FROM ${UserService.TABLE_NAME}
      WHERE id = $1;
    `;
    const result = await pool.query(query, [id]);
    return result.rows[0];
  }
}
