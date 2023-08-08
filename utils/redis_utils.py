import redis, json, datetime
from utils.env import Env
from utils.s3_utils import S3Utils
from app.api.models import FilePaths
from datetime import datetime, timedelta, timezone


env = Env()
s3_utils = S3Utils()


class RedisClient:
    def __init__(self) -> None:
        self.client = redis.Redis(
            host=env.get_value("REDIS_HOST"),
            port=env.get_value("REDIS_PORT"),
            decode_responses=True,
        )

    def get_client(self) -> redis.Redis:
        return self.client


class RedisUtils(RedisClient):
    def __init__(self) -> None:
        super().__init__()
        self.client.config_set("notify-keyspace-events", "Ex")

    def hset_from_dict(
        self, key: str, hash_dict: dict
    ) -> None:  # hmset (deprecated in v4.00)
        for hash_key, hash_value in hash_dict.items():
            self.client.hset(key, hash_key, hash_value)

    def listening_for_expired_keys(self) -> None:
        pubsub = self.client.pubsub()
        pubsub.psubscribe("__keyevent@0__:expired")
        for message in pubsub.listen():
            print(message)

    def listening_for_expired_specific_key(self, key: str) -> bool:
        pubsub = self.client.pubsub()
        pubsub.psubscribe("__keyevent@0__:expired")

        while True:
            message = pubsub.get_message()
            if message:
                key_expired = message["data"]
                if key_expired == key:
                    print("Key expired: ", key_expired)
                    break
        return True

    def check_cached(
        self, file_path: str, include: list, exclude: list, version_id: str
    ) -> tuple[str, str]:
        task_id, download_url = None, None

        all_keys = self.client.keys()
        for key in all_keys:
            if self.client.type(key) == "hash":  # Check if key is a hash
                same_path = (
                    True if file_path == self.client.hget(key, "path") else False
                )
                include_field = self.client.hget(key, "include")
                if include_field is None:
                    same_include = False
                else:
                    same_include = (
                        True
                        if set(include)
                        == set(json.loads(self.client.hget(key, "include")))
                        else False
                    )
                exclude_field = self.client.hget(key, "exclude")
                if exclude_field is None:
                    same_exclude = False
                else:
                    same_exclude = (
                        True
                        if set(exclude)
                        == set(json.loads(self.client.hget(key, "exclude")))
                        else False
                    )
                same_version_id = (
                    True if version_id == self.client.hget(key, "version_id") else False
                )

                if same_path and same_include and same_exclude and same_version_id:
                    if self.client.hget(key, "version_id") == "":
                        # check if the `include` files are the latest version
                        has_last_modified = (
                            True if self.client.hexists(key, "last_modified") else False
                        )
                        if has_last_modified:
                            # get the last modified of the path on minio

                            last_modified_redis_str = self.client.hget(
                                key, "last_modified"
                            )
                            last_modified_redis_obj = datetime.datetime.fromisoformat(
                                last_modified_redis_str
                            )
                            (
                                _,
                                last_modified_minio_obj,
                            ) = s3_utils.get_object_version_and_last_modified(file_path)

                            if last_modified_minio_obj > last_modified_redis_obj:
                                # update version_id on redis and continue the download process
                                all_version_and_modified = (
                                    s3_utils.get_object_all_version_and_last_modified(
                                        file_path
                                    )
                                )
                                # print("DATA_DICT:", all_version_and_modified)

                                last_modified_list = list(
                                    all_version_and_modified.keys()
                                )
                                # print("DATA_LIST:", last_modified_list)

                                for last_modified in last_modified_list:
                                    # convert string to datetime object
                                    last_modified_obj = datetime.datetime.fromisoformat(
                                        last_modified
                                    )
                                    # compare the last modified of the path on minio with the last modified on redis
                                    if last_modified_redis_obj == last_modified_obj:
                                        # get the correct version_id
                                        last_modified_redis_str = (
                                            last_modified_redis_obj.isoformat()
                                        )
                                        new_version_id = all_version_and_modified.get(
                                            last_modified_redis_str, "null"
                                        )

                                        # update the version_id on redis
                                        self.client.hset(
                                            key,
                                            "version_id",
                                            new_version_id,
                                        )

                                return None, None
                            elif last_modified_minio_obj == last_modified_redis_obj:
                                task_id = key
                                # the file is cached and ready to be downloaded
                                download_url = self.client.hget(key, "url")
                                return task_id, download_url
                            else:  # impossible case
                                return None, None
                        else:
                            task_id = key
                            download_url = None
                            return task_id, download_url
                    else:
                        if self.client.hexists(key, "url"):
                            task_id = key
                            download_url = self.client.hget(key, "url")
                            return task_id, None
                        else:
                            return None, None
        return task_id, download_url

    def check_current_last_modified(self, path_name: str, redis_key: str) -> bool:
        object_data = s3_utils.get_all_object_version_and_last_modified(path_name)
        redis_last_modified = self.client.hget(redis_key, "last_modified")
        for version_id, last_modified in object_data.items():
            if last_modified == redis_last_modified:
                return version_id, True
        return None, False

    def update_hash_from_url_list(self, key: str, url: list[str]) -> None:
        url = json.dumps(url)
        self.client.hset(key, "url", url)

    def cached_request(
        self,
        key: str,
        file_path: str,
        include: list,
        exclude: list,
        expire_time: int,
        version_id: int,
    ) -> None:
        field_values = {
            "path": file_path,
            "include": json.dumps(include),
            "exclude": json.dumps(exclude),
            # "url": "",
            "expired_time": expire_time,
            "version_id": version_id,
        }
        self.client.hset(key, mapping=field_values)
        self.client.expire(key, expire_time)

    def cached_last_modified(self, key: str, path_name: str) -> None:
        path_last_modified = s3_utils.get_object_version_and_last_modified(path_name)
        path_last_modified = path_last_modified[1]
        self.client.hset(key, "last_modified", path_last_modified.isoformat())

    def cached_request_multiple_paths(
        self, key: str, file_paths: list[FilePaths]
    ) -> None:
        self.client.hset(key, "request", json.dumps(file_paths))

    def check_cached_multiple_paths(self, request1: list[FilePaths]) -> bool:
        request2 = json.loads(self.client.hget("test", "request"))

        if len(request1) != len(request2):
            return False

        for dict1, dict2 in zip(request1, request2):
            if dict1["path_name"] != dict2["path_name"]:
                return False
            if sorted(dict1["include"]) != sorted(dict2["include"]):
                return False
            if sorted(dict1["exclude"]) != sorted(dict2["exclude"]):
                return False
            if dict1["expired_time"] != dict2["expired_time"]:
                return False
            if dict1["version_id"] != dict2["version_id"]:
                return False

        return True
