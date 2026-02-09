# ============================================
# Makefile - Actividad 4.2
# Root: 4.2/
# ============================================

PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

P1 := P1
P2 := P2
P3 := P3

.DEFAULT_GOAL := help

# --------------------------------------------------
# Evidence of Execution (P1)
#
# Commands executed from 4.2/ root:
#
# 1) Run all P1 test cases and generate final results file:
#    make run-p1-all
#
#    Final results file:
#    P1/results/StatisticsResults.txt
#
#    Execution logs (per TC, timestamped):
#    P1/logs/TC*_YYYYMMDD_HHMMSS.stdout.log
#    P1/logs/TC*_YYYYMMDD_HHMMSS.stderr.log
#
# 2) Run unit tests and save output to log:
#    make test-p1-log
#
#    Test evidence:
#    P1/test_logs/test_P1_<timestamp>.log
#
# --------------------------------------------------

# --------------------------------------------
# Environment
# --------------------------------------------

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# --------------------------------------------
# Helpers
# --------------------------------------------

define REQUIRE_TC
	@if [ -z "$(TC)" ]; then \
		echo "Usage: make $(1) TC=TC1"; \
		exit 1; \
	fi
endef



# --------------------------------------------
# Run single test case (with logs timestamp)
# --------------------------------------------

run-p1: install
	$(call REQUIRE_TC,run-p1)
	@mkdir -p $(P1)/logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	cd $(P1)/source && ../../$(PY) computeStatistics.py ../data/$(TC).txt \
	> ../../$(P1)/logs/$(TC)_$$TS.stdout.log \
	2> ../../$(P1)/logs/$(TC)_$$TS.stderr.log
	@if [ ! -f "$(P1)/results/StatisticsResults.txt" ]; then \
		echo "ERROR: $(P1)/results/StatisticsResults.txt was not generated."; \
		exit 1; \
	fi
	@echo "Saved evidence at $(P1)/results/StatisticsResults.txt"
	@echo "Logs saved at $(P1)/logs/ (stdout/stderr with timestamp)"

run-p2: install
	$(call REQUIRE_TC,run-p2)
	@mkdir -p $(P2)/logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	cd $(P2)/source && ../../$(PY) convertNumbers.py ../data/$(TC).txt \
	> ../../$(P2)/logs/$(TC)_$$TS.stdout.log \
	2> ../../$(P2)/logs/$(TC)_$$TS.stderr.log
	@if [ ! -f "$(P2)/results/ConvertionResults.txt" ]; then \
		echo "ERROR: $(P2)/results/ConvertionResults.txt was not generated."; \
		exit 1; \
	fi
	cp -f $(P2)/results/ConvertionResults.txt $(P2)/results/$(TC).Results.txt
	@echo "Saved evidence at $(P2)/results/$(TC).Results.txt"
	@echo "Logs saved at $(P2)/logs/ (stdout/stderr with timestamp)"

run-p3: install
	$(call REQUIRE_TC,run-p3)
	@mkdir -p $(P3)/logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	cd $(P3)/source && ../../$(PY) wordCount.py ../data/$(TC).txt \
	> ../../$(P3)/logs/$(TC)_$$TS.stdout.log \
	2> ../../$(P3)/logs/$(TC)_$$TS.stderr.log
	@if [ ! -f "$(P3)/results/WordCountResults.txt" ]; then \
		echo "ERROR: $(P3)/results/WordCountResults.txt was not generated."; \
		exit 1; \
	fi
	cp -f $(P3)/results/WordCountResults.txt $(P3)/results/$(TC).Results.txt
	@echo "Saved evidence at $(P3)/results/$(TC).Results.txt"
	@echo "Logs saved at $(P3)/logs/ (stdout/stderr with timestamp)"

# --------------------------------------------
# Run all test cases
# --------------------------------------------

run-p1-all: install
	@for f in $(P1)/data/TC*.txt; do \
		tc=$$(basename $$f .txt); \
		echo "Running P1 $$tc"; \
		$(MAKE) run-p1 TC=$$tc; \
	done

run-p2-all: install
	@for f in $(P2)/data/TC*.txt; do \
		tc=$$(basename $$f .txt); \
		echo "Running P2 $$tc"; \
		$(MAKE) run-p2 TC=$$tc; \
	done

run-p3-all: install
	@for f in $(P3)/data/TC*.txt; do \
		tc=$$(basename $$f .txt); \
		echo "Running P3 $$tc"; \
		$(MAKE) run-p3 TC=$$tc; \
	done

run-all: run-p1-all run-p2-all run-p3-all

# --------------------------------------------
# Tests (with correct PYTHONPATH)
# --------------------------------------------

test-p1: install
	PYTHONPATH=$(P1)/source $(PY) -m pytest $(P1)/tests/test_statistics.py -v

test-p2: install
	PYTHONPATH=$(P2)/source $(PY) -m pytest $(P2)/tests/test_converter.py -v

test-p3: install
	PYTHONPATH=$(P3)/source $(PY) -m pytest $(P3)/tests/test_wordcount.py -v

test: test-p1 test-p2 test-p3

# --------------------------------------------
# Test logs (pytest output saved with timestamp)
# --------------------------------------------

test-p1-log: install
	@mkdir -p $(P1)/test_logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	PYTHONPATH=$(P1)/source $(PY) -m pytest $(P1)/tests/test_statistics.py -v \
	> $(P1)/test_logs/test_P1_$$TS.log 2>&1
	@echo "Test log saved at $(P1)/test_logs/"

test-p2-log: install
	@mkdir -p $(P2)/test_logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	PYTHONPATH=$(P2)/source $(PY) -m pytest $(P2)/tests/test_converter.py -v \
	> $(P2)/test_logs/test_P2_$$TS.log 2>&1
	@echo "Test log saved at $(P2)/test_logs/"

test-p3-log: install
	@mkdir -p $(P3)/test_logs
	@TS=$$(date +"%Y%m%d_%H%M%S"); \
	PYTHONPATH=$(P3)/source $(PY) -m pytest $(P3)/tests/test_wordcount.py -v \
	> $(P3)/test_logs/test_P3_$$TS.log 2>&1
	@echo "Test log saved at $(P3)/test_logs/"

test-all-log: test-p1-log test-p2-log test-p3-log

# --------------------------------------------
# Lint
# --------------------------------------------

lint: install lint-run

lint-run:
	$(PY) -m pylint $(P1) $(P2) $(P3)

lint-run:
	PYTHONPATH=$(P1)/source $(PY) -m pylint $(P1)/source $(P1)/tests
	PYTHONPATH=$(P2)/source $(PY) -m pylint $(P2)/source $(P2)/tests
	PYTHONPATH=$(P3)/source $(PY) -m pylint $(P3)/source $(P3)/tests

# --------------------------------------------
# Clean
# --------------------------------------------

clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-results:
	rm -f $(P1)/results/*.Results.txt $(P1)/results/StatisticsResults.txt
	rm -f $(P2)/results/*.Results.txt $(P2)/results/ConvertionResults.txt
	rm -f $(P3)/results/*.Results.txt $(P3)/results/WordCountResults.txt

clean-logs:
	rm -f $(P1)/logs/*.log
	rm -f $(P2)/logs/*.log
	rm -f $(P3)/logs/*.log

clean-test-logs:
	rm -f $(P1)/test_logs/*.log
	rm -f $(P2)/test_logs/*.log
	rm -f $(P3)/test_logs/*.log

# --------------------------------------------
# Pipeline
# --------------------------------------------

all: install test lint

help:
	@echo "Available commands (run from 4.2/):"
	@echo ""
	@echo " Setup:"
	@echo "   make install                -> Create venv + install dependencies"
	@echo ""
	@echo " Run single test case (logs timestamp):"
	@echo "   make run-p1 TC=TC1"
	@echo "   make run-p2 TC=TC1"
	@echo "   make run-p3 TC=TC1"
	@echo ""
	@echo " Run all test cases:"
	@echo "   make run-p1-all"
	@echo "   make run-p2-all"
	@echo "   make run-p3-all"
	@echo "   make run-all"
	@echo ""
	@echo " Tests:"
	@echo "   make test                   -> Run all tests (P1+P2+P3)"
	@echo "   make test-p1                -> Run P1 tests"
	@echo "   make test-p2                -> Run P2 tests"
	@echo "   make test-p3                -> Run P3 tests"
	@echo ""
	@echo " Tests with logs:"
	@echo "   make test-p1-log"
	@echo "   make test-p2-log"
	@echo "   make test-p3-log"
	@echo "   make test-all-log"
	@echo ""
	@echo " Lint:"
	@echo "   make lint"
	@echo ""
	@echo " Clean:"
	@echo "   make clean"
	@echo "   make clean-results"
	@echo "   make clean-logs"
	@echo "   make clean-test-logs"
	@echo ""
	@echo " Pipeline:"
	@echo "   make all"