/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 */

 $(function () {
    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload()
    .bind('fileuploaddone', function (e, data) {
        var instance_data = data.result[0]['instance_data'];
        var instance_id = data.result[0]['instance_id'];
        var a = oTable.fnAddData(instance_data);
        var oSettings = oTable.fnSettings();
            // Get the added row and add the 'success' class
            var newRow = oSettings.aoData[ a[0] ].nTr;
            $(newRow).addClass('success')
                // Attach the data-id attribute
                .data('id', instance_id);
            // FIXME: make label editable
            // $(".instance-label[data-id=" + instance_id + "]").editable({
            //    type: 'text',
            //    showbuttons: false,
            //    pk: instance_id,
            //    url: data.result[0]['edit_label_url'],
            //    value: '',
            //    title: 'Edit instance label',
            //    success: function(data, new_label){
            //     Viz.data = data;
            //     Viz.scatterPlot();
            //     }
            // });
        })
    .bind('fileuploadstop', function(e) {
        console.log('finished');
        Viz.reloadData();
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