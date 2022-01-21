<?php 
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
session_start();
ob_start();
require 'dbcon.php';
// require 'bin/lib/utils.php';
require 'user_mgmt.php'; 
if(isLoggedin())
{
   header('Location:index.php'); 
   die('Un-ethical activity detected..!!  Do not try to such things here.');
}
if(isset($_POST['log_in']))
{
    //print_r($_POST);
    // $username = mysqli_real_escape_string($dbcon,(htmlentities($_POST['username'])));
    // $password = mysqli_real_escape_string($dbcon,(htmlentities($_POST['password'])));

    $username = (htmlentities($_POST['username']));
    $password = (htmlentities($_POST['password']));
    $msg = login($username,$password);
    if($msg == true)
    {
        header('Location:index.php');
        die('Un-ethical activity detected..!!  Do not try to such things here.');
    }
    else
    {
        ?><script>alert( 'Invalid Credentials' );</script><?php
        unset($_POST);
    }
}

// mysqli_close($dbcon);
ob_end_flush();


?>



<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Login Page | ToDO App</title>
</head>
<body>
	<!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script> -->
</body>
	<h1>Todo appl login form </h1>	

	<form method="POST" action="login.php">
		<label for="username">Enter Username: </label>

		<input id="username" type="text" name="username"/>
		<br>

		<label for="password">Enter Passowrd: </label>
		<input id="password" type="password" name="password"/>
		<br>
		<input name="log_in" type="submit" value="Log In "> </input>

	</form>


	<!-- <main class="form-signin">
  <form>
    <img class="mb-4" src="todo.jpg" alt="" width="72" height="57">
    <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

    <div class="form-floating">
      <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
      <label for="floatingInput">Email address</label>
    </div>
    <div class="form-floating">
      <input type="password" class="form-control" id="floatingPassword" placeholder="Password">
      <label for="floatingPassword">Password</label>
    </div>

    <div class="checkbox mb-3">
      <label>
        <input type="checkbox" value="remember-me"> Remember me
      </label>
    </div>
    <button class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
    <p class="mt-5 mb-3 text-muted">&copy; 2017–2021</p>
  </form> -->
</main>
</html>