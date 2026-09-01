.PHONY: install backend-install frontend-install run frontend frontend-lint frontend-build backend backend-dev backend-test backend-test-cov backend-lint backend-clean

PYTHON ?= python3

install: backend-install frontend-install

backend-install:
	@echo "Building python virtual enviroment..."
	@if ! $(PYTHON) -m venv --help >/dev/null 2>&1; then \
		echo "Python venv is required to create the virtual enviroment, please install it"; \
		exit 1; \
	fi
	cd backend && $(PYTHON) -m venv .venv
	backend/.venv/bin/python -m pip install --upgrade pip
	backend/.venv/bin/python -m pip install -r backend/requirements.txt

frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

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
	find backend/ -type f -name ".coverage" -delete