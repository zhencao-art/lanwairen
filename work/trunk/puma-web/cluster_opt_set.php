    <div class="modal fade" id="cls_opt_set">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">集群属性设置</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="cls_opt_set_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3">属性名称</label>
                    <div class="col-sm-7">
                        <span class="form-control" id="cls_opt_name"></span>
                    </div>
                  </div>
                  <div class="form-group hidden">
                    <label class="control-label col-sm-3" for="vol_vg">存储池</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="vol_vg">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="cls_opt_value" msg="属性值">属性值</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="cls_opt_value" placeholder="输入属性值">
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <img class="btn-loading hidden" src="img/loading.gif">
                <button type="button" class="btn btn-primary" id="cls_opt_set_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="cls_opt_set_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>