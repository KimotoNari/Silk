# Welcome to Silk

## About
> Silk is a security focused note taking alternative that can be self hosted with support for multiple users. It is based on the [flaskr](https://flask.palletsprojects.com/en/stable/tutorial/) project.

## Usage
This project requires having Python 3 and pip installed on your system

### Initial Setup with release package
Create a directory for the project

Copy the .whl file into the directory

### Setup and activate Python Virtual Environment:
In the Silk Directory run:

Windows:
```
> py -3 -m venv .venv
> .venv\Scripts\activate
```
Linux/macOS:
```
$ python3 -m venv .venv
$ . .venv/bin/activate
```

### Install Silk
Within the activated environment:
```
pip install silkmain-0.1.0-py2.py3-none-any.whl
```

### Starting the Dev Build
Before the first run, you need to initialize the database:
```
flask --app silkMain init-db
```

To run the Dev Build:
```
flask --app silkMain run --debug
```
With this running, you will now be able to access the webapp at: http://127.0.0.1:5000/
