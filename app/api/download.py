from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import List
from celery import uuid
from app.api.models.file_path import FilePaths
from app.tasks.download_file import prepare_download
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/")
async def add_download_queue_dev(file_paths: List[FilePaths]):
    task_id_and_file_paths = {}

    for file_path in file_paths:
        task_id = uuid()
        expire_time = datetime.utcnow() + timedelta(
            hours=1
        )  # set default expire time to 1 hour for testing

        prepare_download.apply_async(
            (
                task_id,
                file_path.path_name,
                file_path.include,
                file_path.exclude,
                expire_time,
                file_path.version_id,
            ),
            task_id=task_id,
        )

        task_id_and_file_paths[task_id] = {
            "path": file_path.path_name,
            "include": file_path.include,
            "exclude": file_path.exclude,
            "expire_time": expire_time.isoformat(),
            "version_id": file_path.version_id,
        }

    return JSONResponse(task_id_and_file_paths)
