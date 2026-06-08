# pyrogram imports
from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

# hachoir imports
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# bots imports
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from helper.ffmpeg import change_metadata
from config import Config

# extra imports
from asyncio import sleep
import os, time


UPLOAD_TEXT = "📤 ᴜᴘʟᴏᴀᴅɪɴɢ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ"
DOWNLOAD_TEXT = "📥 ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ꜰɪʟᴇ"
TWO_GB = 2000 * 1024 * 1024

# Premium-account client (only used for 4GB+ uploads via LOG_CHANNEL relay).
app = Client(
    name="trinity_4gb_client",
    api_id=os.environ.get("API_ID") or Config.API_ID,
    api_hash=os.environ.get("API_HASH") or Config.API_HASH,
    session_string=os.environ.get("STRING_SESSION") or Config.STRING_SESSION,
)


@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id = message.from_user.id
    rkn_file = getattr(message, message.media.value)
    filename = rkn_file.file_name
    filesize = humanbytes(rkn_file.file_size)
    mime_type = rkn_file.mime_type
    dcid = FileId.decode(rkn_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    # ── Daily upload-limit guard ──
    if client.premium and client.uploadlimit:
        await digital_botz.reset_uploadlimit_access(user_id)
        user_data = await digital_botz.get_user_data(user_id)
        limit = int(user_data.get('uploadlimit', 0))
        used = int(user_data.get('used_limit', 0))
        remain = limit - used
        used_pct = (used / limit * 100) if limit > 0 else 0

        if remain < int(rkn_file.file_size):
            return await message.reply_text(
                f"<b>🚫 Daily Limit Reached</b>\n\n"
                f"<b>📦 Plan Limit :</b> <code>{humanbytes(limit)}</code>\n"
                f"<b>📤 Used Today :</b> <code>{humanbytes(used)}</code> ({used_pct:.1f}%)\n"
                f"<b>♻️ Remaining  :</b> <code>{humanbytes(remain)}</code>\n"
                f"<b>🎬 This File  :</b> <code>{filesize}</code>\n\n"
                f"<i>Upgrade to keep going 👇</i>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("💎 Upgrade", callback_data="upgrade")]]
                ),
            )

    # ── 4GB+ requires premium string session ──
    if rkn_file.file_size > TWO_GB and client.premium:
        if not Config.STRING_SESSION:
            return await message.reply_text(
                "<b>⚠️ File Too Large</b>\n\n"
                "Renaming files over <b>2 GB</b> needs a premium plan. → /plans"
            )

    # ── Media info card + ask for new name ──
    info_card = (
        f"<b>📂 ꜰɪʟᴇ ʀᴇᴄᴇɪᴠᴇᴅ</b>\n\n"
        f"<b>📄 Name :</b> <code>{filename}</code>\n"
        f"<b>🏷 Type :</b> <code>{extension_type.upper()}</code>\n"
        f"<b>💾 Size :</b> <code>{filesize}</code>\n"
        f"<b>🧩 Mime :</b> <code>{mime_type}</code>\n"
        f"<b>🌐 DC   :</b> <code>{dcid}</code>\n\n"
        f"<b>✏️ Reply to this message with the new file name (include the extension).</b>"
    )
    try:
        await message.reply_text(
            text=info_card,
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True),
        )
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=info_card,
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True),
        )
    except Exception:
        pass


@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if reply_message.reply_markup and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text
        await message.delete()
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)

        if "." not in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = f"{new_name}.{extn}"
        await reply_message.delete()

        button = [[InlineKeyboardButton("📄 Document", callback_data="upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎞 Video", callback_data="upload_video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Audio", callback_data="upload_audio")])

        # NOTE: the ":-" delimiter is parsed by the upload callback — keep it intact.
        await message.reply(
            text=f"<b>🎯 ᴄʜᴏᴏsᴇ ᴏᴜᴛᴘᴜᴛ ꜰᴏʀᴍᴀᴛ</b>\n\n<b>• File Name :-</b><code>{new_name}</code>",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button),
        )


@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    rkn_processing = await update.message.edit("<b>⚙️ Processing…</b>")

    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    user_id = int(update.message.chat.id)
    new_name = update.message.text
    new_filename_ = new_name.split(":-", 1)[1].strip()
    user_data = await digital_botz.get_user_data(user_id)

    try:
        prefix = await digital_botz.get_prefix(user_id)
        suffix = await digital_botz.get_suffix(user_id)
        new_filename = add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await rkn_processing.edit(
            "<b>⚠️ Couldn't apply your prefix/suffix.</b>\n"
            "Please try again, or contact <a href='https://t.me/+iV0nZk2DK9w0MDA1'>Trinity Support</a>.\n"
            f"<code>{e}</code>"
        )

    file = update.message.reply_to_message
    media = getattr(file, file.media.value)

    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"

    await rkn_processing.edit("<b>📥 Starting download…</b>")

    # Reserve the quota up-front; restore it if anything fails.
    used = 0
    if bot.premium and bot.uploadlimit:
        used = int(user_data.get('used_limit', 0))
        await digital_botz.set_used_limit(user_id, used + int(media.file_size))

    async def refund():
        if bot.premium and bot.uploadlimit:
            await digital_botz.set_used_limit(user_id, used)

    try:
        dl_path = await bot.download_media(
            message=file, file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time()),
        )
    except Exception as e:
        await refund()
        return await rkn_processing.edit(f"<b>❌ Download failed:</b> <code>{e}</code>")

    # ── Optional metadata pass ──
    metadata_mode = await digital_botz.get_metadata_mode(user_id)
    if metadata_mode:
        metadata = await digital_botz.get_metadata_code(user_id)
        if metadata:
            await rkn_processing.edit("<b>🧬 Applying metadata…</b>")
            if change_metadata(dl_path, metadata_path, metadata):
                await rkn_processing.edit("<b>✅ Metadata applied.</b>\n\n<b>📤 Uploading…</b>")
            else:
                await rkn_processing.edit("<b>⚠️ Metadata skipped.</b>\n\n<b>📤 Uploading…</b>")
    else:
        await rkn_processing.edit("<b>📤 Uploading…</b>")

    # ── Duration ──
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()
    except Exception:
        pass

    # ── Caption ──
    c_caption = await digital_botz.get_caption(user_id)
    c_thumb = await digital_botz.get_thumbnail(user_id)
    if c_caption:
        try:
            caption = c_caption.format(
                filename=new_filename,
                filesize=humanbytes(media.file_size),
                duration=convert(duration),
            )
        except Exception as e:
            await refund()
            return await rkn_processing.edit(f"<b>⚠️ Caption error:</b> <code>{e}</code>")
    else:
        caption = f"<b>{new_filename}</b>"

    # ── Thumbnail ──
    ph_path = None
    if c_thumb or media.thumbs:
        ph_path = await bot.download_media(c_thumb if c_thumb else media.thumbs[0].file_id)
        try:
            img = Image.open(ph_path).convert("RGB")
            img.thumbnail((320, 320))
            img.save(ph_path, "JPEG")
        except Exception:
            pass

    upload_path = metadata_path if (metadata_mode and os.path.lexists(metadata_path)) else file_path
    out_type = update.data.split("_")[1]

    # ── Upload (4GB+ relayed through premium client + LOG_CHANNEL) ──
    try:
        if media.file_size > TWO_GB:
            sender, target = app, Config.LOG_CHANNEL
        else:
            sender, target = bot, update.message.chat.id

        if out_type == "document":
            sent = await sender.send_document(
                target, document=upload_path, thumb=ph_path, caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()),
            )
        elif out_type == "video":
            sent = await sender.send_video(
                target, video=upload_path, caption=caption, thumb=ph_path, duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()),
            )
        elif out_type == "audio":
            sent = await sender.send_audio(
                target, audio=upload_path, caption=caption, thumb=ph_path, duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()),
            )

        # Relay the big file from the log channel back to the user.
        if media.file_size > TWO_GB:
            time.sleep(2)
            await bot.copy_message(update.from_user.id, sent.chat.id, sent.id)
            await bot.delete_messages(sent.chat.id, sent.id)

    except Exception as e:
        await refund()
        await remove_path(ph_path, file_path, dl_path, metadata_path)
        return await rkn_processing.edit(f"<b>❌ Upload failed:</b> <code>{e}</code>")

    await remove_path(ph_path, file_path, dl_path, metadata_path)
    await rkn_processing.edit("<b>✅ Done!</b>  Renamed & delivered by <b>Trinity Mods</b> ⚡")
