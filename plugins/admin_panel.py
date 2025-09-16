# extra imports
from config import Config
from helper.database import digital_botz
from helper.utils import get_seconds, humanbytes
import os, sys, time, asyncio, logging, datetime, pytz, traceback

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
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    rkn = await message.reply('**Processing.....**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rkn.edit(text=f"**--Bot Status--** \n\n**⌚️ Bot Uptime:** {uptime} \n**🐌 Current Ping:** `{time_taken_s:.3f} ᴍꜱ` \n**👭 Total Users:** `{total_users}`\n**💸 Total Premium Users:** `{total_premium_users}`")

# bot logs process 
@Client.on_message(filters.command('logs') & filters.user(Config.ADMIN))
async def log_file(b, m):
    try:
        await m.reply_document('BotLog.txt')
    except Exception as e:
        await m.reply(str(e))

@Client.on_message(filters.command(["addpremium", "add_premium"]) & filters.user(Config.ADMIN))
async def add_premium(client, message):
    if not client.premium:
        return await message.reply_text("premium mode disabled ✅")
     
    if client.uploadlimit:
        if len(message.command) < 4:
            return await message.reply_text("Usage : /addpremium user_id Plan_Type (e.g... `Pro`, `UltraPro`) time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')", quote=True)

        user_id = int(message.command[1])
        plan_type = message.command[2]

        if plan_type not in ["Pro", "UltraPro"]:
            return await message.reply_text("Invalid Plan Type. Please use 'Pro' or 'UltraPro'.", quote=True)

        time_string = " ".join(message.command[3:])

        time_zone = datetime.datetime.now(pytz.timezone("Asia/Colombo"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Joining Time : %I:%M:%S %p")

        user = await client.get_users(user_id)

        if plan_type == "Pro":
            limit = 107374182400
            type = "Pro"
        elif plan_type == "UltraPro":
            limit = 1073741824000
            type = "UltraPro"

        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("Invalid time format. Please use `/addpremium user_id 1 year 1 month 1 day 1 min 10 s`", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time}
        await digital_botz.addpremium(user_id, user_data, limit, type)

        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        type = user_data.get('usertype', "Free")
        data = await digital_botz.get_user(user_id)
        expiry = data.get("expiry_time")
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Colombo")).strftime("%d-%m-%Y\n⏱️ Expire Time : %I:%M:%S %p")

        await message.reply_text(f"Premium Added Successfully ✅\n\n👤 USER : {user.mention}\n⚡ USER ID : <code>{user_id}</code>\nPLAN :- `{type}`\nDAILY UPLOAD LIMIT :- `{humanbytes(limit)}`\n⏰ PREMIUM ACCESS : <code>{time_string}</code>\n\n⏳ JOINING DATE : {current_time}\n\n⌛️ EXPIRE DATE : {expiry_str_in_ist}", quote=True, disable_web_page_preview=True)

        await client.send_message(
                chat_id=user_id,
                text=f"👋 Hey {user.mention},\nThank You for Purchasing Premium.\nEnjoy !! ✨🎉\n\n⏰ PREMIUM ACCESS : <code>{time}</code>\nPLAN :- `{type}`\nDAILY UPLOAD LIMIT :- `{humanbytes(limit)}`\n⏳ JOINING DATE : {current_time}\n\n⌛️ EXPIRE DATE : {expiry_str_in_ist}", disable_web_page_preview=True
            )    

    else:
        if len(message.command) < 3:
            return await message.reply_text("Usage : /addpremium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')", quote=True)

        user_id = int(message.command[1])
        time_string = " ".join(message.command[2:])

        time_zone = datetime.datetime.now(pytz.timezone("Asia/Colombo"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ JOINING TIME : %I:%M:%S %p")

        user = await client.get_users(user_id)        
        seconds = await get_seconds(time_string)
        if seconds <= 0:
            return await message.reply_text("Invalid time format. Please use `/addpremium user_id 1 year 1 month 1 day 1 min 10 s`", quote=True)

        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
        user_data = {"id": user_id, "expiry_time": expiry_time}
        await digital_botz.addpremium(user_id, user_data)
        data = await digital_botz.get_user(user_id)
        expiry = data.get("expiry_time")
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Colombo")).strftime("%d-%m-%Y\n⏱️ EXPIRE TIME : %I:%M:%S %p")

        await message.reply_text(f"Premium Added Successfully ✅\n\n👤 USER : {user.mention}\n⚡ USER ID : <code>{user_id}</code>\n⏰ PREMIUM ACCESS: <code>{time_string}</code>\n\n⏳ JOINING DATE : {current_time}\n\n⌛️ EXPIRE DATE : {expiry_str_in_ist}", quote=True, disable_web_page_preview=True)

        await client.send_message(
                chat_id=user_id,
                text=f"👋 ʜᴇʏ {user.mention},\nThank You For Purchasing Premium.\nEnjoy !! ✨🎉\n\n⏰ PREMIUM ACCESS : <code>{time}</code>\n⏳ JOINING DATE : {current_time}\n\n⌛️ EXPIRE DATE : {expiry_str_in_ist}", disable_web_page_preview=True
            )    
     

@Client.on_message(filters.command(["removepremium", "remove_premium"]) & filters.user(Config.ADMIN))
async def remove_premium(bot, message):
    if not bot.premium:
        return await message.reply_text("premium mode disabled ✅")
     
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await bot.get_users(user_id)
        if await digital_botz.has_premium_access(user_id):
            await digital_botz.remove_premium(user_id)
            await message.reply_text(f"Hey {user.mention}, Premium Plan Successfully Removed.", quote=True)
            await bot.send_message(chat_id=user_id, text=f"<b>Hey {user.mention},\n\n✨ Your Account Has Been Removed From Our Premium Plan\n\nᴄCheck Your Plan Here /myplan</b>")
        else:
            await message.reply_text("Unable to Remove Premium User !\nAre You Sure, It Was a Premium User ID?", quote=True)
    else:
        await message.reply_text("USAAGE : /remove_premium USER ID", quote=True)


# Restart to cancell all process 
@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    rkn = await b.send_message(text="**🔄 Process Stopped. Bot Is Restarting....**", chat_id=m.chat.id)
    failed = 0
    success = 0
    deactivated = 0
    blocked = 0
    start_time = time.time()
    total_users = await digital_botz.total_users_count()
    all_users = await digital_botz.get_all_users()
    async for user in all_users:
        try:
            restart_msg = f"ʜᴇʏ, {(await b.get_users(user['_id'])).mention}\n\n**🔄 Process Stopped. Bot Is Restarting.....\n\n✅️ Bot Is Restarted. Now Tou Can Use Me.**"
            await b.send_message(user['_id'], restart_msg)
            success += 1
        except InputUserDeactivated:
            deactivated +=1
            await digital_botz.delete_user(user['_id'])
        except UserIsBlocked:
            blocked +=1
            await digital_botz.delete_user(user['_id'])
        except Exception as e:
            failed += 1
            await digital_botz.delete_user(user['_id'])
            print(e)
            pass
        try:
            await rkn.edit(f"<u>Restart In Progress:</u>\n\n• TOTAL USERS: {total_users}\n• SUCCESSFUL: {success}\n• BLOCKED USERS: {blocked}\n• DELETED ACCOUNTS: {deactivated}\n• UNSUCCESSFUL: {failed}")
        except FloodWait as e:
            await asyncio.sleep(e.value)
    completed_restart = datetime.timedelta(seconds=int(time.time() - start_time))
    await rkn.edit(f"Completed Restart: {completed_restart}\n\n• TOTAL USERS: {total_users}\n• SUCCESSFUL: {success}\n• BLOCKED USERS: {blocked}\n• DELETED ACCOUNTS: {deactivated}\n• UNSUCCESSFUL: {failed}")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("ban") & filters.user(Config.ADMIN))
async def ban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\n"
            f"Usage:\n\n"
            f"`/ban user_id ban_duration ban_reason`\n\n"
            f"Eg: `/ban 1234567 28 You misused me.`\n"
            f"This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(user_id,              
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n"
                f"**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await digital_botz.ban_user(user_id, ban_duration, ban_reason)
        await m.reply_text(ban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("unban") & filters.user(Config.ADMIN))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\n"
            f"Usage:\n\n`/unban user_id`\n\n"
            f"Eg: `/unban 1234567`\n"
            f"This will unban user with id `1234567`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await digital_botz.remove_ban(user_id)
        await m.reply_text(unban_log_text, quote=True)
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occurred! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )


@Client.on_message(filters.private & filters.command("banned_users") & filters.user(Config.ADMIN))
async def _banned_users(_, m: Message):
    all_banned_users = await digital_botz.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, " \
                f"**Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)

     
@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} Is Started the Broadcast......")
    all_users = await digital_botz.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast Started..!")
    done = 0
    failed = 0
    success = 0
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
           await sts_msg.edit(f"Broadcast In Progress: \nTOTAL USERS {total_users} \nCOMPLETED: {done} / {total_users}\nSUCCESS: {success}\nFAILED: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Broadcast Completed: \nCompleted In `{completed_in}`.\n\nTOTAL USERS {total_users}\nCOMPLETED: {done} / {total_users}\nSUCCESS: {success}\nFAILED: {failed}")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Blocked the Bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : User ID Invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
