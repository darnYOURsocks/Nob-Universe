import { Router } from 'express';
import config from '../config';

type Pattern = {
  id: string;
  name: string;
  description: string;
};

const patterns: Pattern[] = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    name: 'Spiral',
    description: 'A classic logarithmic spiral pattern.',
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    name: 'Grid',
    description: 'Aligned rectangular grid useful for experiments.',
  },
  {
    id: '33333333-3333-3333-3333-333333333333',
    name: 'Wave',
    description: 'Sine wave-based spatial variation.',
  },
];

export const patternsRouter = Router();

patternsRouter.get('/', async (_req, res) => {
  res.json({
    source: 'api-server',
    pythonEngineUrl: config.pythonEngineUrl,
    patterns,
  });
});
