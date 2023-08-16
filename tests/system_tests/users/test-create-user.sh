#!/bin/bash

TOKEN=$(curl --request POST 'localhost:4000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'
)

RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/users/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer $TOKEN" \
		--data-raw '{ "username" : "testuser2", "email" : "test2@usp.br", "password" : "123", "password_confirmation" : "123" }')

FAILED_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/users/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer $TOKEN" \
		--data-raw '{}')

UNAUTH_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/users/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer fake-token" \
		--data-raw '{ "username" : "testuser3", "email" : "test3@usp.br", "password" : "123", "password_confirmation" : "123" }')

if [ $RESPONSE_STATUS -eq 200 ]
	then
 		echo 'PASSED';
	else
		echo 'FAILED';
		exit 1;
fi;

if [ $FAILED_RESPONSE_STATUS -gt 399 ]
	then
 		echo 'PASSED';
	else
		echo 'FAILED';
		exit 1;
fi;

if [ $UNAUTH_RESPONSE_STATUS -eq 401 ]
 	then
 		echo 'PASSED';
	else
		echo 'FAILED';
		exit 1;
fi;