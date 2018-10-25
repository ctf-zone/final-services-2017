<?php

class Application
{
    private $controller = null;

    private $method = null;

    private $params = array();

    public function __construct()
    {
        $this->parseUrl();
        
        if(!$this->controller)
        {

            require APP . 'controller/index.php';
            $page = new Index();
            $page->default();

        }
        elseif(file_exists(APP . 'controller/' . $this->controller . '.php'))
        {
            require APP . 'controller/' . $this->controller . '.php';

            $this->controller = new $this->controller();

            $class_methods = get_class_methods($this->controller);

            if(in_array($this->method, $class_methods) && $this->method !== '__construct')
            {
                if(!empty($this->params))
                {
                    call_user_func_array(array($this->controller, $this->method), $this->params);
                }
                else
                {
                    try
                    {
                        $this->controller->{$this->method}();
                    }
                    catch(Error $e)
                    {
                        $this->error404();
                    }
                }
            }
            else
            {
                if(strlen($this->method) == 0)
                {
                    $this->controller->default();
                }
                else
                {
                    $this->error404();
                }
            }
        }
        else
        {
            $this->error404();
        }
    }

    private function parseUrl()
    {
        if($_SERVER['REQUEST_URI'] !== '/')
        {
            $path = trim($_SERVER['REQUEST_URI'], '/');
            $path = explode('?', $path)[0];
            $path = explode('/' , $path);

            $this->controller = isset($path[0]) ? mb_strtolower($path[0]) : null;
            $this->method = isset($path[1]) ?  mb_strtolower($path[1]) : null;
            $this->params = (count($path) > 2) ? array_slice($path, 2) : null;               
        }
    }

    private function error404()
    {
        header("HTTP/1.0 404 Not Found");
        echo '404';
    }
}
