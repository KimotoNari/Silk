# Welcome to Silk

## About
> Silk is a security focused note taking alternative that can be self hosted with support for multiple users.

## Usage
This project requires having Python 3 and pip installed on your system
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

### Install Flask
Within the activated environment:
```
pip install flask
```

### Starting the Dev Build
Before the first run, you need to initialize the database:
```
flask --app silkMain init-db
```

To run the Dev Build:
```
flask --app flaskr run --debug
```
With this running, you will now be able to access the webapp at: http://127.0.0.1:5000/