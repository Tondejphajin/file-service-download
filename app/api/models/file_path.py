from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta, timezone


class FilePaths(BaseModel):
    path_name: str
    include: Optional[List[str]] = []
    exclude: Optional[List[str]] = []
    expire_time: Optional[datetime] = datetime.utcnow()
    version_id: Optional[str] = ""


if __name__ == "__main__":
    file_paths = FilePaths(
        path_name="path1",
        include=["fileA", "fileB"],
        exclude=["fileC", "fileD"],
        expire_time=datetime.utcnow() + timedelta(hours=1),
    )

    expire_time = datetime.utcnow()
    print(expire_time)
    expire_time = expire_time + timedelta(hours=1)
    print(expire_time)
    expire_time_seconds = int(expire_time.timestamp())
    print(expire_time_seconds)
    print(datetime.utcfromtimestamp(expire_time_seconds))

    print("-" * 50)

    expire_time = datetime.utcnow()
    print(expire_time)
    expire_time = expire_time + timedelta(days=1)
    print(expire_time)
    expire_time_seconds = int(expire_time.timestamp())
    print(expire_time_seconds)
    print(datetime.fromtimestamp(expire_time_seconds, timezone.utc))

    print("-" * 50)

    time_A = datetime.utcnow() + timedelta(hours=1)
    time_B = datetime.utcnow() + timedelta(hours=2)
    time_diff = int(time_B.timestamp()) - int(time_A.timestamp())
    print(time_diff)
    print(type(time_diff))
