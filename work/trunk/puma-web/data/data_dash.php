<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function info(){
        $res = array("result"=>true);
        $cluster = DataUtil::getClusterState();
        $data = array();
        if($cluster->ret->retcode===0){
            if(isset($cluster->ret->msg)){
                $msg = preg_replace("/\'/","\"",$cluster->ret->msg);
                $clusts = json_decode($msg);
                // var_dump($clusts);
            }
            if(!empty($clusts)){
                foreach($clusts as $i=>$clust){
                    $data["host_name_".$i] = $clust->uname;
                    $data["host_ipaddr_".$i] = $clust->hb_addr;
                    $data["host_status_".$i] = ($clust->crmd=="online"?"<span class='color_green'>":"<span class='color_red'>").$clust->crmd."</span>";
                    $data["host_id_".$i] = $clust->id;
                }
            }
        }
        $prop = DataUtil::getClustName();
        $cluster_name = "";
        // var_dump($prop);
        if($prop->ret->retcode===0){
            $cluster_name = @$prop->ret->msg;
        }
        $data["cluster_name"] = $cluster_name;
        $res["data"] = $data;
        return json_encode($res);
    }
    
    function lun_list(){
        $luns = DataUtil::getLUNList();
        // var_dump($luns);
        $res = array("result" => $luns->ret->retcode===0);
        $res["rc"] = $luns->ret->retcode;
        $htmls = "";
        if($res["result"]){
            $msg = $luns->ret->msg;
            if(!empty($msg)){
                $msg = preg_replace("/\'/","\"",$msg);
                $rs = json_decode($msg);
            }
            if(isset($rs)){
                foreach($rs as $lun){
                    $htmls .= "<tr>
                        <td>".$lun->ip."</td>
                        <td>".$lun->lv_name."</td>
                        <td>".$lun->lun."</td>
                        <td>".(strtoupper($lun->lun_status=="NOT RUNNING")?"--":$lun->lun_status)."</td>
                        <td><span class='".(strtoupper($lun->lun_status)=="NOT RUNNING"?("color_red'>".$lun->lun_status):"color_green'>RUNNING")."</span></td>
                    </tr>";
                }
            }
        }
        if(empty($htmls)){
            $htmls = nondata($res["rc"]);
        }
        $res["data"] = $htmls;
        return json_encode($res);
    }
    function data_hist(){
        date_default_timezone_set('Asia/Shanghai');
        $res = array("result"=>true);
        $data = array();
        $time = time()-3600;
        $line1 = array("name"=>"read","data"=>array());
        $line2 = array("name"=>"write","data"=>array());
        for($i=0;$i<60;$i++){
            $line1["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,50));
            $line2["data"][] = array("x"=>($time+$i*60)*1000,"y"=>rand(0,1000));
        }
        $data[] = $line1;
        $data[] = $line2;
        $res["data"] = $data;
        return json_encode($res);
    }
    
    function eventinfo(){
        $res = array("result"=>true);
        $htmls = "<div class='event-cell'>
            <div class='event-title'>对象:卷vol_test <span class='event-time'>10分钟前</span></div>
            <div class='event-value'>admin,新增卷,成功</div>
        </div>
        <div class='event-cell'>
            <div class='event-title'>对象:卷vol_test <span class='event-time'>10分钟前</span></div>
            <div class='event-value'>admin,新增卷,成功</div>
        </div>";
        $res["data"] = $htmls;
        return json_encode($res);
    }
?>