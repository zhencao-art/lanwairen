<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>集群配置</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="cluster"; require 'header.php'; ?>
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
            <div class="row" style="margin-bottom: 10px;">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 集群操作
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class="panel-body">
                    <button type="button" class="btn btn-danger cluster-func" func_type="cluster_start"> 启动集群 </button>
                    <button type="button" class="btn btn-danger cluster-func" func_type="cluster_stop"> 关闭集群 </button>
                    </div>
			    </div>
		  	</div>
            <div class="row" style="margin-bottom: 10px;">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 集群名称配置 
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="cls_opt_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table cls-name-table" id="cls_opt_list">
                        <tbody class="auto-load-table" id="cluster_list" data-url="data/data_cluster.php?func=cluster_name">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel-panel">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 集群心跳配置
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="hb_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table hb-table" id="hb_list">
                        <thead>
                            <tr>
                                <td>节点名称</td>
                                <td>心跳IP</td>
                                <td>状态</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="hb_ip_list" data-url="data/data_cluster.php?func=hb_ip">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel-panel">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 集群脑裂配置
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="stonith_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <table class="table stonith-table" id="stonith_list">
                        <thead>
                            <tr>
                                <td>节点名称</td>
                                <td>IPMI地址</td>
                                <td>IPMI用户名</td>
                                <td>IPMI密码</td>
                                <td>启用状态</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="sth_list" data-url="data/data_cluster.php?func=stonith_list">
                        </tbody>
                    </table>
                    
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    
    <?php include("cluster_hb_set.php"); ?>
    <?php include("cluster_opt_set.php"); ?>
    <?php include("cluster_stonith_set.php"); ?>
    <?php include("cluster_name_set.php"); ?>
    
    <div id="cluster_set_loadding" class="hidden">
        <?php include("loading.php"); ?>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_clustermgr.js"></script>
    <script src="js/puma_cluster_hb_set.js"></script>
    <script src="js/puma_cluster_opt_set.js"></script>
    <script src="js/puma_cluster_stonith_set.js"></script>
    <script src="js/puma_cluster_name_set.js"></script>
</body>
</html>