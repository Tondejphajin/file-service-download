from fastapi import APIRouter
from utils.env import Env
import requests

router = APIRouter()
env = Env()

def license_verificaiton(app_id:str=None, token:str=None) -> bool:
    if not app_id and not token:
        app_id = env.get_value("APP_ID")
        token = env.get_value("TOKEN")
    
    if app_id and token:
        
        url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/license?appid={app_id}&token={token}"

        response = requests.get(url=url)
        
        if response.status_code == 200:
            return True
        
    return False

@router.post("/")
def check_license(app_id:str=None, token:str=None):
    is_verified = license_verificaiton(app_id, token)

    if is_verified:
        return {"license": "verified"}
    else:
        return {"license": "not verified"}
