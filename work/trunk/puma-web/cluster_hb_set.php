    <div class="modal fade" id="cluster_hb_set">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">心跳IP设置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="hb_set_error_msg"></span>
                    </div>
                  </div>
                  <div class="row stonith-set-panel">
                  <div class="col-sm-6 sep">
                      <div class="form-group">
                        <label class="control-label col-sm-3">主机名称</label>
                        <div class="col-sm-7">
                            <span class="form-control" id="cluster_hb_host_0"></span>
                        </div>
                      </div>
                      <div class="form-group hidden">
                        <label class="control-label col-sm-3" for="cluster_hb_nic_0" msg="网卡">网卡</label>
                        <div class="col-sm-7">
                            <select class="form-control cluster-hb-nic" id="cluster_hb_nic_0"></select>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_hb_ip_0" msg="IP">IP</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_hb_ip_0" placeholder="输入IP" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_hb_mask_0" msg="掩码">掩码</label>
                        <div class="col-sm-7">
                            <input class="form-control" id="cluster_hb_mask_0" placeholder="输入掩码" reg="^\d{1,2}$" reg_tip="只能输入2位以内的数字">
                        </div>
                      </div>
                  </div>
                  <div class="col-sm-6">
                      <div class="form-group">
                        <label class="control-label col-sm-3">主机名称</label>
                        <div class="col-sm-7">
                            <span class="form-control" id="cluster_hb_host_1"></span>
                        </div>
                      </div>
                      <div class="form-group hidden">
                        <label class="control-label col-sm-3" for="cluster_hb_nic_1" msg="网卡">网卡</label>
                        <div class="col-sm-7">
                            <select class="form-control cluster-hb-nic" id="cluster_hb_nic_1"></select>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_hb_ip_1" msg="IP">IP</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_hb_ip_1" placeholder="输入IP" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_hb_mask_1" msg="掩码">掩码</label>
                        <div class="col-sm-7">
                            <input class="form-control" id="cluster_hb_mask_1" placeholder="输入掩码" reg="^\d{1,2}$" reg_tip="只能输入2位以内的数字">
                        </div>
                      </div>
                  </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="cluster_hb_set_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="cluster_hb_set_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>