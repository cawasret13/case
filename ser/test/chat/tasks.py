from celery import shared_task, Task


@shared_task()
def test():
    log.delay()
    return 'Hello'


def log():
    print('hello')