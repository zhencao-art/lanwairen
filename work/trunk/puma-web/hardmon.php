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
    <?php $menu="hardmon"; require 'header.php'; ?>
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
                <div class="panel auto-load" id="hardmon_cluster" data-url="data/data_mon.php?func=info" call_back="refresh_chart">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 系统概况
                        <span class=" navbar-right"><span class='glyphicon glyphicon-menu-up hidden'></span></span>
                        <span class='navbar-right'><a href='#' class="refresh_table text-large" ref-obj="hardmon_cluster" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a><span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="col-sm-3">
                        <div class='mon-values'>节点数<span class="mon-value-inner"><span id="node_all">3</span> 个</span></div>
                    </div>
                    <div class='col-sm-3'>
                        <div class="mon-values">磁盘数<span class="mon-value-inner"><span id="disk_all">10</span> 个</span></div>
                    </div>
                    <div class='col-sm-3'>
                        <div class="mon-values">内存总大小<span class="mon-value-inner"><span id="mem_capacity">30</span> GB</span></div>
                    </div>
                    <div class='col-sm-3'>
                        <div class="mon-values">CPU总核数<span class="mon-value-inner"><span id="cpu_cores">10</span> 个</span></div>
                    </div>
                </div>
                <div class="cluster-chart">
                <div class="col-sm-4">
                    <div>IOPS<span class="content-float-right-iops">IOPS</span></div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class='mon-line-chart auto-refresh' unit_name="IOPS" series_color="#0B7E4F" unit_k="1000">
                    </div>
                </div>
                <div class="col-sm-4">
                    <div>吞吐量<span class="content-float-right-kbps">Kbps</span></div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class='mon-line-chart auto-refresh' unit_name="Kbps" series_color="#0BB1FF" unit_k="1000">
                    </div>
                </div>
                <div class="col-sm-4">
                    <div>延迟<span class="content-float-right-ms">ms</span></div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class='mon-line-chart auto-refresh' unit_name="ms" series_color="#FF4930" unit_k="1000">
                    </div>
                </div>
                </div>
            </div>
            <div class="row content-panel-panel">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 节点列表
                        <span class=" navbar-right"><span class='glyphicon glyphicon-menu-up hidden'></span></span>
                        <span class='navbar-right'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a><span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <table class="table table-border" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>节点IP</td><td>状态</td><td>硬盘数</td><td>内存总大小</td><td>CPU总核数</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="node_list" data-url="data/data_mon.php?func=node_list">
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
      </div>
    </div>
    <div id="info_node_tr" class="hidden">
        <div class="child-title">
            <div style='float:left'> 硬盘</div>
            <div class='status-title status-uninit'></div><div style='float:left'>&nbsp;&nbsp;未使用</div>
            <div class='status-title status-normal'></div><div style='float:left'>&nbsp;&nbsp;正常使用中</div>
            <div class='status-title status-offline'></div><div style='float:left'>&nbsp;&nbsp;OFFLINE</div>
        </div>
        <div class="content-sep"><img src="img/sep2.png"></div>
        <div id="node_disk_list">
        </div>
        <div class="child-title">端口</div>
        <div class="content-sep"><img src="img/sep2.png"></div>
        <div id="node_port_list">
        </div>
        <div class="child-title">性能监控</div>
        <div class="content-sep"><img src="img/sep2.png"></div>
        <div class="cluster-chart">
            <div class="col-sm-4">
                <div>CPU使用率</div>
                <div class='mon-node-chart' unit_name="%" series_name="CPU使用率" series_color="#0B7E4F">
                </div>
            </div>
            <div class="col-sm-4">
                <div>内存使用率</div>
                <div class='mon-node-chart' unit_name="%" series_name="内存使用率" series_color="#0BB1FF">
                </div>
            </div>
            <div class="col-sm-4">
                <div>硬盘容量使用率</div>
                <div class='mon-node-chart' unit_name="%" series_name="硬盘容量使用率" series_color="#FF4930">
                </div>
            </div>
        </div>
    </div>
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/highcharts.js"></script>
    <script src="js/puma_sethighcharts.js"></script>
    <script src="js/puma_hardmon.js"></script>
    <script src="js/puma_common.js"></script>
</body>
</html>