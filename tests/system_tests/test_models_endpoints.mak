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
MAKE-HERE := $(MAKE) -f tests/system_tests/test_models_endpoints.mak

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

create-model-request:
	$(MAKE-HERE) get-token | curl -f -o /dev/null --request POST 'localhost:3000/v1/models' \
		--header 'Content-Type: application/json' \
		--header 'Authorization: Bearer {}' \
		--data-raw '{ \
				"name" : "model_1", \
				"publishing_channel" : "model_1_channel" \
		}'

get-model-request:
	$(MAKE-HERE) get-token | xargs -I {} curl --location --request GET 'localhost:3000/v1/models/629e4f781ed5308d4b8212bc' \
		--header 'Authorization: Bearer {}'

get-models-request:
	$(MAKE-HERE) get-token | xargs -I {} curl --location --request GET 'localhost:3000/v1/models/' \
		--header 'Authorization: Bearer {}'

test-create-model-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(RUN-CONTAINERS) tests/system_tests/config/insert_model.py
	$(MAKE-HERE) create-model-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup

test-get-model-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(RUN-CONTAINERS) tests/system_tests/config/insert_model.py
	$(MAKE-HERE) get-model-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup

test-get-models-endpoint:
	$(MAKE-HERE) setup
	$(RUN-CONTAINERS) tests/system_tests/config/insert_user.py
	$(RUN-CONTAINERS) tests/system_tests/config/insert_model.py
	$(MAKE-HERE) get-models-request && $(call success,"PASSED") || $(call failure,"NOT PASSED")
	$(MAKE-HERE) cleanup


test-models-endpoints:
	$(MAKE-HERE) test-get-model-endpoint
	$(MAKE-HERE) test-get-models-endpoint
	$(MAKE-HERE) test-create-model-endpoint
	
	