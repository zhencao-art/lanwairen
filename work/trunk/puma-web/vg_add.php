    <div class="modal fade" id="vg_add_modal">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">创建存储池</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="vg_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2" for="input_vg_name" msg="存储池名称">存储池名称</label>
                    <div class="col-sm-4">
                        <input class="form-control requirement" id="input_vg_name" placeholder="输入存储池名称" reg="^[0-9|_|a-z|A-Z]{1,12}$" reg_tip="只能输入由字母、数字或下划线组成的12位以内的字符">
                    </div>
                  </div>
                </form>
                <div class="panel panel-follow panel-lun-list">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-th-list"></span> RAID列表
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table cursor-pointer">
                        <thead>
                            <tr>
                                <td></td>
                                <td>RAID名称</td>
                                <td>总容量</td>
                                <td>RAID类型</td>
                                <td>块大小</td>
                            </tr>
                        </thead>
                        <tbody id="vg_raid_list" class="auto-load-table no-refresh pause" data-url="data/data_raid.php?func=raid_list_for_vging" data-url-source="data/data_disk.php?func=disk_list_for_raiding">
                        </tbody>
                    </table>
                    </div>
                </div>
                <div class="panel panel-follow panel-lun-list">
                    <div class="panel-heading panel-heading-noboard">
                        <span class="glyphicon glyphicon-th-list"></span> 磁盘列表
                    </div>
                    <div class="content-sep"><img src="img/sep2.png"></div>
                    <div class="maxheight-vg-table">
                    <table class="table cursor-pointer">
                        <thead>
                            <tr>
                                <td></td>
                                <td>磁盘名称</td>
                                <td>容量</td>
                                <td>是否共享</td>
                            </tr>
                        </thead>
                        <tbody id="vg_disk_list" class="auto-load-table no-refresh pause" data-url="data/data_disk.php?func=disk_list_for_vging" data-url-source="data/data_disk.php?func=disk_list_for_raiding">
                        </tbody>
                    </table>
                    </div>
                </div>
              <div class="modal-footer">
                <img class="btn-loading hidden" src="img/loading.gif">
                <button type="button" class="btn btn-primary" id="vg_add_sub">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
              <div id="modal_abled" class="hidden">
              <?php include("loading.php"); ?>
              </div>
            </div>
        </div>
    </div>