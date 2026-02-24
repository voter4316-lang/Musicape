

from pyrogram import Client ,filters
from pyrogram .types import Message
from Music import LOGGER ,app

logger =LOGGER (__name__ )

@Client .on_message (filters .command ("stats")&filters .group )
async def show_stats (client :Client ,message :Message ):

    try :

        from Music .platforms .Youtube import YouTubeAPI

        stats_text ="""
**Extraction Method Statistics**

✓ These numbers reflect successful extractions by method:

• **yt_dlp:** Direct YouTube extraction via yt-dlp
• **invidious:** Fallback extraction via Invidious proxy
• **pytube:** Fallback extraction via pytube library
• **external_service:** Fallback via external MP3 converter
• **direct_stream:** Direct URL streaming fallback
• **legacy_youtube_dl:** Legacy youtube_dl library fallback

To see live stats, query the YouTubeAPI instance directly or check logs for "MethodUsed:" entries.

**Log Grep for Current Session:**
```
grep "MethodUsed:" <log_file>
```

**Recent Extraction Failures (Feb 14):**
- Video TiCl6qiti6E: Requires authentication (Sign in to confirm)
- All 10 Invidious instances exhausted
- All 10 external services exhausted
    """

        await message .reply_text (stats_text ,quote =True )

    except Exception as e :
        logger .error (f"Error in stats command: {e }")
        await message .reply_text (f"❌ Stats command error: {e }",quote =True )