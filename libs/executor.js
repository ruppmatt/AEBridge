require([
   'dojo/dom',
   'dojo/dom-construct',
   'dojo/_base/lang',
   'ui-common',
   'socket-common',
   'executor-ui',
   'executor-core-util'
 ], function(dom, domConstruct, lang, ui, socket, eui, coreUtil) {

  function reset(){
    setupHeader();
    setupMenu();
    setupSocket();
    setupWorker();
  }

  function setupHeader(){
    ui.setupHeader('Avida-ED Core Executor');
    eui.updateHeader();
  }

  function setupMenu(){
    var items = eui.getMenuItems();
    ui.findMenuItemByName('Restart Worker', items)['events']['click'] = coreUtil.restartAvidaCore;
    ui.findMenuItemByName('Halt Worker', items)['events']['click'] = coreUtil.terminateAvidaCore;
    ui.setupDropdownMenu('menu', items);
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
