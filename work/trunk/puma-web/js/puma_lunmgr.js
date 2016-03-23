var lv_add_modal = $("#lv_add"),
    lv_op_modal = $("#lv_op"),
    lv_info_modal = $("#lv_info"),
    lv_list = $("#lv_list");
var lv_op_node_list = $("#lv_op_node_list"),
    btn_attach = $("#lv_op_attach"),
    btn_detach = $("#lv_op_detach"),
    check_all = $("#checkbox_all"),
    lv_add_error_msg = $("#lv_add_error_msg"),
    btn_lv_add = $("#lv_add_btn"),
    input_vol_name = $("#vol_name"),
    input_vol_size = $("#vol_size"),
    input_vol_copies = $("#vol_copies"),
    tach_loading = $(".btn-loading"),
    lv_info_node_list = $("#lv_info_node_list"),
    input_vol_prealloc = $("#input_vol_prealloc");

$(".lun-add").on("click",function(){
    input_vol_name.val("");
    input_vol_size.val("");
    input_vol_copies.val(3);
    btn_lv_add.removeClass("hidden");
    tach_loading.addClass("hidden");
    lv_add_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});
$("tbody").delegate(".vol-info","click",function(){
    var _this = $(this);
    var vol_name = _this.attr("vol_name");
    $(".vol-infotab").attr("vol_name",vol_name);
    $(".vol-infotab").trigger("update.data");
    lv_info_node_list.empty();
    $.getJSON("data/data_node.php?func=node_list_filter&vol_info=true&vol_name="+vol_name+"&vol_type=detach",function(data){
        lv_info_node_list.html(data.data);
    });
    lv_info_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

$(".vol-infotab").on("update.data",function(){
    var _this = $(this),
        vol_name = _this.attr("vol_name");
    $.getJSON("data/data_lun.php?func=lv_info&vol_name="+vol_name,function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                $("#"+i).html(item);
            });
        }
    });
});
btn_lv_add.on("click",function(){
    var _this = $(this);
    var vol_name = input_vol_name.val();
    var vol_size = input_vol_size.val();
    var vol_copies = input_vol_copies.val();
    var vol_prealloc = input_vol_prealloc.val();
    var reg = new RegExp(input_vol_name.attr("reg"));
    if(!reg.test(vol_name)){
        input_vol_name.trigger("blur");
        return;
    }
    reg = new RegExp(input_vol_size.attr("reg"));
    if(!reg.test(vol_size)){
        input_vol_size.trigger("blur");
        return;
    }
    tach_loading.removeClass("hidden");
    _this.addClass("hidden");
    var param = {"func":"lv_add","vol_name":vol_name,"vol_size":vol_size,"vol_copies":vol_copies,"vol_prealloc":vol_prealloc};
    $.post("data/data_lun.php",param,function(data){
        if(data.result){
            alert("卷创建成功","success");
            lv_list.trigger("data.update");
        }else{
            alert(data.data?data.data:"卷创建失败");
        }
        lv_add_modal.modal("hide");
        tach_loading.addClass("hidden");
        _this.removeClass("hidden");
    },"json");
    return false;
});

lv_op_node_list.delegate("tr","click",function(){
    var _this = $(this);
    var checked = _this.find("input[type='checkbox']").prop("checked");
    _this.find("input[type='checkbox']").prop("checked",!checked);
});

check_all.on("change",function(){
    if(this.checked){
        lv_op_node_list.find("input[type='checkbox']").prop("checked",true);
    }else{
        lv_op_node_list.find("input[type='checkbox']").prop("checked",false);
    }
});

$("tbody").delegate(".vol-tach","click",function(){
    var _this = $(this);
    var vol_name = _this.attr("vol_name");
    var vol_type = _this.attr("vol_type");
    $(".btn-tach").attr("vol_name", vol_name);
    check_all.prop("checked",false);
    lv_op_node_list.empty();
    $.getJSON("data/data_node.php?func=node_list_filter&vol_name="+vol_name+"&vol_type="+vol_type,function(data){
        lv_op_node_list.html(data.data);
    });
    $(".btn-tach").addClass("hidden");
    tach_loading.addClass("hidden");
    if(vol_type=="attach"){
        btn_attach.removeClass("hidden");
    }else{
        btn_detach.removeClass("hidden");
    }
    lv_op_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

$(".btn-tach").on("click",function(){
    var _this = $(this);
    var vol_name = _this.attr("vol_name");
    var vol_type = _this.attr("vol_type");
    var param = {"func":"lv_tach","vol_type":vol_type,"vol_name":vol_name};
    var node_names = "";
    lv_op_node_list.find("input[type='checkbox']").each(function(i,item){
        if(item.checked){
            node_names += (node_names?",":"")+$(item).attr("node_name")
        }
    });
    if(!node_names){
        alert("请至少需要选择一个节点");
        return false;
    }
    tach_loading.removeClass("hidden");
    _this.addClass("hidden");
    param["node_names"] = node_names;
    $.post("data/data_lun.php",param,function(data){
        alert(data.data,"success");
        if(data.result){
            lv_list.trigger("data.update");
        }
        tach_loading.addClass("hidden");
        _this.removeClass("hidden");
        lv_op_modal.modal("hide");
    },"json");
    return false;
});

$("tbody").delegate(".vol-del","click",function(){
    var _this = $(this);
    var vol_name = _this.attr("vol_name");
    var param_confirm = {"title":"提示","content":"确认删除卷?",
        "sub_callback":function(){
            var param = {"func":"lv_del","vol_name":vol_name};
            var util_parent = _this.parents(".panel");
            var loading = util_parent.find(".region-loading");
            if(!loading || loading.length==0){
                util_parent.append("<div class='region-loading'><img src='img/loading.gif'></div>");
                loading = util_parent.find(".region-loading");
            }
            loading.css("width",util_parent.css("width"));
            loading.css("height",util_parent.css("height"));
            loading.removeClass("hidden");
            _this.addClass("hidden");
            $.post("data/data_lun.php",param,function(data){
                if(data.result){
                    alert("删除卷成功","success");
                    lv_list.trigger("data.update");
                }else{
                    alert(data.data?data.data:"删除卷失败");
                    _this.removeClass("hidden");
                }
                loading.addClass("hidden");
            },"json");
        }}
    make_confirm(param_confirm);
    return false;
});