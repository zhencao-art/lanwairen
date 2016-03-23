<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>Target管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="iscsi"; require 'header.php'; ?>
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
                        <span class="glyphicon glyphicon-info-sign"></span> Target列表 
                        <span class='navbar-right op-add'><a href='#' class="map-add text-large" title="创建Target"><span class="glyphicon glyphicon-plus"> </span></a></span>&nbsp;
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td>服务端IQN</td>
                                <td>IP</td>
                                <td>逻辑卷</td>
                                <td>LUN</td>
                                <td>状态</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="map_list" data-url="data/data_map.php?func=map_list" data-url-source="data/data_map.php?func=map_list">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    <div class="modal fade" id="map_move_modal">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title"><span class="glyphicon glyphicon-info-sign"></span> 资源迁移</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="map_move_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="map_move_host">迁移至</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="map_move_host">
                        </select>
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="map_move_sub">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="map_move_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>
    
    <?php include("map_add.php"); ?>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_mapmgr.js"></script>
    <script src="js/puma_map_add.js"></script>
</body>
</html>