import dotenv from 'dotenv';

dotenv.config();

type Config = {
  port: number;
  databaseUrl: string;
  pythonEngineUrl: string;
};

const config: Config = {
  port: Number(process.env.PORT) || 4000,
  databaseUrl:
    process.env.DATABASE_URL || 'postgres://nob:nob_password@postgres:5432/nob_universe',
  pythonEngineUrl: process.env.PYTHON_ENGINE_URL || 'http://python-engine:8000',
};

export default config;
