PYTHON := python3
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(PY) -m pip

# Module entrypoint (recommended)
ENTRY_MODULE := cli.main

# Storage
STORAGE_DIR ?= storage

# Output and logs
OUTDIR := output
LOGDIR := logs
TESTLOGDIR := $(LOGDIR)/test
RUNLOGDIR := $(LOGDIR)/run
LINTLOGDIR := $(LOGDIR)/lint

TIMESTAMP := $(shell date +"%Y%m%d_%H%M%S")

.PHONY: help venv install reinstall logs store run tui test lint pylint format clean

help:
	@echo "Targets:"
	@echo "  make install                 Create venv and install deps"
	@echo "  make reinstall               Recreate venv from scratch"
	@echo "  make store                   Create storage dir ($(STORAGE_DIR))"
	@echo "  make run ARGS='...'          Run CLI (logs saved). If ARGS is empty, runs interactive shell."
	@echo "  make tui                     Run TUI interface"
	@echo "  make test                    Run unit tests with unittest (logs saved)"
	@echo "  make lint                    Run flake8 checks (PEP8)"
	@echo "  make pylint                  Run pylint checks"
	@echo "  make format                  Auto-format with black"
	@echo "  make clean                   Clean environment and generated files"

venv:
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

reinstall:
	rm -rf $(VENV)
	$(MAKE) install

logs:
	mkdir -p $(TESTLOGDIR)
	mkdir -p $(RUNLOGDIR)
	mkdir -p $(LINTLOGDIR)

store:
	mkdir -p $(STORAGE_DIR)

# Usage:
#   make run ARGS="hotels create --id h1 --name 'Hotel A' --location City --total-rooms 3 --available-rooms 3"
#   make run ARGS="customers create --id c1 --name Alice --email alice@example.com"
#   make run ARGS="reservations create --customer-id c1 --hotel-id h1 --rooms 2"
#   make run                         # interactive mode (no ARGS)
run: install logs store
	mkdir -p $(OUTDIR)
	@set -e; \
	STDOUT="$(RUNLOGDIR)/run_$(TIMESTAMP).stdout.log"; \
	STDERR="$(RUNLOGDIR)/run_$(TIMESTAMP).stderr.log"; \
	echo "Running CLI: -m $(ENTRY_MODULE) $(ARGS)"; \
	set +e; \
	PYTHONPATH=src STORAGE_DIR="$(STORAGE_DIR)" $(PY) -m $(ENTRY_MODULE) $(ARGS) > $$STDOUT 2> $$STDERR; \
	EC=$$?; \
	set -e; \
	echo "Run logs:"; \
	echo "  $$STDOUT"; \
	echo "  $$STDERR"; \
	exit $$EC

tui: install store
	@echo "Running TUI: -m tui.main"; \
	PYTHONPATH=src STORAGE_DIR="$(STORAGE_DIR)" $(PY) -m tui.main

test: install logs
	@set -e; \
	STDOUT="$(TESTLOGDIR)/test_$(TIMESTAMP).stdout.log"; \
	STDERR="$(TESTLOGDIR)/test_$(TIMESTAMP).stderr.log"; \
	echo "Running unittest..."; \
	set +e; \
	PYTHONPATH=src STORAGE_DIR="$(STORAGE_DIR)" $(PY) -m unittest discover -s tests -p "test_*.py" -v > $$STDOUT 2> $$STDERR; \
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
	PYTHONPATH=src $(PY) -m flake8 src tests 1> $$STDOUT 2> $$STDERR; \
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
	PYTHONPATH=src $(PY) -m pylint src tests 1> $$STDOUT 2> $$STDERR; \
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
	rm -rf .coverage htmlcov
	# rm -rf $(STORAGE_DIR)
	find . -name "__pycache__" -type d -exec rm -rf {} +