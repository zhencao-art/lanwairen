var lv_add_modal = $("#lv_add"),
    lv_add_error_msg = $("#lv_add_error_msg"),
    btn_lv_add = $("#lv_add_btn"),
    input_vol_name = $("#vol_name"),
    input_vol_vgname = $("#vol_vg"),
    input_vol_size = $("#vol_size"),
    input_vol_chunk = $("#vol_chunk"),
    lv_add_loadding = $("#lv_add_loadding");

$(".lv-add").on("click",function(){
    input_vol_name.val("");
    input_vol_size.val("");
    input_vol_chunk.val("");
    input_vol_vgname.trigger("data.update");
    btn_lv_add.removeClass("hidden");
    lv_add_loadding.addClass("hidden");
    lv_add_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});

input_vol_vgname.on("data.update",function(){
    input_vol_vgname.empty();
    $.getJSON("data/data_vg.php?func=list_vg_json",function(data){
        if(data.result){
            $.each(data.data,function(i,item){
                input_vol_vgname.append("<option value='"+item.vg_name+"'>"+item.vg_name+"</option>");
            });
        } 
    });
});

btn_lv_add.on("click",function(){
    var _this = $(this);
    var vol_name = input_vol_name.val();
    var vol_size = input_vol_size.val();
    var vol_chunk = input_vol_chunk.val();
    var vol_vgname = input_vol_vgname.val();
    var checked = check_input(lv_add_modal);
    if(!checked){
        return;
    }
    if(!vol_vgname){
        alert("请选择存储池!");
        return;
    }
    var param = {"func":"lv_add","vol_name":vol_name,"vol_size":vol_size,"vol_chunk":vol_chunk,"vol_vgname":vol_vgname};
    var param_confirm = {"title":"提示","content":"确定创建卷'"+vol_name+"'?",
        "sub_callback":function(){
            lv_add_loadding.removeClass("hidden");
            $.post("data/data_lv.php",param,function(data){
                if(data.result){
                    alert(data.msg,"success");
                    lv_add_modal.modal("hide");
                }else{
                    alert(data.msg);
                }
                lv_add_loadding.addClass("hidden");
                if($("#lv_list")){
                    $("#lv_list").trigger("data.update");
                }
            },"json");
    }};
    make_confirm(param_confirm);
    return false;
});