from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"Hello": "World"}


@app.get("/maomishen")
async def show_maomishen():
    return {"show": "Maomishen"}
