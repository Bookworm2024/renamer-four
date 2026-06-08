# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

# extra imports
import html
from helper.database import digital_botz
from pyromod.exceptions import ListenerTimeout
from config import Txt

ON_KB = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('🧬 Metadata: ON', callback_data='metadata_1'),
        InlineKeyboardButton('✅', callback_data='metadata_1'),
    ],
    [InlineKeyboardButton('✏️ Set Custom Metadata', callback_data='cutom_metadata')],
])

OFF_KB = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('🧬 Metadata: OFF', callback_data='metadata_0'),
        InlineKeyboardButton('❌', callback_data='metadata_0'),
    ],
    [InlineKeyboardButton('✏️ Set Custom Metadata', callback_data='cutom_metadata')],
])


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):
    wait = await message.reply_text("<b>⏳ Loading…</b>", reply_to_message_id=message.id)
    bool_metadata = await digital_botz.get_metadata_mode(message.from_user.id)
    user_metadata = await digital_botz.get_metadata_code(message.from_user.id)
    await wait.edit(
        f"<b>🧬 ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴍᴇᴛᴀᴅᴀᴛᴀ</b>\n\n<code>{html.escape(str(user_metadata))}</code>",
        reply_markup=ON_KB if bool_metadata else OFF_KB,
    )


@Client.on_callback_query(filters.regex('.*?(custom_metadata|metadata).*?'))
async def query_metadata(bot: Client, query: CallbackQuery):
    data = query.data
    if data.startswith('metadata_'):
        _bool = data.split('_')[1]
        user_metadata = await digital_botz.get_metadata_code(query.from_user.id)
        bool_meta = bool(int(_bool))
        await digital_botz.set_metadata_mode(query.from_user.id, bool_meta=not bool_meta)
        await query.message.edit(
            f"<b>🧬 ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ ᴍᴇᴛᴀᴅᴀᴛᴀ</b>\n\n<code>{html.escape(str(user_metadata))}</code>",
            reply_markup=OFF_KB if bool_meta else ON_KB,
        )

    elif data == 'cutom_metadata':
        await query.message.delete()
        try:
            metadata = await bot.ask(
                text=Txt.SEND_METADATA, chat_id=query.from_user.id,
                filters=filters.text, timeout=60, disable_web_page_preview=True,
            )
            wait = await query.message.reply_text("<b>⏳ Saving…</b>", reply_to_message_id=metadata.id)
            await digital_botz.set_metadata_code(query.from_user.id, metadata_code=metadata.text)
            await wait.edit("<b>✅ Metadata code saved successfully.</b>")
        except ListenerTimeout:
            await query.message.reply_text(
                "<b>⚠️ Timed out.</b>\nRestart with /metadata",
                reply_to_message_id=query.message.id,
            )
        except Exception as e:
            print(e)
