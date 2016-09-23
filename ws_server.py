from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, Namespace
import json
import redis


app = Flask(__name__)
socketio = SocketIO(app)

avida_socket = None
messages_socket = None
console_socket = None

r_server = redis.Redis('localhost');
r_server.set('_ndx', -1);


def BuildMessage(j):
    global r_server
    msg = StripMessage(j)
    msg['_ndx'] = r_server.incr('_ndx')
    return msg


def StripMessage(j):
    rv = {k:j[k] for k in ['type','name','level'] if k in j}
    if rv['type'] == 'response':
        if 'name' not in j['request']:
            rv['name'] = '(' + j['request']['type'] + ')'
        else:
            rv['name'] = '(' + j['request']['type'] + '@' + j['request']['name'] + ')'
    return rv


@app.route('/messages')
def messages():
    return render_template('messages.html')


class AvidaClient(Namespace):
    def on_connect(self):
        global avida_client
        avida_client = request.sid
        print('Avida client connected:', avida_client)

    def on_disconnect(self):
        global avida_client
        print('Avida client disconnected:', avida_client)
        avida_client = None

    def on_ui_msg(self, msg):
        global messages_socket
        if messages_socket:
            emit('ui_msg', BuildMessage(msg), namespace='/messages', room=messages_socket);

    def on_av_msg(self, msg):
        global messages_socket
        if messages_socket:
            emit('av_msg', BuildMessage(msg), namespace='/messages', room=messages_socket);


class MessagesClient(Namespace):
    def on_connect(msg):
        global messages_socket
        messages_socket = request.sid
        print('Message client connected:', messages_socket)

    def on_disconnect(msg):
        global messages_socket
        print('Message client disconnected:', messages_socket)
        messages_socket = None

    def on_send_command(msg):
        global avida_socket
        if avida_socket:
            emit('command', msg, namespace='/avida', room=avida_socket)



socketio.on_namespace(AvidaClient('/avida'))
socketio.on_namespace(MessagesClient('/messages'))

if __name__ == '__main__':
    socketio.run(app)
