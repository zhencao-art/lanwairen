<?php
    require("puma_conf.php");
    
    class Logger{
        
        public static function error($msg){
            error_log("[".Logger::get_time()."][ERROR] $msg\n", 3, LOGGER_FILE);        
        }
        
        public static function info($msg){
            if(LOGGER_LEVEL<1){
                return;
            }
            error_log("[".Logger::get_time()."][INFO] $msg\n", 3, LOGGER_FILE);        
        }
        
        public static function debug($msg){
            if(LOGGER_LEVEL<2){
                return;
            }
            error_log("[".Logger::get_time()."][DEBUG] $msg\n", 3, LOGGER_FILE);        
        }
        
        public static function get_time(){
            date_default_timezone_set('Asia/Shanghai');
            return date("Y-m-d H:i:s");
        }
        
    }
?>