PYTHON=uv pip
APP_DIR=bot

run: ## Run the bot main script
	python -m $(APP_DIR).main

add-exchange: ## Run FastAPI app for adding exchanges
	uvicorn $(APP_DIR).exchange.add_exchange:app --reload

create-dcabot: ## Run FastAPI app for creating DCA bots
	uvicorn $(APP_DIR).dca_bot.create_dca_bot:app --reload

check: ## Run all checks
	make typecheck
	make format
	ruff check .

format: ## Format code using Ruff
	ruff format .

typecheck: ## Run mypy type checks
	mypy $(APP_DIR)

test: ## Run tests using pytest
	pytest tests/

install: ## Install dependencies using uv
	$(PYTHON) install -r requirements.txt

freeze: ## Freeze dependencies to requirements.txt
	$(PYTHON) freeze > requirements.txt

help: ## Show help for commands
	@echo "Makefile Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
