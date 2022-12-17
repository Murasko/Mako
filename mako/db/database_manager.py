import aiosqlite

database_path = "mako/db/database.db"


async def save_twitch_user_profile_picture(
    username: str, profile_picture_url: str
) -> None:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(
            "INSERT INTO twitch_notifications VALUES (?, ?)",
            (username, profile_picture_url),
        )
        await database.commit()


async def get_saved_profile_images(username: str) -> list:
    async with aiosqlite.connect(database_path) as database:
        async with database.execute(
            "SELECT * FROM twitch_notifications WHERE username=?", (username,)
        ) as cursor:
            return await cursor.fetchone()


async def get_notification_channel(guild_id: int) -> int:
    pass


async def set_notification_channel(guild_id: int, notification_channel: int) -> None:
    pass


async def get_watchlist(guild_id: int) -> list:
    pass


async def set_watchlist(guild_id: int, watchlist: list) -> None:
    pass
