
LATEST = $(shell ls -1t dist/orthophotomosaictiles-*.tar.gz | head -n 1)
VERSION = $(shell python3 setup.py --version)

all:
	$(MAKE) clean
	$(MAKE) build
	$(MAKE) install
	$(MAKE) show

build:
	python3 setup.py sdist bdist_wheel

install:
	python3 -m pip -v install $(LATEST)

show:
	python3 -m pip show orthophotomosaictiles

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf {,*/}__pycache__

versionbump:
	bumpversion --tag --commit --current-version $(VERSION) patch setup.py orthophotomosaictiles/version.py
	git push

.PHONY: all build clean

