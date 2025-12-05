import { Router } from 'express';
import { config } from '../config/index.js';

const router = Router();

router.get('/', (_req, res) => {
  res.json({
    status: 'ok',
    pythonEngine: config.pythonEngineUrl,
    patterns: [
      { id: 1, name: 'Recognition', description: 'Detects input patterns.' },
      { id: 2, name: 'Integration', description: 'Combines signals harmonically.' },
      { id: 3, name: 'Propagation', description: 'Broadcasts coherent patterns.' }
    ]
  });
});

router.post('/analyze', async (req, res, next) => {
  try {
    const response = await fetch(`${config.pythonEngineUrl}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body || {})
    });
    const payload = await response.json();
    res.json(payload);
  } catch (error) {
    next(error);
  }
});

export default router;
