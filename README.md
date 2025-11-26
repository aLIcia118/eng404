# flask-api
An example flask rest API server.

To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.

To run the project’s test suite, run `make all_tests`.

To start the application locally to test it on your own machine, run `./local.sh`.

To run production-style checks and ready for deployment, run `make prod`.

## MongoDB configuration
The app connects to MongoDB using one of the following:

- `MONGODB_URI` (recommended for Atlas)
- or `CLOUD_MONGO=1` together with `MONGO_USER`, `MONGO_PASSWD`, `MONGO_HOST`
- or, if nothing is set, it falls back to `mongodb://127.0.0.1:27017`
