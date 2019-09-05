var i = 1, j = 0;
for(i; i<7; i++)
{
    a = document.getElementsByClassName(i);
    if(a.length === 0)
    {
        continue;
    }
    else
    {
        for(j=0;j<a.length;j++)
        {
            if(i<3)
            {
                a[j].style.backgroundColor = "green";
            }
            if(i>=3 && i<6)
            {
                a[j].style.backgroundColor = 'yellow';
                // a[j].addClass('warning');
            }
            if (i>=6)
            {
                a[j].style.backgroundColor = "red"
            }
        }
    }
}

var f = function () {
    var id = $('#abb_id').text();
    var lri = $('#last_rec_id').text();

    $.ajax({
    data:{
        'id':id,
        'last_rec_id':lri
    },
    url:'/ajax2',
    dataType:'json',
    success: function (response) {

        var name = response.name;
        var new_lri = response.lri;
        var lri = $('#last_rec_id').text();
        if (lri === new_lri)
        {
            return;
        }
         for(var i=response.list.length-1; i>=0; i--) {
             var t = "<td>" + response.list[i].t + "C</td>";
             var cpu = '<td>' + response.list[i].cpu + '%</td>';
             var time = '<td>' + response.list[i].time_c + '</td>';
             var res = $('<tr>' + t + cpu + time + '</tr>');
             $("#header_row").after(res);
         }
         $("#last_rec_id").text(new_lri);

    }
});
};


var timerID = setInterval(f,1000);


