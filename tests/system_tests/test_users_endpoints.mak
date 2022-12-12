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
SLEEP := sleep 5
MAKE-HERE := $(MAKE) -f tests/system_tests/test_users_endpoints.mak

setup:
	$(STOP-CONTAINERS)
	$(UP-CONTAINERS)
	$(SLEEP)

cleanup:
	$(STOP-CONTAINERS)

get-token:
	curl --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'

user-auth-request:
	curl -f -o /dev/null --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef'

create-user-request:
	$(MAKE-HERE) get-token | curl -f -o /dev/null --request POST 'localhost:3000/v1/users' \
		--header 'Content-Type: application/json' \
		--header 'Authorization: Bearer {}' \
		--data-raw '{ \
				"username" : "testuser2", \
				"email" : "test@usp.br", \
				"password" : "123", \
				"password_confirmation" : "123" \
		}'

get-user-request:
	$(MAKE-HERE) get-token | curl --location --request GET 'localhost:3000/v1/users/639686c4ba1604f1387a6c00' --header 'Authorization: Bearer {}'

test-auth-user-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(MAKE-HERE) user-auth-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup

test-create-user-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(MAKE-HERE) create-user-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup

test-get-user-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(MAKE-HERE) get-user-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup

test-users-endpoints:
	$(MAKE-HERE)  test-get-user-endpoint
	$(MAKE-HERE)  test-auth-user-endpoint
	$(MAKE-HERE)  test-create-user-endpoint
	
	
	