<?php
	// $dbcon = @mysqli_connect('localhost','root','','mofs');
	// if ( mysqli_connect_errno() ) {
 //        //printf("Connection failed: %s", mysqli_connect_error());
 //        die("Failed to connect at the moment :( ..<br/> contact admin in case of urgency to report this incident ");
 //    }


    class MyDB extends SQLite3 
    {
        function __construct() {
            $filename ='todo';
            if (!file_exists($filename))
                die("Failed to connect at the moment :( ..<br/> App not initialized. Contact Admin ");

            $this->open($filename);

            // $this->exec('SELECT COUNT(*) from users');
            $res = $this->query('SELECT COUNT(*) from users');

            $rcnt = 0;
            while ($row = $res->fetchArray()) 
            {
                $rcnt++;
            }

            if($rcnt <= 0)
                die("Failed to connect at the moment :( ..<br/> App not initialized. Contact Admin ");
        }


        function __destruct() {
            $this->close();
        }
    }


    $dbcon = new MyDB();

?>