/* Author:

*/
// Authenticate AJAX requests
var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
          crossDomain: false, // obviates need for sameOrigin test
          beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      });
$(document).ready(function() {
  /* Multi select - allow multiple selections */
  /* Allow click without closing menu */
  /* Toggle checked state and icon */
  $('.multicheck').click(function(e) {
     $(this).toggleClass("checked");
     $(this).find("span").toggleClass("icon-ok");
     return false;
  });
});


$(function () {
  /* Control check all */
    $('.checkall').click(function () {
        $(this).parents('fieldset:eq(0)').find(':checkbox').attr('checked', this.checked);
    });
});