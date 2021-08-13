# Climbers REST API

Climbers app will help climbers find partners to climb with. This application will allow users to create groups / events at specific date & location that other users will be able to join.
Application will provide those groups with online chat to communicate with other members of the group.

Features:
- CRUD functions for accounts
- JWT authentication
- CRUD functions for rooms, restricted with permissions
- CRUD functions for memberships, restricted with permissions

To do:
- Room chats with usage of websockets
- Room members limit (provided by user creating the room)
- Room archivization after the date of event has passed
- Friends feature
- Private rooms feature


# How to use
Download the repository.

Start with docker:

cd to /climbers and use docker-compose by typing in console
```
docker-compose up
```
Start with Python:

Preferably create a virtual environment.

cd to /climbers/climbersproject
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.
```
pip install -r requirements.txt
```
With requirements installed you can run the app:
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Tests
With docker-compose:
Go into docker-compose.yml file, comment out:
```
"python manage.py wait_for_db
 python manage.py makemigrations &&
 python manage.py migrate &&
 python manage.py runserver 0:8000"
 ```
and uncomment:
 ```
 "coverage run manage.py test && coverage report"
 ```
next just cd to /climbers and use docker-compose by typing in console
 ```
 docker-compose up
 ```
With python:
After installing app and requirements.txt simply go into /climbers/climbersproject and type into console:
  ```
coverage run manage.py test && coverage report
  ```
