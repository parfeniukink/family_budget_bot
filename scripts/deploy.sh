#!/bin/bash

cd ~/family_budget_bot/

git pull origin master
docker-compose down && docker-compose up --build -d
