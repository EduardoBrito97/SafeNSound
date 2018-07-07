$(document).ready(function () {

    $('#delete-btn').click(function () {
        var device_name = $(this).attr('name');
        if (confirm('Are you sure you want unsync "' + device_name + '"'))
        {
            var device_id = $(this).val();
            window.location.href = '/devices/delete/'+device_id;
        }
    })
});
