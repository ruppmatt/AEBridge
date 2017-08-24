
define(
  [
    'dojo/dom',
    'dojo/dom-class',
    'dojo/dom-construct',
    'dojo/_base/window',
    'dojo/_base/lang',
    'dojo/on',
    'dojo/mouse'
  ], function (dom, domClass, domConstruct, win, lang, on, mouse) {

    function setupHeader(title, menu_items){
      var body = win.body();
      var header = domConstruct.create('header', {id:'header'}, body);
      var hflex = domConstruct.create('nav', {id:'header-flex'}, header);
      domConstruct.create('div', {id:'menu', class:'menu'}, hflex);
      domConstruct.create('div', {id:'title',innerHTML:title}, hflex);
      domConstruct.create('div', {id:'status'}, hflex);
      setupSocketAvidaStatus();
    }

    function findMenuItemByName(name, items)
    {
      for (let item of items){
        if (item['name'] === name){
          return item;
        }
      }
      return null;
    }

    function setupDropdownMenu(id, menu_items){
      var menu = dom.byId(id);
      on(menu, 'click', lang.hitch(this, mouseClickHighlight, menu));
      var menu_dropdown = domConstruct.create('div', {class:'menu-dropdown'}, menu);
      var menu_dropdown_content = domConstruct.create('div', {class:'menu-dropdown-content'}, menu);
      for (let item of menu_items){
        if (item['name'] !== undefined){
          var menu_item = domConstruct.create('div', {class:'menu-item'}, menu_dropdown_content);
          menu_item.innerHTML = item['name'];
        }
      }
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
      dom.byId(id).innerHTML = text;
      domClass.replace(id, new_state, old_state);
    }

    function mouseOverHighlight(item){
      if (domClass.contains(item, 'mouse-highlight-onover')){
        domClass.remove(item, 'mouse-highlight-onover');
      } else {
        domClass.add(item, 'mouse-highlight-onover');
      }
    }

    function mouseClickHighlight(item){
      if (domClass.contains(item, 'mouse-highlight-click')){
        domClass.remove(item, 'mouse-highlight-click');
      } else {
        domClass.add(item, 'mouse-highlight-click');
      }
    }

    return {
      setupHeader:setupHeader,
      avidaOnline:avidaOnline,
      socketOnline:socketOnline,
      setAvailability:setAvailability,
      findMenuItemByName:findMenuItemByName,
      setupDropdownMenu:setupDropdownMenu
    };

  }
);
