DROP DATABASE IF EXISTS `dummydata`;
CREATE DATABASE `dummydata`;

USE `dummydata`;
DROP TABLE IF EXISTS `table1`;
CREATE TABLE `table1` ( id bigint unsigned not null auto_increment, data1 varchar(255) default null, data2 varchar(255) default null, constraint pk_table1 primary key (id) );
INSERT INTO `table1` (id, data1, data2) values (1, "qwe", "asd");