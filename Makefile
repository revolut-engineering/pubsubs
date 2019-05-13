venv:
	virtualenv --python=python3 venv && pip install -e .

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

test: venv
	flake8 postoffice/ componennt-tests/
	pytest tests/
