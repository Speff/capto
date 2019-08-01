function close_window(){
    pb = $('#close_progress');
    var p_filled = pb.attr('data-p_filled');
    var new_p = p_filled-7.6;
    pb.width(new_p + '%');
    if(p_filled < 0){
        window.close();
    }
    else{
        pb.attr('data-p_filled', new_p);
        console.log(new_p);
        setTimeout(close_window, 16);
    }
}

$(document).ready(function(){
    var twit_params = window.location.search;
    let searchParams = new URLSearchParams(window.location.search)

    if(searchParams.has('oauth_token') && searchParams.has('oauth_verifier')){
        $.get("/api/auth_twit" + twit_params, function(data){
            if(data.status = "Success")
                $('auth_status').text('Success');
            else
                $('auth_status').text('FAILED');

        });
    }
    else
        $('auth_status').text('FAILED');
    setTimeout(close_window, 16);
});
