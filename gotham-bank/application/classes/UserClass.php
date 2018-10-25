<?php

namespace Bank;

class User extends Bank
{
	public static function credentialsCheck($username, $password)
	{

		$username = mb_strtolower(trim($username));
		$password = trim($password);

		if(Bank::validate('/^[a-z][a-z0-9]{4,20}$/', $username))
			return false;

		return array('username' => $username, 'password' => $password);
	}

	public static function getHash($algo, $password, $salt)
	{
		if(!$salt)
			return false;

		return hash($algo, $password.$salt);
	}

	public static function saltGenerate()
	{
		$strong = True;
		$bytes = openssl_random_pseudo_bytes(32, $strong);
		if($bytes)
		{
			$hex = bin2hex($bytes);
			$salt = substr($hex, 0, 32);

			return $salt;
		}

		return false;
	}

	public static function userdataCheck($userdata)
	{
		$data = array();

		foreach ($userdata as $key => $value) {
			if($key === 'fname' or $key === 'sname')
			{
				if(strlen($value) < 3 or strlen($value) > 100)
					break;
				else
					$data[$key] = $value;
			}
		}

		return (!empty($data['fname']) && !empty($data['sname']))?$data:false;
	}
}
