from fastapi import APIRouter
from utils.env import Env
import requests


router = APIRouter()
env = Env()


def post_app_registration() -> tuple[str, str]:
    url = f"{env.get_value('APP_REGISTER_DOMAIN')}/apps/api/create"
    app_id, token = None, None

    payload = {
        "name": "file_service",
        "scope": "readwrite",
        "service_type": "port",
        "data": "8000",
        "auth_type": "bypass",
    }

    response = requests.post(url=url, json=payload)    

    if response.status_code == 200:
        app_id = response.json()["data"]["authen"]["appid"]
        token = response.json()["data"]["authen"]["token_key"]
    return app_id, token

def get_app_registration_info():
    url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/app/{env.get_value('APP_ID')}?token={env.get_value('TOKEN')}"

    response = requests.get(url=url)
    
    if response.status_code == 200:
        return response.json()

@router.post("/")
def register():
    
    if env.check_key_and_value_exist("APP_ID") and env.check_key_and_value_exist(
        "TOKEN"
    ):  
        app_id =  env.get_value("APP_ID")
        token =  env.get_value("TOKEN")
        
        # maybe error if appid and bypass token are not available or already update.
        return {"registration_info": "already registered", "data":{"app_id":app_id, "token":token}}
    else:
        app_id, token = post_app_registration()
        # app_id, token = 'eca94222-8fbd-42b3-8640-945a51c1ec17', 'farBKPGLU2OwaRPPm9cJx8h6b8BqCkCAgNomTmGDCrHjhkI0i5IvzCxGSoWZNVVE2tZJyZ0ExpjiVgDCQPGKzvNk7romNtGFE9SiGXjUyhhTifTH8iai8RZi'

        if app_id is not None and token is not None:
            env.set_key("APP_ID", app_id)
            env.set_key("TOKEN", token)

            return {"registration_info": "success", "data":{"app_id":app_id, "token":token} }        
        else:
            return {"registration_info": "failed"}


@router.get("/")
def get_register_info():
    data = get_app_registration_info()
    return data