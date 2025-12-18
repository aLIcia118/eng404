# flask-api
An example flask rest API server.

1.create the develpment environment, run `make dev_env`.

2.activate the virtual environment, run 'source .venv/bin/activate'.

To run the full project test suite, run `make all_tests`.  
To run tests for the current module during development, run `make tests`.
They are running tests in all directories.

To start the application locally to test it on your own machine, run `./local.sh`.

after the server starts, you can test endpoints such as 'GET/cities/read, GET/health/db'.

To run production-style checks and ready for deployment, run `make prod`.

## MongoDB configuration
The app connects to MongoDB using one of the following:

- `MONGODB_URI` (recommended for Atlas)
- or `CLOUD_MONGO=1` together with `MONGO_USER`, `MONGO_PASSWD`, `MONGO_HOST`
- or, if nothing is set, it falls back to `mongodb://127.0.0.1:27017`

## Connect to MongoDB in the Cloud
Set MongoDB Atlas URI with your username and password. 
E.g. run `export MONGODB_URI="mongodb+srv://rachel:Jinmuyan1412@rachel.dtxj3lp.mongodb.net/?appName=Rachel"`

If no environment variables are set, the application defaults to"mongodb://127.0.0.1:27017"

To check connection, run
```
python - << 'PY'                                                                                        
import os
from pymongo import MongoClient

uri = os.environ["MONGODB_URI"]
print("Using URI:", uri)

client = MongoClient(uri, serverSelectionTimeoutMS=5000)

try:
    result = client.admin.command("ping")
    print("Ping result:", result)
    print("Successfully connect")
except Exception as e:
    print("Cannot connect：", e)
PY
```
Then you can run `make tests`.

## Run API Server in the Cloud
1. Login to pythonanywhere using this account: username: rachelchen, password: Jinmuyan1412
2. Before you run/change anything, please try GET cities/read or GET health/db, etc. to make sure it can connect to the database and mongoDB data correcctly.
3. test
