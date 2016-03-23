    <div class="modal fade" id="lv_add">
        <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                <h4 class="modal-title">新增逻辑卷</h4>
              </div>
              <div class="modal-body">
                <form class="form-horizontal" role="form">
                  <div class="form-group has-error">
                    <div class="col-sm-offset-3 col-sm-8">
                      <span class="help-block hide" id="lv_add_error_msg"></span>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="vol_name" msg="逻辑卷名称">逻辑卷名称</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="vol_name" placeholder="输入逻辑卷名称" reg="^[0-9|_|a-z|A-Z]+$" reg_tip="只能输入字母、数字和下划线">
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="vol_vg">存储池</label>
                    <div class="col-sm-7">
                        <select class="form-control" id="vol_vg">
                        </select>
                    </div>
                  </div>
                  <div class="form-group">
                    <label class="control-label col-sm-3" for="vol_size" msg="卷大小(G)">卷大小(G)</label>
                    <div class="col-sm-7">
                        <input class="form-control requirement" id="vol_size" placeholder="输入卷大小(G)" reg="^[1-9]\d{0,7}$" reg_tip="只能输入大于0,且最多8位的整数">
                    </div>
                  </div>
                  <div class="form-group hidden">
                    <label class="control-label col-sm-3" for="vol_chunk" msg="块大小">块大小</label>
                    <div class="col-sm-7">
                        <input class="form-control" id="vol_chunk" placeholder="输入块大小" reg="^[1-9]\d{0,11}$" reg_tip="只能输入大于0,且最多12位的整数">
                    </div>
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <img class="btn-loading hidden" src="img/loading.gif">
                <button type="button" class="btn btn-primary" id="lv_add_btn">保存</button>
                <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
              </div>
            </div>
            <div id="lv_add_loadding">
                <?php include("loading.php"); ?>
            </div>
        </div>
    </div>