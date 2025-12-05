.PHONY: help install-api build-api install-python lint-python install-web build-web docker-up docker-down docker-logs

help:
@echo "Available targets:"
@echo "  install-api     Install API server dependencies"
@echo "  build-api       Build the TypeScript API server"
@echo "  install-python  Install Python engine dependencies"
@echo "  install-web     Install web demo dependencies"
@echo "  build-web       Build the web demo"
@echo "  docker-up       Start all services via docker-compose"
@echo "  docker-down     Stop all services"
@echo "  docker-logs     Tail logs from docker-compose"

install-api:
cd api-server && npm install

build-api:
cd api-server && npm run build

install-python:
cd python-engine && pip install .

install-web:
cd web-demo && npm install

build-web:
cd web-demo && npm run build

docker-up:
docker-compose up --build

docker-down:
docker-compose down

docker-logs:
docker-compose logs -f
