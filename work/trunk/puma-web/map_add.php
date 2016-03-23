    <div class="modal fade" id="map_add">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">新增Target</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="map_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2" for="map_ip_name" msg="IP地址">IP地址</label>
                    <div class="col-sm-4">
                        <input class="form-control requirement" id="map_ip_name" placeholder="输入IP地址" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                    </div>
                    <label class="control-label col-sm-2" for="map_ip_nic">网卡</label>
                    <div class="col-sm-4">
                        <select class="form-control" id="map_ip_nic">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2" for="map_ip_mask" msg="掩码">掩码</label>
                    <div class="col-sm-4">
                        <input class="form-control requirement" id="map_ip_mask" placeholder="掩码" reg="^[1-9]\d{0,1}$" reg_tip="只能输入大于0,且最多2位的整数">
                    </div>
                    <label class="control-label col-sm-2" for="map_lv_name">逻辑卷</label>
                    <div class="col-sm-4">
                        <select class="form-control" id="map_lv_name">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2">客户端列表</label>
                    <label class="control-label">
                        <span><a href='#' class="client-add text-large" title="增加客户端"><span class="glyphicon glyphicon-plus"> </span></a></span>
                    </label>
                  </div>
                  <div id="client_add_list">
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="map_add_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="map_add_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>
    
    <div class="modal fade" id="map_update">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">修改Target</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="map_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2" for="map_lun_num" msg="LUN">LUN</label>
                    <div class="col-sm-4">
                        <input class="form-control requirement" id="map_lun_num" placeholder="输入LUN" reg="^\d{1,2}$" reg_tip="只能输入2位以内的数字">
                        <input class="form-control hidden" id="map_ip" >
                        <input class="form-control hidden" id="map_path" >
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-2">客户端列表</label>
                    <label class="control-label">
                        <span><a href='#' class="client-update text-large" title="增加客户端"><span class="glyphicon glyphicon-plus"> </span></a></span>
                    </label>
                  </div>
                  <div id="client_update_list">
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="map_update_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="map_update_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>