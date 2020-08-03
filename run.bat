@echo off
set FLASK_APP=api
IF EXIST yelpsecrets set /p YELP_API_KEY=<yelpsecrets
python setup.py
flask run