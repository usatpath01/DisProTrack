<?php 

	$hash = '';
	if(isset($_GET['get_hash']) && !empty($_GET['get_hash']))
	{
		$var = $_GET['get_hash'];

		$hash = md5($var);
	}

?>


<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Hash Generator</title>
</head>
<body>
	<form method="GET" action="hashgen.php">
		<label>Enter the text for whoch hash is required::   </label>
<input id="get_hash" type="text" name="get_hash" value="<?php if(isset($_GET['get_hash']) && !empty($_GET['get_hash'])){echo $_GET[get_hash];} ?>"></input>

<br><input type="submit" value="Generate">

	</form>

<?php 
	
	if(!empty($hash))
	{
		// echo "MD5 Hash of the input is ::  ";
		// echo $hash;
		print("MD5 Hash of the input is :: ".$hash);
	}

?>
</body>
</html>

