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
import os, time, asyncio


UPLOAD_TEXT = """Uploading..."""
DOWNLOAD_TEXT = """Downloading..."""

app = Client(
    name="4gb_FileRenameBot",
    api_id=os.environ.get("API_ID") or Config.API_ID,
    api_hash=os.environ.get("API_HASH") or Config.API_HASH,
    session_string=os.environ.get("STRING_SESSION") or Config.STRING_SESSION
)

@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
    rkn_file = getattr(message, message.media.value)
    filename = rkn_file.file_name
    filesize = humanbytes(rkn_file.file_size)
    mime_type = rkn_file.mime_type
    dcid = FileId.decode(rkn_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    if client.premium and client.uploadlimit:
        await digital_botz.reset_uploadlimit_access(user_id)
        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        remain = int(limit) - int(used)
        if int(limit) > 0:
            used_percentage = int(used) / int(limit) * 100
        else:
            used_percentage = 0  # Default to 0% usage if limit is 0

        if remain < int(rkn_file.file_size):
            return await message.reply_text(f"{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\nYou have only **{humanbytes(remain)}** Data.\nPlease, Buy Premium Plan s.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]]))
         
	    
    if await digital_botz.has_premium_access(user_id) and client.premium:
        if not Config.STRING_SESSION:
            if rkn_file.file_size > 2000 * 1024 * 1024 and client.premium:
                return await message.reply_text("If you want to rename 4GB+ files then you will have to buy premium. /plans")


        try:
            await message.reply_text(
            text=f"**__Media Info:\n\n◈ Old File Name: `{filename}`\n\n◈ Extension: `{extension_type.upper()}`\n◈ File Size: `{filesize}`\n◈ Mime Type: `{mime_type}`\n◈ DC ID: `{dcid}`\n\nPlease Enter The New Filename With Extension And Reply This Message....__**",
	    reply_to_message_id=message.id,  
	    reply_markup=ForceReply(True)
        )       
            await sleep(30)
        except FloodWait as e:
            await sleep(e.value)
            await message.reply_text(
            text=f"**__Media Info:\n\n◈ ᴏʟᴅ File Name: `{filename}`\n\n◈ Extension: `{extension_type.upper()}`\n◈ File Size: `{filesize}`\n◈ Mime Type: `{mime_type}`\n◈ DC ID: `{dcid}`\n\nPlease Enter The New Filename With Extension And Reply This Message....__**",
	    reply_to_message_id=message.id,  
	    reply_markup=ForceReply(True)
        )
        except:
            pass
    else:
        if rkn_file.file_size > 2000 * 1024 * 1024 and client.premium:
            return await message.reply_text("If you want to rename 4GB+ files then you will have to buy premium. /plans")

        try:
            await message.reply_text(
            text=f"**__Media Info:\n\n◈ Old File Name: `{filename}`\n\n◈ Extension: `{extension_type.upper()}`\n◈ File Size: `{filesize}`\n◈ Mime Type: `{mime_type}`\n◈ DC ID: `{dcid}`\n\nPlease Enter The New Filename With Extension And Reply This Message....__**",
	    reply_to_message_id=message.id,  
	    reply_markup=ForceReply(True)
        )       
            await sleep(30)
        except FloodWait as e:
            await sleep(e.value)
            await message.reply_text(
            text=f"**__Media Info:\n\n◈ Old File Name: `{filename}`\n\n◈ Extension: `{extension_type.upper()}`\n◈ File Size: `{filesize}`\n◈ Mime Type: `{mime_type}`\n◈ DC ID: `{dcid}`\n\nPlease Enter The New Filename With Extension And Reply This Message....__**",
	    reply_to_message_id=message.id,  
	    reply_markup=ForceReply(True)
        )
        except:
            pass

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        new_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()

        button = [[InlineKeyboardButton("📁 Document",callback_data = "upload_document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Video", callback_data = "upload_video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Audio", callback_data = "upload_audio")])
        await message.reply(
            text=f"**Select The Output File Typeᴇ**\n**• File Name :-**`{new_name}`",
            reply_to_message_id=file.id,
            reply_markup=InlineKeyboardMarkup(button)
        )



@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):
    rkn_processing = await update.message.edit("`Processing...`")
	
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")

    user_id = int(update.message.chat.id) 
    new_name = update.message.text
    new_filename_ = new_name.split(":-")[1]
    user_data = await digital_botz.get_user_data(user_id)

    try:
        # adding prefix and suffix
        prefix = await digital_botz.get_prefix(user_id)
        suffix = await digital_botz.get_suffix(user_id)
        new_filename = add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await rkn_processing.edit(f"⚠️ Something went wrong. I am unable to change suffix/prefix at the moment. Please try again later. If the issue persists, please contact support - https://t.me/+iV0nZk2DK9w0MDA1\nError: {e}")

    # msg file location 
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
	
    # file downloaded path
    file_path = f"Renames/{new_filename}"
    
    metadata_path = f"Metadata/{new_filename}"    

    await rkn_processing.edit("`Try To Download....`")
    if bot.premium and bot.uploadlimit:
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        await digital_botz.set_used_limit(user_id, media.file_size)
        total_used = int(used) + int(media.file_size)
        await digital_botz.set_used_limit(user_id, total_used)
	
    try:
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time()))                    
    except Exception as e:
        if bot.premium and bot.uploadlimit:
            used_remove = int(used) - int(media.file_size)
            await digital_botz.set_used_limit(user_id, used_remove)
        return await rkn_processing.edit(e)

    metadata_mode = await digital_botz.get_metadata_mode(user_id)
    if (metadata_mode):        
        metadata = await digital_botz.get_metadata_code(user_id)
        if metadata:
            await rkn_processing.edit("I Found Your METADATA\n\n__**Please Wait...**__\n**ADDING METADATA TO FILE....**")
            if change_metadata(dl_path, metadata_path, metadata):            
                await rkn_processing.edit("Metadata Added.....")
                print("Metadata Added.....")
        await rkn_processing.edit("**Metadata added to the file successfully ✅**\n\n**Uploading...**")
    else:
        await rkn_processing.edit("`Uploading...`")
	    
    duration = 0
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()
    except:
        pass
	    
    ph_path = None
    c_caption = await digital_botz.get_caption(user_id)
    c_thumb = await digital_botz.get_thumbnail(user_id)

    if c_caption:
         try:
             # adding custom caption 
             caption = c_caption.format(filename=new_filename, filesize=humanbytes(media.file_size), duration=convert(duration))
         except Exception as e:
             if bot.premium and bot.uploadlimit:
                 used_remove = int(used) - int(media.file_size)
                 await digital_botz.set_used_limit(user_id, used_remove)
             return await rkn_processing.edit(text=f"Your Caption Error Except Keyword Argument ●> ({e})")
    else:
         caption = f"**{new_filename}**"
 
    if (media.thumbs or c_thumb):
         # downloading thumbnail path
         if c_thumb:
             ph_path = await bot.download_media(c_thumb) 
         else:
             ph_path = await bot.download_media(media.thumbs[0].file_id)
         Image.open(ph_path).convert("RGB").save(ph_path)
         img = Image.open(ph_path)
         img.resize((320, 320))
         img.save(ph_path, "JPEG")

    type = update.data.split("_")[1]
    if media.file_size > 2000 * 1024 * 1024:
        try:
            if type == "document":
                filw = await app.send_document(
                    Config.LOG_CHANNEL,
                    document=metadata_path if metadata_mode else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))

                from_chat = filw.chat.id
                mg_id = filw.id
                time.sleep(2)
                await bot.copy_message(update.from_user.id, from_chat, mg_id)
                await bot.delete_messages(from_chat, mg_id)
            elif type == "video":
                filw = await app.send_video(
                    Config.LOG_CHANNEL,
                    video=metadata_path if metadata_mode else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))

                from_chat = filw.chat.id
                mg_id = filw.id
                time.sleep(2)
                await bot.copy_message(update.from_user.id, from_chat, mg_id)
                await bot.delete_messages(from_chat, mg_id)
            elif type == "audio":
                filw = await app.send_audio(
                    Config.LOG_CHANNEL,
                    audio=metadata_path if metadata_mode else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))

                from_chat = filw.chat.id
                mg_id = filw.id
                time.sleep(2)
                await bot.copy_message(update.from_user.id, from_chat, mg_id)
                await bot.delete_messages(from_chat, mg_id)
        except Exception as e:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await rkn_processing.edit(f" ERROR {e}")
    else:
        try:
            if type == "document":
                await bot.send_document(
                    update.message.chat.id,
                    document=metadata_path if metadata_mode else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
            elif type == "video":
                await bot.send_video(
                    update.message.chat.id,
                    video=metadata_path if metadata_mode else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
            elif type == "audio":
                await bot.send_audio(
                    update.message.chat.id,
                    audio=metadata_path if metadata_mode else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        except Exception as e:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await rkn_processing.edit(f" ERROR {e}")

# please give credit 🙏🥲
		    
    await remove_path(ph_path, file_path, dl_path, metadata_path)
    return await rkn_processing.edit("Uploaded successfully!")
