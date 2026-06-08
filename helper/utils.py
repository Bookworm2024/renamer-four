# extra imports
import math, time, re, datetime, pytz, os
from config import Config, Txt, VERSION

# pyrogram imports
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# How often (seconds) the progress message is allowed to refresh.
# Time-throttled instead of per-chunk → far fewer edit calls → fewer flood-waits → faster transfers.
PROGRESS_REFRESH = 6.0


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start

    # Refresh only every PROGRESS_REFRESH seconds, or on the final chunk.
    last = getattr(message, "_trinity_last_edit", 0)
    if (now - last) < PROGRESS_REFRESH and current != total:
        return
    setattr(message, "_trinity_last_edit", now)

    percentage = current * 100 / total if total else 0
    speed = current / diff if diff > 0 else 0
    time_to_completion = round((total - current) / speed) * 1000 if speed > 0 else 0
    eta = TimeFormatter(milliseconds=time_to_completion)

    # Smooth 16-slot bar
    slots = 16
    filled = int(slots * percentage // 100)
    bar = "▰" * filled + "▱" * (slots - filled)

    text = Txt.PROGRESS_BAR.format(
        ud_type,
        bar,
        humanbytes(current),
        humanbytes(total),
        round(percentage, 1),
        humanbytes(speed),
        eta if eta else "—",
    )
    try:
        await message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖ Cancel", callback_data="close")]]
            ),
        )
    except Exception:
        pass


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    n = 0
    units = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}B"


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{days}d " if days else "")
        + (f"{hours}h " if hours else "")
        + (f"{minutes}m " if minutes else "")
        + (f"{seconds}s " if seconds else "")
    )
    return tmp.strip()


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


async def send_log(b, u):
    if Config.LOG_CHANNEL:
        curr = datetime.datetime.now(pytz.timezone(Config.TIMEZONE))
        log_message = (
            "<b>#NewUser · Trinity Renamer</b>\n\n"
            f"<b>👤 User :</b> {u.mention}\n"
            f"<b>🆔 ID   :</b> <code>{u.id}</code>\n"
            f"<b>🔗 UN   :</b> @{u.username}\n\n"
            f"<b>📅 Date :</b> {curr.strftime('%d %B, %Y')}\n"
            f"<b>⏰ Time :</b> {curr.strftime('%I:%M:%S %p')}\n\n"
            f"<b>🤖 Bot  :</b> {b.mention}"
        )
        try:
            await b.send_message(Config.LOG_CHANNEL, log_message)
        except Exception:
            pass


async def get_seconds_first(time_string):
    conversion_factors = {
        's': 1, 'min': 60, 'hour': 3600,
        'day': 86400, 'month': 86400 * 30, 'year': 86400 * 365,
    }
    parts = time_string.split()
    total_seconds = 0
    for i in range(0, len(parts), 2):
        value = int(parts[i])
        unit = parts[i + 1].rstrip('s')
        total_seconds += value * conversion_factors.get(unit, 0)
    return total_seconds


async def get_seconds(time_string):
    conversion_factors = {
        's': 1, 'min': 60, 'hour': 3600,
        'day': 86400, 'month': 86400 * 30, 'year': 86400 * 365,
    }
    total_seconds = 0
    pattern = r'(\d+)\s*(\w+)'
    matches = re.findall(pattern, time_string)
    for value, unit in matches:
        total_seconds += int(value) * conversion_factors.get(unit, 0)
    return total_seconds


def add_prefix_suffix(input_string, prefix='', suffix=''):
    pattern = r'(?P<filename>.*?)(\.\w+)?$'
    match = re.search(pattern, input_string)
    if match:
        filename = match.group('filename')
        extension = match.group(2) or ''
        prefix_str = f"{prefix} " if prefix else ""
        suffix_str = f" {suffix}" if suffix else ""
        return f"{prefix_str}{filename}{suffix_str}{extension}"
    return input_string


async def remove_path(*paths):
    for path in paths:
        if path and os.path.lexists(path):
            try:
                os.remove(path)
            except Exception:
                pass


def metadata_text(metadata_text):
    author = title = video_title = audio_title = subtitle_title = None
    flags = [i.strip() for i in metadata_text.split('--')]
    for f in flags:
        if "change-author" in f:
            author = f[len("change-author"):].strip()
        if "change-title" in f:
            title = f[len("change-title"):].strip()
        if "change-video-title" in f:
            video_title = f[len("change-video-title"):].strip()
        if "change-audio-title" in f:
            audio_title = f[len("change-audio-title"):].strip()
        if "change-subtitle-title" in f:
            subtitle_title = f[len("change-subtitle-title"):].strip()
    return author, title, video_title, audio_title, subtitle_title
