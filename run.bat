@echo off
set FLASK_APP=api
IF EXIST yelpsecrets.txt set /p YELP_API_KEY=<yelpsecrets.txt
python setup.py
flask run