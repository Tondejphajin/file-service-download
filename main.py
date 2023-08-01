from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.api import download, health_check, ticket, register, license
from app.api import *

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

# def starter_process():
#     # check token and register app
#     register.register()
   
#     # get license
#     license.check_license()
#     # get and update health-check
#     health_check.update_health_check_record() 
    
# starter_process()