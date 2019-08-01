(function($) {
    $.fn.invisible = function() {
        return this.each(function() {
            $(this).css("visibility", "hidden");
        });
    };
    $.fn.visible = function() {
        return this.each(function() {
            $(this).css("visibility", "visible");
        });
    };
}(jQuery));

function send_form(){
    var payload = {};
    payload['label'] = $('#webhook_label').val();
    payload['webhook_url'] = $('#webhook_url').val();
    payload['twit_target'] = $('#twitter_target').val();
    payload['grab_type'] = $('#grab_type_pic').val();
    if($('#select_fav').hasClass('btn-ghost'))
        payload['s_fav'] = 'No';
    else payload['s_fav'] = 'Yes';
    if($('#select_post').hasClass('btn-ghost'))
        payload['s_post'] = 'No';
    else payload['s_post'] = 'Yes';
    payload['hook_uid'] = $('#btn_submit').data('uid');

    try{
        $.ajax({
            url: '/api/add_hook',
            type: 'POST',
            data: payload,
            success: function(data){
                if(data.status == 'webhook stored'){
                    get_hooklist();
                }
                else{
                    console.log(data);
                    $('#signin_message')
                        .html('Server error')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            },
            error: function(xhr, status, error){
                console.log(status);
                console.log(error);
                if(status === 'error'){
                    $('#signin_message')
                        .html('Server offline')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            }
        });
    }
    catch(err){
        console.log(err);
    }
}

function fill_data(data){
    if($('#btn_submit').data('uid') == data.hook_uid){
        $('#btn_submit').removeData('uid');
        $('#webhook_label').val('');
        $('#webhook_url').val('');
        $('#twitter_target').val('');
        $('#grab_type_pic').val("No");
        $('#select_post').addClass('btn-ghost');
        $('#select_fav').addClass('btn-ghost');
        return null;
    }
    $('#btn_submit').data('uid', data.hook_uid);
    $('#webhook_label').val(data.label);
    $('#webhook_url').val(data.url);
    $('#twitter_target').val(data.twit_target);
    if(data.media_only)
        $('#grab_type_pic').val("Yes");
    else
        $('#grab_type_pic').val("No");
    if(data.posts)
        $('#select_post').removeClass('btn-ghost');
    else
        $('#select_post').addClass('btn-ghost');
    if(data.favorites)
        $('#select_fav').removeClass('btn-ghost');
    else
        $('#select_fav').addClass('btn-ghost');
}

function get_hooklist(){
    try{
        $.ajax({
            url: '/api/get_hooks',
            type: 'GET',
            success: function(data){
                if(data.status == 'ok'){
                    var existing_uids = [];
                    for(var i = 0; i < $('.menu-item').length; i++){
                        existing_uids
                            .push($('.menu-item').eq(i).data('hook_uid'));
                        console.log($('.menu-item').eq(i).data('hook_uid'));
                    }

                    var hooklist = data.webhooks;
                    for(var i = 0; i < hooklist.length; i++){
                        var hook_html = $('<a>');
                        var close_button = $('<div>')
                            .append('X');

                        hook_html.click(function(){
                            $(this).toggleClass('active')
                            fill_data($(this).data());
                        });

                        hook_html.addClass('menu-item');
                        close_button.addClass('pull-right');
                        close_button.addClass('pull-right item-delete');
                        hook_html.data(hooklist[i]);
                        close_button.data(hooklist[i]);

                        hook_html
                            .append(hooklist[i].label)
                            .append(close_button);
                        $('#webhook_list').append(hook_html);
                    }
                    
                }
                else{
                    console.log(data);
                    $('#signin_message')
                        .html('Server error')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            },
            error: function(xhr, status, error){
                console.log(status);
                console.log(error);
                if(status === 'error'){
                    $('#signin_message')
                        .html('Server offline')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            }
        });
    }
    catch(err){
        console.log(err);
    }
}

function get_twitter_name(){
    $('#signin_message')
        .html('Signed into twitter. Getting user data...');
    $('#signin_box').visible();
    try{
        $.ajax({
            url: '/api/get_twit_name',
            type: 'GET',
            success: function(data){
                if(data.status == 'Authenticated'){
                    get_hooklist();
                    $('#signin_message')
                        .html('Hello, ' + data.twitter_name);
                    $('#signin_box')
                        .removeClass('alert-error')
                        .addClass('alert-info');
                }
                else{
                    console.log(data);
                    $('#signin_message')
                        .html('Server error')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            },
            error: function(xhr, status, error){
                console.log(status);
                console.log(error);
                if(status === 'error'){
                    $('#signin_message')
                        .html('Server offline')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            }
        });
    }
    catch(err){
        console.log(err);
    }
}

function get_twitter_auth_url(){
    console.log('Not signed into twitter. Fetching link');
    $('#signin_box').visible();
    try{
        $.ajax({
            url: '/api/check_twit_signin',
            type: 'GET',
            success: function(data){
                if(data.status == 'ok'){
                    console.log('got signin link');
                    $('#signin_message')
                        .html('<a href="javascript:void(0)" id="signin_link"> Sign into Twitter </a>');
                    $('#signin_link')
                        .click(function(){
                            var popup = window.open( data['auth_url'], '_blank',
                                'width=500,height=200,status=no');
                            var check_closed = window.setInterval(function() {
                                if (popup.closed != false){
                                    window.clearInterval(check_closed);
                                    window.setTimeout(function(){
                                        location.reload();
                                    }, 1000);
                                }
                            }, 200);
                        });
                }
                else{
                    console.log(data);
                    $('#signin_message')
                        .html('Server error')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            },
            error: function(xhr, status, error){
                console.log(status);
                console.log(error);
                if(status === 'error'){
                    $('#signin_message')
                        .html('Server offline')
                        .parent()
                        .visible();
                    $('#signin_box')
                        .removeClass('alert-info')
                        .addClass('alert-error');
                }
            }
        });
    }
    catch(err){
        console.log(err);
    }
}

function check_server(){
    console.log('Checking server');
    try{
        $.ajax({
            url: '/api/r_u_alive',
            type: 'GET',
            success: function(data){
                if(data.status === 'yes'){
                    if(data.twit_authed === 'signed in'){
                        get_twitter_name();
                        $('#btn_submit')
                            .removeClass('btn-ghost')
                            .click(send_form);
                        $('#webhook_list').empty();
                    }
                    else{
                        $('#signin_message')
                            .text('Not signed into twitter. Getting auth URL');
                        get_twitter_auth_url();
                    }
                }
                else{
                    console.log(data);
                    $('#signin_message')
                        .html('Server error')
                        .parent()
                        .visible();
                }
            },
            error: function(xhr, status, error){
                console.log(status);
                console.log(error);
                if(status === 'error'){
                    $('#signin_message')
                        .html('Server offline')
                        .parent()
                        .visible();
                }
            }
        });
    }
    catch(err){
        console.log(err);
    }
}

function setup_buttons(){
    $('#select_fav').click(function(){
        $(this).toggleClass('btn-ghost');
    });
    $('#select_post').click(function(){
        $(this).toggleClass('btn-ghost');
    });
}

$(document).ready(function(){
    console.log('Site started');
    check_server();
    setup_buttons();
});
