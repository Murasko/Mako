CREATE TABLE IF NOT EXISTS `guild_notification_channel` (
    `guild_id` INT NOT NULL,
    `notification_channel` INT NOT NULL,
    CONSTRAINT pk_guild_notification_channel PRIMARY KEY (guild_id)
);

CREATE TABLE IF NOT EXISTS `guild_admins` (
    `guild_id` INT NOT NULL,
    `user_id` VARCHAR NOT NULL,
    CONSTRAINT pk_guild_admins PRIMARY KEY (guild_id, user_id)
);

CREATE TABLE IF NOT EXISTS `twitch_watchlist` (
    `guild_id` INT NOT NULL,
    `username` VARCHAR NOT NULL,
    CONSTRAINT pk_watchlist PRIMARY KEY (guild_id, username)
);

CREATE TABLE IF NOT EXISTS `twitch_notifications` (
    `username` VARCHAR NOT NULL PRIMARY KEY,
    `profile_picture_url` VARCHAR NOT NULL,
    `status` VARCHAR NOT NULL
);