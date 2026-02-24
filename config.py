import re
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv ()

API_ID =int (getenv ("API_ID","21457002"))
API_HASH =getenv ("API_HASH","6f9f6b8fb05ef1f4d9916e901f27bf52")

BOT_TOKEN =getenv ("BOT_TOKEN","8507183742:AAGJNPeHy0WOCB06et_5KCMx8ZOB-vALnYU")

_mongo_user =getenv ("MONGOUSER",getenv ("MONGO_INITDB_ROOT_USERNAME","mongo"))
_mongo_pass =getenv ("MONGOPASSWORD",getenv ("MONGO_INITDB_ROOT_PASSWORD","TyIYFavtqzNXyzLvFBSvjmUiFiDqdHak"))
_mongo_host =getenv ("MONGOHOST","mongodb.railway.internal")
_mongo_port =getenv ("MONGOPORT","27017")

if getenv ("MONGO_URL"):
    MONGO_DB_URI =getenv ("MONGO_URL")
elif getenv ("MONGO_DB_URI"):
    MONGO_DB_URI =getenv ("MONGO_DB_URI")
else :

    if _mongo_pass :
        MONGO_DB_URI =f"mongodb://{_mongo_user }:{_mongo_pass }@{_mongo_host }:{_mongo_port }/music?authSource=admin"
    else :
        MONGO_DB_URI =f"mongodb://{_mongo_host }:{_mongo_port }/music"

MONGO_DB_NAME =getenv ("MONGO_DB_NAME","music")

YTPROXY_URL =getenv ("YTPROXY_URL",None )
YOUTUBE_PROXY =getenv ("YOUTUBE_PROXY",None )

def _bool_env (var ,default =False ):
    val =getenv (var ,str (default ))
    return str (val ).lower ()in ("1","true","yes")

YOUTUBE_USE_PYTUBE =_bool_env ("YOUTUBE_USE_PYTUBE",True )

YOUTUBE_ENABLED =_bool_env ("YOUTUBE_ENABLED",True )

YOUTUBE_PROXY_LIST =[p .strip ()for p in getenv ("YOUTUBE_PROXY_LIST","").split (",")if p .strip ()]

YOUTUBE_INVIDIOUS_INSTANCES =[i .strip ()for i in getenv ("YOUTUBE_INVIDIOUS_INSTANCES","https://yewtu.be,https://invidious.snopyta.org,https://invidious.kavin.rocks,https://invidious.tiekoetter.com,https://invidious.flokinet.to,https://yewtu.cafe,https://nsxvn4w6i7o2rjgp.onion,https://invidio.us,https://inv.riverside.rocks,https://invidious.byt3.org,https://invidious.slipfox.xyz,https://invidious.xyz,https://invidious.private.coffee,https://yt.artemislena.eu,https://invidious.fdn.fr,https://iv.ggtyler.dev,https://invidious.sethforprivacy.com,https://vid.puffyan.us,https://invidious-us.kavin.rocks,https://youthefuck.com,https://inv.bp.projectsegfau.lt,https://invidious.web.id").split (",")if i .strip ()]

YT_API_KEY =getenv ("YT_API_KEY","AIzaSyAyFW-9snpxGwFa5cu-p81jjE8Fg1h_6rk")
YOUTUBE_FALLBACK_SEARCH_LIMIT =int (getenv ("YOUTUBE_FALLBACK_SEARCH_LIMIT","5"))

DURATION_LIMIT_MIN =int (getenv ("DURATION_LIMIT",300 ))

LOGGER_ID =int (getenv ("LOGGER_ID","-1003646583089"))

OWNER_ID =int (getenv ("OWNER_ID","8557740388"))

AUTO_LEAVING_ASSISTANT =bool (getenv ("AUTO_LEAVING_ASSISTANT",False ))
ASSISTANT_LEAVE_TIME =int (getenv ("ASSISTANT_LEAVE_TIME",5400 ))

SPOTIFY_CLIENT_ID =getenv ("SPOTIFY_CLIENT_ID","1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET =getenv ("SPOTIFY_CLIENT_SECRET","709e1a2969664491b58200860623ef19")

PLAYLIST_FETCH_LIMIT =int (getenv ("PLAYLIST_FETCH_LIMIT",25 ))

TG_AUDIO_FILESIZE_LIMIT =int (getenv ("TG_AUDIO_FILESIZE_LIMIT",2 *1024 **3 ))
TG_VIDEO_FILESIZE_LIMIT =int (getenv ("TG_VIDEO_FILESIZE_LIMIT",2 *1024 **3 ))

PRIVATE_BOT_MODE_MEM =int (getenv ("PRIVATE_BOT_MODE_MEM",1 ))

CACHE_DURATION =int (getenv ("CACHE_DURATION","86400"))
CACHE_SLEEP =int (getenv ("CACHE_SLEEP","3600"))

STRING1 =getenv ("STRING_SESSION","AgFHaGoAVHa9Q15n2IaDNygtcPNPGHBussJjD7XfLJjKV1b-sDdVsBUJ5SAPUoGx6LSJ9EugCx3uTvPNLoosVuiSDI8viGjPOp1sdN30utmvnCzyKIX0IEtPMzx38jkA3fBEWkfwJ-XziR9nkLUzXvn1I3SIVPj6FVPUSq3SW0qO-0nAPO0kIWZRzFTtRLldjDo67E2S3ge1V_dde4upSgJS6MrsWEY0FL6MYCpObLMZ__SGuY5Qq4exbJMGaCpwS5u_DtTuX-LOxMfte5JXR9FOGY3KxBD9UkRIUraQp2VD0PMacbj8bFNApDXwLr9FEjjch8xOydYQfRfL5CIws4dmsu8wxgAAAAH6ziPRAA")
STRING2 =getenv ("STRING_SESSION2",None )
STRING3 =getenv ("STRING_SESSION3",None )
STRING4 =getenv ("STRING_SESSION4",None )
STRING5 =getenv ("STRING_SESSION5",None )

BANNED_USERS =filters .user ()
adminlist ={}
lyrical ={}
votemode ={}
autoclean =[]
confirmer ={}
file_cache :dict [str ,float ]={}

START_IMG_URL =[
"https://image2url.com/r2/default/images/1769269338835-d5ce1f25-55d6-45fc-b9ad-c04ae647827e.jpg",
"https://image2url.com/r2/default/images/1769269355185-77c5d002-ce9a-47ce-aba1-d1b033e60472.jpg",
"https://image2url.com/r2/default/images/1769269377267-3084111d-b3fe-4e5e-be58-418b26f25c4d.jpg",
"https://image2url.com/r2/default/images/1769269399286-a06b9ba6-3f29-47a5-9a32-9f0c3e0a905c.jpg",
"https://image2url.com/r2/default/images/1769269443873-5d739aec-a837-45be-aa83-409ae4259c5e.jpg",
"https://image2url.com/r2/default/images/1769269553883-e7fa9182-2d84-4961-a2bf-4ae63e810b1e.jpg"
]

PING_IMG_URL =getenv (
"PING_IMG_URL","https://image2url.com/r2/default/images/1768792821746-ad62ab76-1fdc-45d7-8b5e-a5343577d6bb.jpg"
)
PLAYLIST_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
TELEGRAM_AUDIO_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
TELEGRAM_VIDEO_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
STREAM_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
SOUNCLOUD_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
YOUTUBE_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
SPOTIFY_ARTIST_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
SPOTIFY_ALBUM_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"
SPOTIFY_PLAYLIST_IMG_URL ="https://image2url.com/r2/default/images/1768793789039-2d4017a9-b0a3-43ec-837c-82855012c3fb.jpg"

DEFAULT_THUMB =START_IMG_URL [0 ]

def time_to_seconds (time ):
    stringt =str (time )
    return sum (int (x )*60 **i for i ,x in enumerate (reversed (stringt .split (":"))))

DURATION_LIMIT =int (time_to_seconds (f"{DURATION_LIMIT_MIN }:360"))