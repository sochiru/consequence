from functools import wraps
from django.conf import settings
import redis


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
MAX_TIMEOUT = 600  # seconds


def single_instance_lock(func):
    task_name = f'{func.__module__}.{func.__name__}'
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        instance_name = '%s_%s' % ('lock', task_name)
        status =  redis_client.set(instance_name, 'lock', nx=True, ex=MAX_TIMEOUT)
        try:
            if status:
                return func(self, *args, **kwargs)
            return None
        finally:
            if status:
                redis_client.delete(instance_name)
    return wrapper
