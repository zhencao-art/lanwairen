<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>存储管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="stor"; require 'header.php'; ?>
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
                <a href='lvmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-inbox"></span><br>
                    逻辑卷管理
                </div>
                </a>
            </div>
            <div class="col-sm-3">
                <a href='vgmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-blackboard"></span><br>
                    存储池管理
                </div>
                </a>
            </div>
            <div class="col-sm-3">
                <a href='raidmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-tasks"></span><br>
                    RAID管理
                </div>
                </a>
            </div>
            <div class="col-sm-3">
                <a href='diskmgr.php'>
                <div class='stor-menu'>
                    <span class="glyphicon glyphicon-hdd"></span><br>
                    磁盘管理
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