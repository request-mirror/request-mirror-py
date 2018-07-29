import redis

from mirror.utils import generate_code

EXPIRATION_TIME = 60 * 15

redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)


def code_exists(code):
    return code in redis_store


def generate_valid_code():
    code = generate_code()
    while code_exists(code):
        code = generate_code()
    return code


def save_or_update(code):
    redis_store.set(code, 1, ex=EXPIRATION_TIME)
