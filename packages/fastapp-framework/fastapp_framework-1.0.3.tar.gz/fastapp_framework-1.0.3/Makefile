SRC_DIR = src

.PHONY: run, run_dev
run_dev:
	docker-compose -f docker-compose-dev.yml up --build
run:
	docker-compose up --build

.PHONY: install_dev
install_dev:
	pip install -e .

.PHONY: lint, mypy
lint:
	python -m pylint $(SRC_DIR)

mypy:
	python -m mypy $(SRC_DIR)