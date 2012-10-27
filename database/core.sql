-- MySQL dump 10.13  Distrib 5.1.61, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: db_uv
-- ------------------------------------------------------
-- Server version	5.1.61

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

CREATE DATABASE IF NOT EXISTS core;

USE core;

--
-- Table structure for table `tb_user_content`
--

DROP TABLE IF EXISTS `tb_user_content`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user_content` (
  `msisdn` varchar(15) DEFAULT NULL,
  `content_id` varchar(20) DEFAULT NULL,
  `content_media` varchar(10) DEFAULT NULL,
  `content_status` varchar(10) DEFAULT NULL,
  `content_class` varchar(10) DEFAULT NULL,
  `content` text,
  `create_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `first_read_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `last_read_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `read_count` smallint(6) DEFAULT NULL,
  `like_count` smallint(6) DEFAULT NULL,
  `content_ttl` smallint(6) DEFAULT NULL,
  `channel` varchar(20) DEFAULT NULL,
  `content_size` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_content_action`
--

DROP TABLE IF EXISTS `tb_content_action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_content_action` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content_id` int(10) NOT NULL,
  `source` int(10) NOT NULL,
  `destination` int(10) NOT NULL,
  `action_type` tinyint(4) NOT NULL COMMENT '1-Like, 2-Comment, 3-Reply, 4-Forward, 5-Share',
  `created_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `follower_feed_fk_2` (`source`,`destination`),
  KEY `message_id_index` (`content_id`),
  KEY `created_ts_index` (`created_ts`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_subscription`
--

DROP TABLE IF EXISTS `tb_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_subscription` (
  `msisdn` int(10) unsigned NOT NULL,
  `device_id` varchar(45) DEFAULT NULL,
  `service_id` int(11) unsigned DEFAULT NULL,
  `subs_status` tinyint(4) NOT NULL COMMENT '1-Pending, 2-Subscribed ,3-Unsubscribed, 4-Expired, 5-Cancelled',
  `start_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `expire_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `renewal_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cancelled_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `channel` tinyint(4) NOT NULL COMMENT '1-IVR, 2-SMS, 3-USSD, 4-WEB, 5-OBD',
  `created_ts` datetime NOT NULL,
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`msisdn`),
  UNIQUE KEY `tb_subscription_uk_1` (`msisdn`,`service_id`),
  KEY `tb_subscription_fk_2` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_followers`
--

DROP TABLE IF EXISTS `tb_followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_followers` (
  `blogger` varchar(15) DEFAULT NULL,
  `follower` varchar(15) DEFAULT NULL,
  `status` int(11) DEFAULT NULL COMMENT '1 active-follow 2 follow-cancel',
  `create_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `update_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `channel` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_user_profile`
--

DROP TABLE IF EXISTS `tb_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user_profile` (
  `msisdn` varchar(45) NOT NULL DEFAULT '0',
  `lang` varchar(40) DEFAULT NULL,
  `operator_id` varchar(45) NOT NULL,
  `status` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1-PreActive, 2-Active, 3-Disabled, 4-Deleted',
  `user_type` tinyint(4) NOT NULL DEFAULT '2' COMMENT '1-celeb, 2-topuser 3-normaluser',
  `created_ts` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `privacy` tinyint(4) NOT NULL DEFAULT '1' COMMENT '1-public, 2-private 3-propublic',
  `follower_count` int(11) DEFAULT '0',
  `following_count` int(11) DEFAULT '0',
  `lang_notify` varchar(40) DEFAULT NULL,
  `new_inbox_size` int(10) NOT NULL DEFAULT '10',
  `heard_inbox_size` int(10) NOT NULL DEFAULT '10',
  `save_inbox_size` int(10) NOT NULL DEFAULT '10',
  `def_inbox_ttl` int(10) DEFAULT NULL,
  `def_save_ttl` int(10) DEFAULT NULL,
  `notify_pref` tinyint(4) DEFAULT '1' COMMENT '1-SMS 2-OBD 3-EMAIL',
  `username` varchar(100) NOT NULL,
  `email` varchar(200) DEFAULT NULL,
  `displayname` varchar(40) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `location` char(2) NOT NULL DEFAULT 'SG' COMMENT 'ISO2 country codes',
  `channel` tinyint(4) NOT NULL COMMENT 'facebook-21, twitter-22, web-23, iphone-24, android-25',
  `device_id` varchar(45) DEFAULT NULL COMMENT 'device id',
  `user_desc` varchar(512) DEFAULT NULL,
  `profile_url` varchar(120) DEFAULT NULL COMMENT 'profile url',
  `intro_audio_url` varchar(120) DEFAULT NULL COMMENT 'introduction audio url',
  `image_url` varchar(120) DEFAULT NULL COMMENT 'profile avatar image',
  `current_location` varchar(160) DEFAULT NULL,
  `facebook_id` varchar(100) DEFAULT NULL COMMENT 'facebook account id',
  `facebook_username` varchar(160) DEFAULT NULL,
  `facebook_screenname` varchar(160) DEFAULT NULL,
  `twitter_username` varchar(160) DEFAULT NULL,
  `facebook_token` varchar(260) DEFAULT NULL,
  `twitter_id` int(11) DEFAULT '-1',
  `twitter_token` varchar(260) DEFAULT NULL,
  `twitter_token_secret` varchar(260) DEFAULT NULL,
  `twitter_screenname` varchar(160) DEFAULT NULL,
  `telco_follower_count` int(11) unsigned NOT NULL DEFAULT '0',
  `notify_email_addr` varchar(100) DEFAULT NULL,
  `notify_new_msg` tinyint(1) NOT NULL DEFAULT '1',
  `fwd_to` varchar(20) DEFAULT NULL,
  `fwd_email_addr` varchar(100) DEFAULT NULL,
  `fwd_phone_no` varchar(20) DEFAULT NULL,
  `block_list` text,
  PRIMARY KEY (`msisdn`),
  UNIQUE KEY `msi_loc` (`msisdn`,`location`),
  UNIQUE KEY `up_uk_3` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_services`
--

DROP TABLE IF EXISTS `tb_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_services` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `service_id` varchar(10) DEFAULT NULL,
  `service_name` varchar(10) DEFAULT NULL,
  `service_group` varchar(10) DEFAULT NULL,
  `desc` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_service_profile`
--

DROP TABLE IF EXISTS `tb_service_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_service_profile` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `service_id` varchar(10) NOT NULL DEFAULT '.*' COMMENT 'reg-ex',
  `profile_key` varchar(10) DEFAULT NULL,
  `profile_value` varchar(10) DEFAULT NULL,
  `desc` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_service_map`
--

DROP TABLE IF EXISTS `tb_service_map`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_service_map` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `in_pattern` varchar(10) DEFAULT NULL,
  `out_pattern` varchar(10) DEFAULT NULL,
  `telco_id` varchar(20) NOT NULL DEFAULT '.*',
  `channel` varchar(20) NOT NULL DEFAULT '.*',
  `service_id` varchar(10) DEFAULT NULL,
  `desc` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_service_charge`
--

DROP TABLE IF EXISTS `tb_service_charge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_service_charge` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `service_id` int(10) DEFAULT NULL,
  `plan_id` int(10) DEFAULT NULL,
  `channel` varchar(4) DEFAULT NULL COMMENT '1-IVR, 2-SMS, 3-OBD, 4-USSD, 5-WEB',
  `duration` int(10) DEFAULT 7,
  `price` int(10) DEFAULT NULL,
  `start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `end_date` timestamp NOT NULL DEFAULT '2020-01-01 00:00:00',
  `status` tinyint(4) DEFAULT '1' COMMENT '0-disable,1-enable',
  `action` tinyint(4) DEFAULT '1' COMMENT '1-Sub, 2-Renewal',
  `remarks` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_number_normalizer`
--

DROP TABLE IF EXISTS `tb_number_normalizer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_number_normalizer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `in_pattern` varchar(40) NOT NULL,
  `out_pattern` varchar(40) NOT NULL,
  `telco_id` varchar(20) NOT NULL DEFAULT '.*',
  `channel` varchar(20) NOT NULL DEFAULT '.*',
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tb_number_normalizer`
--

DROP TABLE IF EXISTS `tb_cdr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `tb_cdr` (
  `callid` varchar(40) default NULL,
  `source` varchar(40) default NULL,
  `src_telco_id` varchar(20) NOT NULL DEFAULT '.*',
  `dialed_number` varchar(40) default NULL,
  `destination` varchar(40) default NULL,
  `dst_telco_id` varchar(20) NOT NULL DEFAULT '.*',
  `service_id` varchar(40) default NULL,
  `start_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `end_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `call_duration` varchar(40) default NULL,
  `call_complete_type` int(4) NOT NULL COMMENT 'user hangup - 1, call release - 2, abnormal completion - 3 ',
  PRIMARY KEY (`callid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=FIXED;
/*!40101 SET @saved_cs_client     = @@character_set_client */;

DROP TABLE IF EXISTS `tb_cdr_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `tb_cdr_transaction` (
  `id` varchar(40) default NULL,
  `callid` varchar(40) default NULL,
  `txn_type` varchar(40) NOT NULL COMMENT 'share, reply, mt-charge, subscription, renewal',
  `source` varchar(40) default NULL,
  `destination` varchar(40) default NULL,
  `start_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `end_time` timestamp NOT NULL default '0000-00-00 00:00:00',
  `txn_status` varchar(40) default NULL COMMENT 'success fail noresponse',
  PRIMARY KEY (`id`, `callid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=FIXED;
/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-05-27 19:59:04
