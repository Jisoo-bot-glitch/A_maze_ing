PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

all : run

run :
	$(PYTHON) $(MAIN) $(CONFIG)

install : 
	$(PYTHON) -m pip install flake8 mypy build

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean : 
	rm -rf .mypy_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name ".DS_Store" -type f -delete

lint: 
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: 
	flake8 .
	mypy . --strict

.PHONY: all run install debug clean lint lint-strict