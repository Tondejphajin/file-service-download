from celery import Celery
import pytest

demo = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)
demo.conf.update(CELERY_ALWAYS_EAGER=True)


@demo.task
def add(x, y):
    return x + y


@pytest.mark.celery(result_backend="redis://localhost:6379/0")
def test_celery():
    assert add(1, 2) == 3


if __name__ == "__main__":
    test_celery()
