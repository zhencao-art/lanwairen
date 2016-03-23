var vg_add_modal = $("#vg_add_modal"),
    vg_disk_list = $("#vg_disk_list"),
    vg_raid_list = $("#vg_raid_list"),
    vg_add_sub = $("#vg_add_sub"),
    modal_abled = $("#modal_abled"),
    vg_name = $("#input_vg_name"),
    vg_stripe = $("#vg_stripe"),
    vg_type = $("#vg_type");

$("body").delegate(".vg-add","click",function(){
    show_vg_add_modal();
});
var show_vg_add_modal = function(){
    vg_name.val("");
    vg_disk_list.removeClass("pause");
    vg_disk_list.trigger("data.update");
    vg_raid_list.removeClass("pause");
    vg_raid_list.trigger("data.update");
    modal_abled.addClass("hidden");
    vg_add_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
}
$("body").delegate(".glyphicon","check",function(e,is_check){
    var _this = $(this);
    _this.removeClass("glyphicon-"+(is_check?"unchecked":"check"));
    _this.addClass("glyphicon-"+(!is_check?"unchecked":"check"));
});

vg_raid_list.delegate("tr","click",function(){
    var _this = $(this);
    var cur_checked = _this.find(".glyphicon").hasClass("glyphicon-check");
    _this.find(".glyphicon").trigger("check",!cur_checked);
});
vg_disk_list.delegate("tr","click",function(){
    var _this = $(this);
    var cur_checked = _this.find(".glyphicon").hasClass("glyphicon-check");
    _this.find(".glyphicon").trigger("check",!cur_checked);
});
vg_add_sub.on("click",function(){
    var _this = $(this);
    var vg_member = [];
    var vg_disk_val = "";
    var vg_raid_val = "";
    vg_raid_list.find(".glyphicon-check").each(function(i,item){
        var _this = $(this);
        vg_member.push(_this.attr("raid-name"));
        vg_raid_val += (vg_raid_val?",":"") + _this.attr("raid-name");
    });
    vg_disk_list.find(".glyphicon-check").each(function(i,item){
        var _this = $(this);
        vg_member.push(_this.attr("disk-name"));
        vg_disk_val += (vg_disk_val?",":"") + _this.attr("disk-name");
    });
    if(vg_member.length==0){
        alert("请至少选择一个RAID或磁盘创建存储池");
        return;
    }
    var checked = check_input(vg_add_modal);
    if(!checked){
        return;
    }
    var tip = "确定使用:<br>";
    if(vg_raid_val){
        tip += "<br>RAID: "+vg_raid_val;
    }
    if(vg_disk_val){
        tip += "<br>物理磁盘: "+vg_disk_val;
    }
    tip += "<br><br>创建存储池?";
    var vg_name_val = vg_name.val();
    var param_confirm = {"title":"提示","content":tip,
        "sub_callback":function(){
            modal_abled.removeClass("hidden");
            _this.addClass("hidden");
            var param = {"func":"vg_create","vg_member":vg_member,"vg_name":vg_name_val};
            $.post("data/data_vg.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    vg_add_modal.modal("hide");
                    if($("#vg_list")){
                        $("#vg_list").trigger("data.update");
                    }
                }else{
                    alert(data.msg);
                }
                _this.removeClass("hidden");
                modal_abled.addClass("hidden");
            },"json");
    }};
    make_confirm(param_confirm);
});