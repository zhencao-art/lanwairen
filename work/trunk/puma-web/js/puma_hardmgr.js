$('.main-line-chart').on("data.update",function(i,obj){
    var _this = $(this);
    var unit_name = _this.attr("unit_name");
    $.getJSON("data/data_hard.php?func=data_hist",function(data){
        fill_line_middle(_this,data.data,unit_name);
    });
});

$('.main-line-chart').trigger("data.update");