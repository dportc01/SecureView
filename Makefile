.PHONY: run frontend frontend-lint backend-dev backend-test backend-lint backend-clean

run:
	@echo "================ STARTING ALL SERVICES ================"
	$(MAKE) -j2 backend-dev frontend
frontend:
	cd frontend/ && npm run dev
frontend-lint:
	cd frontend/ && npm run lint
backend-dev:
	cd backend/ && source .venv/bin/activate && python -m app.main
backend-test:
	cd backend/ && source .venv/bin/activate && pytest -s --log-cli-level=INFO
backend-lint:
	cd backend/ && source .venv/bin/activate && flake8
backend-clean:
	find backend/ -type d -name "__pycache__" -exec rm -rf {} +
	find backend/ -type f -name "*.pyc" -delete