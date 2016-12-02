define(
  [
    'ui-common'
  ], function(ui) {

    var socket = null;
    var avida_online = false;

    function setupSocket(uri){
      /* =============================================================
      All of our socket communication handlers are below
      ============================================================= */

      socket = new io.connect(uri);
      avida_online = false;

      socket.on('connect', function(e) {
        avida_available = false;
        ui.socketOnline(true);
      });
      socket.on('disconnect', function(e) {
        avida_available = false;
        ui.socketOnline(false);
      });
      socket.on('avida-online', function(e){
        avida_available = true;
        ui.avidaOnline(true);
      });
      socket.on('avida-offline', function(e){
        avida_available = false;
        ui.avidaOnline(false);
      });
    }

    function getSocket(){
      return socket;
    }

    function avidaOnline(){
      return avida_online;
    }

    function setAvidaOnline(online){
      avida_online = online;
    }

    return { setupSocket:setupSocket, avidaOnline:avidaOnline, getSocket:getSocket };
  }
);
