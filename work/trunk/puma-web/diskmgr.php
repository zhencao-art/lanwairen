<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>磁盘管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="disk"; require 'header.php'; ?>
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
                        <span class="glyphicon glyphicon-info-sign"></span> 磁盘列表 (已使用插槽: <span id="slot_used"></span>  总插槽: <span id="slot_all"></span>)
                            <span class="dropdown filter-node hidden">
                              <span class="btn dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                <span id="filter_node">所有磁盘</span>
                                <span class="caret"></span>
                              </span>
                              <ul class="dropdown-menu dropdown-menul" aria-labelledby="dropdownMenu1" id="node_filter" data-url-none = "data/data_node.php?func=node_list_json&node_type=ios">

                              </ul>
                            </span>
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>磁盘名称</td>
                                <td>总容量</td>
                                <td>槽位号</td>
                                <td class='besort'>WWN</td>
                                <td class='besort'>是否共享</td>
                                <td class='besort'>磁盘类型</td>
                                <td>使用状态</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="disk_list" data-url="data/data_disk.php?func=disk_list" data-url-source="data/data_disk.php?func=disk_list" call_back="update.infos">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_diskmgr.js"></script>
</body>
</html>