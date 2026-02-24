import time
import re
import random
import asyncio
import io
import sys
from concurrent .futures import ThreadPoolExecutor
from pyrogram import filters
from pyrogram .enums import ChatType
from pyrogram .types import InlineKeyboardButton ,InlineKeyboardMarkup ,Message
from pyrogram .errors .exceptions .not_acceptable_406 import ChannelPrivate
from pyrogram .errors .exceptions .flood_420 import SlowmodeWait
from Music .utils .youtube_search import VideosSearch
import config
import yt_dlp
from Music import app, LOGGER
from Music .misc import _boot_ ,SUDOERS
from Music .utils .database import add_served_chat ,add_served_user ,blacklisted_chats ,get_lang ,is_banned_user ,blacklist_chat
from Music .utils .decorators .language import LanguageStart
from Music .utils .formatters import get_readable_time
from Music .utils .inline import help_pannel ,private_panel ,start_panel
from config import BANNED_USERS ,LOGGER_ID
from strings import get_string

def _extract_info_suppressed (url ):

    old_stdout =sys .stdout
    old_stderr =sys .stderr
    sys .stdout =io .StringIO ()
    sys .stderr =io .StringIO ()
    try :
        ydl_opts ={
        'quiet':True ,
        'no_warnings':True ,
        'skip_download':True ,
        'socket_timeout':15 ,
        }
        with yt_dlp .YoutubeDL (ydl_opts )as ydl :
            info =ydl .extract_info (url ,download =False )
            return info
    except Exception as e :
        return None
    finally :
        sys .stdout =old_stdout
        sys .stderr =old_stderr

def _format_views (views ):

    if not views :
        return "0"
    try :
        views_int =int (views )
        if views_int >=1000000 :
            return f"{views_int //1000000 }M"
        elif views_int >=1000 :
            return f"{views_int //1000 }K"
        else :
            return str (views_int )
    except (ValueError ,TypeError ):
        return str (views )

@app .on_message (filters .command (['start'])&filters .private &~BANNED_USERS )
@LanguageStart
async def start_pm (client ,message :Message ,_ ):
    await add_served_user (message .from_user .id )
    if len (message .text .split ())>1 :
        name =message .text .split (None ,1 )[1 ]
        if name [0 :4 ]=='help':
            is_sudo =message .from_user .id in SUDOERS
            keyboard =help_pannel (_ ,is_sudo )
            return await message .reply_photo (photo =random .choice (config .START_IMG_URL ),caption =_ ['help_1'],reply_markup =keyboard )
        if name [0 :3 ]=='inf':
            if name =='info_telegram':

                key =InlineKeyboardMarkup ([[InlineKeyboardButton (text ='⬇️ Download',callback_data =f"DownloadTelegramFile|{message .from_user .id }")]])
                await app .send_message (chat_id =message .chat .id ,text ='ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ/ᴠɪᴅᴇᴏ ɪɴғᴏʀᴍᴀᴛɪᴏɴ',reply_markup =key )
                try :
                    return await app .send_message (chat_id =config .LOGGER_ID ,text =f'{message .from_user .mention } ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛᴇʟᴇɢʀᴀᴍ ғɪʟᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message .from_user .id }</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message .from_user .username }')
                except ValueError :
                    pass
            m =await message .reply_text ('🔎')
            query =str (name ).replace ('info_','',1 )
            video_url =f'https://www.youtube.com/watch?v={query }'

            info =_extract_info_suppressed (video_url )

            if info :
                title =info .get ('title','Unknown')
                duration =info .get ('duration',0 )or 0
                duration_str =f"{int (duration //60 )}"
                views_count =info .get ('view_count',0 )or 0
                views =_format_views (views_count )

                upload_date =info .get ('upload_date','Unknown')
                published ='Unknown'
                if upload_date and upload_date !='Unknown':
                    try :
                        import datetime
                        dt =datetime .datetime .strptime (str (upload_date ),'%Y%m%d')
                        published =dt .strftime ('%Y-%m-%d')
                    except :
                        published =upload_date

                channel =info .get ('uploader')or info .get ('channel')or 'Unknown'
                channellink =f"https://www.youtube.com/@{channel .replace (' ','')}"if channel and channel !='Unknown'else ""

                thumbnails =info .get ('thumbnails',[])
                thumbnail =None
                if thumbnails and isinstance (thumbnails ,list )and len (thumbnails )>0 :
                    thumbnail =thumbnails [-1 ].get ('url')

                if not thumbnail :
                    try :
                        thumbnail =random .choice (config .START_IMG_URL )
                    except Exception :
                        thumbnail =None
            else :

                results =VideosSearch (video_url ,limit =1 )
                for result in (await results .next ())['result']:
                    title =result .get ('title','Unknown')
                    duration =result .get ('duration','Unknown')
                    duration_str =str (duration )if duration !='Unknown'else '0'

                    views_raw =result .get ('viewCount',{})
                    if isinstance (views_raw ,dict ):
                        views =views_raw .get ('short','0 views')
                    else :
                        views =_format_views (views_raw )

                    published =result .get ('publishedTime','Unknown')

                    channel =result .get ('channel',{}).get ('name','Unknown')
                    channellink =result .get ('channel',{}).get ('link','')

                    thumbs =result .get ('thumbnails')or []
                    thumbnail =None
                    if isinstance (thumbs ,list )and len (thumbs )>0 and thumbs [0 ].get ('url'):
                        thumbnail =thumbs [0 ]['url'].split ('?')[0 ]

                    if not thumbnail :
                        try :
                            thumbnail =random .choice (config .START_IMG_URL )
                        except Exception :
                            thumbnail =None

            searched_text =_ ['start_6'].format (title ,duration_str ,views ,published ,channellink ,channel ,app .mention )
            key =InlineKeyboardMarkup ([[InlineKeyboardButton (text =_ ['S_B_8'],url =video_url )]])
            await m .delete ()
            try :
                await app .send_photo (chat_id =message .chat .id ,photo =thumbnail ,caption =searched_text ,reply_markup =key )
            except Exception as photo_err :
                try :
                    await app .send_message (chat_id =message .chat .id ,text =searched_text ,reply_markup =key )
                except Exception as msg_err :
                    LOGGER (__name__ ).debug (f'Failed to send track info: {msg_err }')
            try :
                return await app .send_message (chat_id =config .LOGGER_ID ,text =f'{message .from_user .mention } ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message .from_user .id }</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message .from_user .username }')
            except ValueError :
                pass
    else :
        out =private_panel (_ )
        await message .reply_photo (photo =random .choice (config .START_IMG_URL ),caption =_ ['start_2'].format (message .from_user .mention ,app .mention ),reply_markup =InlineKeyboardMarkup (out ))
        try :
            return await app .send_message (chat_id =config .LOGGER_ID ,text =f'{message .from_user .mention } ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message .from_user .id }</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message .from_user .username }')
        except ValueError :
            pass

@app .on_message (filters .command (['start'])&filters .group &~BANNED_USERS )
@LanguageStart
async def start_gp (client ,message :Message ,_ ):
    out =start_panel (_ )
    uptime =int (time .time ()-_boot_ )
    try :
        await message .reply_photo (photo =random .choice (config .START_IMG_URL ),caption =_ ['start_1'].format (app .mention ,get_readable_time (uptime )),reply_markup =InlineKeyboardMarkup (out ))
        return await add_served_chat (message .chat .id )
    except ChannelPrivate :
        return
    except SlowmodeWait as e :
        asyncio .sleep (e .value )
        try :
            await message .reply_photo (photo =random .choice (config .START_IMG_URL ),caption =_ ['start_1'].format (app .mention ,get_readable_time (uptime )),reply_markup =InlineKeyboardMarkup (out ))
            return await add_served_chat (message .chat .id )
        except :
            return

@app .on_message (filters .new_chat_members ,group =-1 )
async def welcome (client ,message :Message ):
    for member in message .new_chat_members :
        try :
            language =await get_lang (message .chat .id )
            _ =get_string (language )
            if await is_banned_user (member .id ):
                try :
                    await message .chat .ban_member (member .id )
                except :
                    pass
            if member .id ==app .id :
                if message .chat .type !=ChatType .SUPERGROUP :
                    await message .reply_text (_ ['start_4'])
                    return await app .leave_chat (message .chat .id )
                if message .chat .id in await blacklisted_chats ():
                    await message .reply_text (_ ['start_5'].format (app .mention ,f'https://t.me/{app .username }?start=sudolist'),disable_web_page_preview =True )
                    return await app .leave_chat (message .chat .id )
                ch =await app .get_chat (message .chat .id )
                if ch .title and re .search ('[\\u1000-\\u109F]',ch .title )or (ch .description and re .search ('[\\u1000-\\u109F]',ch .description )):
                    await blacklist_chat (message .chat .id )
                    await message .reply_text ('This group is not allowed to play songs')
                    try :
                        await app .send_message (LOGGER_ID ,f'This group has been blacklisted automatically due to myanmar characters in the chat title, description or message \n Title:{ch .title } \n ID:{message .chat .id }')
                    except ValueError :
                        pass
                    return await app .leave_chat (message .chat .id )
                out =start_panel (_ )
                await message .reply_photo (photo =random .choice (config .START_IMG_URL ),caption =_ ['start_3'].format (message .from_user .first_name ,app .mention ,message .chat .title ,app .mention ),reply_markup =InlineKeyboardMarkup (out ))
                await add_served_chat (message .chat .id )
                await message .stop_propagation ()
        except Exception as ex :
            print (ex )
            try :
                await app .send_message (LOGGER_ID ,f'Error in welcome handler: {type (ex ).__name__ }: {ex }')
            except :
                pass