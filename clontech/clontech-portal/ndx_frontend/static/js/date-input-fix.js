// Determining whether browser supports datetime fields
var testDatefield = document.createElement("input");
testDatefield.setAttribute("type", "date");
var browserDoesntSupportDateField = testDatefield.type !== "date";

// This sets jQuery's datepicker on inputs of type date
if (browserDoesntSupportDateField) { 
  $(document).ready(function() { 
    $('input[type="date"]').datepicker({dateFormat: "yy-mm-dd"});
  })
}