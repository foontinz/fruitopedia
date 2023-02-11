from fastapi import FastAPI, Query
import os

app = FastAPI()


@app.get("/{query}")
async def root(query):
    return {"name": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "nigger":os.environ.get("nigger")}