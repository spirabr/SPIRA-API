RED     := \033[1;31m
GREEN   := \033[1;32m
YELLOW  := \033[1;33m
BLUE    := \033[1;34m
PURPLE  := \033[1;35m
CYAN    := \033[1;36m
WHITE   := \033[1;37m
RESTORE := \033[0m

define message
printf "${BLUE}%s${RESTORE}\n" $(strip $1)
endef

define success
(printf "${GREEN}%s${RESTORE}\n" $(strip $1); exit 0)
endef

define warn
(printf "${YELLOW}%s${RESTORE}\n" $(strip $1); exit 0)
endef

define failure
(printf "${RED}%s${RESTORE}\n" $(strip $1); exit 1)
endef

# --- CUSTOM COMMANDS --- #

BUILD-API-IMAGE := docker compose build tester
RUN-CONTAINERS := docker compose --profile test run --rm tester
STOP-CONTAINERS := docker compose stop

# --- CUSTOM COMMANDS --- #


# --- UNIT TESTS --- #

adapter-unit-tests:
	$(call warn,"running unit tests for adapters")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/adapters || $(call failure,"failed in unit tests for adapters!")
	$(STOP-CONTAINERS)
	$(call success,"passed in unit tests for adapters!")

port-unit-tests:
	$(call warn,"running unit tests for ports")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/ports || $(call failure,"failed in unit tests for ports!")
	$(STOP-CONTAINERS)
	$(call success,"passed in unit tests for ports!")
	
service-unit-tests:
	$(call warn,"running unit tests for services")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/services || $(call failure,"failed in unit tests for services!")
	$(STOP-CONTAINERS)
	$(call success,"passed in unit tests for services!")
	

all-unit-tests:
	$(MAKE) adapter-unit-tests	
	$(MAKE) port-unit-tests	
	$(MAKE) service-unit-tests

# --- UNIT TESTS --- #


# --- INTEGRATION TESTS --- #

endpoint-integration-tests:
	$(call warn,"running integration tests for endpoints")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/endpoints || $(call failure,"failed in integration tests for endpoints!")
	$(STOP-CONTAINERS)
	$(call success,"passed in integration tests for endpoints!")
	
database-connection-tests:
	$(call warn,"running connection tests for database")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/connections/database || $(call failure,"failed in connection tests for database!")
	$(STOP-CONTAINERS)
	$(call success,"passed in connection tests for database!")

message-service-connection-tests:
	$(call warn,"running connection tests for message service")

	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/connections/message_service || $(call failure,"failed in connection tests for message service!")
	$(STOP-CONTAINERS)
	$(call success,"passed in connection tests for message service!")
	
simple-storage-connection-tests:
	$(call warn,"running connection tests for simple storage")

	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/connections/simple_storage || $(call failure,"failed in connection tests for simple storage!")
	$(STOP-CONTAINERS)
	$(call success,"passed in connection tests for simple storage!")
	

all-integration-tests:
	$(MAKE) endpoint-integration-tests
	$(MAKE) database-connection-tests
	$(MAKE) message-service-connection-tests
	$(MAKE) simple-storage-connection-tests

# --- INTEGRATION TESTS --- #


# --- RUN ALL TESTS --- #
all-tests:
	$(STOP-CONTAINERS)
	$(MAKE) all-unit-tests
	$(MAKE) all-integration-tests

	