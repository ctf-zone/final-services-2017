<?php 

spl_autoload_register(function ($class_name) {
    $class_name = explode('\\', $class_name);
    require dirname(__DIR__).'/classes/'.end($class_name).'Class.php';
});