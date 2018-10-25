<?php

class Controller
{
    public $db = null;
    public $model = null;

    function __construct()
    {
        $this->openDatabaseConnection();
        $this->loadModel();
    }

    private function openDatabaseConnection()
    {
        $options = array(PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_OBJ, PDO::ATTR_ERRMODE => PDO::ERRMODE_WARNING);

        $this->db = new PDO(DB_TYPE . ':host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=' . DB_CHARSET, DB_USER, DB_PASS, $options);
    }

    protected function loadModel()
    {
        require APP . 'model/model.php';

        $this->model = new Model($this->db);
    }

    protected function authTest()
    {
        if (empty($_SESSION['userdata']))
            return false;

        if($_SESSION['userdata']['id'] === 1 && $_SESSION['userdata']['name'] === 'support')
            return true;

        $account = $this->model->getAccount($_SESSION['userdata']['name']);
        
        if ($account === false || hash('sha256', $_SESSION['userdata']['password'].$account->salt) !== $account->password)
        {
            unset($_SESSION['userdata']);
            return false;
        }
        return true;
    }

    protected function check($url)
    {
        return true;
    }
}

