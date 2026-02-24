import asyncio
import os
import shutil
import socket
from datetime import datetime
import urllib3
from pyrogram import filters
import config
from Music import app
from Music .misc import SUDOERS
from Music .utils .database import get_active_chats ,remove_active_chat ,remove_active_video_chat
from Music .utils .decorators .language import language
from Music .utils .pastebin import AnonyBin
urllib3 .disable_warnings (urllib3 .exceptions .InsecureRequestWarning )

@app .on_message (filters .command (['logs'])&SUDOERS )
@language
async def log_ (client ,message ,_ ):
    try :
        await message .reply_document (document ='log.txt')
    except :
        await message .reply_text (_ ['server_1'])

@app .on_message (filters .command (['restart'])&SUDOERS )
async def restart_ (_ ,message ):
    response =await message .reply_text ('ʀᴇsᴛᴀʀᴛɪɴɢ...')
    ac_chats =await get_active_chats ()
    for x in ac_chats :
        try :
            await app .send_message (chat_id =int (x ),text =f'{app .mention } ɪs ʀᴇsᴛᴀʀᴛɪɴɢ...\n\nʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 15-20 sᴇᴄᴏɴᴅs.')
            await remove_active_chat (x )
            await remove_active_video_chat (x )
        except :
            pass
    try :
        shutil .rmtree ('raw_files')
        shutil .rmtree ('cache')
    except :
        pass
    await response .edit_text ('» ʀᴇsᴛᴀʀᴛ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ, ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ sᴇᴄᴏɴᴅs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ sᴛᴀʀᴛs...')
    os .system (f'kill -9 {os .getpid ()} && bash start')