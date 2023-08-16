#!/bin/bash

TOKEN=$(curl --request POST 'localhost:4000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'
)

RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/models/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer $TOKEN" \
		--data-raw '{ "name" : "testmodel2", "publishing_channel" : "testtopic2" }')
	
FAILED_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/models/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer $TOKEN" \
		--data-raw "{}")

UNAUTH_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		--request POST 'localhost:4000/v1/models/' \
		--header 'Content-Type: application/json' \
		--header "Authorization: Bearer fake-token" \
		--data-raw '{ "name" : "testmodel3", "publishing_channel" : "testtopic3" }')


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