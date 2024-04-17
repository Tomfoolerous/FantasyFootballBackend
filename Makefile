all: generate run 

generate:
	mkdir -p generated

run:
	python3 data/api_testing/afltables.py
	
clean:
	rm -rf generated
	python3 data/api_testing/afltables.py

run_cached: generate
	python3 data/get_cached_data.py