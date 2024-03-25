# Assignment 3

The codebase for this assignment has been restructured and divided into three distinct directories, each corresponding to one of the three applications.

## Step One
Open a terminal from the root directory of this repo folder

## Step Two
Use docker compose to build and run apps by creating an image *nlp-cpu-env* and multiple containers.
```bash
docker compose -f assignment_3/docker-compose.yml up
```
Waiting for almost 40 sec, open a browser and go to three addresses for these three applications:

- Fastapi: <http://localhost:8050> 
- Streamlit: <http://localhost:8501> 
- Flask: <http://locahost:8000> (this is the only one taking time longer than 30 sec; it includes a delay to ensure the MySQL server is ready for connections.)


## Step Three
Use cmd below to bring everything down, removing containers entirely.
```bash
docker compose -f assignment_3/docker-compose.yml down
```
Use the *--volumes* flag to remove database volumes, as this breaks data persistence.
```bash
docker compose -f assignment_3/docker-compose.yml down --volumes
```