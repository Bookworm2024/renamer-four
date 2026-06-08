import re, os, time

id_pattern = re.compile(r'^.\d+$')

# ─────────────────────────────────────────────
#            TRINITY MODS · FILE RENAMER
#                 Core Configuration
# ─────────────────────────────────────────────

VERSION = "v5.0.0 · Trinity"
BRAND = "Trinity Mods"
UPDATES_CHANNEL = "trinityXmods"
SUPPORT_LINK = "https://t.me/+iV0nZk2DK9w0MDA1"
UPDATES_LINK = "https://t.me/trinityXmods"
GITHUB_LINK = "https://github.com/Trinity-Mods"
OWNER_ID = 6011680723


class Config(object):
    # ── Telegram client ──
    API_ID = os.environ.get("API_ID", "21145186")
    API_HASH = os.environ.get("API_HASH", "daa53f4216112ad22b8a8f6299936a46")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # Premium TG account string session — required only for 4GB+ uploads.
    STRING_SESSION = os.environ.get("STRING_SESSION", "")

    # ── Database ──
    DB_NAME = os.environ.get("DB_NAME", "trinity_renamer")
    DB_URL = os.environ.get("DB_URL", "")

    # ── Branding / misc ──
    START_PIC = os.environ.get("START_PIC", "https://t.me/trinitypics/13")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin
             for admin in os.environ.get('ADMIN', str(OWNER_ID)).split()]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002495227151"))

    # Free daily upload limit (bytes) — 10 GB
    FREE_UPLOAD_LIMIT = 10 * 1024 * 1024 * 1024

    # Feature switches
    UPLOAD_LIMIT_MODE = True
    PREMIUM_MODE = True

    # Force subscribe channel
    try:
        FORCE_SUB = int(os.environ.get("FORCE_SUB", ""))
    except Exception:
        FORCE_SUB = os.environ.get("FORCE_SUB", UPDATES_CHANNEL)

    # Web health endpoint
    PORT = int(os.environ.get("PORT", "9898"))
    BOT_UPTIME = time.time()

    # Timezone used across the bot
    TIMEZONE = os.environ.get("TIMEZONE", "Asia/Colombo")


# ─────────────────────────────────────────────
#            ALL USER-FACING TEXT
# ─────────────────────────────────────────────

class Txt(object):

    START_TXT = """<b>ʜᴇʏ {} 👋</b>

I'm <b>Trinity Renamer</b> — a blazing-fast file engine built by <a href="https://t.me/trinityXmods">Trinity Mods</a>. ⚡

<b>Here's what I can do for you:</b>
›  📂  Rename any file in seconds
›  🖼  Attach a permanent custom thumbnail
›  🎞  Swap between Document · Video · Audio
›  📝  Set custom captions & metadata
›  🏷  Auto-add a prefix / suffix

<b>Just send me a file to begin.</b> 🚀"""

    ABOUT_TXT = """<b>╭─❰ ⚙️ ᴀʙᴏᴜᴛ ᴍᴇ ❱</b>
<b>│</b>
<b>├ 🤖 Bot      :</b> {}
<b>├ 👑 Owner    :</b> {}
<b>├ 🧑‍💻 Dev      :</b> {}
<b>├ 📚 Library  :</b> {}
<b>├ ✏️ Language :</b> {}
<b>├ 🗄 Database :</b> {}
<b>├ 🔖 Version  :</b> <a href="https://t.me/trinityXmods">{}</a>
<b>│</b>
<b>╰─❰ Powered by Trinity Mods ❱</b>"""

    HELP_TXT = """<b>📖 ᴛʀɪɴɪᴛʏ ʀᴇɴᴀᴍᴇʀ — ɢᴜɪᴅᴇ</b>

<b>How renaming works:</b>
<b>1.</b>  Send me any file 📂
<b>2.</b>  Reply with the new name <i>(with extension)</i>
<b>3.</b>  Pick the output → 📄 Document · 🎞 Video · 🎵 Audio

Tap a button below to explore each feature 👇

<i>Need a hand? Join</i> <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Support</a> 💬"""

    UPGRADE_PREMIUM = """<b>💎 ᴛʀɪɴɪᴛʏ ᴘʀᴇᴍɪᴜᴍ</b>

<b>Tier ·  Duration ·  Price</b>
🥉  <b>Bronze</b>    ·  3 Days    ·  30
🥈  <b>Silver</b>    ·  7 Days    ·  70
🥇  <b>Gold</b>      ·  15 Days   ·  150
🏆  <b>Platinum</b>  ·  1 Month   ·  300
💠  <b>Diamond</b>   ·  2 Months  ·  600

<b>✨ Every tier unlocks:</b>
›  ♾ Unlimited daily uploads
›  ⚡ Priority processing
›  🎁 10% off all plans"""

    UPGRADE_PLAN = """<b>💎 ᴛʀɪɴɪᴛʏ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs</b>

🔹 <b>Pro</b>
   ⏳ 1 Month  ·  💸 150  ·  📦 100 GB / day

🔸 <b>Ultra Pro</b>
   ⏳ 1 Month  ·  💸 300  ·  📦 1000 GB / day

<b>✨ Bonus:</b> 10% off when you renew early."""

    THUMBNAIL = """<b>🖼 ᴄᴜsᴛᴏᴍ ᴛʜᴜᴍʙɴᴀɪʟ</b>

›  📸  Send any photo — I'll save it as your thumbnail.
›  👁  /view_thumb — preview the saved one.
›  🗑  /del_thumb — remove it.

<i>Your thumbnail is applied automatically to every rename.</i>"""

    CAPTION = """<b>📝 ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ</b>

›  ✏️  /set_caption — set your caption
›  👁  /see_caption — view it
›  🗑  /del_caption — delete it

<b>Available variables:</b>
<code>{filename}</code> · <code>{filesize}</code> · <code>{duration}</code>

<b>Example:</b>
<code>/set_caption
📕 {filename}
💾 {filesize}
⏱ {duration}</code>"""

    BOT_STATUS = """<b>⚡ ᴛʀɪɴɪᴛʏ · ʙᴏᴛ sᴛᴀᴛᴜs</b>

<b>⌚ Uptime        :</b> <code>{}</code>
<b>👥 Total Users   :</b> <code>{}</code>
<b>💎 Premium Users :</b> <code>{}</code>
<b>📤 Uploaded      :</b> <code>{}</code>
<b>📥 Downloaded    :</b> <code>{}</code>"""

    LIVE_STATUS = """<b>📡 ᴛʀɪɴɪᴛʏ · ʟɪᴠᴇ sᴇʀᴠᴇʀ</b>

<b>⌚ Uptime    :</b> <code>{}</code>
<b>🧠 CPU       :</b> <code>{}%</code>
<b>💾 RAM       :</b> <code>{}%</code>
<b>🗄 Disk      :</b> <code>{}</code>
<b>📂 Used      :</b> <code>{} ({}%)</code>
<b>📤 Free      :</b> <code>{}</code>
<b>⬆️ Upload    :</b> <code>{}</code>
<b>⬇️ Download  :</b> <code>{}</code>
<b>🔖 Version   :</b> <code>{}</code>"""

    METADATA_INFO = """<b>🧬 ᴄᴜsᴛᴏᴍ ᴍᴇᴛᴀᴅᴀᴛᴀ</b>

Use /metadata to toggle on/off and set your code.

<b>Supported flags:</b>
<code>--change-title @trinityXmods</code>
<code>--change-video-title @trinityXmods</code>
<code>--change-audio-title @trinityXmods</code>
<code>--change-subtitle-title @trinityXmods</code>
<code>--change-author @trinityXmods</code>

<i>Stuck?</i> Join <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Support</a> 💬"""

    SEND_METADATA = """<b>🧬 sᴇɴᴅ ʏᴏᴜʀ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴄᴏᴅᴇ</b>

Paste any of the flags below (one per line):
<code>--change-title @trinityXmods</code>
<code>--change-video-title @trinityXmods</code>
<code>--change-audio-title @trinityXmods</code>
<code>--change-subtitle-title @trinityXmods</code>
<code>--change-author @trinityXmods</code>"""

    CUSTOM_FILE_NAME = """<b>🏷 ᴘʀᴇғɪx & sᴜғғɪx</b>

Automatically wrap every renamed file with your own tag.

<b>Prefix</b>
›  /set_prefix · /see_prefix · /del_prefix

<b>Suffix</b>
›  /set_suffix · /see_suffix · /del_suffix

<b>Example:</b>
<code>/set_prefix @trinityXmods</code>
<code>/set_suffix [TrinityMods]</code>"""

    DEV_TXT = """<b>💠 ᴛʀɪɴɪᴛʏ ᴍᴏᴅs</b>

Crafted with care by the Trinity Mods team.

›  📢  <b>Updates :</b> <a href="https://t.me/trinityXmods">@trinityXmods</a>
›  💬  <b>Support :</b> <a href="https://t.me/+iV0nZk2DK9w0MDA1">Trinity Support</a>
›  💻  <b>GitHub  :</b> <a href="https://github.com/Trinity-Mods">Trinity-Mods</a>

<i>Stay tuned for more powerful tools.</i>"""

    # Modern bordered progress card.
    # Slots: 0=action title, 1=bar, 2=current, 3=total, 4=percent, 5=speed, 6=eta
    PROGRESS_BAR = """<b>{0}</b>

<b>╭━━━━━━━━━━━━━━━━━━━➣</b>
<b>┃ {1}</b>
<b>┃ 📦 {2}  of  {3}</b>
<b>┃ ⚡ {4}%</b>
<b>┃ 🚀 {5}/s</b>
<b>┃ ⏱ {6}</b>
<b>╰━━━━━━━━━━━━━━━━━━━➣</b>"""
