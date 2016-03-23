    <?php require_once("include/puma_conf.php"); ?>

    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    
      <div class="alert alert-danger alert-dismissible hide message-global" role="alert" id="msg_global">
        <button type="button" class="close" id="msg_global_btn"><span aria-hidden="true">&times;</span></button>
        <span id="message_global"></span>
      </div>
      <div class="container-fluid">
        <div class="navbar-header col-sm-3 col-md-2 ">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="main.php"> 
          <span><img src='img/<?php echo PDS_LOGO; ?>' width="150"/></span>
          <span class='glyphicon glyphicon-menu-hamburger main_menu_to_show main-menu-to window-mini-view' title="fold/unfold"></span>
          <span class='glyphicon glyphicon-menu-hamburger main_menu_to_hide main-menu-to hide window-mini-view' title="fold/unfold"></span>
          </a>
          
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="hidden" ><a href="main.php">首页</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            <li><img src='img/icon_user.png' width="30" style="margin-top:12px;" class='icon-user window-mini-view'/></li>
          	<li>
          		<a class="view-user-name" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" href="#">
			    	<?php session_start(); print isset($_SESSION["login_name"])?$_SESSION["login_name"]:"请登录"; session_write_close(); ?>
			    	<span class="caret"></span>
			    </a>
			    <ul class="dropdown-menu dropdown-menur" role="menu" aria-labelledby="dLabel">
			    	<li role="presentation"><a id="home_logout" role="menuitem" tabindex="-1" href="#">注销</a></li>
			    	<li role="presentation"><a id="modify_pass" role="menuitem" tabindex="-1" href="#">修改密码</a></li>
			    	<li role="presentation"><a id="modify_theme" role="menuitem" tabindex="-1" href="#">主题</a>
                        <ul class='nav menu-list-child'>
                            <li><a href="#" class='theme-change' theme-name=''>默认主题</a></li>
                            <li><a href="#" class='theme-change' theme-name='white'>白色主题</a></li>
                        </ul>
                    </li>
                    <li class="divider"></li>
                    <li role="presentation"><a role="menuitem" tabindex="-1" href="#"><?php echo PDS_VERSION; ?></a></li>
			    </ul>
          	</li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    
    
    
<div class="modal fade" id="user_pass_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog ">
	<div class="modal-content">
	  <div class="modal-header">
		<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
		<h4 class="modal-title">修改密码</h4>
	  </div>
	  <div class="modal-body">
		<div>
			<form class="form-horizontal" role="form">
			  <div class="form-group has-error">
				<div class="col-sm-offset-3 col-sm-8">
				  <span class="help-block hide" id="user_pass_error_msg"></span>
				</div>
			  </div>
			  <div class="form-group">
				<label class="control-label col-sm-3" for="user_pass_input_old" msg="原密码">原密码</label>
				<div class="col-sm-7">
					<input type="password" class="form-control requirement" id="user_pass_input_old" placeholder="输入原密码">
				</div>
			  </div>
              <div class="form-group">
				<label class="control-label col-sm-3" for="user_pass_input_new" msg="新密码">新密码</label>
				<div class="col-sm-7">
					<input type="password" class="form-control requirement" id="user_pass_input_new" placeholder="输入新密码">
				</div>
			  </div>
              <div class="form-group">
				<label class="control-label col-sm-3" for="user_pass_input_com" msg="确认密码">确认密码</label>
				<div class="col-sm-7">
					<input type="password" class="form-control requirement" id="user_pass_input_com" placeholder="输入确认密码">
				</div>
			  </div>
			  <div class="form-group">
				<div class="col-sm-offset-7 col-sm-5">
				  <button id="user_pass_btn_submit" type="button" class="btn btn-primary"> 提交 </button>&nbsp;&nbsp;&nbsp;
				  <button type="button" class="btn btn-default" data-dismiss="modal"> 取消 </button>
				</div>
			  </div>
			  
			</form>
		</div>
		<div id="user_pass_modal_loading" class="position-absolute hide">
			<?php require 'loading.php';?>
		</div>
	  </div>
	</div>
  </div>
</div>