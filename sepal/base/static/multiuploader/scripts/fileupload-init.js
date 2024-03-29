/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 */

$(function() {
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload().bind('fileuploaddone', function(e, data) {
        // If the upload is successful
        if(!data.result[0]['error']) {
            var instanceData = data.result[0]['instance_data'],
                instanceId = String(data.result[0]['instance_id']),
                editUrl = encodeURI(data.result[0]["edit_label_url"]),
                added = oTable.fnAddData(instanceData),
                oSettings = oTable.fnSettings();

            // Get the added row and add the 'success' class
            var $newRow = $(oSettings.aoData[added[0]].nTr);
            $newRow.addClass('success');
            $newRow.data('id', instanceId);  // FIXME: Attach the data-id attribute

            // Make label name editable
            $(".instance-label[data-id=" + instanceId.toString() + "]").editable({
                type: 'text',
                showbuttons: false,
                pk: instanceId,
                url: editUrl,
                value: '',
                title: 'Edit instance label',
                success: function(data, new_label) {
                    Viz.reloadData();
                }
            });
        }
    }).bind('fileuploadstop', function(e) {
        console.log('Finished upload');
        Viz.reloadData();
    });

    // Load existing files:
    $.getJSON($('#fileupload form').prop('action'), function(files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files).appendTo($('#fileupload .files')).fadeIn(function() {
            // Fix for IE7 and lower:
            $(this).show();
        });
    });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function(e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>').prop('src', this.href).appendTo('body');
    });

});