-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema adsats_database
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `adsats_database` ;

-- -----------------------------------------------------
-- Schema adsats_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `adsats_database` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `adsats_database` ;

-- -----------------------------------------------------
-- Table `adsats_database`.`staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`staff` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`staff` (
  `staff_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `staff_name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `staff_id_UNIQUE` USING BTREE ON `adsats_database`.`staff` (`staff_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `email_UNIQUE` USING BTREE ON `adsats_database`.`staff` (`email`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `staff_name_idx` USING BTREE ON `adsats_database`.`staff` (`staff_name`) INVISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`aircraft`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`aircraft` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`aircraft` (
  `aircraft_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `aircraft_name` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `description` TEXT NULL,
  PRIMARY KEY (`aircraft_id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `aircraft_id_UNIQUE` USING BTREE ON `adsats_database`.`aircraft` (`aircraft_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `aircraft_name_UNIQUE` USING BTREE ON `adsats_database`.`aircraft` (`aircraft_name`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`aircraft_staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`aircraft_staff` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`aircraft_staff` (
  `aircraft_id` INT UNSIGNED NOT NULL,
  `staff_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`aircraft_id`, `staff_id`),
  CONSTRAINT `fk_aircraft_staff_aircraft`
    FOREIGN KEY (`aircraft_id`)
    REFERENCES `adsats_database`.`aircraft` (`aircraft_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_aircraft_staff_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_staff_staff_idx` USING BTREE ON `adsats_database`.`aircraft_staff` (`staff_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_staff_aircraft_idx` USING BTREE ON `adsats_database`.`aircraft_staff` (`aircraft_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`roles` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`roles` (
  `role_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `description` TEXT NULL,
  PRIMARY KEY (`role_id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `role_id_UNIQUE` USING BTREE ON `adsats_database`.`roles` (`role_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `role_name_UNIQUE` USING BTREE ON `adsats_database`.`roles` (`role_name`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`roles_staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`roles_staff` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`roles_staff` (
  `role_id` INT UNSIGNED NOT NULL,
  `staff_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`role_id`, `staff_id`),
  CONSTRAINT `fk_roles_staff_roles`
    FOREIGN KEY (`role_id`)
    REFERENCES `adsats_database`.`roles` (`role_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_roles_staff_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_roles_staff_staff_idx` ON `adsats_database`.`roles_staff` (`staff_id` ASC) INVISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_roles_staff_role_idx` USING BTREE ON `adsats_database`.`roles_staff` (`role_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`categories` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`categories` (
  `category_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `description` TEXT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `category_id_UNIQUE` USING BTREE ON `adsats_database`.`categories` (`category_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `category_name_UNIQUE` USING BTREE ON `adsats_database`.`categories` (`category_name`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`subcategories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`subcategories` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`subcategories` (
  `subcategory_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `subcategory_name` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `description` TEXT NULL,
  `category_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`subcategory_id`, `category_id`),
  CONSTRAINT `fk_subcategories_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `adsats_database`.`categories` (`category_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `subcategory_id_UNIQUE` USING BTREE ON `adsats_database`.`subcategories` (`subcategory_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `subcategory_name_UNIQUE` USING BTREE ON `adsats_database`.`subcategories` (`subcategory_name`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_subcategories_category_idx` USING BTREE ON `adsats_database`.`subcategories` (`category_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`documents` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`documents` (
  `document_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `document_name` VARCHAR(255) NOT NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `staff_id` INT UNSIGNED NULL,
  `subcategory_id` INT UNSIGNED NULL,
  PRIMARY KEY (`document_id`),
  CONSTRAINT `fk_documents_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE SET NULL,
  CONSTRAINT `fk_documents_subcategories`
    FOREIGN KEY (`subcategory_id`)
    REFERENCES `adsats_database`.`subcategories` (`subcategory_id`)
    ON DELETE CASCADE
    ON UPDATE SET NULL)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `document_id_UNIQUE` USING BTREE ON `adsats_database`.`documents` (`document_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `document_name_idx` USING BTREE ON `adsats_database`.`documents` (`document_name`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_documents_staff_idx` USING BTREE ON `adsats_database`.`documents` (`staff_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_documents_subcategories_idx` USING BTREE ON `adsats_database`.`documents` (`subcategory_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`aircraft_documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`aircraft_documents` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`aircraft_documents` (
  `aircraft_id` INT UNSIGNED NOT NULL,
  `document_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`aircraft_id`, `document_id`),
  CONSTRAINT `fk_aircraft_documents_aircraft`
    FOREIGN KEY (`aircraft_id`)
    REFERENCES `adsats_database`.`aircraft` (`aircraft_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_aircraft_documents_documents`
    FOREIGN KEY (`document_id`)
    REFERENCES `adsats_database`.`documents` (`document_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_documents_document_idx` USING BTREE ON `adsats_database`.`aircraft_documents` (`document_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_documents_aircraft_idx` ON `adsats_database`.`aircraft_documents` (`aircraft_id` ASC) INVISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`access_levels`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`access_levels` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`access_levels` (
  `access_level_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `access_level_name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`access_level_id`))
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `access_level_id_UNIQUE` USING BTREE ON `adsats_database`.`access_levels` (`access_level_id`) VISIBLE;

SHOW WARNINGS;
CREATE UNIQUE INDEX `access_level_name_UNIQUE` USING BTREE ON `adsats_database`.`access_levels` (`access_level_name`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`staff_subcategories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`staff_subcategories` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`staff_subcategories` (
  `staff_id` INT UNSIGNED NOT NULL,
  `subcategory_id` INT UNSIGNED NOT NULL,
  `access_level_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`staff_id`, `subcategory_id`),
  CONSTRAINT `fk_staff_subcategories_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_staff_subcategories_access_levels`
    FOREIGN KEY (`access_level_id`)
    REFERENCES `adsats_database`.`access_levels` (`access_level_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_staff_subcategories_subcategories`
    FOREIGN KEY (`subcategory_id`)
    REFERENCES `adsats_database`.`subcategories` (`subcategory_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_staff_subcategories_staff_idx` USING BTREE ON `adsats_database`.`staff_subcategories` (`staff_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_staff_subcategories_access_level_idx` USING BTREE ON `adsats_database`.`staff_subcategories` (`access_level_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_staff_subcategories_subcategories_idx` USING BTREE ON `adsats_database`.`staff_subcategories` (`subcategory_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`notices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`notices` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`notices` (
  `notice_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `subject` VARCHAR(255) NOT NULL,
  `type` VARCHAR(255) NOT NULL,
  `staff_id` INT UNSIGNED NULL,
  `archived` TINYINT NOT NULL DEFAULT 0,
  `details` JSON NOT NULL,
  `noticed_at` TIMESTAMP NULL COMMENT 'If null means has not been issued\nelse means has been issued',
  `deadline_at` TIMESTAMP NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`notice_id`),
  CONSTRAINT `fk_notices_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE SET NULL)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE UNIQUE INDEX `notice_id_UNIQUE` USING BTREE ON `adsats_database`.`notices` (`notice_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `subject` USING BTREE ON `adsats_database`.`notices` (`subject`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_notices_staff_idx` USING BTREE ON `adsats_database`.`notices` (`staff_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`aircraft_notices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`aircraft_notices` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`aircraft_notices` (
  `aircraft_id` INT UNSIGNED NOT NULL,
  `notice_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`aircraft_id`, `notice_id`),
  CONSTRAINT `fk_aircraft_notices_aircraft`
    FOREIGN KEY (`aircraft_id`)
    REFERENCES `adsats_database`.`aircraft` (`aircraft_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_aircraft_notices_notices`
    FOREIGN KEY (`notice_id`)
    REFERENCES `adsats_database`.`notices` (`notice_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_notices_notice_idx` ON `adsats_database`.`aircraft_notices` (`notice_id` ASC) INVISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_aircraft_notices_aircraft_idx` USING BTREE ON `adsats_database`.`aircraft_notices` (`aircraft_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`documents_notices`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`documents_notices` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`documents_notices` (
  `notice_id` INT UNSIGNED NOT NULL,
  `document_name` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notice_id`, `document_name`),
  CONSTRAINT `fk_documents_notices_notices`
    FOREIGN KEY (`notice_id`)
    REFERENCES `adsats_database`.`notices` (`notice_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_documents_notices_notices_idx` USING BTREE ON `adsats_database`.`documents_notices` (`notice_id`) VISIBLE;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `adsats_database`.`notices_staff`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `adsats_database`.`notices_staff` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `adsats_database`.`notices_staff` (
  `notice_id` INT UNSIGNED NOT NULL,
  `staff_id` INT UNSIGNED NOT NULL,
  `read_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`notice_id`, `staff_id`),
  CONSTRAINT `fk_notices_staff_notices`
    FOREIGN KEY (`notice_id`)
    REFERENCES `adsats_database`.`notices` (`notice_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_notices_staff_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `adsats_database`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;
CREATE INDEX `fk_notices_staff_staff_idx` USING BTREE ON `adsats_database`.`notices_staff` (`staff_id`) VISIBLE;

SHOW WARNINGS;
CREATE INDEX `fk_notices_staff_notice_idx` USING BTREE ON `adsats_database`.`notices_staff` (`notice_id`) VISIBLE;

SHOW WARNINGS;
USE `adsats_database`;

DELIMITER $$

USE `adsats_database`$$
DROP TRIGGER IF EXISTS `adsats_database`.`roles_BEFORE_UPDATE` $$
SHOW WARNINGS$$
USE `adsats_database`$$
CREATE DEFINER = CURRENT_USER TRIGGER `adsats_database`.`roles_BEFORE_UPDATE` BEFORE UPDATE ON `roles` FOR EACH ROW
BEGIN
	DECLARE msg VARCHAR(255);
    IF OLD.role_id IN (0, 1) THEN  -- specific ids need to protect
        SET msg = CONCAT('Cannot update row with id ', OLD.role_id, '. Update restricted.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END$$

SHOW WARNINGS$$

USE `adsats_database`$$
DROP TRIGGER IF EXISTS `adsats_database`.`roles_BEFORE_DELETE` $$
SHOW WARNINGS$$
USE `adsats_database`$$
CREATE DEFINER = CURRENT_USER TRIGGER `adsats_database`.`roles_BEFORE_DELETE` BEFORE DELETE ON `roles` FOR EACH ROW
BEGIN
	DECLARE msg VARCHAR(255);
    IF OLD.role_id IN (0, 1) THEN  -- specific ids need to protect
        SET msg = CONCAT('Cannot delete row with id ', OLD.role_id, '. Deletion restricted.');
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
    END IF;
END$$

SHOW WARNINGS$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `adsats_database`.`staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Student', 'student@example.com', 0, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Rikki O\'Neil', 'roneil0@dagondesign.com', false, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Milo Patterfield', 'mpatterfield1@youku.com', false, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Galvan Dahlback', 'gdahlback2@friendfeed.com', true, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Elyn Johl', 'ejohl3@java.com', false, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`staff` (`staff_id`, `staff_name`, `email`, `archived`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Gris Costanza', 'gcostanza4@latimes.com', true, DEFAULT, DEFAULT);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`aircraft`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`aircraft` (`aircraft_id`, `aircraft_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'VQ-BOS', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`aircraft` (`aircraft_id`, `aircraft_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'VP-BLU', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`aircraft` (`aircraft_id`, `aircraft_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'AB-CDE', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`aircraft` (`aircraft_id`, `aircraft_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'FG-HIJ', 1, DEFAULT, DEFAULT, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`aircraft_staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (3, 1);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (4, 1);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (2, 2);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (2, 3);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (3, 3);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (2, 4);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (3, 4);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (4, 4);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (1, 5);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (2, 5);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (4, 5);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (1, 6);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (2, 6);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (3, 6);
INSERT INTO `adsats_database`.`aircraft_staff` (`aircraft_id`, `staff_id`) VALUES (4, 6);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`roles`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Administrator', 0, DEFAULT, DEFAULT, 'Administrator privileges');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Editor', 0, DEFAULT, DEFAULT, 'Editor Privileges');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Cabin attendants', 0, DEFAULT, DEFAULT, 'The individual that attends to passengers safety and comfort while in flight.');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'engineers', 0, DEFAULT, DEFAULT, 'A person who designs builds or maintains engines machines or structures');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Pilots', 0, DEFAULT, DEFAULT, 'A person who operates the flying controls of an aircraft.');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Safety officer', 0, DEFAULT, DEFAULT, 'The person who is responsible for the safety of the people who work or visit there.');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Test Row 6', 0, DEFAULT, DEFAULT, 'Test Row 6 description');
INSERT INTO `adsats_database`.`roles` (`role_id`, `role_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Test Row 7', 1, DEFAULT, DEFAULT, 'Test Row 7 description');

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`roles_staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (1, 1);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (1, 4);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (1, 5);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (1, 6);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (3, 2);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (3, 3);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (3, 4);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (3, 5);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (3, 6);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (4, 1);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (4, 2);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (4, 3);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (4, 4);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (5, 1);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (5, 3);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (5, 4);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (5, 5);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (5, 6);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 1);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 2);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 3);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 4);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 5);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (6, 6);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (7, 2);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (7, 3);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (7, 5);
INSERT INTO `adsats_database`.`roles_staff` (`role_id`, `staff_id`) VALUES (7, 6);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`categories`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Aircraft', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Audit', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Crew documents', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Purchase orders', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Safety management system', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'BCAA', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Test category 6', 0, DEFAULT, DEFAULT, NULL);
INSERT INTO `adsats_database`.`categories` (`category_id`, `category_name`, `archived`, `created_at`, `updated_at`, `description`) VALUES (DEFAULT, 'Test category 7', 1, DEFAULT, DEFAULT, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`subcategories`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Aircraft approvals - certificates and documents', 0, DEFAULT, DEFAULT, NULL, 1);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Aircraft manuals', 0, DEFAULT, DEFAULT, NULL, 1);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Audit program', 0, DEFAULT, DEFAULT, NULL, 2);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'BCAA aircraft occurence reports', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'BCAA audits', 0, DEFAULT, DEFAULT, NULL, 2);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Change management', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Fatigue management', 0, DEFAULT, DEFAULT, NULL, 1);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Ground training', 0, DEFAULT, DEFAULT, NULL, 3);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Licence and approvals', 0, DEFAULT, DEFAULT, NULL, 3);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Safety review board', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Purchase orders', 0, DEFAULT, DEFAULT, NULL, 4);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Safety notice', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Notice to crew', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Hazard notice', 0, DEFAULT, DEFAULT, NULL, 5);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'HR documents', 0, DEFAULT, DEFAULT, NULL, 3);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'BCAA aircarft occurrence report', 0, DEFAULT, DEFAULT, NULL, 7);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Test subcategory 17', 0, DEFAULT, DEFAULT, NULL, 1);
INSERT INTO `adsats_database`.`subcategories` (`subcategory_id`, `subcategory_name`, `archived`, `created_at`, `updated_at`, `description`, `category_id`) VALUES (DEFAULT, 'Test subcategory 18', 1, DEFAULT, DEFAULT, NULL, 2);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`documents`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'UtMassaQuis.txt', false, DEFAULT, DEFAULT, 6, 16);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Cursus.pdf', true, DEFAULT, DEFAULT, 6, 3);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'FusceLacusPurus.mpeg', false, DEFAULT, DEFAULT, 4, 5);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'QuisqueArcu.avi', false, DEFAULT, DEFAULT, NULL, 4);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Ut.mp3', false, DEFAULT, DEFAULT, 2, NULL);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'IpsumPraesentBlandit.xls', true, DEFAULT, DEFAULT, 5, 8);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'PortaVolutpat.tiff', false, DEFAULT, DEFAULT, 1, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Congue.avi', false, DEFAULT, DEFAULT, 4, 5);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EuEstCongue.mp3', false, DEFAULT, DEFAULT, 2, 13);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'DapibusNullaSuscipit.mov', true, DEFAULT, DEFAULT, 2, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'JustoNec.doc', false, DEFAULT, DEFAULT, 6, 12);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'HacHabitassePlatea.txt', true, DEFAULT, DEFAULT, 6, NULL);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'AtVelit.mp3', false, DEFAULT, DEFAULT, 4, 11);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'AmetLobortisSapien.ppt', true, DEFAULT, DEFAULT, 3, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'ASuscipitNulla.avi', false, DEFAULT, DEFAULT, 1, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Tincidunt.png', true, DEFAULT, DEFAULT, 2, 16);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Nunc.ppt', true, DEFAULT, DEFAULT, 5, 8);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Primis.mp3', true, DEFAULT, DEFAULT, 2, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'HabitassePlateaDictumst.avi', false, DEFAULT, DEFAULT, 4, 4);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'LacusMorbiQuis.txt', false, DEFAULT, DEFAULT, 5, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Nulla.mp3', false, DEFAULT, DEFAULT, 2, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'MaurisEnim.xls', false, DEFAULT, DEFAULT, 4, 18);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'LeoPellentesqueUltrices.mpeg', false, DEFAULT, DEFAULT, 3, NULL);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Imperdiet.ppt', false, DEFAULT, DEFAULT, 4, 1);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EgetTempusVel.ppt', false, DEFAULT, DEFAULT, 3, 1);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'PurusAliquet.jpeg', true, DEFAULT, DEFAULT, 2, 11);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Condimentum.mp3', true, DEFAULT, DEFAULT, 5, 16);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Blandit.avi', false, DEFAULT, DEFAULT, 6, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'QuamAOdio.mp3', false, DEFAULT, DEFAULT, 5, NULL);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'ErosElementumPellentesque.xls', false, DEFAULT, DEFAULT, 6, 11);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Venenatis.avi', true, DEFAULT, DEFAULT, 3, 5);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Sagittis.avi', true, DEFAULT, DEFAULT, 2, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EuMiNulla.pdf', false, DEFAULT, DEFAULT, 6, 18);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'RutrumRutrum.avi', true, DEFAULT, DEFAULT, 4, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'CommodoPlaceratPraesent.avi', true, DEFAULT, DEFAULT, 1, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Metus.avi', true, DEFAULT, DEFAULT, 3, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Sodales.tiff', false, DEFAULT, DEFAULT, 5, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Molestie.xls', true, DEFAULT, DEFAULT, 1, 2);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'IdOrnare.gif', true, DEFAULT, DEFAULT, 6, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'ConsequatLectus.ppt', true, DEFAULT, DEFAULT, 4, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'HacHabitasse.jpeg', false, DEFAULT, DEFAULT, 6, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'BlanditUltrices.ppt', true, DEFAULT, DEFAULT, NULL, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'TempusSemperEst.mp3', true, DEFAULT, DEFAULT, 5, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'AnteIpsum.avi', false, DEFAULT, DEFAULT, 1, 2);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'CubiliaCuraeNulla.mp3', false, DEFAULT, DEFAULT, NULL, 13);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Rutrum.pdf', true, DEFAULT, DEFAULT, 4, 2);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'BibendumFelis.tiff', false, DEFAULT, DEFAULT, 6, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'BlanditNamNulla.avi', true, DEFAULT, DEFAULT, 6, 4);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'RhoncusDui.mp3', false, DEFAULT, DEFAULT, 3, 16);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EleifendQuamA.mp3', false, DEFAULT, DEFAULT, 2, 1);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'PlaceratAnte.xls', false, DEFAULT, DEFAULT, 3, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Sapien.xls', true, DEFAULT, DEFAULT, 1, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'UltricesPosuere.mp3', false, DEFAULT, DEFAULT, 4, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SapienIaculisCongue.mp3', true, DEFAULT, DEFAULT, 6, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Turpis.png', true, DEFAULT, DEFAULT, 5, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SitAmet.pdf', true, DEFAULT, DEFAULT, 1, 3);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EratNullaTempus.pdf', false, DEFAULT, DEFAULT, 5, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'MetusAeneanFermentum.ppt', false, DEFAULT, DEFAULT, 1, 13);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'NecDuiLuctus.png', true, DEFAULT, DEFAULT, 6, 11);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SodalesScelerisqueMauris.avi', false, DEFAULT, DEFAULT, 4, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'VolutpatConvallis.jpeg', false, DEFAULT, DEFAULT, 1, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Felis.mp3', true, DEFAULT, DEFAULT, 2, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Curae.tiff', true, DEFAULT, DEFAULT, 1, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SemPraesent.pdf', false, DEFAULT, DEFAULT, 6, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'InHac.pdf', false, DEFAULT, DEFAULT, 4, 18);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Sit.txt', true, DEFAULT, DEFAULT, 6, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'MaecenasLeo.doc', true, DEFAULT, DEFAULT, 2, 5);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'DuiMaecenasTristique.avi', false, DEFAULT, DEFAULT, 6, 4);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Elementum.jpeg', true, DEFAULT, DEFAULT, 2, 16);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Ligula.mp3', true, DEFAULT, DEFAULT, 5, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'MorbiNon.avi', false, DEFAULT, DEFAULT, 6, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'A.ppt', true, DEFAULT, DEFAULT, 2, 8);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'DictumstMaecenasUt.txt', false, DEFAULT, DEFAULT, 6, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EgetNuncDonec.tiff', false, DEFAULT, DEFAULT, 4, 2);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'JustoEtiamPretium.xls', false, DEFAULT, DEFAULT, 5, 10);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SedLacus.avi', false, DEFAULT, DEFAULT, 3, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'LoremVitae.ppt', true, DEFAULT, DEFAULT, 1, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Donec.png', false, DEFAULT, DEFAULT, 6, 17);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Penatibus.avi', true, DEFAULT, DEFAULT, 6, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'NecCondimentum.ppt', true, DEFAULT, DEFAULT, 2, 8);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Diam.xls', true, DEFAULT, DEFAULT, 3, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'QuisqueErat.avi', false, DEFAULT, DEFAULT, NULL, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'VelIpsumPraesent.mp3', false, DEFAULT, DEFAULT, 6, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Erat.jpeg', true, DEFAULT, DEFAULT, 3, 12);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'JustoLacinia.avi', true, DEFAULT, DEFAULT, 1, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Feugiat.jpeg', false, DEFAULT, DEFAULT, 5, 6);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SuscipitAFeugiat.avi', true, DEFAULT, DEFAULT, 6, 3);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'EratIdMauris.txt', true, DEFAULT, DEFAULT, 4, 3);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Eros.xls', true, DEFAULT, DEFAULT, 3, 14);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Aenean.mov', true, DEFAULT, DEFAULT, 1, 9);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'SedNisl.avi', true, DEFAULT, DEFAULT, 6, 18);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Quis.avi', false, DEFAULT, DEFAULT, 4, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Tortor.mp3', false, DEFAULT, DEFAULT, 3, 4);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'MiInteger.doc', true, DEFAULT, DEFAULT, 4, 12);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'IntegerPedeJusto.ppt', false, DEFAULT, DEFAULT, 6, 7);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'NullaDapibusDolor.avi', false, DEFAULT, DEFAULT, 6, 13);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Aliquam.mpeg', false, DEFAULT, DEFAULT, 1, 15);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Donec.mpeg', true, DEFAULT, DEFAULT, 1, 5);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Tristique.mov', false, DEFAULT, DEFAULT, 6, 12);
INSERT INTO `adsats_database`.`documents` (`document_id`, `document_name`, `archived`, `created_at`, `updated_at`, `staff_id`, `subcategory_id`) VALUES (DEFAULT, 'Luctus.gif', false, DEFAULT, DEFAULT, 5, 7);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`aircraft_documents`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 1);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 1);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 5);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 11);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 11);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 13);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 13);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 15);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 15);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 16);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 16);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 17);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 17);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 18);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 19);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 19);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 20);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 20);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 23);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 24);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 24);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 26);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 27);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 28);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 31);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 33);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 33);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 35);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 36);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 37);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 37);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 38);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 40);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 41);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 41);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 42);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 42);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 45);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 48);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 50);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 51);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 52);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 53);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 53);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 54);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 55);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 56);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 56);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 57);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 57);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 59);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 63);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 63);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 66);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 68);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 68);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 73);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 73);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 75);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 75);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 76);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 76);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 76);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 77);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 77);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 78);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 79);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 81);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 82);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 85);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 88);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 89);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (3, 89);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 90);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 93);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 94);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (2, 95);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (4, 97);
INSERT INTO `adsats_database`.`aircraft_documents` (`aircraft_id`, `document_id`) VALUES (1, 100);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`access_levels`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`access_levels` (`access_level_id`, `access_level_name`) VALUES (DEFAULT, 'No access');
INSERT INTO `adsats_database`.`access_levels` (`access_level_id`, `access_level_name`) VALUES (DEFAULT, 'Read-only');
INSERT INTO `adsats_database`.`access_levels` (`access_level_id`, `access_level_name`) VALUES (DEFAULT, 'Full-access');

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`staff_subcategories`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 3, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 4, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 8, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 3, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 11, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 14, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 17, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 4, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 14, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 18, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 11, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 12, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 18, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 13, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (6, 1, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (6, 2, 1);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 2, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 5, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 7, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 11, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 15, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 9, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 16, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 18, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 9, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 10, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 6, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 17, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 4, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 5, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 8, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (6, 4, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (6, 5, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (6, 8, 2);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 1, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (1, 17, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 1, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (2, 7, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 1, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (3, 8, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 4, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 5, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 13, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (4, 15, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 10, 3);
INSERT INTO `adsats_database`.`staff_subcategories` (`staff_id`, `subcategory_id`, `access_level_id`) VALUES (5, 17, 3);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`notices`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Monitored needs-based standardization', 'Safety hazard', 1, true, '{}', '2015-05-02 16:45:51', '2015-05-09 16:45:51', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Polarised foreground attitude', 'Hazard notice', 1, false, '{}', '2011-03-03 00:03:46', '2011-03-10 00:03:46', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Robust 3rd generation hardware', 'Hazard notice', 1, false, '{}', '2021-12-17 19:54:08', '2021-12-24 19:54:08', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Devolved 24/7 methodology', 'Notice to crew', 1, false, '{}', '2019-10-24 21:06:34', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Enterprise-wide eco-centric installation', 'Notice to crew', 1, false, '{}', '2012-12-25 09:05:32', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Automated eco-centric forecast', 'Safety hazard', 1, false, '{}', '2020-07-19 02:29:50', '2020-07-26 02:29:50', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Sharable didactic budgetary management', 'Safety hazard', 1, true, '{}', '2013-05-30 15:05:43', '2013-06-06 15:05:43', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Programmable background hierarchy', 'Notice to crew', 1, false, '{}', '2021-06-27 10:38:13', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Optional intermediate synergy', 'Notice to crew', 1, false, '{}', '2019-07-22 04:36:06', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Business-focused client-driven secured line', 'Hazard notice', 1, true, '{}', '2021-05-30 20:12:46', '2021-06-06 20:12:46', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Down-sized national structure', 'Hazard notice', 1, true, '{}', '2020-05-14 12:37:12', '2020-05-21 12:37:12', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Phased discrete definition', 'Safety hazard', 1, true, '{}', '2019-05-30 02:41:07', '2019-06-06 02:41:07', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Ergonomic coherent approach', 'Safety hazard', 1, true, '{}', '2022-02-08 14:43:19', '2022-02-15 14:43:19', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Re-contextualized disintermediate circuit', 'Safety hazard', 1, false, '{}', '2008-07-06 09:53:30', '2008-07-13 09:53:30', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'User-centric directional support', 'Safety hazard', 1, false, '{}', '2014-01-19 14:33:39', '2014-01-26 14:33:39', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Organized exuding access', 'Notice to crew', 1, true, '{}', '2020-09-28 10:23:00', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'User-friendly well-modulated firmware', 'Notice to crew', 1, false, '{}', '2019-06-24 11:01:24', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Sharable dynamic capacity', 'Notice to crew', 1, true, '{}', '2022-08-07 12:35:05', NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Distributed next generation focus group', 'Safety hazard', 1, true, '{}', '2008-10-15 13:54:58', '2008-10-22 13:54:58', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices` (`notice_id`, `subject`, `type`, `staff_id`, `archived`, `details`, `noticed_at`, `deadline_at`, `created_at`, `updated_at`) VALUES (DEFAULT, 'Integrated hybrid hierarchy', 'Safety hazard', 1, false, '{}', '2019-05-31 07:24:10', '2019-06-07 07:24:10', DEFAULT, DEFAULT);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`aircraft_notices`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 1);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 5);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 8);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 12);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 13);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 17);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 18);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 19);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (1, 20);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 2);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 4);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 5);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 6);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 8);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 10);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (2, 13);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (3, 1);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (3, 8);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (3, 9);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (3, 14);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (3, 17);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 3);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 4);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 5);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 7);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 9);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 17);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 18);
INSERT INTO `adsats_database`.`aircraft_notices` (`aircraft_id`, `notice_id`) VALUES (4, 19);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`documents_notices`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (7, 'QuisqueUt.avi', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (15, 'EstQuamPharetra.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (4, 'In.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (10, 'UtMaurisEget.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (7, 'PedeVenenatisNon.doc', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (19, 'InFaucibusOrci.ppt', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (13, 'Aliquet.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (5, 'EgetElit.png', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (5, 'Ut.ppt', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (7, 'SitAmet.pdf', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (13, 'EgetVulputateUt.mp3', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (19, 'Tortor.avi', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (12, 'NibhFusceLacus.tiff', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (3, 'TortorDuisMattis.mpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (19, 'JustoNecCondimentum.txt', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (4, 'NonInterdumIn.mp3', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (3, 'FaucibusOrci.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (2, 'FelisSed.avi', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (14, 'Nulla.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (20, 'Bibendum.tiff', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (10, 'Odio.doc', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (15, 'Mi.avi', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (5, 'PretiumNisl.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (15, 'Duis.tiff', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (18, 'NamTristique.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (13, 'Aenean.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (1, 'ElementumLigulaVehicula.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (20, 'EgetRutrumAt.png', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (19, 'AcNibh.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (6, 'PedeJusto.tiff', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (4, 'InQuis.doc', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (17, 'NullamSitAmet.xls', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (9, 'NullaSedVel.mp3', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (15, 'ImperdietSapienUrna.ppt', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (11, 'Nullam.mpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (4, 'PotentiIn.tiff', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (10, 'VolutpatQuamPede.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (20, 'Habitasse.pdf', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (10, 'Tortor.jpeg', DEFAULT);
INSERT INTO `adsats_database`.`documents_notices` (`notice_id`, `document_name`, `created_at`) VALUES (5, 'ScelerisqueQuamTurpis.ppt', DEFAULT);

COMMIT;


-- -----------------------------------------------------
-- Data for table `adsats_database`.`notices_staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `adsats_database`;
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (16, 4, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (4, 4, '2023-12-25 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (7, 4, '2023-03-17 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (12, 6, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (5, 4, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (15, 2, '2023-12-24 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (16, 2, '2023-12-16 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (19, 5, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (6, 3, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (19, 1, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (17, 3, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (18, 2, '2023-03-14 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (20, 1, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (13, 5, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (6, 1, '2023-06-12 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (10, 6, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (15, 4, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (14, 4, '2023-07-10 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (10, 4, '2023-12-31 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (10, 3, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (1, 4, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (8, 3, '2023-12-07 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (4, 2, '2023-05-19 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (2, 2, '2023-12-02 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (7, 5, '2023-01-08 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (20, 3, '2023-11-07 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (1, 3, '2023-12-10 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (4, 6, '2023-12-06 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (1, 5, '2023-11-23 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (11, 6, '2023-08-03 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (9, 2, '2023-12-03 00:00:00', DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (6, 5, NULL, DEFAULT, DEFAULT);
INSERT INTO `adsats_database`.`notices_staff` (`notice_id`, `staff_id`, `read_at`, `created_at`, `updated_at`) VALUES (5, 1, NULL, DEFAULT, DEFAULT);

COMMIT;

