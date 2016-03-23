    <div class="modal fade" id="ip_add">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">新增IP</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="lv_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="ip_host">主机</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="ip_host">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="ip_nic">网卡</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="ip_nic">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="ip_name" msg="IP地址">IP地址</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="ip_name" placeholder="输入IP地址" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="ip_mask" msg="掩码">掩码</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="ip_mask" placeholder="输入掩码" reg="^[1-9]\d{0,1}$" reg_tip="只能输入大于0,且最多2位的整数">
                    </div>
                  </div>
                  <div class="form-group hidden net-gateway">
                    <label class="control-label col-sm-3" for="ip_gateway" msg="网关">网关</label>
                    <div class="col-sm-7">
                        <input class="form-control" id="ip_gateway" placeholder="输入网关" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="ip_add_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="net_add_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>