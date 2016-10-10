import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
hdlr = logging.FileHandler('cmd_socket.log')
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace

'''
class SocketIOClient(SocketIO):
    """
    Fix for library bug
    Found: https://stackoverflow.com/questions/37058119/python-and-socket-io-app-hangs-after-connection
    """

    def _should_stop_waiting(self, for_connect=False, for_callbacks=False):
        if for_connect:
            for namespace in self._namespace_by_path.values():
                is_namespace_connected = getattr(
                    namespace, '_connected', False)
                #Added the check and namespace.path
                #because for the root namespaces, which is an empty string
                #the attribute _connected is never set
                #so this was hanging when trying to connect to namespaces
                # this skips the check for root namespace, which is implicitly connected
                if not is_namespace_connected and namespace.path:
                    return False
            return True
        if for_callbacks and not self._has_ack_callback:
            return True
        return super(SocketIO, self)._should_stop_waiting()
'''

class AvidaExternalCommand(BaseNamespace):
    def on_issue_command(self, *args):
        print(args)


step_update = {'type':'stepUpdate'}

def send_command(cmd):
    with SocketIO('localhost', 5000, AvidaExternalCommand) as cmd_socket:
        cmd_namespace = cmd_socket.define(AvidaExternalCommand, '/command')
        cmd_namespace.emit('issue_command', cmd)
