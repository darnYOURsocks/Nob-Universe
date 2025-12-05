import { ErrorRequestHandler, NextFunction, Request, Response } from 'express';

type HttpError = Error & {
  status?: number;
};

export const errorHandler: ErrorRequestHandler = (
  err: HttpError,
  _req: Request,
  res: Response,
  _next: NextFunction,
) => {
  const status = err.status || 500;
  const message = err.message || 'Internal server error';

  // eslint-disable-next-line no-console
  console.error(err);

  res.status(status).json({ message });
};
