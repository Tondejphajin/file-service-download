from fastapi import APIRouter
from utils.env import Env
import requests

router = APIRouter()
env = Env()


def license_verificaiton() -> bool:
    app_id = env.get_value("APP_ID")
    token = env.get_value("TOKEN")
    url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/license?appid={app_id}&token={token}"

    response = requests.get(url=url)
    print(response.text)
    print(response.json())
    print(response.status_code)

    if response.status_code == 200:
        return True


@router.post("/")
async def check_license():
    is_verified = license_verificaiton()

    if is_verified:
        return {"license": "verified"}
    else:
        return {"license": "not verified"}
