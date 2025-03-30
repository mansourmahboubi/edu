import logging

from fastapi import FastAPI

from .actors import sample_actor

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root():
    sample_actor.send()
    return {"Hello": "FastAPI running in a Docker container"}
