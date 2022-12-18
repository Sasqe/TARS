CREATE DATABASE `tensorflow_models` /*!40100 DEFAULT CHARACTER SET utf8 */;
CREATE TABLE `model_storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `model` longblob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
