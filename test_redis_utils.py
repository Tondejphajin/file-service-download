from utils.redis_utils import RedisUtils
from datetime import datetime, timedelta
import uuid


class TestRedisUtils:
    def __init__(self):
        self.redis_utils = RedisUtils()
        self.default_expired_time = datetime.utcnow() + timedelta(days=1)

        self.file_path_1 = {
            "path_name": "videos",
            "include": ["Go.mp4", "Slides.pdf"],
            "exclude": [],
            "expired_time": self.default_expired_time.isoformat(),
            "version_id": "",
        }

        self.file_path_2 = {
            "path_name": "documents",
            "include": ["Cap1.1.pdf", "MD5.pdf"],
            "exclude": [],
            "expired_time": self.default_expired_time.isoformat(),
            "version_id": "",
        }

        self.file_path_3 = {
            "path_name": "pictures",
            "include": ["qr.jpg", "pic.jpg"],
            "exclude": [],
            "expired_time": self.default_expired_time.isoformat(),
            "version_id": "",
        }

    def test_multiple_paths_cache(self):
        all_requested_path = [self.file_path_1, self.file_path_2, self.file_path_3]
        requested_paths = {}

        for path in all_requested_path:
            path_id = str(uuid.uuid4())
            requested_paths[path_id] = path

        redis_key = str(uuid.uuid4())

        send_to_redis = {
            "id": redis_key,
            "data": requested_paths,
        }

        self.redis_utils.cached_multiple_paths_request(send_to_redis)


if __name__ == "__main__":
    redis_utils = TestRedisUtils()
    redis_utils.test_multiple_paths_cache()
