    <div class="modal fade" id="cluster_stonith_set">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">IPMI设置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="stonith_set_error_msg"></span>
                    </div>
                  </div>
                  <div class="row stonith-set-panel">
                  <div class="col-sm-6 sep">
                      <div class="form-group">
                        <label class="control-label col-sm-3">主机名称</label>
                        <div class="col-sm-7">
                            <span class="form-control" id="cluster_stonith_host_0"></span>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_ip_0" msg="IP">IP</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_ip_0" placeholder="输入IP" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_uname_0" msg="用户名">用户名</label>
                        <div class="col-sm-7">
                            <input class="form-control hidden" id="cluster_stonith_nodeid_0" />
                            <input class="form-control requirement" id="cluster_stonith_uname_0" placeholder="输入用户名" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_pass_0" msg="密码">密码</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_pass_0" placeholder="输入密码" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_repass_0" msg="确认密码">确认密码</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_repass_0" placeholder="输入确认密码" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                  </div>
                  <div class="col-sm-6">
                      <div class="form-group">
                        <label class="control-label col-sm-3">主机名称</label>
                        <div class="col-sm-7">
                            <span class="form-control" id="cluster_stonith_host_1"></span>
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_ip_1" msg="IP">IP</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_ip_1" placeholder="输入IP" reg="^((25[0-5]|2[0-4]\d|[01]?\d\d?)($|(?!\.$)\.)){4}$" reg_tip="格式不正确">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_uname_1" msg="用户名">用户名</label>
                        <div class="col-sm-7">
                            <input class="form-control hidden" id="cluster_stonith_nodeid_1" />
                            <input class="form-control requirement" id="cluster_stonith_uname_1" placeholder="输入用户名" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_pass_1" msg="密码">密码</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_pass_1" placeholder="输入密码" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                      <div class="form-group">
                        <label class="control-label col-sm-3" for="cluster_stonith_repass_1" msg="确认密码">确认密码</label>
                        <div class="col-sm-7">
                            <input class="form-control requirement" id="cluster_stonith_repass_1" placeholder="输入确认密码" reg="^[0-9|a-z|A-Z|_]{1,12}$" reg_tip="只能输入12位以内的数字、字母或下划线">
                        </div>
                      </div>
                  </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="cluster_stonith_set_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="cluster_stonith_set_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>