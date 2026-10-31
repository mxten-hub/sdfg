$(document).ready(function(){
    
    $('#reg').on('submit',function(e){
        e.preventDefault(); 
        
        if ($('#password').val() !== $('#confirm_password').val()) {
            alert('Пароли не совпадают!');
            return;
        }

        $.ajax({
            url: '/user_register',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                name: $('#fullname').val(),
                password: $('#password').val(),
                email: $('#email').val()
            }),
            success: function(response) {
                if(response.result) {
                    alert('Регистрация успешна! Сейчас перенаправим на вход.');
                    window.location.href = '/login';
                } else {
                    alert('Ошибка регистрации. Возможно, такой email уже есть.');
                }
            },
            error: function() {
                alert('Ошибка сервера при регистрации.');
            }
        });
    });

    $('#log').on('submit',function(e){
        e.preventDefault(); 
        
        $.ajax({
            url: '/user_autorization',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                password: $('#password').val(),
                email: $('#email').val() 
            }),
            success: function(response) {
                if(response.result) {
                    window.location.href = '/lk';
                } else {
                    alert('Неверный email или пароль!');
                }
            },
            error: function() {
                alert('Ошибка сервера при входе.');
            }
        });
    });
});