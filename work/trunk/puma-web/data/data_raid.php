<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function raid_list(){
        $raids = DataUtil::getRaidList(true,false);
        // var_dump($raids);
        $res = array("result" => $raids->ret->retcode===0);
        $res["rc"] = $raids->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($raids->md_devices)){
            foreach($raids->md_devices as $raid){
                $ops = "";
                if(empty($raid->dev_used) || !$raid->dev_used){
                    $ops = "<a href='#' class='raid-drop' raid_name='".$raid->dev_name."'>删除</a>";
                }
                $htmls .= "<tr>
                    <td><a href='#' class='raid-info' raid_name='".$raid->dev_name."'>".$raid->dev_name."</a></td>
                    <td>".transUnit($raid->dev_size,UNIT_K,1,true,LIMIT_G)."</td>
                    <td>".(isset($raid->dev_level)?$raid->dev_level:"")."</td>
                    <td>".(isset($raid->dev_chunk)?transUnit($raid->dev_chunk,UNIT_K,0):"-")."</td>
                    <td>".(isset($raid->raid_disks)?$raid->raid_disks:"")."</td>
                    <td>".(isset($raid->dev_used) && $raid->dev_used?"使用中":"<span class='color_green'>未使用</span>")."</td>
                    <td>$ops</td>
                </tr>";
            }
        }
        if($htmls==""){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function raid_info(){
        $raid_name = $_REQUEST["raid_name"];
        $raids = DataUtil::getRaidList(true,true);
        // var_dump($raids);
        $res = array("result" => $raids->ret->retcode===0);
        $res["rc"] = $raids->ret->retcode;
        $data = array();
        $htmls = "";
        if($res["result"] && isset($raids->md_devices)){
            foreach($raids->md_devices as $raid){
                if($raid->dev_name == $raid_name){
                    $data["raid_info_name"] = $raid->dev_name;
                    $data["raid_info_size"] = transUnit($raid->dev_size,UNIT_K,1,true,LIMIT_G);
                    $data["raid_info_type"] = $raid->dev_level;
                    $data["raid_info_chunk"] = isset($raid->dev_chunk)?transUnit($raid->dev_chunk,UNIT_K,0):"-";
                    $data["raid_info_status"] = @$raid->raid_stat;
                    if(isset($raid->dev_phy_devices)){
                        foreach($raid->dev_phy_devices as $device){
                            $slot = isset($device->dev->dev_slot)?$device->dev->dev_slot:"";
                            $flag_idx = strpos($slot,":");
                            $slot = $flag_idx || $flag_idx===0?substr($slot,$flag_idx+1):$slot;
                            $htmls .="<tr>
                                <td>".(isset($device->dev) && isset($device->dev->dev_name)?$device->dev->dev_name:"")."</td>
                                <td>".(isset($device->dev) && isset($device->dev->dev_size)?transUnit($device->dev->dev_size,UNIT_K,0,true,LIMIT_G):"")."</td>
                                <td>".$slot."</td>
                                <td>".(isset($device->dev) && isset($device->dev->dev_wwn)?$device->dev->dev_wwn:"")."</td>
                            </tr>";
                        }
                    }
                    break;
                }
            }
        }
        if($htmls==""){
            $htmls = nondata(null);
        }
        $res["data"] = $data;
        $res["disks"] = $htmls;
        return json_encode($res);
    }
    
    function raid_drop(){
        $raid_name = $_REQUEST["raid_name"];
        $rc = DataUtil::dropRaid(str_ireplace("/dev/","",$raid_name));
        $res = array("result" => $rc->ret->retcode===0);
        $res["rc"] = $rc->ret->retcode;
        if(!$res["result"]){
            $res["error"] = $rc->ret->msg;
            Logger::info("删除RAID '$raid_name' 失败,".@$rc->ret->msg);
        }else{
            Logger::info("删除RAID '$raid_name' 成功");
        }
        return json_encode($res);
    }
    
    function raid_create(){
        $raid_name = $_REQUEST["raid_name"];
        $raid_type = $_REQUEST["raid_type"];
        $raid_stripe = $_REQUEST["raid_stripe"];
        $raid_disk = $_REQUEST["raid_disk"];
        $raid_name = $raid_name;
        $res = array("result" => false);
        $rc = DataUtil::createRaid($raid_name,$raid_type,$raid_stripe,$raid_disk);
        $log = "创建RAID '$raid_name'";
        if($rc->ret->retcode===0){
            $log .= " 成功";
            $res["result"] = true;
        }else{
            $log .= " 失败".(@$rc->ret->msg?",":"").@$rc->ret->msg;
        }
        Logger::info($log);
        $res["error"] = @$rc->ret->msg;
        $res["msg"] = $log;
        return json_encode($res);
    }
    
    function raid_list_for_vging(){
        $raids = DataUtil::getRaidList(true,false);
        // var_dump($disks);
        $res = array("result" => $raids->ret->retcode===0);
        $res["rc"] = $raids->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($raids->md_devices)){
            foreach($raids->md_devices as $raid){
                if(!isset($raid->dev_used) || $raid->dev_used){
                    continue;
                }
                $htmls .= "<tr raid-name='".$raid->dev_name."' >
                    <td><span class='glyphicon glyphicon-unchecked' raid-name='".$raid->dev_name."'></span></td>
                    <td>".$raid->dev_name."</td>
                    <td>".transUnit($raid->dev_size,UNIT_K,1,true,LIMIT_G)."</td>
                    <td>".(isset($raid->dev_level)?$raid->dev_level:"")."</td>
                    <td>".(isset($raid->dev_chunk)?$raid->dev_chunk:"")."</td>
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