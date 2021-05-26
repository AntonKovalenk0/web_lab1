function logIn()
{
    debugger;
    var email_=$("#email").val();
    var password_=$("#password").val();
    $.ajax({
        url:'/',
        type:'post',
        data:{'email':email_,
              'password':password_
        },
        success: function(resp)
        {
            debugger;
            if (resp['message']=='Success')
                window.location.href='/main';
            else
                document.getElementById("login").innerHTML =
                    '<h1 style="color:crimson;">'+resp["message"]+'</h1>';
        }
    });
}