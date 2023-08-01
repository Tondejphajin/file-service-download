from fastapi import APIRouter, HTTPException
from utils.minio_utils import MinioClient
from utils.redis_utils import RedisClient
from utils.env import Env
import subprocess, requests

router = APIRouter()
env = Env()


def check_minio() -> bool:
    minio_client = MinioClient()
    if not minio_client.client.bucket_exists(minio_client.bucket_name):
        raise HTTPException(status_code=500, detail="MinIO not available")
    return True

def check_redis() -> bool:
    try:
        redis_client = RedisClient()
        redis_client.client.ping()
    except:
        raise HTTPException(status_code=500, detail="Redis not available")
    return True

def check_worker() -> bool:
    worker_file_name = "worker"
    command = f"celery -A {worker_file_name} status"
    worker_response = subprocess.run(
        command, shell=True, check=True, capture_output=True
    )
    if worker_response.returncode != 0:
        raise HTTPException(status_code=500, detail="Celery worker not available")
    return True

def patch_health_check(payload:dict, app_id:str=None, token:str=None):
    if not app_id:
        app_id = env.get_value('APP_ID')

    if not token:
        token = env.get_value('TOKEN')

    if app_id and token:
        health_id = payload['healthid']

        url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/health-check/{health_id}?appid={app_id}&token={token}"
        response = requests.patch(url=url, json=payload)

        if response.json()["is_online"] != True:
            return HTTPException(status_code=500, detail="Server is not available")

        return response.json()["is_online"]

    return HTTPException(status_code=500, detail="app id or token are not available.")

def get_health_check(app_id:str=None, token:str=None):
    if not app_id:
        app_id = env.get_value('APP_ID')

    if not token:
        token = env.get_value('TOKEN')

    if app_id and token:
        url = f"{env.get_value('APP_REGISTER_DOMAIN')}/appapi/v1/health-check?appid={app_id}&token={token}"
        response = requests.get(url=url)

        if response.status_code != 200:
            return HTTPException(status_code=500, detail="Server is not available")

        return response.json()[0]
    
    return HTTPException(status_code=500, detail="app id or token are not available.")

@router.get("/services")
async def get_services_status():
    if check_minio() and check_redis() and check_worker():
        return {"status": "all services are online"}

@router.get("/")
async def get_health_check_record():
    get_response = get_health_check()
    return {"status": get_response}

@router.patch("/")
def update_health_check_record(app_id:str=None, token:str=None):
    get_response = get_health_check(app_id, token)
    
    if isinstance(get_response, dict) and get_response["is_online"] != True:

        # update health check status
        get_response["is_online"] = True

        patch_response = patch_health_check(get_response)
        return {"status": patch_response}
    return get_response
