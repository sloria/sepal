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

  /* Remove selected and highlighted rows when clicking off of table. */
  $('body').click(function() {
    $('.success').removeClass('success');
    $('.selected').removeClass('selected');
  });

  /* Add click handler for showing/hiding viz span */
  var viz = $('#visualization');
  var dataset = $('#dataset');
  $('#showHidePlot').on('click', function() {
    // Toggle visibility of the viz panel
    viz.toggle();
    viz.toggleClass('span6');
    // Expand/compress the table
    dataset.toggleClass('span6');
    oFC.fnRedrawLayout();
    oFC.fnRecalculateHeight();
    oTable.fnDraw(false);
    // oTable.fnAdjustColumnSizing();
  });
});


function range(start, count)
{
    if(arguments.length == 1)
    {
        count = start;
        start = 0;
    }

    var foo = [];
    for (var i = 0; i < count; i++)
        foo.push(start + i);
    return foo;
}