<?php

class Model
{
    function __construct($db)
    {
        try {
            $this->db = $db;
        } catch (PDOException $e) {
            exit('Database connection could not be established.');
        }
    }

    public function registerAccount($username, $hash, $salt)
    {

        $sql = "INSERT INTO Accounts (username, password, salt) VALUES (:username, :password, :salt)";
        $query = $this->db->prepare($sql);
        $parameters = array(':username' => $username, ':password' => $hash, ':salt' => $salt);
 
        $query->execute($parameters);

        return $this->db->lastInsertId();
    }

    public function getAccount($username)
    {

        $sql = "SELECT * FROM Accounts WHERE BINARY username = :username";
        $query = $this->db->prepare($sql);
        $parameters = array(':username' => $username);

        $query->execute($parameters);

        return $query->fetch();
    }

    public function toSupport($message, $theme, $url, $user_id)
    {
        $sql = "INSERT INTO Support (message, theme, url, user_id) VALUES (:message, :theme, :url, $user_id)";
        $query = $this->db->prepare($sql);
        $parameters = array(':message' => $message, ':theme' => $theme, ':url' => $url);

        return $query->execute($parameters);
    }

    public function toUserData($fname, $sname, $user_id)
    {
        $sql = "INSERT INTO Userdata (first_name, second_name, user_id) VALUES (:first_name, :second_name, $user_id)";
        $query = $this->db->prepare($sql);
        $parameters = array(':first_name' => $fname, ':second_name' => $sname);

        return $query->execute($parameters);
    }

    public function getUserData($id)
    {
        $sql = "SELECT first_name, second_name FROM Userdata WHERE user_id = :id";
        $query = $this->db->prepare($sql);
        $parameters = array(':id' => $id);

        $query->execute($parameters);
        return $query->fetch();
    }

    public function changeUserData($fname, $sname, $user_id)
    {
        $sql = "UPDATE Userdata SET first_name = :first_name, second_name = :second_name WHERE user_id = :user_id";
        $query = $this->db->prepare($sql);
        $parameters = array(':first_name' => $fname, ':second_name' => $sname, ':user_id' => $user_id);

        return $query->execute($parameters);
    }

    public function getLatestCardNumber()
    {
        $sql = "SELECT card_number FROM Cards ORDER BY card_number DESC LIMIT 1";
        $query = $this->db->prepare($sql);
        $query->execute();

        return $query->fetch();
    }

    public function getCardNumbers($user_id)
    {
        $sql = "SELECT * FROM Cards WHERE user_id = $user_id";
        $query = $this->db->prepare($sql);

        $query->execute();

        return $query->fetchAll();
    }

    public function cardRegister($user_id, $card_number, $balance)
    {
        $sql = "INSERT INTO Cards (user_id, card_number, balance) VALUES ($user_id, :card_number, :balance)";
        $query = $this->db->prepare($sql);
        $parameters = array(':card_number' => $card_number, ':balance' => $balance);

        return $query->execute($parameters);
    }

    public function getUserIdbyCard($card_number)
    {
        $sql = "SELECT user_id FROM Cards WHERE card_number = :card_number";
        $query = $this->db->prepare($sql);
        $parameters = array(':card_number' => $card_number);
        
        $query->execute($parameters);

        return $query->fetch();
    }

    public function getCardNumber($user_id)
    {
        $sql = "SELECT card_number FROM Cards where user_id = $user_id";
        $query = $this->db->prepare($sql);
        
        $query->execute();
        
        return $query->fetchAll();
    }

    public function submitTransaction($transactionArray)
    {
        $sql = "INSERT INTO Transactions (user_id,from_card,to_card,count,message,to_user_id) VALUES (:user_id, :from_card, :to_card, :amount, :message, :to_user_id)";
        $query = $this->db->prepare($sql);
        $parameters =  array('user_id' => $transactionArray['user_id'],
                            'to_user_id' => $transactionArray['to_user_id'],
                            'from_card' => $transactionArray['from_card'],
                            'to_card' => $transactionArray['to_card'],
                            'amount' => $transactionArray['amount'],
                            'message' => $transactionArray['message']
                        );
        $result = $query->execute($parameters);
        
        return $this->db->lastInsertId();
    }

    public function updateBalance($card_number,$balance)
    {
        $sql = "UPDATE Cards SET balance = :balance WHERE card_number = :card_number";
        $query = $this->db->prepare($sql);
        $parameters = array('balance' =>  $balance,
                            'card_number' => $card_number
                        );

        return $query->execute($parameters);
    }

    public function getBalance($card_number)
    {
        $sql = "SELECT balance from Cards WHERE card_number = :card_number";
        $query = $this->db->prepare($sql);
        $parameters = array('card_number' =>  $card_number);

        $query->execute($parameters);

        return $query->fetch();
    }

    public function getMessagesToSupport($user_id)
    {
        $sql = "SELECT * FROM (SELECT * FROM Support WHERE user_id = $user_id ORDER BY id DESC LIMIT 5) sub ORDER BY id DESC";
        $query = $this->db->prepare($sql);

        $query->execute();

        return $query->fetchAll();
    }

    public function getTransactionsHistory($user_id)
    {
        $sql = "SELECT * FROM Transactions WHERE user_id = :user_id or to_user_id = :user_id ORDER BY `date` DESC";
        $query = $this->db->prepare($sql);
        $parameters = array('user_id' => $user_id);

        $query->execute($parameters);

        return $query->fetchAll();
    }

    public function getUsernameByCard($card_number)
    {
        $sql = "SELECT * from Userdata WHERE user_id = (SELECT user_id FROM Cards WHERE card_number = :card_number)";
        $query = $this->db->prepare($sql);
        $parameters = array('card_number' => $card_number);

        $query->execute($parameters);

        return $query->fetch();
    }

    public function getTransactionsCount($user_id)
    {
        $sql = "SELECT Count(*) FROM Transactions WHERE user_id = $user_id or to_user_id = $user_id";
        $query = $this->db->prepare($sql);

        $query->execute();

        return $query->fetch(PDO::FETCH_ASSOC)['Count(*)'];
    }

    public function getAllTransactions($user_id)
    {
        $sql = "SELECT * FROM Transactions WHERE user_id = :user_id or to_user_id = :user_id";
        $query = $this->db->prepare($sql);
        $parameters = array('user_id' => $user_id);

        $query->execute($parameters);

        return $query->fetchAll();
    }

    public function getSupportMessageById($id)
    {
        $sql = "SELECT * FROM Support WHERE id = :id";
        $query = $this->db->prepare($sql);
        $parameters = array('id' => $id);

        $query->execute($parameters);

        return $query->fetchAll();
    }

    public function getSupportMessageByUserId($user_id)
    {
        $sql = "SELECT * FROM Support WHERE user_id = :user_id AND `date` > (CURRENT_TIMESTAMP - 900)";
        $query = $this->db->prepare($sql);
        $parameters = array('user_id' => $user_id);

        $query->execute($parameters);

        return $query->fetchAll();
    }

    public function getUsersList()
    {
        $sql = "SELECT id, username, created_date FROM Accounts";
        $query = $this->db->prepare($sql);
        $query->execute();

        return $query->fetchAll();
    }

    public function getUsersData()
    {
        $sql = "SELECT first_name, second_name, user_id FROM Userdata";
        $query = $this->db->prepare($sql);
        $query->execute();

        return $query->fetchAll();
    }

    public function toExportEvents($user_id, $type)
    {
        $sql = "INSERT INTO Export (user_id, type) VALUES (:user_id, :type)";
        $query = $this->db->prepare($sql);
        $parameters = array('user_id' => $user_id, 'type' => $type);

        $result = $query->execute($parameters);

        return $result;
    }

    public function setAuthString($str, $state)
    {
        $sql = "INSERT INTO Auth_strings (str, state) VALUES (:str, :state)";
        $query = $this->db->prepare($sql);
        $parameters = array('str' => $str, 'state' => $state);

        $result = $query->execute($parameters);

        return $result;
    }

    public function getAuthString($str)
    {
        $sql = "SELECT * FROM Auth_strings WHERE BINARY str = :str";
        $query = $this->db->prepare($sql);
        $parameters = array('str' => $str);

        $query->execute($parameters);

        return $query->fetch();
    }

    public function getSupportsMessages()
    {
        $sql = "SELECT * FROM Support WHERE `date` > (CURRENT_TIMESTAMP - 900)";
        $query = $this->db->prepare($sql);

        $query->execute();

        return $query->fetchAll();
    }

    public function changeStateOfAuthString($str)
    {
        $sql = "UPDATE Auth_strings SET state = 1 WHERE BINARY str = :str";
        $query = $this->db->prepare($sql);
        $parameters = array('str' => $str);

        return $query->execute($parameters);
    }
}
