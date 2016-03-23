<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>首页</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="main"; require 'header.php'; ?>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
            <?php require 'left_menu.php'; ?>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <div class="row content-panel-panel auto-load" id="dash_main" data-url="data/data_dash.php?func=info">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 集群名称: <span id="cluster_name"></span>
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="row main-info">
                        <div class="col-sm-6 sep">
                            <table class='table main-info-table'>
                                <tr><td>主机名称</td><td id="host_name_0"></td></tr>
                                <tr><td>状态</td><td id="host_status_0"></td></tr>
                                <tr><td>心跳IP</td><td id="host_ipaddr_0"></td></tr>
                            </table>
                        </div>
                        <div class="col-sm-6">
                            <table class='table main-info-table'>
                                <tr><td>主机名称</td><td id="host_name_1"></td></tr>
                                <tr><td>状态</td><td id="host_status_1"></td></tr>
                                <tr><td>心跳IP</td><td id="host_ipaddr_1"></td></tr>
                            </table>
                        </div>
                    </div>
                </div>
		  	</div>
            
            <div class="row content-panel-panel">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 资源状态
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <table class='table'>
                        <thead>
                            <tr><td>IP</td><td>逻辑卷</td><td>LUN</td><td>位置</td><td>状态</td></tr>
                        </thead>
                        <tbody class="auto-load-table" id="lun_list" data-url="data/data_dash.php?func=lun_list">
                    </tbody>
                    </table>
                </div>
            </div>
                
        </div>
      </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_main.js"></script>
</body>
</html>