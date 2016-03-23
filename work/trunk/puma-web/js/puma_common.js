$(".auto-load").on("data.update",function(e,flag){
    var _this = $(this);
    var url = _this.attr("data-url");
    if(flag && flag=="auto" && !_this.hasClass("auto-refresh")){
        return;
    }
    if(_this.attr("call_back")){
        _this.trigger(_this.attr("call_back"));
    }
    var refresh_btn = _this.find(".refresh_table");
    var loading = $(".data_loading[forid='"+this.id+"']");
    if(loading.length==0){
        _this.find(".panel-heading").append("<span class='navbar-right data_loading hidden' forid="+this.id+"><img src='img/loading.gif' style='height:18px'/></span>");
        loading = $(".data_loading[forid='"+this.id+"']");
    }
    loading.removeClass("hidden");
    if(refresh_btn){
        refresh_btn.addClass("hidden");
    }
    $.getJSON(url,function(data){
        loading.addClass("hidden");
        if(refresh_btn){
            refresh_btn.removeClass("hidden");
        }
        if(data.result){
            $.each(data.data,function(i,item){
                $("#"+i).html(item);
            });
            if(_this.attr("callback")){
                _this.trigger(_this.attr("callback"),data.data);
            }
        }
    });
});

$(".auto-load-table").on("data.update",function(e,flag){
    var _this = $(this);
    var url = _this.attr("data-url");
    if(flag && flag=="auto" && !_this.hasClass("auto-refresh")){
        return;
    }
    var loading = $(".data_loading[forid='"+this.id+"']");
    var panel_heading = _this.parent().siblings(".panel-heading");
    if(panel_heading.length==0){
        panel_heading = _this.parent().parent().siblings(".panel-heading");
    }
    if(_this.attr("load-type")=="tab"){
        panel_heading = _this.parent().parent().siblings(".nav-tabs");
        if(panel_heading.length==0){
            panel_heading = _this.parent().parent().parent().siblings(".nav-tabs");
        }
    }
    if(loading.length==0){
        panel_heading.append("<span class='navbar-right data_loading hidden' forid="+this.id+"><img src='img/loading.gif' style='height:18px'/></span>");
        loading = $(".data_loading[forid='"+this.id+"']");
    }
    if(_this.hasClass("pause")){
        return;
    }
    loading.removeClass("hidden");
    $.getJSON(url,function(data){
        // if(data.result){
            _this.html(data.data);
        // }else{
            // _this.trigger("data.empty");
        // }
        _this.attr("page_count",data.page_count);
        _this.trigger("update.tool");
        loading.addClass("hidden");
        if(_this.attr("call_back")){
            _this.trigger(_this.attr("call_back"),data);
        }
    });
}).on("data.empty",function(){
    var _this = $(this);
    _this.html("<tr><td colspan='20' style='padding:10px'><div class=\"alert alert-danger col-sm-12\" role=\"alert\"><strong>提示:</strong> 没有数据</div></td></tr>");
});

$(".refresh_table").on("click",function(){
    var _this = $(this);
    var target = $("#"+_this.attr("ref-obj"));
    if(target.find("tbody").length!=0){
        target.find("tbody").trigger("data.update");
    }else{
        target.trigger("data.update");
    }
    return false;
});
function load_data(flag){
    $(".auto-load,.auto-load-table").trigger("data.update",flag==1?"auto":"");
    $(".auto-refresh").trigger("data.update",flag==1?"auto":"");
}
function auto_refresh(flag){
    load_data(flag);
    setTimeout("auto_refresh(1)",60000);
}
auto_refresh(0);
$(".notify_menu_downup").click(function(){
    var _this = $(this);
    if(_this.hasClass("glyphicon-chevron-up")){
        _this.parent().parent().children("ul").addClass("hide");
        _this.removeClass("glyphicon-chevron-up");
        _this.addClass("glyphicon-chevron-down");
    }else{
        _this.parent().parent().children("ul").removeClass("hide");
        _this.removeClass("glyphicon-chevron-down");
        _this.addClass("glyphicon-chevron-up");
    }
    return false;
});

$(".main_menu_to_show").click(function(){
    $(".sidebar").addClass("hide");
    $(".main_menu_to_hide").removeClass("hide");
    $(".main_menu_to_show").addClass("hide");
    $(".main").removeClass("col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2");
    $(".main").addClass("col-sm-12");
    $(window).resize();
    return false;
});
$(".main_menu_to_hide").click(function(){
    $(".sidebar").removeClass("hide");
    $(".main_menu_to_hide").addClass("hide");
    $(".main_menu_to_show").removeClass("hide");
    $(".main").removeClass("col-sm-12");
    $(".main").addClass("col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2");
    $(window).resize();
    return false;
});
    
$("body").delegate("input","blur",function(event,flag,msg){
    var _this = $(this);
    var thisid = this.id;
    var siblings = _this.parent().siblings("[for='"+thisid+"']");
    var reg = _this.attr("reg");
    siblings = siblings?siblings:_this.parent().parent().siblings("[for='"+thisid+"']");
    if(_this.val() || flag=="clear"){
        // _this.parent().removeClass("has-error");
        // siblings.removeClass("has-error-custom");
        // siblings.html(siblings.attr("msg"));
        JT_close(thisid);
    }else if(_this.hasClass("requirement")){
        // _this.parent().addClass("has-error");
        // siblings.addClass("has-error-custom");
        // siblings.html(siblings.attr("msg")+"不能为空");
        JT_close(thisid);
        JT_show(thisid,"提示",siblings.attr("msg")+"不能为空");
    }
    if(msg){
        // _this.parent().addClass("has-error");
        // siblings.addClass("has-error-custom");
        // siblings.html(msg);
        JT_close(thisid);
        JT_show(thisid,"提示",msg);
    }
    if(_this.val() && reg){
        if(reg){
            reg = new RegExp(reg);
            if(!reg.test(_this.val())){
                // _this.parent().addClass("has-error");
                // siblings.addClass("has-error-custom");
                // siblings.html(siblings.attr("msg")+_this.attr("reg_tip"));
                JT_close(thisid);
                JT_show(thisid,"提示",siblings.attr("msg")+_this.attr("reg_tip"));
                return;
            }
        }
    }
});

$("#home_logout").on("click",function(event){
    logout();
});
function logout(){
    $.ajax({
        url: "data/data_user.php",
        type: 'post',
        data: {"func":"logout"},
        dataType: "json",
        complete: function (XMLHttpRequest, textStatus) {
            location.href = "login.php";
        },
        success: function (data) {
        }
    });
}
$("#modify_pass").on("click",function(event){
    $("#user_pass_modal").modal("show");
});

$("#user_pass_btn_submit").on("click",function(event){
    var pass_old = $("#user_pass_input_old"),
        pass_new = $("#user_pass_input_new"),
        pass_com = $("#user_pass_input_com");
    if(!pass_old.val()){
        pass_old.trigger("blur");
        pass_old.focus();
        return;
    }
    if(!pass_new.val()){
        pass_new.trigger("blur");
        pass_new.focus();
        return;
    }
    if(!pass_com.val()){
        pass_com.trigger("blur");
        pass_com.focus();
        return;
    }
    if(pass_new.val()!=pass_com.val()){
        alert("新密码与确认密码不一致");
        return;
    }
    if(pass_new.val().length<6){
        alert("新密码长度必须大于6位");
        return;
    }
    $.ajax({
        url: "data/data_user.php",
        type: 'post',
        data: {"func":"update_pass","pass_old":pass_old.val(),"pass_new":pass_new.val()},
        dataType: "json",
        complete: function (XMLHttpRequest, textStatus) {
        },
        success: function (data) {
            if(data.result){
                alert("修改密码成功","success");
                logout();
            }else{
                alert(data.error?data.error:"修改密码失败");
            }
        }
    });
});
$(".theme-change").on("click",function(){
    var theme = $(this).attr("theme-name");
    var param = {"func":"theme","theme":theme};
    $.post("data/data_user.php",param,function(data){
        if(data.result){
            document.location.reload();
        }
    },"json");
});
$(".besort").on("click",function(){
    var _this = $(this);
    var sorted = _this.attr("sorting"),
        col_idx = _this.index(),
        sort_icon = _this.parent().find(".sort");
    _this.parent().find("td").attr("sorting","");
    if(!sorted || sorted=="desc"){
        sorted = "asc";
    }else{
        sorted = "desc";
    }
    var need_sort_list = _this.parent().parent().parent().find("tbody");
    need_sort_list.find(".detail-tabletr").remove();
    var disk_list_tr = need_sort_list.find("tr");
    var sort_list = [];
    $.each(disk_list_tr,function(idx,tr){
        if(idx==0){
            sort_list.push(tr);
            return;
        } 
        var td = $(tr).find("td").get(col_idx);
        var txt = $(td).text();
        var insert = false;
        for(var idxx=0;idxx<sort_list.length;idxx++){
            var newtr = sort_list[idxx];
            var newtd = $(newtr).find("td").get(col_idx);
            if(sorted == "asc" && txt < $(newtd).text()){
                sort_list.splice(idxx, 0, tr);  
                insert = true;
                break;
            }else if(sorted == "desc" && txt > $(newtd).text()){
                sort_list.splice(idxx, 0, tr);  
                insert = true;
                break;
            }
        }
        if(!insert){
            sort_list.push(tr);
        }
    });
    if(sort_icon){
        sort_icon.remove();
    }
    if(sorted=="desc"){
        // sort_list.reverse();
        _this.append("<span class='glyphicon glyphicon-triangle-bottom sort'></span>");
    }else{
        _this.append("<span class='glyphicon glyphicon-triangle-top sort'></span>");
    }
    need_sort_list.html(sort_list);
    
    _this.attr("sorting",sorted);
});

var start_loading = function(target){
    var util_parent = target.parents(".panel");
    var loading = util_parent.find(".region-loading");
    if(!loading || loading.length==0){
        util_parent.append("<div class='region-loading'><img src='img/loading.gif'></div>");
        loading = util_parent.find(".region-loading");
    }
    loading.css("width",util_parent.css("width"));
    loading.css("height",util_parent.css("height"));
    loading.removeClass("hidden");
    return loading;
}
$(window).on("resize",function(){
    if(this.innerWidth<=767){
        $(".window-mini-view").addClass("hidden");
    }else{
        $(".window-mini-view").removeClass("hidden");
    }
});
$(window).resize();
var alert = function(msg,type){
    if(!type){
        type = 'danger';
    }
    if($(".alert-cust-modal")){
        $('#alert_cust').alert('close');
    }
    $("body").append('<div class="alert-cust transparent_class"></div><div class="alert-modal alert-cust-modal"><div class="alert alert-'+type+' alert-dismissible" role="alert" id="alert_cust"> \
    <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
    <strong>提示</strong><div class="alert-content">'+ msg +'</div> </div></div>');
    
    $(".alert-cust-modal").on("click",function(){
        $('#alert_cust').alert('close');
    });
    $('#alert_cust').on('closed.bs.alert', function () {
        $(".alert-cust").remove();
        $(".alert-modal").remove();
    });
}

var make_confirm = function(param){
    var title = param && param.title ? param.title:"";
    var content = param && param.content ? param.content:"";
    var sub_callback = param && param.sub_callback ? param.sub_callback:function(){};
    var cancel_callback = param && param.cancel_callback ? param.cancel_callback:function(){};
    var sub_title = param && param.sub_title ? param.sub_title:"确定";
    var cancel_title = param && param.cancel_title ? param.cancel_title:"取消";
    var rand = Math.round(Math.random()*10000);
    
    $("body").append('\
    <div class="modal fade" id="cust_confirm_'+rand+'"> \
      <div class="modal-dialog"> \
        <div class="modal-content"> \
          <div class="modal-header"> \
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
            <h4 class="modal-title">'+title+'</h4> \
          </div> \
          <div class="modal-body"> \
            <p>'+content+'</p> \
          </div> \
          <div class="modal-footer"> \
            <button type="button" class="btn btn-primary" id="cust_confirm_submit'+rand+'">'+sub_title+'</button> \
            <button type="button" class="btn btn-default" id="cust_confirm_cancel'+rand+'">'+cancel_title+'</button> \
          </div> \
        </div> \
      </div> \
    </div>');
    
    $("#cust_confirm_"+rand).modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    $("#cust_confirm_submit"+rand).on("click",function(){
        $("#cust_confirm_"+rand).modal("hide");
        // $("#cust_confirm_"+rand).remove();
        // $(".modal-backdrop").last().remove();
        sub_callback();
    });
    $("#cust_confirm_cancel"+rand).on("click",function(){
        $("#cust_confirm_"+rand).modal("hide");
        // $("#cust_confirm_"+rand).remove();
        // $(".modal-backdrop").last().remove();
        cancel_callback();
    });
    $("#cust_confirm_"+rand).on('hidden.bs.modal', function (e) {
        // $("#cust_confirm_"+rand).remove();
    });
}

function check_input(target){
    var checked = true;
    target.find("input").each(function(i,item){
        var _this = $(item);
        if(_this.hasClass("hidden")){
            return;
        }
        var reg = _this.attr("reg");
        if((_this.hasClass("requirement") || _this.val()) && reg){
            var regExp = new RegExp(reg);
            if(!regExp.test(_this.val())){
                checked = false;
                _this.trigger("blur");
            }
        }
    });
    return checked;
}
$(".modal").on('hide.bs.modal', function (e) { //hidden
    $(this).find("input").each(function(){
        JT_close(this.id);        
    });
});
$(".menu-tree-father").on("click",function(){
    var _this = $(this).parent();
    _this.find(".accordion_list_child").toggleClass("hidden");
    if(_this.find(".accordion_list_child").hasClass("hidden")){
        _this.find(".menu-tree-father-flag").removeClass("glyphicon-chevron-down");
        _this.find(".menu-tree-father-flag").addClass("glyphicon-chevron-right");
    }else{
        _this.find(".menu-tree-father-flag").removeClass("glyphicon-chevron-right");
        _this.find(".menu-tree-father-flag").addClass("glyphicon-chevron-down");
    }
    return false;
});

function delay_func(func,sec){
    if(!sec){
        sec = 1500;
    }
    setTimeout(func,sec);
}