    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        $("#"+$(e.relatedTarget).attr("aria-controls")).find("tbody").addClass("pause");
        $("#"+$(e.target).attr("aria-controls")).find("tbody").removeClass("pause");
        $(".refresh_table").attr("ref-obj",$(e.target).attr("aria-controls")+"_list");
        var tbody = $("#"+$(".refresh_table").attr("ref-obj")).find("tbody");
        page_no = tbody.attr("page_no")?tbody.attr("page_no"):1;
        page_size = tbody.attr("page_size")?tbody.attr("page_size"):30;
        page_count = tbody.attr("page_count")?tbody.attr("page_count"):1;
        loadDataByPageNo();
    });

    var license_list_body = $("#license_list");
    var page_no = 1,
        page_size = 30,
        page_count = 1,
        show_page_no = $("#page_no"),
        show_page_count = $("#page_count"),
        show_page_count_row = $("#page_count_row"),
        show_page_tool = $("#page_tool");
   
    show_page_no.on("keypress",function(event){
        var _this = $(this);
        if(event.keyCode==13){
            if(_this.val()){
                page_no = parseInt(_this.val());
                loadDataByPageNo();
            }
            return false;
        }
        if(event.keyCode!==8){
            if(!page_count){
                return false;
            }
            if(event.charCode<48 || event.charCode>57){
                return false;
            }
        }
    }).on("keyup",function(event){
        var _this = $(this);
        if(!_this.val()){
            return;
        }
        if(_this.val()>page_count){
            _this.val(page_count);
        }else if(_this.val()<1){
            _this.val(1);
        }
    });

    function loadDataByPageNo(){
        var tbody = $("#"+$(".refresh_table").attr("ref-obj")).find("tbody");
        tbody.attr("page_no",page_no);
        tbody.attr("page_size",page_size);
        tbody.attr("page_count",page_count);
        tbody.attr("data-url",tbody.attr("data-url-origin")+"&page_no="+page_no+"&page_size="+page_size);
        tbody.trigger("data.update");
    }
    $(".auto-load-table").on("update.tool",function(){
        var _this = $(this);
        var page_count_row = parseFloat(_this.attr("page_count"));
        page_count = Math.ceil(page_count_row/page_size);
        show_page_count.html(page_count);
        show_page_count_row.html(page_count_row);
        show_page_no.val(page_no);
        var tool_html = "";
        if(page_no<=1){
            tool_html += "<li class='disabled'> <span aria-label='Previous'> <span aria-hidden='true'>&laquo;</span> </span> </li>";
        }else{
            tool_html += "<li> <a href='#' aria-label='Previous' page='previous' class='page_tool'> <span aria-hidden='true'>&laquo;</span> </a> </li>";
        }
        if(page_count<6){
            for(var i=1;i<=page_count;i++){
                tool_html += "<li "+(i==page_no?"class='active'":"")+"><a href='#' page='"+i+"' class='page_tool'>"+i+"</a></li>";
            }
        }else{
            if(page_no<4){
                for(var i=1;i<=4;i++){
                    tool_html += "<li "+(i==page_no?"class='active'":"")+"><a href='#' page='"+i+"' class='page_tool'>"+i+"</a></li>";
                }
                tool_html += "<li><span class='non-top-bottom-border'>...</span></li>";
                tool_html += "<li><a href='#' page='"+page_count+"' class='page_tool'>"+page_count+"</a></li>";
            }else if(page_no>page_count-3){
                tool_html += "<li><a href='#' page='1' class='page_tool'>1</a></li>";
                tool_html += "<li><span class='non-top-bottom-border'>...</span></li>";
                for(var i=page_count-3;i<=page_count;i++){
                    tool_html += "<li "+(i==page_no?"class='active'":"")+"><a href='#' page='"+i+"' class='page_tool'>"+i+"</a></li>";
                }
            }else{
                tool_html += "<li><a href='#' page='1' class='page_tool'>1</a></li>";
                tool_html += "<li><span class='non-top-bottom-border'>...</span></li>";
                for(var i=page_no-1;i<=page_no+1;i++){
                    tool_html += "<li "+(i==page_no?"class='active'":"")+"><a href='#' page='"+i+"' class='page_tool'>"+i+"</a></li>";
                }
                tool_html += "<li><span class='non-top-bottom-border'>...</span></li>";
                tool_html += "<li><a href='#' page='"+page_count+"' class='page_tool'>"+page_count+"</a></li>";
            }
        }
        if(page_no>=page_count){
            tool_html += "<li class='disabled'> <span aria-label='Next'> <span aria-hidden='true'>&raquo;</span> </span> </li>";
        }else{
            tool_html += "<li> <a href='#' aria-label='Next' page='next' class='page_tool'> <span aria-hidden='true'>&raquo;</span> </a> </li>";
        }
        show_page_tool.html(tool_html);
        
    });
    show_page_tool.delegate(".page_tool","click",function(){
        var _this = $(this);
        var page = _this.attr("page");
        if(page=="previous" && page_no>0){
            page_no--;
        }else if(page=="next" && page_no<page_count){
            page_no++;
        }else{
            page_no = parseInt(page);
        }
        loadDataByPageNo();
        return false;
    });