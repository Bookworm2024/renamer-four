# imports
import html
from pyrogram import Client, filters
from helper.database import digital_botz


# ── Caption ──────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>")
    if len(message.command) == 1:
        return await wait.edit(
            "<b>📝 Send a caption with the command.</b>\n\n"
            "<b>Example:</b>\n"
            "<code>/set_caption 📕 {filename}\n💾 {filesize}\n⏱ {duration}</code>"
        )
    caption = message.text.split(" ", 1)[1]
    await digital_botz.set_caption(message.from_user.id, caption=caption)
    await wait.edit("<b>✅ Caption saved.</b>")


@Client.on_message(filters.private & filters.command(['del_caption', 'delete_caption', 'delcaption']))
async def delete_caption(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>")
    caption = await digital_botz.get_caption(message.from_user.id)
    if not caption:
        return await wait.edit("<b>😶 You don't have a caption set.</b>")
    await digital_botz.set_caption(message.from_user.id, caption=None)
    await wait.edit("<b>🗑 Caption deleted.</b>")


@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>")
    caption = await digital_botz.get_caption(message.from_user.id)
    if caption:
        await wait.edit(f"<b>📝 Your caption:</b>\n\n<code>{html.escape(caption)}</code>")
    else:
        await wait.edit("<b>😶 You don't have a caption set.</b>")


# ── Thumbnail ────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(
            chat_id=message.chat.id, photo=thumb,
            caption="<b>🖼 Your current thumbnail</b>",
        )
        await wait.delete()
    else:
        await wait.edit("<b>😶 You don't have a thumbnail set.</b>")


@Client.on_message(filters.private & filters.command(['del_thumb', 'delete_thumb', 'delthumb']))
async def removethumb(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await digital_botz.set_thumbnail(message.from_user.id, file_id=None)
        return await wait.edit("<b>🗑 Thumbnail deleted.</b>")
    await wait.edit("<b>😶 You don't have a thumbnail set.</b>")


@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    wait = await message.reply_text("<b>⏳ Saving…</b>")
    await digital_botz.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)
    await wait.edit("<b>✅ Thumbnail saved.</b>  It'll be applied to every rename.")
