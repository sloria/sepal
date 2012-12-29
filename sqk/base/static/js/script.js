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

// Click handler for hiding visiualization
$(document).ready(function() {
  var viz = $('#visualization');
  var dataset = $('#dataset');
  // Add click handler for showing/hiding viz span
  $('#showHidePlot').on('click', function() {
    // Toggle visibility of the viz panel
    viz.toggle();
    viz.toggleClass('span5');
    // Expand/compress the table
    dataset.toggleClass('span7');
    oFC.fnRedrawLayout();
    oFC.fnRecalculateHeight();
    oTable.fnDraw(false);
    // oTable.fnAdjustColumnSizing();
  });
});