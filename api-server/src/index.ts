import cors from 'cors';
import express, { Request, Response } from 'express';
import morgan from 'morgan';
import config from './config';
import { errorHandler } from './middleware/errorHandler';
import { patternsRouter } from './routes/patterns';

const app = express();

app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

app.use('/api/patterns', patternsRouter);

app.use(errorHandler);

app.listen(config.port, () => {
  // eslint-disable-next-line no-console
  console.log(`API server listening on port ${config.port}`);
});
