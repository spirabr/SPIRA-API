#!/bin/bash

TOKEN=$(curl --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef' | jq -r '.access_token'
)

RESPONSE_STATUS=$(curl --write-out '%{http_code}' --silent --output /dev/null \
	  --request POST 'localhost:3000/v1/users/auth' \
		--header 'Content-Type: application/x-www-form-urlencoded' \
		--data-urlencode 'username=testuser' \
		--data-urlencode 'password=abcdef'
)

if [ $RESPONSE_STATUS -eq 200 ]
 	then
 		exit 0;
	else
		exit 1;
fi;