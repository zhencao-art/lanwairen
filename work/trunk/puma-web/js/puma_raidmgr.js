
var node_filter = $("#node_filter"),
    filter_node = $("#filter_node"),
    raid_list = $("#raid_list"),
    raid_info_modal = $("#raid_info"),
    raid_cache_info = $(".raid-cache-info");

node_filter.on("data.update",function(){
    var _this = $(this);
    var url = _this.attr("data-url");
    _this.html("<li><a href='#' data-value=''>所有raid</a></li>");
    $.getJSON(url,function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                _this.append("<li><a href='#' data-value='"+item.node_id+"'>"+item.node_id+"</a></li>");
            });
        }
    });
});

$("table").delegate(".raid-info","click",function(){
    var _this = $(this)
        raid_name = _this.attr("raid_name");
    $(".raid-infotab").attr("raid_name",raid_name);
    $(".raid-infotab").trigger("update.data");
    
    raid_info_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

raid_info_modal.find(".panel").on("start_loading",function(){
    var _this = $(this);
    var loading = $(".data_loading[forid='"+this.id+"']");
    var panel_heading = _this.find(".panel-heading");
    if(loading.length==0){
        panel_heading.append("<span class='navbar-right data_loading hidden' forid="+this.id+"><img src='img/loading.gif' style='height:18px'/></span>");
        loading = $(".data_loading[forid='"+this.id+"']");
    }
    loading.removeClass("hidden");
}).on("end_loading",function(){
    var loading = $(".data_loading[forid='"+this.id+"']");
    loading.addClass("hidden");
});

$(".raid-infotab").on("update.data",function(){
    var _this = $(this),
        raid_name = _this.attr("raid_name");
    raid_info_modal.find(".panel").trigger("start_loading");
    $.getJSON("data/data_raid.php?func=raid_info&raid_name="+raid_name,function(data){
        raid_cache_info.addClass("hidden");
        if(data.result){
            $.each(data.data,function(i,item){
                if(i=="raid_info_cache_show" && item){
                    raid_cache_info.removeClass("hidden");
                    return;
                }
                $("#"+i).html(item);
            });
            $("#raid_info_disk_list").html(data.disks);
        }
        raid_info_modal.find(".panel").trigger("end_loading");
    });
});

$("#raid_add_modal").on('hidden.bs.modal', function (e) {
    raid_list.trigger("data.update");
});

node_filter.delegate("a","click",function(){
    var _this = $(this);
    var select = _this.attr("data-value");
    filter_node.html(select?select:"所有磁盘");
    raid_list.attr("data-url",raid_list.attr("data-url-source")+"&node_id="+select);
    raid_list.trigger("data.update");
    return false;
});

$("table").delegate(".raid-drop","click",function(){
    var _this = $(this);
    var raid_name = _this.attr("raid_name");
    var param_confirm = {"title":"提示","content":"确定删除RAID '"+raid_name+"'?",
        "sub_callback":function(){
            var param = {"func":"raid_drop","raid_name":raid_name};
            var loading = start_loading(_this);
            loading.removeClass("hidden");
            $.post("data/data_raid.php",param,function(data){
                if(data.result){
                    alert("删除RAID '"+raid_name+"' 成功","success");
                    raid_list.trigger("data.update");
                }else{
                    alert(data.error?data.error:("删除RAID '"+raid_name+"' 失败"));
                }
                loading.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});

// node_filter.trigger("data.update");

