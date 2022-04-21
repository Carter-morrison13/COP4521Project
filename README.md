# COP4521Project

## A Short Story Website

### Instructions
There are two ways you can run this application:

1. For development, the application can be run in the root folder by running connector.py to setup the database and the tables, 
then run app.py, which will run the application on a flask/waitress server for localhost.

2. For production, we created a multi-container docker image with mysql and flask, to run this docker-image
first you must have the necessary docker engine for your OS, then you can do 'docker compose up -d' in 
the root folder and it should create a docker image called 'cop4521project'.
