#  Mako - Python Discord Bot
#  Copyright (c) 2023. Marco Murawski
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  Contact:
#  info@murasko.de


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


async def set_guild_id(guild_id: int) -> None:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(f"INSERT INTO guild_config VALUES {guild_id}")
        await database.commit()


async def get_notification_channel(guild_id: int) -> int:
    pass


async def set_notification_channel(guild_id: int, notification_channel: int) -> None:
    pass


async def get_watchlist(guild_id: int) -> list:
    pass


async def set_watchlist(guild_id: int, watchlist: list) -> None:
    pass
