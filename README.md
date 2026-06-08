<h1 align="center">⚡ Trinity Mods · File Renamer ⚡</h1>

<p align="center">
  <b>A blazing-fast, powerful Telegram file-renaming bot.</b><br>
  Rename, re-thumbnail, re-caption, re-metadata — Document · Video · Audio.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v5.0.0-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Pyrogram-2.x-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge">
</p>

---

## ✨ Features

- ⚡ **Fast renaming** with a time-throttled progress bar (fewer flood-waits = faster transfers)
- 🖼 **Permanent custom thumbnails**
- 🎞 **Convert** between Document · Video · Audio output
- 📝 **Custom captions** with `{filename}` · `{filesize}` · `{duration}`
- 🧬 **Custom metadata** (title / author / video / audio / subtitle)
- 🏷 **Prefix & suffix** auto-tagging
- 💎 **Premium plans**, daily upload limits & **12-hour free trial**
- 🔒 **Force-subscribe** support
- 🛠 **Admin panel** — stats, broadcast, ban/unban, premium management, logs, restart
- 📦 **4GB+ uploads** via a premium account string session
- 🚀 **uvloop** event loop for extra speed

---

## 🚀 Deploy

| Platform | |
|---|---|
| **Docker** | `docker build -t trinity-renamer . && docker run trinity-renamer` |
| **Render / Koyeb / Railway / Heroku** | Use `render.yaml` / `app.json` and set the env vars below |

---

## ⚙️ Configuration

| Variable | Required | Description |
|---|---|---|
| `BOT_TOKEN` | ✅ | From [@BotFather](https://t.me/BotFather) |
| `API_ID` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `ADMIN` | ✅ | Admin user IDs (space-separated) |
| `DB_URL` | ✅ | MongoDB URL from [cloud.mongodb.com](https://cloud.mongodb.com) |
| `DB_NAME` | ➖ | MongoDB database name |
| `FORCE_SUB` | ➖ | Channel username (without `@`) |
| `LOG_CHANNEL` | ➖ | Log channel ID (must start with `-100`) |
| `START_PIC` | ➖ | Start-message image URL |
| `STRING_SESSION` | ➖ | Premium account session — **required for 4GB+ files** |
| `TIMEZONE` | ➖ | Defaults to `Asia/Colombo` |

---

## 🤖 BotFather Commands

```
start - check I am alive
plans - upgrade to premium
myplan - check your premium plan
ping - check bot latency
id - get your telegram id
view_thumb - view your custom thumbnail
del_thumb - delete your custom thumbnail
set_caption - set a custom caption
see_caption - see your custom caption
del_caption - delete your custom caption
metadata - set & change your metadata
set_prefix - set your prefix
see_prefix - see your prefix
del_prefix - delete your prefix
set_suffix - set your suffix
see_suffix - see your suffix
del_suffix - delete your suffix
restart - restart the bot (admin)
addpremium - add premium (admin)
remove_premium - remove premium (admin)
ban - ban a user (admin)
unban - unban a user (admin)
banned_users - list banned users (admin)
logs - get bot logs (admin)
status - bot status (admin)
broadcast - broadcast a message (admin)
```

---

## 💠 Trinity Mods

- 📢 Updates: [@trinityXmods](https://t.me/trinityXmods)
- 💬 Support: [Trinity Support](https://t.me/+iV0nZk2DK9w0MDA1)
- 💻 GitHub: [Trinity-Mods](https://github.com/Trinity-Mods)

<p align="center"><i>Built with ❤️ by Trinity Mods.</i></p>
