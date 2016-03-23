var map_add_modal = $("#map_add"),
    btn_map_add = $("#map_add_btn"),
    input_map_ip_name = $("#map_ip_name"),
    input_map_ip_mask = $("#map_ip_mask"),
    input_map_ip_nic = $("#map_ip_nic"),
    input_map_tgt_iqn = $("#map_tgt_iqn"),
    input_map_lv_name = $("#map_lv_name"),
    map_add_loadding = $("#map_add_loadding"),
    map_update_modal = $("#map_update"),
    input_map_lun_num = $("#map_lun_num"),
    input_map_ip = $("#map_ip"),
    input_map_path = $("#map_path"),
    btn_map_update = $("#map_update_btn"),
    map_update_loadding = $("#map_update_loadding");

$(".map-add").on("click",function(){
    input_map_ip_name.val("");
    input_map_ip_mask.val("24");
    input_map_tgt_iqn.val("");
    input_map_ip_nic.trigger("data.update");
    input_map_lv_name.trigger("data.update");
    map_add_loadding.addClass("hidden");
    var op_div = $("#client_add_list");
    op_div.html("");
    add_client(op_div,"","ro");
    map_add_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});
$("table").delegate(".map-up","click",function(){
    map_update_loadding.addClass("hidden");
    var _this = $(this),
        allowed_initiators = _this.attr("allowed_initiators");
    var op_div = $("#client_update_list");
    op_div.html("");
    input_map_lun_num.val(_this.attr("lun"));
    input_map_ip.val(_this.attr("ip"));
    input_map_path.val(_this.attr("path"));
    if(allowed_initiators){
        var inits = allowed_initiators.split(" ");
        for(var idx = 0; idx < inits.length; idx++){
            var ini = inits[idx].split(";");
            add_client(op_div,ini[0],ini[1]);
        }
    }else{
        add_client(op_div,"","ro");
    }
    map_update_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});

input_map_ip_nic.on("data.update",function(){
    input_map_ip_nic.html("<option value=''>自动选择</option>");
    $.getJSON("data/data_net.php?func=list_nic&flag=local",function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                input_map_ip_nic.append("<option value='"+item.nic_name+"'>"+item.nic_name+"</option>");
            });
        } 
    });
});
input_map_lv_name.on("data.update",function(){
    input_map_lv_name.empty();
    $.getJSON("data/data_lv.php?func=list_lv_json",function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                input_map_lv_name.append("<option value='"+item.lv_name+"'>"+item.lv_name+"</option>");
            });
        } 
    });
});

btn_map_add.on("click",function(){
    var _this = $(this);
    var ip_name = input_map_ip_name.val();
    var ip_mask = input_map_ip_mask.val();
    var ip_nic = input_map_ip_nic.val();
    var tgt_iqn = input_map_tgt_iqn.val();
    var lv_name = input_map_lv_name.val();
    var checked = check_input(map_add_modal);
    if(!checked){
        return;
    }
    if(!lv_name){
        alert("请选择逻辑卷!");
        return;
    }
    var ini_iqn = [];
    var ini_check = {};
    var ini_checked = "";
    $("#client_add_list .client-add-list").each(function(){
        var _child = $(this);
        var iqn = _child.find(".map-ini-iqn").val();
        if(!iqn){
            return;
        }
        if(ini_check[iqn]){
            ini_checked = iqn;
        }
        ini_check[iqn] = true;
        var rule = "ro";
        _child.find("input[type='radio']").each(function(){
            if(this.checked){
                rule = this.value;
            }
        });
        ini_iqn.push({"iqn":iqn,"acess":rule});
    });
    if(ini_checked){
        alert("客户端IQN '"+ini_checked+"' 重复");
        return;
    }
    map_add_modal.modal("hide");
    var param = {"func":"map_add","ip_name":ip_name,"ip_mask":ip_mask,"ip_nic":ip_nic,"tgt_iqn":tgt_iqn,"ini_iqn":ini_iqn,"lv_name":lv_name};
    var param_confirm = {"title":"提示","content":"确定新增Target?",
        "sub_callback":function(){
            map_add_modal.modal("show");
            map_add_loadding.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert("新增Target成功","success");
                    map_add_modal.modal("hide");
                }else{
                    alert("新增Target失败"+(data.msg?(","+data.msg):""));
                }
                if($("#map_list")){
                    delay_func('$("#map_list").trigger("data.update");');
                }
                map_add_loadding.addClass("hidden");
            },"json");
    },"cancel_callback":function(){
        map_add_modal.modal("show");
    }};
    make_confirm(param_confirm);
});

$("form").delegate(".client-minus","click",function(){
    var _this = $(this);
    JT_close(_this.attr("for"));
    _this.parent().parent().parent().parent().remove();
});
$(".client-add").on("click",function(){
    var op_div = $("#client_add_list");
    add_client(op_div,"","ro");
});
$(".client-update").on("click",function(){
    var op_div = $("#client_update_list");
    add_client(op_div,"","ro");
});
function add_client(target,iqn,ro_ra){
    var name = Math.round(Math.random()*100000);
    var ro_checked = ro_ra=="ro"?"checked":"";
    var rw_checked = ro_ra=="rw"?"checked":"";
    target.append('<div class="form-group client-add-list">'+
                        '<label class="control-label col-sm-2" for="ini_iqn_'+name+'" msg="客户端IQN">客户端IQN</label>'+
                        '<div class="col-sm-4">'+
                        '    <input class="form-control map-ini-iqn" id="ini_iqn_'+name+'" placeholder="输入客户端IQN" value="'+iqn+'" reg="^[\\w|.|\\-|:]{0,50}$" reg_tip="输入50位以内的字母、数字、-、:或小圆点">'+
                        '</div>'+
                        '<label class="control-label col-sm-2">客户端权限</label>'+
                        '<div class="col-sm-3">'+
                        '    <label class="radio-inline">'+
                        '      <input type="radio" name="'+name+'" value="ro" '+ro_checked+'> 只读'+
                        '    </label>'+
                        '    <label class="radio-inline">'+
                        '      <input type="radio" name="'+name+'" value="rw" '+rw_checked+'> 读写'+
                        '    </label>'+
                        '    <label class="radio-inline">'+
                        '        <span><a href="#" class="client-minus text-large" title="删除客户端" for="ini_iqn_'+name+'"><span class="glyphicon glyphicon-minus"> </span></a></span>'+
                        '    </label>'+
                        '</div>'+
                      '</div>');
}

btn_map_update.on("click",function(){
    var _this = $(this);
    var lun_num = input_map_lun_num.val();
    var map_ip = input_map_ip.val();
    var map_path = input_map_path.val();
    var checked = check_input(map_update_modal);
    if(!checked){
        return;
    }
    var ini_iqn = [];
    var ini_check = {};
    var ini_checked = "";
    $("#client_update_list .client-add-list").each(function(){
        var _child = $(this);
        var iqn = _child.find(".map-ini-iqn").val();
        if(!iqn){
            return;
        }
        if(ini_check[iqn]){
            ini_checked = iqn;
        }
        ini_check[iqn] = true;
        var rule = "ro";
        _child.find("input[type='radio']").each(function(){
            if(this.checked){
                rule = this.value;
            }
        });
        ini_iqn.push({"iqn":iqn,"acess":rule});
    });
    if(ini_checked){
        alert("客户端IQN '"+ini_checked+"' 重复");
        return;
    }
    map_update_modal.modal("hide");
    var param = {"func":"map_update","lun_num":lun_num,"map_ip":map_ip,"map_path":map_path,"ini_iqn":ini_iqn};
    var param_confirm = {"title":"提示","content":"确定修改Target?",
        "sub_callback":function(){
            map_update_modal.modal("show");
            map_update_loadding.removeClass("hidden");
            $.post("data/data_map.php",param,function(data){
                if(data.result){
                    alert("修改Target成功","success");
                    if($("#map_list")){
                        $("#map_list").trigger("data.update");
                    }
                    map_update_modal.modal("hide");
                }else{
                    alert("修改Target失败"+(data.msg?(","+data.msg):""));
                }
                map_update_loadding.addClass("hidden");
            },"json");
    },"cancel_callback":function(){
        map_update_modal.modal("show");
    }};
    make_confirm(param_confirm);
});