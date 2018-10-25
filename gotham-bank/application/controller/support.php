<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;

/**
 * Class Support
 */
class Support extends Controller
{

    /**
     * PAGE: 
     * http://yourproject/support
     */
    public function default()
    {
        if (!$this->authTest())
            Bank::exit('/');
        elseif(!empty($_POST['message']) && !empty($_POST['theme']) && !empty($_POST['url']))
        {
            if($_POST['theme'] !== 'tech' && $_POST['theme'] !== 'simple')
            {
                $error = 'theme doesnt exist';
            }
            else
            {
                if($this->check($_POST['url']))
                {
                    $user_id = $_SESSION['userdata']['id'];
                    foreach ($_POST as $support => $value)
                        $$support = trim($value);

                    $result = $this->model->toSupport($message, $theme, $url, $user_id);

                    if($result)
                        $success = 'Your message was sent';
                    else
                        $error = 'Message wasnt sent';

                }                
            }
        }

        $messages = $this->model->getMessagesToSupport($_SESSION['userdata']['id']);

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/support.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function iframe()
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif(!empty($_GET['url']))
        {
            $parse = parse_url($_GET['url']);

            if(isset($parse['host']) && $parse['host'] == $_SERVER['SERVER_NAME'])
            {
                $curl = curl_init();

                curl_setopt($curl, CURLOPT_URL, trim($_GET['url']));
                curl_setopt($curl, CURLOPT_CONNECTTIMEOUT, 4);
                curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
                curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
                curl_setopt($curl, CURLOPT_MAXREDIRS, 4); 

                $data = curl_exec($curl);
                curl_close($curl);

                if($data !== false)
                    print($data);
            }
            else
            {
                $error = 'Only '.$_SERVER['SERVER_NAME'].'!';
                echo json_encode(array('error' => $error));
            }
        }
    }

    public function message($id = 0)
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif(isset($id) && is_numeric($id))
        {
            $message = $this->model->getSupportMessageById($id);
            if($message)
                echo json_encode($message);
            else
                echo json_encode(array('error' => 'not found'));
        }
    }

    public function userhistory($id = 0)
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif(isset($id) && is_numeric($id))
        {
            $message = $this->model->getSupportMessageByUserId($id);
            if($message)
            {
                echo json_encode($message);
            }
            else
                echo json_encode(array('error' => 'not found'));
        }
    }

    public function getmessages()
    {
        if(!$this->authTest() || $_SESSION['userdata']['name'] !== 'support')
            Bank::exit('/');
        else
        {
            $message = $this->model->getSupportsMessages();
            if($message)
                echo json_encode($message);
        }
    }
}