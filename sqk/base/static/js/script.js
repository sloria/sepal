/* Author:

*/

/* Authenticate AJAX requests */
var csrftoken = $.cookie('csrftoken');
$.ajaxSetup({
          crossDomain: false, // obviates need for sameOrigin test
          beforeSend: function(xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
              xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
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

  // Remove success highlighting if clicking off of rows
  $('body').click(function() {
    $('.success').removeClass('success');
  });
});
