.PHONY: test install

test:
	python -m unittest -v

install:
	python setup.py install
