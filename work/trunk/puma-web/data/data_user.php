<?php    
    require_once "../include/puma-common.php";
    require_once "user.php";
    require_once "../include/puma_conf.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function login(){
        global $user_name;
        global $user_pass;
        global $user_theme;
        $username = $_REQUEST["username"];
        $passwd = $_REQUEST["passwd"];
        $res = array("result"=>false);
        if($username == $user_name && md5($passwd) == $user_pass){
            $res["result"] = true;
            session_start();
            $_SESSION["login_name"] = $username;
            $_SESSION["user_theme"] = $user_theme;
            session_write_close();
        }
        return json_encode($res);
    }
    
    function logout(){
        $res = array("result"=>true);
        session_start();
        unset($_SESSION["login_name"]);
        session_write_close();
        return json_encode($res);
    }
    
    function update_pass(){
        global $user_name;
        global $user_pass;
        global $user_theme;
        $pass_old = $_REQUEST["pass_old"];
        $pass_new = $_REQUEST["pass_new"];
        $res = array("result"=>false);
        if(md5($pass_old) != $user_pass){
            $res["error"] = "原密码错误";
            Logger::info("原密码错误,修改密码失败");
        }else{
            $f = @fopen("user.php","w");
            @fputs($f, "<?php\n");
            @fputs($f, "\$user_name = 'admin';\n");
            @fputs($f, "\$user_pass = '".md5($pass_new)."';\n");
            @fputs($f, "\$user_theme = '".(empty($user_theme)?"":$user_theme)."';\n");
            @fputs($f, "?>\n");
            @fclose($f);
            $res["result"] = true;
            Logger::info("修改密码成功");
        }
        return json_encode($res);
    }
    
    function theme(){
        global $user_name;
        global $user_pass;
        $res = array("result"=>false);
        $new_theme = empty($_REQUEST["theme"])?"":$_REQUEST["theme"];
        $f = @fopen("user.php","w");
        @fputs($f, "<?php\n");
        @fputs($f, "\$user_name = 'admin';\n");
        @fputs($f, "\$user_pass = '".$user_pass."';\n");
        @fputs($f, "\$user_theme = '".$new_theme."';\n");
        @fputs($f, "?>\n");
        @fclose($f);
        $res["result"] = true;
        session_start();
        $_SESSION["user_theme"] = $new_theme;
        session_write_close();
        return json_encode($res);
    }
?>