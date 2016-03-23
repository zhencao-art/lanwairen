var lv_list = $("#lv_list");

$("tbody").delegate(".lv-drop","click",function(){
    var _this = $(this);
    var lv_name = _this.attr("lv_name"),
        vg_name = _this.attr("vg_name");
    var param_confirm = {"title":"提示","content":"确认删除卷'"+lv_name+"'?",
        "sub_callback":function(){
            var param = {"func":"lv_del","lv_name":lv_name,"vg_name":vg_name};
            var util_parent = _this.parents(".panel");
            var loading = util_parent.find(".region-loading");
            if(!loading || loading.length==0){
                util_parent.append("<div class='region-loading'><img src='img/loading.gif'></div>");
                loading = util_parent.find(".region-loading");
            }
            loading.css("width",util_parent.css("width"));
            loading.css("height",util_parent.css("height"));
            loading.removeClass("hidden");
            $.post("data/data_lv.php",param,function(data){
                if(data.result){
                    alert("删除卷成功","success");
                }else{
                    alert(data.data?data.data:"删除卷失败");
                }
                lv_list.trigger("data.update");
                loading.addClass("hidden");
            },"json");
        }}
    make_confirm(param_confirm);
    return false;
});