# Climbers REST API

Climbers app will help climbers find partners to climb with. This application will allow users to create groups / events at specific date & location that other users will be able to join.
Application will provide those groups with online chat to communicate with other members of the group.

To do:
- Room chats with ussage of websockets
- Room members limit (provided by user creating the room)
- Room archivisation after the date of event has passed
- Friends feature
- Private rooms feature
- Tests

# How to use
Download the repository.

Start with docker:

cd to /climbers and use docker-compose
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
