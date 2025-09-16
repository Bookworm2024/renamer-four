# extra imports
import random, asyncio, datetime, pytz, time, psutil, shutil

# pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery

# bots imports
from helper.database import digital_botz
from config import Config, rkn
from helper.utils import humanbytes
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__

upgrade_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('buy premium ✓', user_id=int(6011680723)),
         ],[
        InlineKeyboardButton("Back", callback_data = "start")
]])

upgrade_trial_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('buy premium ✓', user_id=int(6011680723)),
         ],[
        InlineKeyboardButton("Trial - 12 Hours ✓", callback_data = "give_trial"),
        InlineKeyboardButton("Back", callback_data = "start")
]])


        
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    start_button = [[        
        InlineKeyboardButton('Updates', url='https://t.me/trinityXmods'),
        InlineKeyboardButton('Support', url='https://t.me/+iV0nZk2DK9w0MDA1')
        ],[
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Help', callback_data='help')
         ]]
        
    if client.premium:
        start_button.append([InlineKeyboardButton('💸 Upgrade To Premium 💸', callback_data='upgrade')])
            
    user = message.from_user
    await digital_botz.add_user(client, message) 
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))
    else:
        await message.reply_text(text=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button), disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    if not client.premium:
        return # premium mode disabled ✓

    user_id = message.from_user.id
    user = message.from_user.mention
    
    if await digital_botz.has_premium_access(user_id):
        data = await digital_botz.get_user(user_id)
        expiry_str_in_ist = data.get("expiry_time")
        time_left_str = expiry_str_in_ist - datetime.datetime.now()

        text = f"USER :- {user}\nUSER ID :- <code>{user_id}</code>\n"

        if client.uploadlimit:
            await digital_botz.reset_uploadlimit_access(user_id)                
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text += f"Plan :- `{type}`\nDaily Upload Limit :- `{humanbytes(limit)}`\nToday Used :- `{humanbytes(used)}`\nRemain :- `{humanbytes(remain)}`\n"

        text += f"Time Left : {time_left_str}\nExpire Date : {expiry_str_in_ist}"

        await message.reply_text(text, quote=True)

    else:
        if client.uploadlimit:
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")

            text = f"USER :- {user}\nUSER ID :- <code>{user_id}</code>\nPlan :- `{type}`\nDaily Upload Limit :- `{humanbytes(limit)}`\nToday Used :- `{humanbytes(used)}`\nRemain :- `{humanbytes(remain)}`\nExpire Date :- Lifetime\n\nIf You Want TO Take Premium Then Click On Below Button 👇"

            await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Checkout Premium Plans 💸", callback_data='upgrade')]]), quote=True)

        else:
            m=await message.reply_sticker("CAACAgIAAxkBAAK3BmjJhKxZw7k69gqfgtx3OnnGF1DQAAJIAANSiZEjbtkuqJw9TwABNgQ")
            await message.reply_text(f"Hey {user},\n\nYou Do Not Have Any Active Premium Plan, If You Want TO Take Premium Then Click On Below Button 👇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 Checkout Premium Plans 💸", callback_data='upgrade')]]))
            await asyncio.sleep(2)
            await m.delete()

@Client.on_message(filters.private & filters.command("plans"))
async def plans(client, message):
    if not client.premium:
        return # premium mode disabled ✓

    user = message.from_user
    upgrade_msg = rkn.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else rkn.UPGRADE_PREMIUM.format(user.mention)
    
    free_trial_status = await digital_botz.get_free_trial_status(user.id)
    if not await digital_botz.has_premium_access(user.id):
        if not free_trial_status:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_trial_button, disable_web_page_preview=True)
        else:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, disable_web_page_preview=True)
    else:
        await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, disable_web_page_preview=True)
   
  
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        start_button = [[        
        InlineKeyboardButton('Updates', url='https://t.me/trinityXmods'),
        InlineKeyboardButton('Support', url='https://t.me/+iV0nZk2DK9w0MDA1')
        ],[
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Help', callback_data='help')
         ]]
            
        if client.premium:
            start_button.append([InlineKeyboardButton('💸 Upgrade To Premium 💸', callback_data='upgrade')])
            
        await query.message.edit_text(
            text=rkn.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup = InlineKeyboardMarkup(start_button))
        
    elif data == "help":
        await query.message.edit_text(
            text=rkn.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("Thumbnail", callback_data = "thumbnail"),
                InlineKeyboardButton("Caption", callback_data = "caption")
                ],[          
                InlineKeyboardButton("Custom File Name", callback_data = "custom_file_name")
                ],[          
                InlineKeyboardButton("About", callback_data = "about"),
                InlineKeyboardButton("METADATA", callback_data = "digital_meta_data")
                                     ],[
                InlineKeyboardButton("Back", callback_data = "start")
                  ]]))         
        
    elif data == "about":
        about_button = [[
         #⚠️ don't change source code & source link ⚠️ #
        InlineKeyboardButton("Source", callback_data = "source_code"), #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️
        InlineKeyboardButton("Bot Status", callback_data = "bot_status")
        ],[
        InlineKeyboardButton("Live Status", callback_data = "live_status")
        ]]
        if client.premium:
            about_button[-1].append(InlineKeyboardButton("Upgrade", callback_data = "upgrade"))
            about_button.append([InlineKeyboardButton("Back", callback_data = "start")])
        else:
            about_button[-1].append(InlineKeyboardButton("Back", callback_data = "start"))
            
        await query.message.edit_text(
            text=rkn.ABOUT_TXT.format(client.mention, __developer__, __programer__, __library__, __language__, __database__, _bot_version_),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(about_button))    
        
    elif data == "upgrade":
        if not client.premium:
            return await query.message.delete()
                
        user = query.from_user
        upgrade_msg = rkn.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else rkn.UPGRADE_PREMIUM.format(user.mention)
    
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not await digital_botz.has_premium_access(query.from_user.id):
            if not free_trial_status:
                await query.message.edit_text(text=upgrade_msg, disable_web_page_preview=True, reply_markup=upgrade_trial_button)   
            else:
                await query.message.edit_text(text=upgrade_msg, disable_web_page_preview=True, reply_markup=upgrade_button)
        else:
            await query.message.edit_text(text=upgrade_msg, disable_web_page_preview=True, reply_markup=upgrade_button)
           
    elif data == "give_trial":
        if not client.premium:
            return await query.message.delete()
                
        await query.message.delete()
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not free_trial_status:            
            await digital_botz.give_free_trail(query.from_user.id)
            new_text = "**Your Premiun Trial Has Added For 12 Hours.\n\nYou Can Use Free Trial 12 Hours From Now 😀\n\nआप अब से 𝟷𝟸 घण्टा के लिए निःशुल्क ट्रायल का उपयोग कर सकते हैं 😀**"
        else:
            new_text = "**🤣 You Already Used Free Now No More Free Trial. Please Buy Subscription Here Are Our 👉 /plans**"
        await client.send_message(query.from_user.id, text=new_text)

    elif data == "thumbnail":
        await query.message.edit_text(
            text=rkn.THUMBNAIL,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "help")]]))
      
    elif data == "caption":
        await query.message.edit_text(
            text=rkn.CAPTION,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "help")]]))
      
    elif data == "custom_file_name":
        await query.message.edit_text(
            text=rkn.CUSTOM_FILE_NAME,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "help")]]))
      
    elif data == "digital_meta_data":
        await query.message.edit_text(
            text=rkn.DIGITAL_METADATA,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "help")]]))
      
    elif data == "bot_status":
        total_users = await digital_botz.total_users_count()
        if client.premium:
            total_premium_users = await digital_botz.total_premium_users_count()
        else:
            total_premium_users = "Disabled ✅"
        
        uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        await query.message.edit_text(
            text=rkn.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "about")]]))
      
    elif data == "live_status":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))    
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_text(
            text=rkn.LIVE_STATUS.format(currentTime, cpu_usage, ram_usage, total, used, disk_usage, free, sent, recv),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton(" Back", callback_data = "about")]]))
      
    elif data == "source_code":
        await query.message.edit_text(
            text=rkn.DEV_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
           #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️   
                InlineKeyboardButton("UPDATES 🥳", url="https://t.me/trinityXmods")
            ],[
                InlineKeyboardButton("🔒 Close", callback_data = "close"),
                InlineKeyboardButton("◀️ Back", callback_data = "start")
                 ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
