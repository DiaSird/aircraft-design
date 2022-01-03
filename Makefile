
default: start

rewrite-display:
				powershell -noprofile -File 'scripts/rewrite-display.ps1'

compose: rewrite-
				docker-compose up -d --build

run:
				poetry run python src/1st-sizing/sizeplt-gui.py

start:
				poetry run python src/main.py

lint:
				poetry run pysen run lint

lint-fix:
				poetry run pysen run format && \
				poetry run pysen run lint

test:
				poetry run pytest

install-dev:
				poetry config virtualenvs.in-project true
				poetry install

install:
				poetry config virtualenvs.in-project true
				poetry install --no-dev

clean:
				rm -rf  **/__pycache__ **/**/__pycache__ .venv


.PHONY: clean test
