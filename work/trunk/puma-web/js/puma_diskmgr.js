
var node_filter = $("#node_filter"),
    filter_node = $("#filter_node"),
    disk_list = $("#disk_list");

// node_filter.on("data.update",function(){
    // var _this = $(this);
    // var url = _this.attr("data-url");
    // _this.html("<li><a href='#' data-value=''>所有磁盘</a></li>");
    // $.getJSON(url,function(data){
        // if(data.result){
            // $.each(data.data,function(i,item){
                // _this.append("<li><a href='#' data-value='"+item.node_id+"'>"+item.node_id+"</a></li>");
            // });
        // }
    // });
// });

$("table").delegate(".disk-info","click",function(){
    return false;
    var _this = $(this),
        disk_name = _this.attr("disk_name");
    $(".disk-infotab").attr("disk_name",disk_name);
    $(".disk-infotab").trigger("update.data");
    
    disk_info_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

disk_list.on("update.infos",function(e,data){
    $("#slot_all").html(data.all_count);
    $("#slot_used").html(data.used_count);
});
// $("#osd_add_modal").on('hidden.bs.modal', function (e) {
    // if($("#disk_info").attr("disk-pre-hide")){
        // $(".disk-infotab").trigger("update.data");
        // disk_info_modal.modal("show");
    // }
// });

// node_filter.delegate("a","click",function(){
    // var _this = $(this);
    // var select = _this.attr("data-value");
    // filter_node.html(select?select:"所有磁盘");
    // disk_list.attr("data-url",disk_list.attr("data-url-source")+"&node_id="+select);
    // disk_list.trigger("data.update");
    // return false;
// });

// node_filter.trigger("data.update");

