-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: 34.134.120.57    Database: hot_takes
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.18-MariaDB-1:10.4.18+maria~stretch

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
  `is_cold` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_hot_cold_comment_id_user_id_UN` (`comment_id`,`user_id`),
  KEY `comment_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `comment_hot_cold_comments_id_FK` FOREIGN KEY (`comment_id`) REFERENCES `comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
  `content` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL,
  `image_path` varchar(200) DEFAULT NULL,
  `was_edited` tinyint(1) DEFAULT NULL,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_takes_id_FK` (`take_id`),
  KEY `comments_users_id_FK` (`user_id`),
  CONSTRAINT `comments_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comments_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
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
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follows_followed_id_follower_id_UN` (`followed_id`,`follower_id`),
  KEY `follows_users_id_FK` (`follower_id`),
  CONSTRAINT `follows_users_id_FK` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follows_users_id_FK_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hashtags`
--

LOCK TABLES `hashtags` WRITE;
/*!40000 ALTER TABLE `hashtags` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
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
  `is_cold` tinyint(1) DEFAULT NULL,
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
  `is_cold` tinyint(1) DEFAULT NULL,
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
  `token` varchar(40) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `session_start` datetime NOT NULL,
  `session_end` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_token_UN` (`token`),
  KEY `session_users_id_FK` (`user_id`),
  CONSTRAINT `session_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `session`
--

LOCK TABLES `session` WRITE;
/*!40000 ALTER TABLE `session` DISABLE KEYS */;
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
  `is_cold` tinyint(1) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `take_hot_cold_take_id_user_id_UN` (`take_id`,`user_id`),
  KEY `take_hot_cold_users_id_FK` (`user_id`),
  CONSTRAINT `take_hot_cold_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `take_hot_cold_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
  `content` varchar(250) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `image_path` varchar(200) DEFAULT NULL,
  `was_edited` tinyint(1) DEFAULT 0,
  `edit_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `takes_users_id_FK` (`user_id`),
  CONSTRAINT `takes_users_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `takes`
--

LOCK TABLES `takes` WRITE;
/*!40000 ALTER TABLE `takes` DISABLE KEYS */;
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
  `take_id` int(10) unsigned NOT NULL,
  `hashtag_id` int(10) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `takes_hashtags_take_id_hashtag_id_UN` (`take_id`,`hashtag_id`),
  KEY `takes_hashtags_hashtags_id_FK` (`hashtag_id`),
  CONSTRAINT `takes_hashtags_hashtags_id_FK` FOREIGN KEY (`hashtag_id`) REFERENCES `hashtags` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `takes_hashtags_takes_id_FK` FOREIGN KEY (`take_id`) REFERENCES `takes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
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
  `email` varchar(60) NOT NULL,
  `password` varchar(255) NOT NULL,
  `display_name` varchar(50) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `first_name` varchar(25) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `profile_pic_path` varchar(255) DEFAULT NULL,
  `profile_banner_path` varchar(255) DEFAULT NULL,
  `headline` varchar(200) DEFAULT NULL,
  `website_link` varchar(160) DEFAULT NULL,
  `location` varchar(70) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Users Table';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'hot_takes'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-06-18 17:40:00
