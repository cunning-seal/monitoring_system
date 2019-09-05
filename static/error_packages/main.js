var f = function () {
    var chld = $('#main_table').children().children();
    var prev_lri = $("#last_rec_id").text();
    $.ajax({
        url:'/errors/ajax/',
        data:{
            'last_rec_id': prev_lri
        },
        dataType: 'json',
        success:function (response) {
            var lri = response.lri;
            var list = response.response;
            if (lri === prev_lri)
                return;
            $("#last_rec_id").text(lri);
            for(var i = list.length-1; i>=0; i--){
                ab = '<td><a href="../abonents/' + list[i].ab_id + '">'+ list[i].ab_name+'</a></td>';
                ap = '<td><a href="../apps/' + list[i].app_id + '">'+ list[i].app_name+'</a></td>';
                sub = '<td>' + list[i].subprocess + '</td>';
                descr = '<td>' + list[i].descr + '</td>';
                time = '<td>' + list[i].time + '</td>';
                if(list[i].i_level<3) {
                    result = '<tr style="background-color: green;"' + ab + ap + sub + descr + time + '</tr>';
                }
                if(list[i].i_level>=3 && list[i].i_level<6){
                    result = '<tr style="background-color: yellow;"' + ab + ap + sub + descr + time + '</tr>';
                }
                if(list[i].i_level>=6) {
                    result = '<tr style="background-color: red;"' + ab + ap + sub + descr + time + '</tr>';
                }
                $('#table_header').after(result);

            }

        }
    });
};

f();
var timerID = setInterval(f, 500);