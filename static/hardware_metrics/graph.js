var timeplot;

function onLoad() {
  var plotInfo = [
    Timeplot.createPlotInfo({
      id: "plot1"
    })
  ];

  timeplot = Timeplot.create(document.getElementById("my-timeplot"), plotInfo);
}

var resizeTimerID = null;
function onResize() {
    if (resizeTimerID == null) {
        resizeTimerID = window.setTimeout(function() {
            resizeTimerID = null;
            timeplot.repaint();
        }, 100);
    }
}

function onLoad() {
  var eventSource = new Timeplot.DefaultEventSource();
  var plotInfo = [
    Timeplot.createPlotInfo({
      id: "plot1",
      dataSource: new Timeplot.ColumnSource(eventSource,1),
      valueGeometry: new Timeplot.DefaultValueGeometry({
        gridColor: "#000000",
        axisLabelsPlacement: "left",
        min: 0,
        max: 150
      }),
      timeGeometry: new Timeplot.DefaultTimeGeometry({
        gridColor: new Timeplot.Color("#000000"),
        axisLabelsPlacement: "bottom"
      }),
      lineColor: "#19570f",
      fillColor: "#38a221",
      showValues: true
    })
  ];

  timeplot = Timeplot.create(document.getElementById("my-timeplot"), plotInfo);
  timeplot.loadText("../../static/hardware_metrics/data.txt", ",", eventSource);
}

