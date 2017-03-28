project := 'trf'

.PHONY: test install uninstall

test:
	@python -m unittest discover -v

install:
	@pip install . --ignore-installed

uninstall:
	@pip uninstall $(trf) -y || true
