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

TIMESTAMP := $(shell date +"%Y%m%d_%H%M%S")

.PHONY: help venv install run test lint format clean logs

help:
	@echo "Targets:"
	@echo "  make install   Create venv and install deps"
	@echo "  make run       Run program (logs saved)"
	@echo "  make test      Run tests (logs saved)"
	@echo "  make clean     Clean environment"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

logs:
	mkdir -p $(TESTLOGDIR)
	mkdir -p $(RUNLOGDIR)

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

clean:
	rm -rf $(VENV)
	rm -rf $(OUTDIR)
	rm -rf $(LOGDIR)
	rm -rf .pytest_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +