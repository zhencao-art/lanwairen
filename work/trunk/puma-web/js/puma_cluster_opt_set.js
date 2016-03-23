var cls_opt_set_modal = $("#cls_opt_set"),
    cls_opt_set_error_msg = $("#cls_opt_set_error_msg"),
    cls_opt_set_btn = $("#cls_opt_set_btn"),
    cls_opt_name = $("#cls_opt_name"),
    cls_opt_value = $("#cls_opt_value"),
    cls_opt_set_loadding = $("#cls_opt_set_loadding");

$(".cls-opt-table").delegate(".cls-opt-upt","click",function(){
    var _this = $(this);
    cls_opt_name.attr("cluster_key",_this.attr("cluster_key"));
    cls_opt_name.html(_this.attr("cluster_key_name"));
    cls_opt_value.val(_this.attr("cluster_value"));
    cls_opt_set_loadding.addClass("hidden");
    cls_opt_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});

cls_opt_set_btn.on("click",function(){
    var _this = $(this);
    var cluster_key = cls_opt_name.attr("cluster_key");
    var cluster_value = cls_opt_value.val();
    var checked = check_input(cls_opt_set_modal);
    if(!checked){
        return;
    }
    var param = {"func":"set_cluster","key":cluster_key,"value":cluster_value};
    var param_confirm = {"title":"提示","content":"确定修改属性'"+cls_opt_name.html()+"'?",
        "sub_callback":function(){
            cls_opt_set_loadding.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    if($("#cluster_list")){
                        $("#cluster_list").trigger("data.update");
                    }
                }else{
                    alert(data.msg);
                }
                cls_opt_set_modal.modal("hide");
                cls_opt_set_loadding.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});