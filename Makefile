VENV_PY = 2.7
VENV_DIR = .venv-$(VENV_PY)

APP_VERSION = $(shell python -m grab_screen -v)

clean:
	rm -rf build/ dist/ grab_screen.egg-info/
	find . -name '*.py[co]' -exec rm -f {} +

prune: clean
	rm -rf .venv-*/ coverage coverage.* coverage_html/ .eggs/ .cache/

pip:
	pip install -e .

pip-dev:
	pip install -e .[dev]

virtualenv:
	python -m virtualenv -p python$(VENV_PY) $(VENV_DIR)

lint:
	python setup.py lint

test:
	python setup.py test

codacy_coverage: test
	coverage xml
	python-codacy-coverage -r coverage.xml -c (`git rev-parse HEAD`)

release: clean
	git tag -a $(APP_VERSION) -m "Release $(APP_VERSION)"
	git push origin $(APP_VERSION)
	python setup.py sdist bdist_wheel upload
