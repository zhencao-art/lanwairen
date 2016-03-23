<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_utils.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function dt(){
        // $prop = DataUtil::opClusterProperty();
        // $res = array("result" => $prop->ret->retcode===0);
        $cur_time = DataUtil::getCurrentDT();
        // var_dump($cur_time);
        $ctime = "";
        if($cur_time->ret->retcode===0){
            $ctime = $cur_time->time->year."-".sprintf("%02d",$cur_time->time->mon)."-".sprintf("%02d",$cur_time->time->day)." ".sprintf("%02d",$cur_time->time->hour).":".sprintf("%02d",$cur_time->time->min).":".sprintf("%02d",$cur_time->time->sec);
        }else{
            $ctime = date("Y-m-d H:m:s");
        }
        $res = array("result" => true);
        $res["data"] = array("dt_info_dt"=>$ctime);
        return json_encode($res);
    }
    
    function dt_get(){
        $cur_tz = DataUtil::getCurrentTZ();
        $res = array("result" => true);
        $tz = "";
        if($cur_tz->ret->retcode===0){
            $tz = $cur_tz->tz[0]->tz;
        }
        $host_name = "";
        $status = "未启用";
        $status_ = 0;
        $url = "";
        $cur_state = DataUtil::getNTPState();
        if($cur_state->ret->retcode===0){
            $status = isset($cur_state->status) && $cur_state->status?"启用中":"未启用";
            $status_ = isset($cur_state->status) && $cur_state->status?1:0;
            $url = isset($cur_state->url)?$cur_state->url:"";
            $host_name = isset($cur_state->host_name)?$cur_state->host_name:"";
        }
        $res["data"] = array(
            "dt_set_tz"=>$tz,
            "dt_set_syc"=>$status,
            "dt_set_syc_srouce"=>$status_,
            "dt_set_host_srouce"=>$host_name,
            "dt_set_srv"=>$url
        );
        return json_encode($res);
    }
    function dt_set(){
        $is_syc = $_REQUEST["is_syc"];
        $srv = $_REQUEST["srv"];
        $dt = $_REQUEST["dt"];
        $tz = $_REQUEST["timezone"];
        $main = $_REQUEST["main"];
        $res = array("result" => false);
        if($is_syc==1){
            $rc = DataUtil::setTZAndNTP($tz,$main,$srv);
        }else{
            $rc = DataUtil::setTZ($tz,$dt);
        }
        $res["result"] = $rc->ret->retcode===0;
        if($rc->ret->retcode===0){
            Logger::info("设置时间".($is_syc==1?"同步":"")."成功");
        }else{
            Logger::info("设置时间".($is_syc==1?"同步":"")."失败,".@$rc->ret->msg);
        }
        return json_encode($res);
    }
    function zone_set(){
        $tz = $_REQUEST["timezone"];
        $res = array("result" => false);
        $rc = DataUtil::setTimezone($tz);
        $res["result"] = $rc->ret->retcode===0;
        if($rc->ret->retcode===0){
            Logger::info("设置时区为'$tz'成功");
        }else{
            Logger::info("设置时区'$tz'失败,".@$rc->ret->msg);
        }
        return json_encode($res);
    }
    function zt(){
        $tzs = DataUtil::getAllTZ();
        $res = array("result" => $tzs->ret->retcode);
        $data = array();
        if($tzs->ret->retcode===0){
            foreach($tzs->tz as $tz){
                $data[] = array("tz"=>$tz->tz);
            }
        }
        $res["data"] = $data;
        return json_encode($res);
    }
    
?>