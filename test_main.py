from fastapi.testclient import TestClient
from main import app
from datetime import datetime, timedelta
from utils.uuid_utils import is_valid_uuid
import json
import collections

client = TestClient(app)


def test_root():  #
    response = client.get("/")
    assert response.status_code == 200


def test_ping():  #
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong!"}


download_url_single_file = None


def test_single_path_single_file_download():  #
    expired_time = datetime.utcnow() + timedelta(hours=1)
    response = client.post(
        "/download/",
        json=[
            {
                "path_name": "videos",
                "include": ["Avengers.mp4"],
                "exclude": [],
                "expired_time": expired_time.isoformat(),
                "version_id": "",
            },
        ],
    )
    assert response.status_code == 200

    for key, _ in response.json().items():
        if is_valid_uuid(key):
            ticket_id = key
        else:
            ticket_id = None
            assert False

    ticket_status = client.get(f"ticket/{ticket_id}/status")
    for line in ticket_status.text.split("\n"):
        # print(line)
        if line.startswith("data:"):
            data = json.loads(line[len("data: ") :])
            # print(data)
            # print(type(data))
            if data["status"] == "SUCCESS":
                assert data["status"] == "SUCCESS"
                break

    ticket_result = client.get(f"ticket/{ticket_id}/result")
    download_url_list = json.loads(ticket_result.json()["result"])
    assert isinstance(download_url_list, list)
    assert len(download_url_list) > 0

    global download_url_single_file
    download_url_single_file = download_url_list


def test_single_path_single_file_download_cache():  #
    response = client.post(
        "/download/",
        json=[
            {
                "path_name": "videos",
                "include": ["Avengers.mp4"],
                "exclude": [],
                "version_id": "",
            },
        ],
    )
    assert response.status_code == 200

    for key, _ in response.json().items():
        if is_valid_uuid(key):
            ticket_id = key
        else:
            ticket_id = None
            assert False

    while True:
        ticket_result = client.get(f"ticket/{ticket_id}/result")
        if ticket_result.json().get("result", None) is not None:
            break

    download_url_list = json.loads(ticket_result.json()["result"])
    assert isinstance(download_url_list, list)
    assert len(download_url_list) > 0

    global download_url_single_file
    assert collections.Counter(download_url_single_file) == collections.Counter(
        download_url_list
    )


download_url_multiple_files = None


def test_single_path_multiple_files_download():  #
    expired_time = datetime.utcnow() + timedelta(hours=1)
    response = client.post(
        "/download/",
        json=[
            {
                "path_name": "videos",
                "include": ["Avengers.mp4", "Go.mp4", "Slides.pdf"],
                "exclude": [],
                "expired_time": expired_time.isoformat(),
                "version_id": "",
            },
        ],
    )
    assert response.status_code == 200

    for key, _ in response.json().items():
        if is_valid_uuid(key):
            ticket_id = key
        else:
            ticket_id = None
            assert False

    ticket_status = client.get(f"ticket/{ticket_id}/status")
    for line in ticket_status.text.split("\n"):
        # print(line)
        if line.startswith("data:"):
            data = json.loads(line[len("data: ") :])
            # print(data)
            # print(type(data))
            if data["status"] == "SUCCESS":
                assert data["status"] == "SUCCESS"
                break

    ticket_result = client.get(f"ticket/{ticket_id}/result")
    # print(ticket_result.json())
    # print(type(ticket_result.json()["result"]))
    download_url_list = json.loads(ticket_result.json()["result"])
    assert isinstance(download_url_list, list)
    assert len(download_url_list) > 0

    global download_url_multiple_files
    download_url_multiple_files = download_url_list


def test_single_path_multiple_files_download_cache():  #
    response = client.post(
        "/download/",
        json=[
            {
                "path_name": "videos",
                "include": ["Avengers.mp4", "Go.mp4", "Slides.pdf"],
                "exclude": [],
                "version_id": "",
            },
        ],
    )
    assert response.status_code == 200

    for key, _ in response.json().items():
        if is_valid_uuid(key):
            ticket_id = key
        else:
            ticket_id = None
            assert False

    while True:
        ticket_result = client.get(f"ticket/{ticket_id}/result")
        if ticket_result.json().get("result", None) is not None:
            break

    download_url_list = json.loads(ticket_result.json()["result"])
    assert isinstance(download_url_list, list)
    assert len(download_url_list) > 0

    global download_url_multiple_files
    assert collections.Counter(download_url_multiple_files) == collections.Counter(
        download_url_list
    )


download_url_multiple_path_single_file = []


def test_multiple_paths_single_file_download():
    expired_time = datetime.utcnow() + timedelta(hours=1)
    response = client.post(
        "/download/",
        json=[
            {
                "path_name": "videos",
                "include": ["Avengers.mp4"],
                "exclude": [],
                "expired_time": expired_time.isoformat(),
                "version_id": "",
            },
            {
                "path_name": "pictures",
                "include": ["pic.jpg"],
                "exclude": [],
                "expired_time": expired_time.isoformat(),
                "version_id": "",
            },
            {
                "path_name": "documents",
                "include": ["Cap1.1.pdf"],
                "exclude": [],
                "expired_time": expired_time.isoformat(),
                "version_id": "",
            },
        ],
    )
    assert response.status_code == 200

    ticket_id = []

    for key, _ in response.json().items():
        if is_valid_uuid(key):
            ticket_id.append(key)
        else:
            ticket_id = None
            assert False

    for id in ticket_id:
        ticket_status = client.get(f"ticket/{id}/status")
        for line in ticket_status.text.split("\n"):
            # print(line)
            if line.startswith("data:"):
                data = json.loads(line[len("data: ") :])
                # print(data)
                # print(type(data))
                if data["status"] == "SUCCESS":
                    assert data["status"] == "SUCCESS"
                    break

    global download_url_multiple_path_single_file

    for id in ticket_id:
        ticket_result = client.get(f"ticket/{id}/result")
        download_url_list = json.loads(ticket_result.json()["result"])
        assert isinstance(download_url_list, list)
        assert len(download_url_list) > 0
        download_url_multiple_path_single_file.append(download_url_list)


if __name__ == "__main__":
    # test_root()
    # test_ping()
    # test_single_path_single_file_download()
    # test_single_path_single_file_download_cache()
    # test_single_path_multiple_files_download()
    # test_single_path_multiple_files_download_cache()
    test_multiple_paths_single_file_download()
