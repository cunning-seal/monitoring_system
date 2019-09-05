google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.setOnLoadCallback(drawBackgroundColor);

function drawBackgroundColor() {
    
    var id = $('#abb_id').text();
    $.ajax({
        data:{
            'id':id,
            'last_rec_id': -1
        },
        url:'/ajax2',
        dataType: 'json',
        success: function (response) {
            titleVar = '';
            var data= new google.visualization.DataTable();
            data.addColumn('string', 'Время');
            data.addColumn('number', 'Температура');
            dataarr = [];
            titleVar = response.name;
            metric_list = response.list;
            dataarr = metric_list.map(function (metric) {
                a = [metric.time_c.toString(), Math.round(metric.t)];
                return a;

            });
            data.addRows(dataarr);

            var options = {
            hAxis: {
              title: 'Время'
            },
            vAxis: {
              title: 'Температура'
            },
            backgroundColor: '#f1f8e9',
              title: titleVar
            };

            var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
            chart.draw(data, options);
        }
    });

      

    }