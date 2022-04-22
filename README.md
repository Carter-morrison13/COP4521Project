# COP4521Project

## A Short Story Website
### Members
	Braden Seidl, Carter Morrison, George Chester, Jacob Schiff, Marco Heflin
### Instructions
There are two ways you can run this application:

1. For development, the application can be run in the root folder by running connector.py to setup the database and the tables, 
then run app.py, which will run the application on a flask/waitress server for localhost.

2. For production, we created a multi-container docker image with mysql and flask, to run this docker-image
first you must have the necessary docker engine for your OS, then you can do 'docker compose up -d' in 
the root folder and it should create a docker image called 'cop4521project'.

### Description

For our project we want to create a website that allows users to create accounts and collaborate 
together to write stories. People can go to the website and look at any and all stories that have been
created and users can vote for the stories they like best. The top stories at any given time can be seen 
from a leaderboard page. To allow for a safe and inclusive environment where all can create, there are 
moderators that can look through all the stories and delete/edit stories as well as delete users if they 
break rules or are innapropriate.

### CURRENT LIBRARIES
- hashlib
- flask
	- render_template
	- Flask
	- request
	- redirect
	- session
- mysql.connector
- time
- waitress
	- serve
### EXTRA FEATURES

- Leaderboard with the ability to vote for your favorite stories
- Hashing of passwords for security
- Docker system
- Database tables were expanded
	
### SEPERATION OF WORK

- Braden Seidl
		- Connector.py, Database set up, flask skeleton, front page, css, password hash
- Carter Morrison
		- Voting system, browse stories, expanded database tables
- George Chester
		- Chatroom functionality, supporter role, chatroomSetup
- Jacob Schiff
		- Moderation system, moderator page for searching, user role implementation
- Marco Heflin
		- Chatroom mapping, waiting room, docker, leaderboard

	We all made small changes to the various web pages throughout the project, cleaned up code, 
	and helped each other debug our various implementations.
