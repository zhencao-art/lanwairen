<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>服务配置</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="conf"; require 'header.php'; ?>
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
                        <span class="glyphicon glyphicon-info-sign"></span>  服务IP列表
                        <span class="op-add navbar-right"><a href="#" class="ip-add"><span class='glyphicon glyphicon-cog'></span></a></span>&nbsp;&nbsp;
                        <span class='op-add navbar-right'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep4.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>IP</td>
                                <td>上次使用时间</td>
                                <td>使用结果</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" data-url="data/data_option.php?func=ip_list" id="ip_list">
                        </tbody>
                    </table>
			    </div>
		  	</div>
        </div>
      </div>
    </div>
    
    <div class="modal fade" id="setup_modal">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">服务IP批量管理</h4>
              </div>
              <div class="modal-body input-div">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="ip_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="col-sm-8 col-sm-offset-2">服务IP</label>
                  </div>
                  <div class="form-group">
                    <div class="col-sm-8 col-sm-offset-2">
                        <textarea class="form-control setup-ip-port" id="ip_port"></textarea>
                    </div>
                  </div>
                  <div class="form-group">
                    <div class="col-sm-8 col-sm-offset-2">
                        请输入服务IP地址,多个地址请换行<br>若需指定端口请使用"IP:端口"的格式(如192.168.1.100:1000)
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-body result-div hidden">
                <div class="result-content">
                </div>
              </div>
              <div class="modal-footer">
                <img class="btn-loading hidden" src="img/loading.gif">
                <button type="button" class="btn btn-primary input-div" id="btn_next">下一步</button>
                <button type="button" class="btn btn-primary result-div hidden" id="btn_pro">上一步</button>
                <button type="button" class="btn btn-primary result-div hidden" id="btn_submit">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
        </div>
    </div>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_setup.js"></script>
</body>
</html>