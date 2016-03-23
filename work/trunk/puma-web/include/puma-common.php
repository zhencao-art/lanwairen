<?php
    require_once("logger.php");
    define("UNIT_k" , 1000 );
    define("UNIT_K" , 1024 );
    define("UNIT_G" , 1073741824 );
    
    define("LIMIT_T",1);
    define("LIMIT_G",2);
    define("LIMIT_M",3);
    define("LIMIT_K",4);
    
    define("DATA_LOAD_ERROR","-1");
    define("NON_DATA","0");
    define("ARGV_NUM_ERROR","1001");
    define("ARGV_ERROR","1002");
    define("REQUIRED_NOTFILL","1003");
    define("REQ_DATA_ERROR","1004");
    define("PARSE_RES_ERROR","1005");
    define("CONF_SERVER_ERROR","1006");
    define("CALL_SERVICE_ERROR","1007");
    
    $error_code = array(
        NON_DATA=>"没有数据",
        DATA_LOAD_ERROR=>"获取数据失败",
        ARGV_NUM_ERROR=>"参数数目错误",
        ARGV_ERROR=>"参数错误",
        REQUIRED_NOTFILL=>"有必填参数未填",
        REQ_DATA_ERROR=>"数据请求失败",
        PARSE_RES_ERROR=>"解析结果失败",
        CONF_SERVER_ERROR=>"服务未配置",
        CALL_SERVICE_ERROR=>"调用服务失败"
    );
    function nondata($flag=NON_DATA){
        global $error_code;
        $msg = "没有数据";
        if(isset($error_code[$flag])){
            $msg = $error_code[$flag];
        }
		return "<td colspan='20' style='padding:10px'><div class=\"alert alert-danger col-sm-12\" role=\"alert\"><strong>提示:</strong> $msg</div></td>";
	}
    
    function transUnit($value,$unit_type,$decimal,$block=false,$limit_unit=0){
        $unit_T = $unit_type*$unit_type*$unit_type*$unit_type*1.0;
        $unit_G = $unit_type*$unit_type*$unit_type*1.0;
        $unit_M = $unit_type*$unit_type*1.0;
        $unit_K = $unit_type*1.0;
        if($block){
            $value = $value * 512;
        }
        if($value>=$unit_T || $limit_unit==LIMIT_T){
            return round($value/$unit_T,$decimal)." T";
        }else if($value>=$unit_G || $limit_unit==LIMIT_G){
            return round($value/$unit_G,$decimal)." G";
        }else if($value>=$unit_M || $limit_unit==LIMIT_M){
            return round($value/$unit_M,$decimal)." M";
        }else if($value>=$unit_K || $limit_unit==LIMIT_K){
            return round($value/$unit_K,$decimal)." K";
        }else{
            return $value;
        }
    }
?>