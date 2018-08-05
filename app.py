from flask import Flask, render_template
from flask import request, redirect
from flask import url_for
from flask_socketio import SocketIO, join_room, leave_room
from werkzeug.routing import Rule

from mirror.store import code_exists, generate_valid_code, save_or_update
from mirror.utils import parse_request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

# Regular routing

# Catch-all methods rule
app.url_map.add(Rule('/r/<code>', endpoint='process_request'))


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    code = ''
    if request.method == 'POST':
        if 'code' in request.form and len(request.form['code'].strip()) > 0:
            code = request.form['code']
            if not code_exists(code):
                return save_and_visit(code)
            else:
                error = 'Mirror already exists! Go <a href="{}">check it out.</a>'.format(url_for('view', code=code))
        else:
            return save_and_visit(generate_valid_code())

    return render_template('index.html', error=error, code=code)


@app.route('/v/<code>', methods=['GET'])
def view(code):
    if not code_exists(code):
        return render_template('404.html')
    save_or_update(code)
    return render_template('view.html', code=code)


@app.endpoint('process_request')
def process_request(code):
    if not code_exists(code):
        return 'The mirror you tried to access, does not exist.', 404
    else:
        save_or_update(code)
        data = parse_request(request)
        app.logger.info("Received request: {}".format(data))
        socketio.emit('request', data, room=code)
        return 'OK'


def save_and_visit(code):
    save_or_update(code)
    return redirect(url_for('view', code=code))


# Socket routes

@socketio.on('join')
def on_join(room):
    app.logger.info("Client connecting to room '{}'".format(room))
    join_room(room)


@socketio.on('leave')
def on_leave(room):
    app.logger.info("Client leaving room '{}'".format(room))
    leave_room(room)


@socketio.on('connect')
def connect():
    app.logger.info("Somebody connected! event: {}".format(request.event))


if __name__ == '__main__':
    socketio.run(app)
