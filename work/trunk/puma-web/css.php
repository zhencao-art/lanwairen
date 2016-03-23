    <link href="css/bootstrap.min.css" rel="stylesheet"/>
    <link href="css/bootstrap-theme.min.css" rel="stylesheet"/>
    <link href="css/tooltip.css" rel="stylesheet"/>
    <link href="css/theme-<?php session_start(); echo empty($_SESSION["user_theme"])?"black":($_SESSION["user_theme"]); session_write_close();?>.css" rel="stylesheet"/>
    <link href="css/common.css" rel="stylesheet"/>
    <link rel="shortcut icon" type="image/x-icon" href="img/favicon.ico" media="screen" />
