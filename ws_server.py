from flask import Flask, render_template
from flask_socketio import SocketIO, emit, Namespace
import json


app = Flask(__name__)
socketio = SocketIO(app)

avida_socket = None
messages_socket = None
console_socket = None

avida_messages = []


@app.route('/messages')
def messages():
    return render_template('messages.html')

class AvidaClient(Namespace):
    def on_connect(msg):
        avida_client = request.sid;

    def on_disconnect(msg):
        avida_client = None

    def on_message(msg):
        avida_messages.append(msg);


class MessagesClient(Namespace):
    def on_connect(msg):
        messages_socket = request.sid

    def on_disconnect(msg):
        messages_socket = None

    def on_receive_filtered(msg):
        if (console_socket):
            emit('receive_filtered', room=console_socket)

    def on_refresh_messages(msg):
        emit('messages', json.dumps(avida_messages))

    def on_send_command(msg):
        if avida_socket:
            emit('command', msg, room=avida_socket)


class ConsoleClient(Namespace):
    def on_connect(msg):
        console_socket = request.sid

    def on_disconnect(msg):
        console_socket = None

    def on_get_filtered(msg):
        if messages_socket:
            emit('send_filtered', room=messages_socket)

    def on_send_command(msg):
        if avida_socket:
            emit('command', msg, room=avida_socket)


socketio.on_namespace(AvidaClient('/avida'))
socketio.on_namespace(MessagesClient('/messages'))
socketio.on_namespace(ConsoleClient('/console'))

if __name__ == '__main__':
    socketio.run(app)
