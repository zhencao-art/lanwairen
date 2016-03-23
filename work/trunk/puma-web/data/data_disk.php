<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function disk_list(){
        $disks = DataUtil::getDiskList();
        $slots = DataUtil::getBackBoardInfo();
        // var_dump($disks);
        $res = array("result" => $disks->ret->retcode===0);
        $res["rc"] = $disks->ret->retcode;
        $used_count = 0;
        $all_count = 0;
        $htmls = "";
        if($res["result"]){
            $used_count = count($disks->disks);
            foreach($disks->disks as $disk){
                $slot = isset($disk->dev_slot)?$disk->dev_slot:"";
                $flag_idx = strpos($slot,":");
                $slot = $flag_idx || $flag_idx===0?substr($slot,$flag_idx+1):$slot;
                $htmls .= "<tr>
                    <td>".$disk->dev_name."</td>
                    <td>".transUnit($disk->dev_size,UNIT_K,0,true,LIMIT_G)."</td>
                    <td>".$slot."</td>
                    <td>".(isset($disk->dev_wwn)?$disk->dev_wwn:"")."</td>
                    <td>".(isset($disk->dev_shared)?($disk->dev_shared?"SHARED":"UNSHARED"):"UNKOWN")."</td>
                    <td>".(isset($disk->rotational)?($disk->rotational===0?"SSD":"HDD"):"UNKOWN")."</td>
                    <td>".(isset($disk->dev_used) && $disk->dev_used?"使用中":"<span class='color_green'>未使用</span>")."</td>
                </tr>";
            }
        }
        if($slots->ret->retcode===0){
            $all_count = @$slots->backboard_info->slot_num;
        }
        if($htmls==""){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        $res["used_count"] = $used_count;
        $res["all_count"] = $all_count;
        return json_encode($res);
    }
    
    function disk_list_for_raiding(){
        $node_id = "";
        $disks = DataUtil::getDiskList();
        $res = array("result" => $disks->ret->retcode===0);
        $res["rc"] = $disks->ret->retcode;
        $htmls = "";
        if($res["result"]){
            foreach($disks->disks as $disk){
                if(!isset($disk->dev_shared) || !$disk->dev_shared || !isset($disk->dev_used) || $disk->dev_used){
                    continue;
                }
                $htmls .= "<tr disk-name='".$disk->dev_name."' >
                    <td><span class='glyphicon glyphicon-unchecked' disk-name='".$disk->dev_name."'></span></td>
                    <td>".$disk->dev_name."</td>
                    <td>".transUnit($disk->dev_size,UNIT_K,0,true,LIMIT_G)."</td>
                    <td>".(isset($disk->dev_shared)?($disk->dev_shared?"SHARED":"UNSHARED"):"UNKOWN")."</td>
                </tr>";
            }
        }
        if($htmls==""){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function disk_list_for_vging(){
        $node_id = "";
        $disks = DataUtil::getDiskList();
        $res = array("result" => $disks->ret->retcode===0);
        $res["rc"] = $disks->ret->retcode;
        $htmls = "";
        if($res["result"]){
            foreach($disks->disks as $disk){
                if(!isset($disk->dev_shared) || !$disk->dev_shared || !isset($disk->dev_used) || $disk->dev_used){
                    continue;
                }
                $htmls .= "<tr disk-name='".$disk->dev_name."' >
                    <td><span class='glyphicon glyphicon-unchecked' disk-name='".$disk->dev_name."'></span></td>
                    <td>".$disk->dev_name."</td>
                    <td>".transUnit($disk->dev_size,UNIT_k,0,true,LIMIT_G)."</td>
                    <td>".(isset($disk->dev_shared)?($disk->dev_shared?"SHARED":"UNSHARED"):"UNKOWN")."</td>
                </tr>";
            }
        }
        if($htmls==""){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
?>