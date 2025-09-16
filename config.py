import re, os, time
id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # digital_botz client config
    API_ID = os.environ.get("API_ID", "21145186")
    API_HASH = os.environ.get("API_HASH", "daa53f4216112ad22b8a8f6299936a46")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 

    # premium account string session required 😢 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    
    # database config
    DB_NAME = os.environ.get("DB_NAME","hornokplease")
    DB_URL = os.environ.get("DB_URL","")
 
    # other configs
    START_PIC = os.environ.get("START_PIC", "https://t.me/trinitypics/13")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6011680723').split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002495227151"))

    # free upload limit 
    FREE_UPLOAD_LIMIT = 10737418240  # 10 GB = 10 * 1024 * 1024 * 1024

    # premium mode feature ✅
    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    #force subs
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", "")) 
    except:
        FORCE_SUB = os.environ.get("FORCE_SUB", "trinityXmods")
        
    # wes response configuration     
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

class rkn(object):
    # part of text configuration
    START_TXT = """<b>Hi, {} 👋

Welcome to the Advanced & Powerful File Renamer Bot 🤖  
✨ With this bot you can:
• Rename files easily 📁  
• Change or add custom thumbnails 🖼️  
• Convert videos to files & files to videos 🎞️  
• Add custom captions & metadata 📑  

🔹 Developed with ❤️ by <a href="https://t.me/trinityXmods">Trinity Mods</a></b>"""

    ABOUT_TXT = """ <b>╭───────────⍟
├🤖 My Name    : {}
├🖥️ Developers : {}
├👨‍💻 Programmer : {}
├📕 Library    : {}
├✏️ Language   : {}
├💾 Data Base  : {}
├📊 Version    : <a href="https://t.me/trinityXmods">{}</a>
╰───────────────⍟</b> """

    HELP_TXT = """<b>📌 How to Use the Bot</b>

<b>•</b> Use <code>/start</code> to begin 🤖  

✏️ <b><u>How to Rename a File</u></b>  
<b>•</b> Send any file to the bot  
<b>•</b> Enter the new file name  
<b>•</b> Choose the format → Document 📄 | Video 🎞️ | Audio 🎵  

ℹ️ For help, contact <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Mods Support</a> 💬"""

    UPGRADE_PREMIUM= """<b>💎 Premium Plans</b>  

<b>•⪼ Plan ★ Duration ⏳ Price 💸</b>  
🥉 <b>Bronze</b>   – 3 Days   – 30  
🥈 <b>Silver</b>   – 7 Days   – 70  
🥇 <b>Gold</b>     – 15 Days  – 150  
🏆 <b>Platinum</b> – 1 Month  – 300  
💎 <b>Diamond</b>  – 2 Months – 600  

<b>✨ Benefits</b>  
✔ Unlimited Daily Uploads  
✔ 10% Discount on All Plans"""
    
    UPGRADE_PLAN= """<b>💎 Available Plans</b>  

📌 <b>Plan:</b> Pro  
⏳ <b>Duration:</b> 1 Month  
💸 <b>Price:</b> 150  
📦 <b>Limit:</b> 100 GB  

📌 <b>Plan:</b> Ultra Pro  
⏳ <b>Duration:</b> 1 Month  
💸 <b>Price:</b> 300  
📦 <b>Limit:</b> 1000 GB  

✨ <b>Extra Benefit:</b> 10% Discount on All Plans"""
    
    THUMBNAIL = """🌌 <b><u>How to Set Thumbnail</u></b>  

📸 <b>•</b> Send any photo to set it as your thumbnail.  
🗑️ <b>•</b> Use /del_thumb to delete your current thumbnail.  
👁️ <b>•</b> Use /view_thumb to view your current thumbnail."""
    
    CAPTION= """📑 <b><u>How to Set Custom Caption</u></b>  

✏️ <b>•</b> <code>/set_caption</code> – Set your custom caption.  
👁️ <b>•</b> <code>/see_caption</code> – View your current caption.  
🗑️ <b>•</b> <code>/del_caption</code> – Delete your custom caption.  

<b>📌 Example:</b>  
<code>/set_caption  
📕 FILE NAME: {filename}  
💾 SIZE: {filesize}  
⏰ DURATION: {duration}</code>"""
    
    BOT_STATUS = """⚡️ <b>Bot Status</b> ⚡️

⌚️ <b>Uptime:</b> `{}`
👥 <b>Total Users:</b> `{}`
💎 <b>Premium Users:</b> `{}`
⬆️ <b>Upload Speed:</b> `{}`
⬇️ <b>Download Speed:</b> `{}`
"""
    LIVE_STATUS = """⚡ <b>LIVE SERVER STATUS</b> ⚡

⌚️ <b>Uptime:</b> `{}`
🖥️ <b>CPU Usage:</b> `{}%`
💾 <b>RAM Usage:</b> `{}%`
🗄️ <b>Total Disk:</b> `{}`
📂 <b>Used Space:</b> `{} ({}%)`
📤 <b>Free Space:</b> `{}`
⬆️ <b>Upload Speed:</b> `{}`
⬇️ <b>Download Speed:</b> `{}`
🔖 <b>Version:</b> V3.0.0 [STABLE]
"""
    DIGITAL_METADATA = """❪ <b>SET CUSTOM METADATA</b> ❫

🔹 <b>Command:</b> /metadata  
Use this to set or change your custom metadata easily.

💡 <b>Examples:</b>
`--change-title @trinityXmods`  
`--change-video-title @trinityXmods`  
`--change-audio-title @trinityXmods`  
`--change-subtitle-title @trinityXmods`  
`--change-author @trinityXmods`

📥 For help, join the group: <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Mods Support</a>
"""
    
    CUSTOM_FILE_NAME = """<u>🖋️ Custom File Name</u>

You can pre-add a prefix or suffix along with your new filename.

➢ /set_prefix - Add a prefix to your filename  
➢ /see_prefix - View your current prefix  
➢ /del_prefix - Delete your prefix  

➢ /set_suffix - Add a suffix to your filename  
➢ /see_suffix - View your current suffix  
➢ /del_suffix - Delete your suffix  

💡 Examples:  
`/set_prefix @trinityXmods`  
`/set_suffix @trinityXmods`  

📥 For help, join: <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Mods Support</a>
"""

    DEV_TXT = """<b><u>Special Thanks & Developers</u></b>

• ❣️ Developer: @trinityXmods

The source code will be made available soon on our official channels:

📢 Telegram: <a href="https://t.me/trinityXmods">Trinity Mods</a>  
💻 GitHub: <a href="https://github.com/Trinity-Mods">Trinity-Mods</a>
"""

    SEND_METADATA = """❪ <b>SET CUSTOM METADATA</b> ❫

💡 <b>Examples:</b>
`--change-title @trinityXmods`  
`--change-video-title @trinityXmods`  
`--change-audio-title @trinityXmods`  
`--change-subtitle-title @trinityXmods`  
`--change-author @trinityXmods`

📥 For help, join: <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Mods Support</a>
"""
    
    RKN_PROGRESS = """<b>
{0}
❁ 🗃️ Size  : {1} | {2}
❁ ⏳ Done  : {3}%
❁ 🚀 Speed : {4}/s
❁ ⏰ ETA   : {5}</b>"""

