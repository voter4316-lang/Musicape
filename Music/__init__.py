from Music .core .bot import Anony
from Music .core .dir import dirr
from Music .core .userbot import Userbot
from Music .misc import dbb
from .logging import LOGGER
dirr ()
dbb ()
app =Anony ()
userbot =Userbot ()
from .platforms import *
Apple =AppleAPI ()
Carbon =CarbonAPI ()
SoundCloud =SoundAPI ()
Spotify =SpotifyAPI ()
Resso =RessoAPI ()
Telegram =TeleAPI ()
YouTube =YouTubeAPI ()