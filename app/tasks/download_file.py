from worker import app
from utils.minio_utils import MinioUtils
from utils.redis_utils import RedisUtils
from utils.s3_utils import S3Utils
from utils import tasks_utils, time_convert_utils, zipfile_utils

minio_utils = MinioUtils()
redis_utils = RedisUtils()
s3_utils = S3Utils()


@app.task
def prepare_download(
    task_id: str,
    path_name: str,
    include: list,
    exclude: list,
    raw_expired_time: int,
    version_id: str,
):
    # remove the trailing slash since the path_name in redis does not have it
    if path_name.endswith("/"):
        path_name = path_name.rstrip("/")

    # check if the request is cached
    redis_key, download_url = redis_utils.check_cached(
        path_name, include, exclude, version_id
    )

    if redis_key is None and download_url is None:
        # convert `raw_expired_time` to seconds, check if it is more than 0 seconds, and check if `version_id` is not None
        try:
            converted_expired_time = time_convert_utils.convert_raw_expired_time_to_sec(
                raw_expired_time
            )
        except Exception as e:
            converted_expired_time = 2147483647
        # cache the request and continue the download process
        redis_utils.cached_request(
            task_id, path_name, include, exclude, converted_expired_time, version_id
        )
    elif isinstance(redis_key, str):
        if isinstance(download_url, str):
            # return the url if the request is cached
            return download_url
        if download_url is None:
            # return the uuid if the request is cached but the url is not cached
            return redis_key
    else:
        return "Error cases"

    is_multiple_files = True if len(include) > 1 else False
    if is_multiple_files:
        # check if there are disk space available
        free_disk_space = tasks_utils.get_free_disk_space()
        multi_files_total_download_size = minio_utils.get_total_download_size(
            path_name, include
        )
        if free_disk_space > int(multi_files_total_download_size * 1.5):
            # download the files
            minio_utils.download_multiple_objects(path_name, include, version_id)
            # get the path of the downloaded files
            downloaded_files_path = tasks_utils.get_file_paths(include)
            # zip the files
            zip_file_path = zipfile_utils.zip_files_and_remove(
                downloaded_files_path, task_id
            )
            # check if the zip file is larger than max_download_size
            if tasks_utils.is_file_from_path_exceed_max_download_size(zip_file_path):
                # split the zip file
                zip_file_path = zipfile_utils.split_file_and_remove(
                    zip_file_path, task_id
                )
            # upload the zip file to minio
            minio_utils.upload_objects_from_path_and_remove(
                minio_path=task_id, local_file_path=zip_file_path
            )

            # get the download url
            download_url = minio_utils.get_objects_url_from_local_path(
                minio_path=task_id,
                local_path=zip_file_path,
                expire=converted_expired_time,
                version_id=version_id,
            )

            # update cache on Redis
            redis_utils.update_hash_from_url_list(task_id, download_url)
            redis_utils.cached_last_modified(task_id, path_name)
            return download_url
        else:
            return "Not enough disk space"
    else:
        # check if the file is larger than max_download_size
        single_file_total_download_size = minio_utils.get_total_download_size(
            path_name, include
        )
        if tasks_utils.is_file_size_exceed_max_download_size(
            single_file_total_download_size
        ):
            # download the file
            minio_utils.download_multiple_objects(path_name, include, version_id)
            # get the path of the downloaded file
            downloaded_file_path = tasks_utils.get_file_paths(include)
            # zip the file
            zip_file_path = zipfile_utils.zip_files_and_remove(
                downloaded_file_path, task_id
            )
            # split the zip file
            zip_file_path = zipfile_utils.split_file_and_remove(zip_file_path, task_id)
            # upload the zip file to minio
            minio_utils.upload_objects_from_path_and_remove(
                minio_path=task_id, local_file_path=zip_file_path
            )
            # get the download url
            download_url = minio_utils.get_objects_url_from_local_path(
                minio_path=task_id,
                local_path=zip_file_path,
                expire=converted_expired_time,
                version_id=version_id,
            )
            # update cache on Redis
            redis_utils.update_hash_from_url_list(task_id, download_url)
            redis_utils.cached_last_modified(task_id, path_name)
            return download_url
        else:
            # get the download url
            download_url = minio_utils.get_object_url_from_list(
                path_name, include, converted_expired_time, version_id
            )
            # update cache on Redis
            redis_utils.update_hash_from_url_list(task_id, download_url)
            redis_utils.cached_last_modified(task_id, path_name)
            return download_url
