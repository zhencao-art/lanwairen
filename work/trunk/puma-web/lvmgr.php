<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>逻辑卷管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="lv"; require 'header.php'; ?>
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
            <div class="row content-panel-panel">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 逻辑卷列表
                        <span class="op-add navbar-right"><a href="#" class="lv-add"><span class='glyphicon glyphicon-plus'></span></a></span>
                        <span class='op-add navbar-right'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep3.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>逻辑卷名称</td>
                                <td class='besort'>存储池名称</td>
                                <td>容量</td>
                                <td>使用状态</td>
                                <td>资源类型</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" data-url="data/data_lv.php?func=lv_list" id="lv_list">
                        </tbody>
                    </table>
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    <?php include('lv_add.php'); ?>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_lvmgr.js"></script>
    <script src="js/puma_lv_add.js"></script>
</body>
</html>