<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function vg_list(){
        $vgs = DataUtil::getVGList(true,false,false);
        // var_dump($vgs);
        $res = array("result" => $vgs->ret->retcode===0);
        $res["rc"] = $vgs->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($vgs->vgs)){
            foreach($vgs->vgs as $vg){
                //vg_uuid vg_cur_lv_num
                $ops = "<a href='#' class='vg-opt' vg_opt_type='extend' vg_name='".$vg->vg_name."'>扩展</a>";
                if(empty($vg->vg_cur_lv_num) || $vg->vg_cur_lv_num==0){
                    $ops = "<a href='#' class='vg-drop' vg_name='".$vg->vg_name."'>删除</a> ".$ops;
                }
                if(isset($vg->vg_cur_pv_num) && $vg->vg_cur_pv_num>1){
                    $ops .= " <a href='#' class='vg-opt' vg_opt_type='reduce' vg_name='".$vg->vg_name."'>缩小</a>";
                }
                $htmls .= "<tr>
                    <td><a href='#' class='vg-info' vg_name='".$vg->vg_name."'>".$vg->vg_name."</a></td>
                    <td>".(isset($vg->vg_total_size)?$vg->vg_total_size." G":"")."</td>
                    <td>".(isset($vg->vg_free_size)?$vg->vg_free_size." G":"")."</td>
                    <td>".(isset($vg->vg_cur_pv_num)?$vg->vg_cur_pv_num:"0")."</td>
                    <td>".(isset($vg->vg_cur_lv_num)?$vg->vg_cur_lv_num:"0")."</td>
                    <td>$ops</td>
                </tr>";
            }
        }
        if($htmls == ""){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    function list_vg_json(){
        $vgs = DataUtil::getVGList(false,false,false);
        $res = array("result" => $vgs->ret->retcode===0);
        $res["rc"] = $vgs->ret->retcode;
        $data = array();
        if($res["result"] && isset($vgs->vgs)){
            foreach($vgs->vgs as $vg){
                $data[] = array(
                    "vg_name"=>$vg->vg_name
                );
            }
        }
        $res["data"] = $data;
        return json_encode($res);
    }
    function vg_info(){
        $vg_name = $_REQUEST["vg_name"];
        $vgs = DataUtil::vgInfo($vg_name,true,true);
        $res = array();
        $info = array();
        $lv_list = "";
        $pv_list = "";
        if($vgs->ret->retcode===0){
            $vg = $vgs->vg;
            $info = array(
                "vg_name"=>$vg->vg_name,
                "vg_uuid"=>$vg->vg_uuid,
                "vg_free_size"=>$vg->vg_free_size." G",
                "vg_size"=>$vg->vg_total_size." G",
                "vg_extent_size"=>$vg->vg_extent_size." K",
                "vg_extent_count"=>$vg->vg_extent_count,
                "vg_cur_lv_num"=>@$vg->vg_cur_lv_num,
                "vg_cur_pv_num"=>@$vg->vg_cur_pv_num
            );
            if(!empty($vg->vg_lvs)){
                foreach($vg->vg_lvs as $lv){
                    $lv_list .= "<tr>
                        <td>".$lv->lv_name."</td>
                        <td>".$lv->lv_size." G</td>
                    </tr>";
                }
            }
            if(!empty($vg->vg_pvs)){
                foreach($vg->vg_pvs as $pv){
                    //pv_dev_size
                    //pv_uuid
                    $pv_list .= "<tr>
                        <td>".$pv->pv_name."</td>
                        <td>".@$pv->pv_size." G</td>
                        <td>".@$pv->pv_free_size." G</td>
                        <td>".@$pv->pv_dev_type."</td>
                    </tr>";
                }
            }
        }
        if($lv_list == ""){
            $lv_list = nondata(NON_DATA);
        }
        if($pv_list == ""){
            $pv_list = nondata(NON_DATA);
        }
        $res["info"] = $info;
        $res["lv_list"] = $lv_list;
        $res["pv_list"] = $pv_list;
        return json_encode($res);
    }
    function lv_list_by_vg(){
        $vg_name = $_REQUEST["vg_name"];
        $lv_list = "";
        $res = array();
        $lvs = DataUtil::listLVbyVG($vg_name);
        if($lvs->ret->retcode===0 && isset($lvs->vg_lvs)){   //PV列表
        // var_dump($pvs->vg_pvs);
            foreach($lvs->vg_lvs as $lv){
                $lv_list .= "<tr>
                    <td>".$lv->lv_name."</td>
                    <td>".$lv->lv_uuid."</td>
                    <td>".$lv->lv_size." G</td>
                </tr>";
            }
        }
        if($lv_list == ""){
            $lv_list = nondata($lvs->ret->retcode);
        }
        $res["data"] = $lv_list;
        return json_encode($res);
    }
    function pv_list_by_vg(){
        $vg_name = $_REQUEST["vg_name"];
        $vgs = DataUtil::vgInfo($vg_name,true,false);
        $res = array();
        $pv_list = "";
        if($vgs->ret->retcode===0){
            $vg = $vgs->vg;
            if(!empty($vg->vg_pvs)){
                foreach($vg->vg_pvs as $pv){
                    //pv_uuid
                    $pv_list .= "<tr>
                        <td><span class='glyphicon glyphicon-unchecked' pv-name='".$pv->pv_name."' pv-size='".@$pv->pv_size."' pv-free-size='".@$pv->pv_free_size."'></span></td>
                        <td>".$pv->pv_name."</td>
                        <td>".@$pv->pv_size." G</td>
                        <td>".@$pv->pv_free_size." G</td>
                        <td>".@$pv->pv_dev_type."</td>
                    </tr>";
                }
            }
        }
        if($pv_list == ""){
            $pv_list = nondata($pvs->ret->retcode);
        }
        $res["data"] = $pv_list;
        return json_encode($res);
    }
    
    function raid_list_by_vg(){
        $raid_list = "";
        $res = array();
        $raids = DataUtil::getRaidList(true,false);
        // var_dump($raids);
        if($raids->ret->retcode===0 && isset($raids->md_devices)){
            foreach($raids->md_devices as $raid){
                if(!isset($raid->dev_used) || !$raid->dev_used){
                    $raid_list .= "<tr>
                        <td><span class='glyphicon glyphicon-unchecked' pv-name='".$raid->dev_name."'></span></td>
                        <td>".$raid->dev_name."</td>
                        <td>".transUnit($raid->dev_size,UNIT_K,1,true,LIMIT_G)."</td>
                        <td>".(isset($raid->dev_level)?$raid->dev_level:"")."</td>
                        <td>".(isset($raid->dev_chunk)?transUnit($raid->dev_chunk,UNIT_K,0):"")."</td>
                    </tr>";
                }
            }
        }
        if($raid_list == ""){
            $raid_list = nondata($raids->ret->retcode);
        }
        $res["data"] = $raid_list;
        return json_encode($res);
    }
    function disk_list_by_vg(){
        $disk_list = "";
        $res = array();
        $disks = DataUtil::getDiskList();
        // var_dump($disks);
        if($disks->ret->retcode===0 && isset($disks->disks)){
            foreach($disks->disks as $disk){
                if(!isset($disk->dev_used) || !$disk->dev_used){
                    $disk_list .= "<tr>
                        <td><span class='glyphicon glyphicon-unchecked' pv-name='".$disk->dev_name."'></span></td>
                        <td>".$disk->dev_name."</a></td>
                        <td>".transUnit($disk->dev_size,UNIT_K,0,true,LIMIT_G)."</td>
                        <td>".(isset($disk->dev_slot)?$disk->dev_slot:"")."</td>
                        <td>".(isset($disk->dev_wwn)?$disk->dev_wwn:"")."</td>
                        <td>".(isset($disk->dev_shared)?($disk->dev_shared?"SHARED":"UNSHARED"):"UNKOWN")."</td>
                        <td></td>
                    </tr>";
                }
            }
        }
        if($disk_list == ""){
            $disk_list = nondata($disks->ret->retcode);
        }
        $res["data"] = $disk_list;
        return json_encode($res);
    }
    function vg_opt(){
        $pvs = $_REQUEST["pvs"];
        $vg_name = $_REQUEST["vg_name"];
        $opt = $_REQUEST["opt"];
        $result = array("result"=>false);
        if($opt=="extend"){
            $rc = DataUtil::extendVG($vg_name,$pvs);
        }else{
            $rc = DataUtil::reduceVG($vg_name,$pvs);
        }
        $rd = ($opt=="extend"?"扩展":"缩小")."存储池 '$vg_name' ";
        if($rc->ret->retcode===0){
            $rd .= "成功";
            $rccode = 0;
            Logger::info($rd);
            $result["result"] = true;
        }else{
            $rd .= "失败".(isset($rc->ret->msg)?(",".$rc->ret->msg):"");
            Logger::info($rd);
        }
        $result["data"] = $rd;
        return json_encode($result);
    }
    
    function vg_drop(){
        $vg_name = $_REQUEST["vg_name"];
        $rc = DataUtil::dropVG($vg_name);
        $res = array("result" => $rc->ret->retcode===0);
        $res["rc"] = $rc->ret->retcode;
        if(!$res["result"]){
            $res["error"] = @$rc->ret->msg;
            Logger::info("删除存储池 '$vg_name' 失败,".@$rc->ret->msg);
        }else{
            Logger::info("删除存储池 '$vg_name' 成功");
        }
        return json_encode($res);
    }
    
    function vg_create(){
        $vg_name = $_REQUEST["vg_name"];
        $vg_member = $_REQUEST["vg_member"];
        
        $res = array("result" => false);
        $rc = DataUtil::createVG($vg_name,$vg_member);
        $log = "创建存储池 '$vg_name'";
        if($rc->ret->retcode===0){
            $log .="成功";
            $res["result"] = true;
        }else{
            $log .="失败";
        }
        Logger::info($log.(@$rc->ret->msg?",":"").@$rc->ret->msg);
        $res["error"] = @$rc->ret->msg;
        $res["msg"] = @$rc->ret->msg.(@$rc->ret->msg?",":"").$log;
        return json_encode($res);
    }
    function list_pvs(){
        $vg_name = $_REQUEST["vg_name"];
        $pvs = DataUtil::listPVbyVG($vg_name);
        $res = array("result" => $pvs->ret->retcode===0);
        $res["rc"] = $pvs->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($pvs->vg_pvs)){
            foreach($pvs->vg_pvs as $pv){
                 $htmls .= "<tr pv-name='".$pv->pv_name."' >
                    <td><span class='glyphicon glyphicon-unchecked' pv-name='".$pv->pv_name."'></span></td>
                    <td>".$pv->pv_uuid."</td>
                    <td>".$pv->pv_size."</td>
                    <td>".$pv->pv_free_size."</td>
                    <td>".$pv->pv_dev_size."</td>
                    </tr>";
            }
        }
        return $htmls;
    }

?>