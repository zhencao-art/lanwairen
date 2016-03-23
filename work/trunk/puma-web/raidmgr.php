<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>RAID管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="raid"; require 'header.php'; ?>
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
                        <span class="glyphicon glyphicon-info-sign"></span> RAID列表
                            <span class="dropdown filter-node hidden">
                              <span class="btn dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                <span id="filter_node">所有RAID</span>
                                <span class="caret"></span>
                              </span>
                              <ul class="dropdown-menu dropdown-menul" aria-labelledby="dropdownMenu1" id="node_filter" data-url-none = "data/data_node.php?func=node_list_json&node_type=ios">

                              </ul>
                            </span>
                        <span class='navbar-right op-add'><a href='#' class="raid-add text-large" ref-obj="sort_tab_list" title="创建RAID"><span class="glyphicon glyphicon-plus"> </span></a></span>&nbsp;
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>RAID名称</td>
                                <td>总容量</td>
                                <td class='besort'>RAID类型</td>
                                <td>块大小</td>
                                <td>RAID磁盘数</td>
                                <td>使用状态</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="raid_list" data-url="data/data_raid.php?func=raid_list" data-url-source="data/data_raid.php?func=raid_list">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    <div class="modal fade" id="raid_info">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title"><span class="glyphicon glyphicon-info-sign"></span> RAID详细</h4>
              </div>
              <div class="modal-body">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> RAID信息
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table raid-infotab infotab-3">
                        <tr>
                            <td>RAID名称</td>
                            <td id="raid_info_name"> </td>
                            <td>RAID类型</td>
                            <td id="raid_info_type"> </td>
                            <td>RAID状态</td>
                            <td id="raid_info_status"> </td>
                        </tr>
                        <tr>
                            <td>总容量</td>
                            <td id="raid_info_size"> </td>
                            <td>块大小</td>
                            <td id="raid_info_chunk" colspan='3'> </td>
                        </tr>
                    </table>
                </div>
                
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 物理磁盘信息
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div>
                        <table class="table" id="sort_tab_list">
                            <thead>
                                <tr>
                                    <td class='besort'>磁盘名称</td>
                                    <td>总容量</td>
                                    <td>槽位号</td>
                                    <td>WWN</td>
                                </tr>
                            </thead>
                            <tbody id="raid_info_disk_list" >
                            </tbody>
                        </table>
                    </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
        </div>
    </div>
    
    <?php include('raid_add.php'); ?>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_raidmgr.js"></script>
    <script src="js/puma_raid_add.js"></script>
</body>
</html>