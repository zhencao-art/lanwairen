var raid_add_modal = $("#raid_add_modal"),
    raid_disk_list = $("#raid_disk_list"),
    raid_add_sub = $("#raid_add_sub"),
    modal_abled = $("#modal_abled"),
    raid_rname = $("#raid_rname"),
    raid_stripe = $("#raid_stripe"),
    raid_type = $("#raid_type"),
    chunk_div = $(".chunk-div");

$("body").delegate(".raid-add","click",function(){
    show_raid_add_modal();
});
raid_type.on("change",function(){
    if($(this).val()==1 || $(this).val()==6){
        chunk_div.addClass("hidden");
    }else{
        chunk_div.removeClass("hidden");
    }
});
var show_raid_add_modal = function(){
    raid_rname.val("");
    raid_type.val("0");
    chunk_div.removeClass("hidden");
    raid_disk_list.removeClass("pause");
    raid_disk_list.trigger("data.update");
    modal_abled.addClass("hidden");
    raid_add_modal.modal({
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

raid_disk_list.delegate("tr","click",function(){
    var _this = $(this);
    var cur_checked = _this.find(".glyphicon").hasClass("glyphicon-check");
    _this.find(".glyphicon").trigger("check",!cur_checked);
});
raid_add_sub.on("click",function(){
    var _this = $(this);
    var raid_stripe_val = raid_stripe.val();
    var raid_name_val = raid_rname.val();
    var raid_type_val = raid_type.val();
    var raid_disk = [];
    raid_disk_list.find(".glyphicon-check").each(function(i,item){
        var _this = $(this);
        raid_disk.push(_this.attr("disk-name"));
    });
    if(raid_type_val==6){
        if(raid_disk.length<=3){
            alert("请至少选择4个磁盘创建RAID6");
            return;
        }
    }else if(raid_disk.length<=1){
        alert("请至少选择2个磁盘创建RAID");
        return;
    }
    var checked = check_input(raid_add_modal);
    if(!checked){
        return;
    }
    var param_confirm = {"title":"提示","content":"确定创建RAID?",
        "sub_callback":function(){
            modal_abled.removeClass("hidden");
            _this.addClass("hidden");
            var param = {"func":"raid_create","raid_disk":raid_disk,"raid_type":raid_type_val,"raid_name":raid_name_val,"raid_stripe":raid_stripe_val};
            $.post("data/data_raid.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    raid_add_modal.modal("hide");
                    if($("#raid_list")){
                        $("#raid_list").trigger("data.update");
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