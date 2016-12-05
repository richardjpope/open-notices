$(document).ready(function(){
  
  $('table.tag-input label').addClass('show-for-sr');
  add_row = $('<p><a href="#">Add another row</a></p>');
  add_row.click(function(){

    //duplicate last row
    count = $('td.key').length;
    new_html = $("table.tag-input tr:last").clone().html();

    //replace ids
    regex = new RegExp("_key_" + (count - 1), "g");
    new_html = new_html.replace(regex, "_key_" + (count));
    regex = new RegExp("_value_" + (count - 1), "g");
    new_html = new_html.replace(regex, "_value_" + (count));
    regex = new RegExp("for tag " + (count - 1), "g");
    new_html = new_html.replace(regex, "for tag " + (count));

    //add new row
    new_html = "<tr>" + new_html + "</tr>";
    $(new_html).appendTo("table.tag-input");

    return false;
  });

  //add button
  add_row.insertAfter('table.tag-input');

});