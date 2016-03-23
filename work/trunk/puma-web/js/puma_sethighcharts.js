Highcharts.setOptions({
	global: {
		useUTC: false
	},
    "colors": [
        '#058DC7', '#50B432', '#ED561B', '#DDDF00', '#6AF9C4', '#64E572', '#24CBE5', '#FFF263', '#FF9655'
    ],
    credits: {
        enabled: false
    }
});

function fill_pie(target,data){
    if(target.highcharts()){
        target.highcharts().series[0].setData(data);
        return;
    }
    target.highcharts({
        chart: {
            backgroundColor: 'none',
            type: 'pie',
            spacing: [0,0,0,0]
        },
        title: {
            text: ''
        },
        tooltip: {
            enabled: false
        },
        plotOptions: {
            pie: {
                shadow: false,
                innerSize: 120,
                borderWidth: 0,
                dataLabels:{enabled: false},
                states:{
                    hover:{enabled: false}
                }
            },
            series: {        
                cursor: 'pointer',
            }
        },
        series: [{
            name: '',
            data: data
            }]
    });
}

function getTooltip(meticname,unit_k){
    var unit_G = unit_k * unit_k * unit_k;
    var unit_M = unit_k * unit_k;
    return {
        useHTML: true,
        shared: true,
        crosshairs: true,
        xDateFormat: '%Y年%m月%d日 %H时%M分',
        backgroundColor: 'rgba(0 , 0 , 0 , 0.85)',
        formatter: function () {
            var fmt = '<p style="margin: 0;padding: 0;text-align: right;color:#FFF">' + Highcharts.dateFormat('%Y年%m月%d日 %H时%M分', this.points[0].x) + '</p>';
            //循环当前鼠标位置上的所有点，计算宽度
            var nameWidth = 0, valueWidth = 0, meticWidth = 0, tableWidth = 0;
            var temp = $('<span style="display: none;"></span>');
            $('body').append(temp);

            $.each(this.points, function (i, point) {
                temp.html(point.series.name);
                var n = temp.width();
                if (n > nameWidth) {
                    nameWidth = n;
                }
                var yname = Highcharts.numberFormat(point.y, 2, ".", ",");
                if(point.y>unit_G){
                    yname = Highcharts.numberFormat(point.y/unit_G, 2, ".", ",");
                    meticname = "G"+meticname;
                }else if(point.y>unit_M){
                    yname = Highcharts.numberFormat(point.y/unit_M, 2, ".", ",");
                    meticname = "M"+meticname;
                }
                temp.html(yname);
                var v = temp.width();
                if (v > valueWidth) {
                    valueWidth = v;
                }

                var _metic = meticname;
                temp.html(_metic);
                var m = temp.width();
                if (m > meticWidth) {
                    meticWidth = m;
                }
            });
            temp.remove();
            temp = null;

            nameWidth += 5;
            valueWidth += 10;
            meticWidth += 5;
            tableWidth += nameWidth + valueWidth + meticWidth;

            $.each(this.points, function (i, item) {
                var series = item.series;
                var yname = Highcharts.numberFormat(item.y, 2, ".", ",");
                if(item.y>unit_G){
                    yname = Highcharts.numberFormat(item.y/unit_G, 2, ".", ",");
                    meticname = "G"+meticname;
                }else if(item.y>unit_M){
                    yname = Highcharts.numberFormat(item.y/unit_M, 2, ".", ",");
                    meticname = "M"+meticname;
                }
                fmt += '<table class="highchartsTipFormat" style="width: ' + tableWidth + 'px;"><tr><td style="width: ' + nameWidth + 'px;color: ' + series.color + ';">' + series.name + ':</td><td style="width: ' + valueWidth + 'px;"><b>' + yname + '</b></td><td style="width: ' + meticWidth + 'px;">' + meticname + '</td></tr></table>';
            });
            return fmt;
        }
    };
}

function fill_line_mini(target,data,color,unit_name){
    if(target.highcharts()){
        var chart = target.highcharts();
        $.each(data,function(i,item){
            for(var idx=0;idx<chart.series.length;idx++){
                if(chart.series[idx].name==item.name){
                    chart.series[idx].setData(item.data);
                    break;
                }
            }
        });
        target.highcharts().redraw();
        return;
    }
    var unit_k = target.attr("unit_k");
    var tip = getTooltip(unit_name,unit_k?unit_k:1024);
    target.highcharts({
        "colors": [
            color, "#FFD51B"
        ],
        chart: {
            backgroundColor: 'none',
            spacing: [0,0,0,0],
            // margin: [30,0,30,0]
            marginTop: 30,
            marginBottom: 25,
            marginRight: 0
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: "datetime",
            gridLineColor: '#606060',
            lineColor: '#606060',
            tickColor: '#606060',
            // tickInterval: 60000,
            tickLength: 5,
            tickPixelInterval: 50
        },
        yAxis: {
            title: { text: '' },
            lineWidth: 1,
            lineColor: '#606060',
            title: {
                align: 'high',
                offset: 0,
                text: unit_name,
                rotation: 0,
                y: -10,
                x: 20
            },
            labels:{
                x: -8
            },
            gridLineColor: '#606060',
            // tickAmount: 5,
            tickPositioner:function(){
                var positions = [],
                    tick = Math.floor(this.dataMin),
                    increment = Math.ceil((this.dataMax - this.dataMin) / 3.9);
                if(!this.dataMax){
                    return positions;
                }
                for (tick; tick - increment <= this.dataMax; tick += increment) {
                    positions.push(tick);
                }
                return positions;
            },
            min: 0
        },
        tooltip: tip,
        legend: {
            layout: 'horizontal',
            align: 'right',
            verticalAlign: 'top',
            borderWidth: 0,
            itemStyle:{ "color": "#FFF", "cursor": "pointer", "fontSize": "12px", "fontWeight": "normal" },
            padding: 0,
            y: 12
        },
        plotOptions: {
            line: {
                lineWidth: 1,
                animation : false
            },
            series: {
                allowPointSelect: false,
                marker: {
                    enabled: false
                }
            }
        },
        series: data
    });
}


function fill_line_middle(target,data,unit_name){
    if(target.highcharts()){
        var chart = target.highcharts();
        $.each(data,function(i,item){
            for(var idx=0;idx<chart.series.length;idx++){
                if(chart.series[idx].name==item.name){
                    chart.series[idx].setData(item.data);
                    break;
                }
            }
        });
        target.highcharts().redraw();
        return;
    }
    var unit_k = target.attr("unit_k");
    var tip = getTooltip(unit_name,unit_k?unit_k:1024);
    target.highcharts({
        chart: {
            backgroundColor: 'none',
            spacing: [0,0,0,0],
            // margin: [30,0,30,0]
            marginTop: 30,
            marginBottom: 25,
            marginRight: 0
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            type: "datetime",
            gridLineColor: '#606060',
            lineColor: '#606060',
            tickColor: '#606060',
            // tickInterval: 60000,
            tickLength: 5,
            tickPixelInterval: 55
        },
        yAxis: {
            title: { text: '' },
            lineWidth: 1,
            lineColor: '#606060',
            title: {
                align: 'high',
                offset: 0,
                text: unit_name,
                rotation: 0,
                y: -10,
                x: 15
            },
            labels:{
                x: -8
            },
            gridLineColor: '#606060',
            // tickAmount: 5,
            tickPositioner:function(){
                var positions = [],
                    tick = Math.floor(this.dataMin),
                    increment = Math.ceil((this.dataMax - this.dataMin) / 3.9);
                if(!this.dataMax){
                    return positions;
                }
                for (tick; tick - increment <= this.dataMax; tick += increment) {
                    positions.push(tick);
                }
                return positions;
            },
            min: 0
        },
        tooltip: tip,
        legend: {
            layout: 'horizontal',
            align: 'right',
            verticalAlign: 'top',
            borderWidth: 0,
            itemStyle:{ "color": "#FFF", "cursor": "pointer", "fontSize": "12px", "fontWeight": "normal" },
            padding: 0,
            y: 12
        },
        plotOptions: {
            line: {
                lineWidth: 1,
                animation : false
            },
            series: {
                allowPointSelect: false,
                marker: {
                    enabled: false
                }
            }
        },
        series: data
    });
}