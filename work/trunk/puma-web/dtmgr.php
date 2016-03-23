<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>日期时间配置</title>
    <?php require("css.php"); ?>
    <link href="css/bootstrap-datetimepicker.min.css" rel="stylesheet"/>
</head>
<body>
    <?php $menu="dt"; require 'header.php'; ?>
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
            <div class="row content-dt-panel auto-load" id="dt_info" data-url="data/data_dt.php?func=dt">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 日期时间信息
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="dt_info" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class='row'>
                        <div class="col-sm-2">当前系统时间</div>
                        <div class="col-sm-10" id="dt_info_dt"></div>
                    </div>
                    
			    </div>
		  	</div>
            <div class="row content-dt-panel auto-load" id="dt_info_set" data-url="data/data_dt.php?func=dt_get">
                <div class="panel">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 同步配置
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="dt_info_set" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                        <span class='navbar-right op-add'><a href='#' class="dt-info-edit text-large" title="同步配置"><span class="glyphicon glyphicon-cog"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div>
                        <div class='row'>
                            <div class="col-sm-2">时区</div>
                            <div class="col-sm-2" id="dt_set_tz"></div>
                            <div class="col-sm-6"><a href='#' class='timezone-edit'><span class="glyphicon glyphicon-pencil"> </span></a></div>
                        </div>
                        <div class='row'>
                            <div class="col-sm-2">时间同步</div>
                            <div class="col-sm-10" id="dt_set_syc"></div>
                            <div class="hidden" id="dt_set_syc_srouce"></div>
                            <div class="hidden" id="dt_set_host_srouce"></div>
                        </div>
                        <div class='row'>
                            <div class="col-sm-2">同步服务器</div>
                            <div class="col-sm-10" id="dt_set_srv"></div>
                        </div>
                    </div>
			    </div>
		  	</div>
        </div>
      </div>
    </div>
    
    <div class="modal fade" id="dt_set_modal">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">时间同步配置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="dt_set_timezone">时区</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="dt_set_timezone"></select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="dt_set_is_syc" msg="时间同步">时间同步</label>
                    <div class="col-sm-7">
                        <label class="radio-inline">
                          <input type="radio" name="dt_set_is_syc" id="dt_set_is_syc_1" value="1"> 启用
                        </label>
                        <label class="radio-inline">
                          <input type="radio" name="dt_set_is_syc" id="dt_set_is_syc_0" value="0"> 不启用
                        </label>
                    </div>
                  </div>
                  <div class="form-group syc-type syc-group">
                    <label class="control-label col-sm-3" for="dt_set_syc_main" msg="主节点">主节点</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="dt_set_syc_main"></select>
                    </div>
                  </div>
                  <div class="form-group syc-type syc-group">
                    <label class="control-label col-sm-3" for="dt_set_syc_srv" msg="同步服务器">同步服务器</label>
                    <div class="col-sm-7">
                        <input class="form-control" id="dt_set_syc_srv" placeholder="输入同步服务器" reg="^(((((25[0-5]|2[0-4]\d|[01]?\d\d?)(\.(25[0-5]|2[0-4]\d|[01]?\d\d?)){3})|([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6}))($|(?!\,$)\,))+)$" reg_tip="格式不正确,多个IP或域名用逗号隔开">
                    </div>
                  </div>
                  <div class="form-group syc-type time-group hidden">
                    <label class="control-label col-sm-3" for="dt_set_syc_dt" msg="日期时间">日期时间</label>
                    <div class="col-sm-7">
                        <input class="form-control" type="text" value="2016-02-01 21:05:00" id="dt_set_syc_dt" data-date-format="yyyy-mm-dd hh:ii:ss" data-date-language='zh-CN' data-date-forceParse=true data-date-endDate="2099-12-30 23:59" data-date-startDate="2000-01-01 00:00" reg="^20\d{2}\-\d{2}\-\d{2} \d{2}\:\d{2}\:\d{2}$" reg_tip="格式不正确,年份只能以20开头">
                    </div>
                  </div>
                </form>
                
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="dt_set_btn">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
              <div id="dt_set_modal_loadding" class="hidden">
              <?php include("loading.php"); ?>
              </div>
            </div>
        </div>
    </div>
    
    
    <div class="modal fade" id="zone_set_modal">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">时区配置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="zone_set_timezone">时区</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="zone_set_timezone"></select>
                    </div>
                  </div>
                </form>
                
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="zone_set_btn">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
              <div id="zone_set_modal_loadding" class="hidden">
              <?php include("loading.php"); ?>
              </div>
            </div>
        </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/bootstrap-datetimepicker.min.js"></script>
    <script src="js/bootstrap-datetimepicker.zh-CN.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_dtmgr.js"></script>
</body>
</html>