import string
import random
import os
from datetime import datetime
from urllib.parse import urlparse


def generate_code():
    # Just alphanumeric characters
    chars = string.ascii_letters + string.digits

    code_len = 7

    return ''.join((random.choice(chars)) for _ in range(code_len))


def parse_request(request):
    return {
        'path': request.path,
        'body': request.get_data().decode('utf-8'),
        'form': request.form,
        'query_string': request.args,
        'headers': dict(request.headers),
        'time': datetime.now().isoformat(),
        'method': request.method,
        'remote_addr': request.headers.get('X-Forwarded-For', request.remote_addr)
    }


def gen_redis_config_dict():
    url = urlparse(os.environ.get('REDIS_URL', 'redis://localhost:6379'))
    if hasattr(url, 'path') and getattr(url, 'path'):
        db = url.path[1:]
    else:
        db = 0
    max_connections = os.environ.get('REDIS_MAX_CONNECTIONS', None)
    return {
        'host': url.hostname,
        'port': url.port,
        'db': db,
        'password': url.password,
        'max_connections': max_connections
    }
