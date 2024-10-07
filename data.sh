#!/bin/bash

# Get the database name from the command line argument
DB_NAME=$1

# Replace 'your_password' with the desired password
sudo su - postgres bash -c "psql -c \"ALTER USER postgres WITH PASSWORD 'your_password';\" && createdb $DB_NAME -O postgres"
