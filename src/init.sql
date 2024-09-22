USE `db`;

-- Users Database
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`(
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN NOT NULL,
    `secret` TEXT NOT NULL,
    PRIMARY KEY (`id`)
);
INSERT INTO `users` (`username`, `password`, `is_admin`, `secret`) VALUES 
('alice', 'hello-world-im-alice', 0, 'I hate Bob.'), 
('bob', 'alices-are-red-violets-are-blue', 0, 'I love Alice.'),
('admin', 'cuhk24ctf{flag4_0w0_you_got_admin_password_of_the_website}', 1, 'cuhk24ctf{flag3_w0w_you_know_basic_xss_now}');

-- Posts Database
DROP TABLE IF EXISTS `posts`;

CREATE TABLE `posts`(
    `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
    `author_id` BIGINT(20) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `content` TEXT NOT NULL,
    `date` DATETIME NOT NULL,
    PRIMARY KEY (`id`)
);
