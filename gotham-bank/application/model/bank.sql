CREATE DATABASE bank;

CREATE TABLE `Accounts` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`username` char(20) NOT NULL,
	`password` char(80) NOT NULL,
	`salt` char(32) NOT NULL,
	`created_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Cards` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`user_id` bigint NOT NULL,
	`card_number` bigint(16) NOT NULL UNIQUE,
	`balance` bigint NOT NULL,
	`created_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Transactions` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`user_id` bigint NOT NULL,
	`to_user_id` bigint(20) NOT NULL,
	`from_card` bigint NOT NULL,
	`to_card` bigint NOT NULL,
	`count` bigint NOT NULL,
	`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`message` TEXT NOT NULL,PRIMARY KEY (`id`)
);

CREATE TABLE `Auth_strings` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`str` char(64) NOT NULL UNIQUE,
	`state` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Support` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`message` TEXT NOT NULL,
	`theme` TEXT NOT NULL,
	`user_id` bigint NOT NULL,
	`attached` TEXT NOT NULL,
	`url` TEXT NOT NULL,
	`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Userdata` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`first_name` TEXT NOT NULL,
	`second_name` TEXT NOT NULL,
	`user_id` bigint NOT NULL,
	`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Export` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`user_id` bigint NOT NULL,
	`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`type` char(20) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Actions` (
	`id` bigint NOT NULL AUTO_INCREMENT UNIQUE,
	`user_id` bigint NOT NULL,
	`action_type` TEXT NOT NULL,
	`date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

/* Credentials: support/support */
INSERT INTO Accounts (username, password, salt) VALUES ('support', 'f1d3210868537a24663fc56008e76d7ddd9c9ba6189f0ba8375229789ca6c150', '90271381');

INSERT INTO Cards (user_id, card_number, balance) VALUES (-1, 1337000000000000, 100000);

ALTER TABLE `Cards` ADD CONSTRAINT `Cards_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts`(`id`)

ALTER TABLE `Transactions` ADD CONSTRAINT `fk_from_card` FOREIGN KEY (`from_card`) REFERENCES `Cards`(`card_number`);

ALTER TABLE `Transactions` ADD CONSTRAINT `fk_to_card` FOREIGN KEY (`to_card`) REFERENCES `Cards`(`card_number`);

ALTER TABLE `Support` ADD CONSTRAINT `Support_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts`(`id`);

ALTER TABLE `Export` ADD CONSTRAINT `Export_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts`(`id`);

ALTER TABLE `Actions` ADD CONSTRAINT `Actions_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts`(`id`);

ALTER TABLE `Userdata` ADD CONSTRAINT `Userdata_fk0` FOREIGN KEY (`user_id`) REFERENCES `Accounts`(`id`);

