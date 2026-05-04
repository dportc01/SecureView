.PHONY: run backend frontend

run:
	$(MAKE) -j2 backend frontend
frontend:
	cd frontend/ && npm run dev
backend:
	cd backend/ && source venv/bin/activate && python app/main.py
backend-test:
	cd backend/ && source venv/bin/activate && pytest
backend-lint:
	cd backend/ && source venv/bin/activate && flake8