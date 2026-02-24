from pyrogram import filters

BLOCKED_URL_PATTERNS =[
't.me/c/',
'youtu.be/',
'youtube.com/shorts/',
'bit.ly/',
'tinyurl.com/',
'ow.ly/',
'goo.gl/',
'short.link/',
'is.gd/',
'buff.ly/',
'adf.ly/',
'clck.ru/',
'lnk.co/',
'rb.gy/',
'lihi.io/',
'snip.ly/',
]

def no_preview_urls (flt ,client ,message ):

    if not message :
        return True

    if message .text :
        text =message .text .lower ()
        for pattern in BLOCKED_URL_PATTERNS :
            if pattern .lower ()in text :
                return False

    if message .caption :
        caption =message .caption .lower ()
        for pattern in BLOCKED_URL_PATTERNS :
            if pattern .lower ()in caption :
                return False

    return True

no_preview_filter =filters .create (no_preview_urls )