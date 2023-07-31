import shutil, os
from utils.env import Env
from utils.minio_utils import MinioUtils
from utils.zipfile_utils import zip_files_and_remove, split_file_and_remove
from utils.s3_utils import S3Utils

minio_utils = MinioUtils()
env = Env()
s3_utils = S3Utils()


def get_free_disk_space():
    _, _, free = shutil.disk_usage("/")
    return free


def get_file_paths(filenames: list[str]) -> list[str]:
    paths = []

    for filename in filenames:
        try:
            # Check if the file exists in the current directory
            if os.path.isfile(filename):
                # Get the absolute path of the file
                paths.append(os.path.abspath(filename))
            else:
                print(f'File "{filename}" does not exist in the current directory.')
                paths.append(None)
        except Exception as e:
            # Catch any other exceptions, print the error message and set the path to None
            print(f'An error occurred while processing the file "{filename}": {str(e)}')
            paths[filename] = None

    return paths


def is_file_path_exceed_max_download_size(file_path: str) -> bool:
    max_download_size = env.get_value("MAX_DOWNLOAD_SIZE")
    file_size = os.path.getsize(file_path)
    if file_size > max_download_size:
        return True
    return False


def large_file_handling(
    task_id: str,
    path_name: str,
    include: list,
    version_id: int,
    unique_path_name: str,
) -> list[str]:
    minio_utils.download_objects(
        path_name,
        include,
        version_id=version_id,
    )
    file_path = get_file_paths(include)
    zip_file_path = zip_files_and_remove(file_path, task_id)
    zip_file_path = get_file_paths([task_id + ".zip"])
    split_file_path = split_file_and_remove(
        zip_file_path=zip_file_path, split_file_name=task_id
    )
    minio_utils.upload_objects_from_path_and_remove(
        unique_path_name,
        split_file_path,
    )
    download_path = [os.path.basename(path) for path in split_file_path]
    url = minio_utils.get_object_url_list(unique_path_name, download_path)
    return url


def large_file_handling_boto3(
    task_id: str,
    path_name: str,
    include: list,
    version_id: int,
    unique_path_name: str,
) -> list[str]:
    minio_utils.download_objects(
        path_name,
        include,
        version_id=version_id,
    )
    file_path = get_file_paths(include)
    zip_file_path = zip_files_and_remove(file_path, task_id)
    zip_file_path = get_file_paths([task_id + ".zip"])
    split_file_path = split_file_and_remove(
        zip_file_path=zip_file_path, split_file_name=task_id
    )
    minio_utils.upload_objects_from_path_and_remove(
        unique_path_name,
        split_file_path,
    )
    download_path = [os.path.basename(path) for path in split_file_path]
    url = minio_utils.get_object_url_list(unique_path_name, download_path)
    return url


def single_file_handling(
    path_name: str,
    include: list,
    version_id: int,
    unique_path_name: str,
) -> list[str]:
    if path_name.endswith("/") is False or unique_path_name.endswith("/") is False:
        path_name = path_name + "/"
        unique_path_name = unique_path_name + "/"
    if unique_path_name == "":
        object_name = path_name + include[0]
    else:
        object_name = unique_path_name + include[0]
    url = minio_utils.get_object_url_with_version_id(object_name, version_id)
    return url


def multiple_files_handling(
    task_id: str,
    path_name: str,
    include: list,
    version_id: int,
    unique_path_name: str,
) -> list[str]:
    minio_utils.download_objects(
        path_name,
        include,
        version_id=version_id,
    )
    if unique_path_name == "":
        upload_path = path_name
    else:
        upload_path = unique_path_name
    file_path = get_file_paths(include)
    zip_file_path = zip_files_and_remove(file_path, task_id)
    zip_file_path = get_file_paths([task_id + ".zip"])
    minio_utils.upload_objects_from_path_and_remove(
        upload_path,
        zip_file_path,
    )
    download_path = [os.path.basename(path) for path in zip_file_path]
    url = minio_utils.get_object_url_list(unique_path_name, download_path)
    return url


def is_file_size_exceed_max_download_size(file_size: int) -> bool:
    max_download_size = env.get_value("MAX_DOWNLOAD_SIZE")
    if file_size > max_download_size:
        return True
    return False


if __name__ == "__main__":
    # url = large_file_handling(
    #     task_id="2642eb77-1994-439a-85db-108e68a29d47",
    #     path_name="videos/",
    #     include=["Avengers.mp4", "Gigachad2.mp4"],
    #     version_id="",
    #     unique_path_name="videos_(1)/"
    # )
    # print(url)

    # url_single_file = single_file_handling(
    #     path_name="videos/",
    #     include=["Avengers.mp4"],
    #     version_id="",
    #     unique_path_name=""
    # )
    # print(url_single_file)

    url_multiple_files = multiple_files_handling(
        task_id="2642eb77-1994-439a-85db-108e68a29d47",
        path_name="pictures",
        include=["pic.jpg", "qr.jpg"],
        version_id="",
        unique_path_name="",
    )
    print(url_multiple_files)
