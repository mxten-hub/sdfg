$(document).ready(function(){
    $('#reg').on('submit',function(e){
        e.preventDefault();
        err = 0;
        if ($('#fullname').val().trim() === '' || $('#password').val().trim() != $('#confirm_password').val().trim()){
            err = 1;
        }else{
            err = 0;
        }
        if (err == 0){
            $.ajax({
                url: '/user_register',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    name: $('#fullname').val(),
                    password: $('#password').val(),
                    email: $('#email').val()
                })
            })
        }
    })

    $('#log').on('submit',function(e){
        e.preventDefault();
                $.ajax({
                    url: '/user_autorization',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        password: $('#password').val(),
                        email: $('#username').val()
                    })
                })
    })
})

