<?php

namespace Bank;

class Bank
{
	protected function validate($regex, $value)
	{
		if(!preg_match($regex, $value))
			return true;

		return false;
	}

	public static function exit($location): void
	{
		header('Location: '.$location);
		exit();
	}
}