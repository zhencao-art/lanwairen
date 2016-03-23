<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function map_list(){
        $luns = DataUtil::getLUNList();
        // var_dump($luns);
        $res = array("result" => $luns->ret->retcode===0);
        $res["rc"] = $luns->ret->retcode;
        $htmls = "";
        if($res["result"]){
            $msg = $luns->ret->msg;
            if(!empty($msg)){
                $msg = preg_replace("/\'/","\"",$msg);
                $rs = json_decode($msg);
            }
            // var_dump($rs);
            if(isset($rs)){
                foreach($rs as $lun){
                    $op = "";
                    if(!empty($lun->lun_status)){
                        $op .= "<span><a href='#' class='map-del' ip='".$lun->ip."' path='".$lun->path."' target_id='".$lun->id."'>删除</a></span> ";
                        $op .= "<span><a href='#' class='map-up' lun='".$lun->lun."' ip='".$lun->ip."' path='".$lun->path."' allowed_initiators='".trim(@$lun->allowed_initiators)."'>修改</a></span> ";
                        if(strtolower($lun->lun_status)!="not running"){
                            $op .= "<span><a href='#' class='map-move' cur_host='".trim(@$lun->lun_status)."' target_id='".$lun->id."'>迁移</a></span> ";
                            $op .= "<span><a href='#' class='map-stop' cur_host='".trim(@$lun->lun_status)."' target_id='".$lun->id."'>停用</a></span>";
                        }else{
                            $op .= "<span><a href='#' class='map-check' ip='".$lun->ip."' path='".$lun->path."' target_id='".$lun->id."'>测试</a></span> ";
                            $op .= "<span><a href='#' class='map-start' cur_host='".trim(@$lun->lun_status)."' target_id='".$lun->id."' not_test='true'>启用</a></span>";
                        }
                    }
                    $htmls .= "<tr>
                        <td><a href='#' class='init-lists' target_id='".$lun->id."' allowed_initiators='".trim(@$lun->allowed_initiators)."'>".$lun->target_iqn."</a></td>
                        <td>".$lun->ip."</td>
                        <td>".$lun->lv_name."</td>
                        <td>".$lun->lun."</td>
                        <td>".$lun->lun_status."</td>
                        <td>$op</td>
                    </tr>";
                }
            }
        }
        if(empty($htmls)){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function map_del(){
        $ipaddr = $_REQUEST["ip"];
        $path = $_REQUEST["path"];
        $rt = DataUtil::dropLUN($ipaddr,$path);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("删除Target映射成功");
        }else{
            Logger::info("删除Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_check(){
        $ipaddr = $_REQUEST["ip"];
        $path = $_REQUEST["path"];
        $rt = DataUtil::checkLUN($ipaddr,$path);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("测试Target映射成功");
        }else{
            Logger::info("测试Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_start(){
        $target_id = $_REQUEST["target_id"];
        $rt = DataUtil::startLUN($target_id);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("启用Target映射成功");
        }else{
            Logger::info("启用Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_stop(){
        $target_id = $_REQUEST["target_id"];
        $rt = DataUtil::stopLUN($target_id);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("停用Target映射成功");
        }else{
            Logger::info("停用Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_add(){
        $ipaddr = $_REQUEST["ip_name"];
        $nic = $_REQUEST["ip_nic"];
        $netmask = $_REQUEST["ip_mask"];
        // $iqn = $_REQUEST["tgt_iqn"];
        $allowed_initiators = @$_REQUEST["ini_iqn"];
        $path = $_REQUEST["lv_name"];
        // $allowed_initiators = array(array("iqn"=>"asdfsdf","acess"=>"ro"));
        if(empty($allowed_initiators)){
            $allowed_initiators = array();
        }
        $rt = DataUtil::createLUN($ipaddr,$nic,$netmask,$allowed_initiators,$path);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("新增Target映射成功");
        }else{
            Logger::info("新增Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_update(){
        $lun_num = $_REQUEST["lun_num"];
        $map_ip = $_REQUEST["map_ip"];
        $map_path = $_REQUEST["map_path"];
        $allowed_initiators = $_REQUEST["ini_iqn"];
        if(empty($allowed_initiators)){
            $allowed_initiators = array(array("iqn"=>"","acess"=>""));
        }
        $rt = DataUtil::updateLUN($map_ip,$map_path,$allowed_initiators,$lun_num);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("更新Target映射成功");
        }else{
            Logger::info("更新Target映射失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    
    function map_move(){
        $target_id = $_REQUEST["target_id"];
        $host_name = $_REQUEST["host_name"];
        $rt = DataUtil::moveResource($target_id,$host_name);
        $res = array("result" => $rt->ret->retcode===0);
        $res["msg"] = @$rt->ret->msg;
        if($rt->ret->retcode===0){
            Logger::info("迁移Target映射至节点'$host_name'成功");
        }else{
            Logger::info("迁移Target映射至节点'$host_name'失败,".@$rt->ret->msg);
        }
        return json_encode($res);
    }
    function host_list(){
        $cluster = DataUtil::getClusterState();
        $data = array();
        if($cluster->ret->retcode===0){
            if(isset($cluster->ret->msg)){
                $msg = preg_replace("/\'/","\"",$cluster->ret->msg);
                $clusts = json_decode($msg);
                // var_dump($clusts);
            }
            if(!empty($clusts)){
                foreach($clusts as $i=>$clust){
                    $data[] = array("host_name"=>$clust->uname,"hb"=>$clust->hb_addr);
                }
            }
        }
        $res = array("result" => $cluster->ret->retcode===0);
        $res["data"] = $data;
        return json_encode($res);
    }
?>