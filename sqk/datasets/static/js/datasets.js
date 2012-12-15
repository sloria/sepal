Datasets = {};

Datasets.refresh_instance_row = function(instance_id){
    var row = $('tr[data-instance-id=' + instance_id + ']');
    $.get('instances/' + instance_id + '/row', function(data) {
        row.replaceWith(data);
            alert('Load was performed.');
});
}

Datasets.refresh_if_ready = function(instance_id) {
    $.get('instances/' + instance_id + "/ready.json", function(data) {
        if (data.ready) {
            Datasets.refresh_instance_row(instance_id);
        } else {
            Datasets.check_ready(instance_id);
        }
    });
};

Datasets.check_ready = function(instance_id) {
    setTimeout(function() {
        Datasets.refresh_if_ready(instance_id);
    }, 10 * 1000);
};