# Makefile

run:
	python -m bot.main

add-exchange:
	python -m bot.exchange.run

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
