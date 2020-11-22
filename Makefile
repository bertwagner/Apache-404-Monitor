help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make audit                          Run the audit			             '
	@echo '                                                                          '

audit:
	. .venvl/bin/activate; \
	python3 process_data.py
