var hardmon_cluster = $("#hardmon_cluster");
hardmon_cluster.on("refresh_chart",function(event){
    $('.mon-line-chart').each(function(i,obj){
        var _this = $(this);
        var unit_name = _this.attr("unit_name"),
            series_color = _this.attr("series_color");
        $.getJSON("data/data_dash.php?func=data_hist",function(data){
            fill_line_mini($(obj),data.data,series_color,unit_name);
        });
    });
});

$("tbody").delegate(".node-info","click",function(){
    var _this = $(this);
    _this.parent().parent().parent().addClass("no-refresh");
    var info_node = $("#info_node_tr_new"),
        node_id = _this.attr("node_id");
    if(info_node.length==0){
        info_node = $("<tr id='info_node_tr_new' class='child-tr detail-tabletr auto-refresh' node_id='"+node_id+"'> <td colspan='5'>"+$("#info_node_tr").html()+"</td></tr>");
    }else{
        if(info_node.attr("node_id")==node_id && !info_node.hasClass("hidden")){
            info_node.addClass("hidden");
            return;
        }
    }
    info_node.removeClass("hidden");
    info_node.attr("node_id",node_id);
    info_node.insertAfter(_this.parent().parent());
    info_node.trigger("data.update");
    return false;
});

$("tbody").delegate(".detail-tabletr","data.update",function(){
    var _this = $(this),
        node_id = _this.attr("node_id"),
        disk_list = _this.find("#node_disk_list"),
        port_list = _this.find("#node_port_list");
    $.getJSON("data/data_mon.php?func=node_infos&node_id="+node_id,function(data){
        if(data.result){
            disk_list.empty();
            $.each(data.disks,function(i,item){
                var color = "status-normal";
                if(item.status==0){
                    color = "status-uninit";
                }else if(item.status==2){
                    color = "status-offline";
                }
                disk_list.append("<div class='node-disk "+color+"'>"+item.slot+"</div>");
            });
            port_list.empty();
            $.each(data.ports,function(i,item){
                port_list.append("<div class='node-port'>"+item.port+"</div>");
            });
        }
    });
    
    _this.find('.mon-node-chart').each(function(i,obj){
        var __this = $(this);
        var unit_name = __this.attr("unit_name"),
            series_name = __this.attr("series_name"),
            series_color = __this.attr("series_color");
        $.getJSON("data/data_mon.php?func=data_hist&name="+series_name,function(data){
            fill_line_mini($(obj),data.data,series_color,unit_name);
        });
        
    });
    
    return false;
});