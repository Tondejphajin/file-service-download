import redis, json
from utils.env import Env
from utils.s3_utils import S3Utils

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

    def is_request_cached(
        self, file_path: str, include: list, exclude: list, version_id: str
    ) -> tuple[str, bool]:
        all_keys = self.client.keys()
        for key in all_keys:
            if self.client.type(key) == "hash":  # Check if key is a hash
                is_path_the_same = (
                    True if file_path == self.client.hget(key, "path") else False
                )
                is_include_the_same = (
                    True
                    if set(include) == set(json.loads(self.client.hget(key, "include")))
                    else False
                )
                is_exclude_the_same = (
                    True
                    if set(exclude) == set(json.loads(self.client.hget(key, "exclude")))
                    else False
                )
                is_version_id_same = (
                    True if version_id == self.client.hget(key, "version_id") else False
                )
                has_last_modified = (
                    True if self.client.hexists(key, "last_modified") != "" else False
                )
                # print(
                #     f"key: {key}, type: {self.client.type(key)}, file_path: {file_path}, include: {include}, exclude: {exclude}, version_id: {version_id}"
                # )
                # print(f"is_hash: True")
                # print(f"is_path_the_same: {bool_is_path_the_same}")
                # print(f"is_include_the_same: {bool_is_include_the_same}")
                # print(f"is_exclude_the_same: {bool_is_exclude_the_same}")
                # print(f"is_version_id_the_same: {bool_version_id_the_same}")
                # print("-" * 50)
                if (
                    is_path_the_same
                    and is_include_the_same
                    and is_exclude_the_same
                    and is_version_id_same
                ):
                    # if self.client.hget(key, "url") == "":
                    #     return key, False
                    # else:
                    #     return key, True
                    if has_last_modified:
                        change_version_id, is_same = self.check_current_last_modified(
                            file_path, key
                        )
                        if change_version_id is not None and is_same:
                            self.client.hset(key, "version_id", change_version_id)
                            return key, True
                    else:
                        return key, False
        return None, False

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
            "expire_time": expire_time,
            "version_id": version_id,
        }
        self.client.hset(key, mapping=field_values)
        self.client.expire(key, expire_time)


if __name__ == "__main__":
    redis_client = RedisUtils()
    # hash_dict = {
    #     "path": "file_path",
    #     "include": json.dumps(["include_json"]),
    #     "exclude": json.dumps(["exclude_json"]),
    #     "url": -1,
    #     "expire_time": 3600,
    # }
    # redis_client.hset_from_dict("uuid69", hash_dict)
    # print(redis_client.client.hgetall("uuid69"))
    # print(type(redis_client.client.hget("uuid69", "url")))
    # url = ["url1", "url2", "url3"]
    # url = json.dumps(url)
    # redis_client.client.hset("uuid69", "url", url)
    # print(redis_client.client.hgetall("uuid69"))

    # print(type(json.loads(redis_client.client.hget("uuid69", "url"))))

    # key = "uuid69"
    # file_path = "file_path"
    # include = ["include_json"]
    # exclude = ["exclude_json"]
    # version_id = ""
    # key, is_cached = redis_client.is_request_cached(
    #     key=key,
    #     file_path=file_path,
    #     include=include,
    #     exclude=exclude,
    #     version_id=version_id,
    # )
    # print(key, is_cached)

    key = "uuid80"
    file_path = "file_path3"
    include = ["include_json"]
    exclude = ["exclude_json"]
    expire_time = 3600
    version_id = "1.0"

    redis_client.cached_request(
        key=key,
        file_path=file_path,
        include=include,
        exclude=exclude,
        expire_time=expire_time,
        version_id=version_id,
    )

    has_field = redis_client.client.hexists(key, "last_modified")
    print(has_field)
