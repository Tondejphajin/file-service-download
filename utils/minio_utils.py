from minio import Minio
from utils.env import Env
from minio.lifecycleconfig import (
    LifecycleConfig,
    Rule,
    Expiration,
    Transition,
)
from minio.commonconfig import ENABLED, Filter, Tags
from minio.versioningconfig import VersioningConfig
import os

env = Env()


class MinioClient:
    def __init__(self) -> None:
        self.client = Minio(
            env.get_value("MINIO_URL"),
            access_key=env.get_value("MINIO_ACCESS_KEY"),
            secret_key=env.get_value("MINIO_SECRET_KEY"),
            secure=False,
        )
        # self.client = Minio(
        #     os.getenv("MINIO_URL"),
        #     access_key=os.getenv("MINIO_SERVER_ACCESS_KEY"),
        #     secret_key=os.getenv("MINIO_SERVER_SECRET_KEY"),
        # )
        self.bucket_name = env.get_value("MINIO_BUCKET_NAME")

    def get_client(self) -> Minio:
        return self.client

    def get_bucket_name(self) -> str:
        return self.bucket_name

    def set_bucket_name(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name


class MinioUtils(MinioClient):
    def __init__(self) -> None:
        super().__init__()
        # self.client.set_bucket_versioning(self.bucket_name, VersioningConfig(ENABLED))

    def generate_unique_path_name(self, path_name: str) -> str:
        all_path = self.client.list_objects(self.bucket_name)
        path_name = path_name.split("/")[0]
        uploaded_path = path_name
        counter = 0
        for path in all_path:
            if path.object_name.startswith(path_name):
                counter += 1
                uploaded_path = path_name.rstrip("/") + "_(" + str(counter) + ")" + "/"
        return uploaded_path

    def check_object_exists(self, object_name: str) -> bool:
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except:
            return False

    def check_object_exists_from_api(
        self, path_name: str, include: list, exclude: list
    ) -> bool:
        requested_objects = include + exclude
        if path_name.endswith("/") is False:
            path_name = path_name + "/"
        for object in requested_objects:
            object_name = path_name + object
            try:
                self.client.stat_object(self.bucket_name, object_name)
            except Exception as e:
                return False
        return True

    def get_object_url(self, object_name: str) -> str:
        return self.client.presigned_get_object(self.bucket_name, object_name)

    def get_object_url_with_version_id(self, object_name: str, version_id: str) -> str:
        return self.client.presigned_get_object(
            self.bucket_name, object_name, version_id=version_id
        )

    def get_object_url_list(
        self, minio_path: str, object_name_list: list[str]
    ) -> list[str]:
        if minio_path.endswith("/") is False:
            minio_path = minio_path + "/"
        urls = []
        for object_name in object_name_list:
            urls.append(
                self.client.presigned_get_object(
                    self.bucket_name, minio_path + object_name
                )
            )
        return urls

    def get_objects_url_from_local_path(
        self, minio_path: str, local_path: list[str]
    ) -> list[str]:
        urls = []
        for path in local_path:
            object_name = os.path.basename(path)
            urls.append(
                self.client.presigned_get_object(
                    self.bucket_name, minio_path + object_name
                )
            )
        return urls

    def upload_object(self, minio_path: str, local_file_path: str) -> None:
        minio_path = minio_path + local_file_path.split("/")[-1]
        try:
            self.client.fput_object(self.bucket_name, minio_path, local_file_path)
        except Exception as e:
            raise e

    def upload_objects_from_path_and_remove(
        self, minio_path: str, local_file_path: list[str]
    ) -> None:
        for i in range(0, len(local_file_path)):
            object_name = os.path.basename(local_file_path[i])
            try:
                self.client.fput_object(
                    self.bucket_name, minio_path + object_name, object_name
                )
                os.remove(local_file_path[i])
            except Exception as e:
                raise e

    def download_object(
        self, minio_path: str, download_file_name: str, version_id: str = None
    ) -> None:
        try:
            self.client.fget_object(
                self.bucket_name, minio_path, download_file_name, version_id=version_id
            )
        except Exception as e:
            raise e

    def download_objects(
        self, minio_paths: str, include: list[str], version_id: str = ""
    ) -> None:
        if minio_paths.endswith("/") is False:
            minio_paths = minio_paths + "/"
        for i in range(0, len(include)):
            download_path = minio_paths + include[i]
            download_file_name = include[i]
            try:
                self.client.fget_object(
                    self.bucket_name,
                    download_path,
                    download_file_name,
                    version_id=version_id,
                )
            except Exception as e:
                raise e

    def set_lifecycle(self, minio_path: str, days: int) -> None:
        config = LifecycleConfig(
            [
                Rule(
                    ENABLED,
                    rule_filter=Filter(prefix=minio_path),
                    rule_id="rule1",
                    expiration=Expiration(days=days),
                ),
            ],
        )
        self.client.set_bucket_lifecycle(self.bucket_name, config)

    def get_total_download_size(self, minio_path: str, include: list) -> int:
        if minio_path.endswith("/") is False:
            minio_path = minio_path + "/"
        total_size = 0
        for object in include:
            object_name = minio_path + object
            try:
                total_size += self.client.stat_object(
                    self.bucket_name, object_name
                ).size
            except Exception as e:
                raise e
        return total_size

    def is_object_larger_than_max_download_size(self, object_path: str) -> bool:
        max_download_size = env.get_value("MAX_DOWNLOAD_SIZE")
        total_size = self.client.stat_object(self.bucket_name, object_path).size
        if total_size > max_download_size:
            return True
        return False

    def remove_object(self, object_path: str) -> None:
        try:
            self.client.remove_object(self.bucket_name, object_path)
        except Exception as e:
            raise e

    def list_objects(self, path_name: str) -> list:
        objects = self.client.list_objects(self.bucket_name, prefix=path_name)
        return objects

    def get_all_path(self, path_name: str) -> list:
        objects = self.client.list_objects(self.bucket_name, prefix=path_name)
        object_list = []
        for object in objects:
            object_list.append(object.object_name)
        return object_list


if __name__ == "__main__":
    minio_client = MinioUtils()
    # unique_path_name = minio_client.generate_unique_path_name("videos/")
    # print(unique_path_name)

    # path = os.path.join(os.getcwd(), "upload\\Avengers.mp4")
    # print(path)
    # version_id = minio_client.client.fput_object(
    #     minio_client.bucket_name, "Avengers.mp4", path
    # )
    # print(version_id.version_id)

    # version_id = minio_client.client.fput_object(
    #     minio_client.bucket_name, "Avengers.mp4", path
    # )
    # print(version_id.version_id)

    # version_id = minio_client.client.fput_object(
    #     minio_client.bucket_name, "Avengers.mp4", path
    # )
    # print(version_id.version_id)

    # minio_client.client.fget_object(
    #     minio_client.bucket_name,
    #     "Avengers.mp4",
    #     "Avengers.mp4",
    #     version_id="9416866d-c7e3-4157-8895-69ee944faf7d",
    # )
    # minio_client.download_objects(minio_paths="videos/", include=["Avengers.mp4"])

    # file_name_and_version_id = {}
    # path = "videos"
    # all_video_path = minio_client.get_all_path(path)
    # for object in all_video_path:
    #     print(object)
    #     objects = minio_client.list_objects(object)
    #     for object in objects:
    #         print(object)
    #         print(object.object_name)
    #         print(object.last_modified)
    #         print(object.version_id)
    #         print("-" * 50)
    #         file_name = object.object_name.split("/")[-1]
    #         file_name_and_version_id[file_name] = object.last_modified
    # print(file_name_and_version_id)
    minio_client.download_object(
        minio_path="videos/Twitter.mp4",
        download_file_name="Twitter.mp4",
        version_id="7f9900cd-bafa-4154-9e30-c7f304d1c127",
    )
