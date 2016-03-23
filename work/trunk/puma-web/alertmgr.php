<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title>告警管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="alert"; require 'header.php'; ?>
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
            <div>

              <!-- Nav tabs -->
              <ul class="nav nav-tabs" role="tablist">
                <li role="presentation" class="active"><a href="#alert" aria-controls="alert" role="tab" data-toggle="tab">&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-alert"></span>&nbsp;告警&nbsp;&nbsp;&nbsp;</a></li>
                <li role="presentation"><a href="#event" aria-controls="event" role="tab" data-toggle="tab">&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-list-alt"></span>&nbsp;事件&nbsp;&nbsp;&nbsp;</a></li>
                <span class='navbar-right tab-refresh'><a href='#' class="refresh_table text-large" ref-obj="alert_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a><span>&nbsp;
              </ul>

              <!-- Tab panes -->
              <div class="tab-content">
                <div role="tabpanel" class="tab-pane active" id="alert">
                    <table class="table" id="alert_list">
                        <thead>
                            <tr>
                                <td>级别</td>
                                <td>状态</td>
                                <td>时间</td>
                                <td>告警对象</td>
                                <td>告警描述</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table no-refresh" load-type='tab' data-url="data/data_alert.php?func=alert_list&page_no=1&page_size=30" data-url-origin="data/data_alert.php?func=alert_list">
                        </tbody>
                    </table>
                </div>
                <div role="tabpanel" class="tab-pane" id="event">
                    <table class="table" id="event_list">
                        <thead>
                            <tr>
                                <td>时间</td>
                                <td>操作人</td>
                                <td>事件对象</td>
                                <td>事件描述</td>
                                <td>状态</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table no-refresh pause" load-type='tab' data-url="data/data_alert.php?func=event_list&page_no=1&page_size=30" data-url-origin="data/data_alert.php?func=event_list">
                        </tbody>
                    </table>
                </div>
              </div>

              <div class="row license-page-row">
                    第 <input id="page_no" class="page-no"/> 页 , 共 <span id="page_count"></span> 页 , 共 <span id="page_count_row"></span> 条记录
                    <nav class="pull-right">
                      <ul class="pagination" id="page_tool">
                        
                      </ul>
                    </nav>
              </div>
            </div>
        </div>
      </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/highcharts.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_alertmgr.js"></script>
</body>
</html>