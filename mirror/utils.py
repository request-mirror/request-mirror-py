import string
import random
from datetime import datetime


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
        'query_string': str(request.args),
        'headers': dict(request.headers),
        'time': datetime.now().isoformat(sep=' '),
        'method': request.method
    }
