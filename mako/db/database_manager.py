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
            f"INSERT INTO twitch_notifications VALUES (?, ?)",
            (username, profile_picture_url,)
        )
        await database.commit()


async def get_saved_profile_images(username: str) -> tuple:
    async with aiosqlite.connect(database_path) as database:
        async with database.execute(
                f"SELECT * FROM twitch_notifications WHERE username=?",
                (username,)
        ) as cursor:
            result = await cursor.fetchone()
            return result


async def set_notification_channel(guild_id: int, notification_channel: int) -> str:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(
            f"INSERT INTO guild_notification_channel (guild_id, notification_channel) VALUES (?, ?)",
            (guild_id, notification_channel,))
        await database.commit()
        return f"Set Channel with ID {notification_channel} as Notification Channel."


async def get_notification_channel(guild_id: int) -> int:
    async with aiosqlite.connect(database_path) as database:
        async with database.execute(
                f"SELECT notification_channel FROM guild_notification_channel WHERE guild_id=?",
                (guild_id,)
        ) as cursor:
            result = await cursor.fetchone()
            return result[0]


async def set_guild_administrator(guild_id: int, user_id: str) -> str:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(f"INSERT INTO guild_admins (guild_id, user_id) VALUES (?, ?)",
                               (guild_id, user_id,))
        await database.commit()
        return f"Added {user_id} as admin."


async def get_guild_administrator(guild_id: int) -> list:
    async with aiosqlite.connect(database_path) as database:
        async with database.execute(
                f"SELECT user_id FROM guild_admins WHERE guild_id=?",
                (guild_id,)
        ) as cursor:
            result = await cursor.fetchall()
            administrators = []
            for admin in result:
                administrators.append(admin[0])
            return administrators


async def remove_guild_administrator(guild_id: int, username: str) -> str:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(
            f"DELETE FROM guild_admins where guild_id=? AND user_id=?",
            (guild_id, username,)
        )
        await database.commit()
        return f"Removed {username} from Administrators for this Guild."


async def get_watchlist(guild_id: int) -> list:
    async with aiosqlite.connect(database_path) as database:
        async with database.execute(
                f"SELECT username FROM twitch_watchlist WHERE guild_id=?",
                (guild_id,)
        ) as cursor:
            result = await cursor.fetchall()
            watchlist = []
            for user in result:
                watchlist.append(user[0])
            return watchlist


async def set_watchlist(guild_id: int, username: str) -> str:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(f"INSERT INTO twitch_watchlist (guild_id, username) VALUES (?, ?)",
                               (guild_id, username,))
        await database.commit()
        return f"Added {username} to Watchlist."


async def remove_watchlist(guild_id: int, username: str) -> str:
    async with aiosqlite.connect(database_path) as database:
        await database.execute(
            f"DELETE FROM twitch_watchlist where guild_id=? AND username=?",
            (guild_id, username,)
        )
        await database.commit()
        return f"Removed {username} from Watchlist for this Guild."
