# Assignment 3

The codebase for this assignment has been restructured and divided into three distinct directories, each corresponding to one of the three applications.

## Option One
Use docker compose
```bash
docker compose -f assignment_3/docker-compose.yml up --build
```

```bash
docker compose -f assignment_3/docker-compose.yml down --volumes
```


## Option Two
Build images for each application
```bash
docker build -t fastapi -f ./assignment_3/Dockerfile_1 .
```

```bash
docker build -t streamlit -f ./assignment_3/Dockerfile_2 .
```

```bash
docker build -t flask -f ./assignment_3/Dockerfile_3 .
```

