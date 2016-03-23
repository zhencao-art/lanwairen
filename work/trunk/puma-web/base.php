<?php 
	session_start();
    // || !isset($_SERVER['HTTP_REFERER'])
	if(!isset($_SESSION["login_name"])){
		header("Location: login.php");
	} 
	session_write_close();
    
    require_once("puma_replaceable.php");
?>