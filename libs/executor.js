require([
   'dojo/dom',
   'dojo/dom-construct',
   'ui-common',
   'socket-common',
   'executor-ui',
   'executor-core-util'
 ], function(dom, domConstruct, ui, socket, eui, coreUtil) {

  function reset(){
    setupHeader();
    setupSocket();
    setupWorker();
  }

  function setupHeader(){
    ui.setupHeader('Avida-ED Core Executor');
    eui.updateHeader();
  }

  function setupSocket(){
    socket.setupSocket('http://localhost:5000/executor');
  }

  function setupWorker(){
    if (window.Worker){
      coreUtil.startAvidaCore('libs/work');
      console.log(coreUtil.getWorker());
    }
  }

  reset();
}
);
