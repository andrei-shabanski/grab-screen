VENV_PY = 2.7
VENV_DIR = .venv-$(VENV_PY)

APP_VERSION = $(shell python -m grab_screen -v)

clean:
	rm -rf build/ dist/ grab_screen.egg-info/
	find . -name '*.py[co]' -exec rm -f {} +

prune: clean
	rm -rf .venv-*/

lint:
	flake8
	bandit -r grab_screen/

test:
	pytest -q --durations=0

pip:
	pip install -r requirements/main.txt

pip-dev:
	pip install -r requirements/dev.txt

virtualenv:
	python -m virtualenv -p python$(VENV_PY) $(VENV_DIR)

release: clean
	git tag -a $(APP_VERSION) -m "Release $(APP_VERSION)"
	git push origin $(APP_VERSION)
	python setup.py sdist upload
	python setup.py bdist_wheel upload
