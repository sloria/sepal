/*
 * jQuery File Upload Plugin JS Example 6.7
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint nomen: true, unparam: true, regexp: true */
/*global $, window, document */

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload().bind('fileuploaddone', function(e, data) {
        // If the upload is successful
        if(!data.result[0]['error']) {
            var instanceData = data.result[0]['instance_data'];
            var instanceId = String(data.result[0]['instance_id']);
            var editUrl = encodeURI(data.result[0]["edit_label_url"]);
            var added = oTable.fnAddData(instanceData);
            var oSettings = oTable.fnSettings();
            // Get the added row and add the 'success' class
            var newRow = oSettings.aoData[added[0]].nTr;
            $(newRow).addClass('success');
            // Attach the data-id attribute
            $(newRow).data('id', instanceId);

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
        console.log('finished');
        Viz.reloadData();
    });;

    // Enable iframe cross-domain access via redirect option:
    $('#fileupload').fileupload(
        'option',
        'redirect',
        window.location.href.replace(
            /\/[^\/]*$/,
            '/cors/result.html?%s'
        )
    );

    if (window.location.hostname === 'blueimp.github.com') {
        // Demo settings:
        $('#fileupload').fileupload('option', {
            url: '//jquery-file-upload.appspot.com/',
            maxFileSize: 5000000,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            process: [
                {
                    action: 'load',
                    fileTypes: /^image\/(gif|jpeg|png)$/,
                    maxFileSize: 20000000 // 20MB
                },
                {
                    action: 'resize',
                    maxWidth: 1440,
                    maxHeight: 900
                },
                {
                    action: 'save'
                }
            ]
        });
        // Upload server status check for browsers with CORS support:
        if ($.support.cors) {
            $.ajax({
                url: '//jquery-file-upload.appspot.com/',
                type: 'HEAD'
            }).fail(function () {
                $('<span class="alert alert-error"/>')
                    .text('Upload server currently unavailable - ' +
                            new Date())
                    .appendTo('#fileupload');
            });
        }
    } else {
        // Load existing files:
        $('#fileupload').each(function () {
            var that = this;
            $.getJSON(this.action, function (result) {
                if (result && result.length) {
                    $(that).fileupload('option', 'done')
                        .call(that, null, {result: result});
                }
            });
        });
    }

});
