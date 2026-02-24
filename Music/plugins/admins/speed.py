from pyrogram import filters
from pyrogram.types import Message

from Music import app
from Music.core.call import Anony
from Music.misc import db
from Music.utils.decorators import AdminRightsCheck
from Music.utils.inline import close_markup
from config import BANNED_USERS
from strings import get_string

checker = []


@app.on_message(filters.command(['speed', 'playback', 'cspeed', 'cplayback']) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def speed_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_['admin_28'])

    speed = message.text.split(None, 1)[1].strip()
    if speed not in ('0.5', '0.75', '1.0', '1.5', '2.0'):
        return await message.reply_text(_['admin_28'])

    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_['queue_2'])

    duration_seconds = int(playing[0].get('seconds', 0))
    if duration_seconds == 0:
        return await message.reply_text(_['admin_27'])

    file_path = playing[0].get('file')
    if not file_path or 'downloads' not in file_path:
        return await message.reply_text(_['admin_27'])

    checkspeed = playing[0].get('speed')
    if checkspeed and str(checkspeed) == str(speed):
        if str(speed) == '1.0':
            return await message.reply_text(_['admin_29'])
    elif str(speed) == '1.0':
        return await message.reply_text(_['admin_29'])

    if chat_id in checker:
        return await message.reply_text(_['admin_30'])
    else:
        checker.append(chat_id)

    try:
        await message.reply_text(_['admin_31'])
    except Exception:
        pass

    mystic = await message.reply_text(text=_['admin_32'].format(message.from_user.mention))
    try:
        await Anony.speedup_stream(chat_id, file_path, speed, playing)
    except Exception:
        if chat_id in checker:
            checker.remove(chat_id)
        return await mystic.edit_text(_['admin_33'], reply_markup=close_markup(_))

    if chat_id in checker:
        checker.remove(chat_id)
    await mystic.edit_text(text=_['admin_34'].format(speed, message.from_user.mention), reply_markup=close_markup(_))
