#!/bin/bash

TOKEN=$(curl --request POST 'localhost:4000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'
)

RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		'localhost:4000/v1/users/639686c4ba1604f1387a6c00/inferences' --header "Authorization: Bearer $TOKEN")

UNAUTH_RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
		'localhost:4000/v1/users/639686c4ba1604f1387a6c00/inferences' --header "Authorization: Bearer")

if [ $RESPONSE_STATUS -eq 200 ]
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