CREATE TABLE IF NOT EXISTS `guild_config` (
    `guild_id` INT NOT NULL,
    `notification_channel` INT NOT NULL,
    `administrators` INT NOT NULL,
    `watchlist` VARCHAR
);