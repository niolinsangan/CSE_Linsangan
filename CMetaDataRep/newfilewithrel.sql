-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema customermetadatarepository
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema customermetadatarepository
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `customermetadatarepository` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `customermetadatarepository` ;

-- -----------------------------------------------------
-- Table `customermetadatarepository`.`attribute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`attribute` (
  `attribute_id` INT NOT NULL,
  `attribute_name` VARCHAR(100) NULL DEFAULT NULL,
  `attribute_datatype` VARCHAR(100) NULL DEFAULT NULL,
  `attribute_description` TEXT NULL DEFAULT NULL,
  `typical_values` TEXT NULL DEFAULT NULL,
  `validation_criteria` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`attribute_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`business_term_owner`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`business_term_owner` (
  `term_owner_code` VARCHAR(100) NULL DEFAULT NULL,
  `term_owner_description` VARCHAR(100) NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`business_term_type`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`business_term_type` (
  `business_term_type_code` INT NOT NULL,
  `business_term_type_description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`business_term_type_code`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`entity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`entity` (
  `entity_id` INT NOT NULL,
  `entity_name` VARCHAR(100) NULL DEFAULT NULL,
  `entity_description` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`entity_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`generic_customer_data_model`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`generic_customer_data_model` (
  `id` INT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`glossary_of_business_terms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`glossary_of_business_terms` (
  `business_term_short_name` VARCHAR(100) NULL DEFAULT NULL,
  `date_term_defined` DATE NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `customermetadatarepository`.`source_systems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customermetadatarepository`.`source_systems` (
  `src_system_id` INT NOT NULL,
  `src_system_name` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`src_system_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
