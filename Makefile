.PHONY: run backend frontend clean-pyc

run:
	@echo "================ STARTING ALL SERVICES ================"
	$(MAKE) -j2 backend frontend
frontend:
	cd frontend/ && npm run dev
backend:
	cd backend/ && source venv/bin/activate && flask --app wsgi run
backend-test:
	cd backend/ && source venv/bin/activate && pytest
backend-lint:
	cd backend/ && source venv/bin/activate && flake8
clean-pycache:
	find backend/ -type d -name "__pycache__" -exec rm -rf {} +
	find backend/ -type f -name "*.pyc" -delete