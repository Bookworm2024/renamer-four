import aiohttp, asyncio, warnings, pytz, datetime
import logging
import logging.config
import glob, sys, importlib.util
from pathlib import Path

# Faster event loop where available (Linux/macOS).
try:
    import uvloop
    uvloop.install()
    _LOOP = "uvloop"
except Exception:
    _LOOP = "asyncio"

import pyromod  # noqa: F401

# pyrogram imports
import pyrogram.utils
from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer

# bots imports
from config import Config, VERSION, BRAND
from plugins.web_support import web_server
from plugins.file_rename import app


pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'), logging.StreamHandler()],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class TrinityRenamerBot(Client):
    def __init__(self):
        super().__init__(
            name="TrinityRenamerBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=250,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE

        # Web health server
        runner = aiohttp.web.AppRunner(await web_server())
        await runner.setup()
        await aiohttp.web.TCPSite(runner, "0.0.0.0", Config.PORT).start()

        # Import extra plugins explicitly (covers files not auto-loaded)
        for name in glob.glob("plugins/*.py"):
            plugin_name = Path(name).stem
            spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", Path(name))
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules[f"plugins{plugin_name}"] = load

        print("─" * 50)
        print(f"  {BRAND} · File Renamer  {VERSION}")
        print(f"  Bot   : @{me.username}  ({me.first_name})")
        print(f"  Loop  : {_LOOP}")
        print(f"  Layer : {__version__} (Layer {layer})")
        print(f"  4GB+  : {'enabled' if Config.STRING_SESSION else 'disabled'}")
        print(f"  {me.first_name} is online ⚡")
        print("─" * 50)

        for admin in Config.ADMIN:
            note = (
                f"<b>⚡ {me.first_name} is online!</b>\n\n"
                f"<b>🔖 Version :</b> <code>{VERSION}</code>\n"
                f"<b>📦 4GB+    :</b> <code>{'Enabled' if Config.STRING_SESSION else 'Disabled'}</code>"
            )
            try:
                await self.send_message(admin, note)
            except Exception:
                pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(pytz.timezone(Config.TIMEZONE))
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"<b>♻️ {me.mention} restarted!</b>\n\n"
                    f"<b>📅 Date :</b> <code>{curr.strftime('%d %B, %Y')}</code>\n"
                    f"<b>⏰ Time :</b> <code>{curr.strftime('%I:%M:%S %p')}</code>\n"
                    f"<b>🌐 Zone :</b> <code>{Config.TIMEZONE}</code>\n"
                    f"<b>🔖 Ver  :</b> <code>{VERSION}</code> · Pyrogram {__version__} (Layer {layer})",
                )
            except Exception:
                print("⚠️  Make the bot an admin in your LOG_CHANNEL.")

    async def stop(self, *args):
        for admin in Config.ADMIN:
            try:
                await self.send_message(admin, "<b>🛑 Trinity Renamer stopped.</b>")
            except Exception:
                pass
        print("Bot stopped.")
        await super().stop()


bot_instance = TrinityRenamerBot()


def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(app.start(), bot_instance.start())
        else:
            await bot_instance.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    loop.run_forever()


if __name__ == "__main__":
    warnings.filterwarnings("ignore", message="There is no current event loop")
    try:
        main()
    except errors.FloodWait as ft:
        print(f"FloodWait — sleeping {ft.value}s")
        asyncio.sleep(ft.value)
        main()
