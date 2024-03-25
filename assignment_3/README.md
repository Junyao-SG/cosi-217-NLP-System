# Assignment 3

The codebase for this assignment has been restructured and divided into three distinct directories, each corresponding to one of the three applications.

## Step One

Open a terminal from the root directory of this repo folder

## Step Two

Use docker compose to build and run apps by creating an image *nlp-cpu-env* and multiple containers. Use *--build* flag to rebuild the image forcely.

```bash
docker compose -f assignment_3/docker-compose.yml up
```

Waiting for almost 40 sec, open a browser and go to three addresses for these three applications:

1. Fastapi: <http://localhost:8050>
    1. Ensure current working path is in ./assignment_3/app_fastapi for using the local file *input.json* (this app is running in a Docker container, but the commands below require a local file for processing)

        ```bash
        cd ./assignment_3/app_fastapi
        ```

    1. Run any cmd:

        ```bash
        curl "http://localhost:8050?pretty=true"
        curl "http://localhost:8050/ner?pretty=true" -H "Content-Type: application/json" -d@input.json
        curl "http://localhost:8050/dep?pretty=true" -H "Content-Type: application/json" -d@input.json
        ```

1. Streamlit: <http://localhost:8501>
    - go to the webpage
1. Flask: <http://localhost:8000> (this is the only one taking time longer than 30 sec; it includes a delay to ensure the MySQL server is ready for connections.)
    - go to the webpage

## Step Three

Use cmd below to bring everything down, removing containers entirely.

```bash
docker compose -f assignment_3/docker-compose.yml down
```

Use the *--volumes* flag to remove database volumes, as this breaks data persistence.

```bash
docker compose -f assignment_3/docker-compose.yml down --volumes
```
