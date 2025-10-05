.PHONY: help dev build deploy clean test k3s-deploy k3s-redeploy

help:
	@echo "Quality Playbook - Available Commands:"
	@echo "  make dev           - Start local development environment"
	@echo "  make build         - Build Docker images"
	@echo "  make deploy        - Deploy to GKE (requires kubectl/helm)"
	@echo "  make k3s-deploy    - Deploy to local k3s cluster"
	@echo "  make k3s-redeploy  - Quick redeploy to k3s (backend|frontend|all)"
	@echo "  make clean         - Clean up containers and volumes"
	@echo "  make test          - Run tests"

dev:
	docker-compose up

dev-backend:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

build:
	docker-compose build

deploy:
	@echo "Building and pushing images..."
	docker build -t gcr.io/$$GCP_PROJECT_ID/qualityplaybook-backend:latest ./backend
	docker build -t gcr.io/$$GCP_PROJECT_ID/qualityplaybook-frontend:latest ./frontend
	docker push gcr.io/$$GCP_PROJECT_ID/qualityplaybook-backend:latest
	docker push gcr.io/$$GCP_PROJECT_ID/qualityplaybook-frontend:latest
	@echo "Deploying to GKE..."
	helm upgrade --install qualityplaybook-backend ./helm/backend
	helm upgrade --install qualityplaybook-frontend ./helm/frontend

clean:
	docker-compose down -v
	rm -rf backend/__pycache__ backend/**/__pycache__
	rm -rf frontend/node_modules frontend/dist

test:
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm run test

install-backend:
	cd backend && uv sync

install-frontend:
	cd frontend && npm install

install: install-backend install-frontend

k3s-deploy:
	@echo "Deploying to local k3s cluster..."
	./scripts/k3s-deploy.sh

k3s-redeploy:
	@echo "Quick redeploy to k3s..."
	./scripts/k3s-redeploy.sh $(filter-out $@,$(MAKECMDGOALS))

%:
	@:
