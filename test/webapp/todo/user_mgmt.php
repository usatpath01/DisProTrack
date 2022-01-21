<?php
	
	/*
	This file contains all the functions realted to the user management module
	The OFS contains two types of user :
	1: Form creator
	*/
	function isLoggedin()
	{
		if(isset($_SESSION['current_user']))
		{
			return true;
		}
		else
		{
			return false;
		}
	}
	
	function login($username,$password)
	{
		global $dbcon;
		$query = "SELECT lastlogin from users where username='".$username."' and pass='".md5($password)."'";
		// echo $query;
		

		$res = $dbcon->query($query);

        $rcnt = 0;
        while ($row = $res->fetchArray()) {
            $rcnt++;
            // echo $row;
            $_SESSION['current_user'] = array('id' => $row['lastlogin'], 'name' => $username );
        }

        if($rcnt  == 0)
        	return false;
        else
        	return true;

	}
	function logout()
	{
		session_destroy();

	}
?>