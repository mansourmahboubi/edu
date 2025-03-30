from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "FastAPI running in a Docker container"}
