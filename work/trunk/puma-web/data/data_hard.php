<?php    
    require_once "../include/data_util.php";
    require_once "../include/puma-common.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function info(){
        $res = array("result"=>true);
        //磁盘概况
        $disk_all = 0;
        $disk_online = 0;
        $disk_offline = 0;
        $disk_uninit = 0;
        $disk_ssds = 0;
        $disk_hdds = 0;
        $disks = DataUtil::getDiskList(NULL);
        if($disks->rc->retcode===0){
            foreach($disks->body->{"pds\mds\get_disk_list_response"}->disk_infos as $disk){
                $disk_all++;
                $disk_hdds++;
                if(isset($disk->logical_id)){
                    if($disk->actual_state){
                        $disk_online++;
                    }else{
                        $disk_offline++;
                    }
                }else{
                    $disk_uninit++;
                }
            }
        }
        
        //统计节点概况
        $nodes_all = 0;
        $nodes_init = 0;
        $nodes_uninit = 0;
        $nodes_normal = 0;
        $nodes_error = 0;
        $nodes_ios = 0;
        $nodes_bac = 0;
        $nodes = DataUtil::getNodeList();
        if($nodes->rc->retcode===0){
            foreach($nodes->body->{'pds\mds\get_node_list_response'}->node_infos as $node){
                if(strtolower($node->node_type)=="mds"){
                    continue;
                }
                if($node->node_state!=NODE_STATE_UNCONFIGED){
                    $nodes_init++;
                    if($node->actual_state){
                        $nodes_normal++;
                    }else{
                        $nodes_error++;
                    }
                }
                if(strtolower($node->node_type)=="bac"){
                    $nodes_bac++;
                }else{
                    $nodes_ios++;
                }
                $nodes_all++;
            }
            $nodes_uninit = $nodes_all - $nodes_init;
        }
        
        $res = array("result"=>true);
        $res["data"] = array(
            "nodes_uninit"=>$nodes_uninit,
            "nodes_all"=>$nodes_all,
            "nodes_init"=>$nodes_init,
            "nodes_error"=>$nodes_error,
            "nodes_normal"=>$nodes_normal,
            "nodes_ios"=>$nodes_ios,
            "nodes_bac"=>$nodes_bac,
            "disk_all"=>$disk_all,
            "disk_ssds"=>$disk_ssds,
            "disk_hdds"=>$disk_hdds,
            "disk_offline"=>$disk_offline,
            "disk_online"=>$disk_online,
            "disk_uninit"=>$disk_uninit
        );
        return json_encode($res);
    }
    
    function data_hist(){
        date_default_timezone_set('Asia/Shanghai');
        $res = array("result"=>true);
        $data = array();
        $time = time()-3600;
        $line1 = array("name"=>"su001","data"=>array());
        $line2 = array("name"=>"su002","data"=>array());
        $line3 = array("name"=>"su003","data"=>array());
        $line4 = array("name"=>"du001","data"=>array());
        $line5 = array("name"=>"du002","data"=>array());
        for($i=0;$i<60;$i++){
            $line1["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,10));
            $line2["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,20));
            $line3["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,40));
            $line4["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,70));
            $line5["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,100));
        }
        $data[] = $line1;
        $data[] = $line2;
        $data[] = $line3;
        $data[] = $line4;
        $data[] = $line5;
        $res["data"] = $data;
        return json_encode($res);
    }
?>