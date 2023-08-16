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

DIR := tests/system_tests/users
BUILD-API-IMAGE := docker compose build tester
RUN-CONTAINERS := docker compose --profile test run --rm tester 
UP-CONTAINERS := docker compose --profile production up --force-recreate -d
STOP-CONTAINERS := docker compose stop
SLEEP := sleep 5
MAKE-HERE := $(MAKE) -f $(DIR)/test_users_endpoints.mak

setup:
	$(STOP-CONTAINERS)
	$(UP-CONTAINERS)
	$(SLEEP)

cleanup:
	$(STOP-CONTAINERS)

test-auth-user:
	bash $(DIR)/test-auth-user.sh && $(call success,"PASSED") || $(call failure,"NOT PASSED")

test-get-user:
	bash $(DIR)/test-get-user.sh && $(call success,"PASSED") || $(call failure,"NOT PASSED")

test-create-user:
	bash $(DIR)/test-create-user.sh && $(call success,"PASSED") || $(call failure,"NOT PASSED")

test-users-endpoints:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(MAKE-HERE) test-auth-user
	$(MAKE-HERE) test-get-user
	$(MAKE-HERE) test-create-user
	$(MAKE-HERE) cleanup
	
	
	