define(
  [
    'executor-ui'
  ], function(eui){

    var core_worker = null;

    function startAvidaCore(dir){
      core_worker = new Worker(dir+'/avida.js');
      eui.workerOnline(true);
    }

    function getWorker(){
      return core_worker;
    }

    function terminateAvidaCore(){
      if (core_worker){
        core_worker.terminate();
        core_worker = null;
        eui.workerOnline(false);
      }
    }

    function sendCoreMessage(msg){
      if (core_worker){
        core_worker.post(msg);
      }
    }

  return {
    startAvidaCore:startAvidaCore,
    terminateAvidaCore:terminateAvidaCore,
    getWorker:getWorker,
    sendCoreMessage:sendCoreMessage
  };
});
