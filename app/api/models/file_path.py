from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta, timezone


class FilePaths(BaseModel):
    path_name: str
    include: Optional[List[str]] = []
    exclude: Optional[List[str]] = []
    expired_time: Optional[datetime] = datetime.utcnow() + timedelta(days=1)
    version_id: Optional[str] = ""
