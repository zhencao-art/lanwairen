<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function cluster_list(){
        $prop = DataUtil::opClusterProperty(CLUSTER_TYPE_CUR,null);
        $res = array("result" => $prop->ret->retcode===0);
        $res["rc"] = $prop->ret->retcode;
        $htmls = "";
        if($prop->ret->retcode===0){
            $props = array();
            if(isset($prop->ret->msg)){
                $msg = preg_replace("/\'/","\"",$prop->ret->msg);
                $propss = json_decode($msg);
                foreach($propss as $p){
                    $props[trim($p->key)] = $p->value;
                }
            }
            if(!empty($props)){
                $htmls .= "<tr>
                            <td>集群名称</td>
                            <td>".$props[KEY_CLUSTER_NAME]."</td>
                            <td><a href='#' cluster_key_name='集群名称' cluster_key='".KEY_CLUSTER_NAME."' cluster_value='".$props[KEY_CLUSTER_NAME]."' class='cls-opt-upt'>修改</a></td>
                        </tr>";
            }
        }
        if(empty($htmls)){
            $htmls = nondata($prop->ret->retcode);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function cluster_name(){
        $prop = DataUtil::getClustName();
        $res = array("result" => $prop->ret->retcode===0);
        $res["rc"] = $prop->ret->retcode;
        $htmls = "";
        // var_dump($prop);
        if($prop->ret->retcode===0){
            if(!empty($prop->ret->msg)){
                $htmls .= "<tr>
                            <td>集群名称</td>
                            <td>".$prop->ret->msg."</td>
                            <td><a href='#' cluster_key_name='集群名称' cluster_key='".KEY_CLUSTER_NAME."' cluster_value='".$prop->ret->msg."' class='cls-name-upt'>修改</a></td>
                        </tr>";
            }
        }
        if(empty($htmls)){
            $htmls = nondata($prop->ret->retcode);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function hb_ip(){
        $htmls = "";
        $cluster = DataUtil::getClusterState();
        if($cluster->ret->retcode===0){
            if(isset($cluster->ret->msg)){
                $msg = preg_replace("/\'/","\"",$cluster->ret->msg);
                $clusts = json_decode($msg);
                // var_dump($clusts);
            }
            if(!empty($clusts)){
                foreach($clusts as $i=>$clust){
                    $htmls .= "<tr class='hb-set-tr' node_name='".$clust->uname."' node_ip='".$clust->hb_addr."'>
                            <td>".$clust->uname."</td>
                            <td>".$clust->hb_addr."</td>
                            <td>".($clust->crmd=="online"?"<span class='color_green'>":"<span class='color_red'>").$clust->crmd."</span>"."</td>";
                    if($i==0){        
                        $htmls .= "<td rowspan='".count($clusts)."' class='cell-v-h'><a href='#' class='cls-hb-upt'>修改</a></td>";
                    }
                    $htmls .= "</tr>";
                }
            }
        }
        
        if(empty($htmls)){
            $htmls = nondata($cluster->ret->retcode);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    function stonith_list(){
        $htmls = "";
        $stonith = DataUtil::getStonithState();
        if($stonith->ret->retcode===0){
            if(isset($stonith->ret->msg)){
                $msg = preg_replace("/\'/","\"",$stonith->ret->msg);
                $stoniths = json_decode($msg);
                // var_dump($stoniths);
            }
            if(!empty($stoniths)){
                foreach($stoniths as $i=>$clust){
                    $host = str_ireplace(STONITH_RES_PRE,"",$clust->id);
                    $htmls .= "<tr class='stonith-set-tr' node_id='".$clust->id."' node_name='".$host."' node_ip='".$clust->ipaddr."' node_uname='".$clust->login."' node_pass='".$clust->passwd."'>
                            <td>".$host."</td>
                            <td>".$clust->ipaddr."</td>
                            <td>".$clust->login."</td>
                            <td>".$clust->passwd."</td>";
                            
                    if($i==0){        
                        if(empty($clust->node_state) || strtolower($clust->node_state)=="not running"){
                            $dis_enable = "<a href='#' class='cls-stonith-enable' is-exist='true'>启用</a>";
                            $able = "<span class='color_red'>已禁用</span>";
                        }else{
                            $dis_enable = "<a href='#' class='cls-stonith-disable'>禁用</a>";
                            $able = "<span class='color_green'>已启用</span>";
                        }
                        $htmls .= "<td rowspan='".count($stoniths)."' class='cell-v-h'>".$able."</td>
                                <td rowspan='".count($stoniths)."' class='cell-v-h'>".$dis_enable." <a href='#' class='cls-stonith-up'>修改</a></td>";
                    }
                    $htmls .= "</tr>";
                }
            }
        }
        if(empty($htmls)){
            $htmls = "";
            $cluster = DataUtil::getClusterState();
            if($cluster->ret->retcode===0){
                if(isset($cluster->ret->msg)){
                    $msg = preg_replace("/\'/","\"",$cluster->ret->msg);
                    $clusts = json_decode($msg);
                    // var_dump($clusts);
                }
                if(!empty($clusts)){
                    foreach($clusts as $i=>$clust){
                        $htmls .= "<tr class='stonith-set-tr' node_id='' node_name='".$clust->uname."'>
                                <td>".$clust->uname."</td>
                                <td>--</td>
                                <td>--</td>
                                <td>--</td>
                                <td>--</td>";
                        if($i==0){        
                            $htmls .= "<td rowspan='".count($clusts)."' class='cell-v-h'><a href='#' class='cls-stonith-enable'>启用</a></td>";
                        }
                        $htmls .= "</tr>";
                    }
                }
            }
        }
        if(empty($htmls)){
            $htmls = nondata($cluster->ret->retcode);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function set_cluster(){
        $key = $_REQUEST["key"];
        $value = $_REQUEST["value"];
        $opts = array();
        $opts[] = array("pName"=>$key,"pValue"=>$value);
        $prop = DataUtil::opClusterProperty(CLUSTER_TYPE_SET,$opts);
        $res = array("result" => $prop->ret->retcode===0);
        if($prop->ret->retcode===0){
            $res["msg"] = "设置集群属性成功";
            Logger::info("设置集群属性成功");
        }else{
            $res["msg"] = "设置集群属性失败,".@$prop->ret->msg;
            Logger::info("设置集群属性失败,".@$prop->ret->msg);
        }
        return json_encode($res);
    }
    
    function set_cluster_name(){
        $name = $_REQUEST["name"];
        $prop = DataUtil::setClusterName($name);
        $res = array("result" => $prop->ret->retcode===0);
        if($prop->ret->retcode===0){
            $res["msg"] = "设置集群名称成功";
            Logger::info("设置集群名称成功");
        }else{
            $res["msg"] = "设置集群名称失败,".@$prop->ret->msg;
            Logger::info("设置集群名称失败,".@$prop->ret->msg);
        }
        return json_encode($res);
    }
    
    function able_stonith(){
        $key = $_REQUEST["key"];
        $value = $_REQUEST["value"];
        $opts = array();
        $opts[] = array("pName"=>$key,"pValue"=>$value);
        $prop = DataUtil::opClusterProperty(CLUSTER_TYPE_SET,$opts);
        $res = array("result" => $prop->ret->retcode===0);
        if($prop->ret->retcode===0){
            $res["msg"] = "设置集群属性成功";
            Logger::info("设置集群属性成功");
        }else{
            $res["msg"] = "设置集群属性失败,".@$prop->ret->msg;
            Logger::info("设置集群属性失败,".@$prop->ret->msg);
        }
        return json_encode($res);
    }
    
    function set_stonith(){
        $sth_type = $_REQUEST["sth_type"];
        $ipmis = $_REQUEST["ipmis"];
        $attrs = array();
        foreach($ipmis as $ipmi){
            $ii = array(
                "host"=>$ipmi["host"],
                "ip"=>$ipmi["ip"],
                "username"=>$ipmi["uname"],
                "passwd"=>$ipmi["pass"]
            );
            if(isset($ipmi["sid"])){
                $ii["id"] = $ipmi["sid"];
            }
            $attrs[] = $ii;
        }
        $tip = "";
        if($sth_type == "update"){
            $tip = "更新IPMI";
            $sth = DataUtil::updateStonithState($attrs);
        }else if($sth_type == "enable"){
            $tip = "启用脑裂";
            $sth = DataUtil::enableStonithState($attrs);
        }else{
            $tip = "禁用脑裂";
            $sth = DataUtil::disableStonithState($attrs);
        }
        $res = array("result" => $sth->ret->retcode===0);
        if($sth->ret->retcode===0){
            $res["msg"] = $tip."成功";
            Logger::info($tip."成功");
        }else{
            $res["msg"] = $tip."失败,".@$sth->ret->msg;
            Logger::info($tip."失败,".@$sth->ret->msg);
        }
        return json_encode($res);
    }
    
    function set_hb(){
        $ips = $_REQUEST["ips"];
        $pass = @$_REQUEST["pass"];
        $hb1 = array(
            "hb"=>$ips[0]["ip"],
            "host"=>$ips[0]["host"],
            "nic"=>$ips[0]["nic"]
        );
        if(isset($ips[0]["mask"])){
            $hb1["cidr_netmask"] = $ips[0]["mask"];
        }
        $hb2 = array(
            "hb"=>$ips[1]["ip"],
            "host"=>$ips[1]["host"],
            "nic"=>$ips[1]["nic"]
        );
        if(isset($ips[1]["mask"])){
            $hb2["cidr_netmask"] = $ips[1]["mask"];
        }
        $sth = DataUtil::setHB($hb1,$hb2,$pass);
        $res = array("result" => $sth->ret->retcode===0);
        if($sth->ret->retcode===0){
            $res["msg"] = "设置心跳IP成功";
            Logger::info("设置心跳IP成功");
        }else{
            $res["msg"] = "设置心跳IP失败,".@$sth->ret->msg;
            Logger::info("设置心跳IP失败,".@$sth->ret->msg);
        }
        return json_encode($res);
    }
    function cluster_start(){
        $cls = DataUtil::startCluster();
        $res = array("result" => $cls->ret->retcode===0);
        if($cls->ret->retcode===0){
            $res["msg"] = "启动集群成功";
            Logger::info("启动集群成功");
        }else{
            $res["msg"] = "启动集群失败,".@$cls->ret->msg;
            Logger::info("启动集群失败,".@$cls->ret->msg);
        }
        return json_encode($res);
    }
    function cluster_stop(){
        $cls = DataUtil::stopCluster();
        $res = array("result" => $cls->ret->retcode===0);
        if($cls->ret->retcode===0){
            $res["msg"] = "关闭集群成功";
            Logger::info("关闭集群成功");
        }else{
            $res["msg"] = "关闭集群失败,".@$cls->ret->msg;
            Logger::info("关闭集群失败,".@$cls->ret->msg);
        }
        return json_encode($res);
    }
?>