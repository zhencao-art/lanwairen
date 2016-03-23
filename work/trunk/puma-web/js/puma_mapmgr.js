var map_list = $("#map_list"),
    map_move_host = $("#map_move_host"),
    map_move_sub = $("#map_move_sub"),
    map_move_modal = $("#map_move_modal"),
    map_move_loading = $("#map_move_loadding");

$("table").delegate(".init-lists","click",function(){
    var _this = $(this)
        allowed_initiators = _this.attr("allowed_initiators"),
        target_id = _this.attr("target_id");
    if($("#"+target_id).length!=0){
        $("#"+target_id).toggleClass("hidden");
        return;
    }
    var htmls = "<tr class='init-detail' id='"+target_id+"'><td colspan='6'><table class='table child-table'><thead><tr><td>客户端IQN</td><td>权限</td></tr></thead><tbody>";
    if(allowed_initiators){
        var inits = allowed_initiators.split(" ");
        for(var idx = 0; idx < inits.length; idx++){
            var ini = inits[idx].split(";");
            htmls += "<tr><td>"+ini[0]+"</td><td>"+(ini[1]=="rw"?"读写":"只读")+"</td></tr>";
        }
    }else{
        htmls += "<tr><td colspan='2'><div class=\"alert alert-danger col-sm-12\" role=\"alert\"><strong>提示:</strong> 没有数据</div></td></tr>";
    }
    htmls += "</tbody></table></td></tr>";
    $(htmls).insertAfter(_this.parent().parent());
    return false;
});

$("table").delegate(".map-check","click",function(){
    var _this = $(this),
        ip = _this.attr("ip"),
        path = _this.attr("path");
    var loading = start_loading(_this);
    var param = {"func":"map_check","ip":ip,"path":path};
    var param_confirm = {"title":"提示","content":"确认测试Target是否可用?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    _this.parent().parent().find(".map-start").removeAttr("not_test");
                    alert("测试为可用","success");
                    // map_list.trigger("data.update");
                }else{
                    alert(data.msg?data.msg:"测试为不可用");
                    _this.parent().parent().find(".map-start").attr("not_test","true");
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

$("table").delegate(".map-stop","click",function(){
    var _this = $(this),
        target_id = _this.attr("target_id");
    var loading = start_loading(_this);
    var param = {"func":"map_stop","target_id":target_id};
    var param_confirm = {"title":"提示","content":"确认停用?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert("停用成功","success");
                }else{
                    alert(data.msg?data.msg:"停用失败");
                }
                delay_func('map_list.trigger("data.update");');
                loading.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            loading.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});

$("table").delegate(".map-start","click",function(){
    var _this = $(this),
        target_id = _this.attr("target_id");
    // if(_this.attr("not_test")){
        // alert("请先测试");
        // return;
    // }
    var loading = start_loading(_this);
    var param = {"func":"map_start","target_id":target_id};
    var param_confirm = {"title":"提示","content":"确认启用?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert("启用成功","success");
                }else{
                    alert(data.msg?data.msg:"启用失败");
                }
                delay_func('map_list.trigger("data.update");');
                loading.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            loading.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});

$("table").delegate(".map-move","click",function(){
    var _this = $(this),
        cur_host = _this.attr("cur_host");
    map_move_host.attr("cur_host",cur_host);
    map_move_host.trigger("update.data");
    map_move_sub.attr("target_id",_this.attr("target_id"));
    map_move_loading.addClass("hidden");
    map_move_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

map_move_host.on("update.data",function(i,item){
    var _this = $(this);
    _this.html("");
    $.getJSON("data/data_map.php?func=host_list",function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                if(item.host_name == _this.attr("cur_host")){
                    return;
                }
                _this.append("<option value='"+item.host_name+"'>"+item.host_name+"</option>");
            });
        }
    });
});

$("table").delegate(".map-del","click",function(){
    var _this = $(this);
    var ip = _this.attr("ip");
    var path = _this.attr("path");
    var loading = start_loading(_this);
    var param = {"func":"map_del","ip":ip,"path":path};
    var param_confirm = {"title":"提示","content":"确认删除Target?",
        "sub_callback":function(){
            loading.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert("删除Target成功","success");
                }else{
                    alert(data.msg?data.msg:"删除Target失败");
                }
                map_list.trigger("data.update");
                loading.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            loading.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});

map_move_sub.on("click",function(){
    var _this = $(this);
    var target_id = _this.attr("target_id");
    var host_name = map_move_host.val();
    if(!host_name){
        alert("请选择要迁移到的节点");
        return;
    }
    var param = {"func":"map_move","target_id":target_id,"host_name":host_name};
    var param_confirm = {"title":"提示","content":"确定迁移此资源?",
        "sub_callback":function(){
            map_move_loading.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    map_move_modal.modal("hide");
                }else{
                    alert(data.msg);
                }
                map_list.trigger("data.update");
                map_move_loading.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});
// node_filter.trigger("data.update");

