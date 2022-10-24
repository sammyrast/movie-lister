# movie lister simple app 
- built with fastapi and psql as backend

# How Do I Run It?
$ docker compose up
and navigate to localhost:8000

# TODOs and missing items
- no filtering applied yet
- no applied searching yet
- Not super user friendly (the html and css needs a lot of work + the JSON load can be prettier with JavaScript)
- env. variables are exposed and secrets are out; these should be handled with env. variables on docker-compose
- Models are on the same main script as the server. This could be simplified by dividing the models-> app-> db file structures.
- GITHUB ACTION for CI/CD for automated testing.
- UNIT TESTING

# hardware
macbook pro 2019

# dev environment
all is in docker and docker-compsoe
