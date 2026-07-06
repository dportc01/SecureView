.PHONY: run frontend frontend-lint frontend-build backend backend-dev backend-test backend-test-cov backend-lint backend-clean

run:
	@echo "================ STARTING ALL SERVICES ================"
	$(MAKE) -j2 backend frontend
frontend:
	cd frontend/ && npm run dev
frontend-lint:
	cd frontend/ && npm run lint
frontend-build:
	cd frontend/ && npm run build
backend:
	cd backend/ && source .venv/bin/activate && python -m app.main
backend-test:
	cd backend/ && source .venv/bin/activate && pytest -s --log-cli-level=INFO
backend-test-cov:
	cd backend/ && source .venv/bin/activate && pytest --cov=app
backend-lint:
	cd backend/ && source .venv/bin/activate && flake8
backend-clean:
	find backend/ -type d -name "__pycache__" -exec rm -rf {} +
	find backend/ -type f -name "*.pyc" -delete
	find backend/ -type f -name ".coverage.*" -delete