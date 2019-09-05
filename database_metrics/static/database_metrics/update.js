// var f = function () {
//     // var time = document.getElementsByTagName('tr')[1].getElementsByTagName('td')[5].textContent;
//
//
//     var id = $('#id_div').text();
//
//     // console.log(typeof(rows[0]));
//
//     $.ajax({
//         url: '/database_metrics/ajax/',
//         data: {
//             "id": id
//         },
//         dataType: 'json',
//         success:function (response) {
//
//             $('#id_div').text(response[0].fields.id);
//             for (var obj in response){
//                 var fields = obj.fields;
//
//                 var connections_number = "<td>" + fields.connections_number + "</td>";
//                 var max_connections_number = "<td>" + fields.max_connections_number + "</td>";
//                 var rollback_percent = "<td>" + fields.rollback_percent + "</td>";
//                 var database_size = "<td>" + fields.database_size + "</td>";
//                 var time = "<td>" + fields.time + "</td>";
//                     var status = fields.db_work_status;
//                 if (status){
//                     st = "<img src='../mainpage/images/ok.png'>"
//                 }
//                 else{
//                     st = "<img src='../mainpage/images/error.png'>"
//                 }
//                 var result = "<tr>" + status + max_connections_number + connections_number + rollback_percent + database_size +
//                     st + time + "</tr>";
//                 $('#table_header').after(result);
//
//             }
//         }
//     })
// };
//
// var timerID = setInterval(f, 2000);
