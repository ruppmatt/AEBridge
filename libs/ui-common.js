
define(
  [
    'dojo/dom',
    'dojo/dom-class',
    'dojo/dom-construct',
    'dojo/_base/window'
  ], function (dom, domClass, domConstruct, win) {

    function setupHeader(title){
      var body = win.body();
      var header = domConstruct.create('div', {id:'header'}, body);
      var hflex = domConstruct.create('div', {id:'header-flex'}, header);
      domConstruct.create('div', {id:'menu'}, hflex);
      domConstruct.create('div', {id:'title',innerHTML:title}, hflex);
      domConstruct.create('div', {id:'status'}, hflex);
      setupSocketAvidaStatus();
    }

    function setupSocketAvidaStatus(){
      var cnx = dom.byId('status');
      domConstruct.create('div', {id:'status_socket', class:'unavailable'}, cnx);
      domConstruct.create('div', {id:'status_avida', class:'unavailable'}, cnx);
      socketOnline(false);
    }


    function avidaOnline(online){
      if (online === true){
        setAvailability('status_avida', 'Avida core online', 'available', 'unavailable');
      } else {
         setAvailability('status_avida', 'Avida core offline', 'unavailable', 'available');
      }
    }


    function socketOnline(online){
      if (online === true){
        setAvailability('status_socket', 'Socket server online', 'available', 'unavailable');
      } else {
         setAvailability('status_socket', 'Socket server offline', 'unavailable', 'available');
         avidaOnline(false);
      }
    }

    function setAvailability(id, text, new_state, old_state){
      console.log(text);
      dom.byId(id).innerHTML = text;
      domClass.replace(id, new_state, old_state);
    }

    return {
      setupHeader:setupHeader,
      avidaOnline:avidaOnline,
      socketOnline:socketOnline
    };

  }
);
