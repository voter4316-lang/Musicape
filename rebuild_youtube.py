import os
import re

filepath =r'Music\platforms\Youtube.py'
with open (filepath ,'r',encoding ='utf-8')as f :
    content =f .read ()

audio_dl_pattern =r'async def audio_dl\s*\([^)]*\):\s*try:\s*filepath\s*=.*?(?=\s+async def video_dl)'

new_audio_dl ='''async def audio_dl (vid_id ,search_title :str =None ,_recursion_depth :int =0 ):
            try :
                filepath =os .path .join ('downloads',f'{vid_id }.mp3')
                os .makedirs (os .path .dirname (filepath ),exist_ok =True )
                if os .path .exists (filepath ):
                    return filepath

                logger .info (f'🎵 [FALLBACK-FIRST] Downloading audio for {vid_id }...')

                # 1. TRY INVIDIOUS (Most reliable fallback)
                if YOUTUBE_INVIDIOUS_INSTANCES :
                    logger .info (f'   → Trying Invidious instances...')
                    for _ in range (len (YOUTUBE_INVIDIOUS_INSTANCES )):
                        inst =self ._next_invidious ()
                        if not inst :
                            break
                        try :
                            invid_url =f"{inst .rstrip ('/')}/watch?v={vid_id }"
                            ydl_fallback ={'format':'bestaudio/best','outtmpl':os .path .join ('downloads',f'{vid_id }'),'postprocessors':[{'key':'FFmpegExtractAudio','preferredcodec':'mp3','preferredquality':'320'}],'quiet':True ,'no_warnings':True ,'retries':5 ,'fragment_retries':5 ,'skip_unavailable_fragments':True ,'js_runtimes':{'node':{'interpreter':'node'}}}
                            if YOUTUBE_PROXY :
                                ydl_fallback ['proxy']=YOUTUBE_PROXY
                            loop =asyncio .get_running_loop ()

                            old_stderr =sys .stderr
                            old_stdout =sys .stdout
                            sys .stderr =io .StringIO ()
                            sys .stdout =io .StringIO ()
                            try :
                                with ThreadPoolExecutor (max_workers =2 )as executor :
                                    await loop .run_in_executor (executor ,lambda :create_ydl(ydl_fallback ).download ([invid_url ]))
                            finally :
                                sys .stderr =old_stderr
                                sys .stdout =old_stdout
                            if os .path .exists (filepath ):
                                logger .info (f'✅ Invidious succeeded for {vid_id }')
                                _log_method(vid_id, 'invidious', self)
                                return filepath
                        except Exception as inv_e :
                            logger .debug (f'Invidious {inst}: {str(inv_e)[:80]}')
                            continue

                # 2. TRY PYTUBE (Reliable fallback)
                if YOUTUBE_USE_PYTUBE :
                    logger .info (f'   → Trying pytube...')
                    try :
                        from pytube import YouTube as PyTube
                        yt_obj =PyTube (f'https://www.youtube.com/watch?v={vid_id }')
                        stream =yt_obj .streams .filter (only_audio =True ).order_by ('abr').desc ().first ()
                        if stream :
                            out =stream .download (output_path ='downloads',filename =f'{vid_id }_pytube')
                            mp3path =filepath
                            try :
                                subprocess .run (['ffmpeg','-y','-i',out ,'-vn','-ab','192k',mp3path ],check =True )
                                if os .path .exists (mp3path ):
                                    logger .info (f'✅ pytube succeeded for {vid_id }')
                                    _log_method(vid_id, 'pytube', self)
                                    if os .path .exists (out )and out != mp3path :
                                        os .remove (out )
                                    return mp3path
                            except Exception as conv_e :
                                logger .debug (f'pytube conversion failed: {str(conv_e)[:80]}')
                    except Exception as py_e :
                        logger .debug (f'pytube failed: {str(py_e)[:80]}')

                # 3. TRY EXTERNAL MP3 SERVICES (Last resort)
                logger .info (f'   → Trying external MP3 extraction services...')
                try :
                    ext_result =await try_external_mp3_extraction (f'https://www.youtube.com/watch?v={vid_id }',filepath )
                    if ext_result and os .path .exists (filepath ):
                        logger .info (f'✅ External service succeeded for {vid_id }')
                        _log_method(vid_id, 'external_service', self)
                        return filepath
                except Exception as ext_e :
                    logger .debug (f'External services failed: {str(ext_e)[:80]}')

                logger .error (f'❌ All fallback methods exhausted for {vid_id }')
                return None
            except Exception as e :
                logger .error (f'audio_dl error for {vid_id }: {str (e )}')
                return None

        '''

match =re .search (r'(        async def audio_dl.*?)(\n        async def video_dl)',content ,re .DOTALL )
if match :
    print (f"Found audio_dl function (length: {len (match .group (1 ))} chars)")
    old_audio_dl =match .group (1 )
    content =content .replace (old_audio_dl ,new_audio_dl .rstrip ()+'\n')
    print ("✅ Replaced audio_dl function")
else :
    print ("❌ Could not find audio_dl function")

new_video_dl ='''async def video_dl (vid_id ,search_title :str =None ,_recursion_depth :int =0 ):
            try :
                filepath =os .path .join ('downloads',f'{vid_id }.mp4')
                os .makedirs (os .path .dirname (filepath ),exist_ok =True )
                if os .path .exists (filepath ):
                    return filepath

                logger .info (f'🎬 [FALLBACK-FIRST] Downloading video for {vid_id }...')

                # 1. TRY INVIDIOUS
                if YOUTUBE_INVIDIOUS_INSTANCES :
                    logger .info (f'   → Trying Invidious instances...')
                    for _ in range (len (YOUTUBE_INVIDIOUS_INSTANCES )):
                        inst =self ._next_invidious ()
                        if not inst :
                            break
                        try :
                            invid_url =f"{inst .rstrip ('/')}/watch?v={vid_id }"
                            ydl_fallback ={'format':'best','outtmpl':os .path .join ('downloads',f'{vid_id }'),'quiet':True ,'no_warnings':True ,'retries':3 ,'fragment_retries':3 ,'skip_unavailable_fragments':True ,'js_runtimes':{'node':{'interpreter':'node'}}}
                            if YOUTUBE_PROXY :
                                ydl_fallback ['proxy']=YOUTUBE_PROXY
                            loop =asyncio .get_running_loop ()

                            old_stderr =sys .stderr
                            old_stdout =sys .stdout
                            sys .stderr =io .StringIO ()
                            sys .stdout =io .StringIO ()
                            try :
                                with ThreadPoolExecutor (max_workers =2 )as executor :
                                    await loop .run_in_executor (executor ,lambda :create_ydl(ydl_fallback ).download ([invid_url ]))
                            finally :
                                sys .stderr =old_stderr
                                sys .stdout =old_stdout
                            if os .path .exists (filepath ):
                                logger .info (f'✅ Invidious video succeeded for {vid_id }')
                                _log_method(vid_id, 'invidious_video', self)
                                return filepath
                        except Exception as inv_e :
                            logger .debug (f'Invidious video {inst}: {str(inv_e)[:80]}')
                            continue

                # 2. TRY EXTERNAL SERVICES
                logger .info (f'   → Trying external video extraction services...')
                try :
                    ext_result =await try_external_mp3_extraction (f'https://www.youtube.com/watch?v={vid_id }',filepath )
                    if ext_result and os .path .exists (filepath ):
                        logger .info (f'✅ External service succeeded for {vid_id }')
                        _log_method(vid_id, 'external_service_video', self)
                        return filepath
                except Exception as ext_e :
                    logger .debug (f'External services failed: {str(ext_e)[:80]}')

                logger .error (f'❌ All video fallback methods exhausted for {vid_id }')
                return None
            except Exception as e :
                logger .error (f'video_dl error for {vid_id }: {str (e )}')
                return None

        '''

match2 =re .search (r'(        async def video_dl.*?)(\n        async def song)',content ,re .DOTALL )
if match2 :
    print (f"Found video_dl function (length: {len (match2 .group (1 ))} chars)")
    old_video_dl =match2 .group (1 )
    content =content .replace (old_video_dl ,new_video_dl .rstrip ()+'\n')
    print ("✅ Replaced video_dl function")
else :
    print ("❌ Could not find video_dl function")

with open (filepath ,'w',encoding ='utf-8')as f :
    f .write (content )

print (f"✅ Successfully rewrote {filepath }")
print (f"   File size: {len (content )} bytes")