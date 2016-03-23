<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<?php  include_once "puma_replaceable.php"; ?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible"/>
    <title><?php echo APP_NAME; ?>登录</title>
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/puma-login.css"/>
    <link rel="shortcut icon" type="image/x-icon" href="img/favicon.ico" media="screen" />
</head>
<body style='background-color:#1D293A'>
    <div class="panel">
        <div class="panel-panel">
            <img src='img/<?php echo LOGIN_LOGO; ?>' class="logo">
            <h2><?php echo LOGIN_APP_NAME; ?></h2>
            <div id="login_error_msg" class="error hidden"></div>
            <input id="uname" class="text-input username" data-template="<div class='popover input-border' role='tooltip'><div class='arrow arrow-border'></div><div class='popover-content input-tip'></div></div>" data-animation="false" data-content="用户名不能为空" data-toggle="popover" data-trigger="manual" placeholder="用户名" name="username">
            <input id="pass" type="password" class="text-input password"data-template="<div class='popover input-border' role='tooltip'><div class='arrow arrow-border'></div><div class='popover-content input-tip'></div></div>" data-animation="false" data-content="密码不能为空" data-toggle="popover" data-trigger="manual" placeholder="密码" name="password">
            <button id="submit" class="btn-login">登 录</button>
            <div class="login-version"> <?php echo PDS_LONG_VERSION; ?> </div>
        </div>
    </div>
    <div class="login-loading hidden">
        <img src="img/loading.gif">
    </div>
    <script src="js/jquery-1.10.2.js"></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/puma_login.js"></script>
</body>
</html>