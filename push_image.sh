#!/bin/bash
docker compose stop
docker compose build api
docker compose push api