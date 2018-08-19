from werkzeug.contrib.fixers import ProxyFix
from flask import Flask, render_template
from flask import request, redirect
from flask import url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from werkzeug.routing import Rule

from mirror.store import mirror_exists, generate_valid_code, create_or_update_mirror, push_request, get_all_requests
from mirror.utils import parse_request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.wsgi_app = ProxyFix(app.wsgi_app)
socketio = SocketIO(app)

# Regular routing

# Catch-all methods rule
app.url_map.add(Rule('/r/<code>', endpoint='process_request'))
app.url_map.add(Rule('/r/<code>/<path:path>', endpoint='process_request'))


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    code = ''
    if request.method == 'POST':
        if 'code' in request.form and len(request.form['code'].strip()) > 0:
            code = request.form['code']
            if not mirror_exists(code):
                return create_or_update_and_visit(code)
            else:
                error = 'Mirror already exists! Go <a href="{}">check it out.</a>'.format(url_for('view', code=code))
        else:
            return create_or_update_and_visit(generate_valid_code())

    return render_template('index.html', error=error, code=code)


@app.route('/v/<code>', methods=['GET'])
def view(code):
    if not mirror_exists(code):
        return render_template('404.html')
    create_or_update_mirror(code)
    return render_template('view.html', code=code, url_root=request.url_root)


@app.endpoint('process_request')
def process_request(code, path=None):
    if not mirror_exists(code):
        return 'The mirror you tried to access, does not exist.', 404
    else:
        data = parse_request(request)
        push_request(code, data)
        app.logger.info("Received request: {}".format(data))
        socketio.emit('request', data, room=code)
        return 'OK'


def create_or_update_and_visit(code):
    create_or_update_mirror(code)
    return redirect(url_for('view', code=code))


# Socket routes

@socketio.on('join')
def on_join(room):
    app.logger.info("Client connecting to room '{}'".format(room))
    join_room(room)
    requests = get_all_requests(room)
    for r in reversed(requests):
        emit('request', r)


@socketio.on('leave')
def on_leave(room):
    app.logger.info("Client leaving room '{}'".format(room))
    leave_room(room)


@socketio.on('connect')
def connect():
    app.logger.info("Somebody connected! event: {}".format(request.event))


if __name__ == '__main__':
    if app.config['ENV'] == 'production':
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'
    socketio.run(app, host=host)
