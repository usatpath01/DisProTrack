<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Home | To-Do App</title>
</head>
<body>
	<?php

		echo "Welcome ". $_SESSION['current_user']['name']," !!";
		echo "Your last login time was at ". $_SESSION['current_user']['id']," !!";


	 echo "<br/>";

	 	echo "Site under construction!!";



	 ?>



	<a href="logout.php">Click to logout out!! </a>

	<!-- <link  href="logout.php"></link> -->

</body>
</html>