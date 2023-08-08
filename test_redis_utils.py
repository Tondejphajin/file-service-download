from utils.redis_utils import RedisUtils
from datetime import datetime, timedelta


if __name__ == "__main__":
    redis_utils = RedisUtils()

    default_expired_time = datetime.utcnow() + timedelta(days=1)
    file_path_1 = {
        "path_name": "videos",
        "include": ["cat.mp4", "dog.mp4"],
        "exclude": [],
        "expired_time": default_expired_time.isoformat(),
        "version_id": "",
    }

    file_path_2 = {
        "path_name": "documents",
        "include": ["report.pdf", "hw.pdf"],
        "exclude": [],
        "expired_time": default_expired_time.isoformat(),
        "version_id": "",
    }

    file_path_3 = {
        "path_name": "pictures",
        "include": ["qr.jpg", "me.jpg"],
        "exclude": [],
        "expired_time": default_expired_time.isoformat(),
        "version_id": "",
    }

    file_path_4 = {
        "path_name": "pictures",
        "include": ["me.jpg", "qr.jpg"],
        "exclude": [],
        "expired_time": default_expired_time.isoformat(),
        "version_id": "",
    }

    file_paths = [file_path_1, file_path_2, file_path_3]

    redis_utils.cached_request_multiple_paths("test", file_paths)

    file_paths_duplicate = [file_path_1, file_path_2, file_path_4]

    result = redis_utils.check_cached_multiple_paths(file_paths_duplicate)
    print(result)
