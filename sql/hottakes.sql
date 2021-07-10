-- MariaDB dump 10.19  Distrib 10.5.10-MariaDB, for Win64 (AMD64)
--
-- Host: 127.0.0.1    Database: hot_takes
-- ------------------------------------------------------
-- Server version	10.5.10-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment_hot_cold`
--

DROP TABLE IF EXISTS `comment_hot_cold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_hot_cold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `comment_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_hot` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_hot_cold_comment_id_user_id_UN` (`comment_id`,`user_id`),
  KEY `comment_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `comment_hot_cold_comments_id_FK` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_hot_cold`
--

LOCK TABLES `comment_hot_cold` WRITE;
/*!40000 ALTER TABLE `comment_hot_cold` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment_hot_cold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `take_id` int(10) unsigned NOT NULL,
  `content` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `image_path` varchar(200) DEFAULT NULL,
  `was_edited` tinyint(1) DEFAULT NULL,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_takes_id_FK` (`take_id`),
  KEY `comments_users_id_FK` (`user_id`),
  CONSTRAINT `comments_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comments_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (53,48,49,'new comment','2021-07-09 21:09:22',NULL,NULL,NULL);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follows` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `follower_id` int(10) unsigned NOT NULL,
  `followed_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `follows_followed_id_follower_id_UN` (`followed_id`,`follower_id`),
  KEY `follows_users_id_FK` (`follower_id`),
  CONSTRAINT `follows_users_id_FK` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follows_users_id_FK_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hashtags`
--

DROP TABLE IF EXISTS `hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hashtags` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `take_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `hashtag` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `hashtags_take_id_hashtag_UN` (`take_id`,`hashtag`),
  KEY `hashtags_users_id_FK` (`user_id`),
  CONSTRAINT `hashtags_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `hashtags_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtags`
--

LOCK TABLES `hashtags` WRITE;
/*!40000 ALTER TABLE `hashtags` DISABLE KEYS */;
INSERT INTO `hashtags` VALUES (1,44,46,'tweet','2021-07-09 17:21:23'),(2,44,46,'hashtags','2021-07-09 17:21:23'),(3,44,46,'yayyy','2021-07-09 17:21:23'),(4,45,46,'tweet','2021-07-09 17:23:03'),(5,45,46,'hashtags','2021-07-09 17:23:03'),(6,45,46,'yayyy','2021-07-09 17:23:03'),(8,46,46,'tweet','2021-07-09 17:57:36'),(9,46,46,'hashtags','2021-07-09 17:57:36'),(10,46,46,'yayyy','2021-07-09 17:57:36'),(12,47,46,'tweet','2021-07-09 17:59:04'),(14,48,46,'tweet','2021-07-09 18:04:43'),(15,48,46,'hashtags','2021-07-09 18:04:43'),(16,48,46,'yayyy','2021-07-09 18:04:43'),(17,48,46,'new','2021-07-09 20:11:45'),(18,48,46,'some','2021-07-09 20:11:45'),(19,48,46,'yep','2021-07-09 20:11:45'),(28,49,48,'tweet','2021-07-09 20:29:47'),(29,49,48,'hashtags','2021-07-09 20:29:47'),(30,49,48,'yayyy','2021-07-09 20:29:47');
/*!40000 ALTER TABLE `hashtags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `to_user_id` int(10) unsigned NOT NULL,
  `from_user_id` int(10) unsigned NOT NULL,
  `content` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `messages_users_id_FK_2` (`to_user_id`),
  CONSTRAINT `messages_users_id_FK` FOREIGN KEY (`to_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `messages_users_id_FK_2` FOREIGN KEY (`to_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (20,46,48,'Hey how are you?!?!?','2021-07-09 20:28:53'),(21,46,48,'Hey how are you?!?!?','2021-07-09 20:28:55'),(23,46,48,'Hey how are you?!?!?','2021-07-09 20:28:59');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `is_read` tinyint(1) NOT NULL DEFAULT 0,
  `type` enum('message','comment','hot_cold_comment','hot_cold_retake','hot_cold_retake_comment','follow') NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `notifications_users_id_FK` (`user_id`),
  CONSTRAINT `notifications_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retake_comment_hot_cold`
--

DROP TABLE IF EXISTS `retake_comment_hot_cold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `retake_comment_hot_cold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `retake_comment_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_hot` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `retake_comment_hot_cold_retake_comment_id_user_id_UN` (`retake_comment_id`,`user_id`),
  KEY `retake_comment_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `retake_comment_hot_cold_retake_comments_id_FK` FOREIGN KEY (`retake_comment_id`) REFERENCES `retake_comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `retake_comment_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retake_comment_hot_cold`
--

LOCK TABLES `retake_comment_hot_cold` WRITE;
/*!40000 ALTER TABLE `retake_comment_hot_cold` DISABLE KEYS */;
/*!40000 ALTER TABLE `retake_comment_hot_cold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retake_comments`
--

DROP TABLE IF EXISTS `retake_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `retake_comments` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `retake_id` int(10) unsigned NOT NULL,
  `content` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `image_path` varchar(200) DEFAULT NULL,
  `was_edited` tinyint(1) DEFAULT NULL,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `retake_comments_retakes_id_FK` (`retake_id`),
  KEY `retake_comments_users_id_FK` (`user_id`),
  CONSTRAINT `retake_comments_retakes_id_FK` FOREIGN KEY (`retake_id`) REFERENCES `retakes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `retake_comments_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retake_comments`
--

LOCK TABLES `retake_comments` WRITE;
/*!40000 ALTER TABLE `retake_comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `retake_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retake_hot_cold`
--

DROP TABLE IF EXISTS `retake_hot_cold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `retake_hot_cold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `retake_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_hot` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `retake_hot_cold_retake_id_user_id_UN` (`retake_id`,`user_id`),
  KEY `retake_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `retake_hot_cold_retakes_id_FK` FOREIGN KEY (`retake_id`) REFERENCES `retakes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `retake_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retake_hot_cold`
--

LOCK TABLES `retake_hot_cold` WRITE;
/*!40000 ALTER TABLE `retake_hot_cold` DISABLE KEYS */;
/*!40000 ALTER TABLE `retake_hot_cold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `retakes`
--

DROP TABLE IF EXISTS `retakes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `retakes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `retake_user_id` int(10) unsigned NOT NULL,
  `take_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `retakes_takes_id_FK` (`take_id`),
  KEY `retakes_users_id_FK` (`retake_user_id`),
  CONSTRAINT `retakes_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `retakes_users_id_FK` FOREIGN KEY (`retake_user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retakes`
--

LOCK TABLES `retakes` WRITE;
/*!40000 ALTER TABLE `retakes` DISABLE KEYS */;
/*!40000 ALTER TABLE `retakes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `session`
--

DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token` varchar(65) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `session_start` datetime NOT NULL DEFAULT current_timestamp(),
  `session_end` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_token_UN` (`token`),
  KEY `session_users_id_FK` (`user_id`),
  CONSTRAINT `session_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
INSERT INTO `session` VALUES (95,'HogLlTO0q5LlB6xPQ7KyrXHsqtBCD0LbuIntccYF6WNt94_62e3xZV98O7Yy',46,'2021-07-09 17:20:54',NULL),(97,'hU-DE92Cr-70lehZOip8BXJPkgJ14xEQodPZ0j4ZL6LGAP7Z2y1VcmXsc-N4',46,'2021-07-09 20:26:19',NULL),(98,'-RZoynpgTelZThrTGJ6pCncBZcUTvUa557EkyuOq_2eK7UGrzMfOKvx-oBGL',48,'2021-07-09 20:26:24',NULL),(99,'UOk_FRwfGva-yyxxrtN3c-w_igOFER_pImN0yxLZTcHQmDBNC9jjqHnDFwPp',46,'2021-07-09 20:26:45',NULL),(100,'GedpbVZIXU5BHMymW4po_EjWs1BUmRn0PHcqnX6t6NtJZgH1jvXcaTVP-XR9',46,'2021-07-09 20:26:49',NULL);
/*!40000 ALTER TABLE `session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `take_hot_cold`
--

DROP TABLE IF EXISTS `take_hot_cold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `take_hot_cold` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `take_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `is_hot` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `take_hot_cold_take_id_user_id_UN` (`take_id`,`user_id`),
  KEY `take_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `take_hot_cold_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `take_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `take_hot_cold`
--

LOCK TABLES `take_hot_cold` WRITE;
/*!40000 ALTER TABLE `take_hot_cold` DISABLE KEYS */;
/*!40000 ALTER TABLE `take_hot_cold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `takes`
--

DROP TABLE IF EXISTS `takes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `takes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `content` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `image_path` varchar(200) DEFAULT NULL,
  `was_edited` tinyint(1) DEFAULT 0,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `takes_users_id_FK` (`user_id`),
  CONSTRAINT `takes_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takes`
--

LOCK TABLES `takes` WRITE;
/*!40000 ALTER TABLE `takes` DISABLE KEYS */;
INSERT INTO `takes` VALUES (44,46,'this is a #tweet with some #hashtags.... #yayyy','2021-07-09 17:21:23',NULL,0,NULL),(45,46,'this is a #tweet with some #hashtags.... #yayyy','2021-07-09 17:23:03',NULL,0,NULL),(46,46,'this is a #tweet with some #hashtags.... #yayyy #tweet','2021-07-09 17:57:36',NULL,0,NULL),(47,46,'this is a #tweet #tweet with some #hashtags.... #yayyy ','2021-07-09 17:59:04',NULL,0,NULL),(48,46,'a #new tweet with #some new hashtags, #yep..','2021-07-09 18:04:43',NULL,1,'2021-07-09 20:22:24'),(49,48,'this is a #tweet #tweet with some #hashtags.... #yayyy ','2021-07-09 20:29:47',NULL,0,NULL);
/*!40000 ALTER TABLE `takes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `takes_hashtags`
--

DROP TABLE IF EXISTS `takes_hashtags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `takes_hashtags` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `hashtag_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `takes_hashtags_hashtags_id_FK` (`hashtag_id`),
  CONSTRAINT `takes_hashtags_hashtags_id_FK` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takes_hashtags`
--

LOCK TABLES `takes_hashtags` WRITE;
/*!40000 ALTER TABLE `takes_hashtags` DISABLE KEYS */;
/*!40000 ALTER TABLE `takes_hashtags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `display_name` varchar(50) DEFAULT NULL,
  `birthdate` date DEFAULT NULL,
  `first_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `profile_pic_path` varchar(255) DEFAULT 'https://cdn.discordapp.com/attachments/841266201657344010/841266288486907914/ABSRlIpzcqh_JEyZP1CW1_RaZDO34zgsV3wfGtpwfn_D3IB6XFnQjvFl5nkymDIEJ58dpJoA1-t8agaWloWXJhVz9WWaXYVIbkkj.png',
  `profile_banner_path` varchar(255) DEFAULT 'https://cdn.discordapp.com/attachments/841266201657344010/841267134037753856/xYLCLELDik-QpSS1IlJGDh6GUVerl--HL5SGNhgwm_we9oTua_QOtpRh4jIuZsvIPGrRqa_kg0WYLV1MQn4XUCP80_32o4oUQET0.png',
  `headline` varchar(200) NOT NULL,
  `website_link` varchar(160) DEFAULT NULL,
  `location` varchar(70) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `salt` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_UN` (`email`),
  UNIQUE KEY `users_username_UN` (`username`),
  UNIQUE KEY `users_salt_UN` (`salt`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COMMENT='Users Table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (46,'GiveMeArrays','none@none.com','e7613925b5cd71032a2c06c43888dc72001042da05d968f1c8098e2e755690885d8aea0b32abea989e6451d1168f2f8042fa7df7990e661856590e0adb1eb3fb',NULL,'1999-08-12',NULL,NULL,'https://cdn.discordapp.com/attachments/841266201657344010/841266288486907914/ABSRlIpzcqh_JEyZP1CW1_RaZDO34zgsV3wfGtpwfn_D3IB6XFnQjvFl5nkymDIEJ58dpJoA1-t8agaWloWXJhVz9WWaXYVIbkkj.png','https://cdn.discordapp.com/attachments/841266201657344010/841267134037753856/xYLCLELDik-QpSS1IlJGDh6GUVerl--HL5SGNhgwm_we9oTua_QOtpRh4jIuZsvIPGrRqa_kg0WYLV1MQn4XUCP80_32o4oUQET0.png','this is a bio',NULL,NULL,NULL,0,1,'2021-07-09 17:20:54','XoPYiOttZ2'),(48,'newUser','none1@none.com','6d0cd2fc916907034ad4655e7d59afbbd82253cf47c31a938a4771e1583ca1781639d2838990f537e4afea89954ce746c580b52d4aae473883ff318199428027',NULL,'1999-08-12',NULL,NULL,'https://cdn.discordapp.com/attachments/841266201657344010/841266288486907914/ABSRlIpzcqh_JEyZP1CW1_RaZDO34zgsV3wfGtpwfn_D3IB6XFnQjvFl5nkymDIEJ58dpJoA1-t8agaWloWXJhVz9WWaXYVIbkkj.png','https://cdn.discordapp.com/attachments/841266201657344010/841267134037753856/xYLCLELDik-QpSS1IlJGDh6GUVerl--HL5SGNhgwm_we9oTua_QOtpRh4jIuZsvIPGrRqa_kg0WYLV1MQn4XUCP80_32o4oUQET0.png','this is a bio',NULL,NULL,NULL,0,1,'2021-07-09 20:26:08','sNv7Qx7r7t');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 21:27:34
