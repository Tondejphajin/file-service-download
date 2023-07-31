from worker import app
from utils.minio_utils import MinioUtils
from utils.redis_utils import RedisUtils
from utils import tasks_utils, zipfile_utils, time_utils
from datetime import datetime, timedelta

minio_utils = MinioUtils()
redis_utils = RedisUtils()


@app.task
def prepare_download(
    task_id: str,
    path_name: str,
    include: list,
    exclude: list,
    raw_expired_time: int,
    version_id: int,
):
    # convert `raw_expired_time` to seconds, check if it is more than 0 seconds, and check if `version_id` is not None
    coverted_expired_time = time_utils.convert_raw_expired_time_to_sec(raw_expired_time)
    has_expired_time = True if coverted_expired_time > 0 else False
    has_version_id = True if version_id != "" else False

    # check if the request is cached
    key, is_request_cached = redis_utils.is_request_cached(
        task_id, path_name, include, exclude, version_id
    )
    if key is not None and is_request_cached:
        # if the request is cached, return the url
        url = redis_utils.client.hget(key, "url")
        return url
    elif key is not None and is_request_cached is False:
        # if the request is cached but the url is not cached, return uuid
        return key
    elif key is None and is_request_cached is False:
        # if the request is not cached, cache the request and continue the download process
        redis_utils.cached_request(
            task_id, path_name, include, exclude, coverted_expired_time, version_id
        )

    # check if all object in `list` and in `exclude` exists in path_name
    check_object_exists = minio_utils.check_object_exists_from_api(
        path_name, include, exclude
    )
    if check_object_exists is False:
        redis_utils.client.delete(task_id)
        return "There are objects that do not exist in the requested path, please check your request again"

    # check if there is enough disk space to download the `include`` files
    free_disk_space = tasks_utils.get_free_disk_space()
    total_download_size = minio_utils.get_total_download_size(path_name, include)
    if free_disk_space < int(total_download_size * 1.5):
        redis_utils.client.delete(task_id)
        return "Not enough disk space"

    # Download the files
    unique_path_name = minio_utils.generate_unique_path_name(path_name)
    is_exceed_max_download = (
        True
        if tasks_utils.is_file_size_exceed_max_download_size(total_download_size)
        else False
    )
    is_multiple_files = True if len(include) > 1 else False
    if is_multiple_files is True:
        if is_exceed_max_download:
            url = tasks_utils.large_file_handling(
                task_id,
                path_name,
                include,
                version_id,
                unique_path_name,
            )
        else:
            url = tasks_utils.multiple_files_handling(
                task_id,
                path_name,
                include,
                version_id,
                unique_path_name,
            )
    elif is_multiple_files is False:
        if is_exceed_max_download:
            url = tasks_utils.large_file_handling(
                task_id,
                path_name,
                include,
                version_id,
                unique_path_name,
            )
        else:
            url = tasks_utils.single_file_handling(
                include, version_id, unique_path_name
            )
    redis_utils.update_hash_from_url_list(task_id, url)
    if has_expired_time:
        if coverted_expired_time > 86000:
            minio_utils.set_lifecycle(unique_path_name, coverted_expired_time)
        redis_utils.client.expire(task_id, coverted_expired_time)
    return url


if __name__ == "__main__":
    # task_id = "uuid1"
    # path_name = "videos/"
    # include = ["Avengers.mp4"]
    # exclude = ["High Harry.mp4"]
    # expire_time = 3600

    # Test 1:
    # task_id = "uuid1"
    # path_name = "videos/"
    # include = ["Avengers.mp4", "High Harry.mp4"]
    # exclude = []
    # expire_time = datetime.utcnow() + timedelta(hours=1)
    # version_id = None

    # prepare_download(task_id, path_name, include, exclude, expire_time, version_id)

    # Test 2:
    # task_id = "uuid30"
    # path_name = "file_path"
    # include = ["include_json"]
    # exclude = ["exclude_json"]
    # expire_time = 3600
    # version_id = ""

    # result = prepare_download(
    #     task_id, path_name, include, exclude, expire_time, version_id
    # )
    # print(result)

    # Test3:
    task_id = "uuid002"
    path_name = "videos"
    include = ["Avengers.mp4"]
    exclude = []
    expire_time = datetime.utcnow() + timedelta(hours=1)
    version_id = ""

    result = prepare_download(
        task_id, path_name, include, exclude, expire_time, version_id
    )
    print(result)
    print(type(result))
