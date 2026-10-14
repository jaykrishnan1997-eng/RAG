UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")
PYTHON := python

# Cross - platform defaults (used on machine with or without goinfre)
VENV := .venv
UV_CACHE_DIR := $(shell uv cache dir 2>/dev/null || echo "$(HOME)/.cache/uv")
HF_HOME := $(HOME)/.cache/huggingface

# Override with goinfre paths on 42 campus machines
ifneq ($(wildcard /goinfre/.),)
VENV := /goinfre/$(USER)/ram-venv
UV_CACHE_DIR := /goinfre/$(USER)/uv-cache
HF_HOME := /goinfre/$(USER)/hf-cache
endif

export UV_CACHE_DIR
export HF_HOME
export UV_PROJECT_ENVIRONMENT := $(VENV)

.PHONY: install run debug clean fclean lint lint-strict purge

install:
	@if [ ! -x "$(UV)" ]; then \
		echo "uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi
	@if [ ! -x "$(UV)" ]; then \
		echo "Error: uv installation failed."; \
		exit 1; \
	fi
	mkdir -p "$(UV_CACHE_DIR)" "$(HF_HOME)"
	$(UV) sync
	@echo "Virtual environment ready: $(VENV)"
	@echo "Run: source $(VENV)/bin/activate";

run: install
	$(UV) run $(PYTHON) -m src

debug: install
	$(UV) run $(PYTHON) -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf data/output

fclean: clean
	rm -rf $(VENV)

purge: fclean
	rm -rf "$(UV_CACHE_DIR)"
	rm -rf "$(HF_HOME)"

lint: install
	$(UV) run flake8 . --exclude=.venv,venv,raw
	$(UV) run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	$(UV) run flake8 . --exclude=.venv,venv,raw
	$(UV) run mypy . --strict