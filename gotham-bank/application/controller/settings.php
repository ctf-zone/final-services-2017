<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\User as User;

/**
 * Class Settings
 */
class Settings extends Controller
{

    /**
     * PAGE: 
     * http://yourproject/settings
     */
    public function default()
    {
        $fname = '';
        $sname = '';

        if (!$this->authTest())
        {
            Bank::exit('/');
        }
        elseif(!empty($_POST['fname']) && !empty($_POST['sname']) && !is_array($_POST['fname']) && !is_array($_POST['sname']))
        {
            $userdata = $this->model->getUserData($_SESSION['userdata']['id']);

            if($userdata)
            {
                $data = User::userdataCheck($_POST);

                if($data)
                {
                    $result = $this->model->changeUserData($data['fname'], $data['sname'], $_SESSION['userdata']['id']);

                    if($result)
                    {
                        $fname = $data['fname'];
                        $sname = $data['sname'];
                        $success = 'Personal data is changed.';
                    }
                    else
                        $error = 'Personal information is not changed, please try again.';
                }
                else
                    $error = 'First name or second name is not valid.';
            }
            else
            {
                $data = User::userdataCheck($_POST);

                if($data)
                {
                    $result = $this->model->toUserData($data['fname'],$data['sname'], $_SESSION['userdata']['id']);

                    if($result)
                    {
                        $fname = $data['fname'];
                        $sname = $data['sname'];
                        $success = 'Personal data is changed.';
                    }
                    else
                        $error = 'Personal information is not changed, please try again.';
                }
                else
                    $error = 'First name or secon name is not valid.';
            }
        }
        else
        {
            $userdata = $this->model->getUserData($_SESSION['userdata']['id']);

            if($userdata)
            {
                $fname = $userdata->first_name;
                $sname = $userdata->second_name;
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/settings.php';
        require APP . 'view/standard/include/footer.php';

    }
}
