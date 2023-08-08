from fastapi.testclient import TestClient
from main import app  # replace with the path to your FastAPI application
import json

client = TestClient(app)


def test_check_status():
    response = client.get(
        "/your_route/ticket_id/status", stream=True
    )  # replace 'your_route' and 'ticket_id' with actual values

    # The response.raw is a urllib3.HTTPResponse object and allows to iterate over streamed data
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream"

    first_data_received = False
    for line in response.iter_lines():
        # filter out keep-alive new lines
        if line:
            decoded_line = line.decode("utf-8")
            assert decoded_line.startswith("data:")
            data = json.loads(decoded_line.replace("data: ", "", 1))
            if not first_data_received:
                assert data["message"] == "Please wait for the file to be ready ... "
                first_data_received = True
            else:
                assert data["message"] == "The file is ready"
                break  # Stop the test after the first actual data message is received
