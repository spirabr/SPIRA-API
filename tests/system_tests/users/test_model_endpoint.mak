BUILD-API-IMAGE := docker compose build tester
RUN-CONTAINERS := docker compose --profile test run --rm tester 
UP-CONTAINERS := docker compose --profile production up --force-recreate -d
STOP-CONTAINERS := docker compose stop
DOWN-CONTAINERS := docker compose down
WAIT-FOR-INITIALIZATION := sleep 10

test-auth-user-endpoint:
	$(STOP-CONTAINERS)
	$(DOWN-CONTAINERS)
	$(UP-CONTAINERS)
	$(STOP-CONTAINERS)
	$(RUN-CONTAINERS) tests/system_tests/users/insert_entities.py
	$(UP-CONTAINERS)
	curl -v --location POST 'http://localhost:3000/v1/users/auth' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'username=testuser' --data-urlencode 'password=spira2022'