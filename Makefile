.PHONY: help install install-dev build clean test lint format

help:  ## Show this help message
	@echo "OpenAI Cost Tracker - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install the package
	pip install -e .

install-dev:  ## Install the package with development dependencies
	pip install -e ".[dev]"

build:  ## Build the package distribution
	python -m build

clean:  ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/

test:  ## Run tests
	python test_package.py

lint:  ## Run linting checks
	flake8 .
	mypy .

format:  ## Format code with black
	black .

dist: clean build  ## Create distribution packages
	@echo "Distribution packages created in dist/"

all: clean install-dev test  ## Clean, install dev dependencies, and test
