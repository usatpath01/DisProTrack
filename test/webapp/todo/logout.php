<?php
	session_start();
    ob_start();
    // require 'bin/lib/utils.php';
    require 'user_mgmt.php';
	if(!isLoggedin())
	{
	   header('Location:login.php');
	   die('Un-ethical activity detected..!!  Do not try to such things here.'); 
	}
	logout();
	header('Location:login.php');
	ob_end_flush();
?>