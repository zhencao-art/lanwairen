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
        $res = array("result" => true);
        $res["data"] = array(
            "node_all"=>4,
            "disk_all"=>20,
            "mem_capacity"=>64,
            "cpu_cores"=>8
        );
        return json_encode($res);
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
                $htmls .= "<tr>
                    <td><a href='#' class='node-info' node_id='".$node->logical_id."' node_type='".$node->node_type."'>".$node->listen_ip."</a></td>
                    <td>".($node->actual_state?"<span class='color_green'>ONLINE</span>":"<span class='color_red'>OFFLINE</span>")."</td>
                    <td>HDD: 5 个 SSD: 0 个</td>
                    <td>16 GB</td>
                    <td>2 个</td>
                </tr>";
            }
        }else{
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function node_infos(){
        $res = array("result" => true);
        $res["disks"] = array(
            array("slot"=>1,"status"=>0),
            array("slot"=>2,"status"=>1),
            array("slot"=>3,"status"=>1),
            array("slot"=>4,"status"=>1),
            array("slot"=>5,"status"=>2)
        );
        $res["ports"] = array(
            array("port"=>1),
            array("port"=>2)
        );
        return json_encode($res);
    }
    
    function data_hist(){
        date_default_timezone_set('Asia/Shanghai');
        $res = array("result"=>true);
        $data = array();
        $time = time()-3600;
        $line = array("name"=>$_REQUEST["name"],"data"=>array());
        for($i=0;$i<60;$i++){
            $line["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,20));
        }
        $data[] = $line;
        $res["data"] = $data;
        return json_encode($res);
    }
?>