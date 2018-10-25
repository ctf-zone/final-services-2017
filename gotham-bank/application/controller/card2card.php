<?php

require dirname(__DIR__).'/classes/autoload.php';

use Bank\Bank as Bank;
use Bank\Logger as Logger;

/**
 * Class Card2card
 */
class Card2card extends Controller
{

    /**
     * PAGE: 
     * http://yourproject/card2card
     */
    public function default()
    {

        if (!$this->authTest())
            Bank::exit('/');

        $error = (!empty($_GET['error']))?trim($_GET['error']):'';

        $cards = $_SESSION['userdata']['card_numbers'];

        $history = Array();
        $transactions = $this->model->getTransactionsHistory($_SESSION['userdata']['id']);

        for($i = 0; $i < count($transactions); $i++)
        {
            foreach ($transactions[$i] as $key => $value) {
                $history[$i][$key] = $value;
                if($key === 'to_card')
                {
                    $username = $this->model->getUsernameByCard($value);
                    if($username)
                        $username = $username->first_name.' '.$username->second_name;
                    else
                        $username = '';

                    $history[$i]['to_card_username'] = $username;
                }
                elseif($key === 'from_card')
                {
                    $username = $this->model->getUsernameByCard($value);
                    if($username)
                        $username = $username->first_name.' '.$username->second_name;
                    else
                        $username = '';

                    $history[$i]['from_card_username'] = $username;
                }
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/card2card.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function ismycard($card_number = 0)
    {
        if (!$this->authTest())
            Bank::exit('/');

        $user_id = $this->model->getUserIdByCard($card_number);
        if (isset($user_id->user_id) && ($user_id->user_id == $_SESSION['userdata']['id']))
            return True;
        else
            return False;
    }

    public function iscardexist($card_number = 0)
    {
        if (!$this->authTest())
            Bank::exit('/');

        $user_id = $this->model->getUserIdByCard($card_number);
        if(isset($user_id->user_id))
            return True;
        else
            return False;
    }

    public function prepare()
    {
        if (!$this->authTest())
            Bank::exit('/');
        elseif(!empty($_POST['from_card']) && !empty($_POST['to_card']) && !empty($_POST['amount']))
        {
            if(!is_array($_POST['to_card']))
            {
                $user_id = $this->model->getUserIdByCard($_POST['to_card']);

                if(!isset($user_id->user_id))
                {
                    $error = 'Wrong card number!';
                    Bank::exit('/card2card?error='.$error);
                }

                $userdata = $this->model->getUserData($user_id->user_id);

                $payment_info = array('from_card' => $_POST['from_card'],
                                    'to_card' => $_POST['to_card'],
                                    'amount' => (int)$_POST['amount']
                                );
            }
            else
            {
                $error = 'Error, please try again';
                Bank::exit('/card2card?error='.$error);
            }
        }
        else
        {
            $error = "All the fields are required!";
            Bank::exit('/card2card?error='.$error);
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/payment_info.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function submit()
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif(!empty($_POST['from_card']) && !empty($_POST['to_card']) && !empty($_POST['amount']))
        {
            if(!is_array($_POST['from_card']) && !is_array($_POST['to_card']))
            {
                $from_card = (int)$_POST['from_card'];
                $to_card = (int)$_POST['to_card'];
                $amount = (int)$_POST['amount'];

                if($this->ismycard($from_card) && $this->iscardexist($to_card) && $to_card !== $from_card)
                {
                    $from_card_balance = $this->model->getBalance($from_card);
                    $to_card_balance = $this->model->getBalance($to_card);

                    if ($amount > 0 && $from_card_balance->balance >= $amount)
                    {
                        $to_user_id = $this->model->getUserIdByCard($_POST['to_card']);
                        $transactionArray = array('user_id' => $_SESSION['userdata']['id'],
                                                'from_card' => $from_card,
                                                'to_card' => $to_card,
                                                'amount' => $amount,
                                                'message' => $_POST['message'],
                                                'to_user_id' => $to_user_id->user_id
                                            );

                        $from_new_balance = $from_card_balance->balance - $transactionArray['amount'];
                        $to_new_balance = $to_card_balance->balance + $transactionArray['amount'];
                        
                        $result = $this->model->submitTransaction($transactionArray);
                        if ($result)
                        {
                            $this->model->updateBalance($transactionArray['from_card'], $from_new_balance);
                            $this->model->updateBalance($transactionArray['to_card'], $to_new_balance);

                            $status = 'Transaction succeed';

                            $to_log = $status.": #ID ".$result.", ".implode(', ', $transactionArray)."\n";
                            $a = Logger::write($to_log);
                        }
                        else 
                        {
                            $status = "Transaction failed: Internal error";
                            Bank::exit('/card2card?error='.$status);
                        }
                    }
                    else
                    {
                        $status = "Transaction failed: Bad amount for transaction";
                        Bank::exit('/card2card?error='.$status);
                    }
                }
                else
                {
                    $status = "Transaction failed: Bad cards";
                    Bank::exit('/card2card?error='.$status);
                }
            }
            else
            {
               $status = "Transaction failed: error, try again";
                Bank::exit('/card2card?error='.$status); 
            }
        }
        else
        {
            $status = "Transaction failed: all fields are required";
            Bank::exit('/card2card?error='.$status);
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/submit_payment.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function export()
    {
        if (!$this->authTest())
            Bank::exit('/');
        elseif(!empty($_REQUEST['export']) & !empty($_REQUEST['id']))
        {
            if($_REQUEST['export'] === 'CSV')
            {
                $transactions = $this->model->getAllTransactions($_REQUEST['id']);

                $csvArray = array(
                    array('id', 'From card', 'To card', 'Count', 'Date', 'Message' )
                );

                if($transactions)
                {
                    $this->model->toExportEvents($_SESSION['userdata']['id'], $_REQUEST['export']);

                    header('Content-Type: application/excel');
                    header('Content-Disposition: attachment; filename="file.csv"');

                    foreach($transactions as $transaction)
                    {
                        $tempArray = array(
                            $transaction->id,
                            $transaction->from_card, 
                            $transaction->to_card,
                            $transaction->count,
                            $transaction->date,
                            $transaction->message
                        );

                        $csvArray[] = $tempArray;
                    }

                    $fp = fopen('php://output', 'w');

                    foreach($csvArray as $row)
                        fputcsv($fp, $row);

                    fclose($fp);
                    exit;
                }
                else
                    Bank::exit('/card2card');
            }
            elseif($_REQUEST['export'] === 'XML')
            {

                $transactions = $this->model->getAllTransactions($_REQUEST['id']);

                if($transactions)
                {
                    $this->model->toExportEvents($_SESSION['userdata']['id'], $_REQUEST['export']);

                    $xmlArray = array('from_card', 'to_card', 'count', 'date', 'message');

                    $xml = new XMLWriter();
                    $xml->openMemory();
                    $xml->startDocument('1.0', 'UTF-8');
                    $xml->setIndent(true);
                        $xml->startElement('transactions');
                            foreach ($transactions as $transaction)
                            {
                                $xml->startElement('transaction');
                                foreach ($transaction as $key => $value)
                                {
                                    $xml->startElement($key);
                                        $xml->writeRaw($value);
                                    $xml->endElement();
                                }
                                $xml->endElement();
                            }
                        $xml->endElement();
                    $xml->endDocument();
                    $xml = $xml->outputMemory();

                    header('Content-Type: application/xml');

                    $fp = fopen('php://output', 'w');
                    fwrite($fp, $xml);
                    fclose($fp);

                    exit;
                }
                else
                    Bank::exit('/card2card');
            }
        }

        require APP . 'view/standard/include/header.php';
        require APP . 'view/standard/export.php';
        require APP . 'view/standard/include/footer.php';
    }

    public function transactionhistory($user_id = 0)
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif(!empty($user_id) && is_numeric($user_id))
        {
            $transactions = $this->model->getTransactionsHistory($user_id);
            if($transactions)
            {
                echo json_encode(array('transactions' => $transactions));
            }
            else
                echo json_encode(array('error' => 'not found'));
        }
    }

    public function getransactionlogs()
    {
        if(!$this->authTest())
            Bank::exit('/');
        elseif($_SERVER['REMOTE_ADDR'] == $_SERVER['SERVER_ADDR'] || $_SESSION['userdata']['id'] === 1)
            echo Logger::read();
    }
}
