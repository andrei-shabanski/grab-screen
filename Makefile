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

cov-report:
	coverage xml
	coverage report

release: clean
	git tag -a $(APP_VERSION) -m "Release $(APP_VERSION)"
	git push origin $(APP_VERSION)
	python setup.py sdist bdist_wheel upload

# instagrations
codacy: cov-report
	python-codacy-coverage

coveralls: cov-report
	coveralls

codecov: cov-report
	codecov

codeclime-install:
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter

codeclime-pre-build:
	./cc-test-reporter before-build

codeclime: cov-report
	./cc-test-reporter after-build --exit-code $TRAVIS_TEST_RESULT; fi
