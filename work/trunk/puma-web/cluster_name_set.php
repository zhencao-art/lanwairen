    <div class="modal fade" id="cls_name_set">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">集群名称设置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="cls_name_set_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="cls_name_value" msg="集群名称">集群名称</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="cls_name_value" placeholder="输入集群名称">
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-primary" id="cls_name_set_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="cls_name_set_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>