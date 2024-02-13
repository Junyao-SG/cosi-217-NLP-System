from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def tmp():
    return {"message" : "Hello, World!!!"}
