
var dt_set_modal = $("#dt_set_modal"),
    dt_set_timezone = $("#dt_set_timezone"),
    dt_set_syc_srouce = $("#dt_set_syc_srouce"),
    dt_set_host_srouce = $("#dt_set_host_srouce"),
    dt_set_syc_srv = $("#dt_set_syc_srv"),
    dt_set_syc_dt = $("#dt_set_syc_dt"),
    dt_set_syc_main = $("#dt_set_syc_main"),
    dt_set_btn = $("#dt_set_btn"),
    dt_info_dt = $("#dt_info_dt"),
    dt_set_modal_loadding = $("#dt_set_modal_loadding"),
    zone_set_modal = $("#zone_set_modal"),
    zone_set_timezone = $("#zone_set_timezone"),
    zone_set_btn = $("#zone_set_btn"),
    zone_set_modal_loadding = $("#zone_set_modal_loadding");

$(".dt-info-edit").on("click",function(){
    load_tz($("#dt_set_tz").html());
    // dt_set_timezone.val($("#dt_set_tz").html());
    dt_set_syc_srv.val($("#dt_set_srv").html());
    $("input[type='radio']").prop("checked",false);
    $("#dt_set_is_syc_"+dt_set_syc_srouce.html()).prop("checked",true);
    dt_set_syc_dt.val(dt_info_dt.html());
    load_host();
    $("#dt_set_is_syc_"+dt_set_syc_srouce.html()).trigger("change");
    dt_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

$(".timezone-edit").on("click",function(){
    load_tz($("#dt_set_tz").html());
    zone_set_modal.modal({
        keyboard: false,
        backdrop: "static",
        show: true
    });
    return false;
});

function load_host(){
    var ntp_host = dt_set_host_srouce.html();
    if(!dt_set_syc_main.html()){
        $.getJSON("data/data_map.php?func=host_list",function(data){
            $.each(data.data,function(i,item){
                dt_set_syc_main.append("<option value='"+item.hb+"' "+(ntp_host==item.host_name?"selected":"")+">"+item.host_name+"</option>");
            });
        });
    }
}
function load_tz(ctz){
    if(!dt_set_timezone.html()){
        dt_set_timezone.append("<option value=''></option>");
        zone_set_timezone.append("<option value=''></option>");
        $.getJSON("data/data_dt.php?func=zt",function(data){
            $.each(data.data,function(i,item){
                var tz = item.tz.replace(/\s/g,"");
                dt_set_timezone.append("<option value='"+tz+"'>"+tz+"</option>");
                zone_set_timezone.append("<option value='"+tz+"'>"+tz+"</option>");
            });
            if(ctz){
                dt_set_timezone.val(ctz);
                zone_set_timezone.val(ctz);
            }
        });
    }else{
        if(ctz){
            dt_set_timezone.val(ctz);
            zone_set_timezone.val(ctz);
        }
    }
}

dt_set_btn.on("click",function(){
    var checked = check_input(dt_set_modal);
    if(!checked){
        return;
    }
    var timezone = dt_set_timezone.val();
    var srv = dt_set_syc_srv.val();
    var dt = dt_set_syc_dt.val();
    var main = dt_set_syc_main.val();
    var is_syc = $("#dt_set_is_syc_1").prop("checked")?1:0;
    if(is_syc===1 && !main){
        alert("启用同步时,主节点不能为空");
        return;
    }
    if(is_syc===1 && !srv){
        dt_set_syc_srv.trigger("blur",["","启用同步时,同步服务器不能为空"]);
        return;
    }
    if(is_syc===0 && !dt){
        dt_set_syc_dt.trigger("blur",["","不启用同步时,日期时间不能为空"]);
        return;
    }
    dt_set_modal.modal("hide");
    var param = {"func":"dt_set","is_syc":is_syc,"timezone":timezone,"srv":srv,"main":main,"dt":dt};
    var param_confirm = {"title":"提示","content":"确认设置时间同步?",
        "sub_callback":function(){
            dt_set_modal.modal("show");
            dt_set_modal_loadding.removeClass("hidden");
            $.post("data/data_dt.php",param,function(data){
                if(data.result){
                    alert("设置时间同步成功","success");
                    dt_set_modal.modal("hide");
                }else{
                    alert(data.error?data.error:"设置时间同步失败");
                }
                $(".refresh_table").trigger("click");
                dt_set_modal_loadding.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            dt_set_modal.modal("show");
            dt_set_modal_loadding.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});

zone_set_btn.on("click",function(){
    var timezone = zone_set_timezone.val();
    zone_set_modal.modal("hide");
    var param = {"func":"zone_set","timezone":timezone};
    var param_confirm = {"title":"提示","content":"确认设置时区为'"+timezone+"'?",
        "sub_callback":function(){
            zone_set_modal.modal("show");
            zone_set_modal_loadding.removeClass("hidden");
            $.post("data/data_dt.php",param,function(data){
                if(data.result){
                    alert("设置时区成功","success");
                    zone_set_modal.modal("hide");
                }else{
                    alert(data.error?data.error:"设置时区失败");
                }
                $(".refresh_table").trigger("click");
                zone_set_modal_loadding.addClass("hidden");
            },"json");
        },
        "cancel_callback":function(){
            zone_set_modal.modal("show");
            zone_set_modal_loadding.addClass("hidden");
        }};
    make_confirm(param_confirm);
    return false;
});

function auto_update(){
    $("#dt_info").trigger("data.update");
    setTimeout("auto_update()",5000);
}
auto_update();

$("input[name='dt_set_is_syc']").on("change",function(){
    $(".syc-type").addClass("hidden");
    if(this.checked){
        if(this.value==0){
            $(".time-group").removeClass("hidden");
        }else{
            $(".syc-group").removeClass("hidden");
        }
    }
});
$("#dt_set_syc_dt").datetimepicker();
// $("#dt_set_syc_dt").datetimepicker({
        // format: "yyyy-mm-dd hh:ii:ss",//设置时间格式，默认值: 'mm/dd/yyyy'
        // initialDate : "2015-02-14 10:00",//初始化的时间
        // weekStart : 0, //一周从哪一天开始。0（星期日）到6（星期六）,默认值0
        // startDate : "2013-02-14 10:00",//可以被选择的最早时间
        // endDate : "2016-02-14 10:00",//可以被选择的最晚时间
        // daysOfWeekDisabled : "0,6",//禁止选择一星期中的某些天，例子中这样是禁止选择周六和周日
        // autoclose : true,//当选择一个日期之后是否立即关闭此日期时间选择器
        // startView : 2,//点开插件后显示的界面。0、小时1、天2、月3、年4、十年，默认值2
        // minView : 0,//插件可以精确到那个时间，比如1的话就只能选择到天，不能选择小时了
        // maxView: 4,//同理
        // todayBtn : true,//是否在底部显示“今天”按钮
        // todayHighlight : true,//是否高亮当前时间
        // keyboardNavigation : true,//是否允许键盘选择时间
        // language : 'zh-CN',//选择语言，前提是该语言已导入
        // forceParse : true,//当选择器关闭的时候，是否强制解析输入框中的值。也就是说，当用户在输入框中输入了不正确的日期，选择器将会尽量解析输入的值，并将解析后的正确值按照给定的格式format设置到输入框中
        // minuteStep : 5,//分钟的间隔
        // pickerPosition : "bottom-right",//显示的位置，还支持bottom-left
        // viewSelect : 0,//默认和minView相同
        // showMeridian : true//是否加上网格
// });

// var time_zones = [
// 'Africa/Abidjan                       '
// ,'Africa/Accra                         '
// ,'Africa/Addis_Ababa                   '
// ,'Africa/Algiers                       '
// ,'Africa/Asmera                        '
// ,'Africa/Bamako                        '
// ,'Africa/Bangui                        '
// ,'Africa/Banjul                        '
// ,'Africa/Bissau                        '
// ,'Africa/Blantyre                      '
// ,'Africa/Brazzaville                   '
// ,'Africa/Bujumbura                     '
// ,'Africa/Cairo                         '
// ,'Africa/Casablanca                    '
// ,'Africa/Ceuta                         '
// ,'Africa/Conakry                       '
// ,'Africa/Dakar                         '
// ,'Africa/Dar_es_Salaam                 '
// ,'Africa/Djibouti                      '
// ,'Africa/Douala                        '
// ,'Africa/El_Aaiun                      '
// ,'Africa/Freetown                      '
// ,'Africa/Gaborone                      '
// ,'Africa/Harare                        '
// ,'Africa/Johannesburg                  '
// ,'Africa/Kampala                       '
// ,'Africa/Khartoum                      '
// ,'Africa/Kigali                        '
// ,'Africa/Kinshasa                      '
// ,'Africa/Lagos                         '
// ,'Africa/Libreville                    '
// ,'Africa/Lome                          '
// ,'Africa/Luanda                        '
// ,'Africa/Lubumbashi                    '
// ,'Africa/Lusaka                        '
// ,'Africa/Malabo                        '
// ,'Africa/Maputo                        '
// ,'Africa/Maseru                        '
// ,'Africa/Mbabane                       '
// ,'Africa/Mogadishu                     '
// ,'Africa/Monrovia                      '
// ,'Africa/Nairobi                       '
// ,'Africa/Ndjamena                      '
// ,'Africa/Niamey                        '
// ,'Africa/Nouakchott                    '
// ,'Africa/Ouagadougou                   '
// ,'Africa/Porto-Novo                    '
// ,'Africa/Sao_Tome                      '
// ,'Africa/Tripoli                       '
// ,'Africa/Tunis                         '
// ,'Africa/Windhoek                      '
// ,'America/Anchorage                    '
// ,'America/Anguilla                     '
// ,'America/Antigua                      '
// ,'America/Araguaina                    '
// ,'America/Argentina/Buenos_Aires       '
// ,'America/Aruba                        '
// ,'America/Asuncion                     '
// ,'America/Bahia                        '
// ,'America/Barbados                     '
// ,'America/Belem                        '
// ,'America/Belize                       '
// ,'America/Boa_Vista                    '
// ,'America/Bogota                       '
// ,'America/Campo_Grande                 '
// ,'America/Caracas                      '
// ,'America/Cayenne                      '
// ,'America/Cayman                       '
// ,'America/Chicago                      '
// ,'America/Costa_Rica                   '
// ,'America/Cuiaba                       '
// ,'America/Curacao                      '
// ,'America/Danmarkshavn                 '
// ,'America/Dawson_Creek                 '
// ,'America/Denver                       '
// ,'America/Dominica                     '
// ,'America/Edmonton                     '
// ,'America/El_Salvador                  '
// ,'America/Fortaleza                    '
// ,'America/Godthab                      '
// ,'America/Grand_Turk                   '
// ,'America/Grenada                      '
// ,'America/Guadeloupe                   '
// ,'America/Guatemala                    '
// ,'America/Guayaquil                    '
// ,'America/Guyana                       '
// ,'America/Halifax                      '
// ,'America/Havana                       '
// ,'America/Hermosillo                   '
// ,'America/Iqaluit                      '
// ,'America/Jamaica                      '
// ,'America/La_Paz                       '
// ,'America/Lima                         '
// ,'America/Los_Angeles                  '
// ,'America/Maceio                       '
// ,'America/Managua                      '
// ,'America/Manaus                       '
// ,'America/Martinique                   '
// ,'America/Mazatlan                     '
// ,'America/Mexico_City                  '
// ,'America/Miquelon                     '
// ,'America/Montevideo                   '
// ,'America/Montreal                     '
// ,'America/Montserrat                   '
// ,'America/Nassau                       '
// ,'America/New_York                     '
// ,'America/Noronha                      '
// ,'America/Panama                       '
// ,'America/Paramaribo                   '
// ,'America/Phoenix                      '
// ,'America/Port-au-Prince               '
// ,'America/Port_of_Spain                '
// ,'America/Porto_Velho                  '
// ,'America/Puerto_Rico                  '
// ,'America/Recife                       '
// ,'America/Regina                       '
// ,'America/Rio_Branco                   '
// ,'America/Santiago                     '
// ,'America/Santo_Domingo                '
// ,'America/Sao_Paulo                    '
// ,'America/Scoresbysund                 '
// ,'America/St_Johns                     '
// ,'America/St_Kitts                     '
// ,'America/St_Lucia                     '
// ,'America/St_Thomas                    '
// ,'America/St_Vincent                   '
// ,'America/Tegucigalpa                  '
// ,'America/Thule                        '
// ,'America/Tijuana                      '
// ,'America/Toronto                      '
// ,'America/Tortola                      '
// ,'America/Vancouver                    '
// ,'America/Whitehorse                   '
// ,'America/Winnipeg                     '
// ,'America/Yellowknife                  '
// ,'Antarctica/Casey                     '
// ,'Antarctica/Davis                     '
// ,'Antarctica/DumontDUrville            '
// ,'Antarctica/Mawson                    '
// ,'Antarctica/McMurdo                   '
// ,'Antarctica/Palmer                    '
// ,'Antarctica/Rothera                   '
// ,'Antarctica/South_Pole                '
// ,'Antarctica/Syowa                     '
// ,'Antarctica/Vostok                    '
// ,'Asia/Aden                            '
// ,'Asia/Almaty                          '
// ,'Asia/Amman                           '
// ,'Asia/Aqtau                           '
// ,'Asia/Aqtobe                          '
// ,'Asia/Ashgabat                        '
// ,'Asia/Baghdad                         '
// ,'Asia/Bahrain                         '
// ,'Asia/Baku                            '
// ,'Asia/Bangkok                         '
// ,'Asia/Beirut                          '
// ,'Asia/Bishkek                         '
// ,'Asia/Brunei                          '
// ,'Asia/Calcutta                        '
// ,'Asia/Choibalsan                      '
// ,'Asia/Colombo                         '
// ,'Asia/Damascus                        '
// ,'Asia/Dhaka                           '
// ,'Asia/Dili                            '
// ,'Asia/Dubai                           '
// ,'Asia/Dushanbe                        '
// ,'Asia/Gaza                            '
// ,'Asia/Hong_Kong                       '
// ,'Asia/Hovd                            '
// ,'Asia/Irkutsk                         '
// ,'Asia/Jakarta                         '
// ,'Asia/Jayapura                        '
// ,'Asia/Jerusalem                       '
// ,'Asia/Kabul                           '
// ,'Asia/Kamchatka                       '
// ,'Asia/Karachi                         '
// ,'Asia/Katmandu                        '
// ,'Asia/Krasnoyarsk                     '
// ,'Asia/Kuala_Lumpur                    '
// ,'Asia/Kuwait                          '
// ,'Asia/Macau                           '
// ,'Asia/Magadan                         '
// ,'Asia/Makassar                        '
// ,'Asia/Manila                          '
// ,'Asia/Muscat                          '
// ,'Asia/Nicosia                         '
// ,'Asia/Omsk                            '
// ,'Asia/Phnom_Penh                      '
// ,'Asia/Pyongyang                       '
// ,'Asia/Qatar                           '
// ,'Asia/Rangoon                         '
// ,'Asia/Riyadh                          '
// ,'Asia/Saigon                          '
// ,'Asia/Seoul                           '
// ,'Asia/Shanghai                        '
// ,'Asia/Singapore                       '
// ,'Asia/Taipei                          '
// ,'Asia/Tashkent                        '
// ,'Asia/Tbilisi                         '
// ,'Asia/Tehran                          '
// ,'Asia/Thimphu                         '
// ,'Asia/Tokyo                           '
// ,'Asia/Ulaanbaatar                     '
// ,'Asia/Vientiane                       '
// ,'Asia/Vladivostok                     '
// ,'Asia/Yakutsk                         '
// ,'Asia/Yekaterinburg                   '
// ,'Asia/Yerevan                         '
// ,'Atlantic/Azores                      '
// ,'Atlantic/Bermuda                     '
// ,'Atlantic/Canary                      '
// ,'Atlantic/Cape_Verde                  '
// ,'Atlantic/Faeroe                      '
// ,'Atlantic/Reykjavik                   '
// ,'Atlantic/South_Georgia               '
// ,'Atlantic/St_Helena                   '
// ,'Atlantic/Stanley                     '
// ,'Australia/Adelaide                   '
// ,'Australia/Brisbane                   '
// ,'Australia/Darwin                     '
// ,'Australia/Eucla                      '
// ,'Australia/Hobart                     '
// ,'Australia/Perth                      '
// ,'Australia/Sydney                     '
// ,'Etc/GMT                              '
// ,'Europe/Amsterdam                     '
// ,'Europe/Andorra                       '
// ,'Europe/Athens                        '
// ,'Europe/Belgrade                      '
// ,'Europe/Berlin                        '
// ,'Europe/Brussels                      '
// ,'Europe/Bucharest                     '
// ,'Europe/Budapest                      '
// ,'Europe/Chisinau                      '
// ,'Europe/Copenhagen                    '
// ,'Europe/Dublin                        '
// ,'Europe/Gibraltar                     '
// ,'Europe/Helsinki                      '
// ,'Europe/Istanbul                      '
// ,'Europe/Kaliningrad                   '
// ,'Europe/Kiev                          '
// ,'Europe/Lisbon                        '
// ,'Europe/London                        '
// ,'Europe/Luxembourg                    '
// ,'Europe/Madrid                        '
// ,'Europe/Malta                         '
// ,'Europe/Minsk                         '
// ,'Europe/Monaco                        '
// ,'Europe/Moscow                        '
// ,'Europe/Oslo                          '
// ,'Europe/Paris                         '
// ,'Europe/Prague                        '
// ,'Europe/Riga                          '
// ,'Europe/Rome                          '
// ,'Europe/Samara                        '
// ,'Europe/Sofia                         '
// ,'Europe/Stockholm                     '
// ,'Europe/Tallinn                       '
// ,'Europe/Tirane                        '
// ,'Europe/Vaduz                         '
// ,'Europe/Vienna                        '
// ,'Europe/Vilnius                       '
// ,'Europe/Warsaw                        '
// ,'Europe/Zurich                        '
// ,'Indian/Antananarivo                  '
// ,'Indian/Chagos                        '
// ,'Indian/Christmas                     '
// ,'Indian/Cocos                         '
// ,'Indian/Comoro                        '
// ,'Indian/Kerguelen                     '
// ,'Indian/Mahe                          '
// ,'Indian/Maldives                      '
// ,'Indian/Mauritius                     '
// ,'Indian/Mayotte                       '
// ,'Indian/Reunion                       '
// ,'Pacific/Apia                         '
// ,'Pacific/Auckland                     '
// ,'Pacific/Chatham                      '
// ,'Pacific/Easter                       '
// ,'Pacific/Efate                        '
// ,'Pacific/Enderbury                    '
// ,'Pacific/Fakaofo                      '
// ,'Pacific/Fiji                         '
// ,'Pacific/Funafuti                     '
// ,'Pacific/Galapagos                    '
// ,'Pacific/Gambier                      '
// ,'Pacific/Guadalcanal                  '
// ,'Pacific/Guam                         '
// ,'Pacific/Honolulu                     '
// ,'Pacific/Johnston                     '
// ,'Pacific/Kiritimati                   '
// ,'Pacific/Kosrae                       '
// ,'Pacific/Kwajalein                    '
// ,'Pacific/Majuro                       '
// ,'Pacific/Marquesas                    '
// ,'Pacific/Midway                       '
// ,'Pacific/Nauru                        '
// ,'Pacific/Niue                         '
// ,'Pacific/Norfolk                      '
// ,'Pacific/Noumea                       '
// ,'Pacific/Pago_Pago                    '
// ,'Pacific/Palau                        '
// ,'Pacific/Pitcairn                     '
// ,'Pacific/Ponape                       '
// ,'Pacific/Port_Moresby                 '
// ,'Pacific/Rarotonga                    '
// ,'Pacific/Saipan                       '
// ,'Pacific/Tahiti                       '
// ,'Pacific/Tarawa                       '
// ,'Pacific/Tongatapu                    '
// ,'Pacific/Truk                         '
// ,'Pacific/Wake                         '
// ,'Pacific/Wallis                       '];