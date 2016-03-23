<?php 
    include_once "logger.php";
    include_once "puma-common.php";
    
    define("IP_LOCAL","local");
    
    define("TYPE_DISK","Physical Disk");
    
    define("CLUSTER_TYPE_CUR","");
    define("CLUSTER_TYPE_ALL","all");
    define("CLUSTER_TYPE_DEF","default");
    define("CLUSTER_TYPE_SET","set");
    define("CLUSTER_TYPE_UNSET","unset");
    
    define("KEY_CLUSTER_NAME","cluster-name");
    define("STONITH_RES_PRE","fencing_ipmi_");
    
    define("LUN_RULE_RO","ro");
    define("LUN_RULE_RW","rw");
    
    class DataUtil{
        public static function getDiskList($node_ip=""){
            $param = array("method"=>"cluster_list_phy_disk","param"=>array("node_ip"=>"$node_ip"));
            return DataUtil::request($param);
        }
        public static function getBackBoardInfo(){
            $param = array("method"=>"get_backboard_info","param"=>array());
            return DataUtil::request($param);
        }
        
        public static function getRaidList($md_detail=false,$pv_detail=false){
            $param = array("method"=>"scan_md_device","param"=>array("detail"=>$md_detail,"p_detail"=>$pv_detail));
            return DataUtil::request($param);
        }
        public static function dropRaid($raid_name,$rm_crashing=true){
            $param = array("method"=>"remove_md_device","param"=>array("md_name"=>$raid_name,"rm_crashing"=>$rm_crashing));
            return DataUtil::request($param);
        }
        public static function createRaid($raid_name,$raid_level,$raid_chunk,$dev_names){
            $md_phy_devices = array();
            foreach($dev_names as $dev_name){
                $md_phy_devices[] = array("dev_name"=>$dev_name);
            }
            $param = array("method"=>"create_md_device",
                "param"=>array(
                    "md_name"=>$raid_name,
                    "md_level"=>$raid_level,
                    "md_chunk"=>$raid_chunk,
                    "md_phy_devices"=>$md_phy_devices
                ));
            return DataUtil::request($param);
        }
        
        public static function getVGList($vg_detail=false,$lv_detail=false,$pv_detail=false){
            $param = array("method"=>"scan_lvm_vg","param"=>array("vg"=>$vg_detail,"lv"=>$lv_detail,"pv"=>$pv_detail));
            return DataUtil::request($param);
        }
        public static function dropVG($vg_name,$crashing=true){
            $param = array("method"=>"remove_lvm_vg","param"=>array("vg_name"=>$vg_name,"crashing"=>$crashing));
            return DataUtil::request($param);
        }
        public static function createVG($vg_name,$pv_names){
            $vg_pvs = array();
            foreach($pv_names as $pv_name){
                $vg_pvs[] = array("pv_name"=>$pv_name);
            }
            $param = array("method"=>"create_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "vg_pvs"=>$vg_pvs
                ));
            return DataUtil::request($param);
        }
        public static function extendVG($vg_name,$pv_names){
            $vg_pvs = array();
            foreach($pv_names as $pv_name){
                $vg_pvs[] = array("pv_name"=>$pv_name);
            }
            $param = array("method"=>"add_pv_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "vg_pvs"=>$vg_pvs
                ));
            return DataUtil::request($param);
        }
        public static function reduceVG($vg_name,$pv_names,$crashing=true){
            $vg_pvs = array();
            foreach($pv_names as $pv_name){
                $vg_pvs[] = array("pv_name"=>$pv_name);
            }
            $param = array("method"=>"del_pv_lvm_vg",
                "param"=>array(
                    "crashing"=>$crashing,
                    "vg_name"=>$vg_name,
                    "vg_pvs"=>$vg_pvs
                ));
            return DataUtil::request($param);
        }
        public static function listPVbyVG($vg_name){
            $param = array("method"=>"scan_pv_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                ));
            return DataUtil::request($param);
        }
        public static function vgInfo($vg_name,$pv=false,$lv=false){
            $param = array("method"=>"find_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "pv"=>$pv,
                    "lv"=>$lv
                ));
            return DataUtil::request($param);
        }
        
        public static function createLV($vg_name,$lv_name,$lv_size,$chunk_size,$lv_type="linear",$size_unit="G"){
            $param = array("method"=>"create_lv_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "lv_name"=>$lv_name,
                    "lv_size"=>$lv_size,
                    "size_unit"=>$size_unit,
                    "lv_type"=>$lv_type
                ));
            if(!empty($chunk_size)){
                $param["param"]["chunk_size"] = $chunk_size;
            }
            return DataUtil::request($param);
        }
        public static function dropLV($vg_name,$lv_name,$all_flag=false){
            $param = array("method"=>"remove_lv_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "lv_name"=>$lv_name,
                    "all_flag"=>$all_flag
                ));
            return DataUtil::request($param);
        }
        public static function listLVbyVG($vg_name){
            $param = array("method"=>"scan_lv_lvm_vg",
                "param"=>array(
                    "vg_name"=>$vg_name,
                ));
            return DataUtil::request($param);
        }
        public static function getLVList(){
            $param = array("method"=>"scan_lv_lvm","param"=>array());
            return DataUtil::request($param);
        }
        public static function extendLV($vg_name,$lv_name,$lv_size,$size_unit="M"){
            $param = array("method"=>"extend_lv_lvm",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "lv_name"=>$lv_name,
                    "lv_size"=>$lv_size,
                    "size_unit"=>$size_unit
                ));
            return DataUtil::request($param);
        }
        public static function reduceLV($vg_name,$lv_name,$lv_size,$size_unit="M"){
            $param = array("method"=>"reduce_lv_lvm",
                "param"=>array(
                    "vg_name"=>$vg_name,
                    "lv_name"=>$lv_name,
                    "lv_size"=>$lv_size,
                    "size_unit"=>$size_unit
                ));
            return DataUtil::request($param);
        }
        
        public static function getLUNList(){
            $param = array("method"=>"get_lun","param"=>array());
            return DataUtil::request($param);
        }
        public static function createLUN($ipaddr,$nic,$netmask,$allowed_initiators,$path){
            $param = array("method"=>"add_lun","param"=>array(
                "ip"=>array(
                    "ip"=>$ipaddr
                ),
                "tgt"=>array(
                    // "tid"=>"",
                    // "portals"=>"",
                    // "additional_parameters"=>array(),
                    // "acls_parameters"=>array(),
                    // "incoming_username"=>"",
                    // "incoming_password"=>"",
                    // "allowed_initiators"=>$allowed_initiators
                ),
                "lu"=>array(
                    "path"=>$path,
                    // "lun"=>"",
                    "allowed_initiators"=>$allowed_initiators
                )
            ));
            if(!empty($nic)){
                $param["param"]["ip"]["nic"] = $nic;
            }
            if(!empty($netmask)){
                $param["param"]["ip"]["cidr_netmask"] = $netmask;
            }
            // if(!empty($iqn)){
                // $param["param"]["tgt"]["iqn"] = $iqn;
                // $param["param"]["lu"]["target_iqn"] = $iqn;
            // }
            return DataUtil::request($param);
        }
        public static function updateLUN($ipaddr,$path,$allowed_initiators,$lun){
            $param = array("method"=>"update_lun","param"=>array(
                "ip"=>array(
                    "ip"=>$ipaddr
                ),
                "tgt"=>array(
                    // "iqn"=>$iqn,
                    // "tid"=>"",
                    // "portals"=>"",
                    // "additional_parameters"=>array(),
                    // "acls_parameters"=>array(),
                    // "incoming_username"=>"",
                    // "incoming_password"=>"",
                    // "allowed_initiators"=>$allowed_initiators
                ),
                "lu"=>array(
                    "path"=>$path,
                    // "target_iqn"=>$iqn,
                    "lun"=>$lun,
                    "allowed_initiators"=>$allowed_initiators
                )
            ));
            // if(!empty($allowed_initiators)){
                // $param["param"]["lu"]["allowed_initiators"] = $allowed_initiators;
            // }
            return DataUtil::request($param);
        }
        public static function checkLUN($ipaddr,$path){
            $param = array("method"=>"check_lun","param"=>array(
                    "ip"=>$ipaddr,
                    "device_path"=>$path
            ));
            return DataUtil::request($param);
        }
        public static function dropLUN($ipaddr,$path){
            $param = array("method"=>"delete_lun","param"=>array("ip"=>"$ipaddr","device_path"=>"$path"));
            return DataUtil::request($param);
        }
        public static function stopLUN($id){
            $param = array("method"=>"stop_cluster_resource","param"=>array("resName"=>"$id","isStop"=>true));
            return DataUtil::request($param);
        }
        public static function startLUN($id){
            $param = array("method"=>"stop_cluster_resource","param"=>array("resName"=>"$id","isStop"=>false));
            return DataUtil::request($param);
        }
        
        public static function getNICInfo($ipaddr=IP_LOCAL){
            $param = array("method"=>"get_nic_info","param"=>array());
            if(!empty($ipaddr)){
                $param["param"]["node"]=$ipaddr;
            }
            return DataUtil::request($param);
        }
        public static function getNIC($ipaddr=IP_LOCAL){
            $param = array("method"=>"get_nic","param"=>array());
            if(!empty($ipaddr)){
                $param["param"]["node"]=$ipaddr;
            }
            return DataUtil::request($param);
        }
        public static function getIPList($ipaddr=IP_LOCAL){
            $param = array("method"=>"get_ip","param"=>array());
            if(isset($ipaddr)){
                $param["param"]["node"]=$ipaddr;
            }
            return DataUtil::request($param);
        }
        public static function addIP($ip,$netmask,$nic,$gateway,$node=IP_LOCAL){
            $param = array("method"=>"add_ip",
                "param"=>array(
                    "node"=>"$node",
                    "ipOpt"=>array(
                        "ip"=>$ip,
                        "nic"=>$nic,
                        "gate_way"=>$gateway,
                        "cidr_netmask"=>$netmask
                    )
                ));
            return DataUtil::request($param);
        }
        public static function dropIP($ip,$netmask,$nic,$node=IP_LOCAL){
            $param = array("method"=>"delete_ip",
                "param"=>array(
                    "node"=>"$node",
                    "ipOpt"=>array(
                        "ip"=>$ip,
                        "nic"=>$nic,
                        "cidr_netmask"=>$netmask
                    )
                ));
            return DataUtil::request($param);
        }
        
        public static function getClusterState($detail_flag=false){
            $param = array("method"=>"get_cluster_state","param"=>array());
            if($detail_flag){
                $param["param"]["detail_flag"] = true;
            }
            return DataUtil::request($param);
        }
        public static function opClusterProperty($type="set",$opts){
            //unset|set   |default|all 
            if(empty($opts)){
                $opts = array();
            }
            $param = array("method"=>"set_property_cluster","param"=>array("code"=>$type,"opt"=>$opts));
            return DataUtil::request($param);
        }
        public static function setClusterName($clustName){
            $param = array("method"=>"set_cluster_name","param"=>array("cluster_name"=>$clustName));
            return DataUtil::request($param);
        }
        public static function getClustName(){
            $param = array("method"=>"get_cluster_name","param"=>array());        
            return DataUtil::request($param);
        }
        
        public static function getStonithState(){
            $param = array("method"=>"get_stonith_ipmi","param"=>array());
            return DataUtil::request($param);
        }
        public static function enableStonithState($attrs){
            $param = array("method"=>"enable_stonith_ipmi","param"=>array("attr"=>$attrs));        
            return DataUtil::request($param);
        }
        public static function updateStonithState($attrs){
            $param = array("method"=>"update_stonith_ipmi","param"=>array("attr"=>$attrs));        
            return DataUtil::request($param);
        }
        public static function disableStonithState($attrs){
            $param = array("method"=>"disable_stonith_ipmi","param"=>array("attr"=>$attrs));        
            return DataUtil::request($param);
        }
        
        public static function moveResource($resId,$toNode){
            $param = array("method"=>"move_cluster_resource","param"=>array("resName"=>$resId,"cluNode"=>$toNode));        
            return DataUtil::request($param);
        }
        public static function setHB($hb1,$hb2,$passwd=""){
            $param = array("method"=>"set_heartbeat","param"=>array("hb1"=>$hb1,"hb2"=>$hb2));   
            if(!empty($passwd)){
                $param["param"]["passwd"] = $passwd;
            }
            return DataUtil::request($param);
        }
        
        public static function getNTPState(){
            $param = array("method"=>"cluster_ntp_get_conf","param"=>array());        
            return DataUtil::request($param);
        }
        public static function getCurrentDT(){
            $param = array("method"=>"get_current_time","param"=>array());        
            return DataUtil::request($param);
        }
        public static function getCurrentTZ(){
            $param = array("method"=>"get_current_tz","param"=>array());        
            return DataUtil::request($param);
        }
        public static function getAllTZ(){
            $param = array("method"=>"list_timezone","param"=>array());        
            return DataUtil::request($param);
        }
        public static function setTZAndNTP($tz,$ip,$url){
            $param = array("method"=>"cluster_ntp_setup","param"=>array("timezone"=>$tz,"node_ip"=>$ip,"public_url"=>$url));        
            return DataUtil::request($param);
        }
        public static function setTZ($tz,$time){
            self::setTimezone($tz);
            $t = array(
                "year"=>substr($time,0,4),
                "mon"=>substr($time,5,2),
                "day"=>substr($time,8,2),
                "hour"=>substr($time,11,2),
                "min"=>substr($time,14,2),
                "sec"=>substr($time,17,2),
                "wday"=>"0"
            );
            $param = array("method"=>"set_time","param"=>array("time"=>$t));        
            return DataUtil::request($param);
        }
        public static function setTimezone($tz){
            $param = array("method"=>"set_timezone","param"=>array("tz"=>array("tz"=>$tz)));        
            return DataUtil::request($param);
        }
        
        public static function startCluster($node=""){
            $param = array("method"=>"start_cluster","param"=>array());        
            if(!empty($node)){
                $param["param"]["node"] = $node;
            }
            return DataUtil::request($param);
        }
        public static function stopCluster($node=""){
            $param = array("method"=>"stop_cluster","param"=>array());        
            if(!empty($node)){
                $param["param"]["node"] = $node;
            }
            return DataUtil::request($param);
        }
        
        private static function request($request){
            Logger::debug("\n==========  Request  ==========\n".json_encode($request,JSON_FORCE_OBJECT)."\n================================");  
            try{
                $script = "python ".dirname(__FILE__)."/core.py \"".preg_replace("/\"/","\\\\\"",json_encode($request,JSON_FORCE_OBJECT))."\"";
                Logger::debug("\n==========  Script  ==========\n$script\n================================");
                exec($script,$out,$rs);
                $outs = "";
                foreach($out as $line){
                    $outs .= $line;
                }
                Logger::debug("\n==========  Response  ==========\n$outs\n================================\n");
                $result = json_decode($outs);
                Logger::debug("retcode:".@$result->ret->retcode);
                return $result;
            }catch(Exception $e){
                Logger::error($e); //message
                return self::returnError(DATA_LOAD_ERROR);
            }
        }
        
        public static function returnError($code){
            $res = new stdClass();
            $res->ret = new stdClass();
            $res->ret->retcode = $code;
            return $res;
        }
 
    }
    
    // var_dump(DataUtil::getDiskList());
    // var_dump(DataUtil::getRaidList());
    // var_dump(DataUtil::createRaid("test_name","0","0",array("tt","t2")));
    // var_dump(DataUtil::dropRaid("test_name",true));
    // var_dump(DataUtil::getVGList());
    // var_dump(DataUtil::dropVG("test_vgname",true));
    // var_dump(DataUtil::extendVG("test_vgname",array("tt","t2")));
    // var_dump(DataUtil::reduceVG("test_vgname",array("tt","t2"),true));
    // var_dump(DataUtil::listPVbyVG("test_vgname"));
    // var_dump(DataUtil::getLVList());
    // var_dump(DataUtil::extendLV("testvg","testlv","100","M"));
    // var_dump(DataUtil::reduceLV("testvg","testlv","100","M"));
    // var_dump(DataUtil::getIPList());

?>