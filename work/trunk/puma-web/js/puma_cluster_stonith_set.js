var cluster_stonith_set_modal = $("#cluster_stonith_set"),
    cluster_stonith_set_error_msg = $("#cluster_stonith_set_error_msg"),
    cluster_stonith_set_add = $("#cluster_stonith_set_btn"),
    cluster_stonith_set_loadding = $("#cluster_stonith_set_loadding");

$(".stonith-table").delegate(".cls-stonith-enable","click",function(){
    if($(this).attr("is-exist")){
        set_stonith_able("enable");
        return false;
    }
    set_stonith_value("启用");
    cluster_stonith_set_add.attr("sth_type","enable");
});
$(".stonith-table").delegate(".cls-stonith-up","click",function(){
    set_stonith_value("提交");
    cluster_stonith_set_add.attr("sth_type","update");
});
$(".stonith-table").delegate(".cls-stonith-disable","click",function(){
    var _this = $(this);
    set_stonith_able("disable");
    return false;
});
function set_stonith_able(flag){
    var tip = "启用";
    if(flag == "disable"){
        tip = "禁用";
    }
    var loading = $("#cluster_set_loadding");
    var ipmis = [];
    $(".stonith-set-tr").each(function(i,item){
        var _thiss = $(this);
        ipmis.push({"host":_thiss.attr("node_name"),
                    "ip":_thiss.attr("node_ip"),
                    "uname":_thiss.attr("node_uname"),
                    "pass":_thiss.attr("node_pass"),
                    "sid":_thiss.attr("node_id")});
    });
    var param = {"func":"set_stonith","sth_type":flag,"ipmis":ipmis};
    var param_confirm = {"title":"提示","content":"确认"+tip+"此功能?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(tip+"此功能成功","success");
                    $("#sth_list").trigger("data.update");
                }else{
                    alert(tip+"此功能失败");
                }
                loading.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            loading.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
}

function set_stonith_value(title){
    $(".stonith-set-tr").each(function(i,item){
        var _this = $(this);
        $("#cluster_stonith_nodeid_"+i).val(_this.attr("node_id"));
        $("#cluster_stonith_host_"+i).html(_this.attr("node_name"));
        $("#cluster_stonith_ip_"+i).val(_this.attr("node_ip"));
        $("#cluster_stonith_uname_"+i).val(_this.attr("node_uname"));
        $("#cluster_stonith_pass_"+i).val(_this.attr("node_pass"));
        $("#cluster_stonith_repass_"+i).val(_this.attr("node_pass"));
    });
    cluster_stonith_set_add.html(title);
    cluster_stonith_set_loadding.addClass("hidden");
    cluster_stonith_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
}

cluster_stonith_set_add.on("click",function(){
    var _this = $(this);
    var checked = check_input(cluster_stonith_set_modal);
    if(!checked){
        return;
    }
    var pass0=$("#cluster_stonith_pass_0").val();
    var repass0=$("#cluster_stonith_repass_0").val();
    if(pass0!=repass0){
        $("#cluster_stonith_repass_0").trigger("blur",["","密码不一致"]);
        return;
    }
    var pass1=$("#cluster_stonith_pass_1").val();
    var repass1=$("#cluster_stonith_repass_1").val();
    if(pass1!=repass1){
        $("#cluster_stonith_repass_1").trigger("blur",["","密码不一致"]);
        return;
    }
    var ipmis = [];
    for(var i=0;i<2;i++){
        ipmis.push({"sid":$("#cluster_stonith_nodeid_"+i).val(),
                    "host":$("#cluster_stonith_host_"+i).html(),
                    "ip":$("#cluster_stonith_ip_"+i).val(),
                    "uname":$("#cluster_stonith_uname_"+i).val(),
                    "pass":$("#cluster_stonith_pass_"+i).val()});
    }
    var param = {"func":"set_stonith","sth_type":cluster_stonith_set_add.attr("sth_type"),"ipmis":ipmis};
    var param_confirm = {"title":"提示","content":"确定"+cluster_stonith_set_add.html()+"?",
        "sub_callback":function(){
            cluster_stonith_set_loadding.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    $("#sth_list").trigger("data.update");
                    cluster_stonith_set_modal.modal("hide");
                }else{
                    alert(data.msg);
                }
                cluster_stonith_set_loadding.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});