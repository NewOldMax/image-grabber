var socket = io.connect('http://' + document.domain + ':' + location.port);
$(document).ready(function(){
    socket.on('connect', function() {
        console.log('connected');
        socket.on('grabed_count', function (msg) {
            $('#current').text(msg);
        });
        socket.on('finish', function (msg) {
            location.href = location.href;
        });
    });

    $('#grab-form').submit(function() {
        var form = $(this);
        var count = form.find('#image_count').val();
        var url = form.find('#site_url').val()
        send(url, count);
        startLoading($('body'));
        $('#current').text(0);
        $('#total').text(count);
        return false;
    });
})

function send(url, count) {
    socket.emit('grab', {
        site_url: url,
        image_count: parseInt(count)
    });
}

var progressBar =   '<div class="wr">'+
                        '<div class="count"><span id="current"></span> / <span id="total"></span></div>'+
                        '<div class="progress progress-striped active">'+
                            '<div class="progress-bar" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width: 100%"></div>'+
                        '</div>'+
                    '</div>';

function startLoading(target) {
    target.append(progressBar);
}

function stopLoading(target) {
    var result = target.find('.wr');
    if (result.length > 0)
    {
        result.remove();
    }
}