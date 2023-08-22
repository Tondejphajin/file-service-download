from dotenv import dotenv_values, set_key
from utils import env_parser as parser


class Env:
    BYTE_VARS = ["MAX_DOWNLOAD_SIZE", "MAX_CHUNK_SIZE"]
    SEC_VARS = ["STREAM_DELAY", "REDIS_EXPIRE_TIME"]
    DAY_VARS = ["MINIO_EXPIRE_TIME"]

    def __init__(self):
        self._config = dotenv_values("local.env")
        self.convert_to_bytes()
        self.convert_to_seconds()
        self.convert_to_days()
        # setattr(self, "MAX_DOWNLOAD_SIZE", self._config["MAX_DOWNLOAD_SIZE"])

    def convert_to_bytes(self):
        for var in self.BYTE_VARS:
            try:
                self._config[var] = parser.convert_to_bytes(self._config[var])
            except KeyError:
                raise Exception(f"Invalid key: {var}")
            except ValueError:
                raise Exception(f"Invalid value for key: {var}")

    def convert_to_seconds(self):
        for var in self.SEC_VARS:
            try:
                self._config[var] = parser.convert_to_seconds(self._config[var])
            except KeyError:
                raise Exception(f"Invalid key: {var}")
            except ValueError:
                raise Exception(f"Invalid value for key: {var}")

    def convert_to_days(self):
        for var in self.DAY_VARS:
            try:
                self._config[var] = parser.convert_to_days(self._config[var])
            except KeyError:
                raise Exception(f"Invalid key: {var}")
            except ValueError:
                raise Exception(f"Invalid value for key: {var}")

    def get_all_env_variables(self):
        return self._config

    def get_all_keys(self):
        return self._config.keys()

    def get_value(self, key: str) -> str:
        try:
            return self._config[key]
        except KeyError:
            raise Exception(f"Invalid key: {key}")

    def check_key_and_value_exist(self, key: str) -> bool:
        return key in self._config.keys() and self._config[key] != ""

    def set_key(self, key: str, value: str):
        set_key(".env", key, value)


if __name__ == "__main__":
    env = Env()
    print(env.get_all_env_variables())
    # print(env.get_value("MINIO_ACCESS_KEY"))
    print(env.get_value("MAX_DOWNLOAD_SIZE"))
