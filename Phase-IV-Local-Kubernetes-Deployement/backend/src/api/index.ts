import { Router } from 'express';
import authRouter from './auth';

const router = Router();

router.use('/users', authRouter); // Mount auth routes under /users

router.get('/status', (req, res) => {
  res.json({ status: 'API is running' });
});

// TODO: Add other API routes here

export default router;
