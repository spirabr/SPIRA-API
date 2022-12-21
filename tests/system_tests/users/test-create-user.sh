#!/bin/bash

TOKEN=$(curl --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'
)

RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:3000/v1/users' \
		--header 'Content-Type: application/json' \
		--header 'Authorization: Bearer %' \
		--data-raw '{ \
				"username" : "testuser2", \
				"email" : "test@usp.br", \
				"password" : "123", \
				"password_confirmation" : "123" \
		}')

FAILED_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:3000/v1/users' \
		--header 'Content-Type: application/json' \
		--header 'Authorization: Bearer %' \
		--data-raw '{}')

if [ $RESPONSE_STATUS -eq 200 ] && [ $FAILED_RESPONSE_STATUS -gt 399 ]
 	then
 		exit 0;
	else
		exit 1;
fi;