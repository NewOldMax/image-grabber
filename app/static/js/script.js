var socket = io.connect('http://' + document.domain + ':' + location.port + '/main');
$(document).ready(function(){
    socket.on('connect', function() {
        console.log('connected');
        socket.on('grabed_count', function (msg) {
            $('#current').text(msg);
        });
        socket.on('finish', function (msg) {
            if (msg == 'saving') {
                $('.wr .count').html('Saving to database...');
            } else if (msg == 'finish') {
                location.href = location.href;
            }
        });
    });

    $('#grab-form').submit(function() {
        var form = $(this);
        var count = form.find('#image_count').val();
        var url = form.find('#site_url').val();
        var event = 'grab_'+form.find('#work_type').val();
        send(event, url, count);
        startLoading($('body'));
        $('#current').text(0);
        $('#total').text(count);
        return false;
    });
})

function send(event, url, count) {
    socket.emit(event, {
        site_url: url,
        image_count: parseInt(count)
    });
}

var progressBar =   '<div class="wr">'+
                        '<div class="count"><span id="current"></span> / <span id="total"></span></div>'+
                        '<div class="sk-circle">'+
                          '<div class="sk-circle1 sk-child"></div>'+
                          '<div class="sk-circle2 sk-child"></div>'+
                          '<div class="sk-circle3 sk-child"></div>'+
                          '<div class="sk-circle4 sk-child"></div>'+
                          '<div class="sk-circle5 sk-child"></div>'+
                          '<div class="sk-circle6 sk-child"></div>'+
                          '<div class="sk-circle7 sk-child"></div>'+
                          '<div class="sk-circle8 sk-child"></div>'+
                          '<div class="sk-circle9 sk-child"></div>'+
                          '<div class="sk-circle10 sk-child"></div>'+
                          '<div class="sk-circle11 sk-child"></div>'+
                          '<div class="sk-circle12 sk-child"></div>'+
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