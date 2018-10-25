<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\User as User;
use Bank\Session as Session;

/**
 * Class Login
 */
class Login extends Controller
{

    /**
     * PAGE: default
     * http://yourproject/login
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
                $account = $this->model->getAccount($credentials['username']);

                if ($account)
                {
                    $password = $credentials['password'];

                    if (User::getHash('sha256', $password, $account->salt) == $account->password)
                    {
                        $userdata = array(
                            'id' => $account->id,
                            'name' => $account->username,
                            'password' => $password,
                            'card_numbers' => Array()
                        );

                        Session::sessionRegenerate();
                        $_SESSION['userdata'] = $userdata;

                        if (empty($_SESSION['token']))
                            $_SESSION['token'] = bin2hex(random_bytes(32));

                        Bank::exit('/');
                    }
                    else
                    {
                        $error = 'User or password is incorrect.';
                    }
                }
                else
                {
                    $error = 'User or password is incorrect.';
                }
            }
            else
            {
                $error = 'User or password is incorrect.';
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/login.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function support()
    {
        if ($this->authTest())
            Bank::exit('/');
        elseif(!empty($_POST['str']) && !empty($_POST['signature']))
        {
            $str = $this->model->getAuthString($_POST['str']);
            if(isset($str->id))
            {
                $signature = base64_decode($_POST['signature']);

                $key_path = dirname(__DIR__).'/config/key.pub';

                $key = openssl_pkey_get_public(file_get_contents($key_path));

                $result = openssl_verify($_POST['str'], $signature, $key, OPENSSL_ALGO_SHA256);
                if($result)
                {
                    $support = $this->model->getAccount('support');
                    if($support)
                    {
                        $userdata = array(
                                'id' => 1, 
                                'name' => 'support',
                                'card_numbers' => Array()
                            );

                        Session::sessionRegenerate();
                        $_SESSION['userdata'] = $userdata;

                        $this->model->changeStateOfAuthString(trim($_POST['str'])); 

                        Bank::exit('/');
                    }
                    else
                    {
                        echo json_encode(array('error' => 'support account not found'));
                    }
                }
                else
                {
                    echo json_encode(array('error' => 'error, try again'));
                }                
            }
            else
            {
                echo json_encode(array('error' => 'str not found'));
            }
        }
        else
        {
            $hash = User::saltGenerate();
            $result = $this->model->setAuthString($hash, 0);

            if($result)
                echo json_encode(array('string' => $hash));
            else
                echo json_encode(array('error' => 'try again'));
        }
    }
}
