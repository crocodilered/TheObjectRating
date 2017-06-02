
--
-- Table structure for table `competition`
--

DROP TABLE IF EXISTS `competition`;
CREATE TABLE `competition` (
  `competition_id` int(11) NOT NULL AUTO_INCREMENT,
  `dt` date NOT NULL,
  `title` varchar(50) NOT NULL,
  PRIMARY KEY (`competition_id`),
  KEY `dt` (`dt`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8;


--
-- Table structure for table `points`
--

DROP TABLE IF EXISTS `points`;
CREATE TABLE `points` (
  `competition_id` int(11) NOT NULL,
  `shooter_id` int(11) NOT NULL,
  `value` float NOT NULL,
  UNIQUE KEY `match_id_shooter_id` (`competition_id`,`shooter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
  `competition_id` int(10) unsigned NOT NULL,
  `shooter_id` int(10) unsigned NOT NULL,
  `value_abs` float unsigned NOT NULL,
  `value_percents` float unsigned NOT NULL,
  PRIMARY KEY (`competition_id`,`shooter_id`),
  KEY `competition_id` (`competition_id`),
  KEY `shooter_id` (`shooter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


--
-- Table structure for table `shooter`
--

DROP TABLE IF EXISTS `shooter`;
CREATE TABLE `shooter` (
  `shooter_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`shooter_id`)
) ENGINE=InnoDB AUTO_INCREMENT=521 DEFAULT CHARSET=utf8;


