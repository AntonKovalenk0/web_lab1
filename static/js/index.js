function LogOut()
{
    debugger;
    console.log('logging out');
    $.ajax({
        url:'/log_out',
        type:'post',
        data:{},
        success: function(resp)
        {
            if (resp['message']=='Success')
                window.location.href='/';
        }
    });
}