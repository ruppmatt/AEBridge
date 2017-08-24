define(
  [
    'dojo/dom',
    'dojo/dom-class',
    'dojo/dom-construct',
    'dojo/_base/window',
    'ui-common'
  ], function (dom, domClass, domConstruct, win, ui) {

    function updateHeader(){
      var status = dom.byId('status');
      console.log(status);
      wstatus = domConstruct.create('div', {id:'status_worker'}, status, 'first');
      workerOnline(false);
    }

    function workerOnline(online){
      if (online === true){
        ui.setAvailability('status_worker', 'Avida core worker available', 'available', 'unavailable');
      } else {
        ui.setAvailability('status_worker', 'Avida core worker not available', 'unavailable', 'available');
      }
    }

    function getMenuItems(){
      return [
        {
          name:'Restart Worker',
          events:{}
        },
        {
          name:'Halt Worker',
          events:{}
        }
      ]
    }

    return {
      updateHeader:updateHeader,
      workerOnline:workerOnline,
      getMenuItems:getMenuItems
    };
});
