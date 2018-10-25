<?php

namespace Bank;

class Session extends Bank
{
	public static function sessionRegenerate()
	{
		return session_regenerate_id(true);
	}

	public static function sessionDestroy($sessionKey)
	{
		session_unset();
		unset($_SESSION[$sessionKey]);
		$result = session_destroy();

		return $result;
	}
}
