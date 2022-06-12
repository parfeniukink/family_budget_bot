#!/bin/bash

cd ~/family_budget_bot/

git pull origin main
docker-compose restart bot
