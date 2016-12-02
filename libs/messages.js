require([
   'dojo/dom',
   'dojo/dom-construct',
   'dojo/_base/window',
   'ui-common',
   'socket-common',
   'message-handling'
], function(dom, domConstruct, win, ui, socket, handlers) {

    reset();

    function reset(){
      ui.setupHeader('Avida-ED Message Viewer');
      setupBody();
      setupSocket();
    }

    function setupBody(){
      domConstruct.create('div', {id:'messages'}, win.body());
    }


   function setupSocket(){
     socket.setupSocket('http://localhost:5000/messages');
     socket.getSocket().on('message', function(e) {
        handlers.createAndAppendMessage(e);
     });
     socket.getSocket().on('avida-online', function(e){
       ui.avidaOnline(true);
       socket.setAvidaOnline(true);
       handlers.doMessageRefresh(e);
     });
     socket.getSocket().on('db_refresh', function(e) {
        handlers.doMessageRefresh(e);
     });
     socket.getSocket().on('db_request', function(e) {
        handlers.displayMessageAtNdx(e);
     });
   }
});
