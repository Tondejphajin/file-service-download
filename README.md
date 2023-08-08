# Backend for file management (download only)

## Current tasks

Symbols:
X = completed
% = in-progress

Test files (test report@ dIA/documents)

1. Test call API (unit test)

- [] SSE
  https://github.com/aio-libs/aiohttp-sse/blob/master/tests/test_sse.py

2. Test download task

- [] Use upload/ download/ delete task files

3. Health_check

- [] initial check

Multiple Path Download

- [] one zip file output
- [] like mega, gg drive

0. DFD (Documentation)

- [ ] DFD is Data Flow Diagram
- [ ] Change information on connection line to data send and receive communicate between 2 objects.
- [ ] Change word for explain process.
- [ ] Information data in level 0 must found level 1.
- [ ] Please explain more and make me understand.

1. environment file

- [x] hostname >> use domain name or container name.
- [x] size of data set human readable such as 1MB 5GB.
- [x] time set human readable such as 1 second, 2 days.
- [x] increase external host, public IP or domain name.
      Note: 1) External host = Network outside Docker, Test by connecting outside service to Docker 2) 0.0.0.0 can accept external and is not the same as local host 3) Config by Docker compose
- [x] control load env file on startup event.
- [x] when using `load_dotenv function` why use `os.getenv` again? pls, choose one function.

2. API

- [x] change path for download to `/download`
- [x] change path for check status to `/ticket/{ticketId}/status` (SSE)
- [x] increase path for get result `/ticket/{ticketId}/result`
- [x] API able to append 1 task. except for these tasks haven't relate or not await.

3. Worker

- [x] Minio Client I told you if it's not async function. You don't have to use async.
- [%] Available to set expire date specific request.

4. Common

- [x] Change to OOP Concept.

5. Redis

- [x] redis trigger expire move or delete file on minio
      Note: 1) Create a task for delete files 2) API for delete files
      Approach: 1) add delete task to queue waiting to be deleted
- [ ] seperate backend and broker in Celery (optional)

New Assignment -> research solution/ algorithm/

- [x] Understand check sum algorithm.
- [x] if request download before file change (update) downloads old version not current. (condition before download)
- [x] if deleted but have request before able to download.
- [x] if ready to download on Redis but have change must be preparing download again. (1)
  - check last modified
- [x] Able to set maximum download in same time.
- [%] if maximum download is 2 or more.it have one current task process system choose first index in queue to execute but disk space not enough can choose request to execute. System must running maximum queue available. (2)
  - Study more about Celery beat

Integration tasks

- [%] app/ register
- [] login/ logout
- [] check license
- [%] health check
  Upcoming

- Set priority in Queue
  Ex: Download has priority than Delete so allocate Delete task to the second worker

Deadline:
1-5: Tue 12:00
New Assignment: Wed 26 July

Note:

- Hidden task report on Gitlab issue
- (2) Need more research

Hidden task:

- Docker
- celery config
- queue expire
- queue priority
- link task

Possible improvements:

- implement logging

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

## Features:

- Zip/ Split files download
- Queue management
- download single/ multiple paths

## Run (windows):

celery -A worker worker --pool=solo -l INFO
celery -A worker flower
uvicorn main:app --reload

## For debugging:

- celery -A tasks worker --pool=solo -l INFO
- use Celery debug tools (rdb)
  - important command:
    - n: next, p: print, c: continue, s: step into, r: return, l: list, w: where, u: up, d: down, b: breakpoint
