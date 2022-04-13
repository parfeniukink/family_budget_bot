BLACK_COMMAND = black ./
FLAKE8_COMMAND = flake8 ./
ISORT_COMMAND = isort ./


.PHONY: code_quality
code_quality:
	${BLACK_COMMAND} && ${ISORT_COMMAND} && ${FLAKE8_COMMAND}

