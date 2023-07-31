from fastapi import APIRouter
from utils.env import Env
import requests


router = APIRouter()
env = Env()


def post_app_registration() -> tuple[str, str]:
    url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/app"
    print(url)

    app_id, token = None, None

    payload = {
        "name": "file_service",
        "scope": "readWrite",
        "service_type": "port",
        "data": "8000",
        "auth_type": "bypass",
    }

    response = requests.post(url=url, json=payload)

    print(response.text)
    print(response.json())  # text -> json
    print(response.status_code)

    if response.status_code == 200:
        app_id = response.json()["data"]["authen"]["app_id"]
        token = response.json()["data"]["authen"]["token_key"]
    return app_id, token


def get_app_registration_info():
    url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/app"

    response = requests.get(url=url)
    print(response.text)
    print(response.json())
    print(response.status_code)

    if response.status_code == 200:
        return response.json()["data"]


@router.post("/")
async def register():
    if env.check_key_and_value_exist("APP_ID") and env.check_key_and_value_exist(
        "TOKEN"
    ):
        return {"registration_info": "already registered"}
    else:
        app_id, token = post_app_registration()
        if app_id is not None and token is not None:
            env.set_key("APP_ID", app_id)
            env.set_key("TOKEN", token)

            return {"registration_info": "success"}
        else:
            return {"registration_info": "failed"}


@router.get("/")
async def get_register_info():
    data = get_app_registration_info()
    return data


if __name__ == "__main__":
    pass
