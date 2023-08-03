from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api import download, health_check, ticket, register, license
import time

# def starter_process():
#     # check token and register app
#     result = register.register()
    
#     if result and result['registration_info'] != "failed":
#         app_id, token = result['data']['app_id'], result['data']['token']
        
#         time.sleep(2)
#         # get license
#         license.check_license(app_id, token)
#         # get and update health-check
#         health_check.update_health_check_record(app_id, token) 

# starter_process()

app = FastAPI()

app.include_router(download.router, prefix="/appapi/v1/download", tags=["download"])
app.include_router(ticket.router, prefix="/appapi/v1/ticket", tags=["ticket"])
app.include_router(register.router, prefix="/appapi/v1/app", tags=["register"])
app.include_router(
    health_check.router, prefix="/appapi/v1/health-check", tags=["healthcheck"]
)
app.include_router(license.router, prefix="/appapi/v1/license", tags=["license"])

@app.get("/")
async def root():
    return FileResponse("app/api/templates/index.html")



