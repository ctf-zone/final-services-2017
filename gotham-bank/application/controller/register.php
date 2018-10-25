<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\User as User;

/**
 * Class Register
 */
class Register extends Controller
{
    /**
     * PAGE: 
     * http://yourproject/register
     */
    public function default()
    {
        if ($this->authTest())
            Bank::exit('/');
        elseif (!empty($_POST['username']) && !empty($_POST['password']))
        {
            $credentials = User::credentialsCheck($_POST['username'], $_POST['password']);

            if($credentials)
            {
                $username = $credentials['username'];
                $password = $credentials['password'];

                if(!$this->model->getAccount($username))
                {
                    $salt = User::saltGenerate();

                    $hash = User::getHash('sha256', $password, $salt);
                    if($hash)
                    {
                        $result = $this->model->registerAccount($username, $hash, $salt);

                        if($result)
                            Bank::exit('/login');
                        else
                            $error = 'Error, please try again.';
                    }
                    else
                    {
                        $error = 'Error, please try again.';
                    }
                }
                else
                {
                    $error = 'Username already exists.';
                }
            }
            else
            {
                $error = 'Error, please try again.';
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/register.php';
        require APP . 'view/standard/include/footer.php';     
    }
}
