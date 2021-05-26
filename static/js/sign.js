function my_function1()
{
    debugger;
    var first_name_=$("#first_name").val();
    var last_name_=$("#last_name").val();
    var email_=$("#email").val();
    var password1_=$("#password1").val();
    var password2_=$("#password2").val();
    $.ajax({
        url:'/signUp',
        type:'post',
        data:{'first_name':first_name_,
            'last_name':last_name_,
            'email':email_,
            'password1':password1_,
            'password2':password2_,
        },
        success: function(resp)
        {
            debugger;
            if (resp['message']=='Success'){
                alert(resp['message']);
                window.location.href='/main';
            }
            console.log(resp);
        }

    });
}