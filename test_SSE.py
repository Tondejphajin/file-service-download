import requests
import json


def test_check_status():
    ticket_id = "7c1229d0-1d8d-4a37-aa49-2233cbf38b2c"
    link = f"http://localhost:8000/ticket/{ticket_id}/status"  # Replace with your actual URL

    response = requests.get(link, stream=True)
    assert response.status_code == 200
    # assert response.headers["content-type"] == "text/event-stream"

    first_data_received = False
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = line.decode("utf-8")
            assert decoded_line.startswith("data:")
            data = json.loads(decoded_line.replace("data: ", "", 1))
            print(data)
            if not first_data_received:
                assert data["status"] == "SUCCESS"
                first_data_received = True


if __name__ == "__main__":
    test_check_status()
