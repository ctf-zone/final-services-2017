CREATE DATABASE bank;

CREATE TABLE `Accounts` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `username` char(20) NOT NULL,
  `password` char(80) NOT NULL,
  `salt` char(32) NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Auth_strings` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `str` char(64) NOT NULL,
  `state` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `str` (`str`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Cards` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `card_number` bigint(16) NOT NULL,
  `balance` bigint(20) NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `card_number` (`card_number`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Export` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` char(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `Export_fk0` (`user_id`),
  CONSTRAINT `Export_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Support` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `message` text NOT NULL,
  `theme` text NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `url` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `Support_fk0` (`user_id`),
  CONSTRAINT `Support_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Transactions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) NOT NULL,
  `to_user_id` bigint(20) NOT NULL,
  `from_card` bigint(20) NOT NULL,
  `to_card` bigint(20) NOT NULL,
  `count` bigint(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `Userdata` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first_name` text NOT NULL,
  `second_name` text NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `Userdata_fk0` (`user_id`),
  CONSTRAINT `Userdata_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

/* Credentials support / hlj1JKSD7BGV9UDALSJKDGLV125674387rbtiva-sIV */
INSERT INTO Accounts (username, password, salt) VALUES ('support', '5bd2db2a3f07ad212ab5f1a6b05e127675491f0a484cf4d22cfc57850a0f361b', '29032c0c6366a4fa8ac737b326201159');

/* Default card number for support */
INSERT INTO Cards (user_id, card_number, balance) VALUES (1, 1337000000000000, 1000000);
