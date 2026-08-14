P3 = python3.12
VENV = .venv
PIP = $(VENV)/bin/pip
P3_VENV = $(VENV)/bin/python3.12
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
RM = rm -rf
MAIN = main.py


all: run

install:
	$(P3) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:

	$(P3_VENV) $(MAIN)

debug:
	$(P3_VENV) -m pdp $(MAIN)

clean:
	$(RM) .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	clear

fclean:
	$(RM) $(VENV)

re:
	fclean install run

lint:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(FLAKE8) . --exclude $(VENV)
	$(MYPY) . --strict

.PHONY: all install run debug clean fclean re lint lint-strict