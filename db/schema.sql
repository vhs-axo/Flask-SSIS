CREATE DATABASE IF NOT EXISTS `ssis`;
USE `ssis`;

CREATE TABLE IF NOT EXISTS `colleges` (
	`code` VARCHAR(15) NOT NULL,
    `name` VARCHAR(63) NOT NULL,
    
    PRIMARY KEY (`code`)
);

CREATE TABLE IF NOT EXISTS `programs` (
	`code` VARCHAR(15) NOT NULL,
    `name` VARCHAR(255) NOT NULL,
    `college` VARCHAR(15) NOT NULL,
    
    PRIMARY KEY (`code`),
    CONSTRAINT `FK_programs_colleges` 
		FOREIGN KEY (`college`) REFERENCES `colleges` (`code`) 
        ON UPDATE CASCADE 
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `students` (
	`id` CHAR(9) NOT NULL,
    `firstname` VARCHAR(127) NOT NULL,
	`lastname` VARCHAR(63) NOT NULL,
    `year` TINYINT UNSIGNED NOT NULL,
    `gender` ENUM('M', 'F', 'O') NOT NULL,
    `program` VARCHAR(15) DEFAULT NULL,
    
    PRIMARY KEY (`id`),
    CONSTRAINT `FK_students_programs` 
		FOREIGN KEY (`program`) REFERENCES `programs` (`code`) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
	CONSTRAINT `students_chk_id` 
		CHECK (regexp_like(`id`, '^[0-9]{4}-[0-9]{4}$')),
	CONSTRAINT `students_chk_year` 
		CHECK (((`year` >= 1) and (`year` <= 8)))
);