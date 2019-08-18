<?php

ini_set('open_basedir', '.');

if(!isset($_GET["app"])) {
    header("Location: index.php?app=kittens.php");
    die();
} else {
    require $_GET["app"];
}

