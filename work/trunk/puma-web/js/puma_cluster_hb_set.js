var cluster_hb_set_modal = $("#cluster_hb_set"),
    cluster_hb_set_error_msg = $("#cluster_hb_set_error_msg"),
    cluster_hb_set_btn = $("#cluster_hb_set_btn"),
    cluster_hb_set_loadding = $("#cluster_hb_set_loadding");

$(".hb-table").delegate(".cls-hb-upt","click",function(){
    $(".cluster-hb-nic").attr("node_mask","");
    $(".cluster-hb-nic").attr("node_ip","");
    $(".cluster-hb-nic").val("");
    $(".hb-set-tr").each(function(i,item){
        var _this = $(this);
        $("#cluster_hb_host_"+i).html(_this.attr("node_name"));
        $("#cluster_hb_ip_"+i).val(_this.attr("node_ip"));
        // $("#cluster_hb_nic_"+i).attr("node_nic",_this.attr("node_nic"));
        $("#cluster_hb_nic_"+i).attr("node_ip",_this.attr("node_ip"));
        $("#cluster_hb_nic_"+i).trigger("data.update");
        $("#cluster_hb_mask_"+i).val(_this.attr("node_mask"));
    });
    cluster_hb_set_loadding.addClass("hidden");
    cluster_hb_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});

$(".cluster-hb-nic").on("data.update",function(){
    var _this = $(this);
    // var node_nic = _this.attr("node_nic");
    var node_nic = "";
    var node_mask = "";
    var node_ip = _this.attr("node_ip");
    _this.html("<option value=''></option>");
    $.getJSON("data/data_net.php?func=list_nic_info&node_ip="+node_ip,function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                _this.append("<option value='"+item.nic_name+"'>"+item.nic_name+"</option>");
                if(item.ip){
                    node_nic = item.nic_name;
                    node_mask = item.mask;
                }
            });
            if(node_nic){
                _this.val(node_nic);
                if($("#cluster_hb_nic_0").attr("node_ip") == node_ip){
                    $("#cluster_hb_mask_0").val(node_mask);
                }else{
                    $("#cluster_hb_mask_1").val(node_mask);
                }
            }
        }
    });
});

cluster_hb_set_btn.on("click",function(){
    var _this = $(this);
    var checked = check_input(cluster_hb_set_modal);
    if(!checked){
        return;
    }
    var ips = [];
    for(var i=0;i<2;i++){
        ips.push({"host":$("#cluster_hb_host_"+i).html(),
                    "ip":$("#cluster_hb_ip_"+i).val(),
                    "mask":$("#cluster_hb_mask_"+i).val(),
                    "nic":$("#cluster_hb_nic_"+i).val()});
    }
    var param = {"func":"set_hb","ips":ips};
    var param_confirm = {"title":"提示","content":"修改心跳IP将重启集群，确定修改?",
        "sub_callback":function(){
            cluster_hb_set_loadding.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    $("#hb_ip_list").trigger("data.update");
                    cluster_hb_set_modal.modal("hide");
                }else{
                    alert(data.msg);
                }
                cluster_hb_set_loadding.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});