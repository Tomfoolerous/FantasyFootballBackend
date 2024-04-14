all: generate run

generate:
	mkdir -p generated

run:
	python3 data/api_testing/afltables.py