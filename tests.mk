make:
	@echo running unit tests for adapters
	python3 -m py.test tests/unit_tests/adapters

	@echo running unit tests for ports
	python3 -m py.test tests/unit_tests/ports

	@echo running unit tests for ports
	python3 -m py.test tests/unit_tests/services

	@echo running integration tests for endpoints
	python3 -m py.test tests/integration_tests