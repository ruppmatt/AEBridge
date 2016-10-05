from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit, Namespace
import json
import redis
import pickle
import zlib


app = Flask(__name__)
socketio = SocketIO(app)

avida_socket = None
messages_socket = None
console_socket = None

r_server = redis.StrictRedis('localhost');
r_server.set('_ndx', -1);

def MakeKey(ndx):
    return 'msg::' + str(ndx)


def ProcessMessage(j):
    global r_server
    msg = StripMessage(j)
    ndx = r_server.incr('_ndx')
    msg['_ndx'] = ndx
    compressed = zlib.compress(pickle.dumps(j),9)
    r_server.set(MakeKey(ndx), compressed)
    return msg


def GetMessage(ndx):
    return pickle.loads(zlib.decompress(r_server.get(MakeKey(ndx))))



def StripMessage(j):
    rv = {k:j[k] for k in ['type','name','level','_update'] if k in j}

    if rv['type'] == 'response':
        if 'name' not in j['request']:
            rv['name'] = '(' + j['request']['type'] + ')'
        else:
            rv['name'] = '(' + j['request']['type'] + '@' + j['request']['name'] + ')'
    return rv



@app.route('/libs/<path:path>')
def send_js(path):
    return send_from_directory('libs', path)


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
            emit('ui_msg', ProcessMessage(msg), namespace='/messages', room=messages_socket);

    def on_av_msg(self, msg):
        global messages_socket
        if messages_socket:
            emit('av_msg', ProcessMessage(msg), namespace='/messages', room=messages_socket);


class MessagesClient(Namespace):
    def on_connect(self):
        global messages_socket
        global r_server
        messages_socket = request.sid
        print('Message client connected:', messages_socket)
        db_ndx = r_server.get('_ndx')
        emit('db_ndx', db_ndx)

    def on_disconnect(self):
        global messages_socket
        print('Message client disconnected:', messages_socket)
        messages_socket = None

    def on_send_command(self,msg):
        global avida_socket
        if avida_socket:
            emit('command', msg, namespace='/avida', room=avida_socket)

    def on_db_request(self, msg):
        db_msg = GetMessage(msg['ndx'])
        if db_msg != None:
            emit('db_request', {'ndx':msg['ndx'], 'data':db_msg})


socketio.on_namespace(AvidaClient('/avida'))
socketio.on_namespace(MessagesClient('/messages'))

if __name__ == '__main__':
    socketio.run(app)
