$(function(){
	$("#uname").focus();
	$("#uname").keyup(function(event){
		if(event.keyCode==13){
			if(!$(this).val()){
                $(this).popover('show');
				return;
			}
			$("#pass").focus();
		}
	});
	$("#pass").keyup(function(event){
		if(event.keyCode==13){
			$("#submit").focus();
			$("#submit").trigger("click");
		}
	});
	$("input").blur(function(){
		var _this = $(this);
		if(_this.val()){
			_this.popover('hide');
		}else{
			_this.popover('show');
		}
	});
	$("#submit").click(function(){
		var loading = $("#login_loading"),
			msg = $("#login_error_msg");
		var uname = $("#uname"),
			pass = $("#pass");
		msg.addClass("hidden");
		if(!uname.val()){
			uname.trigger("blur");
			uname.focus();
			return;
		}
		if(!pass.val()){
			pass.trigger("blur");
			pass.focus();
			return;
		}
		loading.removeClass("hidden");
		$.ajax({
		   type: "POST",
		   url: "data/data_user.php",
		   data: {"func":"login","username":uname.val(),"passwd":pass.val()},
		   dataType: "json",
		   error: function(XMLHttpRequest, textStatus, errorThrown){
			msg.removeClass("hidden");
			msg.removeClass("success");
			msg.addClass("error");
			msg.html("登录失败:"+textStatus);
		   },
		   success: function(rs){
			  	msg.removeClass("success");
			   	msg.removeClass("error");
		   		if(rs.result){
		   			msg.addClass("success");
		   			msg.html("登录成功");
                    // if(rs.ips==0){
                        // document.location="setup.php";
                    // }else{
                        document.location="main.php";
                    // }
		   			// $.ajax({
				 		   // type: "POST",
				 		   // url: "index1.php",
				 		   // data: {"enter":"Sign in","name":uname.val(),"password":pass.val()},
				 		   // dataType: "json",
				 		   // error: function(XMLHttpRequest, textStatus, errorThrown){
				 		   // },
				 		   // success: function(rs){
				 		   // },
						   // complete: function(){
				 			  // if(!rs.init){
					   				// document.location="setup.php";
					   				// return;
					   			// }
						 		// document.location="main.php";
						   // }
				 		// });
		   			
			 	}else{
			 		msg.addClass("error");
					msg.html("用户名或密码错误,请重新登录");
				}
		   },
		   complete: function(){
			   loading.addClass("hidden");
			   msg.removeClass("hidden");
		   }
		});
	});
});