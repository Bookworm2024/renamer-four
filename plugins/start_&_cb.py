# extra imports
import asyncio, datetime, time, psutil, shutil

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# bots imports
from helper.database import digital_botz
from config import Config, Txt, VERSION, OWNER_ID
from helper.utils import humanbytes
from plugins import (
    __version__ as _bot_version_, __developer__, __database__,
    __library__, __language__, __programer__,
)


# ── Reusable keyboards ──────────────────────────────────────────

def start_keyboard(premium: bool):
    kb = [
        [
            InlineKeyboardButton('📢 Updates', url='https://t.me/trinityXmods'),
            InlineKeyboardButton('💬 Support', url='https://t.me/+iV0nZk2DK9w0MDA1'),
        ],
        [
            InlineKeyboardButton('ℹ️ About', callback_data='about'),
            InlineKeyboardButton('📖 Help', callback_data='help'),
        ],
    ]
    if premium:
        kb.append([InlineKeyboardButton('💎 Go Premium', callback_data='upgrade')])
    return InlineKeyboardMarkup(kb)


upgrade_button = InlineKeyboardMarkup([
    [InlineKeyboardButton('💎 Buy Premium', user_id=OWNER_ID)],
    [InlineKeyboardButton('◀️ Back', callback_data="start")],
])

upgrade_trial_button = InlineKeyboardMarkup([
    [InlineKeyboardButton('💎 Buy Premium', user_id=OWNER_ID)],
    [
        InlineKeyboardButton("🎁 Free Trial · 12h", callback_data="give_trial"),
        InlineKeyboardButton("◀️ Back", callback_data="start"),
    ],
])


# ── /start ──────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await digital_botz.add_user(client, message)
    kb = start_keyboard(client.premium)
    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=kb,
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(user.mention),
            reply_markup=kb,
            disable_web_page_preview=True,
        )


# ── /id & /ping (quick utilities) ───────────────────────────────

@Client.on_message(filters.private & filters.command("id"))
async def get_id(client, message):
    uid = message.from_user.id
    reply = message.reply_to_message
    text = f"<b>🆔 Your ID:</b> <code>{uid}</code>"
    if reply and reply.from_user:
        text += f"\n<b>👤 Replied User ID:</b> <code>{reply.from_user.id}</code>"
    await message.reply_text(text, quote=True)


@Client.on_message(filters.private & filters.command("ping"))
async def ping(client, message):
    start_t = time.time()
    msg = await message.reply_text("🏓 Pinging…")
    delta = (time.time() - start_t) * 1000
    await msg.edit(f"🏓 <b>Pong!</b>  <code>{delta:.0f} ms</code>")


# ── /myplan ─────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    if not client.premium:
        return

    user_id = message.from_user.id
    user = message.from_user.mention

    if await digital_botz.has_premium_access(user_id):
        data = await digital_botz.get_user(user_id)
        expiry = data.get("expiry_time")
        time_left = expiry - datetime.datetime.now()

        text = (
            f"<b>💎 ᴛʀɪɴɪᴛʏ ᴘʀᴇᴍɪᴜᴍ</b>\n\n"
            f"<b>👤 User :</b> {user}\n"
            f"<b>🆔 ID   :</b> <code>{user_id}</code>\n"
        )

        if client.uploadlimit:
            await digital_botz.reset_uploadlimit_access(user_id)
            ud = await digital_botz.get_user_data(user_id)
            limit = ud.get('uploadlimit', 0)
            used = ud.get('used_limit', 0)
            remain = int(limit) - int(used)
            ptype = ud.get('usertype', "Free")
            text += (
                f"<b>🏷 Plan :</b> <code>{ptype}</code>\n"
                f"<b>📦 Daily Limit :</b> <code>{humanbytes(limit)}</code>\n"
                f"<b>📤 Used Today  :</b> <code>{humanbytes(used)}</code>\n"
                f"<b>♻️ Remaining   :</b> <code>{humanbytes(remain)}</code>\n"
            )

        text += (
            f"<b>⏳ Time Left :</b> <code>{str(time_left).split('.')[0]}</code>\n"
            f"<b>📅 Expires   :</b> <code>{expiry.strftime('%d %b %Y, %I:%M %p')}</code>"
        )
        await message.reply_text(text, quote=True)
        return

    # Non-premium
    if client.uploadlimit:
        ud = await digital_botz.get_user_data(user_id)
        limit = ud.get('uploadlimit', 0)
        used = ud.get('used_limit', 0)
        remain = int(limit) - int(used)
        ptype = ud.get('usertype', "Free")
        text = (
            f"<b>🆓 ʏᴏᴜʀ ᴘʟᴀɴ</b>\n\n"
            f"<b>👤 User :</b> {user}\n"
            f"<b>🆔 ID   :</b> <code>{user_id}</code>\n"
            f"<b>🏷 Plan :</b> <code>{ptype}</code>\n"
            f"<b>📦 Daily Limit :</b> <code>{humanbytes(limit)}</code>\n"
            f"<b>📤 Used Today  :</b> <code>{humanbytes(used)}</code>\n"
            f"<b>♻️ Remaining   :</b> <code>{humanbytes(remain)}</code>\n"
            f"<b>📅 Expires :</b> <code>Lifetime (Free)</code>\n\n"
            f"<i>Want more power? Tap below 👇</i>"
        )
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💎 View Premium Plans", callback_data='upgrade')]]
            ),
            quote=True,
        )
    else:
        await message.reply_text(
            f"<b>Hey {user},</b>\n\nYou don't have an active premium plan yet. "
            f"Tap below to unlock unlimited power 👇",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("💎 View Premium Plans", callback_data='upgrade')]]
            ),
        )


# ── /plans ──────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command("plans"))
async def plans(client, message):
    if not client.premium:
        return

    user = message.from_user
    msg = Txt.UPGRADE_PLAN if client.uploadlimit else Txt.UPGRADE_PREMIUM

    free_trial_status = await digital_botz.get_free_trial_status(user.id)
    if not await digital_botz.has_premium_access(user.id) and not free_trial_status:
        kb = upgrade_trial_button
    else:
        kb = upgrade_button
    await message.reply_text(text=msg, reply_markup=kb, disable_web_page_preview=True)


# ── Callback router ─────────────────────────────────────────────

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data

    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=start_keyboard(client.premium),
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🖼 Thumbnail", callback_data="thumbnail"),
                    InlineKeyboardButton("📝 Caption", callback_data="caption"),
                ],
                [
                    InlineKeyboardButton("🏷 Prefix / Suffix", callback_data="custom_file_name"),
                    InlineKeyboardButton("🧬 Metadata", callback_data="digital_meta_data"),
                ],
                [
                    InlineKeyboardButton("ℹ️ About", callback_data="about"),
                    InlineKeyboardButton("◀️ Back", callback_data="start"),
                ],
            ]),
        )

    elif data == "about":
        about_button = [
            [
                InlineKeyboardButton("👨‍💻 Developers", callback_data="source_code"),
                InlineKeyboardButton("📊 Bot Status", callback_data="bot_status"),
            ],
            [InlineKeyboardButton("📡 Live Status", callback_data="live_status")],
        ]
        if client.premium:
            about_button[-1].append(InlineKeyboardButton("💎 Premium", callback_data="upgrade"))
        about_button.append([InlineKeyboardButton("◀️ Back", callback_data="start")])

        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(
                client.mention, __programer__, __developer__,
                __library__, __language__, __database__, _bot_version_,
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(about_button),
        )

    elif data == "upgrade":
        if not client.premium:
            return await query.message.delete()
        msg = Txt.UPGRADE_PLAN if client.uploadlimit else Txt.UPGRADE_PREMIUM
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not await digital_botz.has_premium_access(query.from_user.id) and not free_trial_status:
            kb = upgrade_trial_button
        else:
            kb = upgrade_button
        await query.message.edit_text(text=msg, disable_web_page_preview=True, reply_markup=kb)

    elif data == "give_trial":
        if not client.premium:
            return await query.message.delete()
        await query.message.delete()
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not free_trial_status:
            await digital_botz.give_free_trail(query.from_user.id)
            new_text = (
                "<b>🎁 Trial Activated!</b>\n\n"
                "Your <b>12-hour premium trial</b> is now live. "
                "Enjoy unlimited renaming — go send a file! 🚀"
            )
        else:
            new_text = (
                "<b>⚠️ Trial Already Used</b>\n\n"
                "You've already claimed your free trial. "
                "Check out our plans → /plans"
            )
        await client.send_message(query.from_user.id, text=new_text)

    elif data == "thumbnail":
        await query.message.edit_text(
            text=Txt.THUMBNAIL,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="help")]]),
        )

    elif data == "caption":
        await query.message.edit_text(
            text=Txt.CAPTION,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="help")]]),
        )

    elif data == "custom_file_name":
        await query.message.edit_text(
            text=Txt.CUSTOM_FILE_NAME,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="help")]]),
        )

    elif data == "digital_meta_data":
        await query.message.edit_text(
            text=Txt.METADATA_INFO,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="help")]]),
        )

    elif data == "bot_status":
        total_users = await digital_botz.total_users_count()
        if client.premium:
            total_premium_users = await digital_botz.total_premium_users_count()
        else:
            total_premium_users = "Disabled ✅"
        uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - client.uptime))
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        await query.message.edit_text(
            text=Txt.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="about")]]),
        )

    elif data == "live_status":
        currentTime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - client.uptime))
        total, used, free = shutil.disk_usage(".")
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_text(
            text=Txt.LIVE_STATUS.format(
                currentTime, cpu_usage, ram_usage,
                humanbytes(total), humanbytes(used), disk_usage,
                humanbytes(free), sent, recv, VERSION,
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Back", callback_data="about")]]),
        )

    elif data == "source_code":
        await query.message.edit_text(
            text=Txt.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Updates", url="https://t.me/trinityXmods")],
                [
                    InlineKeyboardButton("🔒 Close", callback_data="close"),
                    InlineKeyboardButton("◀️ Back", callback_data="start"),
                ],
            ]),
        )

    elif data == "close":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            pass
        try:
            await query.message.continue_propagation()
        except Exception:
            pass
