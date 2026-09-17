install:
	pip install -r requirements.txt

test:
	pytest -q

generate:
	python scripts/generate_events.py --count 10000 --output data/raw/events.jsonl

spark:
	python scripts/run_spark_job.py

format:
	python -m compileall services src spark_jobs scripts
