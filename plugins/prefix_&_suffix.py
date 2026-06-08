# imports
import html
from pyrogram import Client, filters
from helper.database import digital_botz


# ── Prefix ───────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_prefix(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "<b>🏷 Send a prefix with the command.</b>\n\n"
            "<b>Example:</b> <code>/set_prefix @trinityXmods</code>"
        )
    prefix = message.text.split(" ", 1)[1]
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    await digital_botz.set_prefix(message.from_user.id, prefix)
    await wait.edit("<b>✅ Prefix saved.</b>")


@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if not prefix:
        return await wait.edit("<b>😶 You don't have a prefix set.</b>")
    await digital_botz.set_prefix(message.from_user.id, None)
    await wait.edit("<b>🗑 Prefix deleted.</b>")


@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_prefix(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if prefix:
        await wait.edit(f"<b>🏷 Your prefix:</b>\n\n<code>{html.escape(prefix)}</code>")
    else:
        await wait.edit("<b>😶 You don't have a prefix set.</b>")


# ── Suffix ───────────────────────────────────────────────────────

@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_suffix(client, message):
    if len(message.command) == 1:
        return await message.reply_text(
            "<b>🏷 Send a suffix with the command.</b>\n\n"
            "<b>Example:</b> <code>/set_suffix [TrinityMods]</code>"
        )
    suffix = message.text.split(" ", 1)[1]
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    await digital_botz.set_suffix(message.from_user.id, suffix)
    await wait.edit("<b>✅ Suffix saved.</b>")


@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if not suffix:
        return await wait.edit("<b>😶 You don't have a suffix set.</b>")
    await digital_botz.set_suffix(message.from_user.id, None)
    await wait.edit("<b>🗑 Suffix deleted.</b>")


@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_suffix(client, message):
    wait = await message.reply_text("<b>⏳ Please wait…</b>", reply_to_message_id=message.id)
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if suffix:
        await wait.edit(f"<b>🏷 Your suffix:</b>\n\n<code>{html.escape(suffix)}</code>")
    else:
        await wait.edit("<b>😶 You don't have a suffix set.</b>")
