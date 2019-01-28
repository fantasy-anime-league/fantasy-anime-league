<?php

// test server permissions (error function dep'd)
/*$myfile = fopen("testfile.txt", "w");
$txt = "testing";
fwrite($myfile, $txt);
fclose($myfile);*/

// includes
require_once($_SERVER['DOCUMENT_ROOT'].'/falbanners/includes/falbanner.class.inc.php');

// sanitize inputs
$user = isset($_GET['user']) ? $_GET['user'] : '';
$type = isset($_GET['type']) ? $_GET['type'] : 'cinderella';

// display banner
error_log("1", 0);
$banner = new FALBanner($user,$type);
error_log("2", 0);
$banner->display();

