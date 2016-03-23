<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function ip_list(){
        $ips = DataUtil::getIPList(null);
        // var_dump($ips);
        $res = array("result" => $ips->ret->retcode===0);
        $res["rc"] = $ips->ret->retcode;
        $htmls = "";
        if($res["result"] && isset($ips->ret->msg)){
            $ipss = json_decode(preg_replace("/\'/","\"",$ips->ret->msg));
            if(!empty($ipss)){
                $hb_ip = array();
                foreach($ipss as $ip){
                    if(isset($ip->status) && $ip->status=="heartbeat"){
                        $hb_ip[$ip->host] = $ip->ip;
                    }
                }
                $hts = array();
                foreach($ipss as $ip){
                    $first_row = false;
                    if(!isset($hts[$ip->host])){
                        $hts[$ip->host] = array("htmls"=>"","count"=>0);
                        $first_row = true;
                    }
                    $op = "";
                    if(isset($ip->status) && $ip->status=="free"){
                        $op .= "<span><a href='#' class='ip-del' ip='".$ip->ip."' nic='".$ip->nic."' netmask='".$ip->mask."' s_ip='".@$hb_ip[$ip->host]."'>删除</a></span>";
                    }
                    $check = "";
                    if(isset($ip->status) && $ip->status=="heartbeat"){
                        // $op .= "<span><a href='#' class='ip-update' ip='".$ip->ip."'>修改</a></span>";
                        $check = " class='check-hb-nic' host='".$ip->host."' ip='".$ip->ip."' nic='".$ip->nic."'";
                    }
                    $hts[$ip->host]["count"] ++;
                    $hts[$ip->host]["htmls"] .= "<tr $check>
                        ".($first_row?"<replace_host_name>":"")."
                        <td>".$ip->nic."</td>
                        <td>".$ip->ip."/".$ip->mask."</td>
                        <td>".$ip->gateway."</td>
                        <td>".(isset($ip->status)?($ip->status=="heartbeat"?"集群IP":"服务IP"):"UNKNOWN")."</td>
                        <td>".(isset($ip->status)?($ip->status=="heartbeat"?"--":($ip->status=="free"?"未使用":"使用中")):"UNKNOWN")."</td>
                        <td>$op</td>
                    </tr>";
                }
                foreach($hts as $host=>$htms){
                    $htmss = preg_replace("<replace_host_name>","<td class='ip-list-cell' rowspan='".$htms["count"]."' style='vertical-align: middle;'>".$host."</td>",$htms["htmls"]);
                    $htmls .= $htmss;
                }
            }
        }
        if(empty($htmls)){
            $htmls = nondata($ips->ret->retcode);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function ip_del(){
        $ip = $_REQUEST["ip"];
        $netmask = $_REQUEST["netmask"];
        $nic = $_REQUEST["nic"];
        $s_ip = $_REQUEST["s_ip"];
        $rc = DataUtil::dropIP($ip,$netmask,$nic,$s_ip);
        $res = array("result" => $rc->ret->retcode===0);
        if($rc->ret->retcode===0){
            Logger::info("删除IP'$ip'成功");
        }else{
            Logger::info("删除IP'$ip'失败,".@$rc->ret->msg);
        }
        return json_encode($res);
    }
    
    function ip_add(){
        $ip = $_REQUEST["ip_name"];
        $netmask = $_REQUEST["ip_mask"];
        $nic = $_REQUEST["ip_nic"];
        $ip_host = $_REQUEST["ip_host"];
        $ip_gateway = $_REQUEST["ip_gateway"];
        $hostip = substr($ip_host,strrpos($ip_host,"_")+1);
        $rc = DataUtil::addIP($ip,$netmask,$nic,$ip_gateway,$hostip);
        $res = array("result" => $rc->ret->retcode===0);
        if($rc->ret->retcode===0){
            Logger::info("新增IP'$ip'成功");
        }else{
            Logger::info("新增IP'$ip'失败,".@$rc->ret->msg);
        }
        return json_encode($res);
    }
    
    function list_nic(){
        $node_ip = @$_REQUEST["node_ip"];
        $flag = @$_REQUEST["flag"];
        if($flag == "local"){
            $node_ip = IP_LOCAL;
        }
        $nics = DataUtil::getNIC($node_ip);
        // var_dump($nics);
        $res = array("result" => $nics->ret->retcode===0);
        $res["rc"] = $nics->ret->retcode;
        $data = array();
        if($res["result"] && isset($nics->ret->msg)){
            $nicss = json_decode(preg_replace("/\'/","\"",$nics->ret->msg));
            if(!empty($nicss)){
                foreach($nicss as $nic){
                    $data[] = array("nic_name"=>$nic->nic,"host_name"=>$nic->host);
                }
            }
        }
        $res["data"] = $data;
        return json_encode($res);
    }
    function list_nic_info(){
        $node_ip = @$_REQUEST["node_ip"];
        $nics = DataUtil::getNICInfo($node_ip);
        // var_dump($nics);
        $res = array("result" => $nics->ret->retcode===0);
        $res["rc"] = $nics->ret->retcode;
        $data = array();
        if($res["result"] && isset($nics->ret->msg)){
            $nicss = json_decode(preg_replace("/\'/","\"",$nics->ret->msg));
            if(!empty($nicss)){
                foreach($nicss as $nic){
                    $data[] = array("nic_name"=>$nic->nic,"mask"=>@$nic->cidr_netmask,"ip"=>@$nic->ip);
                }
            }
        }
        $res["data"] = $data;
        return json_encode($res);
    }
?>