from worker import app
from utils.minio_utils import MinioUtils
from utils.redis_utils import RedisUtils

minio_utils = MinioUtils()
redis_utils = RedisUtils()


@app.task
def delete_minio_file(
    result_from_previous_task, key: str, file_path: str, include: list[str]
):
    for file in include:
        object_path = file_path + file
        if redis_utils.listening_for_expired_specific_key(key):
            minio_utils.remove_object(object_path)

    return result_from_previous_task


if __name__ == "__main__":
    delete_minio_file("uuid3", "videos/Avengers6.mp4")
