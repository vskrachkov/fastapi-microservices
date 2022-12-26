from fastapi import FastAPI

application = FastAPI()


@application.get("/hello")
async def hello() -> dict:
    return {"hello": "!!!"}
