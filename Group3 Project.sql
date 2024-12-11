/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.5.2-MariaDB, for osx10.19 (arm64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;
DROP DATABASE IF EXISTS project;
CREATE DATABASE project;
USE project;
--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `airport` (
  `id` int(11) NOT NULL,
  `ident` varchar(55) DEFAULT NULL,
  `name` text DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  `iso_region` text DEFAULT NULL,
  `municipality` text DEFAULT NULL,
  `type` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `airport_pk` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES
(3384,'KATL','Hartsfield Jackson Atlanta International',33.6367,-84.428101,'US-GA','Atlanta','Industrial'),
(3386,'KAUS','Austin Bergstrom International Airport',30.197535,-97.662015,'US-TX','Austin','Technology'),
(3420,'KBNA','Nashville International Airport',36.1245002746582,-86.6781997680664,'US-TN','Nashville','Agricultural'),
(3422,'KBOS','Logan International Airport',42.3643,-71.005203,'US-MA','Boston','Technology'),
(3431,'KBUF','Buffalo Niagara International Airport',42.94049835,-78.73220062,'US-NY','Buffalo','Industrial'),
(3486,'KDEN','Denver International Airport',39.861698150635,-104.672996521,'US-CO','Denver','Industrial'),
(3488,'KDFW','Dallas Fort Worth International Airport',32.896801,-97.038002,'US-TX','Dallas-Fort Worth','Industrial'),
(3497,'KDTW','Detroit Metropolitan Wayne County Airpor',42.212398529052734,-83.35340118408203,'US-MI','Detroit','Industrial'),
(3622,'KJFK','John F Kennedy International Airport',40.639801,-73.7789,'US-NY','New York','Technology'),
(3631,'KLAS','McCarran International Airport',36.08010101,-115.1520004,'US-NV','Las Vegas','Technology'),
(3632,'KLAX','Los Angeles International Airport',33.942501,-118.407997,'US-CA','Los Angeles','Technology'),
(3685,'KMIA','Miami International Airport',25.79319953918457,-80.29060363769531,'US-FL','Miami','Fishing'),
(3754,'KORD','Chicago O\'Hare International Airport',41.9786,-87.9048,'US-IL','Chicago','Industrial'),
(3875,'KSEA','Seattle Tacoma International Airport',47.449001,-122.308998,'US-WA','Seattle','Fishing'),
(3878,'KSFO','San Francisco International Airport',37.61899948120117,-122.375,'US-CA','San Francisco','Technology');
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `player_name` varchar(255) NOT NULL,
  `player_password` varchar(255) NOT NULL,
  `current_funds` int(11) DEFAULT 10000,
  `current_airport` varchar(55) NOT NULL,
  `time_left` float(4, 1) DEFAULT 360.0,
  PRIMARY KEY (`player_id`),
  KEY `game_airport_ident_fk` (`current_airport`),
  CONSTRAINT `game_airport_ident_fk` FOREIGN KEY (`current_airport`) REFERENCES `airport` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods`
--

DROP TABLE IF EXISTS `goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `goods` (
  `id` int(11) NOT NULL,
  `name` text DEFAULT NULL,
  `type` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods`
--

LOCK TABLES `goods` WRITE;
/*!40000 ALTER TABLE `goods` DISABLE KEYS */;
INSERT INTO `goods` VALUES
(1,'Tractors','Agricultural'),
(2,'Grain Storage Bins','Agricultural'),
(3,'Gaming Consoles','Technology'),
(4,'Drones','Technology'),
(5,'Hiking Gear','General'),
(6,'Farm Equipment','Agricultural'),
(7,'Fishing Gear','Fishing'),
(8,'Sunscreen','General'),
(9,'Industrial Lubricants','Industrial'),
(10,'Tools','Industrial'),
(11,'Organic Vegetables','Agricultural'),
(12,'Combine harvester','Agricultural'),
(13,'Beef','Agricultural'),
(14,'Organic Fruit','Agricultural'),
(15,'Heavy Equipment','Industrial'),
(16,'Steel','Industrial'),
(17,'Boat Equipment','Fishing'),
(18,'Fish','Fishing'),
(19,'Lure Fishing','Fishing'),
(20,'Beach Towels','General'),
(21,'Beach Balls','General'),
(22,'Seafood','Fishing'),
(23,'Lubricants','Industrial'),
(24,'Excavator','Industrial'),
(25,'Headphone','Technology'),
(26,'Virtual Reality Headsets','Technology'),
(27,'PS5','Technology'),
(28,'IPAD','Technology'),
(29,'3D Printers','Technology'),
(30,'Smartwatches','Technology');
/*!40000 ALTER TABLE `goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goods_in_different_airport`
--

DROP TABLE IF EXISTS `goods_in_different_airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `goods_in_different_airport` (
  `airport_ident` varchar(55) NOT NULL,
  `goods_id` int(11) NOT NULL,
  `buy_price` int(11) DEFAULT NULL,
  `sell_price` int(11) DEFAULT NULL,
  `stock` int(11) DEFAULT NULL,
  PRIMARY KEY (`airport_ident`,`goods_id`),
  KEY `Goods_in_different_airport_goods_id_fk` (`goods_id`),
  CONSTRAINT `Goods_in_different_airport_airport_ident_fk` FOREIGN KEY (`airport_ident`) REFERENCES `airport` (`ident`),
  CONSTRAINT `Goods_in_different_airport_goods_id_fk` FOREIGN KEY (`goods_id`) REFERENCES `goods` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goods_in_different_airport`
--

LOCK TABLES `goods_in_different_airport` WRITE;
/*!40000 ALTER TABLE `goods_in_different_airport` DISABLE KEYS */;
INSERT INTO `goods_in_different_airport` VALUES
('KATL',1,143,125,5),
('KATL',2,148,132,6),
('KATL',3,140,117,6),
('KATL',4,158,142,5),
('KATL',5,111,97,12),
('KATL',6,129,105,6),
('KATL',7,140,114,7),
('KATL',8,112,95,12),
('KATL',9,87,77,15),
('KATL',10,82,66,17),
('KATL',11,139,122,9),
('KATL',12,149,128,9),
('KATL',13,144,122,5),
('KATL',14,157,138,5),
('KATL',15,87,74,17),
('KATL',16,81,65,18),
('KATL',17,134,116,8),
('KATL',18,152,127,9),
('KATL',19,124,110,9),
('KATL',20,108,92,13),
('KATL',21,110,94,12),
('KATL',22,158,138,9),
('KATL',23,82,68,16),
('KATL',24,95,80,17),
('KATL',25,135,110,9),
('KATL',26,123,103,9),
('KATL',27,142,122,9),
('KATL',28,136,118,8),
('KATL',29,126,111,7),
('KATL',30,134,118,6),
('KAUS',1,144,123,9),
('KAUS',2,157,131,5),
('KAUS',3,94,76,17),
('KAUS',4,88,74,18),
('KAUS',5,111,97,12),
('KAUS',6,121,101,5),
('KAUS',7,142,128,7),
('KAUS',8,112,95,12),
('KAUS',9,154,128,8),
('KAUS',10,133,119,5),
('KAUS',11,154,136,8),
('KAUS',12,154,130,9),
('KAUS',13,138,117,5),
('KAUS',14,135,111,9),
('KAUS',15,147,126,6),
('KAUS',16,152,127,8),
('KAUS',17,140,125,6),
('KAUS',18,151,132,6),
('KAUS',19,130,114,7),
('KAUS',20,108,92,13),
('KAUS',21,110,94,12),
('KAUS',22,159,129,9),
('KAUS',23,143,122,8),
('KAUS',24,135,109,6),
('KAUS',25,82,66,18),
('KAUS',26,92,80,15),
('KAUS',27,94,80,18),
('KAUS',28,89,75,15),
('KAUS',29,91,78,18),
('KAUS',30,80,67,16),
('KBNA',1,88,75,16),
('KBNA',2,89,76,15),
('KBNA',3,135,109,9),
('KBNA',4,159,141,6),
('KBNA',5,111,97,12),
('KBNA',6,85,69,15),
('KBNA',7,126,110,5),
('KBNA',8,112,95,12),
('KBNA',9,124,107,6),
('KBNA',10,141,125,6),
('KBNA',11,99,85,17),
('KBNA',12,93,79,18),
('KBNA',13,81,68,18),
('KBNA',14,99,84,16),
('KBNA',15,120,102,6),
('KBNA',16,122,109,5),
('KBNA',17,132,108,7),
('KBNA',18,135,112,9),
('KBNA',19,148,128,5),
('KBNA',20,108,92,13),
('KBNA',21,110,94,12),
('KBNA',22,120,97,5),
('KBNA',23,126,108,6),
('KBNA',24,128,110,5),
('KBNA',25,135,113,5),
('KBNA',26,156,138,5),
('KBNA',27,135,112,5),
('KBNA',28,156,125,6),
('KBNA',29,128,103,5),
('KBNA',30,122,101,5),
('KBOS',1,126,102,6),
('KBOS',2,121,104,9),
('KBOS',3,84,73,16),
('KBOS',4,96,85,15),
('KBOS',5,111,97,12),
('KBOS',6,150,130,7),
('KBOS',7,151,128,8),
('KBOS',8,112,95,12),
('KBOS',9,137,116,5),
('KBOS',10,123,100,7),
('KBOS',11,140,118,7),
('KBOS',12,123,105,9),
('KBOS',13,144,122,5),
('KBOS',14,141,124,9),
('KBOS',15,157,134,7),
('KBOS',16,151,124,6),
('KBOS',17,132,114,5),
('KBOS',18,133,113,9),
('KBOS',19,159,137,9),
('KBOS',20,108,92,13),
('KBOS',21,110,94,12),
('KBOS',22,139,113,5),
('KBOS',23,140,119,6),
('KBOS',24,134,108,5),
('KBOS',25,85,75,15),
('KBOS',26,92,80,18),
('KBOS',27,95,77,15),
('KBOS',28,99,83,17),
('KBOS',29,80,71,17),
('KBOS',30,99,89,18),
('KBUF',1,123,101,7),
('KBUF',2,148,119,7),
('KBUF',3,155,136,7),
('KBUF',4,155,136,5),
('KBUF',5,111,97,12),
('KBUF',6,121,99,8),
('KBUF',7,141,119,6),
('KBUF',8,112,95,12),
('KBUF',9,98,83,16),
('KBUF',10,96,82,18),
('KBUF',11,149,123,6),
('KBUF',12,138,120,6),
('KBUF',13,125,108,5),
('KBUF',14,138,114,9),
('KBUF',15,88,73,18),
('KBUF',16,88,76,18),
('KBUF',17,155,130,9),
('KBUF',18,155,125,7),
('KBUF',19,137,112,7),
('KBUF',20,108,92,13),
('KBUF',21,110,94,12),
('KBUF',22,123,104,5),
('KBUF',23,81,68,16),
('KBUF',24,97,85,18),
('KBUF',25,151,129,7),
('KBUF',26,128,107,8),
('KBUF',27,147,121,9),
('KBUF',28,145,117,5),
('KBUF',29,134,114,8),
('KBUF',30,154,132,5),
('KDEN',1,130,107,8),
('KDEN',2,154,131,7),
('KDEN',3,126,112,5),
('KDEN',4,122,109,9),
('KDEN',5,111,97,12),
('KDEN',6,141,121,7),
('KDEN',7,124,105,7),
('KDEN',8,112,95,12),
('KDEN',9,88,74,17),
('KDEN',10,93,83,18),
('KDEN',11,139,117,6),
('KDEN',12,146,122,5),
('KDEN',13,127,108,7),
('KDEN',14,153,128,8),
('KDEN',15,91,77,16),
('KDEN',16,92,76,15),
('KDEN',17,152,133,6),
('KDEN',18,138,123,9),
('KDEN',19,136,116,7),
('KDEN',20,108,92,13),
('KDEN',21,110,94,12),
('KDEN',22,123,99,5),
('KDEN',23,95,78,17),
('KDEN',24,84,73,18),
('KDEN',25,132,118,9),
('KDEN',26,143,122,9),
('KDEN',27,127,112,6),
('KDEN',28,132,111,6),
('KDEN',29,140,123,6),
('KDEN',30,141,122,7),
('KDFW',1,128,112,8),
('KDFW',2,147,118,5),
('KDFW',3,122,109,9),
('KDFW',4,159,133,7),
('KDFW',5,111,97,12),
('KDFW',6,151,134,7),
('KDFW',7,130,110,8),
('KDFW',8,112,95,12),
('KDFW',9,87,75,17),
('KDFW',10,88,75,16),
('KDFW',11,139,116,6),
('KDFW',12,128,109,9),
('KDFW',13,127,106,6),
('KDFW',14,153,126,5),
('KDFW',15,96,78,17),
('KDFW',16,89,79,15),
('KDFW',17,128,105,5),
('KDFW',18,145,121,5),
('KDFW',19,152,137,8),
('KDFW',20,108,92,13),
('KDFW',21,110,94,12),
('KDFW',22,142,117,6),
('KDFW',23,90,78,18),
('KDFW',24,86,76,15),
('KDFW',25,153,126,6),
('KDFW',26,154,131,7),
('KDFW',27,122,109,6),
('KDFW',28,160,130,9),
('KDFW',29,132,118,6),
('KDFW',30,127,104,6),
('KDTW',1,142,115,9),
('KDTW',2,134,120,7),
('KDTW',3,148,124,7),
('KDTW',4,124,111,6),
('KDTW',5,111,97,12),
('KDTW',6,125,107,5),
('KDTW',7,158,141,7),
('KDTW',8,112,95,12),
('KDTW',9,99,83,18),
('KDTW',10,94,84,15),
('KDTW',11,150,125,5),
('KDTW',12,154,136,7),
('KDTW',13,142,118,5),
('KDTW',14,126,101,6),
('KDTW',15,89,73,17),
('KDTW',16,100,89,17),
('KDTW',17,156,125,6),
('KDTW',18,156,130,5),
('KDTW',19,139,121,5),
('KDTW',20,108,92,13),
('KDTW',21,110,94,12),
('KDTW',22,123,101,6),
('KDTW',23,100,81,16),
('KDTW',24,97,85,17),
('KDTW',25,121,106,6),
('KDTW',26,158,133,6),
('KDTW',27,130,114,7),
('KDTW',28,130,114,8),
('KDTW',29,122,101,5),
('KDTW',30,153,126,6),
('KJFK',1,149,124,9),
('KJFK',2,146,117,8),
('KJFK',3,94,76,18),
('KJFK',4,100,82,15),
('KJFK',5,111,97,12),
('KJFK',6,131,116,9),
('KJFK',7,154,131,8),
('KJFK',8,112,95,12),
('KJFK',9,154,137,7),
('KJFK',10,127,103,5),
('KJFK',11,154,136,6),
('KJFK',12,136,121,6),
('KJFK',13,156,125,6),
('KJFK',14,128,106,5),
('KJFK',15,138,117,7),
('KJFK',16,150,130,7),
('KJFK',17,133,116,5),
('KJFK',18,147,127,5),
('KJFK',19,158,142,7),
('KJFK',20,108,92,13),
('KJFK',21,110,94,12),
('KJFK',22,140,123,7),
('KJFK',23,135,116,5),
('KJFK',24,125,110,7),
('KJFK',25,83,69,15),
('KJFK',26,86,76,18),
('KJFK',27,89,73,18),
('KJFK',28,99,88,17),
('KJFK',29,91,78,16),
('KJFK',30,81,67,16),
('KLAS',1,151,132,9),
('KLAS',2,130,114,6),
('KLAS',3,86,74,18),
('KLAS',4,83,73,15),
('KLAS',5,111,97,12),
('KLAS',6,159,138,9),
('KLAS',7,145,128,6),
('KLAS',8,112,95,12),
('KLAS',9,146,131,9),
('KLAS',10,138,118,8),
('KLAS',11,140,124,9),
('KLAS',12,127,109,9),
('KLAS',13,132,112,9),
('KLAS',14,143,125,9),
('KLAS',15,137,112,7),
('KLAS',16,130,113,8),
('KLAS',17,124,109,7),
('KLAS',18,144,116,8),
('KLAS',19,149,133,5),
('KLAS',20,108,92,13),
('KLAS',21,110,94,12),
('KLAS',22,142,114,7),
('KLAS',23,121,103,5),
('KLAS',24,149,122,7),
('KLAS',25,99,86,17),
('KLAS',26,91,79,15),
('KLAS',27,99,85,15),
('KLAS',28,95,82,15),
('KLAS',29,100,84,18),
('KLAS',30,86,77,17),
('KLAX',1,129,114,7),
('KLAX',2,152,123,5),
('KLAX',3,84,67,16),
('KLAX',4,83,73,16),
('KLAX',5,111,97,12),
('KLAX',6,156,137,8),
('KLAX',7,127,106,6),
('KLAX',8,112,95,12),
('KLAX',9,142,121,5),
('KLAX',10,148,121,8),
('KLAX',11,151,125,6),
('KLAX',12,136,121,5),
('KLAX',13,141,123,9),
('KLAX',14,132,117,5),
('KLAX',15,155,128,5),
('KLAX',16,159,138,8),
('KLAX',17,149,127,7),
('KLAX',18,134,115,9),
('KLAX',19,121,100,5),
('KLAX',20,108,92,13),
('KLAX',21,110,94,12),
('KLAX',22,130,112,7),
('KLAX',23,126,109,8),
('KLAX',24,156,134,5),
('KLAX',25,97,87,16),
('KLAX',26,92,75,18),
('KLAX',27,97,87,18),
('KLAX',28,95,77,15),
('KLAX',29,100,85,18),
('KLAX',30,83,71,18),
('KMIA',1,137,110,9),
('KMIA',2,126,107,6),
('KMIA',3,157,133,5),
('KMIA',4,126,111,9),
('KMIA',5,111,97,12),
('KMIA',6,144,129,5),
('KMIA',7,94,83,17),
('KMIA',8,112,95,12),
('KMIA',9,145,127,5),
('KMIA',10,126,112,9),
('KMIA',11,135,112,9),
('KMIA',12,132,118,5),
('KMIA',13,135,116,9),
('KMIA',14,145,118,9),
('KMIA',15,148,133,6),
('KMIA',16,127,108,9),
('KMIA',17,84,72,17),
('KMIA',18,82,67,18),
('KMIA',19,85,70,18),
('KMIA',20,108,92,13),
('KMIA',21,110,94,12),
('KMIA',22,96,82,17),
('KMIA',23,153,125,5),
('KMIA',24,131,109,8),
('KMIA',25,120,96,7),
('KMIA',26,133,109,5),
('KMIA',27,155,124,8),
('KMIA',28,124,105,6),
('KMIA',29,151,122,9),
('KMIA',30,131,108,7),
('KORD',1,121,106,7),
('KORD',2,137,112,5),
('KORD',3,157,134,5),
('KORD',4,150,125,6),
('KORD',5,111,97,12),
('KORD',6,138,116,5),
('KORD',7,136,116,9),
('KORD',8,112,95,12),
('KORD',9,83,75,18),
('KORD',10,95,76,15),
('KORD',11,157,129,5),
('KORD',12,156,140,5),
('KORD',13,132,110,9),
('KORD',14,129,110,8),
('KORD',15,88,76,15),
('KORD',16,88,77,15),
('KORD',17,158,141,6),
('KORD',18,135,111,5),
('KORD',19,128,106,5),
('KORD',20,108,92,13),
('KORD',21,110,94,12),
('KORD',22,131,112,8),
('KORD',23,83,72,16),
('KORD',24,83,73,16),
('KORD',25,149,130,9),
('KORD',26,144,121,8),
('KORD',27,152,132,9),
('KORD',28,128,107,5),
('KORD',29,148,131,7),
('KORD',30,123,99,8),
('KSEA',1,148,131,9),
('KSEA',2,154,125,5),
('KSEA',3,121,107,8),
('KSEA',4,160,128,6),
('KSEA',5,111,97,12),
('KSEA',6,156,128,6),
('KSEA',7,93,81,16),
('KSEA',8,112,95,12),
('KSEA',9,134,114,7),
('KSEA',10,135,120,7),
('KSEA',11,123,107,9),
('KSEA',12,139,112,6),
('KSEA',13,129,104,8),
('KSEA',14,141,113,8),
('KSEA',15,135,121,7),
('KSEA',16,133,115,6),
('KSEA',17,87,74,18),
('KSEA',18,87,75,16),
('KSEA',19,97,85,18),
('KSEA',20,108,92,13),
('KSEA',21,110,94,12),
('KSEA',22,81,66,18),
('KSEA',23,145,117,9),
('KSEA',24,121,109,6),
('KSEA',25,149,130,8),
('KSEA',26,149,130,7),
('KSEA',27,133,114,8),
('KSEA',28,154,130,9),
('KSEA',29,129,111,8),
('KSEA',30,157,134,8),
('KSFO',1,122,109,8),
('KSFO',2,133,108,5),
('KSFO',3,83,72,18),
('KSFO',4,82,68,18),
('KSFO',5,111,97,12),
('KSFO',6,123,108,6),
('KSFO',7,145,127,5),
('KSFO',8,112,95,12),
('KSFO',9,131,112,9),
('KSFO',10,151,136,5),
('KSFO',11,134,112,9),
('KSFO',12,155,135,8),
('KSFO',13,152,131,9),
('KSFO',14,158,142,8),
('KSFO',15,142,127,5),
('KSFO',16,144,126,5),
('KSFO',17,158,127,8),
('KSFO',18,127,102,7),
('KSFO',19,158,140,5),
('KSFO',20,108,92,13),
('KSFO',21,110,94,12),
('KSFO',22,134,115,5),
('KSFO',23,142,126,5),
('KSFO',24,138,118,6),
('KSFO',25,82,67,16),
('KSFO',26,84,68,17),
('KSFO',27,96,78,18),
('KSFO',28,85,69,16),
('KSFO',29,97,81,15),
('KSFO',30,95,79,17);
/*!40000 ALTER TABLE `goods_in_different_airport` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Table structure for table `player_inventory`
--

DROP TABLE IF EXISTS `player_inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `player_inventory` (
  `player_id` int(11) NOT NULL,
  `goods_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`player_id`,`goods_id`),
  KEY `player_inventory_player_id_index` (`player_id`),
  KEY `player_inventory_goods_id_fk` (`goods_id`),
  CONSTRAINT `player_inventory_goods_id_fk` FOREIGN KEY (`goods_id`) REFERENCES `goods` (`id`),
  CONSTRAINT `player_inventory_player_info_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `game` (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_inventory`
--

LOCK TABLES `player_inventory` WRITE;
/*!40000 ALTER TABLE `player_inventory` DISABLE KEYS */;
/*!40000 ALTER TABLE `player_inventory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-09-28 20:44:10
