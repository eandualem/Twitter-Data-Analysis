CREATE TABLE IF NOT EXISTS `TweetInformation` 
(
    `id` INT NOT NULL AUTO_INCREMENT,
    `created_at` timestamp NOT NULL,
    `original_text` TEXT DEFAULT NULL,
    `polarity` DECIMAL DEFAULT NULL,
    `subjectivity` DOUBLE DEFAULT NULL,
    `favorite_count` INT DEFAULT NULL,
    `retweet_count` INT DEFAULT NULL,
    `original_author` TEXT DEFAULT NULL,
    `followers_count` BIGINT DEFAULT NULL,
    `friends_count` BIGINT DEFAULT NULL,
    `possibly_sensitive` tinyint(1) DEFAULT NULL,
    `hashtags` TEXT DEFAULT NULL,
    `place` TEXT DEFAULT NULL,
    `hashtags_in_tweets` TEXT DEFAULT NULL,
    `screen_name` TEXT DEFAULT NULL,
    `device` TEXT DEFAULT NULL,
    PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;


