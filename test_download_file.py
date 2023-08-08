from app.tasks.download_file import prepare_download
from datetime import datetime, timedelta
from app.api.models import FilePaths
import uuid, collections, json


class TestDownloadFile:
    def __init__(self):
        self.download_url_single_path_large_single_file = None
        self.download_url_single_path_small_single_file = None
        self.download_url_single_path_multiple_files = None
        self.download_url_multiple_paths_single_file = {}
        self.download_url_multiple_paths_multiple_file = {}

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
        default_expired_time = datetime.utcnow() + timedelta(days=1)
        file_path_1 = {
            "path_name": "videos",
            "include": ["Slides.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_2 = {
            "path_name": "documents",
            "include": ["Cap1.1.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_3 = {
            "path_name": "pictures",
            "include": ["pic.jpg"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_paths = [file_path_1, file_path_2, file_path_3]

        for file in file_paths:
            task_id = str(uuid.uuid4())
            path_name = file["path_name"]
            include = file["include"]
            exclude = file["exclude"]
            expired_time = file["expired_time"]
            version_id = file["version_id"]

            result = prepare_download(
                task_id, path_name, include, exclude, expired_time, version_id
            )

            if isinstance(result, str):
                result = json.loads(result)

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

            self.download_url_multiple_paths_single_file[path_name] = result

    def test_multiple_paths_single_file_cache(self):
        default_expired_time = datetime.utcnow() + timedelta(days=1)
        file_path_1 = {
            "path_name": "videos",
            "include": ["Slides.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_2 = {
            "path_name": "documents",
            "include": ["Cap1.1.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_3 = {
            "path_name": "pictures",
            "include": ["pic.jpg"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_paths = [file_path_1, file_path_2, file_path_3]

        for file in file_paths:
            task_id = str(uuid.uuid4())
            path_name = file["path_name"]
            include = file["include"]
            exclude = file["exclude"]
            expired_time = file["expired_time"]
            version_id = file["version_id"]

            result = prepare_download(
                task_id, path_name, include, exclude, expired_time, version_id
            )

            if isinstance(result, str):
                result = json.loads(result)

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

            assert collections.Counter(result) == collections.Counter(
                self.download_url_multiple_paths_single_file[path_name]
            )

    def test_multiple_paths_multiple_files(self):
        default_expired_time = datetime.utcnow() + timedelta(days=1)
        file_path_1 = {
            "path_name": "videos",
            "include": ["Slides.pdf", "Go.mp4"],
            "exclude": ["Avengers.mp4"],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_2 = {
            "path_name": "documents",
            "include": ["Cap1.1.pdf", "MD5.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_3 = {
            "path_name": "pictures",
            "include": ["pic.jpg", "qr.jpg"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_paths = [file_path_1, file_path_2, file_path_3]

        for file in file_paths:
            task_id = str(uuid.uuid4())
            path_name = file["path_name"]
            include = file["include"]
            exclude = file["exclude"]
            expired_time = file["expired_time"]
            version_id = file["version_id"]

            result = prepare_download(
                task_id, path_name, include, exclude, expired_time, version_id
            )

            if isinstance(result, str):
                result = json.loads(result)

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

            self.download_url_multiple_paths_multiple_file[path_name] = result

    def test_multiple_paths_multiple_files_cache(self):
        default_expired_time = datetime.utcnow() + timedelta(days=1)
        file_path_1 = {
            "path_name": "videos",
            "include": ["Slides.pdf", "Go.mp4"],
            "exclude": ["Avengers.mp4"],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_2 = {
            "path_name": "documents",
            "include": ["Cap1.1.pdf", "MD5.pdf"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_path_3 = {
            "path_name": "pictures",
            "include": ["pic.jpg", "qr.jpg"],
            "exclude": [],
            "expired_time": default_expired_time.isoformat(),
            "version_id": "",
        }

        file_paths = [file_path_1, file_path_2, file_path_3]

        for file in file_paths:
            task_id = str(uuid.uuid4())
            path_name = file["path_name"]
            include = file["include"]
            exclude = file["exclude"]
            expired_time = file["expired_time"]
            version_id = file["version_id"]

            result = prepare_download(
                task_id, path_name, include, exclude, expired_time, version_id
            )

            if isinstance(result, str):
                result = json.loads(result)

            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0

            assert collections.Counter(result) == collections.Counter(
                self.download_url_multiple_paths_multiple_file[path_name]
            )


if __name__ == "__main__":
    download_file = TestDownloadFile()

    download_file.test_single_path_large_single_file()
    print("PASSED: test_single_path_large_single_file")

    download_file.test_single_path_large_single_file_cache()
    print("PASSED: test_single_path_large_single_file_cache")

    download_file.test_single_path_small_single_file()
    print("PASSED: test_single_path_small_single_file")

    download_file.test_single_path_small_single_file_cache()
    print("PASSED: test_single_path_small_single_file_cache")

    download_file.test_single_path_multiple_files()
    print("PASSED: test_single_path_multiples_files")

    download_file.test_single_path_multiple_files_cache()
    print("PASSED: test_single_path_multiples_files_cache")

    download_file.test_multiple_paths_single_file()
    print("PASSED: test_multiple_paths_single_file")

    download_file.test_multiple_paths_single_file_cache()
    print("PASSED: test_multiple_paths_single_file")

    download_file.test_multiple_paths_multiple_files()
    print("PASSED: test_multiple_paths_multiple_files")

    download_file.test_multiple_paths_multiple_files_cache()
    print("PASSED: test_multiple_paths_multiple_files")
