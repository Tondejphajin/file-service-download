from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from celery.result import AsyncResult
from sse_starlette.sse import EventSourceResponse
from worker import app
from utils.env import Env
import asyncio, json

env = Env()
router = APIRouter()


@router.get("/{ticket_id}/status")
async def check_status(ticket_id: str, request: Request):
    response = AsyncResult(ticket_id, app=app)

    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            if response.ready():
                data = {
                    "message": "The file is ready",
                    "status": response.status,
                    "id": response.id,
                }
                yield f"data: {json.dumps(data)}\n\n"
                break
            else:
                data = {
                    "message": "Please wait for the file to be ready ... ",
                    "status": response.status,
                    "id": response.id,
                }
                yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(env.get_value("STREAM_DELAY"))

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/{ticket_id}/result")
async def get_result(ticket_id: str):
    response = AsyncResult(ticket_id, app=app)

    if response.ready():
        return {"result": response.get()}
    else:
        return {"error": "File not ready yet"}
