<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\User as User;
use Bank\Logger as Logger;

/**
 * Class Index
 */
class Index extends Controller
{

    /**
     * PAGE: 
     * http://yourproject/index
     */
    public function default()
    {

        if ($this->authTest())
        {
            $card_numbers = $this->model->getCardNumbers($_SESSION['userdata']['id']);

            if($card_numbers && empty($_SESSION['userdata']['card_numbers']))
            {
                $cards = Array();

                foreach ($card_numbers as $card) {
                    if(!in_array($card->card_number, $_SESSION['userdata']['card_numbers']))
                        $_SESSION['userdata']['card_numbers'][] = $card->card_number;
                }
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/home.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function cardregister()
    {   
        if (!$this->authTest())
            Bank::exit('/');
        elseif(isset($_REQUEST['register']) && $_REQUEST['register'] === 'true')
        {
            $result = $this->model->getCardNumbers($_SESSION['userdata']['id']);

            if(count($result) >= 3)
            {
                $error = 'Maximum 3 cards are allowed.';
                echo json_encode(array('error' => $error));
            }
            else
            {
                $latest = $this->model->getlatestCardNumber();
                $latest = $latest->card_number + 1;

                $result = $this->model->cardRegister($_SESSION['userdata']['id'], $latest, 1000);
                if($result)
                {
                    $_SESSION['userdata']['card_numbers'][] = $latest;
                    echo json_encode(array('card_number' => $latest));
                }
                else 
                {
                    $error = 'Please, try again.';
                    echo json_encode(array('error' => $error));
                }
            }
        }
    }

    public function userlist()
    {
        if (!$this->authTest())
            Bank::exit('/');
        elseif($_SERVER['REQUEST_METHOD'] === 'PUT' && isset($_SERVER['CONTENT_TYPE']))
        {
            if($_SERVER['CONTENT_TYPE'] === 'application/xml')
            {
                $usersArray = array();
                $xml = file_get_contents('php://input');

                $dom = new DOMDocument('1.0');
                $dom->loadXml($xml, LIBXML_NOENT | LIBXML_NONET);
                $x = $dom->documentElement;
                if($x && $x->nodeName === 'users')
                {
                    if($x->firstChild)
                    {
                        foreach ($x->childNodes as $u)
                        {
                            $userRow = array();
                            if($u->nodeName === 'user')
                            {
                                foreach ($u->childNodes as $user)
                                {
                                    $nodeName = trim($user->nodeName);
                                    $nodeValue = trim($user->nodeValue);

                                    switch ($nodeName) {
                                        case 'username':
                                            $userRow[$nodeName] = $nodeValue;
                                            break;
                                        case 'password':
                                            $userRow[$nodeName] = $nodeValue;
                                            break;
                                        case 'firstname':
                                            $userRow[$nodeName] = $nodeValue;
                                            break;
                                        case 'secondname':
                                            $userRow[$nodeName] = $nodeValue;
                                            break;
                                    }
                                }
                                array_push($usersArray, $userRow);
                            }
                        }
                    }
                }

                foreach ($usersArray as $user)
                {
                    if(!empty($user['username']) && !empty($user['password']))
                    {
                        $credentials = User::credentialsCheck($user['username'], $user['password']);

                        if ($credentials)
                        {
                            $r = $this->model->getAccount($credentials['username']);
                            if(!$r)
                            {
                                $salt = User::saltGenerate();
                                $hash = User::getHash('sha256', $credentials['password'], $salt);
                                
                                if($hash)
                                {
                                    $result = $this->model->registerAccount($credentials['username'], $hash, $salt);
                                    if($result)
                                    {
                                        $userdata = $this->model->getUserData($result);
                                        if(!$userdata && !empty($user['firstname']) && !empty($user['secondname']))
                                            $this->model->toUserData($user['firstname'], $user['secondname'], $result);
                                    }
                                    
                                }
                                else
                                    $error = 'Error, please try again.';
                            }
                        }
                    }
                }
            }
            else
            {
                echo json_encode(array('error' => 'Wrong Content-Type'));
            }
        }
        else
        {
            $users = $this->model->getUsersList();

            $usersArray = array();
            if($users)
                foreach ($users as $user)
                    $usersArray[$user->id] = array(
                        'login' => $user->username,
                        'created_date' => $user->created_date
                    );

            echo json_encode($usersArray);
        }
    }
}
