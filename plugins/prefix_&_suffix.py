# imports
from pyrogram import Client, filters, enums
from helper.database import digital_botz

# prefix commond ✨
@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_prefix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExample:- `/set_prefix @trinityXmods`**")
    prefix = message.text.split(" ", 1)[1]
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await digital_botz.set_prefix(message.from_user.id, prefix)
    await RknDev.edit("__**✅ Prefix Saved**__")

@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if not prefix:
        return await RknDev.edit("__**😔 You Don't Have Any Prefix**__")
    await digital_botz.set_prefix(message.from_user.id, None)
    await RknDev.edit("__**❌️ Prefix Deleted**__")

@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_prefix(client, message):
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if prefix:
        await RknDev.edit(f"**Your Prefix:-**\n\n`{prefix}`")
    else:
        await RknDev.edit("__**😔 You Don't Have Any Prefix**__")

# SUFFIX COMMOND ✨
@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_suffix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @trinityXmods`**")
    suffix = message.text.split(" ", 1)[1]
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await digital_botz.set_suffix(message.from_user.id, suffix)
    await RknDev.edit("__**✅ Suffix Saved**__")

@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if not suffix:
        return await RknDev.edit("__**😔 You Don't Have Any Suffix**__")
    await digital_botz.set_suffix(message.from_user.id, None)
    await RknDev.edit("__**❌️ Suffix Deleted**__")

@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_suffix(client, message):
    RknDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if suffix:
        await RknDev.edit(f"**Your Suffix:-**\n\n`{suffix}`")
    else:
        await RknDev.edit("__**😔 You Don't Have Any Suffix**__")
