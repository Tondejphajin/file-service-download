from app.tasks.download_file import prepare_download
from datetime import datetime, timedelta


def test_download_multiples_pictures():
    task_id = "uuid001"
    path_name = "pictures"
    include = ["pic.jpg", "qr.jpg"]
    exclude = []
    expire_time = datetime.now() + timedelta(days=1)
    version_id = ""

    prepare_download(task_id, path_name, include, exclude, expire_time, version_id)


if __name__ == "__main__":
    test_download_multiples_pictures()
