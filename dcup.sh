#!/bin/bash

docker-compose up -d mongo-init-replica
sleep 15

docker-compose up -d mongo
sleep 15

docker-compose up -d rocketchat
sleep 60