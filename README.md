# Getting Started with Django Server
This was created using Django library for backend server

## Creting virtual environment
Run the following command to create virtual environment:
```
python3 -m venv venv
```
Activate the virtual environment with the following command:
```
source venv/bin/activate
```

## Quick install and Run
Run the following script to install all the dependencies and run the server:
```
./run.sh
```

## Installing dependencies
Once the virtual environment is activated, run the following command to install all the dependencies:
```
pip install -r requirements.txt
```

> **Warning** 
> This server is hosted on Heroku which uses a linux system to host the servers. So, if you are using a windows system, some dependencies might not install.

## Running the server
To run the server, run the following command:
```
python manage.py runserver
```
Or if you have heroku installed, you can also emulate the heroku server by running the following command:
```
heroku local
```

## Running Tests
The repo comes with a test suite to test the server. To run the tests, run the following command:
```
python manage.py test
```

## Accessing the Server
Once the server is up and running it will be hosted locally on ``localhost:8000`` or on ``localhost:5000`` if you are using heroku local.

> **Note**
> If you want to access all of the endpoints, you will probably need an application like postman since the browsers can only make GET requests.
