from app.tasks.download_file import prepare_download, prepare_download_dev
from datetime import datetime, timedelta
from app.api.models import FilePaths
import uuid, collections, json


class TestDownloadFile:
    def __init__(self):
        self.download_url_single_path_large_single_file = None
        self.download_url_single_path_small_single_file = None
        self.download_url_single_path_multiple_files = None
        self.download_url_multiple_paths_single_file = None

    def test_single_path_large_single_file(self):
        task_id = str(uuid.uuid4())
        path_name = "videos"
        include = ["Avengers.mp4"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) > 1

        self.download_url_single_path_large_single_file = result

    def test_single_path_large_single_file_cache(self):
        task_id = str(uuid.uuid4())
        path_name = "videos"
        include = ["Avengers.mp4"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) > 1
        assert collections.Counter(result) == collections.Counter(
            self.download_url_single_path_large_single_file
        )

    def test_single_path_small_single_file(self):
        task_id = str(uuid.uuid4())
        path_name = "documents"
        include = ["MD5.pdf"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) == 1

        self.download_url_single_path_small_single_file = result

    def test_single_path_small_single_file_cache(self):
        task_id = str(uuid.uuid4())
        path_name = "documents"
        include = ["MD5.pdf"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) == 1
        assert collections.Counter(result) == collections.Counter(
            self.download_url_single_path_small_single_file
        )

    def test_single_path_multiple_files(self):
        task_id = str(uuid.uuid4())
        path_name = "documents"
        include = ["Cap1.1.pdf", "MD5.pdf"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) > 0

        self.download_url_single_path_multiple_files = result

    def test_single_path_multiple_files_cache(self):
        task_id = str(uuid.uuid4())
        path_name = "documents"
        include = ["Cap1.1.pdf", "MD5.pdf"]
        exclude = []
        expire_time = datetime.now() + timedelta(hours=1)
        version_id = ""

        result = prepare_download(
            task_id, path_name, include, exclude, expire_time, version_id
        )

        if isinstance(result, str):
            result = json.loads(result)

        assert isinstance(result, list)
        assert len(result) == 1
        assert collections.Counter(result) == collections.Counter(
            self.download_url_single_path_multiple_files
        )

    def test_multiple_paths_single_file(self):
        path1 = FilePaths(
            path_name="documents/",
            include=["Cap1.1.pdf"],
            exclude=[],
            expired_time=datetime.now() + timedelta(days=1),
            version_id="",
        )

        path2 = FilePaths(
            path_name="videos/",
            include=["Avengers.mp4"],
            exclude=[],
            expired_time=datetime.now() + timedelta(days=1),
            version_id="",
        )

        request = [path1, path2]
        task_id = str(uuid.uuid4())

        result = prepare_download_dev(task_id, request)
        print(result)


if __name__ == "__main__":
    download_file = TestDownloadFile()

    # download_file.test_single_path_large_single_file()
    # print("PASSED: test_single_path_large_single_file")

    # download_file.test_single_path_large_single_file_cache()
    # print("PASSED: test_single_path_large_single_file_cache")

    # download_file.test_single_path_small_single_file()
    # print("PASSED: test_single_path_small_single_file")

    # download_file.test_single_path_small_single_file_cache()
    # print("PASSED: test_single_path_small_single_file_cache")

    # download_file.test_single_path_multiple_files()
    # print("PASSED: test_single_path_multiples_files")

    # download_file.test_single_path_multiple_files_cache()
    # print("PASSED: test_single_path_multiples_files_cache")

    download_file.test_multiple_paths_single_file()
