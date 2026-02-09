import { Router } from 'express';
import { UserService } from '../services/userService';
import { User } from '../models/user';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config();

const authRouter = Router();

// Ensure JWT_SECRET is defined
const JWT_SECRET = process.env.JWT_SECRET || 'supersecretjwtkey'; // Fallback for development

authRouter.post('/register', async (req, res, next) => {
  try {
    const { username, email, password } = req.body;

    if (!username || !email || !password) {
      return res.status(400).json({ message: 'Missing required fields' });
    }

    const newUser: Omit<User, 'id' | 'created_at' | 'updated_at'> = {
      username,
      email,
      password_hash: password, // password will be hashed inside UserService
    };

    const createdUser = await UserService.createUser(newUser);
    // Exclude password_hash from the response for security
    const { password_hash, ...userResponse } = createdUser;
    res.status(201).json(userResponse);
  } catch (error: any) {
    next(error); // Pass errors to the central error handler
  }
});

authRouter.post('/login', async (req, res, next) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: 'Missing email or password' });
    }

    const user = await UserService.findUserByEmail(email);
    if (!user) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    const isPasswordValid = await bcrypt.compare(password, user.password_hash);
    if (!isPasswordValid) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    const token = jwt.sign({ userId: user.id, email: user.email }, JWT_SECRET, { expiresIn: '1h' });

    res.status(200).json({ token });
  } catch (error: any) {
    next(error);
  }
});

export default authRouter;
