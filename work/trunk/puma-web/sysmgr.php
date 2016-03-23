<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>系统配置</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="sys"; require 'header.php'; ?>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
            <?php require 'left_menu.php'; ?>
        </div>
        <div class="main_menu_hide hide">
          <div>
          	<a href="#"><span class="glyphicon glyphicon-eye-open" title="fold/unfold"></span></a>
          </div>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <div class="col-sm-3">
                <a href='netmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-th"></span><br>
                    网络配置
                </div>
                </a>
            </div>
            <div class="col-sm-3">
                <a href='dtmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-time"></span><br>
                    日期时间
                </div>
                </a>
            </div>
            
        </div>
      </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/puma_common.js"></script>
</body>
</html>