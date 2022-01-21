<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
	session_start();
    ob_start();
    require 'dbcon.php';
// require 'bin/lib/utils.php';
require 'user_mgmt.php'; 
	if(!isLoggedin())
	{
	   header('Location:login.php');
	   die('Un-ethical activity detected..!!  Do not try to such things here.');
	}
	
	include("main.php");



	ob_end_flush();
?>


