# Makefile

run:
	python -m bot.main

add-exchange:
	uvicorn bot.exchange.add_exchange:app --reload

create-dcabot:
	uvicorn bot.dca_bot.create_dca_bot:app --reload


check:
	make typecheck
	make format
	ruff check .

format:
	ruff format .

typecheck:
	mypy bot

test:
	pytest tests/

install:
	uv pip install -r requirements.txt

freeze:
	uv pip freeze > requirements.txt
