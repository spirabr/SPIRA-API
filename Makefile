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

# --- CUSTOM COMMANDS --- #


# --- UNIT TESTS --- #

adapter-unit-tests:
	$(call warn,"running unit tests for adapters")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/adapters

port-unit-tests:
	$(call warn,"running unit tests for ports")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/ports
	
service-unit-tests:
	$(call warn,"running unit tests for services")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/unit_tests/services
	

all-unit-tests:
	$(MAKE) adapter-unit-tests	
	$(MAKE) port-unit-tests	
	$(MAKE) service-unit-tests

# --- UNIT TESTS --- #


# --- INTEGRATION TESTS --- #

endpoint-integration-tests:
	$(call warn,"running integration tests for endpoints")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/endpoints
	
database-connection-tests:
	$(call warn,"running connection tests for database")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/connections/database

message-service-connection-tests:
	$(call warn,"running connection tests for message service")
	$(BUILD-API-IMAGE)
	$(RUN-CONTAINERS) tests/integration_tests/connections/message_service
	

all-integration-tests:
	$(MAKE) endpoint-integration-tests
	$(MAKE) database-connection-tests
	$(MAKE) message-service-connection-tests

# --- INTEGRATION TESTS --- #


# --- RUN ALL TESTS --- #
all-tests:
	$(MAKE) all-unit-tests
	$(MAKE) all-integration-tests

	