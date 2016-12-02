 require([
    'dojo/dom',
    'dojo/dom-construct',
    'ui-common',
    'socket-common'
  ], function(dom, domConstruct, ui, socket) {

   function reset(){
     ui.setupHeader('Avida-ED Log Utility');
     setupFilename();
     unloadLog();
     setupSocket();
   }

   function setupSocket(){
     socket.setupSocket('http://localhost:5000/logger');
   }


   function setupFilename(){
     domConstruct.create('div', {id:'filename'}, header);
   }


   function unloadLog(){
     global.logfile = null;
     dom.byId('filename').innerHTML = 'Drag log file to load';
   }

   var global = {};
   reset();
 }
);
