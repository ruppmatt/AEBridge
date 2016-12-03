"""
Page generated using examples from:
https://flask-socketio.readthedocs.io/en/latest/
https://arusahni.net/blog/2014/03/flask-nocache.html
"""

from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit, Namespace
import json
import redis
import pickle
import zlib
from nocache import nocache



app = Flask(__name__)
socketio = SocketIO(app)

sockets = {};

r_server = redis.StrictRedis('localhost')


def SetupSocketInfo():
    global sockets
    sockets['avida'] = {'id':None, 'namespace':'/avida'}
    sockets['messages'] = {'id':None, 'namespace':'/messages'}
    sockets['logger'] = {'id':None, 'namespace':'/logger'}
    sockets['command'] = {'id':None, 'namespace':'/command'}



def FlushDB():
    """ Flush the DB """
    global r_server
    p = r_server.pipeline()
    p.flushdb()
    p.set('_ndx', -1);
    p.execute()
    print('Flushing DB')



def MakeKey(ndx):
    """
    From a numerical index, create the document key for the database.
    """
    return 'msg::' + str(ndx)


def ProcessMessage(j):
    """
    For an incoming message prepare it for transmission to the messages_socket
    client by stripping unnecessary information and store it in the database.
    """
    global r_server
    ndx = r_server.incr('_ndx')
    data = j['data']
    meta = j['meta']
    j['meta']['_ndx'] = ndx
    msg =  {
            'data':data,
            'meta':meta
            }
    compressed = zlib.compress(pickle.dumps(msg),9)
    r_server.set(MakeKey(ndx), compressed)
    return {'data':StripMessage(data), 'meta':meta}


def GetMessage(ndx):
    """
    Given a numerical index return the message from the database.
    """
    return pickle.loads(zlib.decompress(r_server.get(MakeKey(ndx))))


def DumpMessages():
    """
    Return a list of all (stripped) messages currently in the
    database
    """
    global r_server
    ndx = int(r_server.get('_ndx'))
    if ndx < 0:
        return None
    compressed = r_server.mget(MakeKey(0),MakeKey(ndx))
    if compressed[0] == None:
        return None
    uncompressed = list(map(lambda s: pickle.loads(zlib.decompress(s)) if s else None, compressed[:-1]))
    return uncompressed


def StripMessage(j):
    """
    Strip the message of all but the most necessary information for the
    message client.  Full messages can be retrieved later for dispaly.
    """
    rv = {k:j[k] for k in ['type', 'name', 'level', 'update', 'mode'] if k in j}

    if rv['type'] == 'response':
        if 'name' not in j['request']:
            rv['name'] = '(' + j['request']['type'] + ')'
        else:
            rv['name'] = '(' + j['request']['type'] + '@' + j['request']['name'] + ')'
    return rv


def UpdateAvidaStatus(ns):
    global sockets
    if sockets['avida']['id']:
        OnAvidaConnect(ns)
    else:
        OnAvidaDisconnect(ns)

def OnAvidaConnect(ns):
    global sockets
    event = 'avida-online'
    for s in ['messages','logger']:
        if sockets[s]['id']:
            emit(event, namespace=sockets[s]['namespace'], room=sockets[s]['id'])


def OnAvidaDisconnect(ns):
    global sockets
    event = 'avida-offline'
    for s in ['messages','logger']:
        if sockets[s]['id']:
            emit(event, namespace=sockets[s]['namespace'], room=sockets[s]['id'])




@app.route('/libs/<path:path>')
@nocache
def send_js(path):
    """
        Serve the libs directory for things like json scripts and associated css
    """
    return send_from_directory('libs', path)

@app.route('/css/<path:path>')
@nocache
def send_css(path):
    """
        Serve the libs directory for things like json scripts and associated css
    """
    return send_from_directory('css', path)

# Serve the messages page
@app.route('/messages')
@nocache
def messages():
    return render_template('messages.html')

# Serve the logger page
@app.route('/logger')
@nocache
def logger():
    return render_template('logger.html')





# Handle socket support for the avida client
class AvidaClient(Namespace):
    def on_connect(self):
        global sockets
        sockets['avida']['id'] = request.sid;
        FlushDB()
        print('Avida client connected:', sockets['avida']['id'])
        OnAvidaConnect(Namespace)

    def on_disconnect(self):
        global sockets
        print('Avida client disconnected:', sockets['avida']['id'])
        sockets['avida']['id'] = None
        OnAvidaDisconnect(Namespace)

    def on_message(self, msg):
        """User interface messages"""
        global sockets
        if sockets['messages']['id']:
            emit('message', ProcessMessage(msg), namespace=sockets['messages']['namespace'], room=sockets['messages']['id'])



# Handle socket support for messages client
class MessagesClient(Namespace):
    def on_connect(self):
        """
        Immediately relay the current state of the message database to the
        messages page to prevent if from dispalying stale data.
        """
        global sockets, r_server
        s = sockets['messages']
        sockets['messages']['id'] = request.sid
        print('Message client connected:', sockets['messages']['id'])
        emit('db_refresh', DumpMessages())
        UpdateAvidaStatus(Namespace)

    def on_disconnect(self):
        global sockets
        print('Message client disconnected:', sockets['messages']['id'])
        sockets['messages']['id'] = None

    def on_send_command(self,msg):
        """
        Presumably the messages page can send commands.  This isn't used at
        at the moment.
        """
        pass

    def on_db_request(self, msg):
        """
        The message page's javascript will request messages from the database
        with a particular numerical index.  This method retrieves those
        messages or silently eats the request if the message is not available.
        """
        db_msg = GetMessage(msg['ndx'])
        if db_msg != None:
            emit('db_request', {'ndx':msg['ndx'], 'data':db_msg})



# Handle socket communication for an external command issuer to avida
class ExternalCommandClient(Namespace):
    def on_connect(self):
        global sockets
        sockets['command']['id'] = request.sid
        print('External command client connected: ', sockets['command']['id'])

    def on_disconnect(self):
        global sockets
        sockets['command']['id'] = None
        print('External command client disconnected.')

    def on_issue_command(self, msg):
        """Relay command message to the Avida client if available."""
        global sockets
        if sockets['avida']['id']:
            emit('ext_command', msg, namespace=sockets['avida']['namespace'], room=sockets['avida']['id'])



# Handle socket communication with logger utility
class LoggerClient(Namespace):
    def on_connect(self):
        global sockets
        sockets['logger']['id'] = request.sid
        print('Logger client connected:', sockets['logger']['id'])
        UpdateAvidaStatus(Namespace)


    def on_disconnect(self):
        global sockets
        print('Logger client disconnected:', sockets['logger']['id']);
        sockets['logger']['id'] = None


socketio.on_namespace(AvidaClient('/avida'))
socketio.on_namespace(MessagesClient('/messages'))
socketio.on_namespace(ExternalCommandClient('/command'))
socketio.on_namespace(LoggerClient('/logger'));



if __name__ == '__main__':
    SetupSocketInfo()
    FlushDB()
    socketio.run(app)
