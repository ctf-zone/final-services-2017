<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\Session as Session;

/**
 * Class Logout
 */
class Logout extends Controller
{

    /**
     * PAGE: 
     * http://yourproject/logout
     */
    public function default()
    {
        if(!empty($_SESSION['userdata']))
        {
            if(Session::sessionDestroy('userdata'))
                Bank::exit('/');
            else
            {
                $error = 'Can not destroy session.';
            }
        }
        else
            Bank::exit('/');    
    }
}
