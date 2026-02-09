import express from 'express';
import apiRouter from './api';
import errorHandler from './middleware/errorHandler';

const app = express();
app.use(express.json());

app.use('/api/v1', apiRouter);

// Error handling middleware (must be last)
app.use(errorHandler);

export default app;
