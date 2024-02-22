# COSI-217 Assignment 1

This assignment runs in a conda env with python=3.11.
After create the virtural environment, run:

```bash
pip install -r requirements.txt
```

Ensure to change directory to code folder:
```bash
cd assignment_1
```
### FastAPI
1. Start FastAPI:
```bash
uvicorn fastapi_app:app --reload
```

2. Run any cmd(with or without the parameter pretty) below:
```bash
$ curl http://127.0.0.1:8000
$ curl http://127.0.0.1:8000/ner -H "Content-Type: application/json" -d@input.json
$ curl http://127.0.0.1:8000/dep -H "Content-Type: application/json" -d@input.json
```

```bash
$ curl http://127.0.0.1:8000?pretty=true
$ curl http://127.0.0.1:8000/ner?pretty=true -H "Content-Type: application/json" -d@input.json
$ curl http://127.0.0.1:8000/dep?pretty=true -H "Content-Type: application/json" -d@input.json
```

### Flask
```bash
flask --app flask_app run
```
This flask app will be running on http://127.0.0.1:5000

### Streamlit
```bash
streamlit run streamlit_app.py
```
This streamlit app will run on http://localhost:8501