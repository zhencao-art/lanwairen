<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>硬件管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="hard"; require 'header.php'; ?>
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
            <?php require 'left_menu.php'; ?>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <div class="row content-panel auto-load" id="dash_main" data-url="data/data_hard.php?func=info">
                <div class="col-sm-6 sep content-col">
                    <div class="content-float-right">
                        <div class="content-value-top" id="nodes_all"></div>
                        <div class="content-title-bottom">节点总数</div>
                    </div>
                    <div class="content-float-none">
                        <div class="content-title">节点概况</div>
                        <div class="content-value">节点状态(正常/故障/未用)&nbsp;&nbsp;&nbsp;&nbsp;<span id="nodes_normal">0</span>/<span id="nodes_error" class="color_red">0</span>/<span id="nodes_uninit">0</span></div>
                        <div class="content-value">节点类型(ios/bac)&nbsp;&nbsp;&nbsp;&nbsp;<span id="nodes_ios">0</span>/<span id="nodes_bac">0</span></div>
                    </div>
                </div>
                <div class="col-sm-6 content-col">
                    <div class="content-float-right">
                        <div class="content-value-top" id="disk_all">0</div>
                        <div class="content-title-bottom">磁盘总数</div>
                    </div>
                    <div class="content-float-none">
                        <div class="content-title">磁盘概况</div>
                        <div class="content-value">磁盘状态(正常/异常/未用)&nbsp;&nbsp;&nbsp;&nbsp;<span id="disk_online">0</span>/<span id="disk_offline" class="color_red">0</span>/<span id="disk_uninit">0</span></div>
                        <div class="content-value">磁盘类型(SSD/HDD)&nbsp;&nbsp;&nbsp;&nbsp;<span id="disk_ssds">0</span>/<span id="disk_hdds">0</span></div>
                    </div>
                </div>
		  	</div>
            <div class="row content-panel ">
                <div class="col-sm-6">
                    <div>IOPS<span class="content-float-right-title">IOPS</span></div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class='main-line-chart auto-refresh' unit_name="IOPS" unit_k="1000">
                    </div>
                </div>
                <div class="col-sm-6">
                    <div>吞吐量<span class="content-float-right-title">Kbps</span></div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class='main-line-chart auto-refresh' unit_name="Kbps" unit_k="1000">
                    </div>
                </div>
            </div>
            <div class="row content-panel ">
                <div class="col-sm-6">
                    <div>CPU使用率<span class="content-float-right-title">%</span></div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class='main-line-chart auto-refresh' unit_name="%">
                    </div>
                </div>
                <div class="col-sm-6">
                    <div>内存使用率<span class="content-float-right-title">%</span></div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class='main-line-chart auto-refresh' unit_name="%">
                    </div>
                </div>
		  	</div>
        </div>
      </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/highcharts.js"></script>
    <script src="js/puma_sethighcharts.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_hardmgr.js"></script>
</body>
</html>