# Backend for file management (download only)

## Current tasks

### Tasks:

1. Test call API (unit test)

- [] SSE
  https://github.com/aio-libs/aiohttp-sse/blob/master/tests/test_sse.py

2. Test download task

- [] Use upload/ download/ delete task files

3. Health_check

- [] initial check

### Additional Features:

1. Multiple Path Download

- [] one zip file output
- [] like mega, gg drive

### Possible improvements:

- implement logging

### Limitation:

1. If the file on MinIO that was cached on Redis are deleted, the cache in Redis will still continue to exist instead of it should be deleted

### Notes:

Test files (test report@ dIA/documents)

## DFD diagram

<img src="https://i.imgur.com/uGnbOz0.png"  width="80%" height="80%">

## Use case diagram

<img src="https://i.imgur.com/WE09Aly.jpg" width="80%" height="80%">

## Technologies used:

- Python 3.10.10
- FastAPI
- Docker
- redis
- minio
- celery
- flower

## Run (windows):

celery -A worker worker --pool=solo -l INFO
celery -A worker flower
uvicorn main:app --reload
