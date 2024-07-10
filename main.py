from fastapi import FastAPI
from auth_routers import auth_router
from fastapi_jwt_auth import AuthJWT
from schemas import Settings, LoginModel

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)


@app.get("/")
async def get_home():
    return {"message": "Hello FastAPI"}