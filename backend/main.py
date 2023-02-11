from fastapi import FastAPI, Query
import os

app = FastAPI()


@app.get("/{query}")
async def root(query):
    return {"name": os.environ.get(""),
            }