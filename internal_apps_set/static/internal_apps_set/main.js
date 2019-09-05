var f = function () {
    var header = $('#header').text();
var id = header.split('.')[0].split(' ')[1];
$.ajax({
url:'/ajax',
type: 'GET',
data:{
    'id':id
},
dataType: 'json',
success: function (response) {
    var res = response.res_list;
    var chld = $('#main_table').children().children();
    if (chld.length ===1)
        console.log(1);
    else{
        for(var k = 1; k<chld.length; k++){
            chld[k].remove();
        }
    }
    for(var i = 0; i<res.length; i++){

        var abonent = "<td>"+ res[i].abonent + "</td>";
        var sentB = "<td>" + res[i].sentB + "</td>";
        var recvB = "<td>" + res[i].recvB + "</td>";
        var conN = "<td>" + res[i].conN + "</td>";

        if (res[i].flag === false){
            var disconT = "<td>" + res[i].disconT + "</td>";
            var r_disconT = "<td>" + res[i].r_disconT + "</td>";
            var conT = "<td></td>";
            var r_conT = "<td></td>";
            var indicator = "<th style='background-color: red'></th>"
        }
        else{
            var conT = "<td>" + res[i].conT + "</td>";
            var r_conT = "<td>" + res[i].r_conT + "</td>";
            var disconT = "<td></td>";
            var r_disconT = "<td></td>";
            var indicator = "<th style='background-color: green'></th>"
        }
        for_in = "<tr>" + abonent + sentB + recvB + conT + disconT + r_conT + r_disconT + conN + indicator + "</tr>";
        $("#main_table").append(for_in);

    }
}

});


};

var timerID = setInterval(f, 1000);

// var tID = setTimeout(function () {
//     clearInterval(timerID);
// }, 10000);