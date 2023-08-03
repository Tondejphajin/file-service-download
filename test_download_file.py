from app.tasks.download_file import prepare_download
from datetime import datetime, timedelta

task_id = "uuid1"
path_name = "videos/"
include = ["Avengers.mp4", "Slides.pdf"]
exclude = []
expire_time = datetime.utcnow() + timedelta(hours=1)
version_id = ""

response = prepare_download(
    task_id, path_name, include, exclude, expire_time, version_id
)
print(response)
