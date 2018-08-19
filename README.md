# Request Mirror

Request Mirror is a real-time request debugging application inspired by [RequestBin](https://github.com/Runscope/requestbin). 
The main difference between RequestBin and Request Mirror is that the latter updates in real-time, using WebSockets. 
So whenever you make a request to a _mirror_, you see it appear on the webpage immediately, without needing to 
refresh the page.

Request Mirror is an experiment, so little effort has been made to optimize performance. It also has _zero tests_.

## How to run in Docker

Install [Docker](https://www.docker.com/products/docker-desktop) if you haven't yet.

**Run Redis + Request Mirror**

```bash
$ docker-compose up
```

**Build the Docker Image yourself**

This is optional, because the docker-compose file uses the [existing docker image](https://hub.docker.com/r/daan/request-mirror/) 
from Docker Hub.

```bash
$ docker build -t request-mirror:latest
```

If you want to use your locally built image, replace `daan/request-mirror:latest` in `docker-compose.yml` with 
`request-mirror:latest`

## How to run locally

### Install Dependencies

Request Mirror requires Redis to store active "mirrors". It expects Redis running on the default host and port: 
`localhost:6379`. A Docker Compose file has been provided to run Redis. Just run: `docker-compose up -d`

Request Mirror also requires [Yarn](https://yarnpkg.com/en/) to be installed. Installation instructions can be 
[found here](https://yarnpkg.com/en/docs/install).

You can now install the frontend dependencies of Request Mirror:

```bash
$ yarn
```

Now you should install the required Python packages:

```bash
$ pip install -r requirements.txt
```

It is recommended to do this inside a [Virtual Environment](https://docs.python.org/3/tutorial/venv.html)

### Starting Request Mirror in development mode

After you've taken care of all the dependencies, you can run Request Mirror:

```bash
$ yarn run dev
```

This will run the Flask app and the in development mode, and also run a watcher that watches the frontend files and 
re-packages the frontend whenever one of the source files changes. The frontend is served by Flask by the way.

### Starting Request Mirror with Production ready frontend

You can also pre-build the frontend, and run only the Flask app:

```bash
$ yarn run build
$ python app.py

```

## Architecture

Request Mirror has a very simple architecture

### Backend

The backend consists of a Flask app that serves the home page and the mirror pages and receives requests for mirrors. 
Users can create a mirror with a name of their own choosing, or have Request Mirror generate a random string. The mirror 
name or "code" is stored in Redis with an expiry time of 15 minutes. The expirty time - or time-to-live - is updated 
whenever a new request is sent to that mirror, or when that mirror's page is visited.

The backend uses [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/) to take care of real-time 
communication with the frontend.

### Frontend

There are basically 2 views in Request Mirror: the home page and the mirror pages. Each of these views is served 
separately from the backend, so the application as a whole is not a Single Page App. The mirror view/page however, is a 
React app that is built and bundled using Yarn and [Parcel](https://parceljs.org/).
