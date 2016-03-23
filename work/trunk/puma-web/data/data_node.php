<?php    
    require_once "../include/data_util.php";
    require_once "../include/puma-common.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function node_list(){
        $nodes = DataUtil::getNodeList();
        $res = array("result" => $nodes->rc->retcode===0);
        $res["rc"] = $nodes->rc->retcode;
        $htmls = "";
        if($res["result"]){
            foreach($nodes->body->{'pds\mds\get_node_list_response'}->node_infos as $node){
                if(strtolower($node->node_type)=="mds"){
                    continue;
                }
                $op = "";
                // if($node->actual_state){
                    if($node->node_state==NODE_STATE_UNCONFIGED){
                        $op = "<span><a href='#' class='node-init' node-ip='".$node->listen_ip."' node-type='".$node->node_type."'>初始化</a></span>";
                    }else{
                        $op = "<span><a href='#' class='node-drop' logical-id='".$node->logical_id."' node-id='".$node->node_id."' node-type='".$node->node_type."'>删除</a></span>";
                    }
                // }
                if($node->node_state!=NODE_STATE_UNCONFIGED && strtolower($node->node_type)=="ios"){
                    if($node->node_state==NODE_STATE_ONLINE){
                        $op .= " <span><a href='#' class='node-line' line-type='offline' logical-id='".$node->logical_id."' node-type='".$node->node_type."'>offline</a></span>";
                    }else{
                        $op .= " <span><a href='#' class='node-line' line-type='online' logical-id='".$node->logical_id."' node-type='".$node->node_type."'>online</a></span>";
                    }
                }
                $htmls .= "<tr>
                    <td><a href='#' class='node-info' node_id='".$node->logical_id."' node_longid='".$node->node_id."' node_type='".$node->node_type."'>".$node->logical_id."</a></td>
                    <td>".$node->host_name."</td>
                    <td>".$node->node_type."</td>
                    <td>".$node->listen_ip."</td>";
                $htmls .="
                    <td>".($node->node_state==NODE_STATE_ONLINE?"<span class='color_green'>ONLINE</span>":($node->node_state==NODE_STATE_UNCONFIGED?"--":"<span class='color_red'>OFFLINE</span>"))."</td>
                    <td>".($node->actual_state?"<span class='color_green'>ONLINE</span>":"<span class='color_red'>Missing</span>")."</td>";
                $htmls .="
                    <td>$op</td>
                </tr>";
            }
        }else{
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function node_init(){
        $ip = $_REQUEST["ip"];
        $type = $_REQUEST["node_type"];
        $rc = DataUtil::initNode($ip,$type);
        $res = array("result" => $rc->rc->retcode===0);
        $res["rc"] = $rc->rc->retcode;
        if(!$res["result"]){
            $res["error"] = $rc->rc->message;
            Logger::info("add node '$ip' fail");
        }else{
            Logger::info("add node '$ip' success");
        }
        return json_encode($res);
    }
    function node_drop(){
        $nodeid = $_REQUEST["nodeid"];
        $logicalid = $_REQUEST["logicalid"];
        $rc = DataUtil::dropNode($logicalid,$nodeid);
        $res = array("result" => $rc->rc->retcode===0);
        $res["rc"] = $rc->rc->retcode;
        if(!$res["result"]){
            $res["error"] = $rc->rc->message;
            Logger::info("drop node '$logicalid' fail");
        }else{
            Logger::info("drop node '$logicalid' success");
        }
        return json_encode($res);
    }
    function node_offline(){
        $logicalid = $_REQUEST["logicalid"];
        $rc = DataUtil::offlineNode($logicalid);
        $res = array("result" => $rc->rc->retcode===0);
        $res["rc"] = $rc->rc->retcode;
        if(!$res["result"]){
            $res["error"] = $rc->rc->message;
            Logger::info("offline node '$logicalid' fail");
        }else{
            Logger::info("offline node '$logicalid' success");
        }
        return json_encode($res);
    }
    function node_online(){
        $logicalid = $_REQUEST["logicalid"];
        $rc = DataUtil::onlineNode($logicalid);
        $res = array("result" => $rc->rc->retcode===0);
        $res["rc"] = $rc->rc->retcode;
        if(!$res["result"]){
            $res["error"] = $rc->rc->message;
            Logger::info("online node '$logicalid' fail");
        }else{
            Logger::info("online node '$logicalid' success");
        }
        return json_encode($res);
    }
    
    function node_info(){
        $node_id = $_REQUEST["node_id"];
        $nodes = DataUtil::getNodeInfo($node_id);
        $res = array("result" => $nodes->rc->retcode===0);
        $res["rc"] = $nodes->rc->retcode;
        if($res["result"]){
            $nodeinfo = $nodes->body->{'pds\mds\get_node_info_response'}->node_info;
            $data = array(
                "node_info_id"=>$nodeinfo->logical_id,
                "node_info_name"=>$nodeinfo->host_name,
                "node_info_type"=>$nodeinfo->node_type,
                "node_info_ip"=>$nodeinfo->listen_ip,
                "node_info_config"=>($nodeinfo->node_state==NODE_STATE_ONLINE?"<span class='color_green'>ONLINE</span>":($nodeinfo->node_state==NODE_STATE_UNCONFIGED?"--":"<span class='color_red'>NO</span>")),
                "node_info_state"=>($nodeinfo->actual_state?"<span class='color_green'>ONLINE</span>":"<span class='color_red'>Missing</span>")
            );
            $res["data"] = $data;
        }
        return json_encode($res);
    }
    
    function node_list_json(){
        $node_type = $_REQUEST["node_type"];
        $nodes = DataUtil::getNodeList();
        $res = array("result" => $nodes->rc->retcode===0);
        $res["rc"] = $nodes->rc->retcode;
        $result = array();
        if($res["result"]){
            foreach($nodes->body->{'pds\mds\get_node_list_response'}->node_infos as $node){
                if(strtolower($node->node_type)==$node_type && $node->node_state==NODE_STATE_ONLINE){
                    $result[] = array("node_id"=>$node->logical_id,"state"=>$node->actual_state);
                }
            }
        }
        $res["data"] = $result;
        return json_encode($res);
    }
    
    function node_list_filter(){
        $vol_name = $_REQUEST["vol_name"];
        $vol_type = $_REQUEST["vol_type"];
        $retcode = -1;
        $nodes = array();
        $volinfo = DataUtil::getVolInfo($vol_name);
        $retcode = $volinfo->rc->retcode;
        $attach_nodes = array();
        if(isset($volinfo->body->{'pds\mds\get_volume_info_response'}->volume_info->attach_infos)){
            foreach($volinfo->body->{'pds\mds\get_volume_info_response'}->volume_info->attach_infos as $node){
                date_default_timezone_set('Asia/Shanghai');
                $nodes[] = array(
                    "node_name"=>$node->{"pds\mds\ext_attachinfo_bac_node_logical_id"},
                    "node_status"=>$node->actual_state,
                    "node_time"=>$node->last_heartbeat_time<=0?"-":date("Y-m-d H:i:s",$node->last_heartbeat_time));
                $attach_nodes[$node->{"pds\mds\ext_attachinfo_bac_node_logical_id"}] = $node->actual_state;
            }
        }
        if($vol_type=="attach"){
            $nodes = array();
            $ns = DataUtil::getNodeList();
            foreach($ns->body->{'pds\mds\get_node_list_response'}->node_infos as $node){
                if(strtolower($node->node_type)=="bac" && $node->node_state==NODE_STATE_ONLINE && !isset($attach_nodes[$node->logical_id])){
                    date_default_timezone_set('Asia/Shanghai');
                    $nodes[] = array(
                        "node_name"=>$node->logical_id,
                        "node_status"=>$node->actual_state,
                        "node_time"=>$node->last_heartbeat_time<=0?"-":date("Y-m-d H:i:s",$node->last_heartbeat_time));
                }
            }
        }
        
        $res = array("result" => $retcode===0);
        $res["rc"] = $retcode;
        $result = "";
        if($res["result"] && !empty($nodes)){
            $OK = "NORMAL";
            $FL = "UNNORMAL";
            if($vol_type=="attach"){
                $OK = "ONLINE";
                $FL = "Missing";
            }
            foreach($nodes as $node){
                $result .= "<tr>";
                if(!isset($_REQUEST["vol_info"])){
                    $result .= "<td><input type='checkbox' node_name='".$node["node_name"]."'></td>";
                }
                $result .= "<td>".$node["node_name"]."</td>
                    <td>bac</td>
                    <td>".($node["node_status"]?"<span class='color_green'>$OK</span>":"<span class='color_red'>$FL</span>")."</td>
                    <td>".$node["node_time"]."</td>
                </tr>";
            }
        }else{
            $result = nondata($retcode);
        }
        $res["data"] = $result;
        return json_encode($res);
    }
    
?>