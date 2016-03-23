var ip_add_modal = $("#ip_add"),
    btn_ip_add = $("#ip_add_btn"),
    input_ip_name = $("#ip_name"),
    input_ip_mask = $("#ip_mask"),
    input_ip_nic = $("#ip_nic"),
    input_ip_host = $("#ip_host"),
    input_ip_gateway = $("#ip_gateway"),
    net_add_loadding = $("#net_add_loadding");

$(".ip-add").on("click",function(){
    input_ip_name.val("");
    input_ip_mask.val("");
    input_ip_gateway.val("");
    $(".net-gateway").removeClass("hidden");
    input_ip_host.trigger("data.update");
    input_ip_nic.trigger("data.update");
    net_add_loadding.addClass("hidden");
    ip_add_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});
function check_gateway(){
    if(!nic_cache){
        return;
    }
    var cur_host = input_ip_host.val();
    var cur_nic = input_ip_nic.val();
    var hidden = false;
    $(".check-hb-nic").each(function(i,item){
        var _this = $(this);
        if(_this.attr("host")+"_"+_this.attr("ip") == cur_host && _this.attr("nic")==cur_nic){
            hidden = true;
        }
    });
    if(hidden){
        $(".net-gateway").addClass("hidden");
    }else{
        $(".net-gateway").removeClass("hidden");
    }
}
var nic_cache;
input_ip_nic.on("data.update",function(){
    if(nic_cache){
        return;
    }
    $.getJSON("data/data_net.php?func=list_nic",function(data){
        if(data.result){
            nic_cache = {};
            $.each(data.data,function(i,item){
                if(nic_cache[item.host_name]){
                    nic_cache[item.host_name].push(item.nic_name);
                }else{
                    nic_cache[item.host_name] = [item.nic_name];
                }
            });
            if(input_ip_host.val()){
                input_ip_host.trigger("change");
            }
        } 
    });
}).on("change",function(){
    check_gateway();
});
input_ip_host.on("data.update",function(){
    if(nic_cache){
        return;
    }
    input_ip_host.empty();
    $.getJSON("data/data_map.php?func=host_list",function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                input_ip_host.append("<option value='"+item.host_name+"_"+item.hb+"'>"+item.host_name+"</option>");
            });
            input_ip_host.trigger("change");
        } 
    });
}).on("change",function(){
    input_ip_nic.empty();
    if(nic_cache){
        var hostname = input_ip_host.val().substring(0,input_ip_host.val().lastIndexOf("_"));
        $.each(nic_cache[hostname],function(i,child){
            input_ip_nic.append("<option value='"+child+"'>"+child+"</option>");
        });
    }
    check_gateway();
});

btn_ip_add.on("click",function(){
    var _this = $(this);
    var ip_name = input_ip_name.val();
    var ip_mask = input_ip_mask.val();
    var ip_nic = input_ip_nic.val();
    var ip_host = input_ip_host.val();
    var ip_gateway = input_ip_gateway.val();
    var checked = check_input(ip_add_modal);
    if(!checked){
        return;
    }
    if(!ip_host){
        alert("请选择节点");
        return;
    }
    ip_add_modal.modal("hide");
    var param = {"func":"ip_add","ip_name":ip_name,"ip_mask":ip_mask,"ip_nic":ip_nic,"ip_host":ip_host,"ip_gateway":ip_gateway};
    var param_confirm = {"title":"提示","content":"确定新增IP地址'"+ip_name+"'?",
        "sub_callback":function(){
            ip_add_modal.modal("show");
            net_add_loadding.removeClass("hidden");
            $.post("data/data_net.php",param,function(data){
                if(data.result){
                    alert("新增IP地址成功","success");
                    if($("#ip_list")){
                        $("#ip_list").trigger("data.update");
                    }
                }else{
                    alert("新增IP地址失败");
                }
                ip_add_modal.modal("hide");
                net_add_loadding.addClass("hidden");
            },"json");
    },"cancel_callback":function(){
        ip_add_modal.modal("show");
    }};
    make_confirm(param_confirm);
});