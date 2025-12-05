import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: Number(process.env.PORT) || 4000,
  pythonEngineUrl: process.env.PYTHON_ENGINE_URL || 'http://python-engine:8000',
  databaseUrl: process.env.DATABASE_URL || 'postgres://nob:nob_password@postgres:5432/nob_universe'
};
