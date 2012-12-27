/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 */

$(function () {
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload()
        .bind('fileuploaddone', function (e, new_data) {
            var instance_data = new_data.result[0]['instance_data'];
            console.log(instance_data);
            var a = oTable.fnAddData(instance_data);
            var oSettings = oTable.fnSettings();
            // Get the added row and add the 'success' class
            var nTr = oSettings.aoData[ a[0] ].nTr;
            $(nTr).addClass('success');
        })
        .bind('fileuploadstop', function(e) {
            console.log('finished');
            // TODO: update plot here
        });

    // Load existing files:
    $.getJSON($('#fileupload form').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
            .appendTo($('#fileupload .files'))
            .fadeIn(function () {
                // Fix for IE7 and lower:
                $(this).show();
            });
    });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });

});