    <div class="modal fade" id="raid_add_modal">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">创建RAID</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="lun_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2" for="raid_rname" msg="RAID名称">RAID名称</label>
                    <div class="col-sm-4">
                        <input class="form-control requirement" id="raid_rname" placeholder="输入RAID名称" reg="^md[0-9]{1,6}$" reg_tip="只能输入以md开头，数字结尾组成的8位以内的字符">
                    </div>
                    <label class="control-label col-sm-2" for="raid_type">RAID类型</label>
                    <div class="col-sm-4">
                        <select class="form-control" id="raid_type">
                            <option value='0'>RAID0</option>
                            <option value='1'>RAID1</option>
                            <option value='4'>RAID4</option>
                            <option value='5'>RAID5</option>
                            <option value='6'>RAID6</option>
                            <option value='10'>RAID10</option>
                        </select>
                    </div>
                  </div>
                  <div class="form-group chunk-div hidden">
                    <label class="control-label col-sm-2" for="raid_stripe" msg="块大小(kib)">块大小(kib)</label>
                    <div class="col-sm-4">
                        <select class="form-control" id="raid_stripe">
                            <option>4</option>
                            <option>8</option>
                            <option>16</option>
                            <option>32</option>
                            <option>64</option>
                            <option>128</option>
                            <option>256</option>
                            <option>512</option>
                            <option>1024</option>
                        </select>
                    </div>
                  </div>
                </form>
                <div class="panel panel-lun-list">
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
                        <tbody id="raid_disk_list" class="auto-load-table no-refresh pause" data-url="data/data_disk.php?func=disk_list_for_raiding" data-url-source="data/data_disk.php?func=disk_list_for_raiding">
                        </tbody>
                    </table>
                    </div>
                </div>
                
              </div>
              <div class="modal-footer">
                <img class="btn-loading hidden" src="img/loading.gif">
                <button type="button" class="btn btn-primary" id="raid_add_sub">提交</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
              <div id="modal_abled" class="hidden">
              <?php include("loading.php"); ?>
              </div>
            </div>
        </div>
    </div>