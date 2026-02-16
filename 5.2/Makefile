PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

SRC := src/computeSales.py
PRICE := data/priceCatalogue.json
SALES := data/salesRecord.json

OUTDIR := output
LOGDIR := logs
TESTLOGDIR := $(LOGDIR)/test
RUNLOGDIR := $(LOGDIR)/run
LINTLOGDIR := $(LOGDIR)/lint

TIMESTAMP := $(shell date +"%Y%m%d_%H%M%S")

.PHONY: help venv install run test lint pylint format clean logs

help:
	@echo "Targets:"
	@echo "  make install   Create venv and install deps"
	@echo "  make run       Run program (logs saved)"
	@echo "  make test      Run tests (logs saved)"
	@echo "  make lint      Run flake8 checks (PEP8)"
	@echo "  make pylint    Run pylint checks"
	@echo "  make format    Auto-format with black"
	@echo "  make clean     Clean environment"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

logs:
	mkdir -p $(TESTLOGDIR)
	mkdir -p $(RUNLOGDIR)
	mkdir -p $(LINTLOGDIR)

run: install logs
	mkdir -p $(OUTDIR)
	PYTHONPATH=src $(PY) $(SRC) $(PRICE) $(SALES) \
		> $(RUNLOGDIR)/run_$(TIMESTAMP).stdout.log \
		2> $(RUNLOGDIR)/run_$(TIMESTAMP).stderr.log

test: install logs
	@set -e; \
	STDOUT="$(TESTLOGDIR)/test_$(TIMESTAMP).stdout.log"; \
	STDERR="$(TESTLOGDIR)/test_$(TIMESTAMP).stderr.log"; \
	echo "Running pytest..."; \
	set +e; \
	PYTHONPATH=src $(PY) -m pytest -vv 2> $$STDERR | tee $$STDOUT; \
	EC=$$?; \
	set -e; \
	echo "Test logs:"; \
	echo "  $$STDOUT"; \
	echo "  $$STDERR"; \
	exit $$EC

lint: install logs
	@set -e; \
	STDOUT="$(LINTLOGDIR)/flake8_$(TIMESTAMP).stdout.log"; \
	STDERR="$(LINTLOGDIR)/flake8_$(TIMESTAMP).stderr.log"; \
	echo "Running flake8..."; \
	set +e; \
	$(PY) -m flake8 src tests 2> $$STDERR | tee $$STDOUT; \
	EC=$$?; \
	set -e; \
	echo "Flake8 logs:"; \
	echo "  $$STDOUT"; \
	echo "  $$STDERR"; \
	exit $$EC

pylint: install logs
	@set -e; \
	STDOUT="$(LINTLOGDIR)/pylint_$(TIMESTAMP).stdout.log"; \
	STDERR="$(LINTLOGDIR)/pylint_$(TIMESTAMP).stderr.log"; \
	echo "Running pylint..."; \
	set +e; \
	PYTHONPATH=src $(PY) -m pylint src tests 2> $$STDERR | tee $$STDOUT; \
	EC=$$?; \
	set -e; \
	echo "Pylint logs:"; \
	echo "  $$STDOUT"; \
	echo "  $$STDERR"; \
	exit $$EC

format: install
	$(PY) -m black src tests

clean:
	rm -rf $(VENV)
	rm -rf $(OUTDIR)
	rm -rf $(LOGDIR)
	rm -rf .pytest_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +