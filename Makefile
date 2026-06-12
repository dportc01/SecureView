.PHONY: run backend frontend

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