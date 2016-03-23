
var ip_list = $("#ip_list");

$("table").delegate(".ip-del","click",function(){
    var _this = $(this);
    var ip = _this.attr("ip");
    var netmask = _this.attr("netmask");
    var nic = _this.attr("nic");
    var s_ip = _this.attr("s_ip");
    var param = {"func":"ip_del","ip":ip,"s_ip":s_ip,"nic":nic,"netmask":netmask};
    var loading = start_loading(_this);
    var param_confirm = {"title":"提示","content":"确认删除IP '"+ip+"' ?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_net.php",param,function(data){
                if(data.result){
                    alert("删除IP '"+ip+"' 成功","success");
                    ip_list.trigger("data.update");
                }else{
                    alert("删除IP '"+ip+"' 失败");
                }
                loading.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            loading.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});


