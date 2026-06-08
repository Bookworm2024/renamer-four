# extra imports
from config import Config, VERSION
from helper.database import digital_botz
from helper.utils import get_seconds, humanbytes
import os, sys, time, asyncio, logging, datetime, pytz, traceback, html

# pyrogram imports
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await digital_botz.total_users_count()
    if bot.premium:
        total_premium_users = await digital_botz.total_premium_users_count()
    else:
        total_premium_users = "Disabled ✅"
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - bot.uptime))
    start_t = time.time()
    msg = await message.reply('<b>📊 Crunching numbers…</b>')
    ping = (time.time() - start_t) * 1000
    await msg.edit(
        f"<b>📊 ᴛʀɪɴɪᴛʏ · ᴀᴅᴍɪɴ sᴛᴀᴛs</b>\n\n"
        f"<b>⌚ Uptime  :</b> <code>{uptime}</code>\n"
        f"<b>🐌 Ping    :</b> <code>{ping:.0f} ms</code>\n"
        f"<b>👥 Users   :</b> <code>{total_users}</code>\n"
        f"<b>💎 Premium :</b> <code>{total_premium_users}</code>\n"
        f"<b>🔖 Version :</b> <code>{VERSION}</code>"
    )


@Client.on_message(filters.command('logs') & filters.user(Config.ADMIN))
async def log_file(b, m):
    try:
        await m.reply_document('BotLog.txt', caption="<b>📄 Trinity bot logs</b>")
    except Exception as e:
        await m.reply(str(e))


@Client.on_message(filters.command(["addpremium", "add_premium"]) & filters.user(Config.ADMIN))
async def add_premium(client, message):
    if not client.premium:
        return await message.reply_text("<b>Premium mode is disabled ✅</b>")

    tz = datetime.datetime.now(pytz.timezone(Config.TIMEZONE))
    joining_date = tz.strftime("%d-%m-%Y · %I:%M:%S %p")

    if client.uploadlimit:
        if len(message.command) < 4:
            return await message.reply_text(
                "<b>Usage:</b> <code>/addpremium user_id Plan_Type duration</code>\n\n"
                "Plan_Type → <code>Pro</code> or <code>UltraPro</code>\n"
                "Duration  → e.g. <code>1 month</code>, <code>7 day</code>, <code>12 hour</code>",
                quote=True,
            )

        user_id = int(message.command[1])
        plan_type = message.command[2]
        if plan_type not in ["Pro", "UltraPro"]:
            return await message.reply_text("<b>Invalid plan.</b> Use <code>Pro</code> or <code>UltraPro</code>.", quote=True)

        time_string = " ".join(message.command[3:])
        user = await client.get_users(user_id)
        limit = 107374182400 if plan_type == "Pro" else 1073741824000
        ptype = plan_type

        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("<b>Invalid time format.</b> e.g. <code>/addpremium id Pro 1 month</code>", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        await digital_botz.addpremium(user_id, {"id": user_id, "expiry_time": expiry_time}, limit, ptype)

        ud = await digital_botz.get_user_data(user_id)
        limit = ud.get('uploadlimit', 0)
        ptype = ud.get('usertype', "Free")
        data = await digital_botz.get_user(user_id)
        expiry_str = data.get("expiry_time").astimezone(
            pytz.timezone(Config.TIMEZONE)).strftime("%d-%m-%Y · %I:%M:%S %p")

        await message.reply_text(
            f"<b>✅ ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ</b>\n\n"
            f"<b>👤 User  :</b> {user.mention}\n"
            f"<b>🆔 ID    :</b> <code>{user_id}</code>\n"
            f"<b>🏷 Plan  :</b> <code>{ptype}</code>\n"
            f"<b>📦 Limit :</b> <code>{humanbytes(limit)}</code>\n"
            f"<b>⏰ For   :</b> <code>{time_string}</code>\n"
            f"<b>📅 Start :</b> <code>{joining_date}</code>\n"
            f"<b>⌛ Ends  :</b> <code>{expiry_str}</code>",
            quote=True, disable_web_page_preview=True,
        )
        await client.send_message(
            chat_id=user_id,
            text=(
                f"<b>🎉 Welcome to Trinity Premium, {user.mention}!</b>\n\n"
                f"<b>🏷 Plan  :</b> <code>{ptype}</code>\n"
                f"<b>📦 Limit :</b> <code>{humanbytes(limit)}</code>\n"
                f"<b>⏰ For   :</b> <code>{time_string}</code>\n"
                f"<b>📅 Start :</b> <code>{joining_date}</code>\n"
                f"<b>⌛ Ends  :</b> <code>{expiry_str}</code>\n\n"
                f"Enjoy unlimited power ⚡"
            ),
            disable_web_page_preview=True,
        )

    else:
        if len(message.command) < 3:
            return await message.reply_text(
                "<b>Usage:</b> <code>/addpremium user_id duration</code>\n"
                "Duration → e.g. <code>1 month</code>, <code>7 day</code>, <code>12 hour</code>",
                quote=True,
            )

        user_id = int(message.command[1])
        time_string = " ".join(message.command[2:])
        user = await client.get_users(user_id)
        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("<b>Invalid time format.</b> e.g. <code>/addpremium id 1 month</code>", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        await digital_botz.addpremium(user_id, {"id": user_id, "expiry_time": expiry_time})
        data = await digital_botz.get_user(user_id)
        expiry_str = data.get("expiry_time").astimezone(
            pytz.timezone(Config.TIMEZONE)).strftime("%d-%m-%Y · %I:%M:%S %p")

        await message.reply_text(
            f"<b>✅ ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ</b>\n\n"
            f"<b>👤 User  :</b> {user.mention}\n"
            f"<b>🆔 ID    :</b> <code>{user_id}</code>\n"
            f"<b>⏰ For   :</b> <code>{time_string}</code>\n"
            f"<b>📅 Start :</b> <code>{joining_date}</code>\n"
            f"<b>⌛ Ends  :</b> <code>{expiry_str}</code>",
            quote=True, disable_web_page_preview=True,
        )
        await client.send_message(
            chat_id=user_id,
            text=(
                f"<b>🎉 Welcome to Trinity Premium, {user.mention}!</b>\n\n"
                f"<b>⏰ For   :</b> <code>{time_string}</code>\n"
                f"<b>📅 Start :</b> <code>{joining_date}</code>\n"
                f"<b>⌛ Ends  :</b> <code>{expiry_str}</code>\n\n"
                f"Enjoy unlimited power ⚡"
            ),
            disable_web_page_preview=True,
        )


@Client.on_message(filters.command(["removepremium", "remove_premium"]) & filters.user(Config.ADMIN))
async def remove_premium(bot, message):
    if not bot.premium:
        return await message.reply_text("<b>Premium mode is disabled ✅</b>")
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await bot.get_users(user_id)
        if await digital_botz.has_premium_access(user_id):
            await digital_botz.remove_premium(user_id)
            await message.reply_text(f"<b>✅ Premium removed for {user.mention}.</b>", quote=True)
            await bot.send_message(
                chat_id=user_id,
                text=f"<b>Hey {user.mention},</b>\n\nYour Trinity Premium has ended. Check your plan → /myplan",
            )
        else:
            await message.reply_text("<b>That user isn't a premium member.</b>", quote=True)
    else:
        await message.reply_text("<b>Usage:</b> <code>/remove_premium user_id</code>", quote=True)


@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    note = await b.send_message(chat_id=m.chat.id, text="<b>🔄 Restarting Trinity Renamer…</b>")
    failed = success = deactivated = blocked = 0
    start_time = time.time()
    total_users = await digital_botz.total_users_count()
    all_users = await digital_botz.get_all_users()
    async for user in all_users:
        try:
            mention = (await b.get_users(user['_id'])).mention
            await b.send_message(
                user['_id'],
                f"<b>Hey {mention},</b>\n\n🔄 The bot just restarted and is back online. You can use me again! ✅",
            )
            success += 1
        except InputUserDeactivated:
            deactivated += 1
            await digital_botz.delete_user(user['_id'])
        except UserIsBlocked:
            blocked += 1
            await digital_botz.delete_user(user['_id'])
        except Exception as e:
            failed += 1
            await digital_botz.delete_user(user['_id'])
            print(e)
        try:
            await note.edit(
                f"<b>🔄 Restart in progress…</b>\n\n"
                f"• Total: <code>{total_users}</code>\n"
                f"• Success: <code>{success}</code>\n"
                f"• Blocked: <code>{blocked}</code>\n"
                f"• Deleted: <code>{deactivated}</code>\n"
                f"• Failed: <code>{failed}</code>"
            )
        except FloodWait as e:
            await asyncio.sleep(e.value)
    completed = datetime.timedelta(seconds=int(time.time() - start_time))
    await note.edit(
        f"<b>✅ Restart complete in {completed}</b>\n\n"
        f"• Total: <code>{total_users}</code>\n"
        f"• Success: <code>{success}</code>\n"
        f"• Blocked: <code>{blocked}</code>\n"
        f"• Deleted: <code>{deactivated}</code>\n"
        f"• Failed: <code>{failed}</code>"
    )
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            "<b>Ban a user from the bot.</b>\n\n"
            "<b>Usage:</b> <code>/ban user_id duration_days reason</code>\n"
            "<b>Example:</b> <code>/ban 1234567 28 misuse</code>",
            quote=True,
        )
        return
    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        log_text = f"Banning {user_id} for {ban_duration} days — {html.escape(ban_reason)}."
        try:
            await c.send_message(
                user_id,
                f"<b>🚫 You've been banned for {ban_duration} day(s).</b>\n"
                f"<b>Reason:</b> <i>{html.escape(ban_reason)}</i>",
            )
            log_text += '\n\nUser notified ✅'
        except Exception:
            traceback.print_exc()
            log_text += f"\n\nNotify failed:\n<code>{html.escape(traceback.format_exc())}</code>"
        await digital_botz.ban_user(user_id, ban_duration, ban_reason)
        await m.reply_text(log_text, quote=True)
    except Exception:
        traceback.print_exc()
        await m.reply_text(f"<b>Error:</b>\n<code>{html.escape(traceback.format_exc())}</code>", quote=True)


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            "<b>Unban a user.</b>\n\n"
            "<b>Usage:</b> <code>/unban user_id</code>",
            quote=True,
        )
        return
    try:
        user_id = int(m.command[1])
        log_text = f"Unbanning {user_id}"
        try:
            await c.send_message(user_id, "<b>✅ Your ban has been lifted. Welcome back!</b>")
            log_text += '\n\nUser notified ✅'
        except Exception:
            traceback.print_exc()
            log_text += f"\n\nNotify failed:\n<code>{html.escape(traceback.format_exc())}</code>"
        await digital_botz.remove_ban(user_id)
        await m.reply_text(log_text, quote=True)
    except Exception:
        traceback.print_exc()
        await m.reply_text(f"<b>Error:</b>\n<code>{html.escape(traceback.format_exc())}</code>", quote=True)


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(_, m: Message):
    all_banned_users = await digital_botz.get_all_banned_users()
    count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        count += 1
        text += (
            f"• <b>ID:</b> <code>{user_id}</code> · <b>Days:</b> <code>{ban_duration}</code> · "
            f"<b>On:</b> <code>{banned_on}</code> · <b>Reason:</b> <code>{html.escape(str(ban_reason))}</code>\n\n"
        )
    reply_text = f"<b>🚫 Banned users: {count}</b>\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    try:
        await bot.send_message(Config.LOG_CHANNEL, f"📢 {m.from_user.mention} (<code>{m.from_user.id}</code>) started a broadcast.")
    except Exception:
        pass
    all_users = await digital_botz.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("<b>📢 Broadcast started…</b>")
    done = failed = success = 0
    start_time = time.time()
    total_users = await digital_botz.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await digital_botz.delete_user(user['_id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"<b>📢 Broadcasting…</b>\n\n"
                f"• Total: <code>{total_users}</code>\n"
                f"• Done: <code>{done}</code>\n"
                f"• Success: <code>{success}</code>\n"
                f"• Failed: <code>{failed}</code>"
            )
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"<b>✅ Broadcast complete in {completed_in}</b>\n\n"
        f"• Total: <code>{total_users}</code>\n"
        f"• Done: <code>{done}</code>\n"
        f"• Success: <code>{success}</code>\n"
        f"• Failed: <code>{failed}</code>"
    )


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Blocked the bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Invalid ID")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
