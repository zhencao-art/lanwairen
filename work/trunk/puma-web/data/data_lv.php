<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function lv_list(){
        $lvs = DataUtil::getLVList();
        // var_dump($lvs);
        $res = array("result" => $lvs->ret->retcode===0);
        $res["rc"] = $lvs->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($lvs->lvs)){
            foreach($lvs->lvs as $lv){
                //lv_uuid
                $ops = "";
                if(empty($lv->lv_used) || !$lv->lv_used){
                    $ops = "<a href='#' class='lv-drop' lv_name='".$lv->lv_name."' vg_name='".$lv->vg_name."'>删除</a>";
                }
                $htmls .= "<tr>
                    <td>".$lv->lv_name."</td>
                    <td>".$lv->vg_name."</td>
                    <td>".(isset($lv->lv_size)?($lv->lv_size." G"):"")."</td>
                    <td>".(isset($lv->lv_used) && $lv->lv_used?"使用中":"<span class='color_green'>未使用</span>")."</td>
                    <td>".(isset($lv->lv_cluster) && $lv->lv_cluster?"集群资源":"<span class='color_red'>非集群资源</span>")."</td>
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
    
    function lv_del(){
        $lv_name = $_REQUEST["lv_name"];
        $vg_name = $_REQUEST["vg_name"];
        $rc = DataUtil::dropLV($vg_name,$lv_name);
        $result = array("result"=>$rc->ret->retcode===0);
        $result["rc"] = $rc->ret->retcode;
        if($result["result"]){
            Logger::info("删除卷 '$vol_name' 成功");
        }else{
            $result["data"] = @$rc->ret->msg;
            Logger::info(isset($result["data"])?$result["data"]:"删除卷 '$vol_name' 失败");
        }
        return json_encode($result);
    }
    function lv_add(){
        $vol_name = $_REQUEST["vol_name"];
        $vol_size = $_REQUEST["vol_size"];
        $vol_vgname = $_REQUEST["vol_vgname"];
        $vol_chunk = $_REQUEST["vol_chunk"];
        $rc = DataUtil::createLV($vol_vgname,$vol_name,$vol_size,$vol_chunk);
        $result = array("result"=>$rc->ret->retcode===0);
        if($result["result"]){
            Logger::info("创建卷 '$vol_name' 成功");
            $result["msg"] = "创建卷 '$vol_name' 成功";
        }else{
            Logger::info("创建卷 '$vol_name' 失败".(isset($rc->ret->msg)?",".$rc->ret->msg:""));
            $result["msg"] = "创建卷 '$vol_name' 失败";
        }
        return json_encode($result);
    }
    function list_lv_json(){
        $lvs = DataUtil::getLVList();
        // var_dump($lvs);
        $res = array("result" => $lvs->ret->retcode===0);
        $res["rc"] = $lvs->ret->retcode;
        $rt = array();
        if($res["result"] && isset($lvs->lvs)){
            foreach($lvs->lvs as $lv){
                if(isset($lv->lv_used) && $lv->lv_used || isset($lv->lv_cluster) && !$lv->lv_cluster){
                    continue;
                }
                $rt[] = array("lv_name"=>"/dev/".$lv->vg_name."/".$lv->lv_name);
            }
        }
        $res["data"] = $rt;
        return json_encode($res);
    }
?>