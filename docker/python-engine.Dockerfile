FROM python:3.11-slim
WORKDIR /app
COPY python-engine/pyproject.toml python-engine/setup.cfg python-engine/README.md ./
RUN pip install --no-cache-dir .
COPY python-engine/app ./app
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
