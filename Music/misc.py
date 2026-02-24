import socket
import time
from pyrogram import filters
import config
from Music .core .mongo import mongodb
from .logging import LOGGER
SUDOERS =filters .user ()
_boot_ =time .time ()
XCB =['/','@','.','com',':','push','https','HEAD','master']

def dbb ():
    global db
    db ={}
    LOGGER (__name__ ).info (f'Local Database Initialized.')

async def sudo ():
    global SUDOERS
    SUDOERS .add (config .OWNER_ID )
    CON ='6281178648'
    try :
        sudoersdb =mongodb .sudoers
        sudoers =await sudoersdb .find_one ({'sudo':'sudo'})
        sudoers =[]if not sudoers else sudoers ['sudoers']
        if config .OWNER_ID not in sudoers :
            sudoers .append (config .OWNER_ID )
            await sudoersdb .update_one ({'sudo':'sudo'},{'$set':{'sudoers':sudoers }},upsert =True )
        if sudoers :
            for user_id in sudoers :
                SUDOERS .add (user_id )
    except Exception as e :
        LOGGER (__name__ ).warning (f'Failed to load sudoers from MongoDB: {e }')

        SUDOERS .add (config .OWNER_ID )
    LOGGER (__name__ ).info (f'Sudoers Loaded.')