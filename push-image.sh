#!/bin/bash
docker compose stop
docker compose build api
docker compose push api
docker compose build k8s-test-image
docker compose push k8s-test-image