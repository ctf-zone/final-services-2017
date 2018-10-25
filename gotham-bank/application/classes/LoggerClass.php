<?php

namespace Bank;

class Logger extends Bank
{
	private static function getLogFilename()
	{
		$log_folder = dirname(__DIR__).DIRECTORY_SEPARATOR.'log'.DIRECTORY_SEPARATOR;
		
		if(file_exists($log_folder))
			return $log_folder.'log'.date('d_H').'.txt';
		else
			if(!mkdir($log_folder, 0744))
				return false;
	}

	public static function write($log)
	{
		$log_filename = self::getLogFilename();
		return file_put_contents($log_filename, $log, FILE_APPEND | LOCK_EX);
	}

	public static function read()
	{
		$log_filename = self::getLogFilename();

		return file_get_contents($log_filename);
	}
}
