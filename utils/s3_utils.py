import datetime, boto3, os, logging
from utils.env import Env
from botocore.exceptions import ClientError

env = Env()


class S3Client:
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            endpoint_url=env.get_value("S3_URL"),
            aws_access_key_id=env.get_value("S3_ACCESS_KEY"),
            aws_secret_access_key=env.get_value("S3_SECRET_KEY"),
            config=boto3.session.Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
        self.bucket_name = env.get_value("S3_BUCKET_NAME")
        self.enable_versioning()

    def enable_versioning(self):
        self.client.put_bucket_versioning(
            Bucket=self.bucket_name, VersioningConfiguration={"Status": "Enabled"}
        )


class S3Utils(S3Client):
    def __init__(self) -> None:
        super().__init__()

    def get_object_version_and_last_modified(self, object_name: str) -> tuple[str, str]:
        try:
            response = self.client.list_object_versions(
                Bucket=self.bucket_name, Prefix=object_name
            )
            version_id = response["Versions"][0]["VersionId"]
            last_modified = response["Versions"][0]["LastModified"]
            return version_id, last_modified
        except ClientError as e:
            logging.error(e)
            return None, None

    def get_all_object_version_and_last_modified(
        self, prefix: str
    ) -> dict[str, datetime.datetime]:
        mapping = {}
        response = self.client.list_object_versions(
            Bucket=self.bucket_name, Prefix=prefix
        )
        for obj_version in response.get("Versions", []):
            mapping[obj_version["VersionId"]] = obj_version["LastModified"]
        return mapping

    def upload_file(
        self, file_name: str, object_name: str = None, path_name: str = None
    ) -> tuple[str, datetime.datetime]:
        if object_name is None:
            object_name = os.path.basename(file_name)

        if path_name is not None:
            if path_name.endswith("/") is False:
                path_name = path_name + "/"
            object_name = path_name + object_name

        try:
            with open(file_name, "rb") as data:
                response = self.client.put_object(
                    Bucket=self.bucket_name, Key=object_name, Body=data
                )
            version_id = response.get("VersionId", None)

            object_head = self.client.head_object(
                Bucket=self.bucket_name, Key=object_name, VersionId=version_id
            )
            last_modified = object_head["LastModified"]

            return version_id, last_modified
        except ClientError as e:
            logging.error(e)
            return None, None

    def upload_files_and_remove(
        self, file_name: str, object_name: str = None, path_name: str = None
    ):
        file_name_and_version_id = {}
        file_name_and_last_modified = {}
        if object_name is None:
            object_name = os.path.basename(file_name)

        if path_name is not None:
            if path_name.endswith("/") is False:
                path_name = path_name + "/"
            object_name = path_name + object_name

        try:
            with open(file_name, "rb") as data:
                response = self.client.put_object(
                    Bucket=self.bucket_name, Key=object_name, Body=data
                )
            version_id = response.get("VersionId", None)

            object_head = self.client.head_object(
                Bucket=self.bucket_name, Key=object_name, VersionId=version_id
            )
            last_modified = object_head["LastModified"]

            file_name_and_version_id[os.path.basename(file_name)] = version_id
            file_name_and_last_modified[file_name] = last_modified

            return file_name_and_version_id, file_name_and_last_modified
        except ClientError as e:
            logging.error(e)
            return None, None

    def delete_file(self, object_name: str) -> None:
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name,
            )
        except ClientError as e:
            logging.error(e)


if __name__ == "__main__":
    s3_utils = S3Utils()

    # file_path = r"D:\Downloads\Twitter.mp4"
    # version_id, last_modified = s3_utils.upload_file(file_path, path_name="videos")
    # print(version_id, last_modified)
    # s3_utils.client.delete_object(
    #     Bucket=s3_utils.bucket_name,
    #     Key="videos/Twitter.mp4",
    # )
    x, y = s3_utils.get_object_version_and_last_modified("videos")
    print(x, y)
