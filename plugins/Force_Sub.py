# pyrogram imports
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant

# extra imports
from config import Config
from helper.database import digital_botz
import datetime


async def not_subscribed(_, client, message):
    await digital_botz.add_user(client, message)
    if not Config.FORCE_SUB:
        return False
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        return user.status not in [
            enums.ChatMemberStatus.MEMBER,
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER,
        ]
    except UserNotParticipant:
        return True
    except Exception as e:
        print(f"Force-sub check error: {e}")
        return False


async def handle_banned_user_status(bot, message):
    await digital_botz.add_user(bot, message)
    user_id = message.from_user.id
    ban_status = await digital_botz.get_ban_status(user_id)
    if ban_status.get("is_banned", False):
        days = (datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])).days
        if days > ban_status["ban_duration"]:
            await digital_botz.remove_ban(user_id)
        else:
            return await message.reply_text(
                "<b>🚫 You're banned from using this bot.</b>\n\n"
                "Think it's a mistake? Reach out → "
                "<a href='https://t.me/+iV0nZk2DK9w0MDA1'>Trinity Support</a>"
            )
    await message.continue_propagation()


@Client.on_message(filters.private)
async def _(bot, message):
    await handle_banned_user_status(bot, message)


@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    buttons = [[InlineKeyboardButton(
        text="📢 Join Trinity Channel",
        url=f"https://t.me/{Config.FORCE_SUB}",
    )]]
    text = (
        "<b>🔒 ᴏɴᴇ ʟᴀsᴛ sᴛᴇᴘ!</b>\n\n"
        "To use <b>Trinity Renamer</b>, please join our channel first. "
        "Tap the button below, then send your file again. 👇"
    )
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)
        if user.status == enums.ChatMemberStatus.BANNED:
            return await message.reply_text("<b>🚫 You're banned from the channel.</b>")
    except UserNotParticipant:
        pass
    except Exception as e:
        print(f"Force-sub error: {e}")
    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
