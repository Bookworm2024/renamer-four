# imports
from pyrogram import Client, filters 
from helper.database import digital_botz

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    if len(message.command) == 1:
       return await rkn.edit("**__Give The Caption__\n\nExample:- `/set_caption {filename}\n\n💾 SiZe: {filesize}\n\n⏰ Duration: {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await digital_botz.set_caption(message.from_user.id, caption=caption)
    await rkn.edit("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")
   
@Client.on_message(filters.private & filters.command(['del_caption', 'delete_caption', 'delcaption']))
async def delete_caption(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if not caption:
       return await rkn.edit("__**😔 You Don't Have Any Caption**__")
    await digital_botz.set_caption(message.from_user.id, caption=None)
    await rkn.edit("__**❌️ Caption Deleted**__")
                                       
@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if caption:
       await rkn.edit(f"**You'Re Caption:-**\n\n`{caption}`")
    else:
       await rkn.edit("__**😔 You Don't Have Any Caption**__")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
        await rkn.delete()
    else:
        await rkn.edit("😔 __**You Don't Have Any Thumbnail**__")
		
@Client.on_message(filters.private & filters.command(['del_thumb', 'delete_thumb', 'delthumb']))
async def removethumb(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await digital_botz.set_thumbnail(message.from_user.id, file_id=None)
        await rkn.edit("❌️ __**Thumbnail Deleted**__")
        return
    await rkn.edit("😔 __**You Don't Have Any Thumbnail**__")


@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    rkn = await message.reply_text("__**Please Wait**__")
    await digital_botz.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await rkn.edit("✅️ __**Thumbnail Saved**__")
