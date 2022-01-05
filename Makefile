default: start

# --------------------------------------------------------------------------------------------------
# Docker compose settings
# --------------------------------------------------------------------------------------------------
# For Windows11 + WSL + WSLg(https://github.com/microsoft/wslg)
compose-wsl:
				bash './scripts/set-wslg.sh'

# For Windows10(11) + X server(https://sourceforge.net/projects/vcxsrv/files/)
compose-x:
				powershell -noprofile -File 'scripts/set-xserver.ps1'

compose: compose-wsl
				bash docker-compose -f docker-compose.yml up -d

# --------------------------------------------------------------------------------------------------
# In container command
# --------------------------------------------------------------------------------------------------

start:
				poetry run python src/1st-sizing/sizeplt-gui.py

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
				rm -rf  **/__pycache__ **/**/__pycache__ .venv ./docker/.env


tree:
				powershell -noprofile -File 'scripts/tree.ps1'

.PHONY: clean test
