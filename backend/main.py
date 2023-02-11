from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
async def root(q: int | None = Query(default=None)):
    return {"message": q}