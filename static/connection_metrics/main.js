$(document).ready(function()
{
    $(".dropdown").hover(function()
    {
        var X=$(this).attr('id');
        if(X==1)
        {
            $(".submenu").hide();
            $(this).attr('id', '0');
        }
        else
        {
            $(".submenu").show();
            $(this).attr('id', '1');
        }
    });

// //Mouse hover on sub menu
//     $(".submenu").mouseup(function()
//     {
//         return false;
//     });
//
// //Mouse hover on my account link
//     $(".menu").mouseup(function()
//     {
//         return false
//     });


//Document Click
    $(document).mouseup(function()
    {
        $(".submenu").hide();
        $(".menu").attr('id', '');
        });
    });