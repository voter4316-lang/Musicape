
import asyncio
import yt_dlp
from concurrent .futures import ThreadPoolExecutor
from Music .logging import LOGGER

logger =LOGGER (__name__ )

class VideosSearch :

    def __init__ (self ,query :str ,limit :int =1 ):
        self .query =query
        self .limit =limit
        self ._results =None

    async def next (self ):

        try :
            loop =asyncio .get_event_loop ()
            with ThreadPoolExecutor ()as executor :
                def _search ():
                    ydl_opts ={
                    'quiet':False ,
                    'no_warnings':False ,
                    'default_search':'ytsearch',
                    'extract_flat':True ,
                    }
                    with yt_dlp .YoutubeDL (ydl_opts )as ydl :
                        results =ydl .extract_info (f'ytsearch{self .limit }:{self .query }',download =False )
                        return results .get ('entries',[])

                entries =await loop .run_in_executor (None ,_search )

            formatted_results =[]
            for entry in entries :
                formatted_result ={
                'id':entry .get ('id',''),
                'title':entry .get ('title','Unknown'),
                'link':f"https://www.youtube.com/watch?v={entry .get ('id','')}",
                'channel':{
                'name':entry .get ('uploader','Unknown'),
                'link':entry .get ('channel_url','')
                },
                'duration':self ._format_duration (entry .get ('duration',0 )),
                'thumbnails':[{'url':entry .get ('thumbnail','')}]if entry .get ('thumbnail')else [],
                'viewCount':{'short':entry .get ('view_count',0 )},
                'publishedTime':entry .get ('upload_date','Unknown'),
                }
                formatted_results .append (formatted_result )

            self ._results =formatted_results
            return {'result':formatted_results }

        except Exception as e :
            logger .error (f'YouTube search error: {type (e ).__name__ }: {e }')
            import traceback
            logger .error (f'Traceback: {traceback .format_exc ()}')
            return {'result':[]}

    @staticmethod
    def _format_duration (seconds ):

        if not seconds :
            return '0:00'
        try :
            seconds =int (seconds )
        except (ValueError ,TypeError ):
            return '0:00'
        mins =seconds //60
        secs =seconds %60
        formatted =f'{mins }:{secs :02d}'
        return formatted

class CustomSearch (VideosSearch ):

    pass