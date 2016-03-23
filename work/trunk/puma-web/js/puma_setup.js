var setup_modal = $("#setup_modal"),
    btn_next = $("#btn_next"),
    btn_pro = $("#btn_pro"),
    btn_submit = $("#btn_submit"),
    ip_port = $("#ip_port"),
    btn_loading = $(".btn-loading"),
    ip_list = $("#ip_list"),
    input_div = $(".input-div"),
    result_div = $(".result-div"),
    result_content = $(".result-content");

$(".ip-add").on("click",function(){
    $.getJSON("data/data_option.php?func=ip_list_json",function(data){
        var htmls = "";
        if(data.result){
            $.each(data.data,function(i,item){
                htmls += (htmls?"\n":"")+item.ip+(item.port?(":"+item.port):""); 
            });
        }
        ip_port.val(htmls);
    });
    btn_loading.addClass("hidden");
    btn_pro.trigger("click");
    setup_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
});
btn_next.on("click",function(){
    if(!ip_port.val()){
        alert("服务IP不能为空");
        return;
    }
    var parsed = parse_ip();
    if(parsed.length==0){
        alert("没有解析出服务IP,请检查服务IP的输入信息");
        return;
    }
    var tip = "<strong>确认修改IP:</strong></br>";
    for(var i=0;i<parsed.length;i++){
        tip += (tip?"</br>":"")+"ip : "+parsed[i]["ip"]+(parsed[i]["port"]?("  port:"+parsed[i]["port"]):"");
    }
    result_content.html(tip+"</br>");
    input_div.addClass("hidden");
    result_div.removeClass("hidden");
});
btn_pro.on("click",function(){
    input_div.removeClass("hidden");
    result_div.addClass("hidden");
    result_content.html("");
});
btn_submit.on("click",function(){
    var _this = $(this);
    var parsed = parse_ip();
    if(parsed.length==0){
        alert("没有解析出服务IP,请检查服务IP的输入信息");
        return;
    }
    btn_loading.removeClass("hidden");
    _this.addClass("hidden");
    btn_pro.addClass("hidden");
    var param = {"func":"ip_save","data":parsed};
    $.post("data/data_option.php",param,function(data){
        if(data.result){
            alert("update config success","success");
            ip_list.trigger("data.update");
            setup_modal.modal("hide");
        }else{
            alert(data.error?data.error:"update config fail");
            btn_loading.addClass("hidden");
            _this.removeClass("hidden");
            btn_pro.removeClass("hidden");
        }
    },"json");

});
var parse_ip = function(){
    var ip_ports = ip_port.val();
    var ip_reg = /^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$/;
    var port_reg = /^([1-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/;
    
    var ip_portss = ip_ports.split("\n");
    var parsed = [];
    var dup = {};
    for(var i=0;i<ip_portss.length;i++){
        var idx = ip_portss[i].indexOf(":");
        if(idx>0){
            var ipport = ip_portss[i].split(":");
            var sip = ipport[0].replace(/ /g,"");
            var sport = ipport[1].replace(/ /g,"");
            if(ip_reg.test(sip) && port_reg.test(sport) && !dup[sip+":"+sport]){
                parsed.push({"ip":sip,"port":sport});
                dup[sip+":"+sport] = true;
            }
        }else{
            var sip = ip_portss[i];
            var sport = "";
            if(ip_reg.test(sip) && !dup[sip+":"+sport]){
                parsed.push({"ip":sip,"port":sport});
                dup[sip+":"+sport] = true;
            }
        }
    }
    return parsed;
};

$("table").delegate(".ip-del","click",function(){
    var _this = $(this);
    var ip = _this.attr("ip"),
        port = _this.attr("port");
    var param = {"func":"ip_del","ip":ip,"port":port};
    var loading = _this.parent().find(".row-loading");
    if(!loading || loading.length==0){
        _this.parent().append("<img class='row-loading' src='img/loading.gif'>");
        loading = _this.parent().find(".row-loading");
    }
    loading.removeClass("hidden");
    _this.addClass("hidden");
    $.post("data/data_option.php",param,function(data){
        if(data.result){
            alert("delete server ip <"+ip+":"+port+"> success");
            ip_list.trigger("data.update");
        }else{
            alert(data.error?data.error:"delete server ip <"+ip+":"+port+"> fail");
        }
        _this.removeClass("hidden");
        loading.addClass("hidden");
    },"json");
    return false;
});