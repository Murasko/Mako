CREATE TABLE IF NOT EXISTS `guild_config` (
    `guild_id` INT NOT NULL,
    `notification_channel` INT NOT NULL,
    `administrators` INT NOT NULL,
    `watchlist` VARCHAR
);

CREATE TABLE IF NOT EXISTS `twitch_notifications` (
    `username` VARCHAR NOT NULL,
    `profile_picture_url` VARCHAR NOT NULL
)