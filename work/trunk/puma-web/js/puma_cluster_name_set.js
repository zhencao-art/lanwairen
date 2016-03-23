var cls_name_set_modal = $("#cls_name_set"),
    cls_name_set_error_msg = $("#cls_name_set_error_msg"),
    cls_name_set_btn = $("#cls_name_set_btn"),
    cls_name_value = $("#cls_name_value"),
    cls_name_set_loadding = $("#cls_name_set_loadding");

$(".cls-name-table").delegate(".cls-name-upt","click",function(){
    var _this = $(this);
    cls_name_value.val(_this.attr("cluster_value"));
    cls_name_set_loadding.addClass("hidden");
    cls_name_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});

cls_name_set_btn.on("click",function(){
    var _this = $(this);
    var cluster_value = cls_name_value.val();
    var checked = check_input(cls_name_set_modal);
    if(!checked){
        return;
    }
    var param = {"func":"set_cluster_name","name":cluster_value};
    var param_confirm = {"title":"提示","content":"修改集群名称将重启集群，确定修改?",
        "sub_callback":function(){
            cls_name_set_loadding.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    if($("#cluster_list")){
                        $("#cluster_list").trigger("data.update");
                    }
                }else{
                    alert(data.msg);
                }
                cls_name_set_modal.modal("hide");
                cls_name_set_loadding.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});