from utils.redis_utils import RedisUtils
import json

redis_utils = RedisUtils()


# test hget non-exist key
def test_hget_non_exist_key():
    result = redis_utils.client.hget("non-exist-key", "non-exist-field")
    print(result)


if __name__ == "__main__":
    test_hget_non_exist_key()
    assert False
