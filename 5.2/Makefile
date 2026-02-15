PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

SRC := src/computeSales.py
PRICE := data/priceCatalogue.json
SALES := data/salesRecord.json
OUTDIR := output
OUTFILE := $(OUTDIR)/SalesResults.txt

.PHONY: help venv install run test lint format clean

help:
	@echo "Targets:"
	@echo "  make venv      Create virtual environment"
	@echo "  make install   Install dependencies"
	@echo "  make run       Run computeSales with data files"
	@echo "  make test      Run tests"
	@echo "  make lint      Run PEP8 checks (flake8)"
	@echo "  make format    Auto-format (black)"
	@echo "  make clean     Remove generated files and venv"

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	mkdir -p $(OUTDIR)
	$(PY) $(SRC) $(PRICE) $(SALES)

test:
	$(PY) -m pytest -q

lint:
	$(PY) -m flake8 src tests

format:
	$(PY) -m black src tests

clean:
	rm -rf $(VENV)
	rm -rf $(OUTDIR)
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -name "__pycache__" -type d -exec rm -rf {} +