var cluster_set_loadding = $("#cluster_set_loadding");

$(".cluster-func").on("click",function(){
    var func = $(this).attr("func_type");
    var param = {"func":func};
    var ops = func=="cluster_start"?"启动":"关闭";
    var param_confirm = {"title":"提示","content":"确定"+ops+"集群?",
        "sub_callback":function(){
            cluster_set_loadding.removeClass("hidden");
            $.post("data/data_cluster.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                }else{
                    alert(data.msg);
                }
                cluster_set_loadding.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});