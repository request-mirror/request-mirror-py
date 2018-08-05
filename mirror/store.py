import redis
import dill

from mirror.utils import generate_code

EXPIRATION_TIME = 60 * 15
MAX_REQUESTS = 20

redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)


def mirror_exists(code):
    return code in redis_store


def generate_valid_code():
    code = generate_code()
    while mirror_exists(code):
        code = generate_code()
    return code


def mirror_requests(code):
    return "{}:requests".format(code)


def push_request(code, request):
    r = dill.dumps(request)
    mr = mirror_requests(code)
    p = redis_store.pipeline()
    p.expire(code, EXPIRATION_TIME)
    p.lpush(mr, r)
    p.ltrim(mr, 0, MAX_REQUESTS - 1)
    p.expire(mr, EXPIRATION_TIME)
    p.execute()


def get_all_requests(code):
    requests = redis_store.lrange(mirror_requests(code), 0, MAX_REQUESTS - 1)
    return [dill.loads(r) for r in requests]


def create_or_update_mirror(code):
    p = redis_store.pipeline()
    p.set(code, 1, ex=EXPIRATION_TIME)
    p.expire(mirror_requests(code), EXPIRATION_TIME)
    p.execute()
