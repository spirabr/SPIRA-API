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

BUILD-API-IMAGE := docker compose build tester
RUN-CONTAINERS := docker compose --profile test run --rm tester 
UP-CONTAINERS := docker compose --profile production up --force-recreate -d
STOP-CONTAINERS := docker compose stop
CLEAN-DB := rm -rf ./data/db
SLEEP := sleep 5

setup:
	$(STOP-CONTAINERS)
	$(CLEAN-DB)
	$(UP-CONTAINERS)
	$(SLEEP)

cleanup:
	$(STOP-CONTAINERS)
	$(CLEAN-DB)

user-auth-request:
	curl -f -o /dev/null --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=321'

test-auth-user-endpoint:
	$(MAKE) -f tests/system_tests/users/test_users_endpoint.mak setup
	$(RUN-CONTAINERS) tests/system_tests/users/insert_entities.py
	$(MAKE) -s -f tests/system_tests/users/test_users_endpoint.mak user-auth-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE) -f tests/system_tests/users/test_users_endpoint.mak cleanup
