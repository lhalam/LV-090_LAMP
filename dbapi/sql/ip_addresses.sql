CREATE SCHEMA IF NOT EXISTS ip_addresses DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE ip_addresses ;

-- -----------------------------------------------------
-- Table ipv4_addresses
-- Stores address id, when address was added and address
-- as unsigned integer
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS ipv4_addresses (
  id INT(11) NOT NULL AUTO_INCREMENT,
  address INT(10) UNSIGNED NOT NULL,
  date_added DATE NULL DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX address_UNIQUE (address) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table ipv6_addresses
-- Stores address id, when address was added and address
-- in binary form
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS ipv6_addresses (
  id INT(11) NOT NULL AUTO_INCREMENT,
  address VARBINARY(16) NOT NULL,
  date_added DATE NULL DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX address_UNIQUE (address) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table blacklist
-- Contain a pair of id's for v4 and v6 addresses
-- that are in blacklist
-- When ipv4 added, v6 stays NULL, and vice versa
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS blacklist (
  v4_id_blacklist INT(11) NULL DEFAULT NULL,
  v6_id_blacklist INT(11) NULL DEFAULT NULL,
  CONSTRAINT
    FOREIGN KEY (v4_id_blacklist)
    REFERENCES ipv4_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT
    FOREIGN KEY (v6_id_blacklist)
    REFERENCES ipv6_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table sources
-- Contain information about sources: Name of Source,
-- url if exists, date when source was added and date of
-- last url modification, rank of source (0..10)
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS sources (
  id INT(11) NOT NULL AUTO_INCREMENT,
  source_name VARCHAR(45) NULL DEFAULT NULL,
  url TEXT NULL DEFAULT NULL,
  source_date_added DATE NULL DEFAULT NULL,
  url_date_modified DATE NULL DEFAULT NULL,
  rank TINYINT(4) NOT NULL,
  PRIMARY KEY (id) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table source_to_addresses
-- Reference table where each row represented as
-- source id and corresponding id of ip address
-- that was added by that source, since clolumns may not
-- be unique - many ip addresses can belong to single source
-- When ipv4 added, v6 stays NULL, and vice versa
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS source_to_addresses (
  source_id INT(11) NULL DEFAULT NULL,
  v4_id INT(11) NULL DEFAULT NULL,
  v6_id INT(11) NULL DEFAULT NULL,
  CONSTRAINT
    FOREIGN KEY (source_id)
    REFERENCES sources (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT
    FOREIGN KEY (v4_id)
    REFERENCES ipv4_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT
    FOREIGN KEY (v6_id)
    REFERENCES ipv6_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table whitelist
-- Contain a pair of id's for v4 and v6 addresses
-- that are in whitelist
-- When ipv4 added, v6 stays NULL, and vice versa
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS whitelist (
  v4_id_whitelist INT(11) NULL DEFAULT NULL,
  v6_id_whitelist INT(11) NULL DEFAULT NULL,
  CONSTRAINT
    FOREIGN KEY (v4_id_whitelist)
    REFERENCES ipv4_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT
    FOREIGN KEY (v6_id_whitelist)
    REFERENCES ipv6_addresses (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;
