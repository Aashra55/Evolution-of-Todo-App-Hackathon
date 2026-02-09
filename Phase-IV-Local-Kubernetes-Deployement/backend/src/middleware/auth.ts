import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';

dotenv.config();

// Extend the Request type to include a user property
declare global {
  namespace Express {
    interface Request {
      user?: { userId: string; email: string };
    }
  }
}

const JWT_SECRET = process.env.JWT_SECRET || 'supersecretjwtkey'; // Fallback for development

const authenticateToken = (req: Request, res: Response, next: NextFunction) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

  if (token == null) {
    return res.status(401).json({ message: 'Authentication token required' });
  }

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) {
      return res.status(403).json({ message: 'Invalid or expired token' });
    }
    req.user = user as { userId: string; email: string };
    next();
  });
};

export default authenticateToken;
