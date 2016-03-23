var vg_info_modal = $("#vg_info"),
    vg_list = $("#vg_list");
var vg_opt_modal = $("#vg_opt"),
    vg_opt_title = $("#vg_opt_title"),
    btn_reduce = $("#btn_reduce"),
    btn_extend = $("#btn_extend"),
    opt_loading = $("#opt_loading");

$("table").delegate(".vg-drop","click",function(){
    var _this = $(this);
    var vg_name = _this.attr("vg_name");
    var param = {"func":"vg_drop","vg_name":vg_name};
    var param_confirm = {"title":"提示","content":"确定删除存储池 '"+vg_name+"'?",
        "sub_callback":function(){
            var loading = start_loading(_this);
            // loading.removeClass("hidden");
            $.post("data/data_vg.php",param,function(data){
                if(data.result){
                    alert("删除存储池成功","success");
                    vg_list.trigger("data.update");
                }else{
                    alert(data.error?data.error:"删除存储池失败");
                }
                loading.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});

$("table").delegate(".vg-info","click",function(){
    var _this = $(this),
        vg_name = _this.attr("vg_name");
    $(".vg-infotab").attr("vg_name",vg_name);
    $(".vg-infotab").trigger("update.data");
    // $(".vg-ref").trigger("data.filter",vg_name);
    vg_info_modal.modal({
      keyboard: false,
      backdrop: "static"
    });
    return false;
});

$(".vg-ref").on("data.filter",function(event,vg_name){
    var _this = $(this);
    _this.attr("data-url",_this.attr("data-url-origin")+"&vg_name="+vg_name);
    _this.removeClass("pause");
    _this.trigger("data.update");
});

vg_info_modal.find(".panel").on("start_loading",function(){
    var _this = $(this);
    var loading = $(".data_loading[forid='"+this.id+"']");
    var panel_heading = _this.find(".panel-heading");
    if(loading.length==0){
        panel_heading.append("<span class='navbar-right data_loading hidden' forid="+this.id+"><img src='img/loading.gif' style='height:18px'/></span>");
        loading = $(".data_loading[forid='"+this.id+"']");
    }
    loading.removeClass("hidden");
}).on("end_loading",function(){
    var loading = $(".data_loading[forid='"+this.id+"']");
    loading.addClass("hidden");
});
$(".vg-infotab").on("update.data",function(){
    var _this = $(this),
        vg_name = _this.attr("vg_name");
    vg_info_modal.find(".panel").trigger("start_loading");
    $.getJSON("data/data_vg.php?func=vg_info&vg_name="+vg_name,function(data){
        $.each(data.info,function(i,item){
            if($("#"+i)){
                $("#"+i).html(item);
            }
        });
        $("#lv_list").html(data.lv_list);
        $("#pv_list").html(data.pv_list);
        vg_info_modal.find(".panel").trigger("end_loading");
    });
});

$("table").delegate(".vg-opt","click",function(){
    var _this = $(this),
        vg_name = _this.attr("vg_name"),
        vg_opt_type = _this.attr("vg_opt_type");
    vg_opt_modal.attr("vg_name",vg_name);
    vg_opt_modal.attr("vg_opt_type",vg_opt_type);
    $(".btn-opt").addClass("hidden");
    if(vg_opt_type == "reduce"){
        btn_reduce.removeClass("hidden");
        vg_opt_title.html("缩小存储池 - "+vg_name);
        $(".panel-pv-list").removeClass("hidden");
        $(".panel-lun-list-op").addClass("hidden");
        $(".panel-pv-list .vg-opt-tbody").trigger("data.filter",[vg_name]);
    }else{
        btn_extend.removeClass("hidden");
        vg_opt_title.html("扩展存储池 - "+vg_name);
        $(".panel-pv-list").addClass("hidden");
        $(".panel-lun-list-op").removeClass("hidden");
        $(".panel-lun-list-op .vg-opt-tbody").trigger("data.filter",[vg_name]);
    }
    opt_loading.addClass("hidden");
    vg_opt_modal.modal({
      keyboard: false,
      backdrop: "static"
    });
    return false;
});
$(".vg-opt-tbody").on("data.filter",function(event,vg_name){
    var _this = $(this);
    _this.attr("data-url",_this.attr("data-url-origin")+"&vg_name="+vg_name);
    _this.removeClass("pause");
    _this.html("<td style='padding:10px' colspan='20'><div role='alert' class='alert alert-success col-sm-12'>数据加载中...</div></td>");
    _this.trigger("data.update");
});

$("body").delegate(".glyphicon","check",function(e,is_check){
    var _this = $(this);
    _this.removeClass("glyphicon-"+(is_check?"unchecked":"check"));
    _this.addClass("glyphicon-"+(!is_check?"unchecked":"check"));
});

$(".vg-opt-tbody").delegate("tr","click",function(){
    var _this = $(this);
    var check_obj = _this.find(".glyphicon");
    var cur_checked = check_obj.hasClass("glyphicon-check");
    var vg_opt_type = vg_opt_modal.attr("vg_opt_type");
    if(vg_opt_type=="reduce" && check_obj.attr("pv-size") != check_obj.attr("pv-free-size")){
        alert("只能选择未使用的物理卷");
        return;
    }
    _this.find(".glyphicon").trigger("check",!cur_checked);
});

$(".btn-opt").on("click",function(){
    var thisid = this.id;
    var param = {"func":"vg_opt"};
    var pref = "panel-lun-list-op";
    if(thisid == "btn_reduce"){
        param["opt"] = "reduce";
        pref = "panel-pv-list";
    }else{
        param["opt"] = "extend";
        pref = "panel-lun-list-op";
    }
    var pvs = [];
    $("."+pref+" .vg-opt-tbody").find(".glyphicon").each(function(i,item){
        var _this = $(this);
        if(_this.hasClass("glyphicon-check")){
            pvs.push(_this.attr("pv-name"));
        }
    });
    if(pvs.length==0){
        alert("请至少选择一个RAID或物理磁盘");
        return;
    }
    param["pvs"] = pvs;
    param["vg_name"] = vg_opt_modal.attr("vg_name");
    var param_confirm = {"title":"提示","content":"确定"+vg_opt_title.html()+"?",
        "sub_callback":function(){
            vg_opt_modal.modal("show");
            opt_loading.removeClass("hidden");
            $.ajax({
                type: "POST",
                url: "data/data_vg.php",
                // async: false,
                data: param,
                dataType: "json",
                success: function(data){
                    if(data.result){
                        alert(data.data,"success");
                        vg_opt_modal.modal("hide");
                        vg_list.trigger("data.update");
                    }else{
                        alert(data.data);
                    }
                    opt_loading.addClass("hidden");
                },
                error: function(XMLHttpRequest, textStatus, errorThrown){
                    alert("请求错误:"+textStatus);
                    console.info(textStatus);
                    console.info(errorThrown);
                    opt_loading.addClass("hidden");
                }
            });
    },"cancel_callback":function(){
        vg_opt_modal.modal("show");
    }};
    vg_opt_modal.modal("hide");
    make_confirm(param_confirm);
});