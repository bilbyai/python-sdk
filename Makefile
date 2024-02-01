.PHONY: install-local
install-local:
	@poetry build && pip install dist/bilbyai-0.1.0-py3-none-any.whl --force-reinstall
