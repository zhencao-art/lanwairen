<?php require("base.php"); ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>资源池管理</title>
    <?php require("css.php"); ?>
</head>
<body>
    <?php $menu="vg"; require 'header.php'; ?>
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
                        <span class="glyphicon glyphicon-info-sign"></span> 存储池列表
                        <span class='navbar-right op-add'><a href='#' class="vg-add text-large" ref-obj="sort_tab_list" title="创建存储池"><span class="glyphicon glyphicon-plus"> </span></a></span>&nbsp;
                        <span class='navbar-right op-add'><a href='#' class="refresh_table text-large" ref-obj="sort_tab_list" title="刷新"><span class="glyphicon glyphicon-refresh"> </span></a></span>&nbsp;
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <table class="table" id="sort_tab_list">
                        <thead>
                            <tr>
                                <td class='besort'>存储池名称</td>
                                <td>容量</td>
                                <td>剩余容量</td>
                                <td>块设备数</td>
                                <td>逻辑卷数</td>
                                <td>操作</td>
                            </tr>
                        </thead>
                        <tbody class="auto-load-table" id="vg_list" data-url="data/data_vg.php?func=vg_list">
                        </tbody>
                    </table>
			    </div>
		  	</div>
            <div class="row content-panel hidden">
                
		  	</div>
        </div>
      </div>
    </div>
    
    <div class="modal fade" id="vg_info">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title"><span class="glyphicon glyphicon-info-sign"></span> 存储池详细</h4>
              </div>
              <div class="modal-body">
                <div class="panel" id="vg_info_info">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 存储池信息
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <table class="table vg-infotab infotab-3">
                        <tr>
                            <td>存储池名称</td>
                            <td id="vg_name"> </td>
                            <td>总容量</td>
                            <td id="vg_size"> </td>
                            <td>剩余容量</td>
                            <td id="vg_free_size"> </td>
                        </tr>
                    </table>
                </div>
                <div class="panel panel-follow panel-lun-list" id="vg_info_pvs">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 块设备列表(共: <span id="vg_cur_pv_num"></span> 个)
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <td>设备名称</td>
                                <td>容量</td>
                                <td>剩余容量</td>
                                <td>设备类型</td>
                            </tr>
                        </thead>
                        <tbody id="pv_list" class="auto-load-table pause vg-ref" data-url="data/data_vg.php?func=pv_list_by_vg" data-url-origin="data/data_vg.php?func=pv_list_by_vg">
                        </tbody>
                    </table>
                    </div>
                </div>
                <div class="panel panel-follow panel-lun-list" id="vg_info_lvs">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 逻辑卷列表(共: <span id="vg_cur_lv_num"></span> 个)
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <table class="table fixed-disk-list-table">
                        <thead>
                            <tr>
                                <td>逻辑卷名称</td>
                                <td>容量</td>
                            </tr>
                        </thead>
                    </table>
                    <div class="fixed-table-height">
                        <table class="table fixed-disk-list-table">
                            <tbody id="lv_list" class="auto-load-table pause vg-ref" data-url="data/data_vg.php?func=lv_list_by_vg" data-url-origin="data/data_vg.php?func=lv_list_by_vg">
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
    
    
    <div class="modal fade" id="vg_opt">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title"><span class="glyphicon glyphicon-info-sign"></span> <span id="vg_opt_title">扩展存储池</span></h4>
              </div>
              <div class="modal-body">
                <div class="panel panel-pv-list hidden">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 物理卷列表
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <td></td>
                                <td>物理卷名称</td>
                                <td>总容量</td>
                                <td>剩余容量</td>
                                <td>类型</td>
                            </tr>
                        </thead>
                        <tbody id="raid_list" class="auto-load-table pause vg-opt-tbody" data-url="data/data_vg.php?func=pv_list_by_vg" data-url-origin="data/data_vg.php?func=pv_list_by_vg">
                        </tbody>
                    </table>
                    </div>
                </div>
                <div class="panel panel-lun-list panel-lun-list-op hidden">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> RAID列表
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <td></td>
                                <td>RAID名称</td>
                                <td>总容量</td>
                                <td>RAID类型</td>
                                <td>块大小</td>
                            </tr>
                        </thead>
                        <tbody id="raid_list" class="auto-load-table pause vg-opt-tbody" data-url="data/data_vg.php?func=raid_list_by_vg" data-url-origin="data/data_vg.php?func=raid_list_by_vg">
                        </tbody>
                    </table>
                    </div>
                </div>
                <div class="panel panel-follow panel-lun-list panel-lun-list-op hidden">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-info-sign"></span> 物理磁盘列表
                    </div>
                    <div class="content-sep"><img src="img/sep1.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table">
                        <thead>
                            <tr>
                                <td></td>
                                <td>磁盘名称</td>
                                <td>总容量</td>
                                <td>slot</td>
                                <td>WWN</td>
                                <td>是否共享</td>
                            </tr>
                        </thead>
                        <tbody id="disk_list" class="auto-load-table pause vg-opt-tbody" data-url="data/data_vg.php?func=disk_list_by_vg" data-url-origin="data/data_vg.php?func=disk_list_by_vg">
                        </tbody>
                    </table>
                    </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary btn-opt" id="btn_extend">扩展</button>
                <button type="button" class="btn btn-primary btn-opt" id="btn_reduce">缩小</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="opt_loading" class="hidden">
                <?php require("loading.php"); ?>
            </div>
        </div>
    </div>
    
    <?php include('vg_add.php'); ?>
    
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/tooltip.js"></script>
    <script src="js/puma_common.js"></script>
    <script src="js/puma_vgmgr.js"></script>
    <script src="js/puma_vg_add.js"></script>
</body>
</html>