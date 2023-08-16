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

DIR := tests/system_tests/inferences
BUILD-API-IMAGE := docker compose build tester
RUN-CONTAINERS := docker compose --profile test run --rm tester 
UP-CONTAINERS := docker compose --profile production up -d
STOP-CONTAINERS := docker compose stop
SLEEP := sleep 5
MAKE-HERE := $(MAKE) -f $(DIR)/test_inferences_endpoints.mak

setup:
	$(STOP-CONTAINERS)
	$(UP-CONTAINERS)
	$(SLEEP)

cleanup:
	$(STOP-CONTAINERS)

test-get-inference:
	bash $(DIR)/test-get-inference.sh && $(call success,"PASSED") || $(call failure,"NOT PASSED")

test-get-inferences:
	bash $(DIR)/test-get-inferences.sh && $(call success,"PASSED") || $(call failure,"NOT PASSED")

test-inferences-endpoints:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(RUN-CONTAINERS) tests/system_tests/config/insert_model.py
	$(RUN-CONTAINERS) tests/system_tests/config/insert_inference.py
	$(MAKE-HERE) test-get-inference
	$(MAKE-HERE) test-get-inferences
	$(MAKE-HERE) cleanup
	
	
	