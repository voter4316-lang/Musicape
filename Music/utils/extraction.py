from pyrogram .enums import MessageEntityType
from pyrogram .types import Message ,User
from Music import app

async def extract_user (m :Message )->User :
    if m .reply_to_message :
        return m .reply_to_message .from_user
    if len (m .command )>1 :
        return await app .get_users (int (m .command [1 ])if m .command [1 ].isdecimal ()else m .command [1 ])
    if m .entities and len (m .entities )>(1 if m .text .startswith ('/')else 0 ):
        msg_entities =m .entities [1 ]if m .text .startswith ('/')else m .entities [0 ]
        if msg_entities .type ==MessageEntityType .TEXT_MENTION :
            return await app .get_users (msg_entities .user .id )
    raise ValueError ("No user specified")