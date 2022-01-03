
default: start

img-build:
				docker build --pull --rm -f ".devcontainer/Dockerfile" -t aircraft-design:latest "."

build:
				powershell -noprofile -File 'scripts/img-build.ps1'

rebuild:
				docker rm aircraft-design
				make build

compose:
				powershell -noprofile -File 'scripts/rewrite-display.ps1'
				docker-compose up -d --build

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
