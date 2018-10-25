<?php

/**
 * Class About
 */
class About extends Controller
{
    /**
     * PAGE:
     * http://yourproject/about
     */
    public function default()
    {
        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/about.php';
        require APP . 'view/standard/include/footer.php';     
    }
}
