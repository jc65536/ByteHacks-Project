# ByteHacks-Project
The Haphazard Hackers' project.

### Configuration
You must configure the `YELP-API-KEY` field in config.json.

### How to run backend

Installing Dependencies:<br>
`pip install -r requirements.txt`

Setting Up App: <br>
`python setup.py`

Running Flask App:
```shell
export FLASK_APP=api (Unix)
set FLASK_APP=api (Windows CMD)
flask run
```

```
# Set flask to dev mode
export FLASK_ENV=development
```

or run `run.bat` if you're on Windows

### How to run frontend
**Make sure you are in the src/ folder**<br>
Installing Dependencies:<br>
`npm install`

Running the Server:<br>
`npm run dev`<br>

After running both the frontend and the backend, you can connect to the app by going to [http://localhost:3000][http://localhost:3000]

[http://localhost:3000]: http://localhost:3000