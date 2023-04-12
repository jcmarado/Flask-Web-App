#!/usr/bin/env bash

export DB_USER=test_user
export DB_PASS=test_password
export DB_NAME=active_vehicles
export INSTANCE_CONNECTION_NAME=starlit-oven-380019:us-east4:test-instance
export FLASK_APP=website
export FLASK_ENV=development


flask run -p 8080 --debugger
