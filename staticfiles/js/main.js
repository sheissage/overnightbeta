$(function() {
  var availableTags = [
    "airport",
    "port"
  ];
  $( "#transferlocation" ).autocomplete({
    source: availableTags
  });
});

$(function() {
  var availableTags = [
    "Yes",
    "No"
  ];
  $( "#hoteltransfer" ).autocomplete({
    source: availableTags
  });
});


$(function() {
  $( "#checkindate" ).datepicker();
});

$(function() {
  $( "#checkoutdate" ).datepicker();
});

$(function() {
  $('#eta').timepicker();
});

$(function() {
  $('#estcheckin').timepicker();
});



$(document).ready(function() {
  $("#datepicker-my").datepicker();
  $('#datebutton').click(function() {
    $("#datepicker-my").focus();
  });
});
